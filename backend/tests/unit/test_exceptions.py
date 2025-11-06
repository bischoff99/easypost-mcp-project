"""Unit tests for custom exceptions."""

import pytest

from src.exceptions import (
    BulkOperationError,
    DatabaseConnectionError,
    EasyPostMCPError,
    InvalidAddressError,
    RateLimitExceededError,
    ShipmentCreationError,
    TrackingNotFoundError,
)


class TestEasyPostMCPError:
    """Test base EasyPostMCPError."""

    def test_basic_exception(self):
        """Test basic exception creation."""
        exc = EasyPostMCPError("Test error")
        assert str(exc) == "Test error"
        assert exc.message == "Test error"
        assert exc.details == {}

    def test_exception_with_details(self):
        """Test exception with details dict."""
        details = {"field": "email", "reason": "invalid format"}
        exc = EasyPostMCPError("Validation failed", details=details)
        assert exc.message == "Validation failed"
        assert exc.details == details
        assert exc.details["field"] == "email"

    def test_exception_repr(self):
        """Test exception string representation."""
        exc = EasyPostMCPError("Test error")
        assert "Test error" in str(exc)


class TestShipmentCreationError:
    """Test ShipmentCreationError."""

    def test_without_shipment_data(self):
        """Test error without shipment data."""
        exc = ShipmentCreationError("Failed to create shipment")
        assert exc.message == "Failed to create shipment"
        assert exc.shipment_data is None
        assert "shipment_data" in exc.details

    def test_with_shipment_data(self):
        """Test error with shipment data."""
        shipment_data = {"from_address": {"city": "LA"}, "to_address": {"city": "NYC"}}
        exc = ShipmentCreationError("Failed", shipment_data=shipment_data)
        assert exc.shipment_data == shipment_data
        assert exc.details["shipment_data"] == shipment_data

    def test_inheritance(self):
        """Test ShipmentCreationError inherits from base."""
        exc = ShipmentCreationError("Test")
        assert isinstance(exc, EasyPostMCPError)
        assert isinstance(exc, Exception)


class TestRateLimitExceededError:
    """Test RateLimitExceededError."""

    def test_without_retry_after(self):
        """Test rate limit error without retry time."""
        exc = RateLimitExceededError()
        assert "rate limit exceeded" in exc.message.lower()
        assert exc.retry_after is None

    def test_with_retry_after(self):
        """Test rate limit error with retry time."""
        exc = RateLimitExceededError(retry_after=60)
        assert "60 seconds" in exc.message
        assert exc.retry_after == 60
        assert exc.details["retry_after"] == 60

    def test_inheritance(self):
        """Test RateLimitExceededError inherits from base."""
        exc = RateLimitExceededError()
        assert isinstance(exc, EasyPostMCPError)


class TestTrackingNotFoundError:
    """Test TrackingNotFoundError."""

    def test_tracking_error(self):
        """Test tracking not found error."""
        tracking_number = "EZ1234567890"
        exc = TrackingNotFoundError(tracking_number)
        assert tracking_number in exc.message
        assert exc.tracking_number == tracking_number
        assert exc.details["tracking_number"] == tracking_number

    def test_error_message_format(self):
        """Test error message includes tracking number."""
        exc = TrackingNotFoundError("TRACK123")
        assert "TRACK123" in str(exc)
        assert "not found" in exc.message.lower()

    def test_inheritance(self):
        """Test TrackingNotFoundError inherits from base."""
        exc = TrackingNotFoundError("TEST")
        assert isinstance(exc, EasyPostMCPError)


class TestInvalidAddressError:
    """Test InvalidAddressError."""

    def test_without_address_data(self):
        """Test error without address data."""
        exc = InvalidAddressError("Invalid address format")
        assert exc.message == "Invalid address format"
        assert exc.address_data is None

    def test_with_address_data(self):
        """Test error with address data."""
        address_data = {"street1": "123 Main", "city": "LA"}
        exc = InvalidAddressError("Invalid zip code", address_data=address_data)
        assert exc.address_data == address_data
        assert exc.details["address_data"] == address_data

    def test_inheritance(self):
        """Test InvalidAddressError inherits from base."""
        exc = InvalidAddressError("Test")
        assert isinstance(exc, EasyPostMCPError)


