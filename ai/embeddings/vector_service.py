import chromadb
from typing import List
from pathlib import Path


# Project root:
# national-land-governance/

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHROMA_PATH = str(
    PROJECT_ROOT / "data" / "vector_db"
)

COLLECTION_NAME = "land_governance_documents"


class VectorService:

    def __init__(self):

        # Make sure the directory exists
        Path(CHROMA_PATH).mkdir(
            parents=True,
            exist_ok=True
        )

        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=COLLECTION_NAME
            )
        )

    def add_documents(
        self,
        chunks,
        embeddings,
        document_id,
        document_title
    ):

        if not chunks:
            raise ValueError(
                "No chunks provided."
            )

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match."
            )

        ids = [
            f"document_{document_id}_chunk_{i}"
            for i in range(len(chunks))
        ]

        metadatas = [
            {
                "document_id": document_id,
                "document_title": document_title,
                "chunk_index": i
            }
            for i in range(len(chunks))
        ]

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return {
            "message": "Document chunks stored successfully",
            "chunks_stored": len(chunks)
        }

    def search(
        self,
        query_embedding,
        n_results=5
    ):

        if not query_embedding:
            raise ValueError(
                "Query embedding cannot be empty."
            )

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def count(self):

        return self.collection.count()