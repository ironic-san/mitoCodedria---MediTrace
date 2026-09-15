from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import (
    AuthenticatedUser,
    get_current_user,
    require_patient,
)
from app.schemas.audit import AuditHistoryResponse
from app.services.audit_service import get_patient_audit_logs
from app.services.emergency_service import get_doctor_access_mode
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()


@router.get("/me", response_model=AuditHistoryResponse, summary="Get authenticated patient self audit trail")
def get_patient_self_audit_logs(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: AuthenticatedUser = Depends(require_patient),
):
    """
    Returns the complete access and event audit history for the authenticated patient.
    """
    if not current_user.patient_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    return get_patient_audit_logs(client, current_user.patient_id, limit=limit, offset=offset)


@router.get("/patient/{patient_id}", response_model=AuditHistoryResponse, summary="Get audit logs for a patient")
def get_patient_audit_logs_endpoint(
    patient_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """
    Retrieves audit logs for a specific patient.
    - Patient can view their own audit trail.
    - Doctor with active NORMAL or BREAK_GLASS access can view patient audit trail.
    """
    client = get_supabase_service_client()

    if current_user.role == "PATIENT":
        if current_user.patient_id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Patients may only view their own audit trail.",
            )
    elif current_user.role == "DOCTOR":
        mode = get_doctor_access_mode(client, current_user.doctor_id, patient_id)
        if not mode:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Doctor does not have active access to this patient.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Invalid user role.",
        )

    return get_patient_audit_logs(client, patient_id, limit=limit, offset=offset)
