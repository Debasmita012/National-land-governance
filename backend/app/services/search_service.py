from typing import List, Dict

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


class SearchService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    def search(
        self,
        query: str,
        n_results: int = 5
    ) -> List[Dict]:
        """
        Perform semantic search over stored documents.
        """

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        query_embedding = (
            self.embedding_service.generate_embedding(query)
        )

        results = self.vector_service.search(
            query_embedding=query_embedding,
            n_results=n_results
        )

        formatted_results = []

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for i, document in enumerate(documents):

            formatted_results.append(
                {
                    "text": document,
                    "metadata": metadatas[i],
                    "distance": distances[i]
                }
            )

        return formatted_results