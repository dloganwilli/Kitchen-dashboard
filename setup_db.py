# setup_db.py

import sqlite3
import os

# Ensure the path exists
db_path = os.path.join("data", "recipes.db")
os.makedirs("data", exist_ok=True)

# Connect and create the recipes table
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    ingredients TEXT,
    instructions TEXT
)
""")

conn.commit()
conn.close()
print("✅ Recipe table ready in data/recipes.db")