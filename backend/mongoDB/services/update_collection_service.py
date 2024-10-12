# mongo_db_service.py

from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME

# MongoDB connection
client = MongoClient(MONGO_URI)

def update_collection(AssisContent, content):
    try:
        print("Connected successfully to server")
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        new_data = [
            {
                "role": "user",
                "content": content
            },
            {
                "role": "assistant",
                "content": AssisContent
            }
        ]

        insert_result = collection.insert_many(new_data)
        return "Success"
    except Exception as error:
        print("Error:", error)
        return "Error in updating collection"
