"""配置模块（config）。"""
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    app_name: str = "Settlement QA Assistant"
    db_path: str = os.getenv("DB_PATH", "data/app.db")
    chroma_path: str = os.getenv("CHROMA_PATH", "data/chroma")
    docs_path: str = os.getenv("DOCS_PATH", "data/documents")

    llm_provider: str = os.getenv("LLM_PROVIDER", "ollama")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_chat_model: str = os.getenv("OLLAMA_CHAT_MODEL", "qwen3:8b")

    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_chat_model: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

    embedding_provider: str = os.getenv("EMBEDDING_PROVIDER", "hash")
    ollama_embedding_model: str = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

    default_language: str = os.getenv("DEFAULT_LANGUAGE", "zh-CN")
    short_term_limit: int = int(os.getenv("SHORT_TERM_LIMIT", "8"))

    mcp_server_command: str = os.getenv("MCP_SERVER_COMMAND", "python -m app.mcp.server")

    @property
    def prompt_dir(self) -> Path:
        return Path("app/prompts")


settings = Settings()
