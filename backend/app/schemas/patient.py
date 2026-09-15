from typing import List, Optional
from pydantic import BaseModel


class PatientProfile(BaseModel):
    """Basic patient profile information."""
    patient_id: str
    auth_user_id: Optional[str] = None
    full_name: str
    date_of_birth: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None


class PatientAllergyItem(BaseModel):
    """Allergy item for patient passport."""
    patient_allergy_id: str
    allergy_id: Optional[str] = None
    allergen: str
    allergy_type: Optional[str] = None
    severity: Optional[str] = None
    reaction: Optional[str] = None
    status: Optional[str] = None
    first_reported: Optional[str] = None
    confirmed_date: Optional[str] = None
    notes: Optional[str] = None


class PatientConditionItem(BaseModel):
    """Medical condition item for patient passport."""
    patient_condition_id: str
    condition_id: Optional[str] = None
    condition_name: str
    description: Optional[str] = None
    status: Optional[str] = None
    severity: Optional[str] = None
    diagnosed_date: Optional[str] = None
    resolved_date: Optional[str] = None
    notes: Optional[str] = None


class PatientMedicationItem(BaseModel):
    """Medication item for patient passport."""
    patient_medication_id: str
    medication_id: Optional[str] = None
    medication_name: str
    generic_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = None
    prescribed_by: Optional[str] = None
    prescribed_by_name: Optional[str] = None
    instructions: Optional[str] = None


class MedicalEventItem(BaseModel):
    """Medical event item for patient timeline."""
    event_id: str
    doctor_id: Optional[str] = None
    doctor_name: Optional[str] = None
    event_type: Optional[str] = None
    event_date: Optional[str] = None
    title: str
    description: Optional[str] = None
    severity: Optional[str] = None
    is_critical: bool = False
    status: Optional[str] = None
    version: int = 1
    source_document_id: Optional[str] = None


class IntegrityRecordItem(BaseModel):
    """Cryptographic provenance integrity record item."""
    integrity_id: str
    event_id: str
    event_title: Optional[str] = None
    event_hash: str
    hash_algorithm: str = "SHA-256"
    event_version: int = 1
    blockchain_tx_id: Optional[str] = None
    block_number: Optional[int] = None
    blockchain_timestamp: Optional[str] = None
    verification_status: str = "VERIFIED"
    verified_at: Optional[str] = None


class MedicalSummaryResponse(BaseModel):
    """Consolidated Medical Passport and Summary payload."""
    profile: PatientProfile
    allergies: List[PatientAllergyItem] = []
    conditions: List[PatientConditionItem] = []
    medications: List[PatientMedicationItem] = []
    medical_events: List[MedicalEventItem] = []
    critical_history: List[MedicalEventItem] = []
    integrity_records: List[IntegrityRecordItem] = []
