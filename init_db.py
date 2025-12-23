import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()
conn.close()
