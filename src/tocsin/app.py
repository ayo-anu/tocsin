"""FastAPI application construction for Tocsin."""

from fastapi import FastAPI

from tocsin.config import Settings


def create_app(settings: Settings) -> FastAPI:
    """Create an isolated Tocsin ASGI application."""
    app = FastAPI(title=settings.application_name)

    @app.get("/smoke")
    async def smoke() -> dict[str, str]:
        """Confirm that the minimal HTTP boundary is reachable."""
        return {"message": "Tocsin API is running."}

    return app
