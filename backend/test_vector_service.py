from app.services.pdf_service import extract_text_from_pdf
from app.services.text_service import clean_text, chunk_text
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


PDF_PATH = "../data/documents/test.pdf"


# 1. Extract PDF text
raw_text = extract_text_from_pdf(PDF_PATH)

# 2. Clean text
cleaned_text = clean_text(raw_text)

# 3. Create chunks
chunks = chunk_text(
    cleaned_text,
    chunk_size=1000,
    chunk_overlap=200
)

print(f"Chunks created: {len(chunks)}")


# 4. Generate embeddings
embedding_service = EmbeddingService()

embeddings = embedding_service.generate_embeddings(
    chunks
)

print(f"Embeddings created: {len(embeddings)}")


# 5. Store in ChromaDB
vector_service = VectorService()

result = vector_service.add_documents(
    chunks=chunks,
    embeddings=embeddings,
    document_id=1,
    document_title="Land Governance Test Document"
)

print(result)

print(
    f"Total chunks in vector database: "
    f"{vector_service.count()}"
)