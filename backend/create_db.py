# import sqlite3
import pymysql

# Connect to SQLite database (or create it if it doesn't exist)
#conn = sqlite3.connect("company.db")
#cursor = conn.cursor()

timeout = 10
conn = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="mysql-database-chatbot-for-database-using-python.k.aivencloud.com",
  password="AVNS_KiPRSvvJM8j5gmXI0Y0",
  read_timeout=timeout,
  port=20052,
  user="avnadmin",
  write_timeout=timeout,
)

try:
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
    print("Employees Table Created Successfully!")
    
    employees_data = [  (1, "Alice", "Sales", 50000, "2021-01-15"),
                        (2, "Bob", "Engineering", 70000, "2020-06-10"),
                        (3, "Charlie", "Marketing", 60000, "2022-03-20"),
                        (4, "Ankit", "Engineering", 90000, "2025-02-10"),
                        (5, "David", "Sales", 75000, "2023-04-25")
                    ]
    # Insert sample data into Employees table
    cursor.executemany("""INSERT INTO Employees (ID, Name, Department, Salary, Hire_Date) VALUES (%s, %s, %s, %s, %s)"""
                       , employees_data
    )
    print("Employees Data Successfully Added!")

    # Create Departments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Departments (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Manager TEXT NOT NULL
    );
    """)
    print("Departments Table Created Successfully!")
    
    departments_data = [(1, "Sales", "Alice"),
                        (2, "Engineering", "Bob"),
                        (3, "Marketing", "Charlie"),
                        (4, "HR", "Ankit")
            ]
    # Insert sample data into Departments table
    cursor.executemany("""INSERT INTO Departments (ID, Name, Manager) VALUES (%s, %s, %s)"""
                       , departments_data 
                )
    print("Departments Data Successfully Added!")

    print(f"\nDatabase and tables created successfully!")

finally:
    # Commit changes and close connection
    conn.commit()
    conn.close()

# print("Database and tables created successfully!")
