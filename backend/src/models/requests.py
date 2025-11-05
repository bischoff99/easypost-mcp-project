"""Request models for FastAPI endpoints."""

from pydantic import BaseModel

from src.services.easypost_service import AddressModel, ParcelModel


class ShipmentRequest(BaseModel):
    """Request model for creating shipments."""

    to_address: AddressModel
    from_address: AddressModel
    parcel: ParcelModel
    carrier: str = "USPS"
    service: str | None = None  # Specific service (e.g., "FEDEX_GROUND", "Priority")


class RatesRequest(BaseModel):
    """Request model for getting shipping rates."""

    to_address: AddressModel
    from_address: AddressModel
    parcel: ParcelModel


class BuyShipmentRequest(BaseModel):
    """Request model for buying a shipment with selected rate."""

    from_address: AddressModel
    to_address: AddressModel
    parcel: ParcelModel
    rate_id: str


class BulkShipmentsRequest(BaseModel):
    """Request model for creating shipments in bulk."""

    shipments: list[ShipmentRequest]
