from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
import numpy as np
from config.config import CHUNK_SIZE, CHUNK_OVERLAP_PERCENTAGE

# Calculate chunk overlap based on the configuration
chunk_overlap = int(np.round(CHUNK_SIZE * CHUNK_OVERLAP_PERCENTAGE, 0))

def get_chunk(file_path: str) -> list[Document]:
    """
    Load a PDF file and split it into chunks of text.

    Args:
        file_path (str): The path to the PDF file to be loaded.

    Returns:
        list[Document]: A list of Document objects containing the text chunks.
    """

    # Load the PDF and split it into pages
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()

    # Define a function to split the loaded documents into chunks
    def split_documents(documents: list[Document]) -> list[Document]:
        """
        Split documents into smaller chunks.

        Args:
            documents (list[Document]): A list of Document objects to split.

        Returns:
            list[Document]: A list of Document objects containing the text chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ". ", ""],  # Separators used for splitting
        )
        return text_splitter.split_documents(documents)

    # Split the loaded pages into chunks and return the result
    return split_documents(pages)
