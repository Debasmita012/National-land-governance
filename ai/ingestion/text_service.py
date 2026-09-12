import re
from typing import List


class TextService:

    def clean_text(self, text: str) -> str:

        if not text:
            return ""

        # Replace multiple spaces/tabs with one space
        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        # Replace excessive newlines
        text = re.sub(
            r"\n\s*\n+",
            "\n\n",
            text
        )

        return text.strip()

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> List[str]:

        if not text or not text.strip():
            return []

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0."
            )

        if overlap < 0:
            raise ValueError(
                "overlap cannot be negative."
            )

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size."
            )

        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:

            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start = end - overlap

        return chunks