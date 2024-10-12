# api_routes.py

from flask import Blueprint, request, jsonify
from services.response_generator import get_response

# Create a Blueprint for the API routes
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    response = get_response(data) 
    return jsonify(response)
