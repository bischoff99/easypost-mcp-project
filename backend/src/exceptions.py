"""Custom exception classes for EasyPost MCP."""


class EasyPostMCPError(Exception):
    """Base exception for all EasyPost MCP errors."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ShipmentCreationError(EasyPostMCPError):
    """Raised when shipment creation fails."""

    def __init__(self, message: str, shipment_data: dict = None):
        super().__init__(message, {"shipment_data": shipment_data})
        self.shipment_data = shipment_data


class RateLimitExceededError(EasyPostMCPError):
    """Raised when EasyPost API rate limit is exceeded."""

    def __init__(self, retry_after: int = None):
        message = "EasyPost API rate limit exceeded"
        if retry_after:
            message += f". Retry after {retry_after} seconds"
        super().__init__(message, {"retry_after": retry_after})
        self.retry_after = retry_after


class TrackingNotFoundError(EasyPostMCPError):
    """Raised when tracking number not found."""

    def __init__(self, tracking_number: str):
        super().__init__(
            f"Tracking number not found: {tracking_number}", {"tracking_number": tracking_number}
        )
        self.tracking_number = tracking_number


class InvalidAddressError(EasyPostMCPError):
    """Raised when address validation fails."""

    def __init__(self, message: str, address_data: dict = None):
        super().__init__(message, {"address_data": address_data})
        self.address_data = address_data


class DatabaseConnectionError(EasyPostMCPError):
    """Raised when database connection fails."""

    pass


class BulkOperationError(EasyPostMCPError):
    """Raised when bulk operation fails."""

    def __init__(self, message: str, failed_items: list = None, success_count: int = 0):
        super().__init__(
            message, {"failed_items": failed_items or [], "success_count": success_count}
        )
        self.failed_items = failed_items or []
        self.success_count = success_count
