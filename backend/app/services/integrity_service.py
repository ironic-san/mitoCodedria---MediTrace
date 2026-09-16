from datetime import datetime, timezone
import logging
import uuid
from typing import Optional, Tuple

from fastapi import HTTPException, status
from supabase import Client

from app.schemas.integrity import (
    IntegrityVerifyResponse,
    PatientIntegritySummaryResponse,
)
from app.services.audit_service import log_audit_event
from app.services.blockchain_service import get_blockchain_service
from app.services.emergency_service import get_doctor_access_mode
from app.utils.canonicalization import (
    build_canonical_event,
    canonicalize_and_hash_event,
)

logger = logging.getLogger(__name__)


def get_or_create_blockchain_subject_ref(
    client: Client,
    patient_id: str,
) -> str:
    patient_res = (
        client.table("patients")
        .select("patient_id,blockchain_subject_ref")
        .eq("patient_id", patient_id)
        .single()
        .execute()
    )

    patient = patient_res.data
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found.",
        )

    existing_ref = patient.get("blockchain_subject_ref")
    if existing_ref:
        return str(existing_ref)

    subject_ref = str(uuid.uuid4())

    update_res = (
        client.table("patients")
        .update({"blockchain_subject_ref": subject_ref})
        .eq("patient_id", patient_id)
        .is_("blockchain_subject_ref", "null")
        .execute()
    )

    if update_res.data:
        return subject_ref

    retry_res = (
        client.table("patients")
        .select("blockchain_subject_ref")
        .eq("patient_id", patient_id)
        .single()
        .execute()
    )

    final_ref = retry_res.data.get("blockchain_subject_ref") if retry_res.data else None

    if not final_ref:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to establish blockchain subject reference.",
        )

    return str(final_ref)


def _build_canonical_for_event(
    client: Client,
    event: dict,
) -> Tuple[dict, str, str]:
    """
    Build the locked seven-field canonical event representation.

    Generic medical event:
      event_value = title
      reaction = ""

    Allergy:
      event_value = allergen
      reaction = patient allergy reaction
      status = patient allergy status
    """
    event_type = str(event.get("event_type") or "EVENT").strip().upper()
    patient_id = str(event["patient_id"])

    event_value = str(event.get("title") or "").strip()
    severity = str(event.get("severity") or "").strip().upper()
    reaction = ""
    event_status = str(event.get("status") or "").strip().upper()

    if event_type == "ALLERGY":
        allergy_res = (
            client.table("patient_allergies")
            .select("*")
            .eq("patient_id", patient_id)
            .order("confirmed_date", desc=True)
            .limit(1)
            .execute()
        )

        allergy_row = (allergy_res.data or [None])[0]

        if allergy_row:
            allergy_id = allergy_row.get("allergy_id")
            allergen = None

            if allergy_id:
                master_res = (
                    client.table("allergies")
                    .select("allergen")
                    .eq("allergy_id", allergy_id)
                    .single()
                    .execute()
                )
                if master_res.data:
                    allergen = master_res.data.get("allergen")

            if allergen:
                event_value = str(allergen).strip()

            if allergy_row.get("severity"):
                severity = str(allergy_row["severity"]).strip().upper()

            reaction = str(allergy_row.get("reaction") or "").strip()
            event_status = str(allergy_row.get("status") or event_status).strip().upper()

            event_date = (
                allergy_row.get("confirmed_date")
                or allergy_row.get("first_reported")
                or event.get("event_date")
            )
        else:
            event_date = event.get("event_date")
    else:
        event_date = event.get("event_date")

    canonical_event = build_canonical_event(
        event_type=event_type,
        event_value=event_value,
        severity=severity,
        reaction=reaction,
        event_date=event_date,
        version=int(event.get("version", 1) or 1),
        status=event_status,
    )

    canonical_str, event_hash = canonicalize_and_hash_event(canonical_event)

    return canonical_event, canonical_str, event_hash


