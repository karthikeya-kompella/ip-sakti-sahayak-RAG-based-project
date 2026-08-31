# app/routers/documents.py
import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.document import Document
from app.services.pdf_extract import extract_text_from_pdf
from app.services.ingestion import ingest_document

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])

UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
def upload_document(
    title: str = Form(...),
    regime: str = Form(...),
    language: str = Form(...),
    doc_type: str = Form(...),
    source_url: str | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text_from_pdf(str(file_path))
    if not text.strip():
        raise HTTPException(status_code=400, detail="No extractable text found in PDF")

    doc = ingest_document(
        db=db,
        text=text,
        title=title,
        regime=regime,
        language=language,
        doc_type=doc_type,
        source_url=source_url,
    )
    return {
        "id": doc.id,
        "title": doc.title,
        "status": doc.status,
        "chunk_count": doc.chunk_count,
    }

@router.get("")
def list_documents(regime: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Document)
    if regime:
        query = query.filter(Document.regime == regime)
    return query.all()