from app.database import engine, Base
from app.models.user import User  # IMPORTANT: import model
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")

if __name__ == "__main__":
    create_tables()
