"""Request models for FastAPI endpoints."""

from typing import Any

from pydantic import BaseModel

from src.services.easypost_service import AddressModel, ParcelModel


class CustomsItemModel(BaseModel):
    """Customs item model for international shipments."""

    description: str
    quantity: int = 1
    value: float
    hs_tariff_number: str | None = None
    origin_country: str = "US"


class CustomsInfoModel(BaseModel):
    """Customs info model for international shipments."""

    contents: list[CustomsItemModel]
    customs_certify: bool = True
    customs_signer: str = ""
    contents_type: str = "merchandise"
    restriction_type: str = "none"
    restriction_comments: str = ""
    eel_pfc: str = "NOEEI 30.37(a)"


class ShipmentRequest(BaseModel):
    """Request model for creating shipments."""

    to_address: AddressModel
    from_address: AddressModel
    parcel: ParcelModel
    carrier: str = "USPS"
    service: str | None = None  # Specific service (e.g., "FEDEX_GROUND", "Priority")
    customs_info: dict[str, Any] | None = None  # Customs info for international shipments


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
