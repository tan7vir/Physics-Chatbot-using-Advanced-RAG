# feed_vectordb.py

import chromadb
from langchain.schema.document import Document
from langchain_community.embeddings.ollama import OllamaEmbeddings
from config.config import EMBEDDING_MODEL, VECTOR_DB_PATH # Import the embedding model from the config

# Initialize the persistent Chroma database client with the specified path
client = chromadb.PersistentClient(path="../Data/vectorDB")

def feed_vector_db(chunks: list[Document]):
    """
    Feed the vector database with document chunks.

    Args:
        chunks (list[Document]): A list of Document objects to be added to the vector database.
    """

    # Define the name of the collection in the database
    collection_name = "PhysicsBook"

    # Initialize the embedding function using the model from config
    emb_fn = OllamaEmbeddings(model=EMBEDDING_MODEL)

    # Import Chroma for creating the collection
    from langchain_chroma import Chroma

    # Create a collection for storing embedded documents
    collection = Chroma(
        collection_name=collection_name,
        embedding_function=emb_fn,
        persist_directory=VECTOR_DB_PATH,  # Directory to save data locally; remove if not necessary
    )

    # Calculate unique IDs for each chunk based on their metadata
    chunks_with_ids = calculate_chunk_ids(chunks)
    chunk_ids = [chunk.metadata["id"] for chunk in chunks_with_ids]

    # Add the document chunks and their IDs to the collection
    collection.add_documents(
        documents=chunks_with_ids,
        ids=chunk_ids
    )

def calculate_chunk_ids(chunks):
    """
    Calculate unique IDs for document chunks based on their metadata.

    Args:
        chunks (list[Document]): A list of Document objects to calculate IDs for.

    Returns:
        list[Document]: The input list of Document objects, each with an updated metadata ID.
    """

    # Initialize variables to track the last page ID and current chunk index
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        # Extract source and page metadata from the chunk
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")

        # Create a unique identifier for the current page
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0  # Reset the index for a new page

        # Generate the chunk ID based on the page ID and current chunk index
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id  # Update the last page ID

        # Add the generated ID to the chunk's metadata
        chunk.metadata["id"] = chunk_id

    # Return the updated list of chunks with IDs in their metadata
    return chunks
