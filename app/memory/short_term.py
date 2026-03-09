"""短期记忆模块（short-term memory）。"""
from app.storage.sqlite_store import SQLiteStore


class ShortTermMemory:
    def __init__(self, store: SQLiteStore, max_rounds: int = 8) -> None:
        self.store = store
        self.max_rounds = max_rounds

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.store.execute(
            "INSERT INTO conversations(session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content),
        )

    def get_recent_messages(self, session_id: str) -> list[dict]:
        limit = self.max_rounds * 2
        rows = self.store.fetchall(
            """
            SELECT role, content, created_at FROM conversations
            WHERE session_id = ? ORDER BY id DESC LIMIT ?
            """,
            (session_id, limit),
        )
        return list(reversed(rows))
