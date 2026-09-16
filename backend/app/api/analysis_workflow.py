from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.dependencies import AuthenticatedUser, require_doctor
from app.schemas.ai import (
    GroundedResponse,
    GroundedResponseRequest,
    ReviewAnalysisRequest,
    ReviewAnalysisResponse,
)
from app.schemas.ocr import OCRProcessResponse, OCRWorkflowResponse
from app.schemas.rag import RAGRetrievalRequest, RAGRetrievalResponse
from app.services.ai_service import generate_grounded_response
from app.services.audit_service import log_audit_event
from app.services.emergency_service import get_doctor_access_mode
from app.services.ocr_nlu_adapter import process_file
from app.services.rag_service import retrieve_historical_records
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()

ALLOWED_MIME_TYPES = {"application/pdf", "image/png", "image/jpeg", "image/jpg"}
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


def _require_patient_context(client, current_user: AuthenticatedUser, patient_id: str) -> str:
    if current_user.role != "DOCTOR" or not current_user.doctor_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Doctor access is required.")
    mode = get_doctor_access_mode(client, current_user.doctor_id, patient_id)
    if not mode:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Doctor has no active access to this patient.")
    return mode


def _require_normal_patient_context(client, current_user: AuthenticatedUser, patient_id: str) -> str:
    mode = _require_patient_context(client, current_user, patient_id)
    if mode != "NORMAL":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This workflow step requires active NORMAL_ACCESS; break-glass access is read-only.",
        )
    return mode


