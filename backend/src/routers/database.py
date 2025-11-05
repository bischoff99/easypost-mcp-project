"""Database-backed endpoints for persistent data access."""

import logging
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette import status

from src.database import get_db
from src.services.database_service import DatabaseService
from src.utils.monitoring import metrics

logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)

MAX_REQUEST_LOG_SIZE = 1000

router = APIRouter(tags=["database"])  # Prefix added when including in app


@router.get("/shipments")
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


@router.get("/shipments/{shipment_id}")
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


@router.get("/addresses")
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


@router.get("/analytics/dashboard")
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


@router.get("/batch-operations")
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


@router.get("/user-activity")
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
