from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment and .env."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "MediTrace Backend"
    VERSION: str = "1.0.0"

    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # Uses the same secret name as the existing OCR/NLU project.
    GEMINI_API_KEY: str | None = None
    AI_PROVIDER: str = "gemini"
    AI_MODEL: str = "gemini-3.5-flash-lite"

    # Comma-separated browser origins. Do not use '*' with credentials.
    FRONTEND_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Demo Credentials for Hackathon
    DEMO_DOCTOR_PASSWORD: str = "Doctor@123!"
    DEMO_PATIENT_PASSWORD: str = "Patient@123!"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
