from typing import Dict
from pathlib import Path

from sqlalchemy.orm import Session

from ai.ingestion.pdf_service import PDFService
from ai.ingestion.text_service import TextService
from ai.embeddings.embedding_service import EmbeddingService
from ai.embeddings.vector_service import VectorService

from backend.app.models.base_models import Document

class DocumentIngestionService:

    def __init__(self):

        self.pdf_service = PDFService()
        self.text_service = TextService()
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    def ingest_pdf(
        self,
        db: Session,
        file_path: str,
        document_title: str,
        source: str = "Uploaded PDF"
    ) -> Dict:

        if not file_path:
            raise ValueError(
                "PDF file path cannot be empty."
            )

        if not document_title:
            raise ValueError(
                "Document title cannot be empty."
            )

        # -----------------------------------------
        # STEP 1 — Check PDF exists
        # -----------------------------------------

        pdf_path = Path(file_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        # -----------------------------------------
        # STEP 2 — Register document in PostgreSQL
        # -----------------------------------------

        document = Document(
            title=document_title,
            source=source
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        document_id = document.id

        try:

            # -----------------------------------------
            # STEP 3 — Extract text
            # -----------------------------------------

            extracted_text = (
                self.pdf_service.extract_text(
                    file_path
                )
            )

            if (
                not extracted_text
                or not extracted_text.strip()
            ):
                raise ValueError(
                    "No text could be extracted from PDF."
                )

            # -----------------------------------------
            # STEP 4 — Clean text
            # -----------------------------------------

            cleaned_text = (
                self.text_service.clean_text(
                    extracted_text
                )
            )

            if not cleaned_text:
                raise ValueError(
                    "PDF text is empty after cleaning."
                )

            # -----------------------------------------
            # STEP 5 — Create chunks
            # -----------------------------------------

            chunks = (
                self.text_service.chunk_text(
                    cleaned_text
                )
            )

            if not chunks:
                raise ValueError(
                    "No text chunks were created."
                )

            # -----------------------------------------
            # STEP 6 — Generate embeddings
            # -----------------------------------------

            embeddings = (
                self.embedding_service
                .generate_embeddings(
                    chunks
                )
            )

            if not embeddings:
                raise ValueError(
                    "No embeddings were generated."
                )

            # -----------------------------------------
            # STEP 7 — Store in ChromaDB
            # -----------------------------------------

            vector_result = (
                self.vector_service
                .add_documents(
                    chunks=chunks,
                    embeddings=embeddings,
                    document_id=document_id,
                    document_title=document_title
                )
            )

            # -----------------------------------------
            # STEP 8 — Return complete result
            # -----------------------------------------

            return {
                "document_id": document_id,
                "document_title": document_title,
                "source": source,
                "file_path": file_path,
                "characters_extracted": len(
                    extracted_text
                ),
                "characters_after_cleaning": len(
                    cleaned_text
                ),
                "chunks_created": len(chunks),
                "embeddings_created": len(
                    embeddings
                ),
                "vector_storage": vector_result
            }

        except Exception:

            db.rollback()

            # Remove the PostgreSQL record if
            # ingestion fails.
            db.query(Document).filter(
                Document.id == document_id
            ).delete()

            db.commit()

            raise