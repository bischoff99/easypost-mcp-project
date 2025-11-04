"""
Database models for analytics and metrics tracking.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base


class AnalyticsSummary(Base):
    """Daily/weekly/monthly analytics summaries."""

    __tablename__ = "analytics_summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False, index=True)
    period = Column(String(20), nullable=False)  # daily, weekly, monthly
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Shipment metrics
    total_shipments = Column(Integer, nullable=False, default=0)
    successful_shipments = Column(Integer, nullable=False, default=0)
    failed_shipments = Column(Integer, nullable=False, default=0)

    # Cost metrics
    total_cost = Column(Float, nullable=False, default=0.0)
    average_cost_per_shipment = Column(Float, nullable=True)
    currency = Column(String(3), nullable=False, default="USD")

    # Performance metrics
    average_delivery_days = Column(Float, nullable=True)
    on_time_delivery_rate = Column(Float, nullable=True)  # percentage

    # Carrier performance
    carrier_stats = Column(JSON, nullable=True)  # Breakdown by carrier

    # Geographic data
    top_destinations = Column(JSON, nullable=True)  # Top cities/countries
    domestic_vs_international = Column(JSON, nullable=True)

    # Service level breakdown
    service_breakdown = Column(JSON, nullable=True)

    def __repr__(self):
        return (
            f"<AnalyticsSummary(date={self.date}, "
            f"period={self.period}, shipments={self.total_shipments})>"
        )


class CarrierPerformance(Base):
    """Carrier performance tracking."""

    __tablename__ = "carrier_performance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    carrier = Column(String(50), nullable=False, index=True)
    service = Column(String(50), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Performance metrics
    total_shipments = Column(Integer, nullable=False, default=0)
    on_time_deliveries = Column(Integer, nullable=False, default=0)
    delayed_deliveries = Column(Integer, nullable=False, default=0)
    failed_deliveries = Column(Integer, nullable=False, default=0)

    # Cost metrics
    total_cost = Column(Float, nullable=False, default=0.0)
    average_cost = Column(Float, nullable=True)
    currency = Column(String(3), nullable=False, default="USD")

    # Delivery time metrics
    average_delivery_days = Column(Float, nullable=True)
    min_delivery_days = Column(Integer, nullable=True)
    max_delivery_days = Column(Integer, nullable=True)

    # Rating (calculated)
    on_time_rate = Column(Float, nullable=True)  # percentage
    reliability_score = Column(Float, nullable=True)  # 0-100

    def __repr__(self):
        return (
            f"<CarrierPerformance(carrier={self.carrier}, "
            f"service={self.service}, on_time_rate={self.on_time_rate})>"
        )


class ShipmentMetrics(Base):
    """Detailed metrics for individual shipments."""

    __tablename__ = "shipment_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_id = Column(
        UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False, unique=True
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Processing metrics
    creation_to_purchase_time = Column(Float, nullable=True)  # seconds
    purchase_to_label_time = Column(Float, nullable=True)  # seconds
    total_processing_time = Column(Float, nullable=True)  # seconds

    # Cost breakdown
    base_rate = Column(Float, nullable=True)
    fuel_surcharge = Column(Float, nullable=True)
    insurance_cost = Column(Float, nullable=True)
    tracking_cost = Column(Float, nullable=True)
    other_fees = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)
    currency = Column(String(3), nullable=False, default="USD")

    # Delivery metrics
    estimated_delivery_days = Column(Integer, nullable=True)
    actual_delivery_days = Column(Integer, nullable=True)
    delivery_delay_days = Column(Integer, nullable=True)
    was_on_time = Column(Boolean, nullable=True)

    # Quality metrics
    tracking_updates_count = Column(Integer, nullable=False, default=0)
    exception_events_count = Column(Integer, nullable=False, default=0)
    delivery_attempts = Column(Integer, nullable=False, default=1)

    # Geographic data
    origin_country = Column(String(2), nullable=True)
    destination_country = Column(String(2), nullable=True)
    distance_km = Column(Float, nullable=True)

    # Additional metadata
    carrier = Column(String(50), nullable=True)
    service = Column(String(50), nullable=True)
    package_type = Column(String(50), nullable=True)
    weight_kg = Column(Float, nullable=True)

    def __repr__(self):
        return f"<ShipmentMetrics(shipment_id={self.shipment_id}, total_cost={self.total_cost})>"


class UserActivity(Base):
    """User activity and usage tracking."""

    __tablename__ = "user_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(100), nullable=True, index=True)  # For future user system
    session_id = Column(String(100), nullable=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Activity details
    action = Column(String(100), nullable=False)  # create_shipment, get_rates, track_package, etc.
    resource = Column(String(100), nullable=True)  # shipment, address, parcel, etc.
    resource_id = Column(String(100), nullable=True)

    # Request details
    method = Column(String(10), nullable=False)  # GET, POST, etc.
    endpoint = Column(String(200), nullable=False)
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv4/IPv6

    # Response details
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)

    # Additional context
    extra_metadata = Column(JSON, nullable=True)

    def __repr__(self):
        return (
            f"<UserActivity(action={self.action}, "
            f"status={self.status_code}, time={self.response_time_ms}ms)>"
        )


class SystemMetrics(Base):
    """System performance and health metrics."""

    __tablename__ = "system_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Application metrics
    active_connections = Column(Integer, nullable=False, default=0)
    total_requests = Column(Integer, nullable=False, default=0)
    error_rate = Column(Float, nullable=True)  # percentage

    # Performance metrics
    avg_response_time_ms = Column(Float, nullable=True)
    p95_response_time_ms = Column(Float, nullable=True)
    p99_response_time_ms = Column(Float, nullable=True)

    # Resource usage
    cpu_usage_percent = Column(Float, nullable=True)
    memory_usage_mb = Column(Float, nullable=True)
    disk_usage_percent = Column(Float, nullable=True)

    # Database metrics
    db_connections_active = Column(Integer, nullable=False, default=0)
    db_connections_idle = Column(Integer, nullable=False, default=0)
    db_query_count = Column(Integer, nullable=False, default=0)
    db_slow_queries = Column(Integer, nullable=False, default=0)

    # External API metrics
    easypost_requests = Column(Integer, nullable=False, default=0)
    easypost_errors = Column(Integer, nullable=False, default=0)
    easypost_avg_response_time_ms = Column(Float, nullable=True)

    # Cache metrics (future)
    cache_hit_rate = Column(Float, nullable=True)
    cache_miss_rate = Column(Float, nullable=True)

    def __repr__(self):
        return (
            f"<SystemMetrics(timestamp={self.timestamp}, "
            f"cpu={self.cpu_usage_percent}%, memory={self.memory_usage_mb}MB)>"
        )


class BatchOperation(Base):
    """Batch operations tracking."""

    __tablename__ = "batch_operations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id = Column(String(50), unique=True, index=True, nullable=False)
    operation_type = Column(String(50), nullable=False)  # create_shipments, get_rates, etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Status tracking
    status = Column(
        String(20), nullable=False, default="pending"
    )  # pending, processing, completed, failed
    total_items = Column(Integer, nullable=False)
    processed_items = Column(Integer, nullable=False, default=0)
    successful_items = Column(Integer, nullable=False, default=0)
    failed_items = Column(Integer, nullable=False, default=0)

    # Performance metrics
    total_processing_time = Column(Float, nullable=True)  # seconds
    avg_item_time = Column(Float, nullable=True)  # seconds per item

    # Error tracking
    errors = Column(JSON, nullable=True)  # Array of error details

    # Metadata
    user_id = Column(String(100), nullable=True)
    source = Column(String(50), nullable=True)  # api, ui, scheduled
    parameters = Column(JSON, nullable=True)  # Original request parameters

    def __repr__(self):
        return (
            f"<BatchOperation(batch_id={self.batch_id}, status={self.status}, "
            f"success={self.successful_items}/{self.total_items})>"
        )


# Pydantic models for API responses
from datetime import datetime
from typing import Any, Dict, List

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
    shipments: int
    total_cost: float
    avg_cost: float
    success_rate: float


class VolumeMetrics(BaseModel):
    """Volume metrics by date."""

    date: str
    shipments: int
    cost: float


class RouteMetrics(BaseModel):
    """Route metrics for top shipping routes."""

    origin: str
    destination: str
    shipment_count: int
    total_cost: float


class AnalyticsData(BaseModel):
    """Analytics data structure for API responses."""

    summary: Dict[str, Any]
    by_carrier: List[Dict[str, Any]]
    by_date: List[Dict[str, Any]]
    top_routes: List[Dict[str, Any]]


class AnalyticsResponse(BaseModel):
    """Analytics API response."""

    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    timestamp: datetime
