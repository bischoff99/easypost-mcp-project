"""Rate calculation MCP tool."""

import asyncio
import logging
from datetime import datetime, timezone

from fastmcp import Context
from pydantic import ValidationError

from src.services.easypost_service import AddressModel, ParcelModel

logger = logging.getLogger(__name__)


def register_rate_tools(mcp, easypost_service):
    """Register rate-related tools with MCP server."""

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

            # Add timeout to prevent SSE timeout errors
            result = await asyncio.wait_for(
                easypost_service.get_rates(
                    to_addr.dict(), from_addr.dict(), parcel_obj.dict()
                ),
                timeout=20.0,
            )

            if ctx:
                await ctx.report_progress(1, 1)

            return result
        except asyncio.TimeoutError:
            logger.error("Rates calculation timed out after 20 seconds")
            return {
                "status": "error",
                "data": None,
                "message": "Rates calculation timed out. Please try again.",
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
                "message": "Failed to retrieve rates",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

