from typing import Optional
import numpy as np
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.database import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.core.dependencies import get_current_user_id
from app.core.local_embeddings import get_embedding
from app.llm.groq_client import generate_answer

router = APIRouter(prefix="/rag", tags=["RAG"])


# ✅ REQUEST SCHEMA
class RagRequest(BaseModel):
    query: str
    conversation_id: Optional[int] = None
    top_k: int = 7


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


@router.post("/answer")
def rag_answer(
    payload: RagRequest,                # ✅ JSON BODY
    user_id: int = Depends(get_current_user_id)
):
    db = SessionLocal()
    try:
        query = payload.query
        top_k = payload.top_k

        query_embedding = get_embedding(query)

        chunks = (
            db.query(DocumentChunk)
            .join(Document)
            .filter(Document.user_id == user_id)
            .all()
        )

        scored_chunks = []
        for chunk in chunks:
            if chunk.embedding:
                score = cosine_similarity(query_embedding, chunk.embedding)
                scored_chunks.append((score, chunk.text))

        scored_chunks.sort(reverse=True)
        top_chunks = [text for score, text in scored_chunks[:top_k] if score >= 0.15]

        if not top_chunks:
            answer = "No relevant information found."
        else:
            answer = generate_answer(query, "\n\n".join(top_chunks))

        return {
            "answer": answer,
            "chunks_used": len(top_chunks)
        }

    finally:
        db.close()
