from datetime import datetime, timezone
import logging
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.dependencies import AuthenticatedUser, get_current_user
from app.schemas.ai import DocumentAnalysisResponse
from app.schemas.document import DocumentAccessResponse, DocumentUploadResponse
from app.services.ai_service import get_ai_service
from app.services.audit_service import log_audit_event
from app.services.emergency_service import get_doctor_access_mode
from app.services.ocr_service import extract_document_text
from app.services.patient_service import (
    get_consolidated_medical_summary,
    has_valid_doctor_access,
)
from app.services.supabase_service import get_supabase_service_client

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
}

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


@router.post("/upload", response_model=DocumentUploadResponse, summary="Upload a medical document")
async def upload_document(
    file: UploadFile = File(...),
    patient_id: Optional[str] = Form(None),
    document_type: Optional[str] = Form("OTHER"),
    title: Optional[str] = Form(None),
    document_date: Optional[str] = Form(None),
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """
    Upload a medical document (PDF, PNG, JPG).
    - Patient can upload for themselves.
    - Doctor can upload ONLY if they have valid ACTIVE NORMAL access.
    - Break-glass emergency doctors are explicitly DENIED write/upload operations.
    """
    client = get_supabase_service_client()

    # 1. Resolve & authorize target patient_id
    target_patient_id = None
    if current_user.role == "PATIENT":
        target_patient_id = current_user.patient_id
        if not target_patient_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient profile not linked to authenticated user.",
            )
    elif current_user.role == "DOCTOR":
        if not patient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="patient_id parameter is required when uploading as a Doctor.",
            )

        # Check access mode
        access_mode = get_doctor_access_mode(client, current_user.doctor_id, patient_id)
        if access_mode == "BREAK_GLASS":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Break-glass emergency access does not permit uploading documents (Write operation prohibited).",
            )
        elif not access_mode or not has_valid_doctor_access(client, current_user.doctor_id, patient_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Doctor does not have valid active access to this patient.",
            )
        target_patient_id = patient_id
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Invalid user role.",
        )

    # 2. Validate file type and extension
    filename = file.filename or "uploaded_document"
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    content_type = file.content_type or ""
    if content_type not in ALLOWED_MIME_TYPES and ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{content_type or ext}'. Only PDF, PNG, and JPG files are supported.",
        )

    file_bytes = await file.read()
    if len(file_bytes) > 15 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum allowed limit of 15MB.",
        )

    # 3. Save file to Private Supabase Storage bucket 'medical-documents'
    unique_filename = f"{uuid.uuid4()}_{filename}"
    storage_path = f"{target_patient_id}/{unique_filename}"

    try:
        client.storage.from_("medical-documents").upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": content_type or "application/octet-stream"},
        )
    except Exception:
        pass

    now_utc = datetime.now(timezone.utc)
    doc_title = title.strip() if title else filename
    doc_date = document_date.strip() if document_date else now_utc.strftime("%Y-%m-%d")

    # Resolve uploader doctor_id
    if current_user.role == "DOCTOR":
        uploader_doctor_id = current_user.doctor_id
    else:
        rel_res = client.table("doctor_patient").select("doctor_id").eq("patient_id", target_patient_id).execute()
        if rel_res.data:
            uploader_doctor_id = str(rel_res.data[0]["doctor_id"])
        else:
            first_doc = client.table("doctors").select("doctor_id").limit(1).execute()
            uploader_doctor_id = str(first_doc.data[0]["doctor_id"]) if first_doc.data else "10000000-0000-0000-0000-000000000001"

    # 4. Insert record into medical_documents table
    record_payload = {
        "patient_id": target_patient_id,
        "uploaded_by": uploader_doctor_id,
        "document_type": document_type.upper() if document_type else "OTHER",
        "title": doc_title,
        "file_url": storage_path,
        "document_date": doc_date,
        "extracted_text": None,
        "ocr_status": "PENDING",
        "uploaded_at": now_utc.isoformat(),
    }

    insert_res = client.table("medical_documents").insert(record_payload).execute()
    if not insert_res.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist document metadata in database.",
        )

    created_doc = insert_res.data[0]
    doc_id = str(created_doc["document_id"])

    # Log audit event
    log_audit_event(
        client=client,
        actor_id=current_user.user_id,
        actor_role=current_user.role,
        patient_id=target_patient_id,
        action="DOCUMENT_UPLOAD",
        access_type="NORMAL",
        entity_type="DOCUMENT",
        entity_id=doc_id,
        reason=f"Uploaded medical document '{doc_title}'",
        details={"storage_path": storage_path, "document_type": document_type},
    )

    download_url = storage_path
    try:
        signed_res = client.storage.from_("medical-documents").create_signed_url(storage_path, 3600)
        if isinstance(signed_res, dict) and "signedURL" in signed_res:
            download_url = signed_res["signedURL"]
    except Exception:
        pass

    return DocumentUploadResponse(
        document_id=doc_id,
        patient_id=target_patient_id,
        uploaded_by=uploader_doctor_id,
        title=doc_title,
        document_type=created_doc.get("document_type", "OTHER"),
        storage_path=storage_path,
        document_date=created_doc.get("document_date"),
        uploaded_at=str(created_doc.get("uploaded_at")),
        status="UPLOADED",
        download_url=download_url,
    )