def _latest_integrity_record(client: Client, event_id: str):
    res = (
        client.table("integrity_records")
        .select("*")
        .eq("event_id", event_id)
        .order("event_version", desc=True)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return (res.data or [None])[0]


def verify_medical_event_integrity(
    client: Client,
    doctor_id: str,
    event_id: str,
) -> IntegrityVerifyResponse:
    bc_service = get_blockchain_service()
    now_iso = datetime.now(timezone.utc).isoformat()

    ev_res = (
        client.table("medical_events")
        .select("*")
        .eq("event_id", event_id)
        .neq("status", "TOMBSTONED")
        .neq("status", "DELETED")
        .execute()
    )
    event_rows = ev_res.data or []

    # Current record exists.
    if event_rows:
        event = event_rows[0]
        patient_id = str(event["patient_id"])
        title = event.get("title", "Medical Event")

        mode = get_doctor_access_mode(client, doctor_id, patient_id)
        if not mode:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Doctor does not have valid active access to this patient.",
            )

        canonical_event, canonical_str, current_hash = _build_canonical_for_event(
            client,
            event,
        )

        ir = _latest_integrity_record(client, event_id)

        if not ir or not ir.get("blockchain_proof_id"):
            return IntegrityVerifyResponse(
                event_id=event_id,
                patient_id=patient_id,
                event_title=title,
                verification_status="NOT_ANCHORED",
                current_hash=current_hash,
                anchored_hash=ir.get("event_hash") if ir else None,
                blockchain_tx_id=ir.get("blockchain_tx_id") if ir else None,
                block_number=ir.get("block_number") if ir else None,
                blockchain_timestamp=ir.get("blockchain_timestamp") if ir else None,
                message="Event exists in the database but has no active blockchain proof.",
                canonical_event_data=canonical_event,
                verified_at=now_iso,
            )

        proof_id = str(ir["blockchain_proof_id"])
        proof = bc_service.get_proof(proof_id)

        if not proof:
            return IntegrityVerifyResponse(
                event_id=event_id,
                patient_id=patient_id,
                event_title=title,
                verification_status="HISTORICAL RECORD MISSING",
                current_hash=current_hash,
                anchored_hash=ir.get("event_hash"),
                blockchain_tx_id=ir.get("blockchain_tx_id"),
                block_number=ir.get("block_number"),
                blockchain_timestamp=ir.get("blockchain_timestamp"),
                message="The database references a blockchain proof that could not be retrieved.",
                canonical_event_data=canonical_event,
                verified_at=now_iso,
            )

        verification = bc_service.verify_proof(
            proof_id,
            current_hash,
        )

        if verification.get("verified"):
            client.table("integrity_records").update(
                {
                    "verification_status": "VERIFIED",
                    "verified_at": now_iso,
                }
            ).eq(
                "integrity_id",
                ir["integrity_id"],
            ).execute()

            log_audit_event(
                client=client,
                actor_id=doctor_id,
                actor_role="DOCTOR",
                patient_id=patient_id,
                action="INTEGRITY_VERIFY",
                access_type=mode,
                entity_type="MEDICAL_EVENT",
                entity_id=event_id,
                reason="Cryptographic integrity verification succeeded.",
                details={
                    "status": "VERIFIED",
                    "proof_id": proof_id,
                    "hash": current_hash,
                },
            )

            return IntegrityVerifyResponse(
                event_id=event_id,
                patient_id=patient_id,
                event_title=title,
                verification_status="VERIFIED",
                current_hash=current_hash,
                anchored_hash=proof.get("eventHash"),
                blockchain_tx_id=ir.get("blockchain_tx_id"),
                block_number=ir.get("block_number"),
                blockchain_timestamp=proof.get("registeredAt"),
                message="Database record matches the anchored blockchain proof.",
                canonical_event_data=canonical_event,
                verified_at=now_iso,
            )

        client.table("integrity_records").update(
            {
                "verification_status": "TAMPERED_OR_MODIFIED",
                "verified_at": now_iso,
            }
        ).eq(
            "integrity_id",
            ir["integrity_id"],
        ).execute()

        log_audit_event(
            client=client,
            actor_id=doctor_id,
            actor_role="DOCTOR",
            patient_id=patient_id,
            action="INTEGRITY_VERIFY",
            access_type=mode,
            entity_type="MEDICAL_EVENT",
            entity_id=event_id,
            reason="Integrity mismatch detected.",
            details={
                "status": "TAMPERED_OR_MODIFIED",
                "proof_id": proof_id,
                "current_hash": current_hash,
                "anchored_hash": proof.get("eventHash"),
            },
        )

        return IntegrityVerifyResponse(
            event_id=event_id,
            patient_id=patient_id,
            event_title=title,
            verification_status="TAMPERED_OR_MODIFIED",
            current_hash=current_hash,
            anchored_hash=proof.get("eventHash"),
            blockchain_tx_id=ir.get("blockchain_tx_id"),
            block_number=ir.get("block_number"),
            blockchain_timestamp=proof.get("registeredAt"),
            message="Current medical data does not match the anchored blockchain proof.",
            canonical_event_data=canonical_event,
            verified_at=now_iso,
        )

    # Current event is absent/tombstoned.
    legacy_ir = _latest_integrity_record(client, event_id)

    if legacy_ir and legacy_ir.get("blockchain_proof_id"):
        proof_id = str(legacy_ir["blockchain_proof_id"])
        proof = bc_service.get_proof(proof_id)

        patient_res = (
            client.table("medical_events")
            .select("patient_id")
            .eq("event_id", event_id)
            .limit(1)
            .execute()
        )
        patient_id = (
            str(patient_res.data[0]["patient_id"])
            if patient_res.data
            else "unknown"
        )

        mode = None
        if patient_id != "unknown":
            mode = get_doctor_access_mode(client, doctor_id, patient_id)

        if mode is None and patient_id != "unknown":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        if proof:
            return IntegrityVerifyResponse(
                event_id=event_id,
                patient_id=patient_id,
                event_title="Historical Critical Medical Event",
                verification_status="HISTORICAL RECORD MISSING",
                anchored_hash=proof.get("eventHash"),
                blockchain_tx_id=legacy_ir.get("blockchain_tx_id"),
                block_number=legacy_ir.get("block_number"),
                blockchain_timestamp=proof.get("registeredAt"),
                message="The historical blockchain proof exists, but the current medical record is missing.",
                verified_at=now_iso,
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Medical event with ID '{event_id}' has no current database record or blockchain proof.",
    )


