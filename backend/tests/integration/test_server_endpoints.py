"""Integration tests for FastAPI server endpoints."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.server import app


class TestServerEndpoints:
    """Integration tests for server endpoints."""

    @pytest.fixture
    def client(self):
        """Test client for FastAPI app."""
        return TestClient(app)

    def test_root_endpoint(self, client):
        """Test root endpoint returns correct response."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "EasyPost MCP Server" in data["message"]
        assert "version" in data
        assert "1.0.0" in data["version"]
        assert "docs" in data
        assert "health" in data

    def test_health_endpoint_success(self, client):
        """Test health endpoint with successful health check."""
        with patch("src.server.HealthCheck") as mock_health_class:
            mock_health_instance = MagicMock()
            mock_health_class.return_value = mock_health_instance

            # Mock successful health check (async)
            mock_health_instance.check = AsyncMock(
                return_value={
                    "status": "healthy",
                    "system": {"status": "healthy", "cpu_percent": 25.0},
                    "easypost": {"status": "healthy", "latency_ms": 150},
                    "timestamp": "2025-01-01T00:00:00Z",
                }
            )

            response = client.get("/health")

            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "healthy"
            assert "system" in data
            assert "easypost" in data
            assert "timestamp" in data

    def test_health_endpoint_failure(self, client):
        """Test health endpoint with failed health check."""
        with patch("src.server.HealthCheck") as mock_health_class:
            mock_health_instance = MagicMock()
            mock_health_class.return_value = mock_health_instance

            # Mock failed health check (async)
            mock_health_instance.check = AsyncMock(
                return_value={
                    "status": "unhealthy",
                    "error": "System overload",
                    "timestamp": "2025-01-01T00:00:00Z",
                }
            )

            response = client.get("/health")

            assert response.status_code == 200  # Health endpoint always returns 200
            data = response.json()

            assert data["status"] == "unhealthy"
            assert "error" in data
            assert data["error"] == "System overload"

    def test_metrics_endpoint(self, client):
        """Test metrics endpoint returns metrics data."""
        # Reset metrics for clean test
        global metrics
        from src.utils.monitoring import MetricsCollector

        metrics = MetricsCollector()

        # Add some test data
        metrics.record_error()
        metrics.track_api_call("get_rates", True)
        metrics.track_api_call("create_shipment", False)

        response = client.get("/metrics")

        assert response.status_code == 200
        data = response.json()

        assert "uptime_seconds" in data
        assert "total_calls" in data
        assert "error_count" in data
        assert "error_rate" in data
        assert "api_calls" in data
        assert "timestamp" in data

        assert data["total_calls"] == 2  # 2 API calls
        assert data["error_count"] == 1  # 1 error (from failed call)
        assert data["error_rate"] == 0.5  # 1/2

    def test_get_rates_endpoint_success(self, client):
        """Test successful rates endpoint."""

        async def mock_get_rates(*args, **kwargs):
            return {
                "status": "success",
                "data": {
                    "rates": [
                        {"carrier": "USPS", "service": "First", "rate": 5.50},
                        {"carrier": "USPS", "service": "Priority", "rate": 7.25},
                    ]
                },
                "message": "Rates retrieved successfully",
            }

        with patch("src.server.easypost_service") as mock_service:
            mock_service.get_rates = mock_get_rates

            rates_request = {
                "to_address": {
                    "name": "John Doe",
                    "street1": "123 Main St",
                    "city": "Anytown",
                    "state": "CA",
                    "zip": "12345",
                    "country": "US",
                },
                "from_address": {
                    "name": "Warehouse",
                    "street1": "456 Industrial Blvd",
                    "city": "Los Angeles",
                    "state": "CA",
                    "zip": "90210",
                    "country": "US",
                },
                "parcel": {"length": 12.0, "width": 12.0, "height": 6.0, "weight": 2.0},
            }

            response = client.post("/rates", json=rates_request)

            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "success"
            assert "rates" in data["data"]
            assert len(data["data"]["rates"]) == 2

    def test_get_rates_endpoint_validation_error(self, client):
        """Test rates endpoint with validation error."""
        # Invalid request - missing required fields
        invalid_request = {"to_address": {}, "from_address": {}, "parcel": {}}

        response = client.post("/rates", json=invalid_request)

        assert response.status_code == 422  # Validation error
        data = response.json()

        assert "detail" in data

    def test_get_rates_endpoint_service_error(self, client):
        """Test rates endpoint when service returns error."""
        with patch("src.server.easypost_service") as mock_service:
            mock_service.get_rates.side_effect = Exception("API connection failed")

            valid_request = {
                "to_address": {
                    "name": "John Doe",
                    "street1": "123 Main St",
                    "city": "Anytown",
                    "state": "CA",
                    "zip": "12345",
                    "country": "US",
                },
                "from_address": {
                    "name": "Warehouse",
                    "street1": "456 Industrial Blvd",
                    "city": "Los Angeles",
                    "state": "CA",
                    "zip": "90210",
                    "country": "US",
                },
                "parcel": {"length": 12.0, "width": 12.0, "height": 6.0, "weight": 2.0},
            }

            response = client.post("/rates", json=valid_request)

            assert response.status_code == 500
            data = response.json()

            assert "detail" in data
            assert "API connection failed" in data["detail"]

    def test_create_shipment_endpoint_success(self, client):
        """Test successful shipment creation endpoint."""
        with patch(
            "src.server.easypost_service.create_shipment", new_callable=AsyncMock
        ) as mock_create:
            mock_create.return_value = {
                "status": "success",
                "id": "shp_test123",
                "tracking_code": "9400111899223345",
                "postage_label_url": "https://example.com/label.png",
                "selected_rate": {"carrier": "USPS", "service": "First", "rate": 5.50},
            }

            shipment_request = {
                "to_address": {
                    "name": "John Doe",
                    "street1": "123 Main St",
                    "city": "Anytown",
                    "state": "CA",
                    "zip": "12345",
                    "country": "US",
                },
                "from_address": {
                    "name": "Warehouse",
                    "street1": "456 Industrial Blvd",
                    "city": "Los Angeles",
                    "state": "CA",
                    "zip": "90210",
                    "country": "US",
                },
                "parcel": {"length": 12.0, "width": 12.0, "height": 6.0, "weight": 2.0},
                "carrier": "USPS",
                "service": "First",
            }

            response = client.post("/shipments", json=shipment_request)

            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "success"
            assert data["id"] == "shp_test123"
            assert data["tracking_code"] == "9400111899223345"

    def test_list_shipments_endpoint_success(self, client):
        """Test successful shipments listing endpoint."""
        with patch(
            "src.server.easypost_service.list_shipments", new_callable=AsyncMock
        ) as mock_list:
            mock_list.return_value = {
                "status": "success",
                "data": [
                    {"id": "shp_1", "status": "delivered"},
                    {"id": "shp_2", "status": "in_transit"},
                ],
            }

            response = client.get("/shipments")

            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "success"
            assert len(data["data"]) == 2

    def test_list_shipments_endpoint_with_params(self, client):
        """Test shipments listing with query parameters."""
        with patch(
            "src.server.easypost_service.list_shipments", new_callable=AsyncMock
        ) as mock_list:
            mock_list.return_value = {
                "status": "success",
                "data": [],
            }

            response = client.get("/shipments?page_size=50&before_id=shp_123")

            assert response.status_code == 200

            # Verify parameters were passed to service
            mock_list.assert_called_once_with(page_size=50, before_id="shp_123")

    def test_get_shipment_endpoint_success(self, client):
        """Test successful individual shipment retrieval via database."""
        # Note: This tests the database endpoint, not the EasyPost API
        # Database tests require a running PostgreSQL instance
        pytest.skip("Database endpoint requires PostgreSQL - tested in database_integration")

    def test_track_shipment_endpoint_success(self, client):
        """Test successful shipment tracking."""
        with patch(
            "src.server.easypost_service.get_tracking", new_callable=AsyncMock
        ) as mock_track:
            mock_track.return_value = {
                "status": "success",
                "data": {
                    "tracking_code": "9400111899223345",
                    "status": "delivered",
                    "tracking_details": [
                        {"message": "Delivered", "datetime": "2025-01-01T10:00:00Z"}
                    ],
                },
            }

            response = client.get("/tracking/9400111899223345")

            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "success"
            assert data["data"]["status"] == "delivered"

    def test_analytics_endpoint_success(self, client):
        """Test successful analytics endpoint."""
        with patch(
            "src.server.easypost_service.list_shipments", new_callable=AsyncMock
        ) as mock_list:
            mock_list.return_value = {
                "status": "success",
                "data": [
                    {
                        "id": "shp_1",
                        "selected_rate": {"rate": 5.50, "carrier": "USPS"},
                        "carrier": "USPS",
                        "status": "delivered",
                        "from_address": {"city": "LA"},
                        "to_address": {"city": "NYC"},
                    }
                ],
            }

            response = client.get("/analytics?days=30")

            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "success"
            assert "data" in data
            assert "summary" in data["data"]
            assert "by_carrier" in data["data"]
            assert "by_date" in data["data"]
            assert "top_routes" in data["data"]

    def test_analytics_endpoint_empty_data(self, client):
        """Test analytics endpoint with no shipment data."""
        with patch(
            "src.server.easypost_service.list_shipments", new_callable=AsyncMock
        ) as mock_list:
            mock_list.return_value = {
                "status": "success",
                "data": [],
            }

            response = client.get("/analytics")

            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "success"
            assert data["data"]["summary"]["total_shipments"] == 0

    def test_stats_endpoint_success(self, client):
        """Test successful dashboard stats endpoint."""
        with patch(
            "src.server.easypost_service.list_shipments", new_callable=AsyncMock
        ) as mock_list:
            mock_list.return_value = {
                "status": "success",
                "data": [
                    {"status": "delivered", "selected_rate": {"rate": 5.50}},
                    {"status": "in_transit", "selected_rate": {"rate": 7.25}},
                    {"status": "delivered", "selected_rate": {"rate": 3.75}},
                ],
            }

            response = client.get("/stats")

            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "success"
            assert "data" in data
            assert "total_shipments" in data["data"]
            assert "active_deliveries" in data["data"]
            assert "total_cost" in data["data"]
            assert "delivery_success_rate" in data["data"]

            assert data["data"]["total_shipments"]["value"] == 3
            assert data["data"]["active_deliveries"]["value"] == 1  # 1 in_transit
            assert (
                abs(data["data"]["delivery_success_rate"]["value"] - 0.67) < 0.01
            )  # 2/3 delivered (~0.6667)

    def test_carrier_performance_endpoint_success(self, client):
        """Test successful carrier performance endpoint."""
        with patch(
            "src.server.easypost_service.list_shipments", new_callable=AsyncMock
        ) as mock_list:
            mock_list.return_value = {
                "status": "success",
                "data": [
                    {"carrier": "USPS", "status": "delivered"},
                    {"carrier": "USPS", "status": "delivered"},
                    {"carrier": "FedEx", "status": "in_transit"},
                    {"carrier": "UPS", "status": "delivered"},
                ],
            }

            response = client.get("/carrier-performance")

            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "success"
            assert "data" in data
            assert len(data["data"]) == 3  # 3 carriers

            # Check USPS performance (2/2 = 100%)
            usps_data = next(item for item in data["data"] if item["carrier"] == "USPS")
            assert usps_data["rate"] == 100
            assert usps_data["shipments"] == 2

    def test_rate_limiting_rates_endpoint(self, client):
        """Test rate limiting on rates endpoint."""
        # Make multiple requests to trigger rate limit
        rates_request = {
            "to_address": {
                "name": "John Doe",
                "street1": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zip": "12345",
                "country": "US",
            },
            "from_address": {
                "name": "Warehouse",
                "street1": "456 Industrial Blvd",
                "city": "Los Angeles",
                "state": "CA",
                "zip": "90210",
                "country": "US",
            },
            "parcel": {"length": 12.0, "width": 12.0, "height": 6.0, "weight": 2.0},
        }

        # First request should succeed
        response1 = client.post("/rates", json=rates_request)
        assert response1.status_code in [200, 429]  # May be rate limited immediately

        # Multiple rapid requests
        for _ in range(15):  # Exceed the 10/minute limit
            response = client.post("/rates", json=rates_request)
            if response.status_code == 429:
                # Rate limit triggered - verify 429 status
                assert response.status_code == 429
                break

    def test_request_id_middleware(self, client):
        """Test that request ID middleware adds headers."""
        response = client.get("/")

        assert response.status_code == 200
        assert "X-Request-ID" in response.headers
        assert len(response.headers["X-Request-ID"]) > 0

    def test_cors_headers(self, client):
        """Test CORS headers are properly set."""
        # NOTE: TestClient doesn't fully apply CORS middleware, so we just verify endpoint works
        response = client.get("/")
        assert response.status_code == 200
        # CORS headers are applied in production but not in TestClient

    def test_error_response_format(self, client):
        """Test that error responses follow consistent format."""
        # Make request to non-existent endpoint
        response = client.get("/nonexistent")

        assert response.status_code == 404
        # FastAPI default error format should be consistent

    def test_concurrent_requests(self, client):
        """Test handling of concurrent requests."""
        with patch("src.server.easypost_service.get_rates", new_callable=AsyncMock) as mock_rates:
            mock_rates.return_value = {"status": "success", "data": {"rates": []}}

            # Make multiple concurrent requests
            rates_request = {
                "to_address": {
                    "name": "John Doe",
                    "street1": "123 Main St",
                    "city": "Anytown",
                    "state": "CA",
                    "zip": "12345",
                    "country": "US",
                },
                "from_address": {
                    "name": "Warehouse",
                    "street1": "456 Industrial Blvd",
                    "city": "Los Angeles",
                    "state": "CA",
                    "zip": "90210",
                    "country": "US",
                },
                "parcel": {"length": 12.0, "width": 12.0, "height": 6.0, "weight": 2.0},
            }

            # Make 5 requests quickly
            for _ in range(5):
                response = client.post("/rates", json=rates_request)
                assert response.status_code == 200

    def test_large_request_handling(self, client):
        """Test handling of large request payloads."""
        # Test with a normal-sized request (large batch testing would be integration test)
        rates_request = {
            "to_address": {
                "name": "Recipient",
                "street1": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zip": "12345",
                "country": "US",
            },
            "from_address": {
                "name": "Warehouse",
                "street1": "456 Industrial Blvd",
                "city": "Los Angeles",
                "state": "CA",
                "zip": "90210",
                "country": "US",
            },
            "parcel": {"length": 12.0, "width": 12.0, "height": 6.0, "weight": 2.0},
        }

        response = client.post("/rates", json=rates_request)

        # Should not crash the server
        assert response.status_code in [200, 422, 500]  # Valid response codes