def _reviewable_findings(ocr_findings: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Convert deterministic NLU candidate facts into the review schema."""
    facts = ((ocr_findings or {}).get("nlu") or {}).get("candidate_facts", [])
    result = {"allergies": [], "conditions": [], "medications": [], "events": []}
    for fact in facts:
        if not isinstance(fact, dict):
            continue
        value = fact.get("value") or fact.get("name")
        if not value:
            continue
        entity_type = str(fact.get("entity_type", "")).upper()
        evidence = fact.get("evidence")
        if entity_type == "ALLERGY":
            result["allergies"].append({"allergen": value, "evidence": evidence})
        elif entity_type == "CONDITION":
            result["conditions"].append({"name": value, "evidence": evidence})
        elif entity_type == "MEDICATION":
            item = {"name": value, "evidence": evidence}
            for source, target in (("dose", "dosage"), ("frequency", "frequency"), ("route", "route")):
                if fact.get(source) is not None:
                    item[target] = fact[source]
            result["medications"].append(item)
        elif entity_type in {"PROCEDURE", "EVENT"}:
            result["events"].append({"title": value, "description": evidence or "Extracted from uploaded document"})
    return result


@router.post("/ocr", response_model=OCRWorkflowResponse)
async def ocr_and_nlu(
    file: Optional[UploadFile] = File(None),
    patient_id: str = Form(...),
    document_id: Optional[str] = Form(None),
    document_date: Optional[str] = Form(None),
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """Run OCR followed by suggestion-only deterministic NLU for one authorized patient."""
    client = get_supabase_service_client()
    mode = _require_normal_patient_context(client, current_user, patient_id)

    filename = "medical_document"
    content_type = "application/octet-stream"
    file_bytes = b""
    if document_id:
        doc_res = client.table("medical_documents").select("*").eq("document_id", document_id).eq("patient_id", patient_id).execute()
        if not doc_res.data:
            raise HTTPException(status_code=404, detail="Document not found for this patient.")
        doc = doc_res.data[0]
        storage_path = doc.get("file_url", "")
        filename = doc.get("title") or Path(storage_path).name or filename
        # User-facing titles often have no extension. Preserve the uploaded
        # storage extension so OCR selects the correct parser.
        if not Path(filename).suffix and Path(storage_path).suffix:
            filename = f"{filename}{Path(storage_path).suffix}"
        content_type = "application/pdf" if Path(storage_path).suffix.lower() == ".pdf" else content_type
        file_bytes = client.storage.from_("medical-documents").download(storage_path)
    elif file:
        filename = file.filename or filename
        content_type = file.content_type or content_type
        ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if content_type not in ALLOWED_MIME_TYPES and ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Unsupported medical document type.")
        file_bytes = await file.read()
    else:
        raise HTTPException(status_code=400, detail="Provide either file or document_id.")

    if not file_bytes:
        raise HTTPException(status_code=400, detail="The medical document is empty or unavailable.")

    try:
        pipeline_result = process_file(file_bytes, filename, document_id or patient_id)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="OCR-NLU processing service is unavailable.") from exc

    ocr_data = pipeline_result["ocr"]
    nlu_data = pipeline_result["nlu"]
    if document_id and ocr_data["status"] == "COMPLETED":
        client.table("medical_documents").update({
            "extracted_text": ocr_data["text"],
            "ocr_status": "COMPLETED",
        }).eq("document_id", document_id).execute()
    ocr = OCRProcessResponse(
        extracted_text=ocr_data["text"],
        filename=filename,
        content_type=content_type,
        char_count=len(ocr_data["text"]),
        word_count=len(ocr_data["text"].split()),
        ocr_status=ocr_data["status"],
        confidence_score=ocr_data["confidence"] or 0.0,
        document_date=document_date,
        metadata={"access_mode": mode, **(ocr_data.get("metadata") or {})},
    )
    log_audit_event(client, current_user.user_id, "DOCTOR", patient_id, "OCR_REQUEST", mode, "DOCUMENT", document_id)
    return OCRWorkflowResponse(document_id=document_id, ocr=ocr, nlu=nlu_data)


@router.post("/rag", response_model=RAGRetrievalResponse)
def rag_retrieval(payload: RAGRetrievalRequest, current_user: AuthenticatedUser = Depends(require_doctor)):
    client = get_supabase_service_client()
    return retrieve_historical_records(client, current_user.doctor_id, payload.patient_id, payload.query, payload.max_sources or 5)


@router.post("/response", response_model=GroundedResponse)
def grounded_response(payload: GroundedResponseRequest, current_user: AuthenticatedUser = Depends(require_doctor)):
    client = get_supabase_service_client()
    mode = _require_patient_context(client, current_user, payload.patient_id)
    document_id = payload.document_id or (payload.ocr_findings or {}).get("document_id")
    if not payload.ocr_findings and not payload.rag_retrievals:
        raise HTTPException(status_code=400, detail="At least one of ocr_findings or rag_retrievals is required.")
    result = generate_grounded_response(
        payload.patient_id,
        payload.doctor_query,
        payload.ocr_findings,
        payload.rag_retrievals,
    )
    analysis_id = None
    if document_id:
        findings = _reviewable_findings(payload.ocr_findings)
        now_utc = datetime.now(timezone.utc).isoformat()
        analysis_payload = {
            "document_id": document_id,
            "patient_id": payload.patient_id,
            "analysis_status": "COMPLETED",
            "extracted_data": findings,
            "critical_findings": [],
            "new_findings": [],
            "conflicts": result.get("conflicts", []),
            "ai_summary": result["response"],
            "confidence_score": 0.95 if result.get("model") != "deterministic-fallback" else 0.0,
            "review_status": "PENDING",
            "reviewed_by": None,
            "reviewed_at": None,
            "created_at": now_utc,
        }
        existing = client.table("document_analysis").select("analysis_id").eq("document_id", document_id).execute()
        if existing.data:
            analysis_id = str(existing.data[0]["analysis_id"])
            client.table("document_analysis").update(analysis_payload).eq("analysis_id", analysis_id).execute()
        else:
            inserted = client.table("document_analysis").insert(analysis_payload).execute()
            analysis_id = str(inserted.data[0]["analysis_id"])
    log_audit_event(client, current_user.user_id, "DOCTOR", payload.patient_id, "AI_RESPONSE", mode, "AI_RESPONSE", details={"query": payload.doctor_query})
    return GroundedResponse(
        analysis_id=analysis_id,
        document_id=document_id,
        patient_id=payload.patient_id,
        doctor_query=payload.doctor_query,
        response=result["response"],
        evidence_used=result["evidence_used"],
        review_status="PENDING" if analysis_id else "NOT_CREATED",
        model=result["model"],
    )


class ReviewWorkflowRequest(ReviewAnalysisRequest):
    analysis_id: str


@router.post("/review", response_model=ReviewAnalysisResponse)
def review(payload: ReviewWorkflowRequest, current_user: AuthenticatedUser = Depends(require_doctor)):
    # Reuse the existing guarded review implementation. It rejects BREAK_GLASS
    # before any authoritative write.
    from app.api.analysis import review_document_analysis
    return review_document_analysis(payload.analysis_id, payload, current_user)
