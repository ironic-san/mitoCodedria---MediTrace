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

    # Demo Credentials for Hackathon
    DEMO_DOCTOR_PASSWORD: str = "Doctor@123!"
    DEMO_PATIENT_PASSWORD: str = "Patient@123!"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
