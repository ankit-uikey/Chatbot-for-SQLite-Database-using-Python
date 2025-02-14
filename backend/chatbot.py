import pymysql
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import os

# Download NLTK resources if not available
nltk.download("punkt")
nltk.download("stopwords")

# Predefined department names for validation
DEPARTMENTS = {"Sales", "Engineering", "Marketing"}

def preprocess_input(user_input):
    """Tokenizes user input and removes stopwords & punctuation."""
    tokens = word_tokenize(user_input.lower())
    tokens = [word for word in tokens if word not in stopwords.words("english") and word not in string.punctuation]
    return tokens

def extract_department(user_input):
    """Extracts department name from user input."""
    for dept in DEPARTMENTS:
        if dept.lower() in user_input.lower():
            return dept
    return None

def extract_date(user_input):
    """Extracts date from user input (YYYY-MM-DD format)."""
    match = re.search(r"\d{4}-\d{2}-\d{2}", user_input)
    return match.group(0) if match else None

def generate_sql_query(user_input):
    """Generates SQL query based on user input."""
    user_input = user_input.lower()
    
    # Match query patterns
    if "show" in user_input and "employees" in user_input:
        department = extract_department(user_input)
        if department:
            return f"SELECT Name, Salary, Hire_Date FROM Employees WHERE Department='{department}';"
        return "SELECT Name, Department, Salary, Hire_Date FROM Employees;"
    
    elif "who is the manager" in user_input:
        department = extract_department(user_input)
        if department:
            return f"SELECT Manager FROM Departments WHERE Name='{department}';"
        return None

    elif "list all employees hired after" in user_input:
        hire_date = extract_date(user_input)
        if hire_date:
            return f"SELECT Name, Department, Hire_Date FROM Employees WHERE Hire_Date > '{hire_date}';"
        return None

    elif "total salary expense for" in user_input:
        department = extract_department(user_input)
        if department:
            return f"SELECT SUM(Salary) FROM Employees WHERE Department='{department}';"
        return None

    return None  # No valid query pattern matched

def execute_query(query):
    """Executes the SQL query on the MySQL Server database."""
    #timeout = 2 # Set timeout to 2 seconds
    conn = pymysql.connect(
            charset="utf8mb4",
            connect_timeout= 5, #Set timeout to 5 seconds
            cursorclass=pymysql.cursors.DictCursor,
            db=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            password=os.getenv("DB_PASSWORD"),
            read_timeout=2, # Set timeout to 2 seconds
            port=20052,
            user=os.getenv("DB_USER"),
            write_timeout= 5, # Set timeout to 5 seconds
        )
    
    cursor = conn.cursor()
    print(f"\n Connection to MySQL DB successful! \n")
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return "No matching records found."
        
        # Format response based on query type
        if "SUM(Salary)" in query:
            return f"Total salary expense: ${results[0][0]}" if results[0][0] else "No data available."
        elif "Manager" in query:
            return f"The manager is {results[0][0]}" if results else "No manager found."
        else:
            return "\n".join(str(row) for row in results)
    
    except pymysql.Error as e:
        conn.close()
        return f"Database error: {e}"

def process_query(user_input):
    """Processes user input and returns a chatbot response."""
    query = generate_sql_query(user_input)
    if query:
        return execute_query(query)
    return "Sorry, I didn't understand your request. Please try again with a valid question."
