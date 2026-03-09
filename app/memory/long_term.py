"""长期记忆模块（long-term memory）。"""
from app.storage.sqlite_store import SQLiteStore


class LongTermMemory:
    def __init__(self, store: SQLiteStore) -> None:
        self.store = store

    def get_profile(self, user_id: str) -> dict:
        profile = self.store.fetchone(
            "SELECT user_id, preferred_language, preferred_answer_style, domain_role FROM user_profiles WHERE user_id = ?",
            (user_id,),
        )
        if not profile:
            return {
                "user_id": user_id,
                "preferred_language": "zh-CN",
                "preferred_answer_style": "简洁",
                "domain_role": "财务运营",
            }
        return profile

    def upsert_profile(self, user_id: str, preferred_language: str, preferred_answer_style: str, domain_role: str) -> dict:
        self.store.execute(
            """
            INSERT INTO user_profiles(user_id, preferred_language, preferred_answer_style, domain_role, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
              preferred_language=excluded.preferred_language,
              preferred_answer_style=excluded.preferred_answer_style,
              domain_role=excluded.domain_role,
              updated_at=CURRENT_TIMESTAMP
            """,
            (user_id, preferred_language, preferred_answer_style, domain_role),
        )
        return self.get_profile(user_id)