def anchor_medical_event_integrity(
    client: Client,
    doctor_id: str,
    event_id: str,
    notes: Optional[str] = None,
):
    ev_res = (
        client.table("medical_events")
        .select("*")
        .eq("event_id", event_id)
        .execute()
    )

    if not ev_res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medical event with ID '{event_id}' not found.",
        )

    event = ev_res.data[0]
    patient_id = str(event["patient_id"])

    mode = get_doctor_access_mode(client, doctor_id, patient_id)
    if not mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Doctor does not have valid active access to this patient.",
        )

    subject_ref = get_or_create_blockchain_subject_ref(
        client,
        patient_id,
    )

    canonical_event, canonical_str, event_hash = _build_canonical_for_event(
        client,
        event,
    )

    version = int(event.get("version", 1) or 1)

    previous = _latest_integrity_record(client, event_id)

    # Legacy integrity records may predate the blockchain proof chain.
    # They must not be used as previousProofHash for a new Version 1 proof.
    previous_proof_hash = None
    if previous and previous.get("blockchain_proof_id") and version > 1:
        previous_proof_hash = previous.get("event_hash")

    proof_id = str(uuid.uuid4())

    bc_service = get_blockchain_service()

    tx_result = bc_service.anchor_event(
        proof_id=proof_id,
        subject_ref=subject_ref,
        event_hash=event_hash,
        record_version=version,
        previous_proof_hash=previous_proof_hash,
        status="ACTIVE",
    )

    now_iso = datetime.now(timezone.utc).isoformat()

    integrity_payload = {
        "integrity_id": str(uuid.uuid4()),
        "event_id": event_id,
        "event_hash": event_hash,
        "hash_algorithm": "SHA-256",
        "event_version": version,
        "blockchain_proof_id": proof_id,
        "blockchain_tx_id": tx_result.get("registeredAt") or proof_id,
        "blockchain_timestamp": tx_result.get("registeredAt") or now_iso,
        "verification_status": "VERIFIED",
        "verified_at": now_iso,
    }

    client.table("integrity_records").insert(
        integrity_payload
    ).execute()

    log_audit_event(
        client=client,
        actor_id=doctor_id,
        actor_role="DOCTOR",
        patient_id=patient_id,
        action="INTEGRITY_ANCHOR",
        access_type=mode,
        entity_type="MEDICAL_EVENT",
        entity_id=event_id,
        reason=f"Anchored critical event: {event.get('title')}",
        details={
            "proof_id": proof_id,
            "version": version,
        },
    )

    return {
        "integrity_id": integrity_payload["integrity_id"],
        "event_id": event_id,
        "patient_id": patient_id,
        "event_title": event.get("title", "Critical Medical Event"),
        "event_hash": event_hash,
        "record_hash": event_hash,
        "blockchain_tx_id": integrity_payload["blockchain_tx_id"],
        "block_number": None,
        "blockchain_timestamp": integrity_payload["blockchain_timestamp"],
        "anchored_at": integrity_payload["blockchain_timestamp"],
        "blockchain_network": "Hyperledger Fabric (mychannel)",
        "verification_status": "VERIFIED",
        "status": "ANCHORED",
        "message": "Event anchored to Hyperledger Fabric successfully.",
    }


def get_patient_integrity_summary(
    client: Client,
    doctor_id: str,
    patient_id: str,
) -> PatientIntegritySummaryResponse:
    mode = get_doctor_access_mode(client, doctor_id, patient_id)
    if not mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Doctor does not have valid active access to this patient.",
        )

    ev_res = (
        client.table("medical_events")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )
    events = ev_res.data or []

    integrity_res = (
        client.table("integrity_records")
        .select("*")
        .in_(
            "event_id",
            [e["event_id"] for e in events],
        )
        .order("event_version", desc=True)
        .execute()
        if events
        else None
    )

    records = integrity_res.data if integrity_res else []

    verified_count = sum(
        1 for record in records
        if record.get("verification_status") == "VERIFIED"
    )

    return PatientIntegritySummaryResponse(
        patient_id=patient_id,
        total_critical_events=len(events),
        total_anchored=len(records),
        total_verified=verified_count,
        records=[],
    )
