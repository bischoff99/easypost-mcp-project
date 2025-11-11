"""
Unit tests for bulk_aggregation.py - Aggregation helpers.

These tests mock database calls to verify aggregation
functions work correctly.
"""

import pytest
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

from src.mcp_server.tools.bulk_aggregation import aggregate_results, setup_database_tracking


@pytest.fixture
def sample_results():
    """Sample shipment results for testing."""
    return [
        {
            "line": 1,
            "status": "success",
            "shipment_id": "shp_1",
            "carrier": "USPS",
            "cost": "10.00",
        },
        {
            "line": 2,
            "status": "success",
            "shipment_id": "shp_2",
            "carrier": "FEDEX",
            "cost": "15.00",
        },
        {
            "line": 3,
            "status": "error",
            "error": "Invalid address",
        },
        {
            "line": 4,
            "status": "success",
            "shipment_id": "shp_4",
            "carrier": "USPS",
            "cost": "12.00",
        },
    ]


class TestAggregateResults:
    """Tests for aggregate_results()."""

    def test_aggregates_successful_and_failed(self, sample_results):
        """Test aggregates successful and failed shipments."""
        start_time = datetime.now(UTC)
        end_time = datetime.now(UTC)

        aggregated = aggregate_results(sample_results, start_time, end_time)

        assert len(aggregated["successful"]) == 3
        assert len(aggregated["failed"]) == 1
        assert aggregated["total_cost"] == 37.00

    def test_calculates_carrier_stats(self, sample_results):
        """Test calculates carrier breakdown statistics."""
        start_time = datetime.now(UTC)
        end_time = datetime.now(UTC)

        aggregated = aggregate_results(sample_results, start_time, end_time)
        carrier_stats = aggregated["carrier_stats"]

        assert "USPS" in carrier_stats
        assert carrier_stats["USPS"]["count"] == 2
        assert carrier_stats["USPS"]["cost"] == 22.00

        assert "FEDEX" in carrier_stats
        assert carrier_stats["FEDEX"]["count"] == 1
        assert carrier_stats["FEDEX"]["cost"] == 15.00

    def test_handles_empty_results(self):
        """Test handles empty results gracefully."""
        start_time = datetime.now(UTC)
        end_time = datetime.now(UTC)

        aggregated = aggregate_results([], start_time, end_time)

        assert len(aggregated["successful"]) == 0
        assert len(aggregated["failed"]) == 0
        assert aggregated["total_cost"] == 0.0

    def test_calculates_duration(self):
        """Test calculates processing duration."""
        start_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        end_time = datetime(2024, 1, 1, 12, 0, 5, tzinfo=UTC)

        aggregated = aggregate_results([], start_time, end_time)

        assert aggregated["duration"] == 5.0


class TestSetupDatabaseTracking:
    """Tests for setup_database_tracking()."""

    @pytest.mark.asyncio
    async def test_creates_batch_operation(self):
        """Test creates batch operation when db_service available."""
        mock_db_service = MagicMock()
        mock_batch = MagicMock()
        mock_batch.batch_id = "bulk_123"
        mock_db_service.create_batch_operation = AsyncMock(return_value=mock_batch)

        mock_ctx = AsyncMock()
        mock_ctx.info = AsyncMock()

        start_time = datetime.now(UTC)

        batch_op, batch_id = await setup_database_tracking(
            mock_db_service, start_time, mock_ctx
        )

        assert batch_op == mock_batch
        assert batch_id == "bulk_123"
        mock_db_service.create_batch_operation.assert_called_once()

    @pytest.mark.asyncio
    async def test_returns_none_when_no_db_service(self):
        """Test returns None when db_service is None."""
        start_time = datetime.now(UTC)

        batch_op, batch_id = await setup_database_tracking(None, start_time, None)

        assert batch_op is None
        assert batch_id is None

    @pytest.mark.asyncio
    async def test_handles_db_error_gracefully(self):
        """Test handles database errors gracefully."""
        mock_db_service = MagicMock()
        mock_db_service.create_batch_operation = AsyncMock(
            side_effect=Exception("DB Error")
        )

        mock_ctx = AsyncMock()
        mock_ctx.info = AsyncMock()

        start_time = datetime.now(UTC)

        batch_op, batch_id = await setup_database_tracking(
            mock_db_service, start_time, mock_ctx
        )

        assert batch_op is None
        assert batch_id is None
