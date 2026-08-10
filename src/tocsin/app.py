"""FastAPI application construction for Tocsin."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create an isolated Tocsin ASGI application."""
    app = FastAPI(title="Tocsin")

    @app.get("/smoke")
    async def smoke() -> dict[str, str]:
        """Confirm that the minimal HTTP boundary is reachable."""
        return {"message": "Tocsin API is running."}

    return app
