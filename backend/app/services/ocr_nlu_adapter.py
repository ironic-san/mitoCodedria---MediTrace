"""Adapter for the repository-local OCR-NLU package.

This is the only backend boundary that knows where the OCR-NLU package lives.
The package itself is deterministic and has no Supabase/database dependency.
"""
from pathlib import Path
import os
import sys
import tempfile
from typing import Any, Dict


def _load_pipeline():
    package_root = Path(__file__).resolve().parents[3] / "ocr-nlu"
    if not package_root.exists():
        raise RuntimeError("The repository-local OCR-NLU package is missing.")
    package_root_text = str(package_root)
    if package_root_text not in sys.path:
        sys.path.insert(0, package_root_text)
    from ocr.engine import OCREngine, OCRResult
    from nlu.pipeline import NLUPipeline
    return OCREngine, OCRResult, NLUPipeline


def _serialize(ocr_result: Any, nlu_result: Any) -> Dict[str, Any]:
    confidence = ocr_result.confidence
    normalized_confidence = None if confidence is None else (confidence / 100 if confidence > 1 else confidence)
    return {
        "ocr": {
            "document_id": ocr_result.document_id,
            "text": ocr_result.extracted_text,
            "confidence": normalized_confidence,
            "confidence_percent": confidence,
            "status": ocr_result.status,
            "metadata": ocr_result.metadata,
        },
        "nlu": nlu_result.model_dump(mode="json"),
    }


def process_file(file_bytes: bytes, filename: str, document_id: str = "backend-upload") -> Dict[str, Any]:
    """Run the repository-local OCR engine and NLU pipeline on uploaded bytes."""
    OCREngine, _OCRResult, _NLUPipeline = _load_pipeline()
    suffix = Path(filename or "medical_document").suffix or ".bin"
    temp_fd, temp_path = tempfile.mkstemp(suffix=suffix)
    os.close(temp_fd)
    try:
        # Windows does not allow the PDF/image reader to reopen a file that is
        # still held open by NamedTemporaryFile. Write, close, then process.
        with open(temp_path, "wb") as handle:
            handle.write(file_bytes)
        ocr_result = OCREngine().process(temp_path, document_id)
    finally:
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass
    return _serialize(ocr_result, _NLUPipeline().process(ocr_result))


def process_text(text: str, document_id: str = "backend-text", metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Run only the repository-local NLU pipeline over already extracted text."""
    _OCREngine, OCRResult, NLUPipeline = _load_pipeline()
    ocr_result = OCRResult(
        document_id=document_id,
        file_path="",
        extracted_text=text,
        confidence=None,
        status="COMPLETED",
        metadata=metadata or {},
    )
    return _serialize(ocr_result, NLUPipeline().process(ocr_result))
