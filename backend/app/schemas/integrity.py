from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class IntegrityVerifyResponse(BaseModel):
    """Response payload for critical medical event integrity verification."""
    event_id: str
    patient_id: Optional[str] = None
    event_title: Optional[str] = None
    verification_status: str  # VERIFIED, HISTORICAL RECORD MISSING, TAMPERED_OR_MODIFIED, NOT_ANCHORED
    current_hash: Optional[str] = None
    anchored_hash: Optional[str] = None
    blockchain_tx_id: Optional[str] = None
    block_number: Optional[int] = None
    blockchain_timestamp: Optional[str] = None
    message: str
    canonical_event_data: Optional[Dict[str, Any]] = None
    verified_at: Optional[str] = None


class IntegrityAnchorRequest(BaseModel):
    """Request payload to anchor a critical medical event to the blockchain."""
    event_id: str
    notes: Optional[str] = None


class IntegrityAnchorResponse(BaseModel):
    """Response confirmation for anchoring a critical medical event."""
    integrity_id: str
    event_id: str
    patient_id: str
    event_title: Optional[str] = "Critical Medical Event"
    event_hash: Optional[str] = None
    record_hash: Optional[str] = None
    blockchain_tx_id: Optional[str] = None
    block_number: Optional[int] = None
    blockchain_timestamp: Optional[str] = None
    anchored_at: Optional[str] = None
    blockchain_network: Optional[str] = "Hyperledger Fabric (meditrace-channel)"
    verification_status: Optional[str] = "VERIFIED"
    status: Optional[str] = "ANCHORED"
    message: Optional[str] = "Event anchored to Hyperledger Fabric ledger successfully."


class PatientIntegritySummaryResponse(BaseModel):
    """Summary of all integrity proofs for a patient's critical history."""
    patient_id: str
    total_critical_events: int
    total_anchored: int
    total_verified: int
    records: List[IntegrityVerifyResponse] = Field(default_factory=list)
