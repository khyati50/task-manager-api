import sqlite3

# connect to database file (creates it if it doesn't exist)
conn = sqlite3.connect("tasks.db")

# cursor is used to execute SQL commands
cursor = conn.cursor()

# create tasks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

# save changes
conn.commit()

# close connection
conn.close()

print("Database and table created successfully")
