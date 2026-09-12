import chromadb
from typing import List, Dict


CHROMA_PATH = "../../data/vector_db"
COLLECTION_NAME = "land_governance_documents"


class VectorService:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    def add_documents(
        self,
        chunks: List[str],
        embeddings: List[List[float]],
        document_id: int,
        document_title: str
    ):
        """
        Store document chunks and embeddings.
        """

        if not chunks:
            raise ValueError("No chunks provided.")

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
        query_embedding: List[float],
        n_results: int = 5
    ) -> Dict:
        """
        Search for semantically similar document chunks.
        """

        if not query_embedding:
            raise ValueError("Query embedding cannot be empty.")

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    def count(self) -> int:
        """
        Return total stored chunks.
        """

        return self.collection.count()