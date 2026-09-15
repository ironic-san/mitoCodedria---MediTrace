from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import AuthenticatedUser, require_doctor
from app.schemas.integrity import (
    IntegrityAnchorRequest,
    IntegrityAnchorResponse,
    IntegrityVerifyResponse,
    PatientIntegritySummaryResponse,
)
from app.services.blockchain_service import get_blockchain_service
from app.services.integrity_service import (
    anchor_medical_event_integrity,
    get_patient_integrity_summary,
    verify_medical_event_integrity,
)
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()


@router.post("/{event_id}/verify", response_model=IntegrityVerifyResponse, summary="Verify critical medical event integrity")
@router.post("/verify/{event_id}", response_model=IntegrityVerifyResponse, summary="Verify critical medical event integrity (alias)")
def verify_event_integrity_endpoint(
    event_id: str,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """
    Verifies cryptographic integrity of a critical medical event against Hyperledger Fabric ledger.
    - Requires authenticated DOCTOR with active access to the patient.
    - Computes canonical SHA-256 hash from primary DB representation.
    - Compares against immutable blockchain proof.
    - Returns VERIFIED, HISTORICAL RECORD MISSING, TAMPERED_OR_MODIFIED, or NOT_ANCHORED.
    """
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    return verify_medical_event_integrity(
        client=client,
        doctor_id=current_user.doctor_id,
        event_id=event_id,
    )


@router.post("/anchor", response_model=IntegrityAnchorResponse, summary="Anchor a critical medical event to Hyperledger Fabric")
def anchor_event_integrity_endpoint(
    payload: IntegrityAnchorRequest,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """
    Anchors a critical medical event to the Hyperledger Fabric ledger.
    - Canonicalizes event record.
    - Generates SHA-256 hash.
    - Issues blockchain transaction.
    - Updates integrity_records in database.
    """
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    return anchor_medical_event_integrity(
        client=client,
        doctor_id=current_user.doctor_id,
        event_id=payload.event_id,
        notes=payload.notes,
    )


@router.get("/patient/{patient_id}", response_model=PatientIntegritySummaryResponse, summary="Get all integrity records for a patient")
def get_patient_integrity_overview_endpoint(
    patient_id: str,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """Retrieves full integrity overview and proof status for a patient's critical history."""
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    return get_patient_integrity_summary(
        client=client,
        doctor_id=current_user.doctor_id,
        patient_id=patient_id,
    )


@router.get("/blockchain/info", summary="Get Hyperledger Fabric channel and chaincode metadata")
def get_blockchain_info_endpoint(
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """Returns metadata about the active Hyperledger Fabric adapter and channel status."""
    bc_service = get_blockchain_service()
    return bc_service.get_channel_info()
