"""
Pydantic models for analytics API responses.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ShipmentMetricsResponse(BaseModel):
    """Shipment metrics for analytics API responses."""

    total_shipments: int
    total_cost: float
    average_cost: float
    date_range: dict


class CarrierMetrics(BaseModel):
    """Carrier metrics for analytics."""

    carrier: str
    shipment_count: int
    total_cost: float
    average_cost: float
    percentage_of_total: float
    success_rate: float | None = None


class VolumeMetrics(BaseModel):
    """Volume metrics by date."""

    date: str
    shipment_count: int
    total_cost: float


class RouteMetrics(BaseModel):
    """Route metrics for top shipping routes."""

    origin: str
    destination: str
    shipment_count: int
    total_cost: float


class AnalyticsData(BaseModel):
    """Analytics data structure for API responses."""

    summary: dict[str, Any]
    by_carrier: list[dict[str, Any]]
    by_date: list[dict[str, Any]]
    top_routes: list[dict[str, Any]]


class AnalyticsResponse(BaseModel):
    """Analytics API response."""

    status: str
    data: dict[str, Any] | None = None
    message: str | None = None
    timestamp: datetime
