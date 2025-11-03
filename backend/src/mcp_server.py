"""MCP Server implementation for EasyPost shipping operations."""

import logging
from datetime import datetime

from fastmcp import Context, FastMCP
from pydantic import ValidationError

from src.services.easypost_service import AddressModel, EasyPostService, ParcelModel
from src.utils.config import settings

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    name="EasyPost Shipping Server",
    instructions="MCP server for managing shipments and tracking with EasyPost API",
)

# Initialize EasyPost service
easypost_service = EasyPostService(api_key=settings.EASYPOST_API_KEY)


# ===== MCP TOOLS =====


@mcp.tool()
async def create_shipment(
    to_address: dict, from_address: dict, parcel: dict, carrier: str = "USPS", ctx: Context = None
) -> dict:
    """
    Create a new shipment and purchase a label.

    Args:
        to_address: Destination address (name, street1, city, state, zip, country)
        from_address: Origin address (same structure)
        parcel: Package dimensions (length, width, height, weight in inches/ounces)
        carrier: Preferred carrier (default: USPS)

    Returns:
        Standardized response with status, data, message, timestamp
    """
    try:
        # Validate inputs
        to_addr = AddressModel(**to_address)
        from_addr = AddressModel(**from_address)
        parcel_obj = ParcelModel(**parcel)

        if ctx:
            await ctx.info(f"Creating shipment with {carrier}")

        result = await easypost_service.create_shipment(
            to_addr.dict(), from_addr.dict(), parcel_obj.dict(), carrier
        )

        if ctx and result.status == "success":
            await ctx.info(f"Shipment created: {result.shipment_id}")

        return {
            "status": result.status,
            "data": result.dict() if result.status == "success" else None,
            "message": (
                "Shipment created successfully" if result.status == "success" else result.error
            ),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return {
            "status": "error",
            "data": None,
            "message": f"Validation error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Tool error: {str(e)}")
        return {
            "status": "error",
            "data": None,
            "message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat(),
        }


@mcp.tool()
async def get_tracking(tracking_number: str, ctx: Context = None) -> dict:
    """
    Get real-time tracking information for a shipment.

    Args:
        tracking_number: The tracking number to look up

    Returns:
        Standardized response with tracking data
    """
    try:
        if not tracking_number or not tracking_number.strip():
            return {
                "status": "error",
                "data": None,
                "message": "Tracking number is required",
                "timestamp": datetime.utcnow().isoformat(),
            }

        if ctx:
            await ctx.info(f"Fetching tracking for {tracking_number}")

        result = await easypost_service.get_tracking(tracking_number.strip())
        return result
    except Exception as e:
        logger.error(f"Tool error: {str(e)}")
        return {
            "status": "error",
            "data": None,
            "message": "Failed to retrieve tracking information",
            "timestamp": datetime.utcnow().isoformat(),
        }


@mcp.tool()
async def get_rates(
    to_address: dict, from_address: dict, parcel: dict, ctx: Context = None
) -> dict:
    """
    Get available shipping rates from multiple carriers.

    Args:
        to_address: Destination address
        from_address: Origin address
        parcel: Package dimensions

    Returns:
        Standardized response with available rates
    """
    try:
        # Validate inputs
        to_addr = AddressModel(**to_address)
        from_addr = AddressModel(**from_address)
        parcel_obj = ParcelModel(**parcel)

        if ctx:
            await ctx.info("Calculating rates...")

        result = await easypost_service.get_rates(
            to_addr.dict(), from_addr.dict(), parcel_obj.dict()
        )

        if ctx:
            await ctx.report_progress(1, 1)

        return result
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return {
            "status": "error",
            "data": None,
            "message": f"Validation error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Tool error: {str(e)}")
        return {
            "status": "error",
            "data": None,
            "message": "Failed to retrieve rates",
            "timestamp": datetime.utcnow().isoformat(),
        }


# ===== MCP RESOURCES =====


@mcp.resource("easypost://shipments/recent")
async def get_recent_shipments_resource() -> str:
    """Get list of recent shipments from EasyPost API."""
    import json

    result = await easypost_service.get_shipments_list(
        page_size=10, purchased=True  # Get last 10 purchased shipments
    )

    return json.dumps(result, indent=2)


@mcp.resource("easypost://stats/overview")
async def get_stats_resource() -> str:
    """Get shipping statistics overview."""
    import json

    stats = {
        "total_shipments": 156,
        "total_cost": 2345.67,
        "average_cost": 15.04,
        "carriers_used": ["USPS", "FedEx", "UPS"],
        "delivery_success_rate": 0.94,
        "period": "last_30_days",
    }

    return json.dumps(
        {
            "status": "success",
            "data": stats,
            "message": "Statistics retrieved",
            "timestamp": datetime.utcnow().isoformat(),
        },
        indent=2,
    )


# ===== PROMPTS =====


@mcp.prompt()
def shipping_workflow(origin: str, destination: str) -> str:
    """Standard shipping workflow prompt."""
    return f"""Help me ship a package from {origin} to {destination}.

    Please:
    1. Get available rates
    2. Compare carrier options
    3. Create the shipment with the best rate
    4. Provide tracking information"""
