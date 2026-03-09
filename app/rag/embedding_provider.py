"""Embedding 抽象层（rag）。默认使用可离线运行的哈希向量。"""
from abc import ABC, abstractmethod
import hashlib
from typing import List

from langchain_ollama import OllamaEmbeddings


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        ...

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        ...


class HashEmbeddingProvider(EmbeddingProvider):
    def __init__(self, dim: int = 128) -> None:
        self.dim = dim

    def _embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        for token in text.lower().split():
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            idx = int(digest[:8], 16) % self.dim
            vec[idx] += 1.0
        norm = sum(v * v for v in vec) ** 0.5 or 1.0
        return [v / norm for v in vec]

    def embed_documents(self, texts: List[str]) -> list[list[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, base_url: str, model: str) -> None:
        self.embedding = OllamaEmbeddings(model=model, base_url=base_url)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.embedding.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.embedding.embed_query(text)
