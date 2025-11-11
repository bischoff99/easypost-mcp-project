"""Unit tests for smart customs generation."""

from src.services.smart_customs import (
    HTS_CODE_PATTERNS,
    VALUE_ESTIMATES,
    calculate_item_weight,
    detect_hs_code_from_description,
    estimate_believable_value,
)


class TestCalculateItemWeight:
    """Test calculate_item_weight function."""

    def test_typical_weight(self):
        """Test typical parcel weight calculation."""
        # 10 oz parcel -> 8.8 oz item (88%)
        result = calculate_item_weight(10.0)
        assert result == 8.8
        assert isinstance(result, float)

    def test_light_weight(self):
        """Test light weight parcel."""
        result = calculate_item_weight(1.0)
        assert result == 0.9  # 88% of 1 oz, rounded to 1 decimal

    def test_heavy_weight(self):
        """Test heavy weight parcel."""
        result = calculate_item_weight(160.0)  # 10 lbs
        expected = 160.0 * 0.88
        assert result == round(expected, 1)

    def test_zero_weight(self):
        """Test zero weight edge case."""
        result = calculate_item_weight(0.0)
        assert result == 0.0

    def test_decimal_precision(self):
        """Test result is rounded to 1 decimal place."""
        result = calculate_item_weight(3.333)
        assert isinstance(result, float)
        # Check it's rounded to 1 decimal
        assert result == round(3.333 * 0.88, 1)


class TestEstimateBelievableValue:
    """Test estimate_believable_value function."""

    def test_jeans_default_value(self):
        """Test default jeans value."""
        result = estimate_believable_value(16.0, "jeans")  # 1 lb
        assert result == 25.0  # Default jeans value

    def test_pillow_value(self):
        """Test pillow value estimation."""
        result = estimate_believable_value(20.0, "pillow")
        assert result == 38.0  # Pillow base value

    def test_electronics_value(self):
        """Test electronics (high value) estimation."""
        result = estimate_believable_value(16.0, "phone")
        assert result == 300.0  # Phone base value

    def test_heavy_parcel_scaling(self):
        """Test heavy parcel gets higher value estimate."""
        # Heavy parcel (> 10 lbs) gets scaled up
        result = estimate_believable_value(200.0, "default")  # ~12.5 lbs
        assert result >= 25.0  # Should be at least base value
        assert result <= 200.0  # Should be within reasonable range

    def test_unknown_category_uses_default(self):
        """Test unknown category falls back to default."""
        result = estimate_believable_value(16.0, "unknown_category")
        assert result == 25.0  # Default value

    def test_zero_weight(self):
        """Test zero weight edge case."""
        result = estimate_believable_value(0.0, "jeans")
        assert result >= 0

    def test_return_type(self):
        """Test return value is numeric (int or float)."""
        result = estimate_believable_value(16.0, "jeans")
        assert isinstance(result, (int, float))

    def test_light_weight_uses_base_value(self):
        """Test light weight (< 2 lbs) uses base value."""
        result = estimate_believable_value(16.0, "jeans")  # 1 lb
        assert result == 25.0  # Exactly base value, no scaling

    def test_medium_weight_scaling(self):
        """Test medium weight (2-10 lbs) scales proportionally."""
        result = estimate_believable_value(80.0, "jeans")  # 5 lbs
        # Should be scaled: 25 * (1 + (5-2)*0.2) = 25 * 1.6 = 40
        assert result == 40.0

    def test_heavy_weight_capped_scaling(self):
        """Test heavy weight (> 10 lbs) caps at 3x base value."""
        result = estimate_believable_value(320.0, "jeans")  # 20 lbs
        # Should be capped at reasonable value
        assert result <= 75.0  # Max 3x base value


