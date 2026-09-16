from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import (
    AuthenticatedUser,
    get_current_user,
    require_doctor,
    require_patient,
)
from app.schemas.access import AccessRecordResponse, GrantAccessRequest
from app.schemas.audit import AuditHistoryResponse
from app.schemas.emergency import EmergencyMedicalSummaryResponse
from app.schemas.patient import MedicalSummaryResponse
from app.services.audit_service import get_patient_audit_logs, log_audit_event
from app.services.emergency_service import (
    get_doctor_access_mode,
    get_emergency_medical_summary,
)
from app.services.patient_service import (
    get_consolidated_medical_summary,
    has_valid_doctor_access,
)
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()


@router.get("/me", response_model=MedicalSummaryResponse, summary="Get authenticated patient self passport")
def get_patient_me(current_user: AuthenticatedUser = Depends(require_patient)):
    """
    Returns the authenticated patient's own profile and consolidated medical passport.
    Derived exclusively from authenticated JWT identity (current_user.patient_id).
    """
    if not current_user.patient_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    summary = get_consolidated_medical_summary(client, current_user.patient_id)

    log_audit_event(
        client=client,
        actor_id=current_user.user_id,
        actor_role="PATIENT",
        patient_id=current_user.patient_id,
        action="VIEW_PASSPORT_SELF",
        access_type="NORMAL",
        entity_type="PATIENT_PASSPORT",
        reason="Patient accessed own consolidated health passport",
    )

    return summary


@router.get("/me/audit-logs", response_model=AuditHistoryResponse, summary="Get authenticated patient audit logs")
def get_patient_me_audit_logs(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: AuthenticatedUser = Depends(require_patient),
):
    """Returns access audit history for the authenticated patient."""
    if not current_user.patient_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    return get_patient_audit_logs(client, current_user.patient_id, limit=limit, offset=offset)


@router.get("/{patient_id}", response_model=MedicalSummaryResponse, summary="Get patient profile & summary")
@router.get("/{patient_id}/medical-summary", response_model=MedicalSummaryResponse, summary="Get patient medical summary")
def get_patient_summary(
    patient_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """
    Consolidated Medical Summary for a specific patient.
    - Patient can access their own data.
    - Doctor can access ONLY if they currently have valid active normal access.
    """
    client = get_supabase_service_client()

    # 1. Verify patient existence first
    pat_check = client.table("patients").select("patient_id").eq("patient_id", patient_id).execute()
    if not pat_check.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found.",
        )

    # 2. Authorization check
    mode = "NORMAL"
    if current_user.role == "PATIENT":
        if current_user.patient_id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Patients may only access their own medical records.",
            )
    elif current_user.role == "DOCTOR":
        if not has_valid_doctor_access(client, current_user.doctor_id, patient_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Doctor does not have valid active access to this patient.",
            )
        mode = "NORMAL"
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Invalid user role.",
        )

    summary = get_consolidated_medical_summary(client, patient_id)

    log_audit_event(
        client=client,
        actor_id=current_user.user_id,
        actor_role=current_user.role,
        patient_id=patient_id,
        action="VIEW_MEDICAL_SUMMARY",
        access_type=mode,
        entity_type="PATIENT_SUMMARY",
        reason="Medical summary viewed",
    )

    return summary


