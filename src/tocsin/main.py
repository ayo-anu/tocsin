"""Executable server boundary for the Tocsin API."""

import uvicorn


def main() -> None:
    """Run the application factory through Uvicorn on the local interface."""
    uvicorn.run(
        "tocsin.app:create_app",
        factory=True,
        host="127.0.0.1",
        port=8000,
    )
