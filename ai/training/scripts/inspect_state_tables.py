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


# These pages are where the state-wise tables appear.
PAGES_TO_INSPECT = list(range(142, 157))


def main():

    print("=" * 100)
    print("STATE-WISE LAND USE TABLE INSPECTION")
    print("=" * 100)

    reader = PdfReader(str(PDF_PATH))

    print(f"\nPDF pages: {len(reader.pages)}")

    for page_number in PAGES_TO_INSPECT:

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

        print(text[:15000])

    print("\n")
    print("=" * 100)
    print("STATE TABLE INSPECTION COMPLETE")
    print("=" * 100)


if __name__ == "__main__":
    main()