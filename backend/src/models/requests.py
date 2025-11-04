"""Request models for FastAPI endpoints."""

from pydantic import BaseModel

from src.services.easypost_service import AddressModel, ParcelModel


class ShipmentRequest(BaseModel):
    """Request model for creating shipments."""

    to_address: AddressModel
    from_address: AddressModel
    parcel: ParcelModel
    carrier: str = "USPS"


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
