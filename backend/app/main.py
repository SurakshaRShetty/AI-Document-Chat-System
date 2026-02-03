from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import router as auth_router
from app.documents.routes import router as documents_router
from app.chat.routes import router as chat_router
from app.search.routes import router as search_router
from app.rag.routes import router as rag_router
from app.conversations.routes import router as conversation_router

from app.core.dependencies import get_current_user_id
from app.database import Base
from app.models import *

app = FastAPI(title="RAG Chatbot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ INCLUDE ROUTERS (NO PREFIX HERE)
app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(chat_router)
app.include_router(search_router)
app.include_router(rag_router)
app.include_router(conversation_router)

@app.get("/")
def root():
    return {"status": "RAG backend running"}

@app.get("/me")
def get_me(user_id: int = Depends(get_current_user_id)):
    return {"message": "You are authenticated", "user_id": user_id}
