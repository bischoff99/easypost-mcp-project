from __future__ import annotations

import pytest

from src.models.requests import CustomsInfoModel, CustomsItemModel, ShipmentRequest
from src.services.easypost_service import AddressModel, ParcelModel


def _address(country: str = "US", city: str = "Austin", zip_code: str = "78701") -> AddressModel:
    return AddressModel(
        name="Test",
        street1="123 Main",
        city=city,
        state="TX",
        zip=zip_code,
        country=country,
    )


def _parcel() -> ParcelModel:
    return ParcelModel(length=10, width=5, height=4, weight=16)


def _customs_info() -> dict:
    return CustomsInfoModel(
        contents=[
            CustomsItemModel(description="Shirt", quantity=1, value=25.0, origin_country="US")
        ],
        customs_signer="Tester",
    ).model_dump()


def test_customs_item_requires_positive_values():
    with pytest.raises(ValueError):
        CustomsItemModel(description=" ", quantity=1, value=10)
    with pytest.raises(ValueError):
        CustomsItemModel(description="Item", quantity=0, value=10)
    with pytest.raises(ValueError):
        CustomsItemModel(description="Item", quantity=1, value=0)
    with pytest.raises(ValueError):
        CustomsItemModel(description="Item", quantity=1, value=10, origin_country="XXXX")


def test_customs_info_requires_signer():
    with pytest.raises(ValueError):
        CustomsInfoModel(contents=[CustomsItemModel(description="Hat", quantity=1, value=10)])


def test_shipment_request_requires_customs_info_for_international():
    with pytest.raises(ValueError):
        ShipmentRequest(
            to_address=_address(country="CA", city="Toronto", zip_code="M4B1B3"),
            from_address=_address(country="US"),
            parcel=_parcel(),
        )


def test_shipment_request_rejects_identical_addresses():
    with pytest.raises(ValueError):
        ShipmentRequest(
            to_address=_address(),
            from_address=_address(),
            parcel=_parcel(),
        )


def test_shipment_request_valid_domestic_with_customs():
    request = ShipmentRequest(
        to_address=_address(city="Dallas", zip_code="75001"),
        from_address=_address(city="Austin", zip_code="78701"),
        parcel=_parcel(),
    )

    assert request.carrier == "USPS"
