import time
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.core.security import verify_supabase_token
from app.services.supabase_service import get_supabase_service_client

security_scheme = HTTPBearer(auto_error=False)


class AuthenticatedUser(BaseModel):
    """Container for authenticated user context and application role."""
    auth_user_id: str
    email: str
    role: str  # "DOCTOR" or "PATIENT"
    doctor_id: Optional[str] = None
    patient_id: Optional[str] = None
    full_name: Optional[str] = None
    specialization: Optional[str] = None
    hospital_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    blood_group: Optional[str] = None
    profile_data: dict = {}

    @property
    def user_id(self) -> str:
        return self.auth_user_id


def query_table_with_retry(table_name: str, select_fields: str, filter_col: str, filter_val: str):
    """Executes a Supabase PostgREST query with automatic retries for transient connection drops."""
    last_err = None
    for attempt in range(3):
        try:
            client = get_supabase_service_client()
            res = client.table(table_name).select(select_fields).eq(filter_col, filter_val).execute()
            return res.data or []
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(0.3)
    raise RuntimeError(f"Database query on '{table_name}' failed after 3 attempts: {last_err}")


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> AuthenticatedUser:
    """
    FastAPI dependency to extract Bearer token, verify Supabase JWT,
    resolve application role from user_roles, and populate doctor/patient profile.

    - Missing/invalid/expired token -> HTTP 401
    - User has no assigned role -> HTTP 403
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header or Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme. Bearer token required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    # 1. Verify token with Supabase Auth
    token_data = verify_supabase_token(token)
    auth_user_id = token_data["auth_user_id"]
    token_email = token_data["email"]

    # 2. Resolve user role from user_roles table
    try:
        roles_data = query_table_with_retry(
            table_name="user_roles",
            select_fields="role",
            filter_col="auth_user_id",
            filter_val=auth_user_id
        )
        if not roles_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. User has no assigned application role.",
            )
        role = roles_data[0].get("role", "").upper()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query user roles: {e}",
        ) from e

    # 3. Resolve role-specific record (doctors or patients)
    doctor_id = None
    patient_id = None
    full_name = None
    specialization = None
    hospital_name = None
    phone = None
    date_of_birth = None
    blood_group = None
    profile_data = {}

    if role == "DOCTOR":
        try:
            docs_data = query_table_with_retry(
                table_name="doctors",
                select_fields="*",
                filter_col="auth_user_id",
                filter_val=auth_user_id
            )

            if not docs_data and token_email:
                docs_data = query_table_with_retry(
                    table_name="doctors",
                    select_fields="*",
                    filter_col="email",
                    filter_val=token_email
                )

            if not docs_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doctor profile not found for authenticated user.",
                )

            doc = docs_data[0]
            doctor_id = str(doc.get("doctor_id"))
            full_name = doc.get("full_name")
            specialization = doc.get("specialization")
            hospital_name = doc.get("hospital_name")
            phone = doc.get("phone")
            profile_data = doc
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to query doctor profile: {e}",
            ) from e

    elif role == "PATIENT":
        try:
            pats_data = query_table_with_retry(
                table_name="patients",
                select_fields="*",
                filter_col="auth_user_id",
                filter_val=auth_user_id
            )
            if not pats_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Patient profile not found for authenticated user.",
                )
            pat = pats_data[0]
            patient_id = str(pat.get("patient_id"))
            full_name = pat.get("full_name")
            date_of_birth = str(pat.get("date_of_birth")) if pat.get("date_of_birth") else None
            blood_group = pat.get("blood_group")
            phone = pat.get("phone")
            profile_data = pat
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to query patient profile: {e}",
            ) from e

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid user role '{role}'. Only DOCTOR and PATIENT are allowed.",
        )

    return AuthenticatedUser(
        auth_user_id=auth_user_id,
        email=token_email or profile_data.get("email", ""),
        role=role,
        doctor_id=doctor_id,
        patient_id=patient_id,
        full_name=full_name,
        specialization=specialization,
        hospital_name=hospital_name,
        phone=phone,
        date_of_birth=date_of_birth,
        blood_group=blood_group,
        profile_data=profile_data,
    )


def require_doctor(
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    """FastAPI dependency asserting that current user has role DOCTOR."""
    if current_user.role != "DOCTOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Doctor privileges required.",
        )
    return current_user


def require_patient(
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    """FastAPI dependency asserting that current user has role PATIENT."""
    if current_user.role != "PATIENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Patient privileges required.",
        )
    return current_user