class TestDetectHSCodeFromDescription:
    """Test detect_hs_code_from_description function."""

    def test_pillow_detection(self):
        """Test pillow keyword detection."""
        hs_code, description, value = detect_hs_code_from_description("Memory foam pillow")
        assert hs_code == HTS_CODE_PATTERNS["pillow"][0]
        assert "Pillow" in description
        assert value == VALUE_ESTIMATES["pillow"]

    def test_jeans_detection(self):
        """Test jeans keyword detection."""
        hs_code, description, value = detect_hs_code_from_description("Denim jeans")
        assert hs_code == HTS_CODE_PATTERNS["jeans"][0]
        assert "Jeans" in description or "jeans" in description.lower()
        assert value == VALUE_ESTIMATES["jeans"]

    def test_phone_detection(self):
        """Test phone detection."""
        hs_code, description, value = detect_hs_code_from_description("Mobile phone")
        assert hs_code == HTS_CODE_PATTERNS["phone"][0]
        assert value == VALUE_ESTIMATES["phone"]

    def test_cosmetic_detection(self):
        """Test cosmetic product detection."""
        hs_code, description, value = detect_hs_code_from_description("Cosmetic product")
        # Should match cosmetic pattern
        assert hs_code == HTS_CODE_PATTERNS["cosmetic"][0]

    def test_fishing_equipment_detection(self):
        """Test fishing equipment detection."""
        hs_code, description, value = detect_hs_code_from_description("Fishing rod")
        assert hs_code == HTS_CODE_PATTERNS["fishing"][0]
        assert value == VALUE_ESTIMATES["fishing"]

    def test_coffee_detection(self):
        """Test coffee detection."""
        hs_code, description, value = detect_hs_code_from_description("Ground coffee")
        assert hs_code == HTS_CODE_PATTERNS["coffee"][0]

    def test_no_match_returns_default(self):
        """Test unknown description returns default (jeans)."""
        hs_code, description, value = detect_hs_code_from_description("Unknown product xyz123")
        assert hs_code == HTS_CODE_PATTERNS["default"][0]
        assert value == VALUE_ESTIMATES["default"]

    def test_empty_description(self):
        """Test empty description returns default."""
        hs_code, description, value = detect_hs_code_from_description("")
        assert hs_code == HTS_CODE_PATTERNS["default"][0]
        assert value == VALUE_ESTIMATES["default"]

    def test_case_insensitive(self):
        """Test keyword matching is case-insensitive."""
        hs_code1, _, _ = detect_hs_code_from_description("PILLOW")
        hs_code2, _, _ = detect_hs_code_from_description("pillow")
        hs_code3, _, _ = detect_hs_code_from_description("PiLLoW")
        assert hs_code1 == hs_code2 == hs_code3

    def test_returns_tuple(self):
        """Test function returns tuple of (code, description, value)."""
        result = detect_hs_code_from_description("Shirt")
        assert isinstance(result, tuple)
        assert len(result) == 3
        hs_code, description, value = result
        assert isinstance(hs_code, str)
        assert isinstance(description, str)
        assert isinstance(value, (int, float))

    def test_multiple_keywords_matches_first(self):
        """Test description with multiple keywords matches first found."""
        # "fishing" comes before "rod" in the patterns
        hs_code, _, _ = detect_hs_code_from_description("Fishing rod")
        # Should match fishing pattern
        assert hs_code in [HTS_CODE_PATTERNS["fishing"][0], HTS_CODE_PATTERNS["default"][0]]


