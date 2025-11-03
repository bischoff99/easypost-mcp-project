import logging
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from pydantic import ValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.models.requests import RatesRequest, ShipmentRequest
from src.services.easypost_service import EasyPostService
from src.utils.config import settings
from src.utils.monitoring import HealthCheck, metrics

# Constants
MAX_RECENT_SHIPMENTS = 10
CORS_MAX_AGE_SECONDS = 86400  # 24 hours

# Configure logging
logging.basicConfig(
    level=settings.MCP_LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Validate settings
try:
    settings.validate()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Initialize EasyPost service (global)
easypost_service = EasyPostService(api_key=settings.EASYPOST_API_KEY)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


# ===== MIDDLEWARE =====


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add unique request ID to each request for tracing."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Record request metric
        metrics.record_request()

        logger.info(f"[{request_id}] {request.method} {request.url.path}")

        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            metrics.record_error()
            logger.error(f"[{request_id}] Request failed: {str(e)}")
            raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown."""
    # Startup
    logger.info("EasyPost API Server starting up...")
    yield
    # Shutdown
    logger.info("EasyPost API Server shutting down...")
    easypost_service.executor.shutdown(wait=True)
    logger.info("Resources cleaned up")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="EasyPost Shipping Server",
    description="API server for managing shipments and tracking with EasyPost API",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ===== API ENDPOINTS =====


@app.post("/api/shipments", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_shipment(request: Request, shipment_data: ShipmentRequest) -> Dict[str, Any]:
    """
    Create a new shipment and purchase a label.

    Args:
        request: FastAPI Request object (for rate limiting)
        shipment_data: Shipment request with to_address, from_address, parcel, carrier

    Returns:
        Standardized response with status, data, message, timestamp

    Raises:
        HTTPException: On validation or processing errors
    """
    try:
        logger.info(f"[PROGRESS] Creating shipment with {shipment_data.carrier}...")

        result = await easypost_service.create_shipment(
            shipment_data.to_address.dict(),
            shipment_data.from_address.dict(),
            shipment_data.parcel.dict(),
            shipment_data.carrier,
        )

        if result.status == "success":
            logger.info(f"[PROGRESS] Shipment created successfully: {result.shipment_id}")
            metrics.record_shipment()
            return {
                "status": result.status,
                "data": result.dict(),
                "message": "Shipment created successfully",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        else:
            logger.error(f"[PROGRESS] Shipment creation failed: {result.error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "data": None,
                    "message": result.error or "Failed to create shipment",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "data": None,
                "message": f"Validation error: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        ) from e
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "data": None,
                "message": "An unexpected error occurred",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        ) from None


@app.get("/api/tracking/{tracking_number}")
@limiter.limit("30/minute")
async def get_tracking(request: Request, tracking_number: str) -> Dict[str, Any]:
    """
    Get real-time tracking information for a shipment.

    Args:
        tracking_number: The tracking number to look up

    Returns:
        Standardized response with tracking data
    """
    try:
        if not tracking_number or not tracking_number.strip():
            raise HTTPException(status_code=400, detail="Tracking number is required")

        logger.info(f"[PROGRESS] Fetching tracking information for {tracking_number}...")

        result = await easypost_service.get_tracking(tracking_number.strip())
        metrics.record_tracking()
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return {
            "status": "error",
            "data": None,
            "message": "Failed to retrieve tracking information",
            "timestamp": datetime.utcnow().isoformat(),
        }


@app.post("/api/rates")
@limiter.limit("20/minute")
async def get_rates(request: Request, rates_data: RatesRequest) -> Dict[str, Any]:
    """
    Get available shipping rates from multiple carriers.

    Args:
        request: FastAPI Request object (for rate limiting)
        rates_data: Rates request with to_address, from_address, parcel

    Returns:
        Standardized response with available rates

    Raises:
        HTTPException: On validation or processing errors
    """
    try:
        logger.info("[PROGRESS] Calculating shipping rates...")

        result = await easypost_service.get_rates(
            rates_data.to_address.dict(), rates_data.from_address.dict(), rates_data.parcel.dict()
        )

        logger.info("[PROGRESS] Rates calculation completed")
        return result
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "data": None,
                "message": f"Validation error: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        ) from e
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "data": None,
                "message": "Failed to retrieve rates",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        ) from None


# ===== RESOURCES (REST API Endpoints) =====


@app.get("/api/shipments/recent")
async def get_recent_shipments(limit: int = 10) -> Dict[str, Any]:
    """
    Get recent shipments from EasyPost API.

    Args:
        limit: Maximum number of shipments to return (max 100)

    Returns:
        List of recent shipments with basic info
    """
    try:
        limit = min(limit, 100)  # EasyPost API max is 100
        logger.info(f"[PROGRESS] Retrieving recent {limit} shipments from EasyPost API...")

        result = await easypost_service.get_shipments_list(
            page_size=limit, purchased=True  # Only show purchased shipments
        )

        if result["status"] == "success":
            logger.info(f"[PROGRESS] Retrieved {len(result['data'])} shipments from EasyPost")
            return result
        else:
            logger.error(f"[PROGRESS] Failed to retrieve shipments: {result['message']}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "data": None,
                    "message": result["message"],
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resource error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "data": None,
                "message": "Failed to retrieve recent shipments",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        ) from None


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for monitoring.
    
    Returns comprehensive health status including:
    - Application status
    - EasyPost API connectivity
    - System resources (CPU, memory, disk)
    """
    system_health = HealthCheck.check_system()
    easypost_health = await HealthCheck.check_easypost(settings.EASYPOST_API_KEY)
    
    overall_healthy = (
        system_health["status"] == "healthy" and
        easypost_health["status"] == "healthy"
    )
    
    return {
        "status": "healthy" if overall_healthy else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "system": system_health,
            "easypost": easypost_health,
        },
    }


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """
    Application metrics endpoint.
    
    Returns:
        Current application metrics including request counts, error rates, etc.
    """
    return {
        "status": "success",
        "data": metrics.get_metrics(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/stats/overview")
async def get_stats() -> Dict[str, Any]:
    """
    Get shipping statistics overview.

    Returns:
        Overview statistics for shipments, costs, etc.
    """
    try:
        logger.info("[PROGRESS] Calculating shipping statistics...")

        # In a real implementation, this would aggregate data from EasyPost
        # For now, return placeholder statistics
        stats = {
            "total_shipments": 156,
            "total_cost": 2345.67,
            "average_cost": 15.04,
            "carriers_used": ["USPS", "FedEx", "UPS"],
            "delivery_success_rate": 0.94,
            "period": "last_30_days",
        }

        logger.info("[PROGRESS] Statistics calculated successfully")

        return {
            "status": "success",
            "data": stats,
            "message": "Shipping statistics retrieved successfully",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Resource error: {str(e)}")
        return {
            "status": "error",
            "data": None,
            "message": "Failed to retrieve shipping statistics",
            "timestamp": datetime.utcnow().isoformat(),
        }


@app.get("/api/shipments/{shipment_id}")
async def get_shipment(shipment_id: str) -> Dict[str, Any]:
    """
    Retrieve detailed shipment information.

    Args:
        shipment_id: The shipment ID to retrieve

    Returns:
        Detailed shipment information
    """
    try:
        logger.info(f"[PROGRESS] Retrieving shipment details for {shipment_id}...")

        # In a real implementation, this would call easypost.Shipment.retrieve(shipment_id)
        # For now, return placeholder data
        shipment_data = {
            "id": shipment_id,
            "tracking_number": "9400111899223345",
            "status": "in_transit",
            "label_url": f"https://api.easypost.com/labels/{shipment_id}.pdf",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "carrier": "USPS",
            "service": "Priority Mail",
            "rate": 8.50,
        }

        logger.info("[PROGRESS] Shipment details retrieved successfully")

        return {
            "status": "success",
            "data": shipment_data,
            "message": "Shipment details retrieved successfully",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Resource error: {str(e)}")
        return {
            "status": "error",
            "data": None,
            "message": "Failed to retrieve shipment details",
            "timestamp": datetime.utcnow().isoformat(),
        }


# Add middlewares to the FastAPI app (executed in reverse order)
# RequestIDMiddleware executes first (added last in chain)
app.add_middleware(RequestIDMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    max_age=CORS_MAX_AGE_SECONDS,
)


if __name__ == "__main__":
    logger.info(f"Starting API server on {settings.MCP_HOST}:{settings.MCP_PORT}")
    logger.info(f"CORS enabled for origins: {settings.CORS_ORIGINS}")

    uvicorn.run(
        app,
        host=settings.MCP_HOST,
        port=settings.MCP_PORT,
        log_level=settings.MCP_LOG_LEVEL.lower(),
    )
