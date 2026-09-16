from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class OCRResult:
    document_id: str
    file_path: str
    extracted_text: str
    confidence: float | None
    status: str
    metadata: dict[str, Any] = field(default_factory=dict)


class OCREngine:
    """
    Main OCR interface for MediTrace.

    The rest of the application should interact with this class
    instead of directly calling an OCR library.
    """

    def process(
        self,
        file_path: str | Path,
        document_id: str,
    ) -> OCRResult:
        """
        Process a medical document and return OCR results.
        """

        path = Path(file_path)

        if not path.exists():
            return OCRResult(
                document_id=document_id,
                file_path=str(path),
                extracted_text="",
                confidence=None,
                status="FAILED",
                metadata={"error": "File not found"},
            )

        suffix = path.suffix.lower()

        if suffix in {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}:
            from .image import extract_text_from_image

            return extract_text_from_image(
                path,
                document_id,
            )

        if suffix == ".pdf":
            from .pdf import extract_text_from_pdf

            return extract_text_from_pdf(
                path,
                document_id,
            )

        return OCRResult(
            document_id=document_id,
            file_path=str(path),
            extracted_text="",
            confidence=None,
            status="FAILED",
            metadata={
                "error": f"Unsupported file type: {suffix}"
            },
        )