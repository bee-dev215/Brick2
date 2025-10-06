"""
Pytest configuration and fixtures for BRICK 2 tests.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from brick2.core.database import get_async_session


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mock_database_session():
    """Mock database session for testing."""
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def override_get_db(mock_database_session):
    """Override the database dependency for testing."""
    try:
        from brick2.api.deps import get_db
        from brick2.main import app
        
        app.dependency_overrides[get_db] = lambda: mock_database_session
        yield
        app.dependency_overrides.clear()
    except ImportError:
        # Skip if app.main is not available (for unit tests)
        yield
