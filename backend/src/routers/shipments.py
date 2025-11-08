"""Shipment management endpoints."""

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette import status

from src.dependencies import EasyPostDep
from src.models.requests import (
    BulkShipmentsRequest,
    BuyShipmentRequest,
    RatesRequest,
    ShipmentRequest,
)
from src.utils.monitoring import metrics

logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)

MAX_REQUEST_LOG_SIZE = 1000

# Main shipment router
router = APIRouter(tags=["shipments"])  # Prefix added when including in app

# Separate router for rates (not under /shipments)
rates_router = APIRouter(tags=["rates"])


@rates_router.post("/rates")
@limiter.limit("10/minute")
async def get_rates(request: Request, rates_request: RatesRequest, service: EasyPostDep):
    """Get shipping rates from EasyPost."""
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Getting rates request received")

        # Convert Pydantic models to dicts
        to_address_dict = rates_request.to_address.model_dump()
        from_address_dict = rates_request.from_address.model_dump()
        parcel_dict = rates_request.parcel.model_dump()

        # Get rates from EasyPost service
        result = await service.get_rates(
            to_address=to_address_dict,
            from_address=from_address_dict,
            parcel=parcel_dict,
        )

        logger.info(f"[{request_id}] Rates retrieved successfully")
        metrics.track_api_call("get_rates", True)

        return result

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error getting rates: {error_msg}")
        metrics.track_api_call("get_rates", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting rates: {error_msg}",
        ) from e


@router.post("/shipments")
@limiter.limit("10/minute")
async def create_shipment(
    request: Request, shipment_request: ShipmentRequest, service: EasyPostDep
):
    """Create a shipment with EasyPost."""
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Create shipment request received")

        # Convert to dicts
        to_address = shipment_request.to_address.model_dump()
        from_address = shipment_request.from_address.model_dump()
        parcel = shipment_request.parcel.model_dump()

        result = await service.create_shipment(
            to_address=to_address,
            from_address=from_address,
            parcel=parcel,
            carrier=shipment_request.carrier,
            service=shipment_request.service,
        )

        logger.info(f"[{request_id}] Shipment created successfully")
        metrics.track_api_call("create_shipment", True)

        return result

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error creating shipment: {error_msg}")
        metrics.track_api_call("create_shipment", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating shipment: {error_msg}",
        ) from e


@router.post("/shipments/buy")
@limiter.limit("10/minute")
async def buy_shipment(request: Request, buy_request: BuyShipmentRequest, service: EasyPostDep):
    """Buy a shipment with selected rate."""
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Buy shipment request received")

        # First create the shipment to get rates
        result = await service.get_rates(
            to_address=buy_request.to_address.model_dump(),
            from_address=buy_request.from_address.model_dump(),
            parcel=buy_request.parcel.model_dump(),
        )

        if result["status"] != "success" or not result.get("data"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get rates for shipment",
            )

        # Create shipment to get shipment ID
        shipment_result = await service.create_shipment(
            to_address=buy_request.to_address.model_dump(),
            from_address=buy_request.from_address.model_dump(),
            parcel=buy_request.parcel.model_dump(),
            buy_label=False,  # Don't buy yet
        )

        if shipment_result["status"] != "success":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create shipment",
            )

        # Now buy with the selected rate
        buy_result = await service.buy_shipment(
            shipment_id=shipment_result["id"], rate_id=buy_request.rate_id
        )

        logger.info(f"[{request_id}] Shipment purchased successfully")
        metrics.track_api_call("buy_shipment", True)

        return buy_result

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error buying shipment: {error_msg}")
        metrics.track_api_call("buy_shipment", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error buying shipment: {error_msg}",
        ) from e


