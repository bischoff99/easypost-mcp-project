"""Pytest configuration and shared fixtures."""

import os
from unittest.mock import AsyncMock, MagicMock

# Set test environment variables before importing app
os.environ.setdefault("EASYPOST_API_KEY", "test_key_for_pytest")
os.environ.setdefault("DATABASE_URL", "")

import pytest
from httpx import AsyncClient

from src.dependencies import get_easypost_service
from src.server import app
from tests.factories import EasyPostFactory


@pytest.fixture
def mock_easypost_service():
    """
    Create a mock EasyPost service with default responses.

    Can be customized in individual tests by setting return values.
    """
    from unittest.mock import PropertyMock

    mock = AsyncMock()

    # Set reasonable defaults
    mock.get_rates.return_value = EasyPostFactory.rates()
    mock.create_shipment.return_value = EasyPostFactory.shipment()
    mock.list_shipments.return_value = EasyPostFactory.shipment_list()
    mock.get_tracking.return_value = EasyPostFactory.tracking()

    # Add api_key as a regular attribute (not a Mock)
    type(mock).api_key = PropertyMock(return_value="test_api_key")

    return mock


@pytest.fixture
async def async_client(mock_easypost_service):
    """
    Create async HTTP client with dependency overrides.

    Uses httpx.AsyncClient for true async testing (not TestClient).
    Automatically cleans up overrides after test.
    """
    from httpx import ASGITransport

    # Override the dependency to use our mock
    app.dependency_overrides[get_easypost_service] = lambda: mock_easypost_service

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def client(mock_easypost_service):
    """
    Legacy TestClient fixture for backward compatibility.

    NOTE: Prefer async_client for new tests.
    """
    from contextlib import asynccontextmanager

    from fastapi.testclient import TestClient

    # Override the dependency to use our mock
    app.dependency_overrides[get_easypost_service] = lambda: mock_easypost_service

    # Replace FastMCP lifespan with simple test lifespan
    original_router = app.router.lifespan_context

    @asynccontextmanager
    async def test_lifespan(app_instance):
        # Empty lifespan for testing
        yield {}

    app.router.lifespan_context = test_lifespan

    with TestClient(app) as test_client:
        yield test_client

    # Restore lifespan and clean up
    app.router.lifespan_context = original_router
    app.dependency_overrides.clear()


@pytest.fixture
def mock_db_session():
    """Create a mock database session for testing database endpoints."""
    mock_session = MagicMock()

    async def mock_get_db_generator():
        """Mock async generator for get_db."""
        yield mock_session

    return mock_session, mock_get_db_generator