class TestHTSCodePatterns:
    """Test HTS code database completeness."""

    def test_all_patterns_have_tuples(self):
        """Test all HTS patterns are (code, description) tuples."""
        for _key, value in HTS_CODE_PATTERNS.items():
            assert isinstance(value, tuple)
            assert len(value) == 2
            code, description = value
            assert isinstance(code, str)
            assert isinstance(description, str)

    def test_hts_codes_valid_format(self):
        """Test HTS codes have valid format (10 digits with periods)."""
        for key, (code, _description) in HTS_CODE_PATTERNS.items():
            digits_only = code.replace(".", "")
            assert len(digits_only) == 10, f"Invalid HTS code for {key}: {code}"
            assert digits_only.isdigit(), f"HTS code contains non-digits for {key}: {code}"

    def test_default_exists(self):
        """Test default fallback pattern exists."""
        assert "default" in HTS_CODE_PATTERNS
        code, description = HTS_CODE_PATTERNS["default"]
        assert code == "6203.42.4011"  # Jeans as default
        assert "Jeans" in description

    def test_common_categories_covered(self):
        """Test common shipping categories are covered."""
        common_categories = ["pillow", "jeans", "phone", "coffee", "cosmetic"]
        for category in common_categories:
            assert category in HTS_CODE_PATTERNS, f"Missing common category: {category}"


class TestValueEstimates:
    """Test value estimates database."""

    def test_all_values_positive(self):
        """Test all value estimates are positive."""
        for category, value in VALUE_ESTIMATES.items():
            assert value > 0, f"Invalid value for {category}: {value}"
            assert isinstance(value, (int, float))

    def test_default_exists(self):
        """Test default value estimate exists."""
        assert "default" in VALUE_ESTIMATES
        assert VALUE_ESTIMATES["default"] == 25  # Jeans price

    def test_reasonable_value_ranges(self):
        """Test value estimates are in reasonable ranges."""
        for category, value in VALUE_ESTIMATES.items():
            # All values should be between $10 and $1000 for believability
            assert 10 <= value <= 1000, f"Unrealistic value for {category}: {value}"

    def test_electronics_higher_value(self):
        """Test electronics have higher value estimates."""
        electronics = ["phone", "tablet"]
        for item in electronics:
            if item in VALUE_ESTIMATES:
                assert VALUE_ESTIMATES[item] >= 200, f"{item} should have high value"


class TestIntegration:
    """Integration tests combining multiple functions."""

    def test_typical_customs_workflow(self):
        """Test typical workflow: detect code, calculate weight, estimate value."""
        # Simulate creating customs info for a pillow shipment
        description = "Memory foam pillow"
        parcel_weight = 20.0  # oz

        # Step 1: Detect HTS code
        hs_code, clean_desc, base_value = detect_hs_code_from_description(description)
        assert hs_code == HTS_CODE_PATTERNS["pillow"][0]

        # Step 2: Calculate item weight
        item_weight = calculate_item_weight(parcel_weight)
        assert item_weight == 17.6  # 88% of 20 oz

        # Step 3: Estimate value
        value = estimate_believable_value(parcel_weight, "pillow")
        assert value == 38.0  # Pillow base value (light weight)

    def test_heavy_electronics_workflow(self):
        """Test workflow for heavy electronics."""
        description = "Tablet computer"
        parcel_weight = 80.0  # 5 lbs

        # Detect
        hs_code, clean_desc, base_value = detect_hs_code_from_description(description)
        assert hs_code == HTS_CODE_PATTERNS["tablet"][0]

        # Weight
        item_weight = calculate_item_weight(parcel_weight)
        assert item_weight == 70.4  # 88% of 80 oz

        # Value should be scaled up for heavier item
        value = estimate_believable_value(parcel_weight, "tablet")
        assert value > base_value  # Should be scaled for 5 lbs

    def test_unknown_item_workflow(self):
        """Test workflow for unknown item type."""
        description = "Custom handmade product"
        parcel_weight = 32.0  # 2 lbs

        # Should fall back to default (jeans)
        hs_code, clean_desc, base_value = detect_hs_code_from_description(description)
        assert hs_code == HTS_CODE_PATTERNS["default"][0]
        assert base_value == VALUE_ESTIMATES["default"]

        # Weight calculation still works
        item_weight = calculate_item_weight(parcel_weight)
        assert item_weight == 28.2  # 88% of 32 oz

        # Value uses default
        value = estimate_believable_value(parcel_weight, "default")
        assert value == 25.0  # Exactly 2 lbs, no scaling yet
