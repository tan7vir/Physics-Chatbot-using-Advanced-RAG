from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME  # Importing MongoDB configuration

# Establish MongoDB client connection
client = MongoClient(MONGO_URI)

# Function to delete all chats in the specified collection
def delete_chat(collection_name: str) -> str:
    try:
        # Access the database and the specified collection
        db = client[DB_NAME]
        collection = db[collection_name]

        # Delete all documents from the collection
        delete_result = collection.delete_many({})
        print(f"{delete_result.deleted_count} documents deleted from {collection_name}")

        # Insert a default message into the collection after deletion
        new_data = [{"role": "assistant", "content": "How may I assist you today?"}]
        insert_result = collection.insert_many(new_data)
        
        return "Success"
    except Exception as error:
        print(f"Error deleting chat: {error}")
        return "Error in deleting chat"
