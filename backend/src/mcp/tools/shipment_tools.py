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
        contents: str = "General Merchandise",
        value: float = 50.0,
        ctx: Context = None,
    ) -> dict:
        """
        Create a new shipment and purchase a label.

        Args:
            to_address: Destination address (name, street1, city, state, zip, country)
            from_address: Origin address (same structure)
            parcel: Package dimensions (length, width, height, weight in inches/ounces)
            carrier: Preferred carrier (default: USPS)
            contents: Item description for customs (default: "General Merchandise")
            value: Item value in USD for customs (default: 50.0)
            ctx: MCP context

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

            # Check if international shipment
            is_international = to_addr.country != from_addr.country
            customs_info = None

            if is_international:
                # Create customs info for international shipment
                customs_item = easypost_service.client.customs_item.create(
                    description=contents,
                    hs_tariff_number="9999.00.0000",  # Generic code
                    origin_country=from_addr.country,
                    quantity=1,
                    value=value,
                    weight=parcel_obj.weight,
                )
                customs_info = easypost_service.client.customs_info.create(
                    customs_items=[customs_item]
                )

            # Add timeout to prevent SSE timeout errors
            result = await asyncio.wait_for(
                easypost_service.create_shipment(
                    to_addr.dict(), from_addr.dict(), parcel_obj.dict(), carrier, True, customs_info
                ),
                timeout=30.0,
            )

            if ctx and result.get("status") == "success":
                await ctx.info(f"Shipment created: {result.get('id')}")

            return {
                "status": result.get("status", "error"),
                "data": result if result.get("status") == "success" else None,
                "message": (
                    "Shipment created successfully"
                    if result.get("status") == "success"
                    else result.get("message", "Unknown error")
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
            logger.error(f"Tool error: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "data": None,
                "message": f"Error: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
