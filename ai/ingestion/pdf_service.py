import pymupdf


class PDFService:

    def extract_text(self, file_path: str) -> str:

        if not file_path:
            raise ValueError(
                "PDF file path cannot be empty."
            )

        try:

            document = pymupdf.open(file_path)

            pages_text = []

            for page in document:
                text = page.get_text()

                if text:
                    pages_text.append(text)

            document.close()

            extracted_text = "\n".join(
                pages_text
            )

            return extracted_text

        except Exception as error:

            raise RuntimeError(
                f"Failed to extract text from PDF: {error}"
            )