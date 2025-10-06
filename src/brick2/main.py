"""FastAPI application main module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .core.config import settings
from .api.v1.api import api_router
from .core.database import init_db


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="2.0.0",
        description="BRICK 2 - Ad Orchestrator Backend",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )
    
    # Set up CORS
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Add trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.example.com"]
    )
    
    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Startup event
    @app.on_event("startup")
    async def startup_event():
        """Initialize database on startup."""
        await init_db()
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "version": "2.0.0",
            "environment": "development" if settings.DEBUG else "production"
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "BRICK 2 - Ad Orchestrator Backend",
            "version": "2.0.0",
            "docs": f"{settings.API_V1_STR}/docs"
        }
    
    return app


# Create the app instance
app = create_app()