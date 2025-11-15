"""
Unit tests for bulk_helpers.py - Pure functions.

These tests verify all pure helper functions work correctly
without any I/O operations or external dependencies.
"""

import pytest

from src.mcp_server.tools.bulk_helpers import (
    build_parcel,
    build_shipment_request,
    build_to_address,
    is_international_shipment,
    is_preferred_carrier,
    mark_preferred_rates,
    select_best_rate,
    select_warehouse_address,
    validate_shipment_data,
)
from src.models.bulk_dto import (
    AddressDTO,
    ShipmentDataDTO,
    ValidationResultDTO,
)


@pytest.fixture
def sample_shipment_data():
    """Sample shipment data for testing."""
    return ShipmentDataDTO(
        recipient_name="John",
        recipient_last_name="Doe",
        street1="123 Main St",
        street2="Apt 4B",
        city="San Francisco",
        state="CA",
        zip="94107",
        country="US",
        recipient_phone="555-1234",
        recipient_email="john@example.com",
        contents="Electronics",
        dimensions="10x8x4",
        weight="1.5 lbs",
        origin_state="California",
        carrier_preference="USPS",
    )


@pytest.fixture
def sample_validation_result(sample_shipment_data):
    """Sample validation result for testing."""
    return ValidationResultDTO(
        line=1,
        data=sample_shipment_data,
        length=10.0,
        width=8.0,
        height=4.0,
        weight_oz=24.0,
        valid=True,
        errors=[],
    )


class TestValidateShipmentData:
    """Tests for validate_shipment_data()."""

    def test_valid_shipment(self, sample_shipment_data):
        """Test validation of valid shipment data."""
        result = validate_shipment_data(sample_shipment_data, line_number=1)
        assert result.valid is True
        assert len(result.errors) == 0
        assert result.length == 10.0
        assert result.weight_oz == 24.0

    def test_invalid_weight(self, sample_shipment_data):
        """Test validation fails for overweight package."""
        sample_shipment_data.weight = "200 lbs"
        result = validate_shipment_data(sample_shipment_data, line_number=1)
        assert result.valid is False
        assert any("exceeds 150 lbs" in err for err in result.errors)

    def test_invalid_zip(self, sample_shipment_data):
        """Test validation fails for invalid zip."""
        sample_shipment_data.zip = "12"
        result = validate_shipment_data(sample_shipment_data, line_number=1)
        assert result.valid is False
        assert any("Invalid postal code" in err for err in result.errors)

    def test_missing_street(self, sample_shipment_data):
        """Test validation fails for missing street."""
        sample_shipment_data.street1 = ""
        result = validate_shipment_data(sample_shipment_data, line_number=1)
        assert result.valid is False
        assert any("Missing street address" in err for err in result.errors)

    def test_missing_country(self, sample_shipment_data):
        """Test validation fails for missing country."""
        sample_shipment_data.country = ""
        result = validate_shipment_data(sample_shipment_data, line_number=1)
        assert result.valid is False
        assert any("Missing country" in err for err in result.errors)

    def test_parse_error(self, sample_shipment_data):
        """Test validation handles parse errors."""
        sample_shipment_data.dimensions = "invalid"
        result = validate_shipment_data(sample_shipment_data, line_number=1)
        assert result.valid is False
        assert len(result.errors) > 0


class TestSelectWarehouseAddress:
    """Tests for select_warehouse_address()."""

    def test_custom_sender_address(self, sample_shipment_data):
        """Test uses custom sender address when provided."""
        sample_shipment_data.sender_address = {
            "name": "Custom Sender",
            "street1": "789 Custom St",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90001",
            "country": "US",
        }
        address, info = select_warehouse_address(sample_shipment_data)
        assert address.name == "Custom Sender"
        assert "Custom sender" in info

    def test_auto_select_warehouse(self, sample_shipment_data):
        """Test auto-selects warehouse by category and state."""
        sample_shipment_data.sender_address = None
        address, info = select_warehouse_address(sample_shipment_data)
        assert address is not None
        assert "California" in info


class TestBuildToAddress:
    """Tests for build_to_address()."""

    def test_builds_address_correctly(self, sample_shipment_data):
        """Test builds address from shipment data."""
        address = build_to_address(sample_shipment_data)
        assert address.name == "John Doe"
        assert address.street1 == "123 Main St"
        assert address.city == "San Francisco"
        assert address.state == "CA"
        assert address.zip == "94107"
        assert address.country == "US"


class TestBuildParcel:
    """Tests for build_parcel()."""

    def test_builds_parcel_correctly(self, sample_validation_result):
        """Test builds parcel from validation result."""
        parcel = build_parcel(sample_validation_result)
        assert parcel.length == 10.0
        assert parcel.width == 8.0
        assert parcel.height == 4.0
        assert parcel.weight == 24.0

    def test_raises_on_missing_dimensions(self):
        """Test raises error for missing dimensions."""
        invalid_result = ValidationResultDTO(
            line=1, valid=True, errors=[], length=None, weight_oz=None
        )
        with pytest.raises(ValueError):
            build_parcel(invalid_result)


class TestIsInternationalShipment:
    """Tests for is_international_shipment()."""

    def test_domestic_shipment(self):
        """Test returns False for domestic shipment."""
        to_addr = AddressDTO(
            name="Recipient",
            street1="123 St",
            city="SF",
            state="CA",
            zip="94107",
            country="US",
        )
        from_addr = AddressDTO(
            name="Sender",
            street1="456 St",
            city="LA",
            state="CA",
            zip="90001",
            country="US",
        )
        assert is_international_shipment(to_addr, from_addr) is False

    def test_international_shipment(self):
        """Test returns True for international shipment."""
        to_addr = AddressDTO(
            name="Recipient",
            street1="123 St",
            city="Toronto",
            state="ON",
            zip="M5H 2N2",
            country="CA",
        )
        from_addr = AddressDTO(
            name="Sender",
            street1="456 St",
            city="LA",
            state="CA",
            zip="90001",
            country="US",
        )
        assert is_international_shipment(to_addr, from_addr) is True


class TestBuildShipmentRequest:
    """Tests for build_shipment_request()."""

    def test_builds_request_correctly(self, sample_validation_result):
        """Test builds complete shipment request."""
        to_addr = build_to_address(sample_validation_result.data)
        from_addr = AddressDTO(
            name="Warehouse",
            street1="456 St",
            city="LA",
            state="CA",
            zip="90001",
            country="US",
        )
        parcel = build_parcel(sample_validation_result)

        request = build_shipment_request(
            to_address=to_addr,
            from_address=from_addr,
            parcel=parcel,
            carrier="USPS",
            reference="test-123",
        )

        assert request.to_address == to_addr
        assert request.from_address == from_addr
        assert request.parcel == parcel
        assert request.carrier == "USPS"
        assert request.reference == "test-123"


class TestIsPreferredCarrier:
    """Tests for is_preferred_carrier()."""

    @pytest.mark.parametrize(
        "easypost_carrier,preferred,expected",
        [
            ("USPS", "USPS", True),
            ("FEDEX", "FedEx", True),
            ("FEDEXDEFAULT", "FedEx", True),
            ("UPS", "UPS", True),
            ("UPSDAP", "UPS", True),
            ("DHL", "DHL", True),
            ("DHEXPRESS", "DHL", True),
            ("USAEXPORT", "USA", True),
            ("ASENDIA", "ASENDIA", True),
            ("USPS", "FedEx", False),
            ("UPS", "DHL", False),
            ("", "USPS", False),
        ],
    )
    def test_carrier_matching(self, easypost_carrier, preferred, expected):
        """Test carrier matching logic."""
        assert is_preferred_carrier(easypost_carrier, preferred) == expected


class TestParseCarrierPreference:
    """Tests for parse_carrier_preference()."""

    def test_parses_carrier_with_first_class_service(self):
        """Test parses 'USPS- First Class Mail' correctly."""
        from src.mcp_server.tools.bulk_helpers import parse_carrier_preference

        carrier, service = parse_carrier_preference("USPS- First Class Mail")
        assert carrier == "USPS"
        assert service == "FIRSTCLASS"

    def test_parses_carrier_with_priority_service(self):
        """Test parses 'FedEx- Priority' correctly."""
        from src.mcp_server.tools.bulk_helpers import parse_carrier_preference

        carrier, service = parse_carrier_preference("FedEx- Priority")
        assert carrier == "FEDEX"
        assert service == "PRIORITY"

    def test_parses_carrier_only(self):
        """Test parses carrier-only preference."""
        from src.mcp_server.tools.bulk_helpers import parse_carrier_preference

        carrier, service = parse_carrier_preference("USPS")
        assert carrier == "USPS"
        assert service is None

    def test_handles_none(self):
        """Test handles None preference."""
        from src.mcp_server.tools.bulk_helpers import parse_carrier_preference

        carrier, service = parse_carrier_preference(None)
        assert carrier is None
        assert service is None

    def test_parses_express_service(self):
        """Test parses Express service."""
        from src.mcp_server.tools.bulk_helpers import parse_carrier_preference

        carrier, service = parse_carrier_preference("USPS- Express Mail")
        assert carrier == "USPS"
        assert service == "EXPRESS"


class TestMarkPreferredRates:
    """Tests for mark_preferred_rates()."""

    def test_marks_preferred_rates(self):
        """Test marks preferred rates correctly."""
        rates = [
            {"carrier": "USPS", "rate": "10.00"},
            {"carrier": "FEDEX", "rate": "15.00"},
            {"carrier": "UPS", "rate": "12.00"},
        ]
        marked = mark_preferred_rates(rates, "USPS")
        assert marked[0]["preferred"] is True
        assert marked[1]["preferred"] is False
        assert marked[2]["preferred"] is False

    def test_no_preference_returns_unchanged(self):
        """Test returns rates unchanged when no preference."""
        rates = [{"carrier": "USPS", "rate": "10.00"}]
        marked = mark_preferred_rates(rates, None)
        assert marked == rates


class TestSelectBestRate:
    """Tests for select_best_rate()."""

    def test_selects_preferred_when_purchasing(self):
        """Test selects preferred carrier when purchasing."""
        rates = [
            {"carrier": "USPS", "rate": "15.00", "preferred": False},
            {"carrier": "FEDEX", "rate": "10.00", "preferred": True},
        ]
        selected = select_best_rate(rates, purchase_labels=True, preferred_carrier="FEDEX")
        assert selected["carrier"] == "FEDEX"

    def test_selects_cheapest_when_no_preferred(self):
        """Test selects cheapest when no preferred available."""
        rates = [
            {"carrier": "USPS", "rate": "15.00", "preferred": False},
            {"carrier": "FEDEX", "rate": "10.00", "preferred": False},
        ]
        selected = select_best_rate(rates, purchase_labels=True, preferred_carrier="UPS")
        assert selected["carrier"] == "FEDEX"  # Cheapest

    def test_returns_none_for_empty_rates(self):
        """Test returns None for empty rates."""
        assert select_best_rate([], purchase_labels=True) is None

    def test_selects_cheapest_usps_when_multiple_services(self):
        """
        BUG FIX TEST: When multiple USPS rates exist, select cheapest (First Class),
        not first (which could be Priority/Express).

        This tests the fix for the issue where Express Mail ($93.60) or
        Priority Mail ($80.35) were selected instead of First Class ($46.33).
        """
        rates = [
            {
                "carrier": "USPS",
                "service": "PriorityMailInternational",
                "rate": "74.66",
                "preferred": True,
            },
            {
                "carrier": "USPS",
                "service": "ExpressMailInternational",
                "rate": "93.60",
                "preferred": True,
            },
            {
                "carrier": "USPS",
                "service": "FirstClassPackageInternationalService",
                "rate": "46.33",
                "preferred": True,
            },
            {"carrier": "FedEx", "service": "International", "rate": "55.00", "preferred": False},
        ]
        selected = select_best_rate(rates, purchase_labels=True, preferred_carrier="USPS")

        # Should select cheapest USPS rate (First Class $46.33), not first USPS rate
        assert selected["carrier"] == "USPS"
        assert selected["service"] == "FirstClassPackageInternationalService"
        assert selected["rate"] == "46.33"

    def test_selects_specific_service_when_requested(self):
        """
        Test that when specific service is requested (e.g., "USPS- First Class Mail"),
        it selects that exact service, not just cheapest USPS.
        """
        rates = [
            {"carrier": "USPS", "service": "PriorityMailInternational", "rate": "74.66"},
            {"carrier": "USPS", "service": "ExpressMailInternational", "rate": "93.60"},
            {
                "carrier": "USPS",
                "service": "FirstClassPackageInternationalService",
                "rate": "46.33",
            },
        ]

        # Request specific service
        selected = select_best_rate(
            rates, purchase_labels=True, preferred_carrier="USPS- First Class Mail"
        )

        # Should select First Class service (matched by keyword)
        assert selected["carrier"] == "USPS"
        assert "FirstClass" in selected["service"]
        assert selected["rate"] == "46.33"

    def test_selects_priority_when_explicitly_requested(self):
        """Test that Priority is selected when explicitly requested, even if more expensive."""
        rates = [
            {
                "carrier": "USPS",
                "service": "FirstClassPackageInternationalService",
                "rate": "46.33",
            },
            {"carrier": "USPS", "service": "PriorityMailInternational", "rate": "74.66"},
            {"carrier": "USPS", "service": "ExpressMailInternational", "rate": "93.60"},
        ]

        # Request Priority specifically
        selected = select_best_rate(rates, purchase_labels=True, preferred_carrier="USPS- Priority")

        # Should select Priority (more expensive but explicitly requested)
        assert selected["carrier"] == "USPS"
        assert "Priority" in selected["service"]
        assert selected["rate"] == "74.66"

    def test_fallback_to_cheapest_when_service_not_available(self):
        """Test fallback to cheapest USPS when requested service not available."""
        rates = [
            {
                "carrier": "USPS",
                "service": "FirstClassPackageInternationalService",
                "rate": "46.33",
            },
            {"carrier": "USPS", "service": "PriorityMailInternational", "rate": "74.66"},
        ]

        # Request service that doesn't exist (Ground)
        selected = select_best_rate(rates, purchase_labels=True, preferred_carrier="USPS- Ground")

        # Should fallback to cheapest USPS
        assert selected["carrier"] == "USPS"
        assert selected["rate"] == "46.33"
