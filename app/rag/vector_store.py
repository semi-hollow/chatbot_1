"""向量检索模块（rag）。"""
import chromadb
from chromadb.api.models.Collection import Collection
from app.rag.embedding_provider import EmbeddingProvider


class DocumentVectorStore:
    def __init__(self, persist_path: str, embedding_provider: EmbeddingProvider) -> None:
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection: Collection = self.client.get_or_create_collection("settlement_docs")
        self.embedding_provider = embedding_provider

    def upsert_chunks(self, chunks: list[dict]) -> None:
        ids = [c["chunk_id"] for c in chunks]
        docs = [c["content"] for c in chunks]
        metas = [{k: v for k, v in c.items() if k != "content"} for c in chunks]
        embeddings = self.embedding_provider.embed_documents(docs)
        self.collection.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=embeddings)

    def search(self, query: str, top_k: int = 4) -> list[dict]:
        query_emb = self.embedding_provider.embed_query(query)
        result = self.collection.query(query_embeddings=[query_emb], n_results=top_k)
        out = []
        for i in range(len(result["ids"][0])):
            out.append(
                {
                    "chunk_id": result["ids"][0][i],
                    "content": result["documents"][0][i],
                    "metadata": result["metadatas"][0][i],
                }
            )
        return out
