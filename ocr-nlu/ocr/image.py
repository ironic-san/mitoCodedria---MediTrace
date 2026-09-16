from pathlib import Path

import cv2
import pytesseract

from .engine import OCRResult
from .preprocessing import preprocess_image


def extract_text_from_image(
    file_path: Path,
    document_id: str,
) -> OCRResult:

    image = cv2.imread(str(file_path))

    if image is None:
        return OCRResult(
            document_id=document_id,
            file_path=str(file_path),
            extracted_text="",
            confidence=None,
            status="FAILED",
            metadata={"error": "Unable to read image"},
        )

    processed_image = preprocess_image(image)

    # Get OCR text
    text = pytesseract.image_to_string(
        processed_image,
        config="--psm 6",
    ).strip()

    # Get word-level confidence scores
    data = pytesseract.image_to_data(
        processed_image,
        config="--psm 6",
        output_type=pytesseract.Output.DICT,
    )

    confidences = []

    for confidence in data["conf"]:
        try:
            value = float(confidence)

            # Tesseract uses negative values when confidence is unavailable
            if value >= 0:
                confidences.append(value)

        except (ValueError, TypeError):
            continue

    average_confidence = (
        sum(confidences) / len(confidences)
        if confidences
        else None
    )

    return OCRResult(
        document_id=document_id,
        file_path=str(file_path),
        extracted_text=text,
        confidence=average_confidence,
        status="COMPLETED",
        metadata={
            "source_type": "image",
            "ocr_engine": "tesseract",
            "confidence_unit": "percentage",
            "confidence_word_count": len(confidences),
        },
    )