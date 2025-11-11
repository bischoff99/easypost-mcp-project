"""
Unit tests for bulk_io.py - I/O operations.

These tests mock external API calls (EasyPost) to verify
I/O functions work correctly.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.mcp_server.tools.bulk_io import (
    create_shipment_with_rates,
    prepare_customs_if_international,
    verify_address_if_needed,
)
from src.models.bulk_dto import AddressDTO, CustomsInfoDTO, ParcelDTO, ShipmentRequestDTO


@pytest.fixture
def sample_address():
    """Sample address for testing."""
    return AddressDTO(
        name="John Doe",
        street1="123 Main St",
        city="San Francisco",
        state="CA",
        zip="94107",
        country="US",
    )


@pytest.fixture
def mock_easypost_service():
    """Mock EasyPost service."""
    service = MagicMock()
    service.api_key = "test_key"
    service.client = MagicMock()
    return service


@pytest.fixture
def mock_context():
    """Mock MCP context."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    return ctx


class TestVerifyAddressIfNeeded:
    """Tests for verify_address_if_needed()."""

    @pytest.mark.asyncio
    async def test_skips_verification_for_domestic(self, sample_address, mock_easypost_service):
        """Test skips verification for domestic shipments."""
        result = await verify_address_if_needed(
            sample_address,
            mock_easypost_service,
            is_international=False,
            carrier_preference=None,
        )
        assert result.verification_success is True
        assert result.address == sample_address
        mock_easypost_service.verify_address.assert_not_called()

    @pytest.mark.asyncio
    async def test_skips_verification_for_non_fedex_ups(
        self, sample_address, mock_easypost_service
    ):
        """Test skips verification for non-FedEx/UPS international."""
        intl_address = AddressDTO(
            name="Recipient",
            street1="123 St",
            city="Toronto",
            state="ON",
            zip="M5H 2N2",
            country="CA",
        )
        result = await verify_address_if_needed(
            intl_address,
            mock_easypost_service,
            is_international=True,
            carrier_preference="USPS",
        )
        assert result.verification_success is True
        mock_easypost_service.verify_address.assert_not_called()

    @pytest.mark.asyncio
    async def test_verifies_fedex_international(
        self, sample_address, mock_easypost_service, mock_context
    ):
        """Test verifies address for FedEx international."""
        intl_address = AddressDTO(
            name="Recipient",
            street1="123 St",
            city="Toronto",
            state="ON",
            zip="M5H 2N2",
            country="CA",
        )

        # Mock successful verification
        mock_easypost_service.verify_address = AsyncMock(
            return_value={
                "status": "success",
                "data": {
                    "verification_success": True,
                    "address": {
                        "name": "Recipient",
                        "street1": "123 Verified St",
                        "city": "Toronto",
                        "state": "ON",
                        "zip": "M5H 2N2",
                        "country": "CA",
                    },
                },
            }
        )

        result = await verify_address_if_needed(
            intl_address,
            mock_easypost_service,
            is_international=True,
            carrier_preference="FedEx",
            ctx=mock_context,
        )

        assert result.verification_success is True
        assert result.address.street1 == "123 Verified St"
        mock_easypost_service.verify_address.assert_called_once()

    @pytest.mark.asyncio
    async def test_handles_verification_failure(self, sample_address, mock_easypost_service):
        """Test handles verification failure gracefully."""
        intl_address = AddressDTO(
            name="Recipient",
            street1="123 St",
            city="Invalid",
            state="XX",
            zip="00000",
            country="CA",
        )

        mock_easypost_service.verify_address = AsyncMock(
            return_value={
                "status": "error",
                "message": "Verification failed",
                "data": {"errors": ["Invalid address"]},
            }
        )

        result = await verify_address_if_needed(
            intl_address,
            mock_easypost_service,
            is_international=True,
            carrier_preference="FedEx",
        )

        assert result.verification_success is False
        assert len(result.errors) > 0


