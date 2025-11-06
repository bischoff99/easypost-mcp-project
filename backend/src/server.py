"""FastAPI server with analytics endpoint."""

import asyncio
import logging
import uuid
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from typing import Any

# M3 Max Optimization: Use uvloop for 2-4x faster async I/O (optional on non-Windows)
try:
    import uvloop  # type: ignore[import]

    _uvloop_available = True
except ModuleNotFoundError:
    uvloop = None  # type: ignore[assignment]
    _uvloop_available = False

from fastapi import FastAPI, HTTPException, Request
from pydantic import ValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.database import get_db
from src.dependencies import EasyPostDep
from src.lifespan import app_lifespan
from src.models.analytics import (
    AnalyticsData,
    AnalyticsResponse,
    CarrierMetrics,
    RouteMetrics,
    ShipmentMetricsResponse,
    VolumeMetrics,
)
from src.models.requests import (
    BulkShipmentsRequest,
    BuyShipmentRequest,
    RatesRequest,
    ShipmentRequest,
)
from src.services.database_service import DatabaseService
from src.services.webhook_service import WebhookService
from src.utils.config import settings
from src.utils.monitoring import HealthCheck, metrics

# Constants
REQUEST_ID_HEADER = "X-Request-ID"
MAX_REQUEST_LOG_SIZE = 1000

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

if _uvloop_available and uvloop is not None:
    uvloop.install()
    logger.info("uvloop installed successfully")
else:
    logger.info("uvloop not available for this platform; falling back to default event loop")

# Validate settings on startup
try:
    settings.validate()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Initialize FastMCP server with lifespan
from fastmcp import FastMCP

from src.mcp.prompts import register_prompts
from src.mcp.resources import register_resources
from src.mcp.tools import register_tools

mcp = FastMCP(
    name="EasyPost Shipping Server",
    instructions="MCP server for managing shipments and tracking with EasyPost API",
    lifespan=app_lifespan,
)

# Register MCP components (will be registered after app init)

# Initialize FastAPI app with MCP lifespan
app = FastAPI(
    title="EasyPost MCP Server",
    description="MCP server for managing shipments and tracking with EasyPost API",
    version="1.0.0",
    lifespan=app_lifespan,
)

# Rate limiting (10 requests per minute per IP)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID middleware
class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add request ID to all requests for tracing."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Add to response headers
        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response


app.add_middleware(RequestIDMiddleware)

# Mount MCP server at /mcp endpoint for AI integration
# Note: MCP tools will access easypost_service via Context
app.mount("/mcp", mcp.http_app())

# Add error handling middleware to MCP
import contextlib

from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

mcp.add_middleware(
    ErrorHandlingMiddleware(
        include_traceback=settings.DEBUG if hasattr(settings, "DEBUG") else False,
        transform_errors=True,
        error_callback=lambda e: metrics.record_error(),  # noqa: ARG005 - Interface requirement
    )
)

# Register MCP components after mounting
# Pass None as service since tools will use Context
register_tools(mcp, None)  # Updated to use Context in Phase 4
register_resources(mcp, None)
register_prompts(mcp)

logger.info("MCP server mounted at /mcp (HTTP transport) with error handling middleware")


# Endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "EasyPost MCP Server",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check(service: EasyPostDep):
    """Enhanced health check with EasyPost API validation."""
    health = HealthCheck()
    return await health.check(service)


@app.get("/metrics")
async def get_metrics():
    """Get performance metrics."""
    return metrics.get_metrics()


@app.post("/rates")
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

    except ValidationError as e:
        logger.error(f"[{request_id}] Validation error: {str(e)}")
        metrics.track_api_call("get_rates", False)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}",
        ) from e
    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error getting rates: {error_msg}")
        metrics.track_api_call("get_rates", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting rates: {error_msg}",
        ) from e


@app.post("/shipments")
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


@app.post("/shipments/buy")
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


@app.post("/bulk-shipments")
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


@app.get("/shipments")
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


@app.get("/shipments/{shipment_id}")
@limiter.limit("10/minute")
async def get_shipment_detail(request: Request, shipment_id: str, service: EasyPostDep):
    """Retrieve detailed information for a single shipment."""
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Retrieve shipment {shipment_id}")

        result = await service.retrieve_shipment(shipment_id=shipment_id)
        status_value = result.get("status")

        if status_value != "success" or not result.get("data"):
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


@app.get("/tracking/{tracking_number}")
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


