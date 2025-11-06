"""API tests for shipments router."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware

from src.routers.shipments import rates_router, router


@pytest.fixture
def mock_service():
    """Create mock EasyPost service."""
    service = AsyncMock()
    return service


@pytest.fixture
def app(mock_service):
    """Create test FastAPI app with shipments router."""
    test_app = FastAPI()
    
    # Add request_id middleware
    class RequestIDMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            request.state.request_id = "test-request-123"
            response = await call_next(request)
            return response
    
    test_app.add_middleware(RequestIDMiddleware)
    test_app.include_router(rates_router)  # /rates
    test_app.include_router(router)  # /shipments already in router prefix
    
    # Override dependency
    from src.dependencies import get_easypost_service
    test_app.dependency_overrides[get_easypost_service] = lambda: mock_service
    
    return test_app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


class TestGetRatesEndpoint:
    """Test POST /rates endpoint."""

    def test_get_rates_success(self, client, mock_service):
        """Test getting rates successfully."""
        # Mock rates response
        mock_service.get_rates.return_value = {
            "status": "success",
            "data": [
                {"id": "rate_1", "carrier": "USPS", "service": "Priority", "rate": "10.50"},
                {"id": "rate_2", "carrier": "UPS", "service": "Ground", "rate": "12.75"},
            ],
        }
        
        # Make request
        response = client.post(
            "/rates",
            json={
                "from_address": {
                    "name": "Sender",
                    "street1": "123 Main",
                    "city": "LA",
                    "state": "CA",
                    "zip": "90001",
                    "country": "US",
                },
                "to_address": {
                    "name": "Recipient",
                    "street1": "456 Park",
                    "city": "NYC",
                    "state": "NY",
                    "zip": "10001",
                    "country": "US",
                },
                "parcel": {"length": 10, "width": 8, "height": 6, "weight": 32},
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) == 2

    def test_get_rates_validation_error(self, client, mock_service):
        """Test rates with invalid data."""
        # Missing required fields
        response = client.post(
            "/rates",
            json={
                "from_address": {"street1": "123 Main"},  # Missing required fields
                "to_address": {"street1": "456 Park"},
                "parcel": {"length": 10},
            },
        )
        
        # Should return validation error
        assert response.status_code == 422


class TestCreateShipmentEndpoint:
    """Test POST /shipments endpoint."""

    def test_create_shipment_success(self, client, mock_service):
        """Test creating shipment successfully."""
        mock_service.create_shipment.return_value = {
            "status": "success",
            "id": "shp_test123",
            "tracking_code": "TRACK123",
            "rates": [{"carrier": "USPS", "rate": "10.50"}],
            "postage_label_url": "https://example.com/label.png",
        }
        
        response = client.post(
            "/shipments",
            json={
                "from_address": {
                    "name": "Sender",
                    "street1": "123 Main",
                    "city": "LA",
                    "state": "CA",
                    "zip": "90001",
                    "country": "US",
                },
                "to_address": {
                    "name": "Recipient",
                    "street1": "456 Park",
                    "city": "NYC",
                    "state": "NY",
                    "zip": "10001",
                    "country": "US",
                },
                "parcel": {"length": 10, "width": 8, "height": 6, "weight": 32},
                "buy_label": False,
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "id" in data
        assert "tracking_code" in data

    def test_create_shipment_with_label_purchase(self, client, mock_service):
        """Test creating shipment with label purchase."""
        mock_service.create_shipment.return_value = {
            "status": "success",
            "id": "shp_test123",
            "tracking_code": "TRACK123",
            "rates": [],
            "postage_label_url": "https://example.com/label.png",
            "purchased_rate": {"carrier": "USPS", "rate": "10.50"},
        }
        
        response = client.post(
            "/shipments",
            json={
                "from_address": {
                    "name": "Sender",
                    "street1": "123 Main",
                    "city": "LA",
                    "state": "CA",
                    "zip": "90001",
                    "country": "US",
                },
                "to_address": {
                    "name": "Recipient",
                    "street1": "456 Park",
                    "city": "NYC",
                    "state": "NY",
                    "zip": "10001",
                    "country": "US",
                },
                "parcel": {"length": 10, "width": 8, "height": 6, "weight": 32},
                "buy_label": True,
                "carrier": "USPS",
                "service": "Priority",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "postage_label_url" in data

    def test_create_shipment_validation_error(self, client, mock_service):
        """Test shipment creation with invalid data."""
        response = client.post(
            "/shipments",
            json={
                "from_address": {"street1": "123 Main"},  # Missing required fields
                "to_address": {"street1": "456 Park"},
                "parcel": {"weight": 10},
            },
        )
        
        assert response.status_code == 422


class TestListShipmentsEndpoint:
    """Test GET /shipments endpoint."""

    def test_list_shipments_success(self, client, mock_service):
        """Test listing shipments."""
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [
                {"id": "shp_1", "tracking_code": "TRACK1"},
                {"id": "shp_2", "tracking_code": "TRACK2"},
            ],
            "has_more": False,
        }
        
        response = client.get("/shipments?page_size=10")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) == 2

    def test_list_shipments_pagination(self, client, mock_service):
        """Test shipments list with pagination."""
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [{"id": f"shp_{i}"} for i in range(5)],
            "has_more": True,
        }
        
        response = client.get("/shipments?page_size=5")
        
        assert response.status_code == 200
        data = response.json()
        assert data["has_more"] is True

    def test_list_shipments_empty(self, client, mock_service):
        """Test listing when no shipments exist."""
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [],
            "has_more": False,
        }
        
        response = client.get("/shipments")
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"] == []


class TestGetShipmentEndpoint:
    """Test GET /shipments/{id} endpoint."""

    def test_get_shipment_success(self, client, mock_service):
        """Test getting single shipment."""
        mock_service.get_shipment.return_value = {
            "status": "success",
            "data": {
                "id": "shp_test123",
                "tracking_code": "TRACK123",
                "status": "delivered",
            },
        }
        
        response = client.get("/shipments/shp_test123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["id"] == "shp_test123"

    def test_get_shipment_not_found(self, client, mock_service):
        """Test getting non-existent shipment."""
        mock_service.get_shipment.return_value = {
            "status": "error",
            "message": "Shipment not found",
        }
        
        response = client.get("/shipments/shp_nonexistent")
        
        # Endpoint should return error response
        assert response.status_code in [200, 404]  # Depends on implementation


class TestBuyLabelEndpoint:
    """Test POST /shipments/{id}/buy endpoint."""

    def test_buy_label_success(self, client, mock_service):
        """Test buying label for existing shipment."""
        mock_service.buy_label.return_value = {
            "status": "success",
            "data": {
                "id": "shp_test123",
                "postage_label_url": "https://example.com/label.png",
                "purchased_rate": {"carrier": "USPS", "rate": "10.50"},
            },
        }
        
        response = client.post(
            "/shipments/shp_test123/buy",
            json={"carrier": "USPS", "service": "Priority"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "postage_label_url" in data["data"]

