import re
from typing import List


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.

    Removes excessive whitespace, repeated blank lines,
    and common formatting artifacts.
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces before/after newlines
    text = re.sub(r" *\n *", "\n", text)

    # Collapse more than two consecutive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Cleaned document text.
        chunk_size: Maximum approximate character size of each chunk.
        chunk_overlap: Number of characters shared between chunks.

    Returns:
        List of text chunks.
    """

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - chunk_overlap

    return chunks