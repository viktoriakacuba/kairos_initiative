import sqlite3
from typing import List, Tuple

DB_PATH = "core/memory.sqlite"

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input TEXT NOT NULL,
                response TEXT NOT NULL
            )
        """)

def save_interaction(input_text: str, response_text: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO memory (input, response) VALUES (?, ?)",
            (input_text, response_text)
        )

def get_last_n(n: int = 3) -> List[Tuple[str, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT input, response FROM memory ORDER BY id DESC LIMIT ?",
            (n,)
        )
        return cursor.fetchall()[::-1]
