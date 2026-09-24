from pathlib import Path
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


def inspect_pdf(pdf_path: Path):
    print("\n" + "=" * 80)
    print(f"FILE: {pdf_path.name}")
    print("=" * 80)

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        print(f"ERROR opening PDF: {exc}")
        return

    print(f"Pages: {len(reader.pages)}")

    # Inspect first few pages
    pages_to_check = min(5, len(reader.pages))

    for index in range(pages_to_check):
        print("\n" + "-" * 80)
        print(f"PAGE {index + 1}")
        print("-" * 80)

        try:
            text = reader.pages[index].extract_text() or ""
        except Exception as exc:
            print(f"ERROR extracting page: {exc}")
            continue

        # Keep output manageable
        text = text[:5000]

        print(text)

    print("\n" + "=" * 80)


def main():
    print("=" * 80)
    print("OFFICIAL LAND USE PDF INSPECTOR")
    print("=" * 80)

    if not LAND_USE_DIR.exists():
        raise FileNotFoundError(
            f"Land-use directory not found:\n{LAND_USE_DIR}"
        )

    pdf_files = sorted(
        LAND_USE_DIR.glob("*.pdf")
    )

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in:\n{LAND_USE_DIR}"
        )

    print(f"\nFound {len(pdf_files)} PDF file(s).")

    for pdf_path in pdf_files:
        inspect_pdf(pdf_path)

    print("\nInspection completed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nINSPECTION FAILED")
        print(str(exc))
        sys.exit(1)
