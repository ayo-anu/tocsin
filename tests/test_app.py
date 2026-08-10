"""Tests for the minimal HTTP application boundary."""

import asyncio
from unittest.mock import Mock

import httpx
from fastapi import FastAPI
from pytest import MonkeyPatch

from tocsin.app import create_app
from tocsin.main import main


def test_create_app_returns_isolated_fastapi_instances() -> None:
    """Each factory call constructs a distinct application."""
    first_app = create_app()
    second_app = create_app()

    assert isinstance(first_app, FastAPI)
    assert isinstance(second_app, FastAPI)
    assert first_app is not second_app


async def get(path: str) -> httpx.Response:
    """Issue an in-process request to a new application instance."""
    transport = httpx.ASGITransport(app=create_app())
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


def test_main_runs_application_factory_on_loopback(monkeypatch: MonkeyPatch) -> None:
    """The executable delegates to Uvicorn with the approved local boundary."""
    run = Mock()
    monkeypatch.setattr("tocsin.main.uvicorn.run", run)

    main()

    run.assert_called_once_with(
        "tocsin.app:create_app",
        factory=True,
        host="127.0.0.1",
        port=8000,
    )
