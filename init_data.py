import sqlite3

"""GlobalGiving Project API
Read the API Docs
API Key Version 1 Active
4b5fb6dd-91e3-44ae-8202-36cf16fdaf24"""



# Connect to SQLite database (will create it if it doesn't exist)
conn = sqlite3.connect("data/altrue.db")
cursor = conn.cursor()

# Create 'queries' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS queries (
    query_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_query TEXT NOT NULL,
    topic TEXT,
    location TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Create 'responses' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS responses (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_id INTEGER,
    model_used TEXT,
    projects_json TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (query_id) REFERENCES queries(query_id)
)
''')

conn.commit()
conn.close()
print("Database initialized ✅")