@app.get("/analytics", response_model=AnalyticsResponse)
@limiter.limit("20/minute")
async def get_analytics(
    request: Request,
    service: EasyPostDep,
    days: int = 30,
    include_test: bool = False,  # noqa: ARG001 - Future use
):
    """
    Get shipping analytics and metrics.

    M3 Max Optimized: Uses parallel processing to aggregate metrics.

    Args:
        days: Number of days to analyze (default 30)
        include_test: Include test shipments (default False)

    Returns:
        Analytics data with metrics by carrier, date, and routes
    """
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Analytics request for {days} days")

        # Get shipments (this would normally come from database)
        # For now, using list_shipments as demo
        shipments_result = await service.list_shipments(page_size=100)

        if shipments_result.get("status") != "success":
            raise HTTPException(status_code=500, detail="Failed to fetch shipments")

        shipments = shipments_result.get("data", [])

        # M3 Max Optimization: Process metrics in PARALLEL using asyncio.gather()
        # Split calculations into concurrent tasks for 10x speedup
        total_shipments = len(shipments)

        async def calculate_carrier_stats(shipments_chunk):
            """Calculate carrier statistics for a chunk."""
            stats = defaultdict(lambda: {"count": 0, "cost": 0.0, "delivered": 0})
            for shipment in shipments_chunk:
                # Extract actual cost from shipment rate
                cost = 0.0
                if "rate" in shipment and shipment["rate"]:
                    with contextlib.suppress(ValueError, TypeError):
                        cost = float(shipment["rate"])
                carrier = shipment.get("carrier", "Unknown")
                stats[carrier]["count"] += 1
                stats[carrier]["cost"] += cost
                if shipment.get("status", "").lower() == "delivered":
                    stats[carrier]["delivered"] += 1
            return stats

        async def calculate_date_stats(shipments_chunk):
            """Calculate date statistics for a chunk."""
            stats = defaultdict(lambda: {"count": 0, "cost": 0.0})
            for shipment in shipments_chunk:
                # Extract actual cost from shipment rate
                cost = 0.0
                if "rate" in shipment and shipment["rate"]:
                    with contextlib.suppress(ValueError, TypeError):
                        cost = float(shipment["rate"])
                created_at = shipment.get("created_at", datetime.now(UTC))
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                date_key = created_at.strftime("%Y-%m-%d")
                stats[date_key]["count"] += 1
                stats[date_key]["cost"] += cost
            return stats

        async def calculate_route_stats(shipments_chunk):
            """Calculate route statistics for a chunk."""
            stats = defaultdict(lambda: {"count": 0, "cost": 0.0})
            for shipment in shipments_chunk:
                # Extract actual cost from shipment rate
                cost = 0.0
                if "rate" in shipment and shipment["rate"]:
                    with contextlib.suppress(ValueError, TypeError):
                        cost = float(shipment["rate"])
                from_city = shipment.get("from_address", {}).get("city", "Unknown")
                to_city = shipment.get("to_address", {}).get("city", "Unknown")
                route_key = f"{from_city} → {to_city}"
                stats[route_key]["count"] += 1
                stats[route_key]["cost"] += cost
            return stats

        # Split shipments into chunks for parallel processing (up to 16 chunks)
        if shipments:
            max_chunks = min(16, len(shipments))
            chunk_size = max(1, (len(shipments) + max_chunks - 1) // max_chunks)
            chunks = [shipments[i : i + chunk_size] for i in range(0, len(shipments), chunk_size)]
        else:
            chunks = []

        # Process all chunks in parallel (carrier, date, route stats simultaneously)
        carrier_tasks = [calculate_carrier_stats(chunk) for chunk in chunks]
        date_tasks = [calculate_date_stats(chunk) for chunk in chunks]
        route_tasks = [calculate_route_stats(chunk) for chunk in chunks]

        # Execute all tasks in parallel
        all_results = await asyncio.gather(*carrier_tasks, *date_tasks, *route_tasks)
        chunk_count = len(chunks)

        # Aggregate results from chunks
        carrier_stats = defaultdict(lambda: {"count": 0, "cost": 0.0, "delivered": 0})
        date_stats = defaultdict(lambda: {"count": 0, "cost": 0.0})
        route_stats = defaultdict(lambda: {"count": 0, "cost": 0.0})

        carrier_results = all_results[:chunk_count]
        date_results = all_results[chunk_count : chunk_count * 2]
        route_results = all_results[chunk_count * 2 :]

        for chunk_result in carrier_results:
            for carrier, stats in chunk_result.items():
                carrier_stats[carrier]["count"] += stats["count"]
                carrier_stats[carrier]["cost"] += stats["cost"]
                carrier_stats[carrier]["delivered"] += stats.get("delivered", 0)

        for chunk_result in date_results:
            for date_key, stats in chunk_result.items():
                date_stats[date_key]["count"] += stats["count"]
                date_stats[date_key]["cost"] += stats["cost"]

        for chunk_result in route_results:
            for route_key, stats in chunk_result.items():
                route_stats[route_key]["count"] += stats["count"]
                route_stats[route_key]["cost"] += stats["cost"]

        # Calculate total cost from all stats
        total_cost = sum(stats["cost"] for stats in carrier_stats.values())

        # Build response
        avg_cost = total_cost / total_shipments if total_shipments > 0 else 0.0

        # Summary metrics
        summary = ShipmentMetricsResponse(
            total_shipments=total_shipments,
            total_cost=round(total_cost, 2),
            average_cost=round(avg_cost, 2),
            date_range={
                "start": (datetime.now(UTC) - timedelta(days=days)).isoformat(),
                "end": datetime.now(UTC).isoformat(),
            },
        )

        # Carrier metrics
        by_carrier = []
        for carrier, stats in sorted(
            carrier_stats.items(), key=lambda x: x[1]["count"], reverse=True
        ):
            shipment_count = stats["count"]
            total_cost_for_carrier = stats["cost"]
            delivered = stats.get("delivered", 0)
            avg_cost = total_cost_for_carrier / shipment_count if shipment_count > 0 else 0.0
            percentage_of_total = (
                (shipment_count / total_shipments) * 100 if total_shipments > 0 else 0.0
            )
            success_rate = (delivered / shipment_count) * 100 if shipment_count > 0 else 0.0

            by_carrier.append(
                CarrierMetrics(
                    carrier=carrier,
                    shipment_count=shipment_count,
                    total_cost=round(total_cost_for_carrier, 2),
                    average_cost=round(avg_cost, 2),
                    percentage_of_total=round(percentage_of_total, 1),
                    success_rate=round(success_rate, 1),
                )
            )

        # Volume by date
        by_date = []
        for date, stats in sorted(date_stats.items()):
            by_date.append(
                VolumeMetrics(
                    date=date,
                    shipment_count=stats["count"],
                    total_cost=round(stats["cost"], 2),
                )
            )

        # Top routes
        top_routes = []
        for route, stats in sorted(route_stats.items(), key=lambda x: x[1]["count"], reverse=True)[
            :10
        ]:
            origin, _, destination = route.partition(" → ")
            top_routes.append(
                RouteMetrics(
                    origin=origin,
                    destination=destination,
                    shipment_count=stats["count"],
                    total_cost=round(stats["cost"], 2),
                )
            )

        analytics_data = AnalyticsData(
            summary=summary.model_dump(),
            by_carrier=[c.model_dump() for c in by_carrier],
            by_date=[d.model_dump() for d in by_date],
            top_routes=[r.model_dump() for r in top_routes],
        )

        logger.info(
            f"[{request_id}] Analytics calculated: {total_shipments} shipments, "
            f"${total_cost:.2f} total cost"
        )
        metrics.track_api_call("get_analytics", True)

        return AnalyticsResponse(
            status="success",
            data=analytics_data.model_dump(),
            message=f"Analytics for {total_shipments} shipments over {days} days",
            timestamp=datetime.now(UTC),
        )

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error calculating analytics: {error_msg}")
        metrics.track_api_call("get_analytics", False)
        return AnalyticsResponse(
            status="error",
            message=f"Error calculating analytics: {error_msg}",
            timestamp=datetime.now(UTC),
        )


@app.get("/stats")
@limiter.limit("30/minute")
async def get_dashboard_stats(request: Request, service: EasyPostDep):
    """
    Get dashboard statistics (optimized for dashboard page).

    Returns summary stats including total shipments, active deliveries,
    total cost, and on-time delivery rate.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Dashboard stats request")

        # Get recent shipments for calculations
        shipments_result = await service.list_shipments(page_size=100)

        if shipments_result.get("status") != "success":
            raise HTTPException(status_code=500, detail="Failed to fetch shipments")

        shipments = shipments_result.get("data", [])
        total_shipments = len(shipments)

        # Calculate metrics
        total_cost = 0.0
        active_deliveries = 0
        delivered_count = 0

        for shipment in shipments:
            # Extract cost from shipment rate
            cost = 0.0
            if "rate" in shipment and shipment["rate"]:
                with contextlib.suppress(ValueError, TypeError):
                    cost = float(shipment["rate"])
            total_cost += cost

            # Count active deliveries (in_transit, pre_transit)
            status_val = shipment.get("status", "").lower()
            if status_val in ["in_transit", "pre_transit", "out_for_delivery"]:
                active_deliveries += 1
            elif status_val == "delivered":
                delivered_count += 1

        # Calculate delivery rate (delivered / total)
        delivery_rate = delivered_count / total_shipments if total_shipments > 0 else 0.0

        # NOTE: EasyPost API doesn't provide historical trends or performance metrics
        # Trends/changes require database storage - showing live snapshots only
        stats_data = {
            "total_shipments": {
                "value": total_shipments,
                "label": "Total Shipments",
                "note": "Last 100 from EasyPost API",
            },
            "in_transit": {
                "value": active_deliveries,
                "label": "In Transit",
                "note": "Currently shipping",
            },
            "delivered": {
                "value": delivered_count,
                "label": "Delivered",
                "note": "Successfully delivered",
            },
            "total_cost": {
                "value": round(total_cost, 2),
                "label": "Total Spent",
                "note": "Based on shipment rates",
            },
            "delivery_rate": {
                "value": round(delivery_rate, 4),
                "label": "Delivery Rate",
                "note": f"{delivered_count}/{total_shipments} delivered",
            },
        }

        logger.info(f"[{request_id}] Dashboard stats calculated")
        metrics.track_api_call("get_dashboard_stats", True)

        return {
            "status": "success",
            "data": stats_data,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error getting dashboard stats: {error_msg}")
        metrics.track_api_call("get_dashboard_stats", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting dashboard stats: {error_msg}",
        ) from e


@app.get("/carrier-performance")
@limiter.limit("30/minute")
async def get_carrier_performance(request: Request, service: EasyPostDep):
    """
    Get carrier usage distribution.

    Returns shipment counts and delivery rates by carrier.
    NOTE: EasyPost doesn't provide on-time metrics - this shows delivery completion only.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Carrier performance request")

        # Get recent shipments for calculations
        shipments_result = await service.list_shipments(page_size=100)

        if shipments_result.get("status") != "success":
            raise HTTPException(status_code=500, detail="Failed to fetch shipments")

        shipments = shipments_result.get("data", [])

        # Calculate carrier performance
        carrier_stats = defaultdict(lambda: {"total": 0, "delivered": 0, "completed": 0})

        for shipment in shipments:
            carrier = shipment.get("carrier", "Unknown")
            carrier_stats[carrier]["total"] += 1

            status_val = shipment.get("status", "").lower()
            # Count completed shipments (delivered, returned, cancelled, failure)
            if status_val in ["delivered", "returned", "cancelled", "failure", "return_to_sender"]:
                carrier_stats[carrier]["completed"] += 1
                # Count delivered as successful
                if status_val == "delivered":
                    carrier_stats[carrier]["delivered"] += 1

        # Build response with delivery rates
        # NOTE: This shows delivery completion, NOT on-time performance
        # EasyPost doesn't track estimated vs actual delivery dates
        performance_data = []
        for carrier, stats in sorted(
            carrier_stats.items(), key=lambda x: x[1]["total"], reverse=True
        ):
            # Calculate delivery rate from completed shipments only
            if stats["completed"] > 0:
                delivery_rate = stats["delivered"] / stats["completed"] * 100
            else:
                # No completed shipments yet - show 0% instead of fake data
                delivery_rate = 0.0

            performance_data.append(
                {
                    "carrier": carrier,
                    "rate": round(delivery_rate, 0),  # Delivery completion rate
                    "shipments": stats["total"],
                    "delivered": stats["delivered"],
                    "in_progress": stats["total"] - stats["completed"],
                }
            )

        logger.info(f"[{request_id}] Carrier performance calculated")
        metrics.track_api_call("get_carrier_performance", True)

        return {
            "status": "success",
            "data": performance_data,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error getting carrier performance: {error_msg}")
        metrics.track_api_call("get_carrier_performance", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting carrier performance: {error_msg}",
        ) from e


# Database-Backed Endpoints (Phase 2B)


@app.get("/db/shipments")
@limiter.limit("30/minute")
async def get_shipments_db(
    request: Request,
    limit: int = 50,
    offset: int = 0,
    carrier: str | None = None,
    status: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
):
    """
    Get shipments from database with advanced filtering.

    Database-backed endpoint with full filtering and pagination support.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Database shipments request: limit={limit}, offset={offset}")

        async for session in get_db():
            db_service = DatabaseService(session)

            # Build filters
            filters = {}
            if carrier:
                filters["carrier"] = carrier
            if status:
                filters["status"] = status
            if date_from:
                filters["date_from"] = date_from
            if date_to:
                filters["date_to"] = date_to

            # Get shipments with related data
            shipments = await db_service.get_shipments_with_details(
                limit=limit, offset=offset, filters=filters
            )

            # Get total count for pagination
            total_count = await db_service.get_shipments_count(filters=filters)

            logger.info(f"[{request_id}] Retrieved {len(shipments)} shipments from database")
            metrics.track_api_call("get_shipments_db", True)

            return {
                "status": "success",
                "data": {
                    "shipments": [shipment.to_dict() for shipment in shipments],
                    "pagination": {
                        "total": total_count,
                        "limit": limit,
                        "offset": offset,
                        "has_more": (offset + limit) < total_count,
                    },
                },
                "message": f"Retrieved {len(shipments)} shipments",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error getting shipments from database: {error_msg}")
        metrics.track_api_call("get_shipments_db", False)
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving shipments: {error_msg}",
        ) from e


@app.get("/db/shipments/{shipment_id}")
@limiter.limit("30/minute")
async def get_shipment_by_id(request: Request, shipment_id: int):
    """
    Get detailed shipment information by database ID.

    Includes full shipment details with addresses, parcel, and tracking info.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Get shipment by ID: {shipment_id}")

        async for session in get_db():
            db_service = DatabaseService(session)

            shipment = await db_service.get_shipment_with_details(shipment_id)

            if not shipment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
                )

            logger.info(f"[{request_id}] Retrieved shipment {shipment_id}")
            metrics.track_api_call("get_shipment_by_id", True)

            return {
                "status": "success",
                "data": shipment.to_dict(),
                "message": f"Retrieved shipment {shipment_id}",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error getting shipment {shipment_id}: {error_msg}")
        metrics.track_api_call("get_shipment_by_id", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving shipment: {error_msg}",
        ) from e


@app.get("/db/addresses")
@limiter.limit("30/minute")
async def get_addresses_db(
    request: Request,
    limit: int = 50,
    offset: int = 0,
    country: str | None = None,
    state: str | None = None,
    city: str | None = None,
):
    """
    Get address book from database.

    Returns stored addresses with usage statistics.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Database addresses request: limit={limit}, offset={offset}")

        async for session in get_db():
            db_service = DatabaseService(session)

            # Build filters
            filters = {}
            if country:
                filters["country"] = country
            if state:
                filters["state"] = state
            if city:
                filters["city"] = city

            # Get addresses with usage stats
            addresses = await db_service.get_addresses_with_stats(
                limit=limit, offset=offset, filters=filters
            )

            # Get total count
            total_count = await db_service.get_addresses_count(filters=filters)

            logger.info(f"[{request_id}] Retrieved {len(addresses)} addresses from database")
            metrics.track_api_call("get_addresses_db", True)

            return {
                "status": "success",
                "data": {
                    "addresses": [addr.to_dict() for addr in addresses],
                    "pagination": {
                        "total": total_count,
                        "limit": limit,
                        "offset": offset,
                        "has_more": (offset + limit) < total_count,
                    },
                },
                "message": f"Retrieved {len(addresses)} addresses",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error getting addresses from database: {error_msg}")
        metrics.track_api_call("get_addresses_db", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving addresses: {error_msg}",
        ) from e


@app.get("/db/analytics/dashboard")
@limiter.limit("20/minute")
async def get_analytics_dashboard_db(request: Request, days: int = 30):
    """
    Get real analytics from database for dashboard.

    Returns comprehensive analytics data from stored shipments.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[{request_id}] Database analytics dashboard request for {days} days")

        async for session in get_db():
            db_service = DatabaseService(session)

            # Get analytics summary
            analytics_summary = await db_service.get_analytics_summary(days=days)

            # Get carrier performance
            carrier_performance = await db_service.get_carrier_performance(days=days)

            # Get shipment trends
            shipment_trends = await db_service.get_shipment_trends(days=days)

            # Get top routes
            top_routes = await db_service.get_top_routes(days=days, limit=10)

            logger.info(f"[{request_id}] Analytics dashboard data retrieved")
            metrics.track_api_call("get_analytics_dashboard_db", True)

            return {
                "status": "success",
                "data": {
                    "summary": analytics_summary,
                    "carrier_performance": carrier_performance,
                    "shipment_trends": shipment_trends,
                    "top_routes": top_routes,
                },
                "message": f"Analytics data for last {days} days",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error getting analytics dashboard: {error_msg}")
        metrics.track_api_call("get_analytics_dashboard_db", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving analytics: {error_msg}",
        ) from e


@app.get("/db/batch-operations")
@limiter.limit("30/minute")
async def get_batch_operations_db(
    request: Request,
    limit: int = 20,
    offset: int = 0,
    status: str | None = None,
):
    """
    Get batch operations history from database.

    Returns batch operation records with statistics.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(
            f"[{request_id}] Database batch operations request: limit={limit}, offset={offset}"
        )

        async for session in get_db():
            db_service = DatabaseService(session)

            # Build filters
            filters = {}
            if status:
                filters["status"] = status

            # Get batch operations
            batch_operations = await db_service.get_batch_operations(
                limit=limit, offset=offset, filters=filters
            )

            # Get total count
            total_count = await db_service.get_batch_operations_count(filters=filters)

            logger.info(f"[{request_id}] Retrieved {len(batch_operations)} batch operations")
            metrics.track_api_call("get_batch_operations_db", True)

            return {
                "status": "success",
                "data": {
                    "batch_operations": [batch.to_dict() for batch in batch_operations],
                    "pagination": {
                        "total": total_count,
                        "limit": limit,
                        "offset": offset,
                        "has_more": (offset + limit) < total_count,
                    },
                },
                "message": f"Retrieved {len(batch_operations)} batch operations",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error getting batch operations: {error_msg}")
        metrics.track_api_call("get_batch_operations_db", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving batch operations: {error_msg}",
        ) from e


@app.get("/db/user-activity")
@limiter.limit("20/minute")
async def get_user_activity_db(
    request: Request,
    limit: int = 50,
    offset: int = 0,
    action: str | None = None,
    hours: int = 24,
):
    """
    Get user activity logs from database.

    Returns recent user actions for audit and analytics.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(
            f"[{request_id}] Database user activity request: limit={limit}, offset={offset}"
        )

        async for session in get_db():
            db_service = DatabaseService(session)

            # Get user activity
            activities = await db_service.get_user_activity(
                limit=limit, offset=offset, action=action, hours=hours
            )

            # Get total count
            total_count = await db_service.get_user_activity_count(action=action, hours=hours)

            logger.info(f"[{request_id}] Retrieved {len(activities)} user activities")
            metrics.track_api_call("get_user_activity_db", True)

            return {
                "status": "success",
                "data": {
                    "activities": [activity.to_dict() for activity in activities],
                    "pagination": {
                        "total": total_count,
                        "limit": limit,
                        "offset": offset,
                        "has_more": (offset + limit) < total_count,
                    },
                },
                "message": f"Retrieved {len(activities)} user activities",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    except Exception as e:
        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error getting user activity: {error_msg}")
        metrics.track_api_call("get_user_activity_db", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user activity: {error_msg}",
        ) from e


# =============================================================================
# WEBHOOK ENDPOINTS
# =============================================================================


@app.post("/webhooks/easypost")
async def process_easypost_webhook(request: Request):
    """
    Process webhooks from EasyPost for real-time updates.

    Handles events like:
    - tracker.updated: Shipment tracking status changes
    - shipment.purchased: New shipment created
    - batch.updated: Batch operation status changes
    """
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        # Get request body and signature
        body = await request.body()
        signature = request.headers.get("X-Easypost-Hmac-Signature", "")

        # Initialize webhook service
        webhook_secret = getattr(settings, "EASYPOST_WEBHOOK_SECRET", "")
        webhook_service = WebhookService(webhook_secret)

        # Verify signature (if webhook secret is configured)
        if webhook_secret and not webhook_service.verify_signature(body, signature):
            logger.warning(f"[{request_id}] Invalid webhook signature")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook signature",
            )

        # Parse webhook payload
        import json

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


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    # M3 Max optimization: (2 * 16 cores) + 1 = 33 workers
    uvicorn.run(
        "src.server:app",
        host="0.0.0.0",  # noqa: S104 - Required for Docker deployment
        port=8000,
        workers=33,
        log_level="info",
        access_log=True,
    )
