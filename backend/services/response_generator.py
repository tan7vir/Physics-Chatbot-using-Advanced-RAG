# response_generator.py

import requests
from langchain.prompts import ChatPromptTemplate
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from config.config import EMBEDDING_MODEL, GENERATE_API_URL, PDF_PATH, VECTOR_DB_PATH  # Import config

from services.pdf_chunk_service import get_chunk  
from services.vector_db_service import feed_vector_db  
from utils.logger import setup_logger

response_logger = setup_logger("response_generator")

# Define the prompt template for generating responses
PROMPT_TEMPLATE = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    Please do proper formatting and grammar and If the prompt is empty answer like normal. don't tell according to your 
    knowledge or something like that. sometimes tell according to your book.
"""

def load_books():
    """Load and chunk the PDF pages, then feed them to the vector database."""
    chunked_pages = get_chunk(PDF_PATH)  # Use the config constant
    print("<<--Pages chunked-->>")
    feed_vector_db(chunked_pages)
    print("<<--Pages fed to vector db-->>")

def get_response(data: object) -> dict:
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

    # Perform a similarity search
    result = collection.similarity_search_with_score(data.get('prompt'), k=5)
    response_logger.info("Similarity search done")

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in result])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=data.get('prompt'))

    # Prepare the data payload with the user's prompt
    payload = {
        "model": data.get('model'),
        "prompt": prompt,
        "stream": False
    }

    # Send a POST request to generate the response
    response = requests.post(GENERATE_API_URL, json=payload)  # Use the config constant
    response_logger.info("Response generated")
    sources = [doc.metadata.get("id", None) for doc, _score in result]

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        response_text = response_data.get('response', '').replace('\n\n', ' ').replace('\n', ' ').strip()

        return {
            "response": response_text,
            "sources": sources
        }
    else:
        return {"response": "Oops! Something went wrong!"}
