# app/db/chroma_client.py
import chromadb
from app.config import settings

chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)

collection = chroma_client.get_or_create_collection(
    name="ipsakti_documents",
    metadata={"hnsw:space": "cosine"},
)