"""
Database models package for EasyPost MCP.
"""

# Import all models to ensure they are registered with SQLAlchemy
from .analytics import (
    AnalyticsSummary,
    BatchOperation,
    CarrierPerformance,
    ShipmentMetrics,
    SystemMetrics,
    UserActivity,
)
from .requests import RatesRequest, ShipmentRequest
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
    "AnalyticsSummary",
    "CarrierPerformance",
    "ShipmentMetrics",
    "UserActivity",
    "SystemMetrics",
    "BatchOperation",
]
