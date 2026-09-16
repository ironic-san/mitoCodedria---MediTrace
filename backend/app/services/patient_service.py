from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from supabase import Client

from app.schemas.patient import (
    IntegrityRecordItem,
    MedicalEventItem,
    MedicalSummaryResponse,
    PatientAllergyItem,
    PatientConditionItem,
    PatientMedicationItem,
    PatientProfile,
)


def has_valid_doctor_access(client: Client, doctor_id: str, patient_id: str) -> bool:
    """
    Returns True if the doctor currently has valid, active, non-expired normal access to the patient.
    Checks doctor_patient table for status='ACTIVE' and ended_at > current_time.
    """
    if not doctor_id or not patient_id:
        return False

    res = (
        client.table("doctor_patient")
        .select("*")
        .eq("doctor_id", doctor_id)
        .eq("patient_id", patient_id)
        .in_("relationship_type", ["NORMAL_ACCESS", "PRIMARY_CARE"])
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
                    continue  # Expired
            except Exception:
                # Invalid expiry data must fail closed.
                continue
        return True  # Valid active relationship

    return False


def has_any_valid_doctor_access(client: Client, doctor_id: str, patient_id: str) -> bool:
    """
    Returns True if doctor has either normal active access OR valid active break-glass emergency access.
    """
    if has_valid_doctor_access(client, doctor_id, patient_id):
        return True

    from app.services.emergency_service import has_valid_emergency_access
    return has_valid_emergency_access(client, doctor_id, patient_id)


def get_consolidated_medical_summary(client: Client, patient_id: str) -> MedicalSummaryResponse:
    """
    Consolidates full patient medical record from DB:
    profile, allergies, conditions, medications, events, critical history, integrity records.
    """
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

    # 2. Master lists map for fast joins
    allergies_master = {}
    all_all_res = client.table("allergies").select("*").execute()
    for row in all_all_res.data or []:
        allergies_master[str(row["allergy_id"])] = row

    conditions_master = {}
    all_cond_res = client.table("medical_conditions").select("*").execute()
    for row in all_cond_res.data or []:
        conditions_master[str(row["condition_id"])] = row

    medications_master = {}
    all_med_res = client.table("medications").select("*").execute()
    for row in all_med_res.data or []:
        medications_master[str(row["medication_id"])] = row

    doctors_master = {}
    all_doc_res = client.table("doctors").select("*").execute()
    for row in all_doc_res.data or []:
        doctors_master[str(row["doctor_id"])] = row.get("full_name", "")

    # 3. Patient Allergies
    allergies_list = []
    pat_all_res = client.table("patient_allergies").select("*").eq("patient_id", patient_id).execute()
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

    # 4. Patient Conditions
    conditions_list = []
    pat_cond_res = client.table("patient_conditions").select("*").eq("patient_id", patient_id).execute()
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

    # 5. Patient Medications
    medications_list = []
    pat_med_res = client.table("patient_medications").select("*").eq("patient_id", patient_id).execute()
    for pm in pat_med_res.data or []:
        m_id = str(pm.get("medication_id"))
        doc_id = str(pm.get("prescribed_by")) if pm.get("prescribed_by") else None
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
                prescribed_by=doc_id,
                prescribed_by_name=doctors_master.get(doc_id) if doc_id else None,
                instructions=pm.get("instructions"),
            )
        )

    # 6. Patient Medical Events
    events_list = []
    pat_ev_res = client.table("medical_events").select("*").eq("patient_id", patient_id).execute()
    for ev in pat_ev_res.data or []:
        doc_id = str(ev.get("doctor_id")) if ev.get("doctor_id") else None
        events_list.append(
            MedicalEventItem(
                event_id=str(ev["event_id"]),
                patient_id=str(ev["patient_id"]),
                doctor_id=doc_id,
                doctor_name=doctors_master.get(doc_id) if doc_id else None,
                event_type=ev.get("event_type", "CONSULTATION"),
                event_date=str(ev.get("event_date")),
                title=ev.get("title", ""),
                description=ev.get("description"),
                severity=ev.get("severity"),
                is_critical=bool(ev.get("is_critical", False)),
                status=ev.get("status"),
                source_document_id=str(ev.get("source_document_id")) if ev.get("source_document_id") else None,
                created_at=str(ev.get("created_at")),
            )
        )

    # 7. Critical History Filter
    critical_history = [e for e in events_list if e.is_critical]

    # 8. Integrity Records
    integrity_list = []
    event_ids = [e.event_id for e in events_list]
    if event_ids:
        try:
            ir_res = client.table("integrity_records").select("*").in_("event_id", event_ids).execute()
            for ir in ir_res.data or []:
                integrity_list.append(
                    IntegrityRecordItem(
                        integrity_id=str(ir["integrity_id"]),
                        patient_id=patient_id,
                        event_id=str(ir["event_id"]),
                        record_hash=ir.get("event_hash", ""),
                        blockchain_tx_id=ir.get("blockchain_tx_id", ""),
                        block_number=ir.get("block_number"),
                        blockchain_network="Hyperledger Fabric (meditrace-channel)",
                        verified=bool(ir.get("verification_status") == "VERIFIED"),
                        verified_at=str(ir.get("verified_at")) if ir.get("verified_at") else None,
                        anchored_at=str(ir.get("blockchain_timestamp")) if ir.get("blockchain_timestamp") else None,
                    )
                )
        except Exception:
            pass

    return MedicalSummaryResponse(
        profile=profile,
        allergies=allergies_list,
        conditions=conditions_list,
        medications=medications_list,
        medical_events=events_list,
        critical_history=critical_history,
        integrity_records=integrity_list,
    )
