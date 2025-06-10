import sqlite3
from typing import List, Tuple

DB_PATH = "core/memory.sqlite"

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                input TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_interaction(user_id: str, input_text: str, response_text: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO memory (user_id, input, response) VALUES (?, ?, ?)",
            (user_id, input_text, response_text)
        )

def get_last_n(user_id: str, n: int = 3) -> List[Tuple[str, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT input, response FROM memory WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, n)
        )
        return cursor.fetchall()[::-1]
