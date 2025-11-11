"""
Unit tests for bulk_aggregation.py - Aggregation helpers.

These tests mock database calls to verify aggregation
functions work correctly.
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.mcp_server.tools.bulk_aggregation import aggregate_results


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
