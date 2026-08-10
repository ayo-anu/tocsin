"""Tests for validated runtime configuration."""

from collections.abc import Iterator

import pytest
from pydantic import ValidationError
from pytest import MonkeyPatch

from tocsin.app import create_app
from tocsin.config import EnvironmentName, LogLevel, load_settings

CONFIGURATION_VARIABLES = (
    "TOCSIN_ENVIRONMENT",
    "TOCSIN_LOG_LEVEL",
    "TOCSIN_APPLICATION_NAME",
)


@pytest.fixture(autouse=True)
def isolate_configuration_environment(monkeypatch: MonkeyPatch) -> Iterator[None]:
    """Prevent configuration tests from reading recognized ambient values."""
    for variable in CONFIGURATION_VARIABLES:
        monkeypatch.delenv(variable, raising=False)
    yield


def test_load_settings_uses_safe_local_defaults() -> None:
    """Missing configuration resolves to safe local values."""
    settings = load_settings()

    assert settings.environment is EnvironmentName.LOCAL
    assert settings.log_level is LogLevel.INFO
    assert settings.application_name == "Tocsin"


def test_settings_are_immutable() -> None:
    """Validated configuration cannot be mutated at runtime."""
    settings = load_settings()

    with pytest.raises(ValidationError):
        setattr(settings, "log_level", LogLevel.DEBUG)


def test_load_settings_reads_valid_environment_overrides(monkeypatch: MonkeyPatch) -> None:
    """Recognized variables override defaults and retain typed values."""
    monkeypatch.setenv("TOCSIN_ENVIRONMENT", "test")
    monkeypatch.setenv("TOCSIN_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("TOCSIN_APPLICATION_NAME", "  Tocsin Test  ")

    settings = load_settings()

    assert settings.environment is EnvironmentName.TEST
    assert settings.log_level is LogLevel.DEBUG
    assert settings.application_name == "Tocsin Test"
    assert create_app(settings).title == "Tocsin Test"


@pytest.mark.parametrize(
    ("variable", "value", "field"),
    [
        ("TOCSIN_ENVIRONMENT", "staging", "environment"),
        ("TOCSIN_LOG_LEVEL", "verbose", "log_level"),
        ("TOCSIN_APPLICATION_NAME", "   ", "application_name"),
        ("TOCSIN_APPLICATION_NAME", "x" * 101, "application_name"),
    ],
)
def test_load_settings_rejects_invalid_values(
    monkeypatch: MonkeyPatch,
    variable: str,
    value: str,
    field: str,
) -> None:
    """Malformed environment values fail with their field identified."""
    monkeypatch.setenv(variable, value)

    with pytest.raises(ValidationError) as error:
        load_settings()

    assert field in str(error.value)
