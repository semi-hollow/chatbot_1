"""API 数据模型（api）。"""
from pydantic import BaseModel


class ImportDocumentRequest(BaseModel):
    file_path: str


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str
    language: str = "zh-CN"


class UserProfileRequest(BaseModel):
    preferred_language: str
    preferred_answer_style: str
    domain_role: str
