from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.dependencies import AuthenticatedUser, require_doctor
from app.schemas.integrity import (
    IntegrityAnchorRequest,
    IntegrityAnchorResponse,
    IntegrityVerifyResponse,
)
from app.services.blockchain_service import get_blockchain_service
from app.services.emergency_service import get_doctor_access_mode

from app.services.integrity_service import (
    anchor_medical_event_integrity,
    verify_medical_event_integrity,
)
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()


class CreateIntegrityEventRequest(BaseModel):
    patient_id: str
    event_type: str
    event_date: str
    title: str
    description: str = ""
    severity: str = "MODERATE"
    is_critical: bool = True
    status: str = "COMPLETED"


class IntegrityVerifyRequest(BaseModel):
    event_id: str


@router.post("/events")
def create_and_anchor_integrity_event(
    payload: CreateIntegrityEventRequest,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """Create a critical medical event and anchor its integrity proof."""
    client = get_supabase_service_client()

    mode = get_doctor_access_mode(
        client,
        current_user.doctor_id,
        payload.patient_id,
    )

    if not mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Doctor does not have valid active access to this patient.",
        )

    insert_result = (
        client.table("medical_events")
        .insert({
            "patient_id": payload.patient_id,
            "doctor_id": current_user.doctor_id,
            "event_type": payload.event_type,
            "event_date": payload.event_date,
            "title": payload.title,
            "description": payload.description,
            "severity": payload.severity,
            "is_critical": payload.is_critical,
            "status": payload.status,
        })
        .execute()
    )

    if not insert_result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create medical event.",
        )

    event = insert_result.data[0]

    anchored = anchor_medical_event_integrity(
        client,
        current_user.doctor_id,
        str(event["event_id"]),
        "Created and anchored through integrity API",
    )

    return {
        "event": event,
        "integrity": anchored,
    }




@router.get("/patient/{patient_id}")
def get_patient_integrity(
    patient_id: str,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """Return readable integrity events for a patient."""
    client = get_supabase_service_client()

    mode = get_doctor_access_mode(
        client,
        current_user.doctor_id,
        patient_id,
    )

    if not mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Doctor does not have valid active access to this patient.",
        )

    # Get integrity records belonging to this patient's medical events.
    event_res = (
        client.table("medical_events")
        .select("*")
        .eq("patient_id", patient_id)
        .eq("is_critical", True)
        .execute()
    )

    events = event_res.data or []

    if not events:
        return []

    event_ids = [str(e["event_id"]) for e in events]

    integrity_res = (
        client.table("integrity_records")
        .select("*")
        .in_("event_id", event_ids)
        .order("event_version", desc=False)
        .execute()
    )

    integrity_rows = integrity_res.data or []

    doctor_ids = list({
        str(e["doctor_id"])
        for e in events
        if e.get("doctor_id")
    })

    doctor_map = {}

    if doctor_ids:
        doctor_res = (
            client.table("doctors")
            .select("doctor_id,full_name")
            .in_("doctor_id", doctor_ids)
            .execute()
        )

        doctor_map = {
            str(d["doctor_id"]): d.get("full_name", "Unknown Doctor")
            for d in (doctor_res.data or [])
        }

    event_map = {
        str(e["event_id"]): e
        for e in events
    }

    # Only return proofs actually linked to medical events in integrity_records.
    readable = []

    for ir in integrity_rows:
        event_id = str(ir["event_id"])
        event = event_map.get(event_id)

        if not event:
            continue

        readable.append({
            "eventId": event_id,
            "date": str(event.get("event_date", ""))[:10],
            "eventType": event.get("event_type"),
            "event": event.get("title"),
            "description": event.get("description"),
            "severity": event.get("severity"),
            "reaction": None,
            "status": event.get("status"),
            "confirmedBy": doctor_map.get(
                str(event.get("doctor_id")),
                "Unknown Doctor",
            ),
            "integrityStatus": ir.get("verification_status"),
            "proofId": ir.get("blockchain_proof_id"),
            "recordVersion": ir.get("event_version"),
            "eventHash": ir.get("event_hash"),
            "blockchainTimestamp": ir.get("blockchain_timestamp"),
        })

    return readable


@router.get("/{event_id}", response_model=IntegrityVerifyResponse)
def get_integrity(
    event_id: str,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """Return the current integrity verification result for a critical event."""
    client = get_supabase_service_client()
    return verify_medical_event_integrity(client, current_user.doctor_id, event_id)
