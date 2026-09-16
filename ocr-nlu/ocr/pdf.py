from pathlib import Path

import pytesseract
from pypdf import PdfReader
from pdf2image import convert_from_path

from .engine import OCRResult


def _calculate_confidence(image) -> float | None:
    """Calculate average word-level Tesseract confidence."""

    data = pytesseract.image_to_data(
        image,
        config="--psm 6",
        output_type=pytesseract.Output.DICT,
    )

    confidences = []

    for confidence in data["conf"]:
        try:
            value = float(confidence)

            if value >= 0:
                confidences.append(value)

        except (ValueError, TypeError):
            continue

    if not confidences:
        return None

    return sum(confidences) / len(confidences)


def extract_text_from_pdf(
    file_path: Path,
    document_id: str,
) -> OCRResult:

    # ---------------------------------------------------------
    # First attempt: extract existing PDF text
    # ---------------------------------------------------------
    try:
        reader = PdfReader(str(file_path))

        pages_text = []

        for page in reader.pages:
            text = page.extract_text() or ""
            pages_text.append(text)

        extracted_text = "\n".join(pages_text).strip()

        # Digital/text-based PDF
        if extracted_text:
            return OCRResult(
                document_id=document_id,
                file_path=str(file_path),
                extracted_text=extracted_text,
                confidence=None,
                status="COMPLETED",
                metadata={
                    "source_type": "digital_pdf",
                    "ocr_engine": "pypdf",
                    "page_count": len(reader.pages),
                },
            )

    except Exception as exc:
        return OCRResult(
            document_id=document_id,
            file_path=str(file_path),
            extracted_text="",
            confidence=None,
            status="FAILED",
            metadata={
                "error": f"PDF text extraction failed: {exc}"
            },
        )

    # ---------------------------------------------------------
    # No text found → treat as scanned PDF
    # ---------------------------------------------------------
    try:
        images = convert_from_path(str(file_path))

        page_text = []
        page_confidences = []

        for page_number, image in enumerate(images, start=1):

            text = pytesseract.image_to_string(
                image,
                config="--psm 6",
            ).strip()

            confidence = _calculate_confidence(image)

            if confidence is not None:
                page_confidences.append(confidence)

            page_text.append(
                f"[Page {page_number}]\n{text}"
            )

        extracted_text = "\n\n".join(page_text).strip()

        document_confidence = (
            sum(page_confidences) / len(page_confidences)
            if page_confidences
            else None
        )

        return OCRResult(
            document_id=document_id,
            file_path=str(file_path),
            extracted_text=extracted_text,
            confidence=document_confidence,
            status="COMPLETED",
            metadata={
                "source_type": "scanned_pdf",
                "ocr_engine": "tesseract",
                "page_count": len(images),
                "confidence_unit": "percentage",
            },
        )

    except Exception as exc:
        return OCRResult(
            document_id=document_id,
            file_path=str(file_path),
            extracted_text="",
            confidence=None,
            status="FAILED",
            metadata={
                "error": f"Scanned PDF OCR failed: {exc}"
            },
        )