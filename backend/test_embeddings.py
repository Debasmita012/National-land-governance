from app.services.embedding_service import EmbeddingService


service = EmbeddingService()


text = """
Land governance involves the management, regulation,
and administration of land resources and land-use systems.
"""


embedding = service.generate_embedding(text)


print("\nEmbedding generated successfully!")
print("Embedding dimensions:", len(embedding))
print("First 10 values:")
print(embedding[:10])