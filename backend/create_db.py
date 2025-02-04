import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Create Employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Department TEXT NOT NULL,
    Salary INTEGER NOT NULL,
    Hire_Date TEXT NOT NULL
);
""")

# Insert sample data into Employees table
cursor.executemany("""
INSERT INTO Employees (ID, Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?, ?)
""", [
    (1, "Alice", "Sales", 50000, "2021-01-15"),
    (2, "Bob", "Engineering", 70000, "2020-06-10"),
    (3, "Charlie", "Marketing", 60000, "2022-03-20"),
    (4, "Ankit", "Engineering", 90000, "2025-02-10")
])

# Create Departments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Departments (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Manager TEXT NOT NULL
);
""")

# Insert sample data into Departments table
cursor.executemany("""
INSERT INTO Departments (ID, Name, Manager) VALUES (?, ?, ?)
""", [
    (1, "Sales", "Alice"),
    (2, "Engineering", "Bob"),
    (3, "Marketing", "Charlie"),
    (4, "Engineering", "Ankit")
])

# Commit changes and close connection
conn.commit()
conn.close()

print("Database and tables created successfully!")
