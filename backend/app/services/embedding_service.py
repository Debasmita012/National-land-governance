from sentence_transformers import SentenceTransformer
from typing import List


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingService:
    def __init__(self):
        print(f"Loading embedding model: {MODEL_NAME}")
        self.model = SentenceTransformer(MODEL_NAME)
        print("Embedding model loaded successfully!")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Convert a single text string into an embedding vector.
        """

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        embedding = self.model.encode(
            text,
            convert_to_numpy=True
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Convert multiple text chunks into embedding vectors.
        """

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        return embeddings.tolist()