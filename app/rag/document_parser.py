"""文档解析模块（rag）。支持 Markdown 与 Word。"""
from pathlib import Path
from docx import Document


def parse_file(file_path: str) -> tuple[str, str]:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".md":
        text = path.read_text(encoding="utf-8")
    elif suffix == ".docx":
        doc = Document(file_path)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    else:
        raise ValueError(f"不支持的文件类型: {suffix}")
    return path.name, text


def split_into_chunks(source_file: str, text: str, chunk_size: int = 500, overlap: int = 100) -> list[dict]:
    chunks = []
    start = 0
    chunk_index = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk_text = text[start:end]
        title = chunk_text.splitlines()[0][:50] if chunk_text else source_file
        chunk_id = f"{Path(source_file).stem}-{chunk_index}"
        chunks.append(
            {
                "chunk_id": chunk_id,
                "source_file": source_file,
                "chunk_index": chunk_index,
                "title": title,
                "content": chunk_text,
            }
        )
        chunk_index += 1
        start += chunk_size - overlap
    return chunks
