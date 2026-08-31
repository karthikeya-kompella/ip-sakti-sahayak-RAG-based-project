# app/models/document.py
from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    regime = Column(String, nullable=False, index=True)      # e.g. "IN-AYUSH", "US-FDA"
    language = Column(String, nullable=False)                 # e.g. "hi", "en"
    doc_type = Column(String, nullable=False)                 # "regulation" | "patent" | "guideline"
    source_url = Column(String, nullable=True)
    file_path = Column(String, nullable=True)                 # where the raw file is stored on disk
    status = Column(String, nullable=False, default="pending")  # pending | processing | done | failed
    chunk_count = Column(Integer, nullable=True)               # filled in once ingestion completes
    created_at = Column(DateTime(timezone=True), server_default=func.now())