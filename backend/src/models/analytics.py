"""Analytics data models."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ShipmentMetrics(BaseModel):
    """Shipment metrics for analytics."""

    total_shipments: int = Field(..., description="Total number of shipments")
    total_cost: float = Field(..., description="Total shipping cost in USD")
    average_cost: float = Field(..., description="Average cost per shipment")
    date_range: dict = Field(..., description="Start and end dates of data")


class CarrierMetrics(BaseModel):
    """Carrier performance metrics."""

    carrier: str = Field(..., max_length=50)
    shipment_count: int
    total_cost: float
    average_cost: float
    percentage_of_total: float


class VolumeMetrics(BaseModel):
    """Shipment volume over time."""

    date: str = Field(..., description="Date in YYYY-MM-DD format")
    shipment_count: int
    total_cost: float


class RouteMetrics(BaseModel):
    """Top shipping routes."""

    origin: str = Field(..., max_length=100)
    destination: str = Field(..., max_length=100)
    shipment_count: int
    total_cost: float


class AnalyticsResponse(BaseModel):
    """Complete analytics response."""

    status: str = Field(..., pattern="^(success|error)$")
    data: Optional[dict] = None
    message: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AnalyticsData(BaseModel):
    """Analytics data structure."""

    summary: ShipmentMetrics
    by_carrier: List[CarrierMetrics]
    by_date: List[VolumeMetrics]
    top_routes: List[RouteMetrics]
