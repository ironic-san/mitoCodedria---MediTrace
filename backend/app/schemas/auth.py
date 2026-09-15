from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Payload for user login."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Authentication token response payload."""
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    role: Optional[str] = None
    user_id: Optional[str] = None


class UserMeResponse(BaseModel):
    """User profile response for /auth/me endpoint."""
    auth_user_id: str
    email: str
    role: str
    doctor_id: Optional[str] = None
    patient_id: Optional[str] = None
    full_name: Optional[str] = None
    specialization: Optional[str] = None
    hospital_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    blood_group: Optional[str] = None
