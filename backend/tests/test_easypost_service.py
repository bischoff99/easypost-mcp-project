import pytest

from src.services.easypost_service import (
    AddressModel,
    EasyPostService,
    ParcelModel,
    ShipmentResponse,
)


class TestModels:
    """Test Pydantic models for validation."""

    def test_address_model_valid(self):
        """Test valid address creation."""
        addr = AddressModel(
            name="Test User", street1="123 Test St", city="Test City", state="CA", zip="12345"
        )
        assert addr.country == "US"
        assert addr.name == "Test User"

    def test_address_model_custom_country(self):
        """Test address with custom country."""
        addr = AddressModel(
            name="Test User",
            street1="123 Test St",
            city="Toronto",
            state="ON",
            zip="M5H 2N2",
            country="CA",
        )
        assert addr.country == "CA"

    def test_parcel_model_valid(self):
        """Test valid parcel creation."""
        parcel = ParcelModel(length=10.0, width=8.0, height=5.0, weight=2.0)
        assert parcel.length == 10.0
        assert parcel.weight == 2.0

    def test_parcel_model_invalid_dimensions(self):
        """Test parcel with invalid (negative) dimensions."""
        with pytest.raises(ValueError):
            ParcelModel(length=-1.0, width=8.0, height=5.0, weight=2.0)

    def test_parcel_model_zero_dimensions(self):
        """Test parcel with zero dimensions (should fail)."""
        with pytest.raises(ValueError):
            ParcelModel(length=0, width=8.0, height=5.0, weight=2.0)

    def test_shipment_response_success(self):
        """Test successful shipment response."""
        response = ShipmentResponse(
            status="success",
            shipment_id="shp_123",
            tracking_number="EZ1000000001",
            label_url="https://example.com/label.pdf",
            rate="10.50",
            carrier="USPS",
        )
        assert response.status == "success"
        assert response.error is None

    def test_shipment_response_error(self):
        """Test error shipment response."""
        response = ShipmentResponse(status="error", error="Invalid API key")
        assert response.status == "error"
        assert response.shipment_id is None


class TestEasyPostService:
    """Test EasyPostService methods."""

    def test_sanitize_error_truncates_long_messages(self):
        """Test error message sanitization."""
        service = EasyPostService(api_key="test_key")
        long_error = Exception("x" * 300)
        sanitized = service._sanitize_error(long_error)
        assert len(sanitized) <= 203  # 200 + "..."
        assert sanitized.endswith("...")

    def test_sanitize_error_keeps_short_messages(self):
        """Test short error messages stay unchanged."""
        service = EasyPostService(api_key="test_key")
        short_error = Exception("Short error message")
        sanitized = service._sanitize_error(short_error)
        assert sanitized == "Short error message"

    @pytest.mark.asyncio
    async def test_get_shipments_list_success(self):
        """Test successful shipment list retrieval."""
        service = EasyPostService(api_key="test_key")

        # Mock the synchronous method
        mock_result = {
            "status": "success",
            "data": [
                {
                    "id": "shp_test1",
                    "tracking_number": "9400111899223345",
                    "status": "delivered",
                    "created_at": "2024-01-01T00:00:00Z",
                    "carrier": "USPS",
                    "service": "Priority",
                    "rate": "10.50",
                }
            ],
            "message": "Successfully retrieved 1 shipments",
            "has_more": False,
            "timestamp": "2024-01-01T00:00:00Z",
        }

        # Mock the sync method
        service._get_shipments_list_sync = lambda *args, **kwargs: mock_result

        result = await service.get_shipments_list(page_size=10, purchased=True)

        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == "shp_test1"
        assert result["data"][0]["carrier"] == "USPS"

    @pytest.mark.asyncio
    async def test_get_shipments_list_error(self):
        """Test shipment list retrieval error handling."""
        service = EasyPostService(api_key="test_key")

        # Mock the sync method to raise an exception
        service._get_shipments_list_sync = lambda *args, **kwargs: (_ for _ in ()).throw(
            Exception("API Error")
        )

        result = await service.get_shipments_list(page_size=10)

        assert result["status"] == "error"
        assert result["data"] == []
        assert "Failed to retrieve shipments list" in result["message"]


# Integration tests would require actual EasyPost API key
# and should be run separately with @pytest.mark.integration
