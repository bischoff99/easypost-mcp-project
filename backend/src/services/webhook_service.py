"""
Webhook service for processing EasyPost webhook events.

Handles real-time updates from EasyPost for shipment tracking,
status changes, and other events.
"""

import hashlib
import hmac
import logging
from typing import Any, Dict

from ..database import async_session
from .database_service import DatabaseService
from .sync_service import SyncService

logger = logging.getLogger(__name__)


class WebhookService:
    """Service for processing EasyPost webhooks."""

    def __init__(self, webhook_secret: str):
        """
        Initialize webhook service.

        Args:
            webhook_secret: EasyPost webhook secret for signature verification
        """
        self.webhook_secret = webhook_secret

    def verify_signature(self, request_body: bytes, signature: str) -> bool:
        """
        Verify EasyPost webhook signature.

        Args:
            request_body: Raw request body
            signature: X-Easypost-Hmac-Signature header value

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Compute HMAC-SHA256
            expected_signature = hmac.new(
                self.webhook_secret.encode("utf-8"), request_body, hashlib.sha256
            ).hexdigest()

            # Compare signatures (constant time comparison)
            return hmac.compare_digest(expected_signature, signature)

        except Exception as e:
            logger.error(f"Signature verification error: {e}")
            return False

    async def process_webhook(self, event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process webhook event from EasyPost.

        Args:
            event_type: Type of event (e.g., 'tracker.updated', 'shipment.purchased')
            event_data: Event payload from EasyPost

        Returns:
            Processing result
        """
        try:
            logger.info(f"Processing webhook event: {event_type}")

            # Route to appropriate handler
            if event_type == "tracker.updated":
                return await self._handle_tracker_update(event_data)
            elif event_type == "shipment.purchased":
                return await self._handle_shipment_purchased(event_data)
            elif event_type == "batch.updated":
                return await self._handle_batch_update(event_data)
            else:
                logger.warning(f"Unhandled webhook event type: {event_type}")
                return {"status": "ignored", "message": f"Event type {event_type} not handled"}

        except Exception as e:
            logger.error(f"Webhook processing error: {e}")
            return {"status": "error", "message": str(e)}

    async def _handle_tracker_update(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle tracker.updated event.

        Updates shipment status and creates tracking event in PostgreSQL.
        """
        try:
            result = event_data.get("result", {})
            shipment_id = result.get("id")
            tracking_code = result.get("tracking_code")
            status_value = result.get("status")

            # Get tracking details
            tracking_details = result.get("tracking_details", [])
            latest_event = tracking_details[0] if tracking_details else {}

            logger.info(
                f"Tracker update: {tracking_code} -> {status_value} " f"(shipment: {shipment_id})"
            )

            # Sync tracking event to PostgreSQL (non-blocking)
            SyncService.sync_tracking_event_async(shipment_id, latest_event)

            return {
                "status": "success",
                "message": f"Tracker updated for {tracking_code}",
                "shipment_id": shipment_id,
            }

        except Exception as e:
            logger.error(f"Error handling tracker update: {e}")
            return {"status": "error", "message": str(e)}

    async def _handle_shipment_purchased(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle shipment.purchased event.

        Syncs newly purchased shipment to PostgreSQL.
        """
        try:
            result = event_data.get("result", {})
            shipment_id = result.get("id")
            tracking_code = result.get("tracking_code")

            logger.info(f"Shipment purchased: {shipment_id} ({tracking_code})")

            # Sync shipment to PostgreSQL (non-blocking)
            SyncService.sync_shipment_async(result)

            return {
                "status": "success",
                "message": f"Shipment {tracking_code} synced",
                "shipment_id": shipment_id,
            }

        except Exception as e:
            logger.error(f"Error handling shipment purchased: {e}")
            return {"status": "error", "message": str(e)}

    async def _handle_batch_update(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle batch.updated event.

        Updates batch operation status in PostgreSQL.
        """
        try:
            result = event_data.get("result", {})
            batch_id = result.get("id")
            status_value = result.get("status")

            logger.info(f"Batch update: {batch_id} -> {status_value}")

            # Update batch operation in PostgreSQL
            async with async_session() as session:
                db_service = DatabaseService(session)

                # Update batch status
                await db_service.update_batch_operation(
                    batch_id,
                    {
                        "status": status_value,
                        "processed_items": result.get("num_shipments", 0),
                    },
                )

            return {
                "status": "success",
                "message": f"Batch {batch_id} updated",
                "batch_id": batch_id,
            }

        except Exception as e:
            logger.error(f"Error handling batch update: {e}")
            return {"status": "error", "message": str(e)}
