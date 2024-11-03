import requests
from langchain.prompts import ChatPromptTemplate
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from config.config import (
    EMBEDDING_MODEL, 
    GENERATE_API_URL, 
    PDF_PATH, 
    VECTOR_DB_PATH, 
    SUMMARY_MODEL,
    SECONDARY_MODEL  # Import configuration constants
)

from services.pdf_chunk_service import get_chunk  
from services.vector_db_service import feed_vector_db  
from services.query_enhancement import query_enhncement
from utils.logger import setup_logger


# Set up the logger for the response generator
response_logger = setup_logger("response_generator")

summary = ""

# Define the prompt template for generating responses
PROMPT_TEMPLATE = """
You are a physics assistant for 9-10 grade students, tasked with providing clear, concise, and age-appropriate explanations. Use the summary and context from previous conversations selectively to ensure your responses build upon relevant previously discussed knowledge only:

**Summary of Previous Conversation:**  
{summary} *(Refer back to this selectively for continuity when it directly relates to the new question. Avoid incorporating detailed examples or content from the summary that does not directly relate to the current question.)*

**Context:**  
{context} *(Use this for additional details only if they directly support answering the current question. Avoid straying into tangential areas unless the question explicitly requires such details.)*

**Question:**  
{question}

**Instructions:**

1. 🗨️ **For general inquiries or greetings**: Provide a friendly and concise response, quickly refocusing on the subject matter. For example, "Hello! Let’s get back to exploring physics. What would you like to learn today?"
2. 📘 **For factual questions**: Provide a direct and succinct answer immediately related to the question. Follow with a brief explanation if necessary but keep it focused. For example, "Physics primarily concerns the study of matter, energy, and the fundamental forces of nature. It seeks to understand how these elements interact and influence the universe."
3. 📖 **For elaborate explanations**: Give a detailed response but ensure all parts of the explanation are directly relevant to the question asked. Avoid using complex examples from unrelated contexts. Encourage deeper thinking with a directly related follow-up question.
4. 🧮 **For mathematical questions**: Start with the necessary theories directly related to the question. Provide a step-by-step solution using LaTeX, ensuring the explanation is pertinent to the specific question asked, without diversion.

🚀 **Engagement Tips:**
- Use emojis to maintain an engaging tone.
- Keep explanations relevant and concise.
- Encourage questions but ensure they are targeted to keep the discussion focused and relevant.
"""

SUMMARY_TEMPLATE = """Generate a concise summary of this conversation with only the main question and essential points from the response in a single, compact sentence. Keep the summary short, suitable for adding to an ongoing chat history.

User's Question:
{user_context}

Model's Response:
{response_context}

response will be like: 'User asked: summary of the question. Response: concise summary of the response.'
"""


def load_books():
    """Load and chunk the PDF pages, then feed them to the vector database."""
    chunked_pages = get_chunk(PDF_PATH)  # Use the config constant
    print("<<-- Pages chunked -->>")
    
    # Feed chunked pages into the vector database
    feed_vector_db(chunked_pages)
    print("<<-- Pages fed to vector db -->>")

def get_response(data: dict) -> dict:
    """Generate a response based on the user's prompt."""

    # Load the books (optional; uncomment if you want to load books every time)
    # load_books()
    global summary
    emb_fn = OllamaEmbeddings(model=EMBEDDING_MODEL)  # Use the config constant
    collection_name = "PhysicsBook"

    # Prepare the vector database
    collection = Chroma(
        collection_name=collection_name,
        embedding_function=emb_fn,
        persist_directory=VECTOR_DB_PATH,  # Use the config constant
    )

    context_texts = []  # Initialize a list to hold context texts

    # Perform initial similarity search for context
    temp_result = collection.similarity_search_with_score(data.get('prompt'), k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in temp_result])
    context_texts.append(context_text)

    # Enhance the original question
    enhanced_questions = query_enhncement(data.get('prompt'), context_texts)

    # Loop through each enhanced question to perform similarity searches
    for question in enhanced_questions:
        result = collection.similarity_search_with_score(question, k=1)
        response_logger.info(f"Similarity search done for question: {question}")

        # Collect results for each question into context_texts
        context_text = "\n---\n".join([doc.page_content for doc, _score in result])
        context_texts.append(context_text)

    # Join all context texts into a single string
    context_text = "\n\n---\n\n".join(context_texts)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Format the prompt with context and the user's question
    prompt = PROMPT_TEMPLATE.format(context=context_text, question=data.get('prompt'), summary = summary)

    # For debugging purposes
    # print(prompt)

    # Prepare the data payload with the user's prompt
    payload = {
        "model": data.get('model'),
        "prompt": prompt,
        "stream": False
    }
    # Send a POST request to generate the response
    response = requests.post(GENERATE_API_URL, json=payload)  # Use the config constant
    response_logger.info("Response generated")

    # Collect sources from the similarity search result
    sources = [doc.metadata.get("id", None) for doc, _score in result]

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        response_text = response_data.get('response', '').strip()  # Clean the response text

        # For Summary
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = SUMMARY_TEMPLATE.format(user_context=data.get('prompt'), response_context=response_text)

        payload = {
            "model": SUMMARY_MODEL,   # SECONDARY_MODEL
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(GENERATE_API_URL, json=payload)

        if response.status_code == 200:
              response_data = response.json()
              summary_temp = response_data.get('response', '').strip() 

              summary += summary_temp + "\n"
        return {
            "response": response_text,
            "sources": sources
        }
    else:
        return {"response": "Oops! Something went wrong!"}

if __name__ == "__main__":
    # Create a data object with 'prompt' and 'model'
    data = {
        "prompt": "who is bose?",
        "model": "gemma2:2b"
    }

    # Call the get_response function with the data object
    response = get_response(data)
    print(response)  # Print the final response for verification
