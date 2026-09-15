from typing import Optional
from pydantic import BaseModel, Field


class GrantAccessRequest(BaseModel):
    """Payload for patient granting doctor access."""
    doctor_id: Optional[str] = Field(None, description="UUID of the target doctor")
    doctor_email: Optional[str] = Field(None, description="Email of the target doctor")
    duration_days: int = Field(7, ge=1, le=365, description="Access duration in days (default: 7)")


class AccessRecordResponse(BaseModel):
    """Access record information."""
    access_id: str
    doctor_id: str
    doctor_name: Optional[str] = None
    doctor_email: Optional[str] = None
    patient_id: str
    patient_name: Optional[str] = None
    granted_at: str
    expires_at: Optional[str] = None
    status: str  # ACTIVE, EXPIRED, REVOKED
    relationship_type: str = "NORMAL_ACCESS"
