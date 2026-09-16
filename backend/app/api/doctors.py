from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import AuthenticatedUser, require_doctor
from app.schemas.doctor import DoctorPatientItem, DoctorProfileResponse
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()


@router.get("/me", response_model=DoctorProfileResponse, summary="Get authenticated doctor profile")
def get_doctor_me(current_user: AuthenticatedUser = Depends(require_doctor)):
    """
    Returns the authenticated doctor's basic profile.
    Doctor identity derived strictly from authenticated JWT context.
    """
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    return DoctorProfileResponse(
        doctor_id=current_user.doctor_id,
        auth_user_id=current_user.auth_user_id,
        full_name=current_user.full_name or "",
        email=current_user.email,
        phone=current_user.phone,
        specialization=current_user.specialization,
        license_number=current_user.profile_data.get("license_number"),
        hospital_name=current_user.hospital_name,
    )


@router.get("/patients", response_model=List[DoctorPatientItem], summary="Get patients accessible by authenticated doctor")
def get_doctor_accessible_patients(current_user: AuthenticatedUser = Depends(require_doctor)):
    """
    Returns all patients for whom the authenticated doctor currently has valid active normal access.
    Excludes expired, revoked, or non-active access relationships.
    """
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()

    # Query active access relationships for this doctor
    rel_res = (
        client.table("doctor_patient")
        .select("*")
        .eq("doctor_id", current_user.doctor_id)
        .eq("relationship_type", "NORMAL_ACCESS")
        .eq("status", "ACTIVE")
        .execute()
    )

    rows = rel_res.data or []
    now_utc = datetime.now(timezone.utc)

    # Filter out expired access
    valid_patient_ids = []
    expiry_map = {}
    rel_type_map = {}

    for row in rows:
        p_id = str(row["patient_id"])
        ended_at_str = row.get("ended_at")

        if ended_at_str:
            try:
                ended_dt = datetime.fromisoformat(ended_at_str.replace("Z", "+00:00"))
                if ended_dt.tzinfo is None:
                    ended_dt = ended_dt.replace(tzinfo=timezone.utc)
                if ended_dt <= now_utc:
                    continue  # Expired access
            except Exception:
                pass

        valid_patient_ids.append(p_id)
        expiry_map[p_id] = ended_at_str
        rel_type_map[p_id] = row.get("relationship_type", "NORMAL_ACCESS")

    if not valid_patient_ids:
        return []

    # Fetch patient profile details
    pats_res = client.table("patients").select("*").in_("patient_id", valid_patient_ids).execute()
    patients_data = pats_res.data or []

    result = []
    for pat in patients_data:
        p_id = str(pat["patient_id"])
        dob_str = pat.get("date_of_birth")
        age = None
        if dob_str:
            try:
                dob_dt = datetime.fromisoformat(dob_str)
                today = datetime.now(timezone.utc).date()
                age = today.year - dob_dt.year - ((today.month, today.day) < (dob_dt.month, dob_dt.day))
            except Exception:
                pass

        result.append(
            DoctorPatientItem(
                patient_id=p_id,
                full_name=pat.get("full_name", "Unknown Patient"),
                date_of_birth=dob_str,
                gender=pat.get("gender"),
                blood_group=pat.get("blood_group"),
                access_status="ACTIVE",
                access_expiry=expiry_map.get(p_id),
                relationship_type=rel_type_map.get(p_id, "NORMAL_ACCESS"),
            )
        )

    return result
