"""Tests for bulk shipment tools."""

import pytest
from src.mcp.tools.bulk_tools import (
    parse_dimensions,
    parse_weight,
    parse_spreadsheet_line,
    CA_STORE_ADDRESSES,
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

    def test_parse_dimensions_default(self):
        """Test default dimensions for invalid input."""
        length, width, height = parse_dimensions("invalid")
        assert length == 12.0
        assert width == 9.0
        assert height == 6.0

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
        assert data["country"] == "Philippines"
        assert data["dimensions"] == "13 x 12 x 2"
        assert data["weight"] == "1.8 lbs"
        assert "Dead Sea Mineral Bath Salts" in data["contents"]

    def test_parse_spreadsheet_line_invalid(self):
        """Test parsing invalid line with too few columns."""
        line = "California\tFEDEX\tBarra"  # Only 3 columns
        
        with pytest.raises(ValueError, match="Invalid line format"):
            parse_spreadsheet_line(line)

    def test_ca_store_addresses_exist(self):
        """Test that California store addresses are defined."""
        assert "Los Angeles" in CA_STORE_ADDRESSES
        assert "San Francisco" in CA_STORE_ADDRESSES
        assert "San Diego" in CA_STORE_ADDRESSES
        
        # Verify LA store has required fields
        la_store = CA_STORE_ADDRESSES["Los Angeles"]
        assert la_store["name"] == "Beauty & Wellness LA"
        assert la_store["city"] == "Los Angeles"
        assert la_store["state"] == "CA"
        assert la_store["zip"] == "90048"
        assert "Beverly Blvd" in la_store["street1"]

