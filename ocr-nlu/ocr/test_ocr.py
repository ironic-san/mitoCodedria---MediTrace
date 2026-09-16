from pathlib import Path
from difflib import SequenceMatcher

from .engine import OCREngine


SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"


def normalize_text(text: str) -> str:
    """Normalize text for basic PDF-vs-image comparison."""

    return " ".join(text.lower().split())


def compare_text(pdf_text: str, image_text: str) -> float:
    """Return similarity percentage between two extracted texts."""

    pdf_normalized = normalize_text(pdf_text)
    image_normalized = normalize_text(image_text)

    if not pdf_normalized:
        return 0.0

    return SequenceMatcher(
        None,
        pdf_normalized,
        image_normalized,
    ).ratio() * 100


def main():
    engine = OCREngine()

    files = sorted(
        path
        for path in SAMPLES_DIR.iterdir()
        if path.suffix.lower() in {".png", ".pdf"}
    )

    if not files:
        print("No PDF or PNG files found.")
        return

    results = {}

    # ---------------------------------------------------------
    # Process every sample
    # ---------------------------------------------------------

    for file_path in files:

        result = engine.process(
            file_path=file_path,
            document_id=file_path.stem,
        )

        # Remove the test suffix so PDF and PNG can be paired.
        base_name = file_path.stem.replace("_scanned", "")

        results.setdefault(base_name, {})[
            file_path.suffix.lower()
        ] = result

    # ---------------------------------------------------------
    # Compact comparison summary
    # ---------------------------------------------------------

    print("\n")
    print("=" * 110)
    print("OCR TEST SUMMARY")
    print("=" * 110)

    print(
        f"{'DOCUMENT':45}"
        f"{'TYPE':12}"
        f"{'CONFIDENCE':15}"
        f"{'WORDS':10}"
    )

    print("-" * 110)

    for document_name, document_results in results.items():

        for file_type in [".pdf", ".png"]:

            result = document_results.get(file_type)

            if result is None:
                continue

            word_count = len(result.extracted_text.split())

            confidence = (
                f"{result.confidence:.2f}"
                if result.confidence is not None
                else "N/A"
            )

            source_type = result.metadata.get(
                "source_type",
                "unknown",
            )

            print(
                f"{document_name[:44]:45}"
                f"{source_type[:11]:12}"
                f"{confidence:15}"
                f"{word_count:<10}"
            )

    # ---------------------------------------------------------
    # PDF vs PNG comparison
    # ---------------------------------------------------------

    print("\n")
    print("=" * 110)
    print("PDF vs PNG TEXT SIMILARITY")
    print("=" * 110)

    print(
        f"{'DOCUMENT':60}"
        f"{'SIMILARITY':15}"
        f"{'PNG CONFIDENCE':15}"
    )

    print("-" * 110)

    for document_name, document_results in results.items():

        pdf_result = document_results.get(".pdf")
        png_result = document_results.get(".png")

        if pdf_result is None or png_result is None:
            continue

        similarity = compare_text(
            pdf_result.extracted_text,
            png_result.extracted_text,
        )

        confidence = (
            f"{png_result.confidence:.2f}"
            if png_result.confidence is not None
            else "N/A"
        )

        print(
            f"{document_name[:59]:60}"
            f"{similarity:>8.2f}%       "
            f"{confidence:>8}"
        )

    print("\n")
    print("Full extracted text is intentionally omitted from the summary.")
    print("Use the OCRResult output/debugging when detailed inspection is needed.")


if __name__ == "__main__":
    main()