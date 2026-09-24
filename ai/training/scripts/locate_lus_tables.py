from pathlib import Path
from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[3]

LAND_USE_DIR = (
    PROJECT_ROOT
    / "ai"
    / "training"
    / "data"
    / "land_use"
)


SEARCH_TERMS = [
    "TABLE",
    "LAND USE CLASSIFICATION",
    "LAND USE",
    "AREA UNDER DIFFERENT LAND USE",
    "NET AREA SOWN",
    "FOREST",
    "NON-AGRICULTURAL",
]


def find_matches(pdf_path):
    print("\n" + "=" * 80)
    print(pdf_path.name)
    print("=" * 80)

    reader = PdfReader(str(pdf_path))

    for page_number, page in enumerate(reader.pages, start=1):

        try:
            text = page.extract_text() or ""
        except Exception:
            continue

        normalized = " ".join(
            text.upper().split()
        )

        matches = []

        for term in SEARCH_TERMS:
            if term in normalized:
                matches.append(term)

        if matches:
            print(
                f"Page {page_number:3d} -> "
                + ", ".join(matches)
            )


def main():
    print("=" * 80)
    print("LAND USE STATISTICS TABLE LOCATOR")
    print("=" * 80)

    pdf_files = sorted(
        LAND_USE_DIR.glob("*.pdf")
    )

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDFs found in {LAND_USE_DIR}"
        )

    for pdf in pdf_files:
        find_matches(pdf)

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)


if __name__ == "__main__":
    main()