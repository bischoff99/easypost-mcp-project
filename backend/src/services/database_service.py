"""
Database service layer for EasyPost MCP.
Provides CRUD operations and business logic for database models.
"""

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import (
    Address,
    AnalyticsSummary,
    BatchOperation,
    CarrierPerformance,
    Shipment,
    ShipmentEvent,
    SystemMetrics,
    UserActivity,
)

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service class for database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # Shipment CRUD Operations
    async def create_shipment(self, shipment_data: Dict[str, Any]) -> Shipment:
        """Create a new shipment."""
        shipment = Shipment(**shipment_data)
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        logger.info(f"Created shipment {shipment.id}")
        return shipment

    async def get_shipment(self, shipment_id: UUID) -> Optional[Shipment]:
        """Get shipment by ID with related data."""
        stmt = select(Shipment).where(Shipment.id == shipment_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_shipment_by_easypost_id(self, easypost_id: str) -> Optional[Shipment]:
        """Get shipment by EasyPost ID."""
        stmt = select(Shipment).where(Shipment.easypost_id == easypost_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_shipment(
        self, shipment_id: UUID, update_data: Dict[str, Any]
    ) -> Optional[Shipment]:
        """Update shipment."""
        stmt = (
            update(Shipment)
            .where(Shipment.id == shipment_id)
            .values(**update_data)
            .returning(Shipment)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        updated = result.scalar_one_or_none()
        if updated:
            logger.info(f"Updated shipment {shipment_id}")
        return updated

    async def delete_shipment(self, shipment_id: UUID) -> bool:
        """Delete shipment."""
        stmt = delete(Shipment).where(Shipment.id == shipment_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        deleted = result.rowcount > 0
        if deleted:
            logger.info(f"Deleted shipment {shipment_id}")
        return deleted

    async def list_shipments(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None,
        carrier: Optional[str] = None,
    ) -> List[Shipment]:
        """List shipments with optional filtering."""
        stmt = select(Shipment)

        if status:
            stmt = stmt.where(Shipment.status == status)
        if carrier:
            stmt = stmt.where(Shipment.carrier == carrier)

        stmt = stmt.limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # Address CRUD Operations
    async def create_address(self, address_data: Dict[str, Any]) -> Address:
        """Create a new address."""
        address = Address(**address_data)
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)
        logger.info(f"Created address {address.id}")
        return address

    async def get_address(self, address_id: UUID) -> Optional[Address]:
        """Get address by ID."""
        stmt = select(Address).where(Address.id == address_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_address(
        self, address_id: UUID, update_data: Dict[str, Any]
    ) -> Optional[Address]:
        """Update address."""
        stmt = (
            update(Address).where(Address.id == address_id).values(**update_data).returning(Address)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    # Analytics Operations
    async def create_analytics_summary(self, summary_data: Dict[str, Any]) -> AnalyticsSummary:
        """Create analytics summary."""
        summary = AnalyticsSummary(**summary_data)
        self.session.add(summary)
        await self.session.commit()
        await self.session.refresh(summary)
        return summary

    async def get_analytics_summary_by_date(self, date, period: str) -> Optional[AnalyticsSummary]:
        """Get analytics summary for specific date and period."""
        from datetime import date as date_type

        # Convert string to date if needed
        if isinstance(date, str):
            date = date_type.fromisoformat(date)

        stmt = select(AnalyticsSummary).where(
            AnalyticsSummary.date == date, AnalyticsSummary.period == period
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_carrier_performance_record(
        self, carrier: str, service: str, date: str
    ) -> Optional[CarrierPerformance]:
        """Get carrier performance record for specific carrier/service/date."""
        stmt = select(CarrierPerformance).where(
            CarrierPerformance.carrier == carrier,
            CarrierPerformance.service == service,
            CarrierPerformance.date == date,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_carrier_performance(
        self, performance_data: Dict[str, Any]
    ) -> CarrierPerformance:
        """Create carrier performance record."""
        performance = CarrierPerformance(**performance_data)
        self.session.add(performance)
        await self.session.commit()
        await self.session.refresh(performance)
        return performance

    # User Activity Tracking
    async def log_user_activity(self, activity_data: Dict[str, Any]) -> UserActivity:
        """Log user activity."""
        activity = UserActivity(**activity_data)
        self.session.add(activity)
        await self.session.commit()
        await self.session.refresh(activity)
        return activity

    # System Metrics
    async def record_system_metrics(self, metrics_data: Dict[str, Any]) -> SystemMetrics:
        """Record system performance metrics."""
        metrics = SystemMetrics(**metrics_data)
        self.session.add(metrics)
        await self.session.commit()
        await self.session.refresh(metrics)
        return metrics

    # Batch Operations
    async def create_batch_operation(self, batch_data: Dict[str, Any]) -> BatchOperation:
        """Create batch operation record."""
        batch = BatchOperation(**batch_data)
        self.session.add(batch)
        await self.session.commit()
        await self.session.refresh(batch)
        logger.info(f"Created batch operation {batch.batch_id}")
        return batch

    async def update_batch_operation(
        self, batch_id: str, update_data: Dict[str, Any]
    ) -> Optional[BatchOperation]:
        """Update batch operation."""
        stmt = (
            update(BatchOperation)
            .where(BatchOperation.batch_id == batch_id)
            .values(**update_data)
            .returning(BatchOperation)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def get_batch_operation(self, batch_id: str) -> Optional[BatchOperation]:
        """Get batch operation by ID."""
        stmt = select(BatchOperation).where(BatchOperation.batch_id == batch_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # Utility Methods
    async def get_shipment_count(self) -> int:
        """Get total shipment count."""
        stmt = select(func.count(Shipment.id))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_shipments_by_status(self) -> Dict[str, int]:
        """Get shipment count by status."""
        stmt = select(Shipment.status, func.count(Shipment.id)).group_by(Shipment.status)
        result = await self.session.execute(stmt)
        return dict(result.all())

    async def get_recent_activities(self, limit: int = 10) -> List[UserActivity]:
        """Get recent user activities."""
        stmt = select(UserActivity).order_by(UserActivity.timestamp.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # API Endpoint Methods
    async def get_shipments_with_details(
        self, limit: int = 50, offset: int = 0, filters: Optional[Dict[str, Any]] = None
    ) -> List[Shipment]:
        """Get shipments with related data for API endpoints."""
        from sqlalchemy.orm import selectinload

        stmt = select(Shipment).options(
            selectinload(Shipment.from_address),
            selectinload(Shipment.to_address),
            selectinload(Shipment.parcel),
        )

        # Apply filters
        if filters:
            if filters.get("carrier"):
                stmt = stmt.where(Shipment.carrier == filters["carrier"])
            if filters.get("status"):
                stmt = stmt.where(Shipment.status == filters["status"])
            if filters.get("date_from"):
                stmt = stmt.where(Shipment.created_at >= filters["date_from"])
            if filters.get("date_to"):
                stmt = stmt.where(Shipment.created_at <= filters["date_to"])

        stmt = stmt.limit(limit).offset(offset).order_by(Shipment.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_shipments_count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Get total shipments count with filters."""
        stmt = select(func.count(Shipment.id))

        # Apply filters
        if filters:
            if filters.get("carrier"):
                stmt = stmt.where(Shipment.carrier == filters["carrier"])
            if filters.get("status"):
                stmt = stmt.where(Shipment.status == filters["status"])
            if filters.get("date_from"):
                stmt = stmt.where(Shipment.created_at >= filters["date_from"])
            if filters.get("date_to"):
                stmt = stmt.where(Shipment.created_at <= filters["date_to"])

        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_shipment_with_details(self, shipment_id: UUID) -> Optional[Shipment]:
        """Get shipment with all related data."""
        from sqlalchemy.orm import selectinload

        stmt = (
            select(Shipment)
            .options(
                selectinload(Shipment.from_address),
                selectinload(Shipment.to_address),
                selectinload(Shipment.parcel),
                selectinload(Shipment.customs_info),
                selectinload(Shipment.events),
            )
            .where(Shipment.id == shipment_id)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_addresses_with_stats(
        self, limit: int = 50, offset: int = 0, filters: Optional[Dict[str, Any]] = None
    ) -> List[Address]:
        """Get addresses with usage statistics."""
        # Get addresses with shipment counts
        stmt = (
            select(
                Address,
                func.count(Shipment.from_address_id).label("from_count"),
                func.count(Shipment.to_address_id).label("to_count"),
            )
            .outerjoin(
                Shipment,
                (Shipment.from_address_id == Address.id) | (Shipment.to_address_id == Address.id),
            )
            .group_by(Address.id)
        )

        # Apply filters
        if filters:
            if filters.get("country"):
                stmt = stmt.where(Address.country == filters["country"])
            if filters.get("state"):
                stmt = stmt.where(Address.state == filters["state"])
            if filters.get("city"):
                stmt = stmt.where(Address.city == filters["city"])

        stmt = stmt.limit(limit).offset(offset)
        result = await self.session.execute(stmt)

        addresses = []
        for row in result:
            address = row[0]
            # Add usage statistics
            address.usage_count = row[1] + row[2]  # from_count + to_count
            addresses.append(address)

        return addresses

    async def get_addresses_count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Get total addresses count with filters."""
        stmt = select(func.count(Address.id))

        # Apply filters
        if filters:
            if filters.get("country"):
                stmt = stmt.where(Address.country == filters["country"])
            if filters.get("state"):
                stmt = stmt.where(Address.state == filters["state"])
            if filters.get("city"):
                stmt = stmt.where(Address.city == filters["city"])

        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_analytics_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics summary for dashboard (last N days)."""
        from datetime import datetime, timedelta, timezone

        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)

        # Get shipment statistics
        stmt = select(
            func.count(Shipment.id).label("total_shipments"),
            func.sum(Shipment.total_cost).label("total_cost"),
            func.avg(Shipment.total_cost).label("average_cost"),
        ).where(Shipment.created_at >= start_date)

        result = await self.session.execute(stmt)
        row = result.first()

        return {
            "total_shipments": row[0] or 0,
            "total_cost": float(row[1] or 0),
            "average_cost": float(row[2] or 0),
            "date_range": {"start": start_date.isoformat(), "end": end_date.isoformat()},
        }

    async def get_carrier_performance(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get carrier performance metrics for dashboard (last N days)."""
        from datetime import datetime, timedelta, timezone

        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Get carrier performance
        stmt = (
            select(
                Shipment.carrier,
                func.count(Shipment.id).label("total_shipments"),
                func.avg(ShipmentEvent.delivery_time_hours).label("avg_delivery_time"),
                (func.count(ShipmentEvent.id) * 100.0 / func.count(Shipment.id)).label(
                    "on_time_rate"
                ),
            )
            .outerjoin(
                ShipmentEvent,
                (ShipmentEvent.shipment_id == Shipment.id) & (ShipmentEvent.status == "delivered"),
            )
            .where(Shipment.created_at >= start_date)
            .group_by(Shipment.carrier)
        )

        result = await self.session.execute(stmt)

        performance = []
        for row in result:
            performance.append(
                {
                    "carrier": row[0],
                    "total_shipments": row[1],
                    "avg_delivery_time": float(row[2] or 0),
                    "on_time_rate": float(row[3] or 0),
                }
            )

        return performance

    async def get_shipment_trends(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get shipment trends over time."""
        from datetime import datetime, timedelta, timezone

        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Get daily shipment counts and costs
        stmt = (
            select(
                func.date(Shipment.created_at).label("date"),
                func.count(Shipment.id).label("count"),
                func.sum(Shipment.total_cost).label("cost"),
            )
            .where(Shipment.created_at >= start_date)
            .group_by(func.date(Shipment.created_at))
            .order_by(func.date(Shipment.created_at))
        )

        result = await self.session.execute(stmt)

        trends = []
        for row in result:
            trends.append({"date": row[0].isoformat(), "count": row[1], "cost": float(row[2] or 0)})

        return trends

    async def get_top_routes(self, days: int = 30, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top shipping routes by volume."""
        from datetime import datetime, timedelta, timezone

        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Get route statistics
        stmt = (
            select(
                Address.city.label("from_city"),
                Address.state.label("from_state"),
                Address.country.label("from_country"),
                Address.city.label("to_city"),
                Address.state.label("to_state"),
                Address.country.label("to_country"),
                func.count(Shipment.id).label("count"),
                func.sum(Shipment.total_cost).label("total_cost"),
            )
            .select_from(Shipment)
            .join(Address, Shipment.from_address_id == Address.id)
            .join(Address, Shipment.to_address_id == Address.id)
            .where(Shipment.created_at >= start_date)
            .group_by(
                Address.city,
                Address.state,
                Address.country,
                Address.city,
                Address.state,
                Address.country,
            )
            .order_by(func.count(Shipment.id).desc())
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        routes = []
        for row in result:
            routes.append(
                {
                    "origin": f"{row[0]}, {row[1]} {row[2]}",
                    "destination": f"{row[3]}, {row[4]} {row[5]}",
                    "count": row[6],
                    "total_cost": float(row[7] or 0),
                }
            )

        return routes

    async def get_batch_operations(
        self, limit: int = 20, offset: int = 0, filters: Optional[Dict[str, Any]] = None
    ) -> List[BatchOperation]:
        """Get batch operations with pagination."""
        stmt = select(BatchOperation)

        # Apply filters
        if filters and filters.get("status"):
            stmt = stmt.where(BatchOperation.status == filters["status"])

        stmt = stmt.limit(limit).offset(offset).order_by(BatchOperation.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_batch_operations_count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Get total batch operations count."""
        stmt = select(func.count(BatchOperation.id))

        # Apply filters
        if filters and filters.get("status"):
            stmt = stmt.where(BatchOperation.status == filters["status"])

        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_user_activity(
        self, limit: int = 50, offset: int = 0, action: Optional[str] = None, hours: int = 24
    ) -> List[UserActivity]:
        """Get user activity logs."""
        from datetime import datetime, timedelta, timezone

        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)

        stmt = select(UserActivity).where(UserActivity.timestamp >= start_time)

        if action:
            stmt = stmt.where(UserActivity.action == action)

        stmt = stmt.limit(limit).offset(offset).order_by(UserActivity.timestamp.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_user_activity_count(self, action: Optional[str] = None, hours: int = 24) -> int:
        """Get user activity count."""
        from datetime import datetime, timedelta, timezone

        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)

        stmt = select(func.count(UserActivity.id)).where(UserActivity.timestamp >= start_time)

        if action:
            stmt = stmt.where(UserActivity.action == action)

        result = await self.session.execute(stmt)
        return result.scalar()
