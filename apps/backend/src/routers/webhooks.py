"""Webhook endpoints for external integrations."""

import json
import logging

from fastapi import APIRouter, HTTPException, Request
from starlette import status

from src.services.webhook_service import WebhookService
from src.utils.config import settings
from src.utils.monitoring import metrics

logger = logging.getLogger(__name__)

MAX_REQUEST_LOG_SIZE = 1000

router = APIRouter(tags=["webhooks"])  # Prefix added when including in app


@router.post("/easypost")
async def process_easypost_webhook(request: Request):
    """
    Process webhooks from EasyPost for real-time updates.

    Handles events like:
    - tracker.updated: Shipment tracking status changes
    - shipment.purchased: New shipment created
    - batch.updated: Batch operation status changes

    SECURITY: Requires EASYPOST_WEBHOOK_SECRET to be configured.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        # Get request body and signature
        body = await request.body()
        signature = request.headers.get("X-Easypost-Hmac-Signature", "")

        # Initialize webhook service
        webhook_secret = getattr(settings, "EASYPOST_WEBHOOK_SECRET", "")

        # SECURITY: Webhook secret is REQUIRED, not optional
        if not webhook_secret:
            logger.error(f"[{request_id}] Webhook secret not configured - rejecting webhook")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Webhook processing not configured",
            )

        webhook_service = WebhookService(webhook_secret)

        # SECURITY: ALWAYS verify signature
        if not webhook_service.verify_signature(body, signature):
            logger.warning(
                f"[{request_id}] Invalid webhook signature from IP: {request.client.host}"
            )
            metrics.track_api_call("webhook_easypost_invalid_signature", False)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook signature",
            )

        # Parse webhook payload
        payload = json.loads(body)
        event_type = payload.get("description", "")
        event_data = payload.get("result", {})

        logger.info(f"[{request_id}] Webhook received: {event_type}")

        # Process event
        result = await webhook_service.process_webhook(event_type, {"result": event_data})

        metrics.track_api_call("webhook_easypost", True)

        return {
            "status": "success",
            "message": "Webhook processed",
            "event_type": event_type,
            "result": result,
        }

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Webhook processing error: {error_msg}")
        metrics.track_api_call("webhook_easypost", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Webhook processing failed: {error_msg}",
        ) from e