class TestDatabaseConnectionError:
    """Test DatabaseConnectionError."""

    def test_database_error(self):
        """Test database connection error."""
        exc = DatabaseConnectionError("Connection refused")
        assert exc.message == "Connection refused"
        assert exc.details == {}

    def test_inheritance(self):
        """Test DatabaseConnectionError inherits from base."""
        exc = DatabaseConnectionError("Test")
        assert isinstance(exc, EasyPostMCPError)


class TestBulkOperationError:
    """Test BulkOperationError."""

    def test_without_failed_items(self):
        """Test bulk operation error without failed items."""
        exc = BulkOperationError("Bulk operation failed")
        assert exc.message == "Bulk operation failed"
        assert exc.failed_items == []
        assert exc.success_count == 0

    def test_with_failed_items(self):
        """Test bulk operation error with failed items."""
        failed_items = [{"id": "1", "error": "timeout"}, {"id": "2", "error": "invalid"}]
        exc = BulkOperationError("Partial failure", failed_items=failed_items, success_count=8)
        assert exc.failed_items == failed_items
        assert exc.success_count == 8
        assert exc.details["failed_items"] == failed_items
        assert exc.details["success_count"] == 8

    def test_inheritance(self):
        """Test BulkOperationError inherits from base."""
        exc = BulkOperationError("Test")
        assert isinstance(exc, EasyPostMCPError)


class TestExceptionRaising:
    """Test that exceptions can be raised and caught."""

    def test_raise_shipment_creation_error(self):
        """Test raising and catching ShipmentCreationError."""
        with pytest.raises(ShipmentCreationError) as exc_info:
            raise ShipmentCreationError("Failed to create")

        assert "Failed to create" in str(exc_info.value)

    def test_raise_rate_limit_error(self):
        """Test raising and catching RateLimitExceededError."""
        with pytest.raises(RateLimitExceededError) as exc_info:
            raise RateLimitExceededError(retry_after=30)

        assert exc_info.value.retry_after == 30

    def test_raise_tracking_not_found(self):
        """Test raising and catching TrackingNotFoundError."""
        with pytest.raises(TrackingNotFoundError) as exc_info:
            raise TrackingNotFoundError("TRACK123")

        assert exc_info.value.tracking_number == "TRACK123"

    def test_raise_invalid_address(self):
        """Test raising and catching InvalidAddressError."""
        with pytest.raises(InvalidAddressError) as exc_info:
            raise InvalidAddressError("Bad address")

        assert "Bad address" in str(exc_info.value)

    def test_raise_database_connection_error(self):
        """Test raising and catching DatabaseConnectionError."""
        with pytest.raises(DatabaseConnectionError) as exc_info:
            raise DatabaseConnectionError("Connection lost")

        assert "Connection lost" in str(exc_info.value)

    def test_raise_bulk_operation_error(self):
        """Test raising and catching BulkOperationError."""
        with pytest.raises(BulkOperationError) as exc_info:
            raise BulkOperationError("Bulk failed", failed_items=["item1"], success_count=5)

        assert exc_info.value.success_count == 5

    def test_catch_as_base_exception(self):
        """Test catching specific exceptions as base EasyPostMCPError."""
        with pytest.raises(EasyPostMCPError):
            raise ShipmentCreationError("Test")

        with pytest.raises(EasyPostMCPError):
            raise RateLimitExceededError()

        with pytest.raises(EasyPostMCPError):
            raise TrackingNotFoundError("TEST")

        with pytest.raises(EasyPostMCPError):
            raise InvalidAddressError("Test")

        with pytest.raises(EasyPostMCPError):
            raise DatabaseConnectionError("Test")

        with pytest.raises(EasyPostMCPError):
            raise BulkOperationError("Test")
