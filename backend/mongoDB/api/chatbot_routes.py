# mongo_db_routes.py

from flask import Blueprint, request, jsonify
from mongoDB.services.fetch_collections_service import fetch_all_collection, fetch_chat_list
from mongoDB.services.delete_chat_service import delete_chat
from mongoDB.services.update_collection_service import update_collection

# Create a Blueprint for the MongoDB-related routes
mongo_blueprint = Blueprint('mongo_api', __name__)

@mongo_blueprint.route('/fetch_collection', methods=['POST'])
def fetch_collection():
    response = fetch_all_collection()
    return jsonify(response)

@mongo_blueprint.route('/fetch_chat', methods=['POST'])
def fetch_chat():
    data = request.get_json()
    collection_name = data.get("collection_name")
    response = fetch_chat_list(collection_name=collection_name)
    
    for doc in response:
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
    
    return jsonify(response)

@mongo_blueprint.route('/delete_chat_', methods=['POST'])
def delete_chat_():
    data = request.get_json()
    collection_name = data.get("collection_name")
    response = delete_chat(collection_name=collection_name)
    return jsonify(response)

@mongo_blueprint.route('/add_response', methods=['POST'])
def add_response():
    data = request.get_json()
    AssisContent = data.get("AssisContent")
    content = data.get("content")
    response = update_collection(AssisContent=AssisContent, content=content)
    return jsonify(response)
