"""Tracking endpoints."""

import logging

from fastapi import APIRouter, HTTPException, Request
from starlette import status

from src.dependencies import EasyPostDep
from src.utils.monitoring import metrics

logger = logging.getLogger(__name__)

MAX_REQUEST_LOG_SIZE = 1000

router = APIRouter(tags=["tracking"])  # Prefix added when including in app


@router.get("/{tracking_number}")
async def track_shipment(request: Request, tracking_number: str, service: EasyPostDep):
    """Track a shipment by tracking number."""
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Track shipment {tracking_number}")

        result = await service.get_tracking(tracking_number=tracking_number)

        logger.info(f"[{request_id}] Tracking info retrieved")
        metrics.track_api_call("track_shipment", True)

        return result

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error tracking {tracking_number}: {error_msg}")
        metrics.track_api_call("track_shipment", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error tracking shipment: {error_msg}",
        ) from e
