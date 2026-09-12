from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.models.base_models import Document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/")
def create_document(
    title: str,
    source: str | None = None,
    file_path: str | None = None,
    document_type: str | None = None,
    text_content: str | None = None,
    db: Session = Depends(get_db)
):
    document = Document(
        title=title,
        source=source,
        file_path=file_path,
        document_type=document_type,
        text_content=text_content
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "message": "Document created successfully",
        "document": {
            "id": document.id,
            "title": document.title,
            "source": document.source,
            "file_path": document.file_path,
            "document_type": document.document_type
        }
    }


@router.get("/")
def get_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).order_by(Document.id).all()

    return [
        {
            "id": document.id,
            "title": document.title,
            "source": document.source,
            "file_path": document.file_path,
            "document_type": document.document_type
        }
        for document in documents
    ]


@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "id": document.id,
        "title": document.title,
        "source": document.source,
        "file_path": document.file_path,
        "document_type": document.document_type,
        "text_content": document.text_content
    }