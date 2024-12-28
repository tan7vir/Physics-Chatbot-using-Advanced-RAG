import requests
from langchain.prompts import ChatPromptTemplate
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_chroma import Chroma
# from config.config import (
#     EMBEDDING_MODEL, 
#     GENERATE_API_URL, 
#     PDF_PATH, 
#     VECTOR_DB_PATH, 
#     SUMMARY_MODEL,
#     SECONDARY_MODEL  # Import configuration constants
# )

EMBEDDING_MODEL = "bge-large:335m"  # Use this variable for your embedding model # Embedding Model
PDF_PATH = "../Data/PhysicsBook.pdf"
GENERATE_API_URL = "http://localhost:11434/api/generate"  # URL for the response generation API
# GENERATE_API_URL = "http://127.0.0.1:11434/api/generate"  # URL for the response generation API
VECTOR_DB_PATH = "../Data/vectorDB"
SECONDARY_MODEL = "qwen2.5:3b"
SUMMARY_MODEL = "qwen2.5:3b"

PROMPT_TEMPLATE = """

Question: {question}
---

Instructions:
1. Determine the type of the question:
   - "factual" for questions based on facts and direct answers.
   - "elaborate" for questions that require explanation or detailed information with math.
   - "math" for questions that need step by step solution by doing math and calculations.

2. Assess the necessity of the context for answering the question:
   - "yes" if the previous summary or context is needed to provide an accurate answer.
   - "no" if the answer to the question can be provided without referring back to any previous context.

Response Format:
- Provide the assessment in the following format: ("type of question", "need for context"), e.g., ("factual", "yes").

Example:
Question: What is the capital of France?
Response: ("factual", "no")

Example with Context:
Question: How does this event relate to what we discussed last week about World War II?
Response: ("elaborate", "yes")
"""

def get_question_type (question):
    
    
    prompt = PROMPT_TEMPLATE.format(question=question)

    payload = {
        "model": SUMMARY_MODEL,
        "prompt": prompt,
        "stream": False
    }
    # Send a POST request to generate the response
    response = requests.post(GENERATE_API_URL, json=payload)  # Use the config constant

    if response.status_code == 200:
            response_data = response.json()
            summary_temp = response_data.get('response', '').strip() 

            print (summary_temp)
    return {
        "question": question,
        "type": summary_temp
    }

# For debugging purposes
if __name__ == "__main__":
    import sys
    question = "what is the equation of centrifugal force?"
    result = get_question_type(question)
    # print(result)