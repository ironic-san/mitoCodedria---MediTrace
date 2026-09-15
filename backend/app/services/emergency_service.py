import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from fastapi import HTTPException, status
from supabase import Client

from app.schemas.emergency import (
    BreakGlassEndResponse,
    BreakGlassResponse,
    EmergencyMedicalSummaryResponse,
)
from app.schemas.patient import (
    MedicalEventItem,
    PatientAllergyItem,
    PatientConditionItem,
    PatientMedicationItem,
    PatientProfile,
)
from app.services.audit_service import log_audit_event

logger = logging.getLogger(__name__)


def has_valid_emergency_access(client: Client, doctor_id: str, patient_id: str) -> bool:
    """
    Returns True if the doctor currently has a valid, active, non-expired BREAK_GLASS session for the patient.
    """
    if not doctor_id or not patient_id:
        return False

    res = (
        client.table("doctor_patient")
        .select("*")
        .eq("doctor_id", doctor_id)
        .eq("patient_id", patient_id)
        .eq("relationship_type", "BREAK_GLASS")
        .eq("status", "ACTIVE")
        .execute()
    )

    rows = res.data or []
    if not rows:
        return False

    now_utc = datetime.now(timezone.utc)

    for row in rows:
        ended_at_str = row.get("ended_at")
        if ended_at_str:
            try:
                ended_at_dt = datetime.fromisoformat(ended_at_str.replace("Z", "+00:00"))
                if ended_at_dt.tzinfo is None:
                    ended_at_dt = ended_at_dt.replace(tzinfo=timezone.utc)
                if ended_at_dt <= now_utc:
                    continue  # Session expired
            except Exception:
                pass
        return True

    return False


def get_doctor_access_mode(client: Client, doctor_id: str, patient_id: str) -> Optional[str]:
    """
    Resolves the doctor's current valid access mode for a patient:
    Returns 'NORMAL' if active normal access exists.
    Returns 'BREAK_GLASS' if active emergency break-glass session exists.
    Returns None if doctor has no active access.
    """
    if not doctor_id or not patient_id:
        return None

    now_utc = datetime.now(timezone.utc)

    res = (
        client.table("doctor_patient")
        .select("*")
        .eq("doctor_id", doctor_id)
        .eq("patient_id", patient_id)
        .eq("status", "ACTIVE")
        .execute()
    )

    rows = res.data or []
    has_normal = False
    has_break_glass = False

    for row in rows:
        ended_at_str = row.get("ended_at")
        is_valid = True
        if ended_at_str:
            try:
                ended_at_dt = datetime.fromisoformat(ended_at_str.replace("Z", "+00:00"))
                if ended_at_dt.tzinfo is None:
                    ended_at_dt = ended_at_dt.replace(tzinfo=timezone.utc)
                if ended_at_dt <= now_utc:
                    is_valid = False
            except Exception:
                pass

        if is_valid:
            rel_type = (row.get("relationship_type") or "").upper()
            if rel_type in {"BREAK_GLASS", "EMERGENCY"}:
                has_break_glass = True
            else:
                has_normal = True

    if has_normal:
        return "NORMAL"
    if has_break_glass:
        return "BREAK_GLASS"
    return None


def initiate_break_glass(
    client: Client,
    doctor_id: str,
    patient_id: str,
    reason: str,
    duration_hours: int = 4,
) -> BreakGlassResponse:
    """
    Doctor initiates an emergency break-glass session.
    Creates temporary authorization in doctor_patient, logs in emergency_events and audit_logs.
    """
    # 1. Verify target patient exists
    pat_res = client.table("patients").select("patient_id, full_name").eq("patient_id", patient_id).execute()
    if not pat_res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found.",
        )

    # 2. Verify target doctor exists
    doc_res = client.table("doctors").select("doctor_id, full_name").eq("doctor_id", doctor_id).execute()
    if not doc_res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID '{doctor_id}' not found.",
        )

    now_utc = datetime.now(timezone.utc)
    hours = min(max(duration_hours, 1), 24)
    expires_at_utc = now_utc + timedelta(hours=hours)

    # Clean up prior break-glass record to maintain unique constraint
    try:
        client.table("doctor_patient").delete().eq("doctor_id", doctor_id).eq("patient_id", patient_id).eq("relationship_type", "BREAK_GLASS").execute()
    except Exception:
        pass

    # Insert break-glass relationship record
    session_payload = {
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "relationship_type": "BREAK_GLASS",
        "status": "ACTIVE",
        "started_at": now_utc.isoformat(),
        "ended_at": expires_at_utc.isoformat(),
    }

    insert_res = client.table("doctor_patient").insert(session_payload).execute()
    session_id = str(insert_res.data[0]["relationship_id"]) if insert_res.data else str(uuid.uuid4())

    # Log in emergency_events table
    try:
        client.table("emergency_events").insert({
            "patient_id": patient_id,
            "trigger_source": "DOCTOR_BREAK_GLASS",
            "trigger_type": "EMERGENCY_OVERRIDE",
            "reason": reason,
            "status": "ACTIVE",
            "started_at": now_utc.isoformat(),
            "ended_at": expires_at_utc.isoformat(),
        }).execute()
    except Exception as e:
        logger.warning(f"Could not record emergency_event: {e}")

    # Log immutable audit event
    log_audit_event(
        client=client,
        actor_id=doctor_id,
        actor_role="DOCTOR",
        patient_id=patient_id,
        action="BREAK_GLASS_INITIATED",
        access_type="BREAK_GLASS",
        entity_type="EMERGENCY_ACCESS",
        entity_id=session_id,
        reason=reason,
        details={
            "duration_hours": hours,
            "expires_at": expires_at_utc.isoformat(),
        },
    )

    return BreakGlassResponse(
        session_id=session_id,
        doctor_id=doctor_id,
        patient_id=patient_id,
        status="ACTIVE",
        started_at=now_utc.isoformat(),
        expires_at=expires_at_utc.isoformat(),
        reason=reason,
        access_type="BREAK_GLASS",
    )


