"""Rate calculation MCP tool."""

import asyncio
import logging
from datetime import UTC, datetime

from fastmcp import Context
from fastmcp.exceptions import ToolError
from pydantic import ValidationError

from src.services.easypost_service import AddressModel, ParcelModel

logger = logging.getLogger(__name__)


def register_rate_tools(mcp, easypost_service=None):  # noqa: ARG001 - Uses Context instead
    """Register rate-related tools with MCP server."""

    @mcp.tool(tags=["rates", "shipping", "core"])
    async def get_rates(
        to_address: dict, from_address: dict, parcel: dict, ctx: Context | None = None
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
            # Get service from context lifespan (dict access)
            if ctx:
                lifespan_ctx = ctx.request_context.lifespan_context
                service = (
                    lifespan_ctx.get("easypost_service")
                    if isinstance(lifespan_ctx, dict)
                    else lifespan_ctx.easypost_service
                )
            elif easypost_service:
                service = easypost_service
            else:
                raise ToolError("EasyPost service not available. Check server configuration.")

            # Validate inputs
            to_addr = AddressModel(**to_address)
            from_addr = AddressModel(**from_address)
            parcel_obj = ParcelModel(**parcel)

            if ctx:
                await ctx.info("Calculating rates...")

            # Add timeout to prevent SSE timeout errors
            result = await asyncio.wait_for(
                service.get_rates(to_addr.dict(), from_addr.dict(), parcel_obj.dict()),
                timeout=20.0,
            )

            if ctx:
                await ctx.report_progress(1, 1)

            return result
        except TimeoutError:
            logger.error("Rates calculation timed out after 20 seconds")
            return {
                "status": "error",
                "data": None,
                "message": "Rates calculation timed out. Please try again.",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return {
                "status": "error",
                "data": None,
                "message": f"Validation error: {str(e)}",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except ToolError as e:
            logger.error(f"Tool error: {str(e)}")
            return {
                "status": "error",
                "data": None,
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            logger.error(f"Tool error: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "data": None,
                "message": f"Failed to retrieve rates: {str(e)}",
                "timestamp": datetime.now(UTC).isoformat(),
            }
