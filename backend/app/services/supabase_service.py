from supabase import create_client, Client
from app.core.config import get_settings


def get_supabase_service_client() -> Client:
    """
    Returns a fresh server-side Supabase client with administrative service_role privileges.
    Creates a new client instance to ensure user sessions do not mutate administrative state.
    WARNING: Backend-only! Never expose this client or its credentials to frontend clients.
    """
    settings = get_settings()
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


def get_supabase_client() -> Client:
    """Convenience alias for the backend Supabase service-role client."""
    return get_supabase_service_client()
