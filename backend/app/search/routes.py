import numpy as np
from fastapi import APIRouter, Depends
from app.database import SessionLocal
from app.models.document_chunk import DocumentChunk
from app.models.document import Document
from app.core.dependencies import get_current_user_id
from app.core.local_embeddings import get_embedding

router = APIRouter()


def cosine_similarity(a, b):
    a = np.array(a).reshape(-1)
    b = np.array(b).reshape(-1)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


@router.post("/search/")
def semantic_search(
    query: str,
    top_k: int = 3,
    user_id: int = Depends(get_current_user_id)
):
    db = SessionLocal()

    # 1️⃣ Embed query (FLAT)
    query_embedding = get_embedding(query)
    query_embedding = np.array(query_embedding).reshape(-1)

    # 2️⃣ Fetch only user's chunks (NO relationship join)
    chunks = (
        db.query(DocumentChunk)
        .join(Document, Document.id == DocumentChunk.document_id)
        .filter(Document.user_id == user_id)
        .all()
    )

    results = []

    for chunk in chunks:
        if not chunk.embedding:
            continue

        chunk_embedding = np.array(chunk.embedding).reshape(-1)

        score = cosine_similarity(query_embedding, chunk_embedding)

        results.append({
            "score": score,
            "text": chunk.text
        })

    db.close()

    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "query": query,
        "results": results[:top_k]
    }
