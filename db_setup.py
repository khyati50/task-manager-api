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
    status TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
)
""")
# create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# save changes
conn.commit()

# close connection
conn.close()

print("Database and table created successfully")
