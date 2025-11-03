"""Live API validation tests for EasyPost integration."""

from datetime import datetime

import pytest

from src.services.easypost_service import EasyPostService
from src.utils.config import settings


@pytest.mark.asyncio
class TestLiveEasyPostAPI:
    """Test actual EasyPost API calls and validate responses."""

    @pytest.fixture
    async def service(self):
        """Create EasyPost service instance."""
        return EasyPostService(api_key=settings.EASYPOST_API_KEY)

    @pytest.fixture
    def domestic_addresses(self):
        """Sample domestic US addresses."""
        return {
            "to_address": {
                "name": "John Doe",
                "street1": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip": "10001",
                "country": "US",
            },
            "from_address": {
                "name": "Beauty & Wellness LA",
                "street1": "8500 Beverly Blvd",
                "city": "Los Angeles",
                "state": "CA",
                "zip": "90048",
                "country": "US",
            },
        }

    @pytest.fixture
    def international_addresses(self):
        """Sample international addresses."""
        return {
            "to_address": {
                "name": "Barra Odeamar",
                "street1": "Blk 6 Lot 48 Camella Vera",
                "city": "Valenzuela City",
                "state": "Metro Manila",
                "zip": "1440",
                "country": "PH",
                "phone": "+639612109875",
            },
            "from_address": {
                "name": "Beauty & Wellness LA",
                "street1": "8500 Beverly Blvd",
                "city": "Los Angeles",
                "state": "CA",
                "zip": "90048",
                "country": "US",
            },
        }

    @pytest.fixture
    def standard_parcel(self):
        """Standard parcel dimensions."""
        return {"length": 10.0, "width": 8.0, "height": 6.0, "weight": 16.0}

    async def test_live_rates_response_structure(
        self, service, domestic_addresses, standard_parcel
    ):
        """Test that live API returns properly structured response."""
        result = await service.get_rates(
            domestic_addresses["to_address"],
            domestic_addresses["from_address"],
            standard_parcel,
        )

        # Validate response structure
        assert result["status"] in ["success", "error"]
        assert "data" in result
        assert "message" in result
        assert "timestamp" in result

        # If successful, validate data structure
        if result["status"] == "success":
            rates = result["data"]
            assert isinstance(rates, list)
            assert len(rates) > 0, "Should return at least one rate"

            # Validate each rate object
            for rate in rates:
                assert "carrier" in rate
                assert "service" in rate
                assert "rate" in rate
                assert isinstance(rate["carrier"], str)
                assert isinstance(rate["service"], str)
                assert isinstance(rate["rate"], str)

                # Rate should be a valid number
                rate_value = float(rate["rate"])
                assert rate_value > 0, f"Rate should be positive, got {rate_value}"

    async def test_live_rates_has_real_carriers(self, service, domestic_addresses, standard_parcel):
        """Test that real carriers are returned."""
        result = await service.get_rates(
            domestic_addresses["to_address"],
            domestic_addresses["from_address"],
            standard_parcel,
        )

        if result["status"] == "success":
            carriers = [r["carrier"] for r in result["data"]]

            # Should have common carriers
            carrier_set = set(carriers)
            common_carriers = {"USPS", "UPS", "FedEx", "FedExDefault", "UPSDAP"}

            assert (
                len(carrier_set.intersection(common_carriers)) > 0
            ), f"Expected common carriers, got: {carrier_set}"

    async def test_live_rates_realistic_pricing(self, service, domestic_addresses, standard_parcel):
        """Test that returned rates are realistic."""
        result = await service.get_rates(
            domestic_addresses["to_address"],
            domestic_addresses["from_address"],
            standard_parcel,
        )

        if result["status"] == "success":
            rates = result["data"]

            # Extract prices
            prices = [float(r["rate"]) for r in rates]

            # Domestic shipping should be reasonable
            assert all(p > 0 for p in prices), "All rates should be positive"
            assert all(p < 200 for p in prices), "Domestic rates should be < $200"
            assert min(prices) < 50, "Should have economy option < $50"

    async def test_live_international_rates(
        self, service, international_addresses, standard_parcel
    ):
        """Test international shipping rates."""
        result = await service.get_rates(
            international_addresses["to_address"],
            international_addresses["from_address"],
            standard_parcel,
        )

        if result["status"] == "success":
            rates = result["data"]

            assert len(rates) > 0, "Should return international rates"

            # International should be more expensive than domestic
            prices = [float(r["rate"]) for r in rates]
            assert min(prices) > 10, "International minimum should be > $10"

            # Should have USPS international options
            carriers = [r["carrier"] for r in rates]
            assert any(
                "USPS" in c or "USA" in c for c in carriers
            ), "Should have USPS international options"

    async def test_rate_response_has_delivery_info(
        self, service, domestic_addresses, standard_parcel
    ):
        """Test that rates include delivery information."""
        result = await service.get_rates(
            domestic_addresses["to_address"],
            domestic_addresses["from_address"],
            standard_parcel,
        )

        if result["status"] == "success" and result["data"]:
            # Check if delivery info is present in at least some rates
            has_delivery_days = any(r.get("delivery_days") is not None for r in result["data"])
            has_delivery_date = any(r.get("delivery_date") is not None for r in result["data"])

            # At least one type of delivery info should be present
            assert has_delivery_days or has_delivery_date, "Rates should include delivery estimates"

    async def test_invalid_country_code_validation(self, service, standard_parcel):
        """Test that invalid country codes are properly rejected."""
        invalid_address = {
            "name": "Test",
            "street1": "123 Main",
            "city": "City",
            "state": "State",
            "zip": "12345",
            "country": "Netherland",  # Invalid - should be NL or Netherlands
        }

        from_address = {
            "name": "Test",
            "street1": "456 Market",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90001",
            "country": "US",
        }

        result = await service.get_rates(invalid_address, from_address, standard_parcel)

        # Should return error (either from validation or EasyPost)
        assert result["status"] == "error" or len(result.get("data", [])) == 0

    async def test_timestamp_format(self, service, domestic_addresses, standard_parcel):
        """Test that timestamp is in ISO format."""
        result = await service.get_rates(
            domestic_addresses["to_address"],
            domestic_addresses["from_address"],
            standard_parcel,
        )

        # Validate timestamp format
        timestamp = result["timestamp"]
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            assert dt is not None
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {timestamp}")

    async def test_multiple_carriers_returned(self, service, domestic_addresses, standard_parcel):
        """Test that multiple carrier options are returned."""
        result = await service.get_rates(
            domestic_addresses["to_address"],
            domestic_addresses["from_address"],
            standard_parcel,
        )

        if result["status"] == "success":
            carriers = list(set(r["carrier"] for r in result["data"]))

            # Should have multiple carriers for domestic US
            assert len(carriers) >= 2, f"Expected multiple carriers, got: {carriers}"

    async def test_rate_consistency(self, service, domestic_addresses, standard_parcel):
        """Test that calling API twice returns consistent carrier options."""
        result1 = await service.get_rates(
            domestic_addresses["to_address"],
            domestic_addresses["from_address"],
            standard_parcel,
        )

        result2 = await service.get_rates(
            domestic_addresses["to_address"],
            domestic_addresses["from_address"],
            standard_parcel,
        )

        if result1["status"] == "success" and result2["status"] == "success":
            carriers1 = set(r["carrier"] for r in result1["data"])
            carriers2 = set(r["carrier"] for r in result2["data"])

            # Should return same carriers (rates may vary slightly)
            assert carriers1 == carriers2, "Carriers should be consistent"
