"""Unit tests for EEL/PFC customs requirements (EasyPost guide compliance)."""

import pytest

from src.services.smart_customs import extract_customs_smart


class MockEasyPostClient:
    """Mock EasyPost client for testing."""

    def __init__(self):
        self.customs_item = MockCustomsItemResource()
        self.customs_info = MockCustomsInfoResource()


class MockCustomsItemResource:
    """Mock CustomsItem resource."""

    def create(self, **kwargs):
        """Create mock customs item."""
        return {
            "description": kwargs.get("description", ""),
            "quantity": kwargs.get("quantity", 1),
            "value": kwargs.get("value", 0.0),
            "weight": kwargs.get("weight", 0.0),
            "hs_tariff_number": kwargs.get("hs_tariff_number", ""),
            "origin_country": kwargs.get("origin_country", "US"),
        }


class MockCustomsInfoResource:
    """Mock CustomsInfo resource."""

    def __init__(self):
        self.last_create_params = {}

    def create(self, **kwargs):
        """Create mock customs info and store params."""
        self.last_create_params = kwargs
        return kwargs


class TestEELPFCRequirements:
    """Test EEL/PFC requirements per EasyPost customs guide."""

    def test_low_value_uses_noeei_automatic(self):
        """Test shipments < $2,500 automatically use NOEEI 30.37(a)."""
        client = MockEasyPostClient()

        # Single item worth $100 (well below $2,500 threshold)
        result = extract_customs_smart(
            contents="(1) Jeans HTS: 6203.42.4011 ($100)",
            weight_oz=16.0,
            easypost_client=client,
        )

        assert result is not None
        assert result["eel_pfc"] == "NOEEI 30.37(a)"

    def test_low_value_multi_item_uses_noeei(self):
        """Test multiple items totaling < $2,500 use NOEEI."""
        client = MockEasyPostClient()

        # 10 items @ $200 each = $2,000 total (below threshold)
        result = extract_customs_smart(
            contents="(10) Phones HTS: 8517.12.0000 ($200 each)",
            weight_oz=80.0,
            easypost_client=client,
        )

        assert result is not None
        assert result["eel_pfc"] == "NOEEI 30.37(a)"

    def test_high_value_requires_aes_itn(self):
        """Test shipments ≥ $2,500 require AES ITN."""
        client = MockEasyPostClient()

        # Single item worth $3,000 (above threshold)
        with pytest.raises(ValueError) as excinfo:
            extract_customs_smart(
                contents="(1) Expensive Tablet HTS: 8471.30.0100 ($3000)",
                weight_oz=32.0,
                easypost_client=client,
            )

        error_msg = str(excinfo.value)
        assert "$3000.00" in error_msg or "$3,000" in error_msg
        assert "AES ITN" in error_msg
        assert "aesdirect.census.gov" in error_msg

    def test_high_value_multi_item_requires_aes_itn(self):
        """Test multiple items totaling ≥ $2,500 require AES ITN."""
        client = MockEasyPostClient()

        # 5 items @ $500 each = $2,500 total (at threshold)
        with pytest.raises(ValueError) as excinfo:
            extract_customs_smart(
                contents="(5) Laptops HTS: 8471.30.0100 ($500 each)",
                weight_oz=80.0,
                easypost_client=client,
            )

        error_msg = str(excinfo.value)
        assert "$2500" in error_msg or "$2,500" in error_msg
        assert "AES ITN" in error_msg

    def test_custom_eel_pfc_accepted(self):
        """Test custom EEL/PFC (AES ITN) is accepted for high-value shipments."""
        client = MockEasyPostClient()

        # High-value shipment with custom AES ITN
        result = extract_customs_smart(
            contents="(1) Expensive Equipment HTS: 8471.30.0100 ($3000)",
            weight_oz=32.0,
            easypost_client=client,
            eel_pfc="AES X20120502123456",  # Example ITN from EasyPost guide
        )

        assert result is not None
        assert result["eel_pfc"] == "AES X20120502123456"

    def test_custom_eel_pfc_overrides_automatic(self):
        """Test custom EEL/PFC overrides automatic NOEEI even for low values."""
        client = MockEasyPostClient()

        # Low-value shipment but user provides custom EEL/PFC
        result = extract_customs_smart(
            contents="(1) Jeans HTS: 6203.42.4011 ($50)",
            weight_oz=16.0,
            easypost_client=client,
            eel_pfc="CUSTOM_EEL_CODE",
        )

        assert result is not None
        assert result["eel_pfc"] == "CUSTOM_EEL_CODE"

    def test_threshold_exactly_2500_requires_itn(self):
        """Test exactly $2,500 requires AES ITN."""
        client = MockEasyPostClient()

        # Exactly at threshold
        with pytest.raises(ValueError) as excinfo:
            extract_customs_smart(
                contents="(10) Items HTS: 6203.42.4011 ($250 each)",
                weight_oz=160.0,
                easypost_client=client,
            )

        error_msg = str(excinfo.value)
        assert "2500" in error_msg

    def test_threshold_just_below_2500_uses_noeei(self):
        """Test $2,499 uses automatic NOEEI."""
        client = MockEasyPostClient()

        # Just below threshold
        result = extract_customs_smart(
            contents="(1) High-End Laptop HTS: 8471.30.0100 ($2499)",
            weight_oz=32.0,
            easypost_client=client,
        )

        assert result is not None
        assert result["eel_pfc"] == "NOEEI 30.37(a)"