@router.get("/{document_id}", response_model=DocumentAccessResponse, summary="Get document metadata & signed URL")
@router.get("/{document_id}/access", response_model=DocumentAccessResponse, summary="Get document metadata & access URL")
def get_document_access(
    document_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """
    Verifies authorization and issues secure access/signed URL for a document.
    - Patient can access their own document.
    - Doctor can access if they currently have valid active normal access.
    """
    client = get_supabase_service_client()

    doc_res = client.table("medical_documents").select("*").eq("document_id", document_id).execute()
    if not doc_res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID '{document_id}' not found.",
        )

    doc_data = doc_res.data[0]
    owner_patient_id = str(doc_data["patient_id"])

    # Authorization check
    mode = "NORMAL"
    if current_user.role == "PATIENT":
        if current_user.patient_id != owner_patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Patients can only access their own documents.",
            )
    elif current_user.role == "DOCTOR":
        if not has_valid_doctor_access(client, current_user.doctor_id, owner_patient_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Doctor does not have valid active access to this patient's documents.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Invalid user role.",
        )

    raw_file_url = doc_data.get("file_url", "")
    download_url = raw_file_url

    if raw_file_url and not raw_file_url.startswith("http://") and not raw_file_url.startswith("https://") and not raw_file_url.startswith("synthetic://"):
        try:
            signed_res = client.storage.from_("medical-documents").create_signed_url(raw_file_url, 3600)
            if isinstance(signed_res, dict) and "signedURL" in signed_res:
                download_url = signed_res["signedURL"]
            elif hasattr(signed_res, "get"):
                download_url = signed_res.get("signedURL", raw_file_url)
        except Exception:
            download_url = raw_file_url

    log_audit_event(
        client=client,
        actor_id=current_user.user_id,
        actor_role=current_user.role,
        patient_id=owner_patient_id,
        action="DOCUMENT_ACCESS",
        access_type=mode,
        entity_type="DOCUMENT",
        entity_id=document_id,
        reason=f"Accessed document '{doc_data.get('title')}'",
    )

    return DocumentAccessResponse(
        document_id=str(doc_data["document_id"]),
        patient_id=owner_patient_id,
        uploaded_by=str(doc_data.get("uploaded_by")) if doc_data.get("uploaded_by") else None,
        title=doc_data.get("title", "Medical Document"),
        document_type=doc_data.get("document_type", "OTHER"),
        document_date=str(doc_data.get("document_date")) if doc_data.get("document_date") else None,
        file_url=raw_file_url,
        download_url=download_url,
        ocr_status=doc_data.get("ocr_status"),
        uploaded_at=str(doc_data.get("uploaded_at")) if doc_data.get("uploaded_at") else None,
    )


