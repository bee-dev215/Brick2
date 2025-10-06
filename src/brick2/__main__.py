"""Main entry point for running the application."""

import uvicorn
from .core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "brick2.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
