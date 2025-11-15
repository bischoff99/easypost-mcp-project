from __future__ import annotations

import pytest

from tests.factories import EasyPostFactory


@pytest.mark.asyncio
async def test_get_rates_returns_service_payload(async_client, mock_easypost_service):
    expected = EasyPostFactory.rates()
    mock_easypost_service.get_rates.return_value = expected

    request = EasyPostFactory.shipment_request()
    payload = {
        "to_address": request["to_address"],
        "from_address": request["from_address"],
        "parcel": request["parcel"],
    }

    response = await async_client.post("/api/rates", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["data"] == expected["data"]
    mock_easypost_service.get_rates.assert_awaited_once()
    kwargs = mock_easypost_service.get_rates.await_args.kwargs
    assert kwargs["to_address"]["name"] == payload["to_address"]["name"]
    assert kwargs["from_address"]["name"] == payload["from_address"]["name"]


@pytest.mark.asyncio
async def test_create_shipment_returns_transformed_response(async_client, mock_easypost_service):
    mock_easypost_service.create_shipment.return_value = {
        "status": "success",
        "id": "shp_123",
        "tracking_code": "trk_123",
    }

    request = EasyPostFactory.shipment_request()
    response = await async_client.post("/api/shipments", json=request)

    body = response.json()
    assert response.status_code == 200
    assert body["shipment_id"] == "shp_123"
    assert body["tracking_number"] == "trk_123"
    mock_easypost_service.create_shipment.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_shipment_handles_service_failure(async_client, mock_easypost_service):
    mock_easypost_service.create_shipment.side_effect = Exception("boom")

    response = await async_client.post("/api/shipments", json=EasyPostFactory.shipment_request())

    assert response.status_code == 500
    assert "Error creating shipment" in response.json()["detail"]


@pytest.mark.asyncio
async def test_buy_shipment_flow(async_client, mock_easypost_service):
    mock_easypost_service.get_rates.return_value = {"status": "success", "data": [{}]}
    mock_easypost_service.create_shipment.return_value = {
        "status": "success",
        "id": "shp_123",
    }
    buy_payload = {"status": "success", "label_url": "http://label"}
    mock_easypost_service.buy_shipment.return_value = buy_payload

    request = EasyPostFactory.shipment_request()
    request.update({"rate_id": "rate_123"})

    response = await async_client.post("/api/shipments/buy", json=request)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["label_url"] == "http://label"
    mock_easypost_service.buy_shipment.assert_awaited_once()
    buy_kwargs = mock_easypost_service.buy_shipment.await_args.kwargs
    assert buy_kwargs == {"shipment_id": "shp_123", "rate_id": "rate_123"}


@pytest.mark.asyncio
async def test_list_shipments_forwards_args(async_client, mock_easypost_service):
    mock_easypost_service.list_shipments.return_value = EasyPostFactory.shipment_list()

    response = await async_client.get("/api/shipments", params={"page_size": 5, "before_id": "shp_2"})

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_easypost_service.list_shipments.assert_awaited_once_with(page_size=5, before_id="shp_2")


@pytest.mark.asyncio
async def test_get_shipment_detail_returns_404_when_missing(async_client, mock_easypost_service):
    mock_easypost_service.retrieve_shipment.return_value = {
        "status": "error",
        "message": "Shipment not found",
    }

    response = await async_client.get("/api/shipments/shp_missing")

    assert response.status_code == 404
    assert response.json()["detail"] == "Shipment not found"
