"""
Database models package for EasyPost MCP.
"""

# Import all models to ensure they are registered with SQLAlchemy
from .bulk_dto import (
    AddressDTO,
    CustomsInfoDTO,
    CustomsItemDTO,
    ParcelDTO,
    ShipmentDataDTO,
    ShipmentRequestDTO,
    ShipmentResultDTO,
    ValidationResultDTO,
    VerifiedAddressDTO,
)
from .requests import RatesRequest, ShipmentRequest
from .responses import (
    AddressesDBResponse,
    AnalyticsDashboardDBResponse,
    BulkShipmentsResponse,
    BuyShipmentResponse,
    CarrierPerformanceResponse,
    CreateShipmentResponse,
    DashboardStatsResponse,
    ErrorResponse,
    PaginationInfo,
    RatesResponse,
    RefundShipmentResponse,
    ShipmentDBDetailResponse,
    ShipmentDetailResponse,
    ShipmentsDBResponse,
    ShipmentsListResponse,
    TrackingResponse,
    WebhookResponse,
)
from .shipment import Address, CustomsInfo, Parcel, Shipment, ShipmentEvent

# Export all models and request types
__all__ = [
    # Request models
    "ShipmentRequest",
    "RatesRequest",
    # Database models
    "Shipment",
    "Address",
    "Parcel",
    "CustomsInfo",
    "ShipmentEvent",
    # Bulk DTOs
    "AddressDTO",
    "ParcelDTO",
    "CustomsInfoDTO",
    "CustomsItemDTO",
    "ShipmentDataDTO",
    "ValidationResultDTO",
    "VerifiedAddressDTO",
    "ShipmentRequestDTO",
    "ShipmentResultDTO",
    # Response models
    "ErrorResponse",
    "RatesResponse",
    "CreateShipmentResponse",
    "BuyShipmentResponse",
    "RefundShipmentResponse",
    "BulkShipmentsResponse",
    "ShipmentsListResponse",
    "ShipmentDetailResponse",
    "TrackingResponse",
    "ShipmentsDBResponse",
    "ShipmentDBDetailResponse",
    "AddressesDBResponse",
    "AnalyticsDashboardDBResponse",
    "DashboardStatsResponse",
    "CarrierPerformanceResponse",
    "WebhookResponse",
    "PaginationInfo",
]
