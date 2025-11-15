from __future__ import annotations

from datetime import UTC, datetime

import pytest


@pytest.mark.asyncio
async def test_get_analytics_success(async_client, mock_easypost_service):
    shipments = [
        {
            "carrier": "UPS",
            "rate": "12.5",
            "status": "delivered",
            "created_at": datetime.now(UTC).isoformat(),
            "from_address": {"city": "London"},
            "to_address": {"city": "Paris"},
        },
        {
            "carrier": "USPS",
            "rate": "7.0",
            "status": "in_transit",
            "created_at": datetime.now(UTC).isoformat(),
            "from_address": {"city": "London"},
            "to_address": {"city": "Berlin"},
        },
    ]
    mock_easypost_service.list_shipments.return_value = {
        "status": "success",
        "data": shipments,
    }

    response = await async_client.get("/api/analytics", params={"days": 7})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["data"]["summary"]["total_shipments"] == 2
    mock_easypost_service.list_shipments.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_analytics_handles_service_error(async_client, mock_easypost_service):
    mock_easypost_service.list_shipments.return_value = {
        "status": "error",
        "message": "boom",
    }

    response = await async_client.get("/api/analytics")

    assert response.status_code == 500
    assert "Failed to fetch shipments" in response.json()["detail"]
