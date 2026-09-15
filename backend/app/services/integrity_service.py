from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
from fastapi import HTTPException, status
from supabase import Client

from app.schemas.integrity import (
    IntegrityAnchorResponse,
    IntegrityVerifyResponse,
    PatientIntegritySummaryResponse,
)
from app.services.audit_service import log_audit_event
from app.services.blockchain_service import get_blockchain_service
from app.services.emergency_service import get_doctor_access_mode
from app.utils.canonicalization import canonicalize_and_hash_event

logger = logging.getLogger(__name__)


def verify_medical_event_integrity(
    client: Client,
    doctor_id: str,
    event_id: str,
) -> IntegrityVerifyResponse:
    """
    Verifies cryptographic integrity of a critical medical event against Hyperledger Fabric ledger.
    - Requires doctor to have valid NORMAL or BREAK_GLASS access to the event's patient.
    - Canonicalizes event record and computes SHA-256 hash.
    - Compares with ledger proof: VERIFIED, TAMPERED_OR_MODIFIED, HISTORICAL RECORD MISSING, NOT_ANCHORED.
    - Logs audit record.
    """
    bc_service = get_blockchain_service()
    now_iso = datetime.now(timezone.utc).isoformat()

    # 1. Look for active event in medical_events table
    ev_res = (
        client.table("medical_events")
        .select("*")
        .eq("event_id", event_id)
        .neq("status", "TOMBSTONED")
        .neq("status", "DELETED")
        .execute()
    )
    event_rows = ev_res.data or []

    if event_rows:
        event = event_rows[0]
        patient_id = str(event.get("patient_id"))
        title = event.get("title", "Medical Event")

        # Authorization check: doctor must have NORMAL or BREAK_GLASS access
        mode = get_doctor_access_mode(client, doctor_id, patient_id)
        if not mode:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Doctor does not have valid active access to this patient.",
            )

        # Compute current canonical representation and hash
        canonical_str, current_hash = canonicalize_and_hash_event(event)

        # Check DB integrity_records and Blockchain proof
        ir_res = client.table("integrity_records").select("*").eq("event_id", event_id).execute()
        ir_rows = ir_res.data or []
        bc_proof = bc_service.get_proof(event_id)

        if not ir_rows and not bc_proof:
            return IntegrityVerifyResponse(
                event_id=event_id,
                patient_id=patient_id,
                event_title=title,
                verification_status="NOT_ANCHORED",
                current_hash=current_hash,
                anchored_hash=None,
                blockchain_tx_id=None,
                block_number=None,
                blockchain_timestamp=None,
                message="Event exists in database but has not been anchored to the blockchain ledger.",
                verified_at=now_iso,
            )

        anchored_hash = bc_proof.get("event_hash") if bc_proof else (ir_rows[0].get("event_hash") if ir_rows else None)
        tx_id = bc_proof.get("blockchain_tx_id") if bc_proof else (ir_rows[0].get("blockchain_tx_id") if ir_rows else None)
        blk = bc_proof.get("block_number") if bc_proof else (ir_rows[0].get("block_number") if ir_rows else None)
        bc_ts = bc_proof.get("blockchain_timestamp") if bc_proof else (ir_rows[0].get("blockchain_timestamp") if ir_rows else None)

        if anchored_hash and current_hash.lower() == anchored_hash.lower():
            # Update DB verification flag
            if ir_rows:
                client.table("integrity_records").update({
                    "verification_status": "VERIFIED",
                    "verified_at": now_iso,
                }).eq("event_id", event_id).execute()

            log_audit_event(
                client=client,
                actor_id=doctor_id,
                actor_role="DOCTOR",
                patient_id=patient_id,
                action="INTEGRITY_VERIFY",
                access_type=mode,
                entity_type="MEDICAL_EVENT",
                entity_id=event_id,
                reason="Cryptographic integrity verification succeeded (VERIFIED)",
                details={"status": "VERIFIED", "hash": current_hash, "tx_id": tx_id},
            )

            return IntegrityVerifyResponse(
                event_id=event_id,
                patient_id=patient_id,
                event_title=title,
                verification_status="VERIFIED",
                current_hash=current_hash,
                anchored_hash=anchored_hash,
                blockchain_tx_id=tx_id,
                block_number=blk,
                blockchain_timestamp=bc_ts,
                message="Cryptographic integrity verified. Database record matches immutable Hyperledger Fabric ledger.",
                verified_at=now_iso,
            )
        else:
            log_audit_event(
                client=client,
                actor_id=doctor_id,
                actor_role="DOCTOR",
                patient_id=patient_id,
                action="INTEGRITY_VERIFY",
                access_type=mode,
                entity_type="MEDICAL_EVENT",
                entity_id=event_id,
                reason="Integrity mismatch detected (TAMPERED_OR_MODIFIED)",
                details={"status": "TAMPERED_OR_MODIFIED", "current_hash": current_hash, "anchored_hash": anchored_hash},
            )

            return IntegrityVerifyResponse(
                event_id=event_id,
                patient_id=patient_id,
                event_title=title,
                verification_status="TAMPERED_OR_MODIFIED",
                current_hash=current_hash,
                anchored_hash=anchored_hash,
                blockchain_tx_id=tx_id,
                block_number=blk,
                blockchain_timestamp=bc_ts,
                message="Integrity violation detected. Current database record hash does not match anchored blockchain proof.",
                verified_at=now_iso,
            )

    # 2. Case: Event missing or tombstoned in DB -> Check blockchain proof
    bc_proof = bc_service.get_proof(event_id)
    if bc_proof:
        anchored_patient_id = bc_proof.get("patient_id")
        if anchored_patient_id:
            mode = get_doctor_access_mode(client, doctor_id, anchored_patient_id)
            if not mode:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied. Doctor does not have valid active access to this patient.",
                )

        log_audit_event(
            client=client,
            actor_id=doctor_id,
            actor_role="DOCTOR",
            patient_id=anchored_patient_id or "unknown",
            action="INTEGRITY_VERIFY",
            access_type=mode or "NORMAL",
            entity_type="MEDICAL_EVENT",
            entity_id=event_id,
            reason="Historical record missing in DB but proof exists on blockchain",
            details={"status": "HISTORICAL RECORD MISSING", "proof": bc_proof},
        )

        return IntegrityVerifyResponse(
            event_id=event_id,
            patient_id=anchored_patient_id or "unknown",
            event_title=bc_proof.get("event_title", "Historical Critical Medical Event"),
            verification_status="HISTORICAL RECORD MISSING",
            current_hash=None,
            anchored_hash=bc_proof.get("event_hash"),
            blockchain_tx_id=bc_proof.get("blockchain_tx_id"),
            block_number=bc_proof.get("block_number"),
            blockchain_timestamp=bc_proof.get("blockchain_timestamp"),
            message="Blockchain proof exists on Hyperledger Fabric ledger, but corresponding medical record is missing or tombstoned in the primary database.",
            verified_at=now_iso,
        )

    # 3. Completely missing
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Medical event with ID '{event_id}' not found in database or blockchain ledger.",
    )


