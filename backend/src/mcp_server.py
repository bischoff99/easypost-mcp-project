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
    """Get shipping statistics overview calculated from real EasyPost data."""
    import json
    from datetime import timedelta

    try:
        # Fetch recent shipments (last 30 days worth, up to 100)
        thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).isoformat()
        result = await easypost_service.get_shipments_list(
            page_size=100, purchased=True, start_datetime=thirty_days_ago
        )

        if result["status"] == "error":
            return json.dumps(result, indent=2)

        shipments = result.get("data", {}).get("shipments", [])

        # Calculate real statistics
        total_shipments = len(shipments)
        total_cost = 0.0
        carriers_used_set = set()
        delivered_count = 0

        for shipment in shipments:
            # Calculate total cost from selected rate
            if shipment.get("selected_rate") and shipment["selected_rate"].get("rate"):
                total_cost += float(shipment["selected_rate"]["rate"])

            # Track carriers used
            if shipment.get("selected_rate") and shipment["selected_rate"].get("carrier"):
                carriers_used_set.add(shipment["selected_rate"]["carrier"])

            # Track delivery success
            if shipment.get("status") == "delivered":
                delivered_count += 1

        average_cost = round(total_cost / total_shipments, 2) if total_shipments > 0 else 0
        delivery_success_rate = (
            round(delivered_count / total_shipments, 2) if total_shipments > 0 else 0
        )

        stats = {
            "total_shipments": total_shipments,
            "total_cost": round(total_cost, 2),
            "average_cost": average_cost,
            "carriers_used": sorted(carriers_used_set),
            "delivery_success_rate": delivery_success_rate,
            "delivered_count": delivered_count,
            "period": "last_30_days",
            "data_source": "real_easypost_api",
        }

        return json.dumps(
            {
                "status": "success",
                "data": stats,
                "message": f"Statistics calculated from {total_shipments} shipments",
                "timestamp": datetime.utcnow().isoformat(),
            },
            indent=2,
        )
    except Exception as e:
        logger.error(f"Error calculating stats: {str(e)}")
        return json.dumps(
            {
                "status": "error",
                "message": f"Failed to calculate statistics: {str(e)}",
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


@mcp.prompt()
def compare_carriers(
    origin: str, destination: str, weight_oz: float, length: float, width: float, height: float
) -> str:
    """Compare shipping rates across all available carriers."""
    return f"""Help me compare shipping costs from {origin} to {destination}.

Package details:
- Weight: {weight_oz} oz
- Dimensions: {length} x {width} x {height} inches

Please:
1. Use get_rates tool to fetch rates from USPS, FedEx, and UPS
2. Compare prices, delivery times, and service levels
3. Create a comparison table showing:
   - Carrier name
   - Service type
   - Price
   - Estimated delivery time
4. Recommend the best option based on:
   - Lowest cost
   - Fastest delivery
   - Best value (cost vs speed)"""


@mcp.prompt()
def track_and_notify(tracking_number: str, recipient_email: str = None) -> str:
    """Track a shipment and format notification message."""
    email_part = (
        f" and prepare an email notification for {recipient_email}" if recipient_email else ""
    )
    return f"""Track shipment {tracking_number}{email_part}.

Please:
1. Use get_tracking tool to fetch current tracking status
2. Extract key information:
   - Current status
   - Current location
   - Estimated delivery date
   - Last update timestamp
3. Format the information in a clear, customer-friendly way{'''
4. Draft an email notification with:
   - Subject line
   - Body with tracking details
   - Next steps for recipient''' if recipient_email else ''}"""


@mcp.prompt()
def cost_optimization(
    origin: str,
    destination: str,
    weight_oz: float,
    length: float,
    width: float,
    height: float,
    max_budget: float = None,
    max_days: int = None,
) -> str:
    """Find the most cost-effective shipping option with constraints."""
    constraints = []
    if max_budget:
        constraints.append(f"- Budget: ${max_budget} maximum")
    if max_days:
        constraints.append(f"- Delivery: {max_days} days maximum")

    constraints_text = "\n".join(constraints) if constraints else "- No constraints specified"

    return f"""Find the most cost-effective shipping option from {origin} to {destination}.

Package details:
- Weight: {weight_oz} oz
- Dimensions: {length} x {width} x {height} inches

Constraints:
{constraints_text}

Please:
1. Get rates from all available carriers
2. Filter options that meet the constraints
3. Rank by cost (lowest to highest)
4. Show top 3 options with pros/cons
5. Recommend the best value option with justification"""


@mcp.prompt()
def bulk_rate_check(origin: str, destinations: str, weight_oz: float) -> str:
    """Check rates for shipping to multiple destinations."""
    return f"""Check shipping rates from {origin} to multiple destinations.

Package details:
- Weight: {weight_oz} oz
- Standard box dimensions (12 x 9 x 6 inches)

Destinations: {destinations}

Please:
1. For each destination, get USPS rates (most economical for bulk)
2. Create a summary table showing:
   - Destination
   - USPS Ground price
   - USPS Priority price
   - Estimated delivery time
3. Calculate total cost for all shipments
4. Identify any bulk discount opportunities"""
