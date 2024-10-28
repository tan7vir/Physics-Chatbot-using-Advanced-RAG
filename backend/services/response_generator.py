import requests
from langchain.prompts import ChatPromptTemplate
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from config.config import (
    EMBEDDING_MODEL, 
    GENERATE_API_URL, 
    PDF_PATH, 
    VECTOR_DB_PATH, 
    SECONDARY_MODEL  # Import configuration constants
)

from services.pdf_chunk_service import get_chunk  
from services.vector_db_service import feed_vector_db  
from services.query_enhancement import query_enhncement
from utils.logger import setup_logger


# Set up the logger for the response generator
response_logger = setup_logger("response_generator")

# Define the prompt template for generating responses
PROMPT_TEMPLATE = """
You are a physics assistant for 9-10 grade students, providing clear, concise, and age-appropriate explanations based on the following context:

**Context:**
{context}
**Answer the following question:**
**Question:**
{question}

**Instructions:**
1. 📘 **For factual questions**: Provide a direct answer, possibly with a brief explanation if necessary. Keep it concise. Example: "The boiling point of water is 100°C, which is when water turns to vapor."
2. 📖 **For elaborate questions**: Offer a detailed explanation with an example. Encourage further thinking by posing a follow-up question. Example: "Energy is conserved in isolated systems. Think about how this applies when you throw a ball into the air."
3. 🧮 **For mathematical questions**: Start with the necessary theories, then provide a step-by-step solution using LaTeX for clarity, and conclude with the final answer neatly formatted. Example: "To find the force, use F=ma. For a mass of 10 kg and acceleration 5 m/s², F = 50 N."

🚀 **Keep it fun and engaging!** Use emojis to lighten the tone and enhance readability. Encourage curiosity and exploration to make learning enjoyable.
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
    enhanced_questions = query_enhncement(data.get('prompt'))

    # Loop through each enhanced question to perform similarity searches
    for question in enhanced_questions:
        result = collection.similarity_search_with_score(question, k=1)
        response_logger.info(f"Similarity search done for question: {question}")

        # Collect results for each question into context_texts
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in result])
        context_texts.append(context_text)

    # Join all context texts into a single string
    context_text = "\n\n---\n\n".join(context_texts)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Format the prompt with context and the user's question
    prompt = prompt_template.format(context=context_text, question=data.get('prompt'))

    # For debugging purposes
    print(prompt)

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
