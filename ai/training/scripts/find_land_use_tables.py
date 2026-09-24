from pathlib import Path
import re
import sys

from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[3]

LAND_USE_DIR = (
    PROJECT_ROOT
    / "ai"
    / "training"
    / "data"
    / "land_use"
)

KEYWORDS = [
    "LAND USE CLASSIFICATION",
    "land use classification",
    "STATE/UT",
    "State/UT",
    "district",
    "District",
    "Agricultural Area",
    "Forest",
    "Non-Agricultural",
    "Barren",
    "Net Area Sown",
    "Irrigated",
]


def inspect_file(pdf_path):
    print("\n" + "=" * 90)
    print(pdf_path.name)
    print("=" * 90)

    reader = PdfReader(str(pdf_path))

    matches = []

    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            continue

        text_lower = text.lower()

        found = []

        for keyword in KEYWORDS:
            if keyword.lower() in text_lower:
                found.append(keyword)

        if found:
            matches.append(
                (page_number, found, text)
            )

    print(f"Pages containing relevant terms: {len(matches)}")

    for page_number, found, text in matches:
        print("\n" + "-" * 90)
        print(f"PAGE {page_number}")
        print("MATCHES:", ", ".join(found))
        print("-" * 90)

        # Print a compact preview
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        preview = "\n".join(lines[:35])

        print(preview)


def main():
    print("=" * 90)
    print("LAND USE TABLE DISCOVERY")
    print("=" * 90)

    pdf_files = sorted(LAND_USE_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDFs found in {LAND_USE_DIR}"
        )

    for pdf_path in pdf_files:
        inspect_file(pdf_path)

    print("\n" + "=" * 90)
    print("TABLE DISCOVERY COMPLETE")
    print("=" * 90)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nFAILED")
        print(exc)
        sys.exit(1)