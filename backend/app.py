""" from flask import Flask, request, jsonify
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
"""

import streamlit as st
import sqlite3

# Function to fetch data from SQLite
def query_database(query, params=()):
    conn = sqlite3.connect("company.db")  # Ensure database.db exists
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Function to process natural language queries
def process_query(user_input):
    user_input = user_input.lower()

    if "employees in" in user_input:
        dept = user_input.split("employees in ")[-1]
        query = "SELECT Name FROM Employees WHERE Department = ?"
        results = query_database(query, (dept,))
        return f"Employees in {dept}: " + ", ".join([row[0] for row in results]) if results else "No employees found."

    elif "manager of" in user_input:
        dept = user_input.split("manager of ")[-1]
        query = "SELECT Manager FROM Departments WHERE Name = ?"
        results = query_database(query, (dept,))
        return f"The manager of {dept} is {results[0][0]}" if results else "Department not found."

    elif "hired after" in user_input:
        date = user_input.split("hired after ")[-1]
        query = "SELECT Name FROM Employees WHERE Hire_Date > ?"
        results = query_database(query, (date,))
        return f"Employees hired after {date}: " + ", ".join([row[0] for row in results]) if results else "No employees found."

    elif "total salary expense for" in user_input:
        dept = user_input.split("total salary expense for ")[-1]
        query = "SELECT SUM(Salary) FROM Employees WHERE Department = ?"
        results = query_database(query, (dept,))
        return f"Total salary expense for {dept}: ${results[0][0]}" if results[0][0] else "Department not found."

    else:
        return "Sorry, I didn't understand that."

# Streamlit UI
st.title("Chatbot for SQLite Database")
st.write("Ask me about employees, departments, or salaries.")

# Chat interface
user_input = st.text_input("You:", "")
if user_input:
    response = process_query(user_input)
    st.text_area("Bot:", response, height=100, disabled=True)
