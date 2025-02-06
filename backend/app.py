from flask import Flask, request, jsonify, send_from_directory
from chatbot import process_query
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="../frontend")
CORS(app)  # Enable cross-origin requests

# Serve the index.html file
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

# Serve static files (CSS, JS)
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

# This route handles chat messages sent via POST requests
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    response = process_query(user_input)
    return jsonify({"response": response})
    
if __name__ == "__main__":
    app.run(debug=True)
