"""Integration tests for database-backed server endpoints.

NOTE: Database-backed endpoints (/db/*) were removed for personal use.
These tests are skipped as the endpoints no longer exist.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient


@pytest.mark.skip(reason="Database-backed endpoints (/db/*) removed for personal use")
class TestDatabaseBackedEndpoints:
    """Test database-backed API endpoints."""

    def test_get_shipments_db_empty(self, client: TestClient):
        """Test getting shipments from empty database."""
        with (
            patch("src.server.get_db") as mock_get_db,
            patch("src.server.DatabaseService") as mock_db_service_class,
        ):
            # Mock empty database - async generator pattern
            mock_session = MagicMock()

            async def mock_db_generator():
                yield mock_session

            mock_get_db.return_value = mock_db_generator()

            mock_db_service = MagicMock()
            mock_db_service_class.return_value = mock_db_service
            mock_db_service.get_shipments_with_details = AsyncMock(return_value=[])
            mock_db_service.get_shipments_count = AsyncMock(return_value=0)

            response = client.get("/db/shipments")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["data"]["shipments"] == []
            assert data["data"]["pagination"]["total"] == 0

    def test_get_shipments_db_with_data(self, client: TestClient):
        """Test getting shipments with data from database."""
        with (
            patch("src.server.get_db") as mock_get_db,
            patch("src.server.DatabaseService") as mock_db_service_class,
        ):
            # Mock database with data - async generator pattern
            mock_session = MagicMock()

            async def mock_db_generator():
                yield mock_session

            mock_get_db.return_value = mock_db_generator()

            mock_db_service = MagicMock()
            mock_db_service_class.return_value = mock_db_service

            # Mock shipment data
            mock_shipment = MagicMock()
            mock_shipment.to_dict.return_value = {
                "id": 1,
                "easypost_id": "sh_test_123",
                "status": "created",
                "carrier": "USPS",
                "total_cost": 10.50,
            }

            mock_db_service.get_shipments_with_details = AsyncMock(return_value=[mock_shipment])
            mock_db_service.get_shipments_count = AsyncMock(return_value=1)

            response = client.get("/db/shipments?limit=10&carrier=USPS")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert len(data["data"]["shipments"]) == 1
            assert data["data"]["shipments"][0]["carrier"] == "USPS"
            assert data["data"]["pagination"]["total"] == 1

    def test_get_shipment_by_id_found(self, client: TestClient):
        """Test getting specific shipment by ID."""
        with (
            patch("src.server.get_db") as mock_get_db,
            patch("src.server.DatabaseService") as mock_db_service_class,
        ):
            # Mock database - async generator pattern
            mock_session = MagicMock()

            async def mock_db_generator():
                yield mock_session

            mock_get_db.return_value = mock_db_generator()

            mock_db_service = MagicMock()
            mock_db_service_class.return_value = mock_db_service

            mock_shipment = MagicMock()
            mock_shipment.to_dict.return_value = {
                "id": 123,
                "easypost_id": "sh_test_123",
                "status": "delivered",
                "tracking_code": "9400111899223344",
            }

            mock_db_service.get_shipment_with_details = AsyncMock(return_value=mock_shipment)

            response = client.get("/db/shipments/123")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["data"]["id"] == 123
            assert data["data"]["status"] == "delivered"

    def test_get_shipment_by_id_not_found(self, client: TestClient):
        """Test getting shipment that doesn't exist."""
        with (
            patch("src.server.get_db") as mock_get_db,
            patch("src.server.DatabaseService") as mock_db_service_class,
        ):
            # Mock database - async generator pattern
            mock_session = MagicMock()

            async def mock_db_generator():
                yield mock_session

            mock_get_db.return_value = mock_db_generator()

            mock_db_service = MagicMock()
            mock_db_service_class.return_value = mock_db_service
            mock_db_service.get_shipment_with_details = AsyncMock(return_value=None)

            response = client.get("/db/shipments/999")

            assert response.status_code == 404
            data = response.json()
            assert "Shipment not found" in data["detail"]

    def test_get_addresses_db(self, client: TestClient):
        """Test getting address book from database."""
        with (
            patch("src.server.get_db") as mock_get_db,
            patch("src.server.DatabaseService") as mock_db_service_class,
        ):
            # Mock database - async generator pattern
            mock_session = MagicMock()

            async def mock_db_generator():
                yield mock_session

            mock_get_db.return_value = mock_db_generator()

            mock_db_service = MagicMock()
            mock_db_service_class.return_value = mock_db_service

            mock_address = MagicMock()
            mock_address.to_dict.return_value = {
                "id": 1,
                "name": "John Doe",
                "street1": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "country": "US",
                "usage_count": 5,
            }

            mock_db_service.get_addresses_with_stats = AsyncMock(return_value=[mock_address])
            mock_db_service.get_addresses_count = AsyncMock(return_value=1)

            response = client.get("/db/addresses?country=US&limit=25")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert len(data["data"]["addresses"]) == 1
            assert data["data"]["addresses"][0]["country"] == "US"
            assert data["data"]["addresses"][0]["usage_count"] == 5

    def test_get_analytics_dashboard_db(self, client: TestClient):
        """Test getting analytics dashboard from database."""
        with (
            patch("src.server.get_db") as mock_get_db,
            patch("src.server.DatabaseService") as mock_db_service_class,
        ):
            # Mock database - async generator pattern
            mock_session = MagicMock()

            async def mock_db_generator():
                yield mock_session

            mock_get_db.return_value = mock_db_generator()

            mock_db_service = MagicMock()
            mock_db_service_class.return_value = mock_db_service

            # Mock analytics data
            mock_db_service.get_analytics_summary = AsyncMock(
                return_value={
                    "total_shipments": 150,
                    "total_cost": 1250.75,
                    "average_cost": 8.34,
                    "date_range": {"start": "2025-10-01", "end": "2025-11-01"},
                }
            )

            mock_db_service.get_shipment_trends = AsyncMock(
                return_value=[
                    {"date": "2025-10-25", "count": 10, "cost": 85.50},
                    {"date": "2025-10-26", "count": 15, "cost": 120.25},
                ]
            )

            mock_db_service.get_top_routes = AsyncMock(
                return_value=[
                    {
                        "origin": "New York",
                        "destination": "Los Angeles",
                        "count": 25,
                        "cost": 200.00,
                    },
                    {"origin": "Chicago", "destination": "Miami", "count": 18, "cost": 150.00},
                ]
            )

            response = client.get("/db/analytics/dashboard?days=30")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["data"]["summary"]["total_shipments"] == 150
            assert len(data["data"]["shipment_trends"]) == 2
            assert len(data["data"]["top_routes"]) == 2

    def test_database_error_handling(self, client: TestClient):
        """Test that database errors are handled gracefully."""
        with patch("src.server.get_db") as mock_get_db:
            # Mock database connection failure - async generator that raises
            async def mock_db_generator_error():
                raise Exception("Database connection failed")
                yield  # unreachable but required for generator

            mock_get_db.return_value = mock_db_generator_error()

            response = client.get("/db/shipments")

            assert response.status_code == 500
            data = response.json()
            assert "Error retrieving shipments" in data["detail"]

    def test_pagination_metadata(self, client: TestClient):
        """Test that pagination metadata is correct."""
        with (
            patch("src.server.get_db") as mock_get_db,
            patch("src.server.DatabaseService") as mock_db_service_class,
        ):
            # Mock database - async generator pattern
            mock_session = MagicMock()

            async def mock_db_generator():
                yield mock_session

            mock_get_db.return_value = mock_db_generator()

            mock_db_service = MagicMock()
            mock_db_service_class.return_value = mock_db_service
            mock_db_service.get_shipments_with_details = AsyncMock(return_value=[])
            mock_db_service.get_shipments_count = AsyncMock(return_value=150)

            response = client.get("/db/shipments?limit=20&offset=40")

            assert response.status_code == 200
            data = response.json()
            pagination = data["data"]["pagination"]
            assert pagination["total"] == 150
            assert pagination["limit"] == 20
            assert pagination["offset"] == 40
            assert pagination["has_more"] is True  # 40 + 20 = 60 < 150

    def test_filtering_parameters(self, client: TestClient):
        """Test that filtering parameters are passed correctly."""
        with (
            patch("src.server.get_db") as mock_get_db,
            patch("src.server.DatabaseService") as mock_db_service_class,
        ):
            # Mock database - async generator pattern
            mock_session = MagicMock()

            async def mock_db_generator():
                yield mock_session

            mock_get_db.return_value = mock_db_generator()

            mock_db_service = MagicMock()
            mock_db_service_class.return_value = mock_db_service
            mock_db_service.get_shipments_with_details = AsyncMock(return_value=[])
            mock_db_service.get_shipments_count = AsyncMock(return_value=0)

            client.get(
                "/db/shipments?carrier=USPS&status=delivered&date_from=2025-01-01&date_to=2025-12-31"
            )

            # Verify filters were passed to service
            call_args = mock_db_service.get_shipments_with_details.call_args
            filters = call_args[1]["filters"]  # kwargs
            assert filters["carrier"] == "USPS"
            assert filters["status"] == "delivered"
            assert filters["date_from"] == "2025-01-01"
            assert filters["date_to"] == "2025-12-31"
