from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import AuthenticatedUser, get_current_user
from app.schemas.ai import NLUProcessRequest, NLUProcessResponse
from app.services.ai_service import extract_nlu_findings
from app.services.audit_service import log_audit_event
from app.services.emergency_service import get_doctor_access_mode
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

    nlu_res = extract_nlu_findings(
        extracted_text=payload.extracted_text,
        patient_id=payload.patient_id,
        document_meta=payload.document_meta,
    )

    if payload.patient_id:
        client = get_supabase_service_client()
        mode = "NORMAL"
        if current_user.role == "DOCTOR" and current_user.doctor_id:
            mode = get_doctor_access_mode(client, current_user.doctor_id, payload.patient_id) or "NORMAL"

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
                "normalizations_count": len(nlu_res.normalizations),
                "critical_findings_count": len(nlu_res.critical_findings),
            },
        )

    return nlu_res
