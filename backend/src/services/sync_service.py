"""
Sync service for automatic EasyPost → PostgreSQL data synchronization.

Implements non-blocking background sync to keep PostgreSQL in sync with EasyPost API.
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy import select

from ..database import async_session
from ..models import Address
from .database_service import DatabaseService

logger = logging.getLogger(__name__)


class SyncService:
    """
    Service for syncing EasyPost data to PostgreSQL.

    All sync operations are non-blocking and use asyncio.create_task()
    to avoid slowing down API responses.
    """

    @staticmethod
    async def sync_shipment(shipment_data: Dict[str, Any]) -> Optional[UUID]:
        """
        Sync shipment from EasyPost to PostgreSQL.

        Args:
            shipment_data: Shipment data from EasyPost API

        Returns:
            Database shipment ID if successful, None otherwise
        """
        try:
            async with async_session() as session:
                db_service = DatabaseService(session)

                # Check if shipment already exists
                existing = await db_service.get_shipment_by_easypost_id(shipment_data.get("id", ""))

                if existing:
                    # Update existing shipment
                    update_data = {
                        "status": shipment_data.get("status", "unknown"),
                        "tracking_code": shipment_data.get("tracking_code"),
                        "carrier": shipment_data.get("carrier"),
                        "service": shipment_data.get("service"),
                        "total_cost": float(shipment_data.get("selected_rate", {}).get("rate", 0)),
                    }
                    await db_service.update_shipment(existing.id, update_data)
                    logger.info(f"Synced shipment update: {shipment_data.get('id')}")
                    return existing.id
                else:
                    # Create new shipment (if we have all required data)
                    # This would require syncing addresses first
                    logger.info(
                        f"Shipment {shipment_data.get('id')} not in database (addresses required)"
                    )
                    return None

        except Exception as e:
            # Non-blocking sync should never fail the main request
            logger.warning(f"Failed to sync shipment to database: {e}")
            return None

    @staticmethod
    async def sync_address(address_data: Dict[str, Any]) -> Optional[UUID]:
        """
        Sync address from EasyPost to PostgreSQL.

        Args:
            address_data: Address data from EasyPost API

        Returns:
            Database address ID if successful, None otherwise
        """
        try:
            async with async_session() as session:
                # Check if address exists
                easypost_id = address_data.get("id", "")
                stmt = select(Address).where(Address.easypost_id == easypost_id)
                result = await session.execute(stmt)
                existing = result.scalar_one_or_none()

                if existing:
                    logger.debug(f"Address {easypost_id} already in database")
                    return existing.id

                # Create new address
                new_address = Address(
                    easypost_id=easypost_id,
                    name=address_data.get("name"),
                    company=address_data.get("company"),
                    street1=address_data.get("street1", ""),
                    street2=address_data.get("street2"),
                    city=address_data.get("city", ""),
                    state=address_data.get("state"),
                    zip=address_data.get("zip", ""),
                    country=address_data.get("country", "US"),
                    phone=address_data.get("phone"),
                    email=address_data.get("email"),
                    is_residential=address_data.get("residential"),
                    verifications=address_data.get("verifications"),
                )

                session.add(new_address)
                await session.commit()
                await session.refresh(new_address)

                logger.info(f"Synced new address to database: {easypost_id}")
                return new_address.id

        except Exception as e:
            logger.warning(f"Failed to sync address to database: {e}")
            return None

    @staticmethod
    async def sync_tracking_event(shipment_easypost_id: str, event_data: Dict[str, Any]) -> bool:
        """
        Sync tracking event to PostgreSQL.

        Args:
            shipment_easypost_id: EasyPost shipment ID
            event_data: Tracking event data

        Returns:
            True if successful, False otherwise
        """
        try:
            async with async_session() as session:
                from ..models import ShipmentEvent

                db_service = DatabaseService(session)

                # Find shipment in database
                shipment = await db_service.get_shipment_by_easypost_id(shipment_easypost_id)
                if not shipment:
                    logger.warning(
                        f"Cannot sync event: shipment {shipment_easypost_id} not in database"
                    )
                    return False

                # Create event
                event = ShipmentEvent(
                    shipment_id=shipment.id,
                    status=event_data.get("status", ""),
                    message=event_data.get("message"),
                    description=event_data.get("description"),
                    carrier_status=event_data.get("carrier_detail", {}).get("status"),
                    tracking_location=event_data.get("tracking_location"),
                    event_datetime=event_data.get("datetime") or datetime.now(timezone.utc),
                )

                session.add(event)
                await session.commit()

                logger.info(f"Synced tracking event for shipment {shipment_easypost_id}")
                return True

        except Exception as e:
            logger.warning(f"Failed to sync tracking event: {e}")
            return False

    @staticmethod
    def sync_shipment_async(shipment_data: Dict[str, Any]) -> None:
        """
        Non-blocking wrapper for sync_shipment.

        Usage:
            SyncService.sync_shipment_async(shipment_data)
        """
        asyncio.create_task(SyncService.sync_shipment(shipment_data))

    @staticmethod
    def sync_address_async(address_data: Dict[str, Any]) -> None:
        """
        Non-blocking wrapper for sync_address.

        Usage:
            SyncService.sync_address_async(address_data)
        """
        asyncio.create_task(SyncService.sync_address(address_data))

    @staticmethod
    def sync_tracking_event_async(shipment_id: str, event_data: Dict[str, Any]) -> None:
        """
        Non-blocking wrapper for sync_tracking_event.

        Usage:
            SyncService.sync_tracking_event_async(shipment_id, event_data)
        """
        asyncio.create_task(SyncService.sync_tracking_event(shipment_id, event_data))
