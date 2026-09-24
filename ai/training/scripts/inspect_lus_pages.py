from pathlib import Path
from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[3]

PDF_PATH = (
    PROJECT_ROOT
    / "ai"
    / "training"
    / "data"
    / "land_use"
    / "LUS-Publication-2024-25.pdf"
)


PAGES_TO_INSPECT = [
    13,
    65,
    66,
    69,
    70,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    110,
    118,
    119,
    120,
    122,
]


def main():

    print("=" * 100)
    print("LAND USE CLASSIFICATION TABLE INSPECTION")
    print("=" * 100)

    reader = PdfReader(str(PDF_PATH))

    print(f"\nPDF pages: {len(reader.pages)}")

    for page_number in PAGES_TO_INSPECT:

        if page_number > len(reader.pages):
            continue

        print("\n")
        print("#" * 100)
        print(f"PDF PAGE {page_number}")
        print("#" * 100)

        page = reader.pages[page_number - 1]

        try:
            text = page.extract_text() or ""
        except Exception as exc:
            print(f"ERROR: {exc}")
            continue

        print(text[:12000])

    print("\n")
    print("=" * 100)
    print("INSPECTION COMPLETE")
    print("=" * 100)


if __name__ == "__main__":
    main()