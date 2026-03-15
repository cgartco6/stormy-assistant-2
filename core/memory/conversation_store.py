import sqlite3
import os

class ConversationStore:
    def __init__(self, db_path="data/conversations.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT,
                    stormy_response TEXT,
                    mood TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save(self, user_input, response, mood):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO conversations (user_input, stormy_response, mood) VALUES (?, ?, ?)",
                (user_input, response, mood)
            )
