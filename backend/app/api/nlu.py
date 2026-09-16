from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import AuthenticatedUser, get_current_user
from app.schemas.ai import NLUProcessRequest, NLUProcessResponse
from app.services.audit_service import log_audit_event
from app.services.emergency_service import get_doctor_access_mode
from app.services.ocr_nlu_adapter import process_text
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()


@router.post("", response_model=NLUProcessResponse, summary="Extract structured medical findings using NLU")
@router.post("/process", response_model=NLUProcessResponse, summary="Extract structured medical findings using NLU (alias)")
def process_nlu_endpoint(
    payload: NLUProcessRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """
    Explicit NLU endpoint:
    - Input: extracted OCR text as JSON.
    - Analyzes clinical semantics, conditions, allergies, medications, procedures, events.
    - Applies standard medical term normalizations (e.g. T2DM -> Type 2 Diabetes Mellitus, BID -> twice daily).
    - Identifies critical flags and risk alerts.
    - CRITICAL: Guaranteed suggestion-only output (is_suggestion_only=True). Never writes to medical DB.
    """
    if not payload.extracted_text or len(payload.extracted_text.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="extracted_text cannot be empty.",
        )

    if payload.patient_id and current_user.role == "PATIENT" and payload.patient_id != current_user.patient_id:
        raise HTTPException(status_code=403, detail="Patients may only process their own medical text.")
    if payload.patient_id and current_user.role == "DOCTOR":
        if not current_user.doctor_id:
            raise HTTPException(status_code=404, detail="Doctor profile is not linked to the authenticated user.")
        client = get_supabase_service_client()
        if get_doctor_access_mode(client, current_user.doctor_id, payload.patient_id) != "NORMAL":
            raise HTTPException(status_code=403, detail="NLU requires active NORMAL_ACCESS; break-glass is read-only.")

    try:
        document_meta = payload.document_meta or {}
        pipeline_result = process_text(
            payload.extracted_text,
            document_id=document_meta.get("document_id", "standalone-nlu"),
            metadata=document_meta,
        )
    except Exception as exc:
        raise HTTPException(status_code=503, detail="OCR-NLU processing service is unavailable.") from exc

    nlu_data = pipeline_result["nlu"]

    if payload.patient_id:
        client = get_supabase_service_client()
        mode = "NORMAL"
        if current_user.role == "DOCTOR" and current_user.doctor_id:
            mode = "NORMAL"

        log_audit_event(
            client=client,
            actor_id=current_user.user_id,
            actor_role=current_user.role,
            patient_id=payload.patient_id,
            action="NLU_EXTRACTED",
            access_type=mode,
            entity_type="AI_FINDINGS",
            reason="NLU structured extraction performed",
            details={
                "facts_count": len(nlu_data.get("candidate_facts", [])),
                "validation_issues_count": len(nlu_data.get("validation_issues", [])),
            },
        )

    return NLUProcessResponse(
        extracted_text=payload.extracted_text,
        findings=nlu_data,
        normalizations=[],
        critical_findings=[
            fact.get("original_text", "")
            for fact in nlu_data.get("candidate_facts", [])
            if fact.get("entity_type") == "CRITICAL_FINDING"
        ],
        is_suggestion_only=True,
        summary=(
            f"OCR-NLU extraction completed with {len(nlu_data.get('candidate_facts', []))} candidate facts "
            f"and {len(nlu_data.get('validation_issues', []))} validation issues."
        ),
    )
