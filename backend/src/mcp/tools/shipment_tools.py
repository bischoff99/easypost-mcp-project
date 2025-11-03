"""Shipment creation MCP tool."""

import asyncio
import logging
from datetime import datetime, timezone

from fastmcp import Context
from pydantic import ValidationError

from src.services.easypost_service import AddressModel, ParcelModel

logger = logging.getLogger(__name__)


def register_shipment_tools(mcp, easypost_service):
    """Register shipment-related tools with MCP server."""

    @mcp.tool()
    async def create_shipment(
        to_address: dict,
        from_address: dict,
        parcel: dict,
        carrier: str = "USPS",
        ctx: Context = None,
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

            # Add timeout to prevent SSE timeout errors
            result = await asyncio.wait_for(
                easypost_service.create_shipment(
                    to_addr.dict(), from_addr.dict(), parcel_obj.dict(), carrier
                ),
                timeout=30.0,
            )

            if ctx and result.status == "success":
                await ctx.info(f"Shipment created: {result.shipment_id}")

            return {
                "status": result.status,
                "data": result.dict() if result.status == "success" else None,
                "message": (
                    "Shipment created successfully" if result.status == "success" else result.error
                ),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except asyncio.TimeoutError:
            logger.error("Shipment creation timed out after 30 seconds")
            return {
                "status": "error",
                "data": None,
                "message": "Shipment creation timed out. Please try again.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return {
                "status": "error",
                "data": None,
                "message": f"Validation error: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error(f"Tool error: {str(e)}")
            return {
                "status": "error",
                "data": None,
                "message": "An unexpected error occurred",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
