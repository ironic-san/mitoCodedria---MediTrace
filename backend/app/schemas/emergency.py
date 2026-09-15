from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.patient import (
    MedicalEventItem,
    PatientAllergyItem,
    PatientConditionItem,
    PatientMedicationItem,
    PatientProfile,
)


class BreakGlassRequest(BaseModel):
    patient_id: str = Field(..., description="Target patient UUID")
    reason: str = Field(..., min_length=5, description="Clinical justification for emergency break-glass access")
    duration_hours: Optional[int] = Field(4, ge=1, le=24, description="Emergency session validity in hours (default: 4, max: 24)")


class BreakGlassResponse(BaseModel):
    session_id: str
    doctor_id: str
    patient_id: str
    status: str = "ACTIVE"
    started_at: str
    expires_at: str
    reason: str
    access_type: str = "BREAK_GLASS"
    allowed_scopes: List[str] = [
        "CRITICAL_PROFILE",
        "CRITICAL_ALLERGIES",
        "CRITICAL_CONDITIONS",
        "CRITICAL_MEDICATIONS",
        "CRITICAL_EVENTS",
        "RAG_HISTORICAL_QUERY",
        "INTEGRITY_VERIFICATION",
    ]
    message: str = "Break-glass emergency authorization granted. Read-only critical access active."


class BreakGlassEndRequest(BaseModel):
    patient_id: str = Field(..., description="Target patient UUID")
    reason: Optional[str] = Field("Emergency treatment concluded", description="Reason for ending emergency session")


class BreakGlassEndResponse(BaseModel):
    session_id: Optional[str]
    doctor_id: str
    patient_id: str
    status: str = "ENDED"
    ended_at: str
    message: str = "Break-glass emergency session concluded successfully."


class EmergencyMedicalSummaryResponse(BaseModel):
    patient_id: str
    access_type: str = "BREAK_GLASS"
    accessed_at: str
    profile: PatientProfile
    critical_allergies: List[PatientAllergyItem]
    critical_conditions: List[PatientConditionItem]
    critical_medications: List[PatientMedicationItem]
    critical_events: List[MedicalEventItem]
    disclaimer: str = (
        "EMERGENCY BREAK-GLASS RECORD: Filtered to critical information only. "
        "Write operations are strictly prohibited under emergency access. "
        "All emergency access actions are audited."
    )