def end_break_glass(
    client: Client,
    doctor_id: str,
    patient_id: str,
    reason: str = "Emergency treatment concluded",
) -> BreakGlassEndResponse:
    """
    Terminates an active break-glass session early.
    """
    now_utc = datetime.now(timezone.utc)

    # Find active session
    res = (
        client.table("doctor_patient")
        .select("relationship_id")
        .eq("doctor_id", doctor_id)
        .eq("patient_id", patient_id)
        .eq("relationship_type", "BREAK_GLASS")
        .eq("status", "ACTIVE")
        .execute()
    )

    session_id = str(res.data[0]["relationship_id"]) if res.data else None

    # Update status to ENDED
    client.table("doctor_patient").update({
        "status": "ENDED",
        "ended_at": now_utc.isoformat(),
    }).eq("doctor_id", doctor_id).eq("patient_id", patient_id).eq("relationship_type", "BREAK_GLASS").execute()

    # Log audit event
    log_audit_event(
        client=client,
        actor_id=doctor_id,
        actor_role="DOCTOR",
        patient_id=patient_id,
        action="BREAK_GLASS_ENDED",
        access_type="BREAK_GLASS",
        entity_type="EMERGENCY_ACCESS",
        entity_id=session_id,
        reason=reason,
    )

    return BreakGlassEndResponse(
        session_id=session_id,
        doctor_id=doctor_id,
        patient_id=patient_id,
        status="ENDED",
        ended_at=now_utc.isoformat(),
    )


