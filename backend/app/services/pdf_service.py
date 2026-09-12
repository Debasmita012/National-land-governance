import fitz
from pathlib import Path


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from all pages of a PDF file.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted text as a single string.
    """

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            "The provided file is not a PDF."
        )

    extracted_pages = []

    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            if text.strip():
                extracted_pages.append(
                    f"\n--- Page {page_number} ---\n{text.strip()}"
                )

    return "\n".join(extracted_pages).strip()


def get_pdf_page_count(file_path: str) -> int:
    """
    Return the number of pages in a PDF.
    """

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    with fitz.open(pdf_path) as document:
        return len(document)