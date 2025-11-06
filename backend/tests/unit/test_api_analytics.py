"""API tests for analytics router."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware

from src.routers.analytics import router


@pytest.fixture
def mock_service():
    """Create mock EasyPost service."""
    service = AsyncMock()
    return service


@pytest.fixture
def app(mock_service):
    """Create test FastAPI app with analytics router."""
    test_app = FastAPI()
    
    # Add request_id middleware simulation
    class RequestIDMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            request.state.request_id = "test-request-123"
            response = await call_next(request)
            return response
    
    test_app.add_middleware(RequestIDMiddleware)
    test_app.include_router(router, prefix="/analytics")
    
    # Override dependency
    from src.dependencies import get_easypost_service
    test_app.dependency_overrides[get_easypost_service] = lambda: mock_service
    
    return test_app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


class TestAnalyticsEndpoint:
    """Test /analytics endpoint."""

    def test_get_analytics_success(self, client, mock_service):
        """Test getting analytics successfully."""
        # Mock service response
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [
                {
                    "id": "shp_1",
                    "carrier": "USPS",
                    "rate": "10.50",
                    "status": "delivered",
                    "created_at": datetime.now(UTC).isoformat(),
                    "from_address": {"city": "LA"},
                    "to_address": {"city": "NYC"},
                },
                {
                    "id": "shp_2",
                    "carrier": "UPS",
                    "rate": "15.75",
                    "status": "in_transit",
                    "created_at": datetime.now(UTC).isoformat(),
                    "from_address": {"city": "SF"},
                    "to_address": {"city": "Boston"},
                },
            ],
        }
        
        # Make request
        response = client.get("/analytics/analytics?days=30")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        assert "summary" in data["data"]
        assert "by_carrier" in data["data"]
        assert "by_date" in data["data"]
        assert "top_routes" in data["data"]

    def test_get_analytics_custom_days(self, client, mock_service):
        """Test analytics with custom day range."""
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [],
        }
        
        response = client.get("/analytics/analytics?days=7")
        
        assert response.status_code == 200
        data = response.json()
        # Should still return structure even with no data
        assert "data" in data

    def test_get_analytics_service_error(self, client, mock_service):
        """Test analytics handles service errors."""
        mock_service.list_shipments.return_value = {
            "status": "error",
            "message": "Failed to fetch shipments",
        }
        
        response = client.get("/analytics/analytics?days=30")
        
        # Should return 500 error
        assert response.status_code == 500

    def test_get_analytics_carrier_aggregation(self, client, mock_service):
        """Test analytics aggregates carriers correctly."""
        # Multiple shipments with same carrier
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [
                {"carrier": "USPS", "rate": "10", "status": "delivered", 
                 "created_at": datetime.now(UTC).isoformat(),
                 "from_address": {"city": "LA"}, "to_address": {"city": "NYC"}},
                {"carrier": "USPS", "rate": "12", "status": "delivered",
                 "created_at": datetime.now(UTC).isoformat(),
                 "from_address": {"city": "LA"}, "to_address": {"city": "NYC"}},
                {"carrier": "UPS", "rate": "20", "status": "in_transit",
                 "created_at": datetime.now(UTC).isoformat(),
                 "from_address": {"city": "SF"}, "to_address": {"city": "Boston"}},
            ],
        }
        
        response = client.get("/analytics/analytics?days=30")
        data = response.json()
        
        # Should aggregate by carrier
        carriers = data["data"]["by_carrier"]
        assert len(carriers) == 2  # USPS and UPS
        
        # USPS should have 2 shipments
        usps_data = [c for c in carriers if c["carrier"] == "USPS"][0]
        assert usps_data["shipment_count"] == 2


class TestStatsEndpoint:
    """Test /stats endpoint."""

    def test_get_stats_success(self, client, mock_service):
        """Test getting dashboard stats successfully."""
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [
                {"rate": "10.50", "status": "delivered"},
                {"rate": "15.75", "status": "in_transit"},
                {"rate": "8.25", "status": "pre_transit"},
            ],
        }
        
        response = client.get("/analytics/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        stats = data["data"]
        assert "total_shipments" in stats
        assert "active_deliveries" in stats
        assert "total_cost" in stats
        assert "delivery_success_rate" in stats

    def test_get_stats_empty_data(self, client, mock_service):
        """Test stats with no shipments."""
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [],
        }
        
        response = client.get("/analytics/stats")
        
        assert response.status_code == 200
        data = response.json()
        # Should handle empty gracefully
        stats = data["data"]
        assert stats["total_shipments"]["value"] == 0

    def test_get_stats_calculates_cost(self, client, mock_service):
        """Test stats calculates total cost correctly."""
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [
                {"rate": "10.50", "status": "delivered"},
                {"rate": "15.75", "status": "delivered"},
                {"rate": "8.25", "status": "delivered"},
            ],
        }
        
        response = client.get("/analytics/stats")
        data = response.json()
        
        total_cost = data["data"]["total_cost"]["value"]
        # Should sum to 34.50
        assert total_cost == 34.50

    def test_get_stats_counts_active_deliveries(self, client, mock_service):
        """Test stats counts active deliveries."""
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [
                {"rate": "10", "status": "in_transit"},
                {"rate": "10", "status": "pre_transit"},
                {"rate": "10", "status": "out_for_delivery"},
                {"rate": "10", "status": "delivered"},
            ],
        }
        
        response = client.get("/analytics/stats")
        data = response.json()
        
        # First 3 are active, last is delivered
        active = data["data"]["active_deliveries"]["value"]
        assert active == 3

    def test_get_stats_service_error(self, client, mock_service):
        """Test stats handles service errors."""
        mock_service.list_shipments.return_value = {
            "status": "error",
            "message": "Service unavailable",
        }
        
        response = client.get("/analytics/stats")
        
        assert response.status_code == 500


class TestCarrierPerformanceEndpoint:
    """Test /carrier-performance endpoint."""

    def test_get_carrier_performance_success(self, client, mock_service):
        """Test getting carrier performance."""
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [
                {"carrier": "USPS", "status": "delivered"},
                {"carrier": "USPS", "status": "delivered"},
                {"carrier": "USPS", "status": "in_transit"},
                {"carrier": "UPS", "status": "delivered"},
            ],
        }
        
        response = client.get("/analytics/carrier-performance")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 2  # USPS and UPS

    def test_carrier_performance_calculates_rates(self, client, mock_service):
        """Test carrier performance calculates on-time rates."""
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [
                {"carrier": "USPS", "status": "delivered"},
                {"carrier": "USPS", "status": "delivered"},
                {"carrier": "USPS", "status": "returned"},  # Completed but not delivered
            ],
        }
        
        response = client.get("/analytics/carrier-performance")
        data = response.json()
        
        carriers = data["data"]
        usps = [c for c in carriers if c["carrier"] == "USPS"][0]
        
        # 2 delivered out of 3 completed = 67% (rounded to 67)
        assert usps["shipments"] == 3
        assert usps["rate"] >= 60  # Approximately 67%

    def test_carrier_performance_empty_data(self, client, mock_service):
        """Test carrier performance with no data."""
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [],
        }
        
        response = client.get("/analytics/carrier-performance")
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"] == []

    def test_carrier_performance_service_error(self, client, mock_service):
        """Test carrier performance handles errors."""
        mock_service.list_shipments.return_value = {
            "status": "error",
            "message": "Connection failed",
        }
        
        response = client.get("/analytics/carrier-performance")
        
        assert response.status_code == 500

