import time
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import (
    AuthenticatedUser,
    get_current_user,
    require_doctor,
    require_patient,
)
from app.schemas.auth import LoginRequest, TokenResponse, UserMeResponse
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()


@router.post("/login", response_model=TokenResponse, summary="Authenticate user and issue token")
def login(payload: LoginRequest):
    """
    Authenticates email and password against Supabase Auth, returning a Bearer access_token.
    Retries transient connection drops automatically.
    """
    email = payload.email.strip()
    password = payload.password

    # Retry logic for transient network disconnects
    auth_res = None
    last_err = None
    for attempt in range(3):
        try:
            auth_client = get_supabase_service_client()
            auth_res = auth_client.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })
            if auth_res:
                break
        except Exception as e:
            last_err = e
            err_str = str(e).lower()
            if "invalid login credentials" in err_str or "invalid credentials" in err_str:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password.",
                ) from e
            if attempt < 2:
                time.sleep(0.5)
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Authentication failed: {e}",
                ) from e

    session = getattr(auth_res, "session", auth_res)
    user = getattr(auth_res, "user", None)

    if not session or not getattr(session, "access_token", None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or sign-in failed.",
        )

    access_token = session.access_token
    expires_in = getattr(session, "expires_in", None)
    refresh_token = getattr(session, "refresh_token", None)
    auth_user_id = str(getattr(user, "id", "")) if user else ""

    # Fetch assigned role using clean service_role client
    role = None
    if auth_user_id:
        db_client = get_supabase_service_client()
        role_res = db_client.table("user_roles").select("role").eq("auth_user_id", auth_user_id).execute()
        if role_res.data:
            role = role_res.data[0].get("role")

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_in,
        refresh_token=refresh_token,
        role=role,
        user_id=auth_user_id,
    )


@router.get("/me", response_model=UserMeResponse, summary="Get current authenticated user identity & profile")
def get_me(current_user: AuthenticatedUser = Depends(get_current_user)):
    """
    Returns identity and role-linked ID for current authenticated user.
    """
    return UserMeResponse(
        auth_user_id=current_user.auth_user_id,
        email=current_user.email,
        role=current_user.role,
        doctor_id=current_user.doctor_id,
        patient_id=current_user.patient_id,
        full_name=current_user.full_name,
        specialization=current_user.specialization,
        hospital_name=current_user.hospital_name,
        phone=current_user.phone,
        date_of_birth=current_user.date_of_birth,
        blood_group=current_user.blood_group,
    )


@router.get("/doctor-only", summary="Test endpoint for doctor-only authorization")
def doctor_only_test(current_user: AuthenticatedUser = Depends(require_doctor)):
    """Sample endpoint asserting require_doctor dependency."""
    return {
        "status": "granted",
        "message": f"Welcome Dr. {current_user.full_name}",
        "doctor_id": current_user.doctor_id,
        "role": current_user.role,
    }


@router.get("/patient-only", summary="Test endpoint for patient-only authorization")
def patient_only_test(current_user: AuthenticatedUser = Depends(require_patient)):
    """Sample endpoint asserting require_patient dependency."""
    return {
        "status": "granted",
        "message": f"Welcome {current_user.full_name}",
        "patient_id": current_user.patient_id,
        "role": current_user.role,
    }
