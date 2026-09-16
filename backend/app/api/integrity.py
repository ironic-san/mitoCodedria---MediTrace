from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.dependencies import AuthenticatedUser, require_doctor
from app.schemas.integrity import IntegrityVerifyResponse
from app.services.integrity_service import verify_medical_event_integrity
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()


class IntegrityVerifyRequest(BaseModel):
    event_id: str


@router.post("/verify", response_model=IntegrityVerifyResponse)
def verify_integrity(
    payload: IntegrityVerifyRequest,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """Verify a critical event for a doctor with NORMAL or BREAK_GLASS access."""
    event_id = payload.event_id.strip()
    client = get_supabase_service_client()
    return verify_medical_event_integrity(client, current_user.doctor_id, event_id)


@router.get("/{event_id}", response_model=IntegrityVerifyResponse)
def get_integrity(
    event_id: str,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """Return the current integrity verification result for a critical event."""
    client = get_supabase_service_client()
    return verify_medical_event_integrity(client, current_user.doctor_id, event_id)