def get_emergency_medical_summary(
    client: Client,
    doctor_id: str,
    patient_id: str,
) -> EmergencyMedicalSummaryResponse:
    """
    Retrieves filtered critical emergency health passport for a patient.
    Requires doctor to have either NORMAL or active BREAK_GLASS access.
    """
    mode = get_doctor_access_mode(client, doctor_id, patient_id)
    if not mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Doctor must initiate break-glass emergency access first.",
        )

    # 1. Profile
    pat_res = client.table("patients").select("*").eq("patient_id", patient_id).execute()
    if not pat_res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found.",
        )
    p_data = pat_res.data[0]

    dob_str = p_data.get("date_of_birth")
    age = None
    if dob_str:
        try:
            dob_dt = datetime.fromisoformat(dob_str)
            today = datetime.now(timezone.utc).date()
            age = today.year - dob_dt.year - ((today.month, today.day) < (dob_dt.month, dob_dt.day))
        except Exception:
            pass

    profile = PatientProfile(
        patient_id=str(p_data["patient_id"]),
        auth_user_id=p_data.get("auth_user_id"),
        full_name=p_data.get("full_name", ""),
        date_of_birth=p_data.get("date_of_birth"),
        age=age,
        gender=p_data.get("gender"),
        blood_group=p_data.get("blood_group"),
        phone=p_data.get("phone"),
        email=p_data.get("email"),
        address=p_data.get("address"),
        emergency_contact_name=p_data.get("emergency_contact_name"),
        emergency_contact_phone=p_data.get("emergency_contact_phone"),
    )

    # Master caches
    allergies_master = {str(r["allergy_id"]): r for r in client.table("allergies").select("*").execute().data or []}
    conditions_master = {str(r["condition_id"]): r for r in client.table("medical_conditions").select("*").execute().data or []}
    medications_master = {str(r["medication_id"]): r for r in client.table("medications").select("*").execute().data or []}
    doctors_master = {str(r["doctor_id"]): r.get("full_name", "") for r in client.table("doctors").select("*").execute().data or []}

    # 2. Critical Allergies (ACTIVE allergies, severe/life-threatening highlighted)
    allergies_list = []
    pat_all_res = client.table("patient_allergies").select("*").eq("patient_id", patient_id).eq("status", "ACTIVE").execute()
    for pa in pat_all_res.data or []:
        alg_id = str(pa.get("allergy_id"))
        m_alg = allergies_master.get(alg_id, {})
        allergies_list.append(
            PatientAllergyItem(
                patient_allergy_id=str(pa["patient_allergy_id"]),
                allergy_id=alg_id,
                allergen=m_alg.get("allergen", "Unknown Allergen"),
                allergy_type=m_alg.get("allergy_type"),
                severity=pa.get("severity"),
                reaction=pa.get("reaction"),
                status=pa.get("status"),
                first_reported=pa.get("first_reported"),
                confirmed_date=pa.get("confirmed_date"),
                notes=pa.get("notes"),
            )
        )

    # 3. Critical Conditions (ACTIVE conditions)
    conditions_list = []
    pat_cond_res = client.table("patient_conditions").select("*").eq("patient_id", patient_id).eq("status", "ACTIVE").execute()
    for pc in pat_cond_res.data or []:
        c_id = str(pc.get("condition_id"))
        m_cond = conditions_master.get(c_id, {})
        conditions_list.append(
            PatientConditionItem(
                patient_condition_id=str(pc["patient_condition_id"]),
                condition_id=c_id,
                condition_name=m_cond.get("name", "Unknown Condition"),
                description=m_cond.get("description"),
                status=pc.get("status"),
                severity=pc.get("severity"),
                diagnosed_date=pc.get("diagnosed_date"),
                resolved_date=pc.get("resolved_date"),
                notes=pc.get("notes"),
            )
        )

    # 4. Critical Medications (ACTIVE medications)
    medications_list = []
    pat_med_res = client.table("patient_medications").select("*").eq("patient_id", patient_id).eq("status", "ACTIVE").execute()
    for pm in pat_med_res.data or []:
        m_id = str(pm.get("medication_id"))
        doc_pres_id = str(pm.get("prescribed_by")) if pm.get("prescribed_by") else None
        m_med = medications_master.get(m_id, {})
        medications_list.append(
            PatientMedicationItem(
                patient_medication_id=str(pm["patient_medication_id"]),
                medication_id=m_id,
                medication_name=m_med.get("name", "Unknown Medication"),
                generic_name=m_med.get("generic_name"),
                dosage=pm.get("dosage"),
                frequency=pm.get("frequency"),
                route=pm.get("route"),
                start_date=pm.get("start_date"),
                end_date=pm.get("end_date"),
                status=pm.get("status"),
                prescribed_by=doc_pres_id,
                prescribed_by_name=doctors_master.get(doc_pres_id) if doc_pres_id else None,
                instructions=pm.get("instructions"),
            )
        )

    # 5. Critical Medical Events (is_critical=True or severity=HIGH/CRITICAL)
    events_list = []
    pat_ev_res = client.table("medical_events").select("*").eq("patient_id", patient_id).execute()
    for ev in pat_ev_res.data or []:
        is_crit = bool(ev.get("is_critical", False)) or str(ev.get("severity", "")).upper() in {"HIGH", "CRITICAL", "SEVERE"}
        if is_crit:
            ev_doc_id = str(ev.get("doctor_id")) if ev.get("doctor_id") else None
            events_list.append(
                MedicalEventItem(
                    event_id=str(ev["event_id"]),
                    patient_id=str(ev["patient_id"]),
                    doctor_id=ev_doc_id,
                    doctor_name=doctors_master.get(ev_doc_id) if ev_doc_id else None,
                    event_type=ev.get("event_type", "CONSULTATION"),
                    event_date=str(ev.get("event_date")),
                    title=ev.get("title", ""),
                    description=ev.get("description"),
                    severity=ev.get("severity"),
                    is_critical=is_crit,
                    status=ev.get("status"),
                    source_document_id=str(ev.get("source_document_id")) if ev.get("source_document_id") else None,
                    created_at=str(ev.get("created_at")),
                )
            )

    now_utc = datetime.now(timezone.utc)

    # Audit the emergency viewing
    log_audit_event(
        client=client,
        actor_id=doctor_id,
        actor_role="DOCTOR",
        patient_id=patient_id,
        action="VIEW_EMERGENCY_SUMMARY",
        access_type=mode,
        entity_type="PATIENT_SUMMARY",
        entity_id=patient_id,
        reason="Doctor accessed emergency critical medical summary",
        details={
            "allergies_count": len(allergies_list),
            "conditions_count": len(conditions_list),
            "medications_count": len(medications_list),
            "critical_events_count": len(events_list),
        },
    )

    return EmergencyMedicalSummaryResponse(
        patient_id=patient_id,
        access_type=mode,
        accessed_at=now_utc.isoformat(),
        profile=profile,
        critical_allergies=allergies_list,
        critical_conditions=conditions_list,
        critical_medications=medications_list,
        critical_events=events_list,
    )
