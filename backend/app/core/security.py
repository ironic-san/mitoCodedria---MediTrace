import time
from fastapi import HTTPException, status
from app.services.supabase_service import get_supabase_service_client


def verify_supabase_token(token: str) -> dict:
    """
    Cryptographically validates the Supabase JWT access token against Supabase Auth server.
    Ensures signature, issuer, and expiration are verified by Supabase Auth API.
    Retries transient connection drops automatically.
    Returns dict containing user information if valid, or raises HTTP 401.
    """
    if not token or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    clean_token = token.strip()
    res = None
    last_exc = None

    for attempt in range(3):
        try:
            client = get_supabase_service_client()
            res = client.auth.get_user(clean_token)
            if res:
                break
        except Exception as e:
            last_exc = e
            err_str = str(e).lower()
            if "jwt expired" in err_str or "token is expired" in err_str:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication token has expired.",
                    headers={"WWW-Authenticate": "Bearer"},
                ) from e
            elif "invalid jwt" in err_str or "invalid token" in err_str or "jwt claim" in err_str:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication token signature or claims.",
                    headers={"WWW-Authenticate": "Bearer"},
                ) from e

            if attempt < 2:
                time.sleep(0.5)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication token verification failed: {last_exc}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = getattr(res, "user", res)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    uid = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)
    email = getattr(user, "email", None) or (user.get("email") if isinstance(user, dict) else None)

    if not uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not resolve user identity from authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "auth_user_id": str(uid),
        "email": str(email) if email else "",
        "raw_user": user,
    }
