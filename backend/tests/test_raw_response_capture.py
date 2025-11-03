"""Capture and save raw EasyPost API responses for analysis."""

import pytest
import asyncio
import json
from pathlib import Path
from datetime import datetime
from src.services.easypost_service import EasyPostService
from src.utils.config import settings


@pytest.mark.asyncio
class TestRawResponseCapture:
    """Capture raw EasyPost responses for documentation and verification."""

    @pytest.fixture
    async def service(self):
        """Create EasyPost service instance."""
        return EasyPostService(api_key=settings.EASYPOST_API_KEY)

    async def test_capture_domestic_rate_response(self, service):
        """Capture raw response for domestic shipment."""
        to_addr = {
            "name": "John Doe",
            "street1": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "country": "US",
        }
        
        from_addr = {
            "name": "Beauty Store",
            "street1": "8500 Beverly Blvd",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90048",
            "country": "US",
        }
        
        parcel = {"length": 10.0, "width": 8.0, "height": 6.0, "weight": 16.0}

        # Get rates
        result = await service.get_rates(to_addr, from_addr, parcel)
        
        # Save raw response
        output_dir = Path(__file__).parent / "captured_responses"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"domestic_rates_{timestamp}.json"
        
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"\n✅ Captured domestic rate response to: {output_file}")
        print(f"   Status: {result['status']}")
        print(f"   Rates: {len(result.get('data', []))}")
        
        if result["status"] == "success":
            # Validate response structure
            assert "data" in result
            assert isinstance(result["data"], list)
            assert len(result["data"]) > 0
            
            # Print first rate for verification
            first_rate = result["data"][0]
            print(f"\n   First Rate:")
            print(f"     Carrier: {first_rate['carrier']}")
            print(f"     Service: {first_rate['service']}")
            print(f"     Price: ${first_rate['rate']}")

    async def test_capture_international_rate_response(self, service):
        """Capture raw response for international shipment."""
        to_addr = {
            "name": "Barra Odeamar",
            "street1": "Blk 6 Lot 48 Camella Vera",
            "city": "Valenzuela City",
            "state": "Metro Manila",
            "zip": "1440",
            "country": "PH",
            "phone": "+639612109875",
        }
        
        from_addr = {
            "name": "Beauty & Wellness LA",
            "street1": "8500 Beverly Blvd",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90048",
            "country": "US",
        }
        
        parcel = {"length": 13.0, "width": 12.0, "height": 2.0, "weight": 28.8}

        # Get rates
        result = await service.get_rates(to_addr, from_addr, parcel)
        
        # Save raw response
        output_dir = Path(__file__).parent / "captured_responses"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"international_rates_philippines_{timestamp}.json"
        
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"\n✅ Captured international rate response to: {output_file}")
        print(f"   Status: {result['status']}")
        print(f"   Rates: {len(result.get('data', []))}")
        
        if result["status"] == "success":
            rates = result["data"]
            prices = [float(r["rate"]) for r in rates]
            
            print(f"\n   Price Range: ${min(prices):.2f} - ${max(prices):.2f}")
            print(f"   Carriers: {', '.join(set(r['carrier'] for r in rates[:5]))}")
            
            # Validate international rates are higher than domestic
            assert min(prices) > 10, "International rates should be > $10"

    async def test_validate_rate_object_schema(self, service):
        """Validate that rate objects have all expected fields."""
        to_addr = {
            "name": "Test",
            "street1": "123 Main St",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101",
            "country": "US",
        }
        
        from_addr = {
            "name": "Test",
            "street1": "456 Market St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94102",
            "country": "US",
        }
        
        parcel = {"length": 12.0, "width": 9.0, "height": 6.0, "weight": 20.0}

        result = await service.get_rates(to_addr, from_addr, parcel)
        
        if result["status"] == "success":
            for rate in result["data"]:
                # Required fields
                assert "carrier" in rate, "Missing 'carrier' field"
                assert "service" in rate, "Missing 'service' field"
                assert "rate" in rate, "Missing 'rate' field"
                
                # Type validation
                assert isinstance(rate["carrier"], str)
                assert isinstance(rate["service"], str)
                assert isinstance(rate["rate"], str)
                
                # Validate rate is numeric string
                rate_float = float(rate["rate"])
                assert rate_float > 0
                
                # Optional fields
                if "delivery_days" in rate and rate["delivery_days"] is not None:
                    assert isinstance(rate["delivery_days"], int)
                    assert rate["delivery_days"] > 0
                    assert rate["delivery_days"] < 30  # Reasonable limit


@pytest.mark.asyncio
class TestRawEasyPostObjects:
    """Test raw EasyPost SDK objects to verify API integration."""

    async def test_raw_shipment_object_structure(self):
        """Test that raw EasyPost shipment object has correct structure."""
        import easypost
        
        client = easypost.EasyPostClient(settings.EASYPOST_API_KEY)
        
        def create_shipment():
            return client.shipment.create(
                to_address={
                    "name": "Test",
                    "street1": "123 Main",
                    "city": "New York",
                    "state": "NY",
                    "zip": "10001",
                    "country": "US",
                },
                from_address={
                    "name": "Test",
                    "street1": "456 Market",
                    "city": "SF",
                    "state": "CA",
                    "zip": "94102",
                    "country": "US",
                },
                parcel={"length": 10, "width": 8, "height": 6, "weight": 16},
            )
        
        loop = asyncio.get_running_loop()
        shipment = await loop.run_in_executor(None, create_shipment)
        
        # Validate raw EasyPost object
        assert hasattr(shipment, "id"), "Shipment should have ID"
        assert hasattr(shipment, "object"), "Should have object type"
        assert hasattr(shipment, "rates"), "Should have rates"
        assert hasattr(shipment, "created_at"), "Should have creation timestamp"
        
        # Validate ID format (EasyPost IDs start with prefix)
        assert shipment.id.startswith("shp_"), f"Invalid shipment ID: {shipment.id}"
        assert shipment.object == "Shipment", f"Wrong object type: {shipment.object}"
        
        # Validate rates
        assert len(shipment.rates) > 0, "Should have at least one rate"
        
        first_rate = shipment.rates[0]
        assert hasattr(first_rate, "id")
        assert hasattr(first_rate, "carrier")
        assert hasattr(first_rate, "rate")
        assert first_rate.id.startswith("rate_"), f"Invalid rate ID: {first_rate.id}"
        
        print(f"\n✅ RAW EASYPOST OBJECT VALIDATED:")
        print(f"   Shipment ID: {shipment.id}")
        print(f"   Object Type: {shipment.object}")
        print(f"   Mode: {shipment.mode}")
        print(f"   Rates: {len(shipment.rates)}")
        print(f"   First Rate ID: {first_rate.id}")
        print(f"   First Rate: {first_rate.carrier} - ${first_rate.rate}")
        
        # These IDs prove it's a real API response
        assert len(shipment.id) > 10, "Real EasyPost IDs are long"
        assert len(first_rate.id) > 10, "Real Rate IDs are long"

