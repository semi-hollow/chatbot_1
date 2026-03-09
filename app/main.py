"""应用入口。"""
from fastapi import FastAPI

from app.agents.single_agent import SettlementAgent
from app.api.routes import build_router
from app.config.settings import settings
from app.memory.long_term import LongTermMemory
from app.memory.short_term import ShortTermMemory
from app.mcp.client import MCPClient
from app.models.model_factory import build_chat_model
from app.prompts.prompt_manager import PromptManager
from app.rag.embedding_provider import HashEmbeddingProvider, OllamaEmbeddingProvider
from app.rag.vector_store import DocumentVectorStore
from app.skills.implementations import build_skills
from app.storage.sqlite_store import SQLiteStore


class Container:
    def __init__(self) -> None:
        self.store = SQLiteStore(settings.db_path)
        self.short_memory = ShortTermMemory(self.store, max_rounds=settings.short_term_limit)
        self.long_memory = LongTermMemory(self.store)

        if settings.embedding_provider == "ollama":
            emb = OllamaEmbeddingProvider(settings.ollama_base_url, settings.ollama_embedding_model)
        else:
            emb = HashEmbeddingProvider()

        self.vector_store = DocumentVectorStore(settings.chroma_path, emb)
        self.prompt_manager = PromptManager(settings.prompt_dir)
        self.mcp_client = MCPClient(settings.mcp_server_command)
        self.agent = SettlementAgent(
            llm=build_chat_model(settings),
            prompt_manager=self.prompt_manager,
            short_memory=self.short_memory,
            long_memory=self.long_memory,
            skills=build_skills(),
            mcp_client=self.mcp_client,
            vector_store=self.vector_store,
        )


container = Container()
app = FastAPI(title=settings.app_name)
app.include_router(build_router(container))
