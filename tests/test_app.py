"""Tests for the minimal HTTP application boundary."""

import asyncio
from unittest.mock import Mock

import httpx
import pytest
from fastapi import FastAPI
from pydantic import ValidationError
from pytest import MonkeyPatch

from tocsin.app import create_app
from tocsin.config import EnvironmentName, LogLevel, Settings
from tocsin.main import main


def make_settings() -> Settings:
    """Build settings without consulting ambient values for tested fields."""
    return Settings(
        environment=EnvironmentName.TEST,
        log_level=LogLevel.INFO,
        application_name="Tocsin",
    )


def test_create_app_returns_isolated_fastapi_instances() -> None:
    """Each factory call constructs a distinct application."""
    settings = make_settings()
    first_app = create_app(settings)
    second_app = create_app(settings)

    assert isinstance(first_app, FastAPI)
    assert isinstance(second_app, FastAPI)
    assert first_app is not second_app


async def get(path: str) -> httpx.Response:
    """Issue an in-process request to a new application instance."""
    transport = httpx.ASGITransport(app=create_app(make_settings()))
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.get(path)


def test_smoke_route_returns_deterministic_response() -> None:
    """The smoke route proves that the in-process HTTP boundary works."""
    response = asyncio.run(get("/smoke"))

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"message": "Tocsin API is running."}


def test_later_monitoring_routes_are_absent() -> None:
    """Health and metrics semantics remain deferred to their roadmap task."""
    assert asyncio.run(get("/health")).status_code == 404
    assert asyncio.run(get("/metrics")).status_code == 404


def test_main_passes_loaded_settings_to_application(monkeypatch: MonkeyPatch) -> None:
    """The executable passes one settings object through the composition root."""
    settings = make_settings()
    app = Mock(spec=FastAPI)
    load_settings = Mock(return_value=settings)
    create_app = Mock(return_value=app)
    run = Mock()
    monkeypatch.setattr("tocsin.main.load_settings", load_settings)
    monkeypatch.setattr("tocsin.main.create_app", create_app)
    monkeypatch.setattr("tocsin.main.uvicorn.run", run)

    main()

    load_settings.assert_called_once_with()
    create_app.assert_called_once_with(settings)
    run.assert_called_once_with(
        app,
        host="127.0.0.1",
        port=8000,
    )


def test_main_rejects_invalid_environment_before_serving(monkeypatch: MonkeyPatch) -> None:
    """Invalid real environment configuration prevents Uvicorn startup."""
    monkeypatch.setenv("TOCSIN_LOG_LEVEL", "INVALID")
    run = Mock()
    monkeypatch.setattr("tocsin.main.uvicorn.run", run)

    with pytest.raises(ValidationError):
        main()

    run.assert_not_called()
