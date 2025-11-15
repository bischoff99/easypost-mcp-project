from __future__ import annotations

import pytest

from tests.factories import EasyPostFactory


@pytest.mark.asyncio
async def test_track_shipment_returns_payload(async_client, mock_easypost_service):
    mock_easypost_service.get_tracking.return_value = EasyPostFactory.tracking()

    response = await async_client.get("/api/tracking/9400111899223345")

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["tracking_number"] == "9400111899223345"
    mock_easypost_service.get_tracking.assert_awaited_once_with(tracking_number="9400111899223345")


@pytest.mark.asyncio
async def test_track_shipment_handles_failure(async_client, mock_easypost_service):
    mock_easypost_service.get_tracking.side_effect = Exception("downstream failure")

    response = await async_client.get("/api/tracking/9400")

    assert response.status_code == 500
    assert "Error tracking shipment" in response.json()["detail"]
