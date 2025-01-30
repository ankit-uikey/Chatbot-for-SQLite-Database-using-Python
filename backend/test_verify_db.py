import sqlite3

conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Fetch and print Employees data
print("Employees Table:")
for row in cursor.execute("SELECT * FROM Employees;"):
    print(row)

# Fetch and print Departments data
print("\nDepartments Table:")
for row in cursor.execute("SELECT * FROM Departments;"):
    print(row)

conn.close()
