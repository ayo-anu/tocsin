"""Executable server boundary for the Tocsin API."""

import uvicorn

from tocsin.app import create_app
from tocsin.config import load_settings


def main() -> None:
    """Load configuration and run Tocsin on the local interface."""
    settings = load_settings()
    app = create_app(settings)
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
