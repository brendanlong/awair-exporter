"""Configuration management for the Awair exporter."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    awair_access_token: str = Field(..., description="Awair API access token")
    awair_base_url: str = Field(
        default="https://developer-apis.awair.is", description="Base URL for Awair API"
    )


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()  # type: ignore
