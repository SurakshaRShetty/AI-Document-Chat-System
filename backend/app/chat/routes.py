from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.dependencies import get_current_user_id
from app.database import SessionLocal
from app.models.document_chunk import DocumentChunk
from app.models.document import Document
from app.llm.groq_client import generate_answer
import numpy as np

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    document_id: int
    question: str


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


@router.post("/ask")
def ask_question(
    payload: ChatRequest,
    user_id: int = Depends(get_current_user_id)
):
    db = SessionLocal()
    try:
        chunks = (
            db.query(DocumentChunk)
            .join(Document)
            .filter(
                Document.id == payload.document_id,
                Document.user_id == user_id
            )
            .all()
        )

        if not chunks:
            return {"answer": "No document chunks found."}

        query_embedding = np.array(payload.question)

        scored = []
        for chunk in chunks:
            if chunk.embedding:
                score = cosine_similarity(chunk.embedding, chunk.embedding)
                scored.append((score, chunk.text))

        scored.sort(reverse=True)
        context = "\n\n".join([t for _, t in scored[:5]])

        answer = generate_answer(payload.question, context)

        return {
            "question": payload.question,
            "answer": answer
        }

    finally:
        db.close()
