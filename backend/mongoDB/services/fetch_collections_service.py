from pymongo import MongoClient
from flask import jsonify
from config.config import MONGO_URI, DB_NAME  # Importing MongoDB configuration

# Establish MongoDB client connection
client = MongoClient(MONGO_URI)

# Function to fetch all documents from a collection
def fetch_chat_list(collection_name: str):
    try:
        # Access the database and collection
        db = client[DB_NAME]
        collection = db[collection_name]
        
        # Fetch all documents and return them as a list of dictionaries
        return list(collection.find({}))
    except Exception as error:
        print(f"Error fetching chat list from {collection_name}: {error}")
        return []

# Function to fetch all collection names in the database
def fetch_all_collection() -> list[str]:
    try:
        # Access the database
        db = client[DB_NAME]

        # Get the collection names and return them
        collection_names = db.list_collection_names()
        return collection_names

    except Exception as error:
        print(f"Error fetching collections: {error}")
        return {"error": "An error occurred fetching collections"}
