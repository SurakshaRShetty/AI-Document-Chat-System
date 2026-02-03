import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.core.dependencies import get_current_user_id
from app.documents.pdf_utils import extract_text_from_pdf
from app.documents.chunk_utils import chunk_text
from app.core.local_embeddings import get_embedding

router = APIRouter()
UPLOAD_DIR = "uploads"


# ---------------------------
# 1️⃣ UPLOAD DOCUMENT
# ---------------------------
@router.post("/documents")
def upload_document(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Extract and chunk text
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)

    if not chunks:
        raise HTTPException(status_code=400, detail="No text found in PDF")

    db: Session = SessionLocal()

    try:
        # Save document
        document = Document(
            user_id=user_id,
            filename=file.filename,
            file_path=file_path
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        document_id = document.id

        # Save chunks with embeddings
        for index, chunk_text_content in enumerate(chunks):
            embedding = get_embedding(chunk_text_content)

            # 🔥 GUARANTEE FLAT VECTOR
            if isinstance(embedding, list) and len(embedding) > 0 and isinstance(embedding[0], list):
                embedding = embedding[0]

            db.add(
                DocumentChunk(
                    document_id=document_id,
                    chunk_index=index,
                    text=chunk_text_content,
                    embedding=embedding
                )
            )

        db.commit()

        return {
            "message": "Document uploaded successfully",
            "document_id": document_id,
            "chunks_created": len(chunks)
        }

    finally:
        db.close()


# ---------------------------
# 2️⃣ READ DOCUMENT CHUNKS
# ---------------------------
@router.get("/documents/{document_id}/chunks")
def get_document_chunks(
    document_id: int,
    user_id: int = Depends(get_current_user_id)
):
    db: Session = SessionLocal()

    try:
        chunks = (
            db.query(DocumentChunk)
            .join(Document, Document.id == DocumentChunk.document_id)
            .filter(
                Document.id == document_id,
                Document.user_id == user_id
            )
            .order_by(DocumentChunk.chunk_index)
            .all()
        )

        return {
            "document_id": document_id,
            "total_chunks": len(chunks),
            "chunks": [
                {
                    "chunk_index": c.chunk_index,
                    "text_preview": c.text[:300]
                }
                for c in chunks
            ]
        }

    finally:
        db.close()
