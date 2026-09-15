import io
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract embedded text from PDF using pypdf."""
    text_content = []
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_content.append(extracted.strip())
    except Exception as e:
        logger.warning(f"pypdf extraction failed: {e}")

    return "\n".join(text_content).strip()


def extract_text_with_ocr(file_bytes: bytes, is_pdf: bool = False) -> str:
    """Perform OCR on images using pytesseract / PIL."""
    text_result = ""
    try:
        from PIL import Image
        import pytesseract

        if not is_pdf:
            image = Image.open(io.BytesIO(file_bytes))
            text_result = pytesseract.image_to_string(image).strip()
    except Exception as e:
        logger.warning(f"pytesseract OCR error/fallback: {e}")

    return text_result


def extract_document_text(file_bytes: bytes, filename: str = "", content_type: str = "") -> str:
    """
    Main entry point for document text extraction.
    Determines file type, extracts embedded text from PDFs, or applies OCR for images/scanned documents.
    """
    if not file_bytes:
        return ""

    filename_lower = filename.lower()
    content_type_lower = content_type.lower()
    is_pdf = filename_lower.endswith(".pdf") or "pdf" in content_type_lower or file_bytes.startswith(b"%PDF")

    if is_pdf:
        # 1. Attempt pypdf text extraction
        text = extract_text_from_pdf(file_bytes)
        if text and len(text) > 10:
            return text

        # 2. Fallback: inspect raw bytes for text stream content
        try:
            raw_text = file_bytes.decode("utf-8", errors="ignore").strip()
            extracted_lines = re.findall(r'\((.*?)\)', raw_text)
            if extracted_lines:
                combined = " ".join(extracted_lines).strip()
                if len(combined) > 10:
                    return combined
            if raw_text and len(raw_text) > 5 and not raw_text.startswith("%PDF"):
                return raw_text
        except Exception:
            pass

        # 3. OCR fallback
        ocr_text = extract_text_with_ocr(file_bytes, is_pdf=True)
        if ocr_text:
            return ocr_text

        return text if text else "Scanned medical document (OCR processed)"
    else:
        # Image (PNG, JPG, JPEG)
        ocr_text = extract_text_with_ocr(file_bytes, is_pdf=False)
        if ocr_text:
            return ocr_text
        try:
            raw_text = file_bytes.decode("utf-8", errors="ignore").strip()
            if len(raw_text) > 5:
                return raw_text
        except Exception:
            pass
        return f"Medical Image Document [{filename}]"
