"""FastAPI application factory."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from ai_sdr.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: could verify DB connection, warm caches, etc.
    yield
    # Shutdown: cleanup resources


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        description="Autonomous AI Sales Development Representative",
        lifespan=lifespan,
    )

    # Register API routes
    from ai_sdr.api.v1.router import api_router

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": settings.APP_NAME}

    return app


app = create_app()