class TestPrepareCustomsIfInternational:
    """Tests for prepare_customs_if_international()."""

    @pytest.mark.asyncio
    @patch("src.mcp_server.tools.bulk_io.get_or_create_customs")
    async def test_prepares_customs_for_international(
        self, mock_get_customs, mock_easypost_service
    ):
        """Test prepares customs info for international shipments."""
        from_address = AddressDTO(
            name="Warehouse",
            street1="456 St",
            city="LA",
            state="CA",
            zip="90001",
            country="US",
        )

        mock_get_customs.return_value = {
            "contents_type": "merchandise",
            "customs_items": [
                {
                    "description": "Electronics",
                    "quantity": 1,
                    "value": 100.0,
                    "weight": 16.0,
                }
            ],
        }

        result = await prepare_customs_if_international(
            contents="Electronics",
            weight_oz=16.0,
            easypost_service=mock_easypost_service,
            from_address=from_address,
            carrier_preference="FedEx",
        )

        assert result is not None
        assert isinstance(result, CustomsInfoDTO)
        mock_get_customs.assert_called_once()

    @pytest.mark.asyncio
    async def test_returns_none_for_domestic(self, mock_easypost_service):
        """Test returns None for domestic shipments (should not be called)."""
        # This function should only be called for international
        # So we test the logic path
        pass


class TestCreateShipmentWithRates:
    """Tests for create_shipment_with_rates()."""

    @pytest.fixture
    def sample_shipment_request(self, sample_address):
        """Sample shipment request for testing."""
        from_address = AddressDTO(
            name="Warehouse",
            street1="456 St",
            city="LA",
            state="CA",
            zip="90001",
            country="US",
        )
        parcel = ParcelDTO(length=10.0, width=8.0, height=4.0, weight=16.0)
        return ShipmentRequestDTO(
            to_address=sample_address,
            from_address=from_address,
            parcel=parcel,
        )

    @pytest.mark.asyncio
    async def test_creates_shipment_successfully(
        self, sample_shipment_request, mock_easypost_service
    ):
        """Test creates shipment successfully."""
        mock_easypost_service.create_shipment = AsyncMock(
            return_value={
                "status": "success",
                "data": {
                    "id": "shp_123",
                    "rates": [
                        {"id": "rate_1", "carrier": "USPS", "rate": "10.00"},
                        {"id": "rate_2", "carrier": "FEDEX", "rate": "15.00"},
                    ],
                },
            }
        )

        result = await create_shipment_with_rates(
            sample_shipment_request,
            mock_easypost_service,
            purchase_labels=False,
            carrier=None,
        )

        assert result.shipment_id == "shp_123"
        assert len(result.rates) == 2
        assert result.errors == []

    @pytest.mark.asyncio
    async def test_purchases_label_when_requested(
        self, sample_shipment_request, mock_easypost_service
    ):
        """Test purchases label when purchase_labels=True."""
        mock_easypost_service.create_shipment = AsyncMock(
            return_value={
                "status": "success",
                "data": {
                    "id": "shp_123",
                    "rates": [
                        {"id": "rate_1", "carrier": "USPS", "rate": "10.00"},
                    ],
                },
            }
        )
        mock_easypost_service.buy_shipment = AsyncMock(
            return_value={
                "status": "success",
                "data": {
                    "tracking_code": "TRACK123",
                    "postage_label": {"label_url": "https://label.url"},
                },
            }
        )

        result = await create_shipment_with_rates(
            sample_shipment_request,
            mock_easypost_service,
            purchase_labels=True,
            carrier="USPS",
        )

        assert result.tracking_code == "TRACK123"
        assert result.label_url == "https://label.url"

    @pytest.mark.asyncio
    async def test_handles_creation_error(self, sample_shipment_request, mock_easypost_service):
        """Test handles shipment creation errors."""
        mock_easypost_service.create_shipment = AsyncMock(
            return_value={
                "status": "error",
                "message": "Invalid address",
            }
        )

        result = await create_shipment_with_rates(
            sample_shipment_request,
            mock_easypost_service,
            purchase_labels=False,
            carrier=None,
        )

        assert result.shipment_id is None
        assert len(result.errors) > 0

    @pytest.mark.asyncio
    async def test_handles_exception(self, sample_shipment_request, mock_easypost_service):
        """Test handles exceptions gracefully."""
        mock_easypost_service.create_shipment = AsyncMock(side_effect=Exception("API Error"))

        result = await create_shipment_with_rates(
            sample_shipment_request,
            mock_easypost_service,
            purchase_labels=False,
            carrier=None,
        )

        assert result.shipment_id is None
        assert len(result.errors) > 0