@router.post("/{document_id}/analyze", response_model=DocumentAnalysisResponse, summary="Analyze document with OCR & AI")
def analyze_document(
    document_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """
    Perform OCR/text extraction and AI analysis on a document.
    Compares extracted medical facts against patient's existing structured records.
    Stores analysis in document_analysis table with review_status='PENDING'.
    """
    client = get_supabase_service_client()

    doc_res = client.table("medical_documents").select("*").eq("document_id", document_id).execute()
    if not doc_res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID '{document_id}' not found.",
        )

    doc_data = doc_res.data[0]
    owner_patient_id = str(doc_data["patient_id"])

    # Authorization check
    mode = "NORMAL"
    if current_user.role == "PATIENT":
        if current_user.patient_id != owner_patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Patients can only analyze their own documents.",
            )
    elif current_user.role == "DOCTOR":
        if not has_valid_doctor_access(client, current_user.doctor_id, owner_patient_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Doctor does not have valid active access to this patient.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Invalid user role.",
        )

    extracted_text = doc_data.get("extracted_text")
    storage_path = doc_data.get("file_url", "")

    if not extracted_text or doc_data.get("ocr_status") != "COMPLETED":
        file_bytes = None
        if storage_path and not storage_path.startswith("synthetic://"):
            try:
                file_bytes = client.storage.from_("medical-documents").download(storage_path)
            except Exception:
                pass

        extracted_text = extract_document_text(
            file_bytes=file_bytes or b"",
            filename=doc_data.get("title", ""),
            content_type="",
        )

        client.table("medical_documents").update({
            "extracted_text": extracted_text,
            "ocr_status": "COMPLETED",
        }).eq("document_id", document_id).execute()

    patient_summary_model = get_consolidated_medical_summary(client, owner_patient_id)
    patient_summary_dict = patient_summary_model.model_dump()

    doc_meta = {
        "document_id": document_id,
        "patient_id": owner_patient_id,
        "title": doc_data.get("title"),
        "document_type": doc_data.get("document_type"),
        "document_date": doc_data.get("document_date"),
    }

    ai_service = get_ai_service()
    ai_result = ai_service.analyze_document(extracted_text, patient_summary_dict, doc_meta)

    now_utc = datetime.now(timezone.utc)

    existing_analysis = (
        client.table("document_analysis")
        .select("*")
        .eq("document_id", document_id)
        .execute()
    )

    analysis_payload = {
        "document_id": document_id,
        "patient_id": owner_patient_id,
        "analysis_status": "COMPLETED",
        "extracted_data": ai_result.extracted_data,
        "critical_findings": ai_result.critical_findings,
        "new_findings": ai_result.new_findings,
        "conflicts": ai_result.conflicts,
        "ai_summary": ai_result.summary,
        "confidence_score": ai_result.confidence_score,
        "review_status": "PENDING",
        "reviewed_by": None,
        "reviewed_at": None,
        "created_at": now_utc.isoformat(),
    }

    if existing_analysis.data:
        analysis_id = str(existing_analysis.data[0]["analysis_id"])
        client.table("document_analysis").update(analysis_payload).eq("analysis_id", analysis_id).execute()
    else:
        insert_res = client.table("document_analysis").insert(analysis_payload).execute()
        analysis_id = str(insert_res.data[0]["analysis_id"])

    log_audit_event(
        client=client,
        actor_id=current_user.user_id,
        actor_role=current_user.role,
        patient_id=owner_patient_id,
        action="DOCUMENT_ANALYZED",
        access_type=mode,
        entity_type="DOCUMENT_ANALYSIS",
        entity_id=analysis_id,
        reason=f"AI document analysis completed for '{doc_data.get('title')}'",
    )

    return DocumentAnalysisResponse(
        analysis_id=analysis_id,
        document_id=document_id,
        patient_id=owner_patient_id,
        analysis_status="COMPLETED",
        extracted_data=ai_result.extracted_data,
        critical_findings=ai_result.critical_findings,
        new_findings=ai_result.new_findings,
        conflicts=ai_result.conflicts,
        ai_summary=ai_result.summary,
        confidence_score=ai_result.confidence_score,
        review_status="PENDING",
        reviewed_by=None,
        reviewed_at=None,
        created_at=now_utc.isoformat(),
    )


@router.get("/{document_id}/analysis", response_model=DocumentAnalysisResponse, summary="Get document analysis result")
def get_document_analysis(
    document_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """
    Retrieve latest document analysis result for a document.
    """
    client = get_supabase_service_client()

    doc_res = client.table("medical_documents").select("*").eq("document_id", document_id).execute()
    if not doc_res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID '{document_id}' not found.",
        )

    doc_data = doc_res.data[0]
    owner_patient_id = str(doc_data["patient_id"])

    # Authorization check
    if current_user.role == "PATIENT":
        if current_user.patient_id != owner_patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Patients can only access their own document analysis.",
            )
    elif current_user.role == "DOCTOR":
        if not has_valid_doctor_access(client, current_user.doctor_id, owner_patient_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Doctor does not have valid active access to this patient.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Invalid user role.",
        )

    analysis_res = (
        client.table("document_analysis")
        .select("*")
        .eq("document_id", document_id)
        .execute()
    )

    if not analysis_res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No analysis found for document '{document_id}'. Run POST /documents/{document_id}/analyze first.",
        )

    an = analysis_res.data[0]
    return DocumentAnalysisResponse(
        analysis_id=str(an["analysis_id"]),
        document_id=str(an["document_id"]),
        patient_id=str(an["patient_id"]),
        analysis_status=an.get("analysis_status", "COMPLETED"),
        extracted_data=an.get("extracted_data") or {},
        critical_findings=an.get("critical_findings") or [],
        new_findings=an.get("new_findings") or [],
        conflicts=an.get("conflicts") or [],
        ai_summary=an.get("ai_summary", ""),
        confidence_score=an.get("confidence_score", 0.95),
        review_status=an.get("review_status", "PENDING"),
        reviewed_by=an.get("reviewed_by"),
        reviewed_at=an.get("reviewed_at"),
        created_at=str(an.get("created_at")),
    )
