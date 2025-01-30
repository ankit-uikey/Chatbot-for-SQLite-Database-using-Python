from flask import Flask, request, jsonify
from chatbot import process_query
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# This route handles chat messages sent via POST requests
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    response = process_query(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