def anchor_medical_event_integrity(
    client: Client,
    doctor_id: str,
    event_id: str,
    notes: Optional[str] = None,
) -> IntegrityAnchorResponse:
    """
    Anchors a critical medical event record to the Hyperledger Fabric ledger.
    """
    ev_res = client.table("medical_events").select("*").eq("event_id", event_id).execute()
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

    canonical_str, event_hash = canonicalize_and_hash_event(event)

    bc_service = get_blockchain_service()
    tx_result = bc_service.anchor_event(
        event_id=event_id,
        patient_id=patient_id,
        event_hash=event_hash,
        event_title=event.get("title", "Critical Medical Event"),
        metadata={
            "doctor_id": doctor_id,
            "event_date": str(event.get("event_date")),
            "notes": notes,
        },
    )

    now_iso = datetime.now(timezone.utc).isoformat()

    ir_payload = {
        "event_id": event_id,
        "event_hash": event_hash,
        "hash_algorithm": "SHA-256",
        "event_version": event.get("version", 1) or 1,
        "blockchain_tx_id": tx_result["blockchain_tx_id"],
        "block_number": tx_result["block_number"],
        "blockchain_timestamp": tx_result["blockchain_timestamp"],
        "verification_status": "VERIFIED",
        "verified_at": now_iso,
    }

    try:
        client.table("integrity_records").delete().eq("event_id", event_id).execute()
    except Exception:
        pass

    ins_res = client.table("integrity_records").insert(ir_payload).execute()
    integrity_id = str(ins_res.data[0]["integrity_id"]) if ins_res.data else "unknown"

    log_audit_event(
        client=client,
        actor_id=doctor_id,
        actor_role="DOCTOR",
        patient_id=patient_id,
        action="INTEGRITY_ANCHOR",
        access_type=mode,
        entity_type="MEDICAL_EVENT",
        entity_id=event_id,
        reason=f"Anchored critical event to Hyperledger Fabric: {event.get('title')}",
        details={"tx_id": tx_result["blockchain_tx_id"], "block": tx_result["block_number"]},
    )

    return IntegrityAnchorResponse(
        integrity_id=integrity_id,
        event_id=event_id,
        patient_id=patient_id,
        event_title=event.get("title", "Critical Medical Event"),
        event_hash=event_hash,
        record_hash=event_hash,
        blockchain_tx_id=tx_result["blockchain_tx_id"],
        block_number=tx_result["block_number"],
        blockchain_network=tx_result.get("blockchain_network", "Hyperledger Fabric (meditrace-channel)"),
        blockchain_timestamp=tx_result.get("blockchain_timestamp"),
        anchored_at=tx_result.get("blockchain_timestamp"),
        verification_status="VERIFIED",
        status="ANCHORED",
        message="Event anchored to Hyperledger Fabric ledger successfully.",
    )


def get_patient_integrity_summary(
    client: Client,
    doctor_id: str,
    patient_id: str,
) -> PatientIntegritySummaryResponse:
    """
    Retrieves full integrity overview for all critical events of a patient.
    """
    mode = get_doctor_access_mode(client, doctor_id, patient_id)
    if not mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Doctor does not have valid active access to this patient.",
        )

    ev_res = client.table("medical_events").select("*").eq("patient_id", patient_id).execute()
    events = ev_res.data or []
    event_ids = [str(e["event_id"]) for e in events]

    ir_rows = []
    if event_ids:
        try:
            ir_res = client.table("integrity_records").select("*").in_("event_id", event_ids).execute()
            ir_rows = ir_res.data or []
        except Exception:
            pass

    verified_count = sum(1 for r in ir_rows if r.get("verification_status") == "VERIFIED")

    return PatientIntegritySummaryResponse(
        patient_id=patient_id,
        total_critical_events=len(events),
        total_anchored=len(ir_rows),
        total_verified=verified_count,
        integrity_records=ir_rows,
    )
