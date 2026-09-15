from typing import Optional
from pydantic import BaseModel


class DoctorProfileResponse(BaseModel):
    """Authenticated doctor profile response."""
    doctor_id: str
    auth_user_id: Optional[str] = None
    full_name: str
    email: str
    phone: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    hospital_name: Optional[str] = None


class DoctorPatientItem(BaseModel):
    """Patient overview accessible by an authorized doctor."""
    patient_id: str
    full_name: str
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    access_status: str
    access_expiry: Optional[str] = None
    relationship_type: str = "NORMAL_ACCESS"
