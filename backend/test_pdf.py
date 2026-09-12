from app.services.pdf_service import (
    extract_text_from_pdf,
    get_pdf_page_count
)


PDF_PATH = "../data/documents/test.pdf"


try:
    page_count = get_pdf_page_count(PDF_PATH)

    print(f"PDF pages: {page_count}")

    text = extract_text_from_pdf(PDF_PATH)

    print("\nExtracted text:")
    print("=" * 60)
    print(text[:3000])
    print("=" * 60)

except Exception as e:
    print(f"Error: {e}")