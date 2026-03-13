import sqlite3
import json
from pathlib import Path

class EmbeddingDatabase:
    def __init__(self, db_path: str = "embeddings.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS embeddings (
                    tool_name TEXT PRIMARY KEY,
                    embedding TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_embedding(self, tool_name: str, embedding: list):
        """Save an embedding for a tool"""
        embedding_json = json.dumps(embedding)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO embeddings (tool_name, embedding) VALUES (?, ?)",
                (tool_name, embedding_json)
            )
            conn.commit()

    def load_embedding(self, tool_name: str):
        """Load an embedding for a tool"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT embedding FROM embeddings WHERE tool_name = ?",
                (tool_name,)
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
        return None

    def load_all_embeddings(self):
        """Load all embeddings from the database"""
        embeddings = {}
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT tool_name, embedding FROM embeddings")
            for tool_name, embedding_json in cursor.fetchall():
                embeddings[tool_name] = json.loads(embedding_json)
        return embeddings

    def clear_all(self):
        """Clear all embeddings from the database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM embeddings")
            conn.commit()
