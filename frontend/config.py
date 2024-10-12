# config.py

# Backend API URLs
BACKEND_URL = 'http://127.0.0.1:5000'
GENERATE_URL = f'{BACKEND_URL}/api/generate'
FETCH_COLLECTION_URL = f'{BACKEND_URL}/mongo/fetch_collection'
FETCH_CHAT_URL = f'{BACKEND_URL}/mongo/fetch_chat'
DELETE_CHAT_URL = f'{BACKEND_URL}/mongo/delete_chat_'
ADD_RESPONSE_URL = f'{BACKEND_URL}/mongo/add_response'

# Default model
DEFAULT_MODEL = 'gemma2:2b'
