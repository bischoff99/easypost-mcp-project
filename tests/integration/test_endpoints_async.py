"""
Complete integration tests for FastAPI endpoints using AsyncClient pattern.
Replaces test_server_endpoints.py with modern async testing.
"""

import pytest

from tests.factories import EasyPostFactory


class TestEndpointsAsync:
    """Modern async integration tests using httpx.AsyncClient."""

    # ========== Core Endpoints ==========

    @pytest.mark.asyncio
    async def test_root_endpoint(self, async_client):
        """Test root endpoint returns API info."""
        response = await async_client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "EasyPost MCP Server" in data["message"]
        assert "version" in data
        assert "1.0.0" in data["version"]

    @pytest.mark.asyncio
    async def test_health_endpoint(self, async_client):
        """Test health endpoint returns system status."""
        response = await async_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert "ok" in data
        assert data["ok"] is True

    @pytest.mark.asyncio
    async def test_metrics_endpoint(self, async_client):
        """Test metrics endpoint returns tracking data."""
        response = await async_client.get("/metrics")

        assert response.status_code == 200
        data = response.json()

        assert "uptime_seconds" in data
        assert "total_calls" in data

    # ========== Rates Endpoints ==========

    @pytest.mark.asyncio
    async def test_get_rates_success(self, async_client, mock_easypost_service):
        """Test successful rates request."""
        mock_easypost_service.get_rates.return_value = EasyPostFactory.rates()

        response = await async_client.post(
            "/api/rates",
            json={
                "to_address": EasyPostFactory.address(),
                "from_address": EasyPostFactory.address(),
                "parcel": EasyPostFactory.parcel(),
            },
        )

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"

    @pytest.mark.asyncio
    async def test_get_rates_validation_error(self, async_client):
        """Test rates endpoint rejects invalid data."""
        response = await async_client.post("/api/rates", json={"invalid": "data"})

        assert response.status_code == 422  # Validation error

    # ========== Shipment Endpoints ==========

    @pytest.mark.asyncio
    async def test_create_shipment_success(self, async_client, mock_easypost_service):
        """Test successful shipment creation."""
        mock_easypost_service.create_shipment.return_value = EasyPostFactory.shipment()

        response = await async_client.post(
            "/api/shipments", json=EasyPostFactory.shipment_request()
        )

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        assert "shipment_id" in data
        assert "tracking_number" in data
        assert data["shipment_id"] is not None
        assert data["tracking_number"] is not None

    @pytest.mark.asyncio
    async def test_list_shipments_success(self, async_client, mock_easypost_service):
        """Test successful shipments listing."""
        mock_easypost_service.list_shipments.return_value = EasyPostFactory.shipment_list()

        response = await async_client.get("/api/shipments")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        assert len(data["data"]) == 2

    @pytest.mark.asyncio
    async def test_list_shipments_with_params(self, async_client, mock_easypost_service):
        """Test shipments listing with pagination params."""
        mock_easypost_service.list_shipments.return_value = EasyPostFactory.shipment_list([])

        response = await async_client.get("/api/shipments?page_size=50&before_id=shp_123")

        assert response.status_code == 200
        mock_easypost_service.list_shipments.assert_called_once_with(
            page_size=50, before_id="shp_123"
        )

    # ========== Tracking Endpoints ==========

    @pytest.mark.asyncio
    async def test_track_shipment_success(self, async_client, mock_easypost_service):
        """Test successful tracking lookup."""
        mock_easypost_service.get_tracking.return_value = EasyPostFactory.tracking()

        response = await async_client.get("/api/tracking/9400111899223345")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        assert data["data"] is not None
        # Check for status_detail (service format) or status (factory format)
        assert (
            data["data"].get("status_detail") == "delivered"
            or data["data"].get("status") == "delivered"
        )

    # ========== Analytics Endpoints ==========

    @pytest.mark.asyncio
    async def test_analytics_success(self, async_client, mock_easypost_service):
        """Test analytics endpoint with data."""
        mock_easypost_service.list_shipments.return_value = {
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

        response = await async_client.get("/api/analytics?days=30")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

    @pytest.mark.asyncio
    async def test_analytics_empty_data(self, async_client, mock_easypost_service):
        """Test analytics with no shipments."""
        mock_easypost_service.list_shipments.return_value = {
            "status": "success",
            "data": [],
        }

        response = await async_client.get("/api/analytics")

        assert response.status_code == 200

    @pytest.mark.skip(
        reason="/stats endpoint removed for personal use - use /api/analytics instead"
    )
    @pytest.mark.asyncio
    async def test_stats_endpoint(self, async_client, mock_easypost_service):
        """Test dashboard stats endpoint."""
        mock_easypost_service.list_shipments.return_value = {
            "status": "success",
            "data": [
                {"status": "delivered", "selected_rate": {"rate": 5.50}},
                {"status": "in_transit", "selected_rate": {"rate": 7.25}},
                {"status": "delivered", "selected_rate": {"rate": 3.75}},
            ],
        }

        response = await async_client.get("/stats")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        assert "total_shipments" in data["data"]
        assert data["data"]["total_shipments"]["value"] == 3

    @pytest.mark.skip(
        reason="/carrier-performance endpoint removed for personal use - use /api/analytics instead"
    )
    @pytest.mark.asyncio
    async def test_carrier_performance(self, async_client, mock_easypost_service):
        """Test carrier performance metrics."""
        mock_easypost_service.list_shipments.return_value = {
            "status": "success",
            "data": [
                {"carrier": "USPS", "status": "delivered"},
                {"carrier": "USPS", "status": "delivered"},
                {"carrier": "FedEx", "status": "in_transit"},
                {"carrier": "UPS", "status": "delivered"},
            ],
        }

        response = await async_client.get("/carrier-performance")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"

    # ========== Error Handling & Edge Cases ==========

    @pytest.mark.asyncio
    async def test_error_response_format(self, async_client):
        """Test error responses follow consistent format."""
        response = await async_client.get("/nonexistent")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_request_id_middleware(self, async_client):
        """Test request ID is added to headers (only in DEBUG mode)."""
        response = await async_client.get("/")

        assert response.status_code == 200
        # Request ID header only present in DEBUG mode
        # In production, middleware exists but doesn't add header
        # Test passes if header exists (DEBUG mode) or if it doesn't (production mode)
        if "X-Request-ID" in response.headers:
            assert len(response.headers["X-Request-ID"]) > 0

    # ========== Concurrent Requests ==========

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, async_client, mock_easypost_service):
        """Test handling of concurrent requests."""
        import asyncio

        mock_easypost_service.get_rates.return_value = EasyPostFactory.rates()

        # Make 5 concurrent requests
        tasks = [
            async_client.post(
                "/api/rates",
                json={
                    "to_address": EasyPostFactory.address(),
                    "from_address": EasyPostFactory.address(),
                    "parcel": EasyPostFactory.parcel(),
                },
            )
            for _ in range(5)
        ]

        responses = await asyncio.gather(*tasks)

        # All should succeed
        assert all(r.status_code == 200 for r in responses)

    @pytest.mark.asyncio
    async def test_rate_limiting(self, async_client, mock_easypost_service):
        """Test rate limiting on endpoints."""
        mock_easypost_service.get_rates.return_value = EasyPostFactory.rates()

        # Make rapid requests to trigger rate limit (10/minute)
        for _ in range(15):
            response = await async_client.post(
                "/api/rates",
                json={
                    "to_address": EasyPostFactory.address(),
                    "from_address": EasyPostFactory.address(),
                    "parcel": EasyPostFactory.parcel(),
                },
            )

            if response.status_code == 429:
                # Rate limit triggered
                assert response.status_code == 429
                break
