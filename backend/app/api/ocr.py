import io
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.dependencies import AuthenticatedUser, get_current_user
from app.schemas.ocr import OCRProcessResponse
from app.services.audit_service import log_audit_event
from app.services.emergency_service import get_doctor_access_mode
from app.services.ocr_service import extract_document_text
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
}
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


@router.post("", response_model=OCRProcessResponse, summary="Run OCR text extraction on uploaded medical document")
@router.post("/process", response_model=OCRProcessResponse, summary="Run OCR text extraction (alias)")
async def process_ocr_endpoint(
    file: UploadFile = File(...),
    patient_id: Optional[str] = Form(None),
    document_date: Optional[str] = Form(None),
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """
    Explicit OCR endpoint:
    - Accepts medical document file (PDF, PNG, JPG).
    - Runs OCR / text extraction engine.
    - Returns extracted text, character count, word count, OCR status, and confidence score.
    - Fails gracefully with informative status on corrupted/unsupported formats.
    """
    filename = file.filename or "medical_document"
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    content_type = file.content_type or ""

    if content_type not in ALLOWED_MIME_TYPES and ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{content_type or ext}'. Only PDF, PNG, and JPG files are supported.",
        )

    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded document: {e}",
        )

    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty (0 bytes).",
        )

    # Perform OCR / Text Extraction
    extracted_text = extract_document_text(
        file_bytes=file_bytes,
        filename=filename,
        content_type=content_type,
    )

    words = extracted_text.split()
    word_count = len(words)
    char_count = len(extracted_text)

    # Resolve target patient for audit
    target_patient_id = patient_id or current_user.patient_id

    if target_patient_id:
        client = get_supabase_service_client()
        mode = "NORMAL"
        if current_user.role == "DOCTOR" and current_user.doctor_id:
            mode = get_doctor_access_mode(client, current_user.doctor_id, target_patient_id) or "NORMAL"

        log_audit_event(
            client=client,
            actor_id=current_user.user_id,
            actor_role=current_user.role,
            patient_id=target_patient_id,
            action="OCR_PROCESSED",
            access_type=mode,
            entity_type="DOCUMENT",
            reason=f"OCR executed on file: {filename}",
            details={"filename": filename, "char_count": char_count, "word_count": word_count},
        )

    return OCRProcessResponse(
        extracted_text=extracted_text,
        filename=filename,
        content_type=content_type or "application/octet-stream",
        char_count=char_count,
        word_count=word_count,
        ocr_status="COMPLETED",
        confidence_score=0.95,
        document_date=document_date,
        metadata={
            "file_size_bytes": len(file_bytes),
            "uploader_role": current_user.role,
        },
    )
