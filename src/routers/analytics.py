"""Simplified analytics endpoints for personal use."""

import logging
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from starlette import status

from src.dependencies import EasyPostDep
from src.models.analytics import (
    AnalyticsData,
    AnalyticsResponse,
    CarrierMetrics,
    RouteMetrics,
    ShipmentMetricsResponse,
    VolumeMetrics,
)
from src.utils.monitoring import metrics

logger = logging.getLogger(__name__)

MAX_REQUEST_LOG_SIZE = 1000

router = APIRouter(tags=["analytics"])  # Prefix added when including in app


def _build_carrier_metrics(
    carrier_stats: dict[str, dict[str, Any]], total_shipments: int
) -> list[CarrierMetrics]:
    """Build carrier metrics list from statistics."""
    by_carrier = []
    for carrier, stats in sorted(carrier_stats.items(), key=lambda x: x[1]["count"], reverse=True):
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
    return by_carrier


def _build_date_metrics(date_stats: dict[str, dict[str, Any]]) -> list[VolumeMetrics]:
    """Build date metrics list from statistics."""
    by_date = []
    for date, stats in sorted(date_stats.items()):
        by_date.append(
            VolumeMetrics(
                date=date,
                shipment_count=stats["count"],
                total_cost=round(stats["cost"], 2),
            )
        )
    return by_date


def _build_route_metrics(route_stats: dict[str, dict[str, Any]]) -> list[RouteMetrics]:
    """Build route metrics list from statistics."""
    top_routes = []
    for route, stats in sorted(route_stats.items(), key=lambda x: x[1]["count"], reverse=True)[:10]:
        origin, _, destination = route.partition(" → ")
        top_routes.append(
            RouteMetrics(
                origin=origin,
                destination=destination,
                shipment_count=stats["count"],
                total_cost=round(stats["cost"], 2),
            )
        )
    return top_routes


@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(
    request: Request,
    service: EasyPostDep,
    days: int = Query(default=30, ge=1, le=365),
    include_test: bool = False,  # noqa: ARG001 - Future use
) -> dict[str, Any]:
    """
    Get simplified shipping analytics for personal use.

    Args:
        days: Number of days to analyze (default 30)
        include_test: Include test shipments (default False)

    Returns:
        Basic analytics data with metrics by carrier, date, and routes
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

        # Simple sequential processing (no parallel chunks for personal use)
        carrier_stats = defaultdict(lambda: {"count": 0, "cost": 0.0, "delivered": 0})
        date_stats = defaultdict(lambda: {"count": 0, "cost": 0.0})
        route_stats = defaultdict(lambda: {"count": 0, "cost": 0.0})

        for shipment in shipments:
            # Carrier stats
            cost = 0.0
            if "rate" in shipment and shipment["rate"]:
                try:
                    cost = float(shipment["rate"])
                except (ValueError, TypeError):
                    logger.debug(f"Could not parse cost from shipment rate: {shipment.get('rate')}")
            carrier = shipment.get("carrier", "Unknown")
            carrier_stats[carrier]["count"] += 1
            carrier_stats[carrier]["cost"] += cost
            if shipment.get("status", "").lower() == "delivered":
                carrier_stats[carrier]["delivered"] += 1

            # Date stats
            created_at = shipment.get("created_at", datetime.now(UTC))
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            date_key = created_at.strftime("%Y-%m-%d")
            date_stats[date_key]["count"] += 1
            date_stats[date_key]["cost"] += cost

            # Route stats
            from_city = shipment.get("from_address", {}).get("city", "Unknown")
            to_city = shipment.get("to_address", {}).get("city", "Unknown")
            route_key = f"{from_city} → {to_city}"
            route_stats[route_key]["count"] += 1
            route_stats[route_key]["cost"] += cost

        total_shipments = len(shipments)
        total_cost = sum(stats["cost"] for stats in carrier_stats.values())
        avg_cost = total_cost / total_shipments if total_shipments > 0 else 0.0

        # Build response components
        summary = ShipmentMetricsResponse(
            total_shipments=total_shipments,
            total_cost=round(total_cost, 2),
            average_cost=round(avg_cost, 2),
            date_range={
                "start": (datetime.now(UTC) - timedelta(days=days)).isoformat(),
                "end": datetime.now(UTC).isoformat(),
            },
        )

        by_carrier = _build_carrier_metrics(carrier_stats, total_shipments)
        by_date = _build_date_metrics(date_stats)
        top_routes = _build_route_metrics(route_stats)

        analytics_data = AnalyticsData(
            summary=summary.model_dump(),
            by_carrier=[carrier.model_dump() for carrier in by_carrier],
            by_date=[date.model_dump() for date in by_date],
            top_routes=[route.model_dump() for route in top_routes],
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
        import traceback

        error_msg = str(e)[:MAX_REQUEST_LOG_SIZE]
        logger.error(f"[{request_id}] Error calculating analytics: {error_msg}")
        logger.error(f"[{request_id}] Traceback: {traceback.format_exc()[:500]}")
        metrics.track_api_call("get_analytics", False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating analytics: {error_msg}",
        ) from e
