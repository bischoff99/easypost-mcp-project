"""Request models for FastAPI endpoints."""

from typing import Any, Self

from pydantic import BaseModel, model_validator

from src.services.easypost_service import AddressModel, ParcelModel


class CustomsItemModel(BaseModel):
    """Customs item model for international shipments."""

    description: str
    quantity: int = 1
    value: float
    hs_tariff_number: str | None = None
    origin_country: str = "US"

    @model_validator(mode="after")
    def validate_customs_item(self) -> Self:
        """
        Validate customs item data.

        Ensures:
        - Quantity is positive
        - Value is positive (required for customs)
        - Description is not empty
        """
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")

        if self.value <= 0:
            raise ValueError("value must be positive for customs declaration")

        if not self.description.strip():
            raise ValueError("description is required for customs")

        # Normalize country code to 2 letters uppercase
        if self.origin_country:
            self.origin_country = self.origin_country.strip().upper()
            if len(self.origin_country) not in [2, 3]:  # Allow 2 or 3 letter codes
                raise ValueError(
                    f"origin_country must be 2 or 3 letter ISO code, got: {self.origin_country}"
                )

        return self


class CustomsInfoModel(BaseModel):
    """Customs info model for international shipments."""

    contents: list[CustomsItemModel]
    customs_certify: bool = True
    customs_signer: str = ""
    contents_type: str = "merchandise"
    restriction_type: str = "none"
    restriction_comments: str = ""
    eel_pfc: str = "NOEEI 30.37(a)"

    @model_validator(mode="after")
    def validate_customs_info(self) -> Self:
        """
        Validate customs information.

        Ensures:
        - At least one item in contents
        - Customs signer is provided when certified
        - Valid contents type
        """
        if not self.contents:
            raise ValueError("customs_info must contain at least one item")

        if self.customs_certify and not self.customs_signer.strip():
            raise ValueError("customs_signer is required when customs_certify is True")

        valid_contents_types = ["merchandise", "returned_goods", "documents", "gift", "sample"]
        if self.contents_type not in valid_contents_types:
            raise ValueError(
                f"contents_type must be one of {valid_contents_types}, got: {self.contents_type}"
            )

        return self


class ShipmentRequest(BaseModel):
    """Request model for creating shipments."""

    to_address: AddressModel
    from_address: AddressModel
    parcel: ParcelModel
    carrier: str = "USPS"
    service: str | None = None  # Specific service (e.g., "FEDEX_GROUND", "Priority")
    customs_info: dict[str, Any] | None = None  # Customs info for international shipments

    @model_validator(mode="after")
    def validate_international_shipment(self) -> Self:
        """
        Validate shipment based on origin and destination.

        Ensures:
        - Customs info is provided for international shipments
        - Country codes are valid format (2 or 3 letters)
        - Addresses are not identical
        """
        to_country = getattr(self.to_address, "country", "US").strip().upper()
        from_country = getattr(self.from_address, "country", "US").strip().upper()

        # Normalize country codes (handle both 2 and 3 letter codes)
        # Common conversions
        country_map = {
            "USA": "US",
            "GBR": "GB",
            "CAN": "CA",
            "AUS": "AU",
            "DEU": "DE",
            "FRA": "FR",
        }
        to_country = country_map.get(to_country, to_country)
        from_country = country_map.get(from_country, from_country)

        # Check if international shipment (different countries)
        is_international = to_country != from_country

        if is_international and not self.customs_info:
            raise ValueError(
                f"customs_info is required for international shipments "
                f"(from {from_country} to {to_country})"
            )

        # Validate addresses are not identical
        to_city = getattr(self.to_address, "city", "").strip().lower()
        from_city = getattr(self.from_address, "city", "").strip().lower()
        to_zip = getattr(self.to_address, "zip", "").strip()
        from_zip = getattr(self.from_address, "zip", "").strip()

        if (
            to_country == from_country
            and to_city == from_city
            and to_zip == from_zip
            and to_city
            and to_zip
        ):
            raise ValueError(
                "to_address and from_address appear to be identical - "
                "please verify shipment addresses"
            )

        return self


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