class TestUPSItemLimit:
    """Test UPS 100-item limit enforcement."""

    def test_single_item_no_truncation(self):
        """Test single item is not affected by limit."""
        client = MockEasyPostClient()

        result = extract_customs_smart(
            contents="(1) Jeans HTS: 6203.42.4011 ($25)",
            weight_oz=16.0,
            easypost_client=client,
        )

        assert result is not None
        assert len(result["customs_items"]) == 1

    def test_multi_item_under_100_no_truncation(self):
        """Test multiple items under 100 are not truncated."""
        client = MockEasyPostClient()

        # Create 50 items with low values ($1 each, cumulative qty 1+2+...+50=1275 × $1 = $1,275)
        items = " ".join([f"({i}) Item{i} ($1 each)" for i in range(1, 51)])
        contents = f"{items} HTS: 6203.42.4011"

        result = extract_customs_smart(
            contents=contents,
            weight_oz=800.0,
            easypost_client=client,
        )

        assert result is not None
        assert len(result["customs_items"]) == 50

    def test_multi_item_exactly_100_no_truncation(self):
        """Test exactly 100 items are allowed."""
        client = MockEasyPostClient()

        # Create 100 items with eel_pfc for high cumulative value
        items = " ".join([f"({i}) Item{i} ($1 each)" for i in range(1, 101)])
        contents = f"{items} HTS: 6203.42.4011"

        result = extract_customs_smart(
            contents=contents,
            weight_oz=1600.0,
            easypost_client=client,
            eel_pfc="AES X20120502123456",  # Required (cumulative qty × $1 = $5,050)
        )

        assert result is not None
        assert len(result["customs_items"]) == 100

    def test_multi_item_over_100_truncated(self):
        """Test items over 100 are truncated with warning."""
        client = MockEasyPostClient()

        # Create 150 items (exceeds UPS limit)
        items = " ".join([f"({i}) Item{i} ($1 each)" for i in range(1, 151)])
        contents = f"{items} HTS: 6203.42.4011"

        result = extract_customs_smart(
            contents=contents,
            weight_oz=2400.0,
            easypost_client=client,
            eel_pfc="AES X20120502123456",  # Required for high cumulative value
        )

        assert result is not None
        # Should be truncated to 100
        assert len(result["customs_items"]) == 100


class TestOptionalFields:
    """Test optional contents_explanation and restriction_comments fields."""

    def test_contents_explanation_passed_through(self):
        """Test contents_explanation is passed to CustomsInfo."""
        client = MockEasyPostClient()

        result = extract_customs_smart(
            contents="(1) Special Item HTS: 6203.42.4011 ($50)",
            weight_oz=16.0,
            easypost_client=client,
            contents_explanation="Custom handmade product",
        )

        assert result is not None
        assert result["contents_explanation"] == "Custom handmade product"

    def test_restriction_comments_passed_through(self):
        """Test restriction_comments is passed to CustomsInfo."""
        client = MockEasyPostClient()

        result = extract_customs_smart(
            contents="(1) Medical Item HTS: 6203.42.4011 ($50)",
            weight_oz=16.0,
            easypost_client=client,
            restriction_comments="Requires refrigeration",
        )

        assert result is not None
        assert result["restriction_comments"] == "Requires refrigeration"

    def test_optional_fields_default_to_empty(self):
        """Test optional fields default to empty string when not provided."""
        client = MockEasyPostClient()

        result = extract_customs_smart(
            contents="(1) Regular Item HTS: 6203.42.4011 ($50)",
            weight_oz=16.0,
            easypost_client=client,
        )

        assert result is not None
        # Should have keys with empty values
        assert result.get("contents_explanation") == ""
        assert result.get("restriction_comments") == ""


class TestIntegrationEasyPostGuide:
    """Integration tests matching EasyPost customs guide examples."""

    def test_tshirt_to_uk_example(self):
        """Test T-shirt to UK example from EasyPost guide."""
        client = MockEasyPostClient()

        # From guide: T-shirt valued at $10
        result = extract_customs_smart(
            contents="(1) T-shirt HTS: 6109.10.0012 ($10)",
            weight_oz=5.0,
            easypost_client=client,
            customs_signer="Steve Brule",  # From guide example
        )

        assert result is not None
        assert result["customs_certify"] is True
        assert result["customs_signer"] == "Steve Brule"
        assert result["contents_type"] == "merchandise"
        assert result["restriction_type"] == "none"
        assert result["eel_pfc"] == "NOEEI 30.37(a)"  # Value < $2,500
        assert result["non_delivery_option"] == "return"
        assert len(result["customs_items"]) == 1

    def test_high_value_electronics_requires_itn(self):
        """Test high-value electronics shipment requires ITN."""
        client = MockEasyPostClient()

        # High-value electronics (common scenario)
        with pytest.raises(ValueError) as excinfo:
            extract_customs_smart(
                contents="(2) Professional Cameras HTS: 8525.80.5000 ($2000 each)",
                weight_oz=80.0,
                easypost_client=client,
                customs_signer="John Doe",
            )

        error_msg = str(excinfo.value)
        assert "4000.00" in error_msg  # 2 items @ $2,000 = $4,000
        assert "AES ITN" in error_msg
