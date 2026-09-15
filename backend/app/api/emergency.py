from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import AuthenticatedUser, require_doctor
from app.schemas.emergency import (
    BreakGlassEndRequest,
    BreakGlassEndResponse,
    BreakGlassRequest,
    BreakGlassResponse,
    EmergencyMedicalSummaryResponse,
)
from app.services.emergency_service import (
    end_break_glass,
    get_emergency_medical_summary,
    initiate_break_glass,
)
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()


@router.post("/break-glass", response_model=BreakGlassResponse, summary="Initiate emergency break-glass access")
def initiate_emergency_break_glass(
    payload: BreakGlassRequest,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """
    Doctor explicitly initiates emergency break-glass access to a patient's critical records.
    - Requires authenticated DOCTOR.
    - Requires clinical justification reason.
    - Creates temporary emergency authorization session (default 4 hours, max 24 hours).
    - Grants read-only access to critical health data, RAG, and integrity verification.
    - Write operations are strictly prohibited.
    - Immutable audit record is created.
    """
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    return initiate_break_glass(
        client=client,
        doctor_id=current_user.doctor_id,
        patient_id=payload.patient_id,
        reason=payload.reason,
        duration_hours=payload.duration_hours or 4,
    )


@router.post("/break-glass/end", response_model=BreakGlassEndResponse, summary="Conclude emergency break-glass access")
def end_emergency_break_glass(
    payload: BreakGlassEndRequest,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """
    Doctor concludes/terminates an active break-glass emergency session early.
    """
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    return end_break_glass(
        client=client,
        doctor_id=current_user.doctor_id,
        patient_id=payload.patient_id,
        reason=payload.reason or "Emergency treatment concluded",
    )


@router.get("/patient/{patient_id}", response_model=EmergencyMedicalSummaryResponse, summary="Get patient emergency critical summary")
def get_patient_emergency_summary_endpoint(
    patient_id: str,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """
    Retrieves filtered critical emergency medical passport for a patient.
    Requires doctor to have active NORMAL access OR active BREAK_GLASS emergency access.
    """
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    return get_emergency_medical_summary(
        client=client,
        doctor_id=current_user.doctor_id,
        patient_id=patient_id,
    )
