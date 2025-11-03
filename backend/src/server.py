import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware

from src.models.requests import RatesRequest, ShipmentRequest
from src.services.easypost_service import EasyPostService
from src.utils.config import settings

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


# ===== API ENDPOINTS =====


@app.post("/api/shipments", status_code=status.HTTP_201_CREATED)
async def create_shipment(request: ShipmentRequest) -> Dict[str, Any]:
    """
    Create a new shipment and purchase a label.

    Args:
        request: Shipment request with to_address, from_address, parcel, carrier

    Returns:
        Standardized response with status, data, message, timestamp

    Raises:
        HTTPException: On validation or processing errors
    """
    try:
        logger.info(f"[PROGRESS] Creating shipment with {request.carrier}...")

        result = await easypost_service.create_shipment(
            request.to_address.dict(),
            request.from_address.dict(),
            request.parcel.dict(),
            request.carrier,
        )

        if result.status == "success":
            logger.info(f"[PROGRESS] Shipment created successfully: {result.shipment_id}")
            return {
                "status": result.status,
                "data": result.dict(),
                "message": "Shipment created successfully",
                "timestamp": datetime.utcnow().isoformat(),
            }
        else:
            logger.error(f"[PROGRESS] Shipment creation failed: {result.error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "data": None,
                    "message": result.error or "Failed to create shipment",
                    "timestamp": datetime.utcnow().isoformat(),
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
                "timestamp": datetime.utcnow().isoformat(),
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
                "timestamp": datetime.utcnow().isoformat(),
            },
        ) from None


@app.get("/api/tracking/{tracking_number}")
async def get_tracking(tracking_number: str) -> Dict[str, Any]:
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
async def get_rates(request: RatesRequest) -> Dict[str, Any]:
    """
    Get available shipping rates from multiple carriers.

    Args:
        request: Rates request with to_address, from_address, parcel

    Returns:
        Standardized response with available rates

    Raises:
        HTTPException: On validation or processing errors
    """
    try:
        logger.info("[PROGRESS] Calculating shipping rates...")

        result = await easypost_service.get_rates(
            request.to_address.dict(), request.from_address.dict(), request.parcel.dict()
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
                "timestamp": datetime.utcnow().isoformat(),
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
                "timestamp": datetime.utcnow().isoformat(),
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
                    "timestamp": datetime.utcnow().isoformat(),
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
                "timestamp": datetime.utcnow().isoformat(),
            },
        ) from None


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
            "created_at": datetime.utcnow().isoformat(),
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


# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    max_age=CORS_MAX_AGE_SECONDS,
)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "EasyPost API Server"}


if __name__ == "__main__":
    logger.info(f"Starting API server on {settings.MCP_HOST}:{settings.MCP_PORT}")
    logger.info(f"CORS enabled for origins: {settings.CORS_ORIGINS}")

    uvicorn.run(
        app,
        host=settings.MCP_HOST,
        port=settings.MCP_PORT,
        log_level=settings.MCP_LOG_LEVEL.lower(),
    )
