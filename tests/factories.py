"""Test data factories for EasyPost MCP tests."""

from datetime import UTC, datetime
from typing import Any


class EasyPostFactory:
    """Factory for creating EasyPost API response fixtures."""

    @staticmethod
    def shipment(
        id: str = "shp_test123",  # noqa: A002 - Test factory, not shadowing in practice
        tracking_code: str = "9400111899223345",
        status: str = "delivered",
        **kwargs,
    ) -> dict[str, Any]:
        """Create a mock shipment response."""
        base = {
            "status": "success",
            "id": id,
            "tracking_code": tracking_code,
            "shipment_status": status,
            "postage_label_url": f"https://example.com/labels/{id}.png",
            "selected_rate": {
                "carrier": "USPS",
                "service": "First",
                "rate": 5.50,
                "currency": "USD",
            },
            "created_at": datetime.now(UTC).isoformat(),
        }
        base.update(kwargs)
        return base

    @staticmethod
    def rates(rates: list[dict] = None) -> dict[str, Any]:
        """Create a mock rates response.

        Returns format expected by RatesResponse model: {"status": "success", "data": [...]}
        """
        default_rates = [
            {
                "carrier": "USPS",
                "service": "First",
                "rate": 5.50,
                "delivery_days": 2,
                "currency": "USD",
            },
            {
                "carrier": "USPS",
                "service": "Priority",
                "rate": 7.25,
                "delivery_days": 1,
                "currency": "USD",
            },
        ]
        return {
            "status": "success",
            "data": rates if rates is not None else default_rates,
        }

    @staticmethod
    def tracking(
        tracking_code: str = "9400111899223345", status: str = "delivered", **kwargs
    ) -> dict[str, Any]:
        """Create a mock tracking response.

        Matches format returned by EasyPostService.get_tracking()
        """
        base = {
            "status": "success",
            "data": {
                "tracking_number": tracking_code,  # Service uses tracking_number, not tracking_code
                "status_detail": status,  # Service uses status_detail
                "status": status,  # Keep for backward compatibility
                "tracking_details": [
                    {
                        "message": "Delivered",
                        "status": "delivered",
                        "datetime": "2025-01-01T10:00:00Z",
                        "location": "New York, NY",
                    }
                ],
                "est_delivery_date": "2025-01-02T12:00:00Z",
            },
        }
        base.update(kwargs)
        return base

    @staticmethod
    def shipment_list(shipments: list[dict] = None) -> dict[str, Any]:
        """Create a mock shipments list response."""
        default_shipments = [
            {
                "id": "shp_1",
                "status": "delivered",
                "tracking_code": "9400111899223345",
                "carrier": "USPS",
                "selected_rate": {"rate": 5.50, "carrier": "USPS"},
            },
            {
                "id": "shp_2",
                "status": "in_transit",
                "tracking_code": "9400111899223346",
                "carrier": "FedEx",
                "selected_rate": {"rate": 12.00, "carrier": "FedEx"},
            },
        ]
        return {
            "status": "success",
            "data": shipments if shipments is not None else default_shipments,
        }

    @staticmethod
    def error(message: str = "API Error", status_code: int = 500) -> dict[str, Any]:
        """Create a mock error response."""
        return {
            "status": "error",
            "message": message,
            "code": status_code,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    @staticmethod
    def address(
        name: str = "John Doe",
        street1: str = "123 Main St",
        city: str = "Anytown",
        state: str = "CA",
        zip: str = "12345",  # noqa: A002 - Test factory, matches EasyPost API field name
        country: str = "US",
        **kwargs,
    ) -> dict[str, str]:
        """Create a mock address."""
        base = {
            "name": name,
            "street1": street1,
            "city": city,
            "state": state,
            "zip": zip,
            "country": country,
        }
        base.update(kwargs)
        return base

    @staticmethod
    def parcel(
        length: float = 12.0,
        width: float = 12.0,
        height: float = 6.0,
        weight: float = 2.0,
        **kwargs,
    ) -> dict[str, float]:
        """Create a mock parcel."""
        base = {"length": length, "width": width, "height": height, "weight": weight}
        base.update(kwargs)
        return base

    @staticmethod
    def shipment_request(**kwargs) -> dict[str, Any]:
        """Create a complete shipment request."""
        base = {
            "to_address": EasyPostFactory.address(),
            "from_address": EasyPostFactory.address(
                name="Warehouse", street1="456 Industrial Blvd", city="Los Angeles", zip="90210"
            ),
            "parcel": EasyPostFactory.parcel(),
            "carrier": "USPS",
            "service": "First",
        }
        base.update(kwargs)
        return base