@router.get("/{patient_id}/audit", response_model=AuditHistoryResponse, summary="Get patient audit history")
def get_patient_audit_history(
    patient_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """Workflow alias that never exposes broad audit history through break-glass."""
    client = get_supabase_service_client()
    if current_user.role == "PATIENT":
        if current_user.patient_id != patient_id:
            raise HTTPException(status_code=403, detail="Patients may only view their own audit history.")
    elif current_user.role == "DOCTOR":
        if not has_valid_doctor_access(client, current_user.doctor_id, patient_id):
            raise HTTPException(status_code=403, detail="Normal doctor access is required for audit history.")
    else:
        raise HTTPException(status_code=403, detail="Invalid user role.")
    return get_patient_audit_logs(client, patient_id, limit=limit, offset=offset)


@router.get("/{patient_id}/emergency-summary", response_model=EmergencyMedicalSummaryResponse, summary="Get patient emergency summary")
def get_patient_emergency_summary_route(
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


@router.post("/{patient_id}/access", response_model=AccessRecordResponse, summary="Grant doctor normal access")
def grant_doctor_access(
    patient_id: str,
    payload: GrantAccessRequest,
    current_user: AuthenticatedUser = Depends(require_patient),
):
    """
    Patient grants normal temporary access to a specific doctor.
    """
    if current_user.patient_id != patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Patients can only manage access to their own records.",
        )

    client = get_supabase_service_client()

    target_doc = None
    if payload.doctor_id:
        doc_res = client.table("doctors").select("*").eq("doctor_id", payload.doctor_id).execute()
        if doc_res.data:
            target_doc = doc_res.data[0]
    elif payload.doctor_email:
        doc_res = client.table("doctors").select("*").eq("email", payload.doctor_email.strip()).execute()
        if doc_res.data:
            target_doc = doc_res.data[0]

    if not target_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified doctor could not be found.",
        )

    doc_id = str(target_doc["doctor_id"])
    doc_name = target_doc.get("full_name")
    doc_email = target_doc.get("email")

    pat_res = client.table("patients").select("full_name").eq("patient_id", patient_id).execute()
    pat_name = pat_res.data[0].get("full_name") if pat_res.data else ""

    now_utc = datetime.now(timezone.utc)
    duration_days = payload.duration_days if payload.duration_days > 0 else 7
    expires_at_utc = now_utc + timedelta(days=duration_days)

    client.table("doctor_patient").delete().eq("doctor_id", doc_id).eq("patient_id", patient_id).eq("relationship_type", "NORMAL_ACCESS").execute()

    record_payload = {
        "doctor_id": doc_id,
        "patient_id": patient_id,
        "relationship_type": "NORMAL_ACCESS",
        "status": "ACTIVE",
        "started_at": now_utc.isoformat(),
        "ended_at": expires_at_utc.isoformat(),
    }

    insert_res = client.table("doctor_patient").insert(record_payload).execute()
    if not insert_res.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record doctor access permission.",
        )

    created_rec = insert_res.data[0]
    access_id = str(created_rec["relationship_id"])

    log_audit_event(
        client=client,
        actor_id=current_user.user_id,
        actor_role="PATIENT",
        patient_id=patient_id,
        action="GRANT_ACCESS",
        access_type="NORMAL",
        entity_type="DOCTOR_PATIENT",
        entity_id=access_id,
        reason=f"Patient granted {duration_days} days normal access to Dr. {doc_name}",
        details={"doctor_id": doc_id, "duration_days": duration_days, "expires_at": expires_at_utc.isoformat()},
    )

    return AccessRecordResponse(
        access_id=access_id,
        patient_id=patient_id,
        doctor_id=doc_id,
        doctor_name=doc_name,
        doctor_email=doc_email,
        patient_name=pat_name,
        relationship_type="NORMAL_ACCESS",
        status="ACTIVE",
        granted_at=str(created_rec.get("started_at")),
        expires_at=str(created_rec.get("ended_at")),
    )


@router.delete("/{patient_id}/access/{access_id}", summary="Revoke doctor normal access")
def revoke_doctor_access(
    patient_id: str,
    access_id: str,
    current_user: AuthenticatedUser = Depends(require_patient),
):
    """
    Patient explicitly revokes a doctor's active access immediately.
    """
    if current_user.patient_id != patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Patients can only revoke access to their own records.",
        )

    client = get_supabase_service_client()

    rec_res = (
        client.table("doctor_patient")
        .select("*")
        .eq("relationship_id", access_id)
        .eq("patient_id", patient_id)
        .execute()
    )

    if not rec_res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Access record with ID '{access_id}' not found for this patient.",
        )

    rec = rec_res.data[0]
    doc_id = str(rec.get("doctor_id"))
    now_utc = datetime.now(timezone.utc)

    client.table("doctor_patient").update({
        "status": "ENDED",
        "ended_at": now_utc.isoformat(),
    }).eq("relationship_id", access_id).execute()

    log_audit_event(
        client=client,
        actor_id=current_user.user_id,
        actor_role="PATIENT",
        patient_id=patient_id,
        action="REVOKE_ACCESS",
        access_type="NORMAL",
        entity_type="DOCTOR_PATIENT",
        entity_id=access_id,
        reason=f"Patient revoked doctor access immediately (Doctor: {doc_id})",
    )

    return {
        "status": "revoked",
        "access_id": access_id,
        "patient_id": patient_id,
        "doctor_id": doc_id,
        "message": "Doctor access permission revoked successfully.",
        "revoked_at": now_utc.isoformat(),
    }
