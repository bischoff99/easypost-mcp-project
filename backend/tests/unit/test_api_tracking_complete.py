"""Complete API tests for tracking router."""

import builtins
import contextlib
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware

from src.routers.tracking import router


@pytest.fixture
def mock_service():
    """Create mock EasyPost service."""
    return AsyncMock()


@pytest.fixture
def app(mock_service):
    """Create test FastAPI app."""
    test_app = FastAPI()

    class RequestIDMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            request.state.request_id = "test-request-123"
            return await call_next(request)

    test_app.add_middleware(RequestIDMiddleware)
    test_app.include_router(router, prefix="/tracking")

    from src.dependencies import get_easypost_service

    test_app.dependency_overrides[get_easypost_service] = lambda: mock_service

    return test_app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


class TestTrackingEndpoint:
    """Test tracking endpoint comprehensively."""

    def test_track_shipment_success(self, client, mock_service):
        """Test successful tracking."""
        mock_service.get_tracking.return_value = {
            "status": "success",
            "data": {
                "tracking_number": "TRACK123",
                "status_detail": "delivered",
                "updated_at": "2025-11-06T00:00:00Z",
                "events": [{"status": "delivered", "message": "Delivered"}],
            },
            "message": "Tracking retrieved",
        }

        response = client.get("/tracking/TRACK123")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["tracking_number"] == "TRACK123"

    def test_track_shipment_error_raises_exception(self, client, mock_service):
        """Test tracking error handling."""
        mock_service.get_tracking.side_effect = Exception("Network error")

        response = client.get("/tracking/INVALID123")

        # Should return 500 error
        assert response.status_code == 500

    def test_track_shipment_logs_request(self, client, mock_service):
        """Test tracking logs the request."""
        mock_service.get_tracking.return_value = {
            "status": "success",
            "data": {"tracking_number": "LOG_TEST"},
        }

        with patch("src.routers.tracking.logger") as mock_logger:
            client.get("/tracking/LOG_TEST")

            # Should log info about the tracking request
            assert mock_logger.info.called

    def test_track_shipment_tracks_metrics(self, client, mock_service):
        """Test tracking records metrics."""
        mock_service.get_tracking.return_value = {
            "status": "success",
            "data": {"tracking_number": "METRICS"},
        }

        with patch("src.routers.tracking.metrics") as mock_metrics:
            client.get("/tracking/METRICS")

            # Should track the API call
            mock_metrics.track_api_call.assert_called_with("track_shipment", True)

    def test_track_shipment_metrics_on_error(self, client, mock_service):
        """Test metrics tracking on error."""
        mock_service.get_tracking.side_effect = Exception("Error")

        with patch("src.routers.tracking.metrics") as mock_metrics:
            with contextlib.suppress(builtins.BaseException):
                client.get("/tracking/ERROR_TEST")

            # Should track failed call
            mock_metrics.track_api_call.assert_called_with("track_shipment", False)

    def test_track_different_tracking_numbers(self, client, mock_service):
        """Test tracking with various tracking number formats."""
        for tracking_num in ["1234567890", "EZ123ABC", "TRACK_TEST_123"]:
            mock_service.get_tracking.return_value = {
                "status": "success",
                "data": {"tracking_number": tracking_num},
            }

            response = client.get(f"/tracking/{tracking_num}")
            assert response.status_code == 200