@router.post("/bulk-shipments")
@limiter.limit("5/minute")
async def create_bulk_shipments(
    request: Request, bulk_request: BulkShipmentsRequest, service: EasyPostDep
):
    """Create multiple shipments concurrently."""
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(
            f"[{request_id}] Bulk shipment request received ({len(bulk_request.shipments)} items)"
        )

        shipments = bulk_request.shipments
        if not shipments:
            metrics.track_api_call("bulk_create_shipments", True)
            return {
                "status": "success",
                "data": {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "errors": [],
                    "results": [],
                },
                "timestamp": datetime.now(UTC).isoformat(),
            }

        concurrency = min(8, len(shipments))
        semaphore = asyncio.Semaphore(concurrency)

        async def process(index: int, shipment_req: ShipmentRequest):
            async with semaphore:
                payload = shipment_req.model_dump()
                try:
                    result = await service.create_shipment(
                        to_address=payload["to_address"],
                        from_address=payload["from_address"],
                        parcel=payload["parcel"],
                        carrier=payload.get("carrier", "USPS"),
                        service=payload.get("service"),
                        buy_label=False,
                    )
                    return index, result, None
                except Exception as exc:
                    return index, None, str(exc)

        tasks = [
            asyncio.create_task(process(idx, shipment)) for idx, shipment in enumerate(shipments)
        ]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        successes = 0
        errors: list[dict[str, Any]] = []
        results: list[dict[str, Any]] = []

        for outcome in raw_results:
            if isinstance(outcome, Exception):
                errors.append(
                    {"index": len(errors) + 1, "message": str(outcome)[:MAX_REQUEST_LOG_SIZE]}
                )
                continue

            index, result, error = outcome
            if error:
                errors.append({"index": index + 1, "message": error[:MAX_REQUEST_LOG_SIZE]})
            else:
                results.append({"index": index + 1, "result": result})
                if result.get("status") == "success":
                    successes += 1
                else:
                    errors.append(
                        {
                            "index": index + 1,
                            "message": result.get("message", "Unknown error")[
                                :MAX_REQUEST_LOG_SIZE
                            ],
                        }
                    )

        failed = len(errors)
        metrics.track_api_call("bulk_create_shipments", failed == 0)

        response_payload = {
            "total": len(shipments),
            "successful": successes,
            "failed": failed,
            "errors": errors,
            "results": results,
        }

        status_message = (
            "All shipments created successfully"
            if failed == 0
            else "Bulk shipment processing completed with errors"
        )

        logger.info(
            f"[{request_id}] Bulk shipment processing complete "
            f"(success={successes}, failed={failed})"
        )

        return {
            "status": "success",
            "message": status_message,
            "data": response_payload,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Bulk shipment error: {error_msg}")
        metrics.track_api_call("bulk_create_shipments", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing bulk shipments: {error_msg}",
        ) from e


@router.post("/shipments/{shipment_id}/buy")
@limiter.limit("10/minute")
async def buy_existing_shipment(
    request: Request, shipment_id: str, rate_id: str, service: EasyPostDep
):
    """Buy an existing shipment with selected rate."""
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Buy existing shipment {shipment_id} with rate {rate_id}")

        buy_result = await service.buy_shipment(shipment_id=shipment_id, rate_id=rate_id)

        logger.info(f"[{request_id}] Shipment purchased successfully")
        metrics.track_api_call("buy_existing_shipment", True)

        return buy_result

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error buying shipment: {error_msg}")
        metrics.track_api_call("buy_existing_shipment", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error buying shipment: {error_msg}",
        ) from e


@router.post("/shipments/{shipment_id}/refund")
@limiter.limit("10/minute")
async def refund_shipment(request: Request, shipment_id: str, service: EasyPostDep):
    """Refund a shipment."""
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Refund request for shipment {shipment_id}")

        result = await service.refund_shipment(shipment_id)

        if result["status"] == "success":
            logger.info(f"[{request_id}] Shipment refunded successfully")
            metrics.track_api_call("refund_shipment", True)
        else:
            logger.warning(f"[{request_id}] Refund failed: {result.get('message')}")
            metrics.track_api_call("refund_shipment", False)

        return result

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error refunding shipment: {error_msg}")
        metrics.track_api_call("refund_shipment", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error refunding shipment: {error_msg}",
        ) from e


@router.get("/shipments")
async def list_shipments(
    request: Request, service: EasyPostDep, page_size: int = 20, before_id: str | None = None
):
    """List shipments from EasyPost."""
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] List shipments request received")

        result = await service.list_shipments(page_size=page_size, before_id=before_id)

        logger.info(f"[{request_id}] Shipments list retrieved")
        metrics.track_api_call("list_shipments", True)

        return result

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error listing shipments: {error_msg}")
        metrics.track_api_call("list_shipments", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing shipments: {error_msg}",
        ) from e


@router.get("/shipments/{shipment_id}")
@limiter.limit("10/minute")
async def get_shipment_detail(request: Request, shipment_id: str, service: EasyPostDep):
    """Retrieve detailed information for a single shipment."""
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Retrieve shipment {shipment_id}")

        result = await service.retrieve_shipment(shipment_id)
        if result.get("status") != "success" or not result.get("data"):
            detail = result.get("message", "Failed to retrieve shipment")
            status_code = (
                status.HTTP_404_NOT_FOUND
                if isinstance(detail, str) and "not found" in detail.lower()
                else status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            metrics.track_api_call("get_shipment_detail", False)
            raise HTTPException(status_code=status_code, detail=detail)

        metrics.track_api_call("get_shipment_detail", True)
        return result

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error retrieving shipment {shipment_id}: {error_msg}")
        metrics.track_api_call("get_shipment_detail", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving shipment: {error_msg}",
        ) from e
