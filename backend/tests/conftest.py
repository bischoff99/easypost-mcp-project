"""Pytest configuration and shared fixtures."""

from unittest.mock import AsyncMock

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
def client():
    """
    Legacy TestClient fixture for backward compatibility.

    NOTE: Prefer async_client for new tests.
    """
    from fastapi.testclient import TestClient

    return TestClient(app)
