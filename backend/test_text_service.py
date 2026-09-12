from app.services.pdf_service import extract_text_from_pdf
from app.services.text_service import clean_text, chunk_text


PDF_PATH = "../data/documents/test.pdf"


# Extract PDF text
raw_text = extract_text_from_pdf(PDF_PATH)

print(f"Raw text length: {len(raw_text)} characters")


# Clean text
cleaned_text = clean_text(raw_text)

print(f"Cleaned text length: {len(cleaned_text)} characters")


# Create chunks
chunks = chunk_text(
    cleaned_text,
    chunk_size=1000,
    chunk_overlap=200
)

print(f"Number of chunks: {len(chunks)}")


# Display first three chunks
for index, chunk in enumerate(chunks[:3], start=1):
    print("\n" + "=" * 60)
    print(f"CHUNK {index}")
    print("=" * 60)
    print(chunk)