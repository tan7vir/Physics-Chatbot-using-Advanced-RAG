from flask import Flask
from flask_cors import CORS
import atexit
import subprocess
import os

# Import the API routes
from api.chatbot_routes import api_blueprint
from mongoDB.api.chatbot_routes import mongo_blueprint

app = Flask(__name__)
CORS(app)

# Register the API blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(mongo_blueprint, url_prefix='/mongo')

# Function to start Ollama
def start_ollama():
    try:
        # Redirect stdout and stderr to os.devnull
        with open(os.devnull, 'w') as devnull:
            ollama_process = subprocess.Popen(
                ["ollama", "serve"], 
                stdout=devnull,  # Discard stdout
                stderr=devnull,  # Discard stderr
                shell=True       # Required for Windows
            ) 
            print("Ollama is starting...", flush=True)
            return ollama_process
    except Exception as e:
        print(f"Error starting Ollama: {e}", flush=True)
        return None

# Start Ollama when Backend starts
ollama_process = start_ollama()

# Stop the Ollama server
def stop_ollama():
    if ollama_process:
        ollama_process.terminate()  
        print("Ollama server stopped.", flush=True)

# Register the stop_ollama function to be called on exit
atexit.register(stop_ollama)

if __name__ == "__main__":
    app.run(debug=True)
