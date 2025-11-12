<<<<<<< HEAD
"""Response models for FastAPI endpoints."""

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class BaseResponse(BaseModel):
    """Base response model with common fields."""

    model_config = ConfigDict(
        ser_json_timedelta="float",
    )

    status: Literal["success", "error"]
    message: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ErrorResponse(BaseResponse):
    """Error response model."""

    status: Literal["error"] = "error"
    detail: str | None = None
    errors: list[dict[str, Any]] | None = None


# Shipment Response Models
class ShipmentsListResponse(BaseResponse):
    """Response for listing shipments."""

    status: Literal["success"] = "success"
    data: list[dict[str, Any]] | None = None


class ShipmentDetailResponse(BaseResponse):
    """Response for single shipment detail."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None


class CreateShipmentResponse(BaseResponse):
    """Response for creating a shipment."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    shipment_id: str | None = None
    tracking_number: str | None = None


class BuyShipmentResponse(BaseResponse):
    """Response for buying a shipment."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    label_url: str | None = None
    tracking_number: str | None = None


class RefundShipmentResponse(BaseResponse):
    """Response for refunding a shipment."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None


# Rates Response Models
class RatesResponse(BaseResponse):
    """Response for shipping rates."""

    status: Literal["success"] = "success"
    data: list[dict[str, Any]] | None = None


# Tracking Response Models
class TrackingResponse(BaseResponse):
    """Response for tracking information."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    tracking_number: str | None = None


# Bulk Operations Response Models
class BulkShipmentsResponse(BaseResponse):
    """Response for bulk shipment creation."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    total: int = 0
    successful: int = 0
    failed: int = 0


# Database Response Models
class PaginationInfo(BaseModel):
    """Pagination information."""

    total: int
    limit: int
    offset: int
    has_more: bool


class ShipmentsDBResponse(BaseResponse):
    """Response for database shipments list."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    pagination: PaginationInfo | None = None


class ShipmentDBDetailResponse(BaseResponse):
    """Response for database shipment detail."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None


class AddressesDBResponse(BaseResponse):
    """Response for database addresses list."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    pagination: PaginationInfo | None = None


class AnalyticsDashboardDBResponse(BaseResponse):
    """Response for database analytics dashboard."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None


# Analytics Response Models (already exists in analytics.py, but adding here for completeness)
# Note: AnalyticsResponse is already defined in src/models/analytics.py


class DashboardStatsResponse(BaseResponse):
    """Response for dashboard statistics."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None


class CarrierPerformanceResponse(BaseResponse):
    """Response for carrier performance metrics."""

    status: Literal["success"] = "success"
    data: list[dict[str, Any]] | None = None
||||||| 7a576da
=======
"""Response models for FastAPI endpoints."""

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class BaseResponse(BaseModel):
    """Base response model with common fields."""

    model_config = ConfigDict(
        ser_json_timedelta='float',
    )

    status: Literal["success", "error"]
    message: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ErrorResponse(BaseResponse):
    """Error response model."""

    status: Literal["error"] = "error"
    detail: str | None = None
    errors: list[dict[str, Any]] | None = None


# Shipment Response Models
class ShipmentsListResponse(BaseResponse):
    """Response for listing shipments."""

    status: Literal["success"] = "success"
    data: list[dict[str, Any]] | None = None


class ShipmentDetailResponse(BaseResponse):
    """Response for single shipment detail."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None


class CreateShipmentResponse(BaseResponse):
    """Response for creating a shipment."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    shipment_id: str | None = None
    tracking_number: str | None = None


class BuyShipmentResponse(BaseResponse):
    """Response for buying a shipment."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    label_url: str | None = None
    tracking_number: str | None = None


class RefundShipmentResponse(BaseResponse):
    """Response for refunding a shipment."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None


# Rates Response Models
class RatesResponse(BaseResponse):
    """Response for shipping rates."""

    status: Literal["success"] = "success"
    data: list[dict[str, Any]] | None = None


# Tracking Response Models
class TrackingResponse(BaseResponse):
    """Response for tracking information."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    tracking_number: str | None = None


# Bulk Operations Response Models
class BulkShipmentsResponse(BaseResponse):
    """Response for bulk shipment creation."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    total: int = 0
    successful: int = 0
    failed: int = 0


# Database Response Models
class PaginationInfo(BaseModel):
    """Pagination information."""

    total: int
    limit: int
    offset: int
    has_more: bool


class ShipmentsDBResponse(BaseResponse):
    """Response for database shipments list."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    pagination: PaginationInfo | None = None


class ShipmentDBDetailResponse(BaseResponse):
    """Response for database shipment detail."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None


class AddressesDBResponse(BaseResponse):
    """Response for database addresses list."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None
    pagination: PaginationInfo | None = None


class AnalyticsDashboardDBResponse(BaseResponse):
    """Response for database analytics dashboard."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None


# Analytics Response Models (already exists in analytics.py, but adding here for completeness)
# Note: AnalyticsResponse is already defined in src/models/analytics.py


class DashboardStatsResponse(BaseResponse):
    """Response for dashboard statistics."""

    status: Literal["success"] = "success"
    data: dict[str, Any] | None = None


class CarrierPerformanceResponse(BaseResponse):
    """Response for carrier performance metrics."""

    status: Literal["success"] = "success"
    data: list[dict[str, Any]] | None = None


# Webhook Response Models
class WebhookResponse(BaseResponse):
    """Response for webhook processing."""

    status: Literal["success"] = "success"
    event_type: str | None = None
    result: dict[str, Any] | None = None
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8
