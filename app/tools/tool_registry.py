"""工具模块（tools）。定义 LangChain 可调用工具。"""
from datetime import datetime
from langchain_core.tools import tool


def build_tools(vector_store, runtime_trace: dict):
    @tool
    def search_documents(query: str, top_k: int = 4) -> str:
        """检索结算文档，返回相关片段与来源。"""
        runtime_trace.setdefault("used_tools", []).append("search_documents")
        chunks = vector_store.search(query, top_k=top_k)
        runtime_trace["retrieved_chunks"] = chunks
        lines = []
        for c in chunks:
            meta = c["metadata"]
            lines.append(f"[{meta.get('source_file')}|{c['chunk_id']}] {c['content']}")
        return "\n".join(lines) if lines else "未检索到相关文档。"

    @tool
    def get_current_time() -> str:
        """获取当前时间。"""
        runtime_trace.setdefault("used_tools", []).append("get_current_time")
        return datetime.now().isoformat()

    @tool
    def multiply(a: float, b: float) -> float:
        """执行乘法计算。"""
        runtime_trace.setdefault("used_tools", []).append("multiply")
        return a * b

    return [search_documents, get_current_time, multiply]
