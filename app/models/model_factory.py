"""模型模块（models）。提供 Ollama 优先的聊天模型工厂。"""
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI


def build_chat_model(settings):
    if settings.llm_provider == "openai-compatible":
        return ChatOpenAI(
            model=settings.openai_chat_model,
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key,
            temperature=0,
        )

    return ChatOllama(
        model=settings.ollama_chat_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )
