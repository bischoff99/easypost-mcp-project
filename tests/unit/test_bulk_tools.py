"""Tests for bulk shipment tools."""

import pytest

from src.mcp_server.tools.bulk_tools import (
    CA_STORE_ADDRESSES,
    parse_dimensions,
    parse_spreadsheet_line,
    parse_weight,
)


class TestBulkToolsParsing:
    """Test parsing utilities for bulk shipment tool."""

    def test_parse_dimensions_standard(self):
        """Test parsing standard dimension string."""
        length, width, height = parse_dimensions("13 x 12 x 2")
        assert length == 13.0
        assert width == 12.0
        assert height == 2.0

    def test_parse_dimensions_with_spaces(self):
        """Test parsing dimensions with extra spaces."""
        length, width, height = parse_dimensions("10  x  8  x  6")
        assert length == 10.0
        assert width == 8.0
        assert height == 6.0

    def test_parse_dimensions_invalid(self):
        """Test that invalid dimensions raise ValueError with clear message."""
        import pytest

        with pytest.raises(ValueError) as exc_info:
            parse_dimensions("invalid")

        assert "Could not parse dimensions" in str(exc_info.value)
        assert "12.5 x 10 x 3" in str(exc_info.value)  # Example in error message

    def test_parse_dimensions_decimal(self):
        """Test parsing dimensions with decimal values."""
        length, width, height = parse_dimensions("12.5 x 10.25 x 3.75")
        assert length == 12.5
        assert width == 10.25
        assert height == 3.75

    def test_parse_dimensions_unicode_separator(self):
        """Test parsing dimensions with Unicode multiplication sign."""
        length, width, height = parse_dimensions("12 × 10 × 3")
        assert length == 12.0
        assert width == 10.0
        assert height == 3.0

    def test_parse_dimensions_asterisk_separator(self):
        """Test parsing dimensions with asterisk separator."""
        length, width, height = parse_dimensions("12*10*3")
        assert length == 12.0
        assert width == 10.0
        assert height == 3.0

    def test_parse_dimensions_by_separator(self):
        """Test parsing dimensions with 'by' separator."""
        length, width, height = parse_dimensions("12 by 10 by 3")
        assert length == 12.0
        assert width == 10.0
        assert height == 3.0

    def test_parse_dimensions_fractional(self):
        """Test parsing dimensions with fractional inches (e.g., 11 1/2)."""
        # Test fractional dimensions
        length, width, height = parse_dimensions("16 x 11 1/2 x 3 1/2")
        assert length == 16.0
        assert width == 11.5
        assert height == 3.5

        # Test another fractional combination
        length, width, height = parse_dimensions("11 1/2 x 9 3/4 x 2 1/4")
        assert length == 11.5
        assert width == 9.75
        assert height == 2.25

    def test_parse_weight_pounds(self):
        """Test parsing weight in pounds."""
        weight = parse_weight("1.8 lbs")
        assert weight == 28.8  # 1.8 * 16

    def test_parse_weight_pounds_singular(self):
        """Test parsing weight with 'lb' singular."""
        weight = parse_weight("2 lb")
        assert weight == 32.0  # 2 * 16

    def test_parse_weight_ounces(self):
        """Test parsing weight already in ounces."""
        weight = parse_weight("16 oz")
        assert weight == 16.0

    def test_parse_weight_decimal(self):
        """Test parsing decimal weight."""
        weight = parse_weight("1.5 lbs")
        assert weight == 24.0  # 1.5 * 16

    def test_parse_weight_numeric_only_decimal(self):
        """Test parsing numeric-only weight (should infer lbs for decimal)."""
        weight = parse_weight("5.26")
        assert weight == 84.16  # 5.26 * 16 (inferred as lbs)

    def test_parse_weight_numeric_only_large(self):
        """Test parsing large numeric-only weight (should infer oz)."""
        weight = parse_weight("84.16")
        assert weight == 84.16  # Large decimal inferred as oz

    def test_parse_weight_numeric_only_small(self):
        """Test parsing small numeric-only weight (should infer lbs)."""
        weight = parse_weight("2")
        assert weight == 32.0  # 2 * 16 (inferred as lbs)

    def test_parse_weight_kg(self):
        """Test parsing weight in kilograms."""
        weight = parse_weight("1 kg")
        assert abs(weight - 35.274) < 0.1  # 1 kg ≈ 35.274 oz

    def test_parse_weight_grams(self):
        """Test parsing weight in grams."""
        weight = parse_weight("100 g")
        assert abs(weight - 3.527) < 0.1  # 100g ≈ 3.527 oz

    def test_parse_weight_invalid(self):
        """Test parsing invalid weight raises error."""
        with pytest.raises(ValueError, match="Could not parse weight"):
            parse_weight("abc")

    def test_parse_weight_empty(self):
        """Test parsing empty weight raises error."""
        with pytest.raises(ValueError, match="Weight string is empty"):
            parse_weight("")

    def test_parse_spreadsheet_line_valid(self):
        """Test parsing valid spreadsheet line."""
        line = "California\tFEDEX- Priority\tBarra\tOdeamar\t+639612109875\tjustinenganga@gmail.com\tBlk 6 Lot 48 Camella Vera, Bignay\t\tValenzuela City\tMetro Manila\t1440\tPhilippines\tTRUE\t13 x 12 x 2\t1.8 lbs\t1.5 lbs Dead Sea Mineral Bath Salts"

        data = parse_spreadsheet_line(line)

        assert data["origin_state"] == "California"
        assert data["carrier_preference"] == "FEDEX- Priority"
        assert data["recipient_name"] == "Barra"
        assert data["recipient_last_name"] == "Odeamar"
        assert data["recipient_phone"] == "+639612109875"
        assert data["recipient_email"] == "justinenganga@gmail.com"
        assert data["street1"] == "Blk 6 Lot 48 Camella Vera, Bignay"
        assert data["street2"] == ""
        assert data["city"] == "Valenzuela City"
        assert data["state"] == "Metro Manila"
        assert data["zip"] == "1440"
        assert data["country"] == "PH"  # Returns ISO country code, not full name
        assert data["dimensions"] == "13 x 12 x 2"
        assert data["weight"] == "1.8 lbs"
        assert "Dead Sea Mineral Bath Salts" in data["contents"]

    def test_parse_spreadsheet_line_invalid(self):
        """Test parsing invalid line with too few columns."""
        line = "California\tFEDEX\tBarra"  # Only 3 columns

        with pytest.raises(ValueError, match="Missing required fields"):
            parse_spreadsheet_line(line)

    def test_ca_store_addresses_exist(self):
        """Test that California store addresses are defined."""
        assert "Los Angeles" in CA_STORE_ADDRESSES

        # Verify LA store has required fields
        la_store = CA_STORE_ADDRESSES["Los Angeles"]
        assert la_store["name"] == "LA General Warehouse"
        assert la_store["company"] == "California Distribution Center"
        assert la_store["city"] == "Los Angeles"
        assert la_store["state"] == "CA"
        assert la_store["zip"] == "90021"
        assert la_store["country"] == "US"
        assert "Olympic Blvd" in la_store["street1"]
        assert la_store["phone"] == "213-555-0100"


class TestFieldTypeDetection:
    """Test detect_field_type function for enhanced patterns."""

    def test_email_with_plus_addressing(self):
        """Test email detection with plus addressing."""
        from src.mcp_server.tools.bulk_tools import detect_field_type

        assert detect_field_type("user+tag@example.com") == "email"
        assert detect_field_type("john.doe+spam@company.co.uk") == "email"

    def test_phone_with_extension(self):
        """Test phone number detection with extensions."""
        from src.mcp_server.tools.bulk_tools import detect_field_type

        assert detect_field_type("555-123-4567 x1234") == "phone"
        assert detect_field_type("555-123-4567 ext 100") == "phone"
        assert detect_field_type("555-123-4567 extension 5") == "phone"

    def test_international_postal_codes(self):
        """Test postal code detection for multiple countries."""
        from src.mcp_server.tools.bulk_tools import detect_field_type

        # US
        assert detect_field_type("90210") == "postal_code"
        assert detect_field_type("10001-1234") == "postal_code"

        # Canada
        assert detect_field_type("M5H 2N2") == "postal_code"
        assert detect_field_type("K1A0B1") == "postal_code"

        # UK
        assert detect_field_type("SW1A 1AA") == "postal_code"
        assert detect_field_type("EC1A 1BB") == "postal_code"

        # Germany/France
        assert detect_field_type("10115") == "postal_code"
        assert detect_field_type("75001") == "postal_code"

    def test_po_box_detection(self):
        """Test PO Box address detection."""
        from src.mcp_server.tools.bulk_tools import detect_field_type

        assert detect_field_type("P.O. Box 123") == "street"
        assert detect_field_type("PO Box 456") == "street"
        assert detect_field_type("Box 789") == "street"

    def test_military_address_detection(self):
        """Test military address detection."""
        from src.mcp_server.tools.bulk_tools import detect_field_type

        assert detect_field_type("APO AE 09012") == "street"
        assert detect_field_type("FPO AP 96374") == "street"
        assert detect_field_type("DPO AA 34004") == "street"
