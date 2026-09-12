from backend.database import SessionLocal

from ai.ingestion.document_ingestion_service import (
    DocumentIngestionService
)


db = SessionLocal()

try:

    service = DocumentIngestionService()

    result = service.ingest_pdf(
        db=db,
        file_path="data/documents/test.pdf",
        document_title=(
            "Land Governance Test Document"
        ),
        source="Test PDF"
    )

    print("\nDOCUMENT INGESTION")
    print("=" * 60)

    print("\nDocument ID:")
    print(result["document_id"])

    print("\nDocument title:")
    print(result["document_title"])

    print("\nSource:")
    print(result["source"])

    print("\nCharacters extracted:")
    print(result["characters_extracted"])

    print("\nCharacters after cleaning:")
    print(result["characters_after_cleaning"])

    print("\nChunks created:")
    print(result["chunks_created"])

    print("\nEmbeddings created:")
    print(result["embeddings_created"])

    print("\nVector storage:")
    print(result["vector_storage"])

finally:

    db.close()