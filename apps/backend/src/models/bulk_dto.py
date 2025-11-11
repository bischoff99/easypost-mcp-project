"""
DTOs (Data Transfer Objects) for bulk shipment operations.

These models separate data structures from business logic,
enabling pure functions and easier testing.
"""

from typing import Any

from pydantic import BaseModel, Field


class AddressDTO(BaseModel):
    """Address data transfer object."""

    name: str
    street1: str
    street2: str | None = None
    city: str
    state: str
    zip: str
    country: str
    phone: str | None = None
    email: str | None = None
    company: str | None = None


class ParcelDTO(BaseModel):
    """Parcel dimensions and weight."""

    length: float
    width: float
    height: float
    weight: float  # in ounces


class CustomsItemDTO(BaseModel):
    """Customs item information."""

    description: str
    quantity: int
    value: float
    weight: float
    hs_tariff_number: str | None = None
    origin_country: str | None = None


class CustomsInfoDTO(BaseModel):
    """Customs information for international shipments."""

    contents_type: str
    contents_explanation: str | None = None
    restriction_type: str | None = None
    restriction_comments: str | None = None
    customs_certify: bool = False
    customs_signer: str | None = None
    eel_pfc: str | None = None
    customs_items: list[CustomsItemDTO] = Field(default_factory=list)
    incoterm: str | None = None


class ShipmentDataDTO(BaseModel):
    """Parsed shipment data from spreadsheet."""

    recipient_name: str
    recipient_last_name: str
    street1: str
    street2: str | None = None
    city: str
    state: str
    zip: str
    country: str
    recipient_phone: str | None = None
    recipient_email: str | None = None
    contents: str
    dimensions: str
    weight: str
    origin_state: str | None = None
    sender_address: dict[str, Any] | None = None
    carrier_preference: str | None = None


class ValidationResultDTO(BaseModel):
    """Validation result for a shipment line."""

    line: int
    data: ShipmentDataDTO | None = None
    length: float | None = None
    width: float | None = None
    height: float | None = None
    weight_oz: float | None = None
    valid: bool
    errors: list[str] = Field(default_factory=list)


class VerifiedAddressDTO(BaseModel):
    """Verified address result."""

    address: AddressDTO
    verification_success: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ShipmentRequestDTO(BaseModel):
    """Complete shipment request ready for API call."""

    to_address: AddressDTO
    from_address: AddressDTO
    parcel: ParcelDTO
    customs_info: CustomsInfoDTO | None = None
    carrier: str | None = None
    reference: str | None = None


class ShipmentResultDTO(BaseModel):
    """Result from creating a shipment."""

    shipment_id: str | None = None
    rates: list[dict[str, Any]] = Field(default_factory=list)
    selected_rate: dict[str, Any] | None = None
    tracking_code: str | None = None
    label_url: str | None = None
    errors: list[str] = Field(default_factory=list)
    line_number: int
    warehouse_info: str | None = None
