"""API 路由模块（api）。"""
from fastapi import APIRouter, HTTPException

from app.api.schemas import ImportDocumentRequest, ChatRequest, UserProfileRequest
from app.rag.document_parser import parse_file, split_into_chunks


def build_router(container) -> APIRouter:
    router = APIRouter()

    @router.post("/documents/import")
    def import_document(req: ImportDocumentRequest):
        try:
            source_file, text = parse_file(req.file_path)
            chunks = split_into_chunks(source_file, text)
            container.vector_store.upsert_chunks(chunks)
            return {"status": "ok", "source_file": source_file, "chunks": len(chunks)}
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    @router.post("/chat")
    def chat(req: ChatRequest):
        return container.agent.chat(req.user_id, req.session_id, req.message, req.language)

    @router.get("/conversations/{session_id}")
    def get_conversation(session_id: str):
        return {"session_id": session_id, "messages": container.short_memory.get_recent_messages(session_id)}

    @router.post("/users/{user_id}/profile")
    def set_profile(user_id: str, req: UserProfileRequest):
        profile = container.long_memory.upsert_profile(
            user_id=user_id,
            preferred_language=req.preferred_language,
            preferred_answer_style=req.preferred_answer_style,
            domain_role=req.domain_role,
        )
        return profile

    @router.get("/users/{user_id}/profile")
    def get_profile(user_id: str):
        return container.long_memory.get_profile(user_id)

    return router
