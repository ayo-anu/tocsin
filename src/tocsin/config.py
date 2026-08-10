"""Validated runtime configuration for Tocsin."""

from enum import StrEnum

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentName(StrEnum):
    """Supported runtime environment names."""

    LOCAL = "local"
    TEST = "test"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    """Supported application log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    """Immutable, validated process settings."""

    model_config = SettingsConfigDict(env_prefix="TOCSIN_", frozen=True)

    environment: EnvironmentName = EnvironmentName.LOCAL
    log_level: LogLevel = LogLevel.INFO
    application_name: str = Field(default="Tocsin", min_length=1, max_length=100)

    @field_validator("application_name", mode="before")
    @classmethod
    def normalize_application_name(cls, value: object) -> object:
        """Remove surrounding whitespace before length validation."""
        return value.strip() if isinstance(value, str) else value


def load_settings() -> Settings:
    """Read and validate settings from the process environment."""
    return Settings()
