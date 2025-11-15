from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import asyncio
import pytest

from src.services.easypost_service import EasyPostService


@pytest.fixture
def service_with_client():
    with patch("src.services.easypost_service.easypost.EasyPostClient") as client_cls:
        client = MagicMock()
        client.shipment = MagicMock()
        client.customs_item = MagicMock()
        client.customs_info = MagicMock()
        client.address = MagicMock()
        client_cls.return_value = client
        service = EasyPostService("EZAK" + "0" * 24)
        yield service, client


def _simple_rate(rate_id: str = "rate_1") -> SimpleNamespace:
    return SimpleNamespace(
        id=rate_id,
        carrier="UPS",
        service="Ground",
        rate="10.00",
        delivery_days=3,
    )


def _address_dict(country: str = "US") -> dict[str, str]:
    return {
        "name": "Test",
        "street1": " 10 Downing St ",
        "city": "London",
        "state": "LN",
        "zip": "SW1A 2AA",
        "country": country,
    }


def _parcel_dict() -> dict[str, float]:
    return {"length": 10.0, "width": 5.0, "height": 4.0, "weight": 16.0}


def test_create_shipment_sync_returns_rates(service_with_client):
    service, client = service_with_client

    rate = _simple_rate()
    client.shipment.create.return_value = SimpleNamespace(id="shp_123")
    client.shipment.retrieve.return_value = SimpleNamespace(
        id="shp_123", tracking_code="trk_123", rates=[rate]
    )

    result = service._create_shipment_sync(
        _address_dict("uk"),
        _address_dict("US"),
        _parcel_dict(),
        carrier="UPS",
        service=None,
        buy_label=False,
    )

    assert result["status"] == "success"
    assert result["rates"] == [
        {
            "id": "rate_1",
            "carrier": "UPS",
            "service": "Ground",
            "rate": "10.00",
            "delivery_days": 3,
        }
    ]
    # Ensure normalization uppercases country before hitting EasyPost
    to_address = client.shipment.create.call_args[1]["to_address"]
    assert to_address["country"] == "UK"


def test_create_shipment_sync_requires_rate_when_buying(service_with_client):
    service, client = service_with_client

    rate = _simple_rate()
    client.shipment.create.return_value = SimpleNamespace(id="shp_123")
    client.shipment.retrieve.return_value = SimpleNamespace(
        id="shp_123", tracking_code="trk_123", rates=[rate]
    )

    result = service._create_shipment_sync(
        _address_dict(),
        _address_dict(),
        _parcel_dict(),
        carrier="UPS",
        service=None,
        buy_label=True,
        rate_id=None,
    )

    assert result["status"] == "error"
    assert "rate_id is required" in result["message"]


def test_buy_shipment_sync_success(service_with_client):
    service, client = service_with_client

    rate = _simple_rate()
    shipment = SimpleNamespace(
        id="shp_123",
        status="created",
        rates=[rate],
        to_address=SimpleNamespace(street1="10 Down", city="London", country="GB"),
        customs_info=None,
        duty_payment=None,
    )
    client.shipment.retrieve.return_value = shipment
    client.shipment.buy.return_value = SimpleNamespace(
        id="shp_123",
        tracking_code="trk_123",
        postage_label=SimpleNamespace(label_url="http://label"),
        selected_rate=SimpleNamespace(rate="10.00", carrier="UPS", service="Ground"),
    )

    result = service._buy_shipment_sync("shp_123", "rate_1")

    assert result["status"] == "success"
    assert result["data"]["purchased_rate"]["carrier"] == "UPS"
    client.shipment.buy.assert_called_once_with("shp_123", rate={"id": "rate_1"})


def test_buy_shipment_sync_missing_rate(service_with_client):
    service, client = service_with_client

    shipment = SimpleNamespace(
        id="shp_123",
        rates=[_simple_rate("other")],
        to_address=SimpleNamespace(street1="10 Down", city="London", country="GB"),
        customs_info=None,
        duty_payment=None,
    )
    client.shipment.retrieve.return_value = shipment

    result = service._buy_shipment_sync("shp_123", "rate_missing")

    assert result["status"] == "error"
    assert "Rate rate_missing not found" in result["message"]


def test_refund_shipment_sync_returns_payload(service_with_client):
    service, client = service_with_client

    client.shipment.retrieve.return_value = SimpleNamespace(
        id="shp_123",
        tracking_code="trk_123",
        selected_rate=SimpleNamespace(carrier="UPS", rate="10.00"),
    )
    client.shipment.refund.return_value = SimpleNamespace(refund_status="submitted")

    result = service._refund_shipment_sync("shp_123")

    assert result["status"] == "success"
    assert result["data"]["refund_status"] == "submitted"


def test_get_rates_sync_normalizes_addresses(service_with_client):
    service, client = service_with_client

    client.shipment.create.return_value = SimpleNamespace(rates=[_simple_rate()])

    result = service._get_rates_sync(_address_dict("gb"), _address_dict("US"), _parcel_dict())

    assert result[0]["carrier"] == "UPS"
    called_to = client.shipment.create.call_args[1]["to_address"]
    assert called_to["country"] == "GB"


def test_verify_address_sync_warning(service_with_client):
    service, client = service_with_client

    verified = SimpleNamespace(
        id="adr_1",
        street1="10 DOWNING",
        street2="",
        city="London",
        state="LN",
        zip="SW1A",
        country="GB",
        name="Test",
        company=None,
        phone=None,
        email=None,
        verifications={
            "delivery": {"success": False, "errors": ["Invalid"]},
            "carrier": {"success": True, "errors": []},
        },
    )
    client.address.create.return_value = verified

    result = service._verify_address_sync(_address_dict())

    assert result["status"] == "warning"
    assert result["data"]["verification_success"] is False
    assert result["data"]["errors"] == ["Invalid"]


@pytest.mark.asyncio
async def test_api_call_with_retry_handles_rate_limit(monkeypatch, service_with_client):
    service, _ = service_with_client

    class RateLimitError(Exception):
        http_status = 429

    attempts = {"count": 0}

    def flaky_call():
        if attempts["count"] == 0:
            attempts["count"] += 1
            raise RateLimitError()
        return "ok"

    async def immediate_sleep(_):
        return None

    monkeypatch.setattr("src.services.easypost_service.asyncio.sleep", immediate_sleep)

    result = await service._api_call_with_retry(flaky_call, max_retries=2)

    assert result == "ok"
    assert attempts["count"] == 1


@pytest.mark.asyncio
async def test_create_shipment_returns_error_when_sync_fails(service_with_client):
    service, _ = service_with_client

    service._create_shipment_sync = MagicMock(side_effect=RuntimeError("boom"))

    result = await service.create_shipment(
        _address_dict(),
        _address_dict(),
        _parcel_dict(),
    )

    assert result["status"] == "error"
    assert result["message"] == "Failed to create shipment"
