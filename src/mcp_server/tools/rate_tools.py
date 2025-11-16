"""Rate calculation MCP tool."""

import asyncio
import logging
from datetime import UTC, datetime

from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError
from pydantic import ValidationError

from src.mcp_server.tools._utils import resolve_service
from src.services.easypost_service import AddressModel, EasyPostService, ParcelModel
from src.utils.constants import STANDARD_TIMEOUT

logger = logging.getLogger(__name__)


def register_rate_tools(
    mcp: FastMCP, easypost_service: EasyPostService | None = None
) -> None:  # noqa: ARG001 - Uses Context instead
    """Register rate-related tools with MCP server."""

    @mcp.tool(
        tags={"rates", "shipping", "core"},
        annotations={
            "readOnlyHint": True,
            "idempotentHint": True,
        },
    )
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
            # Resolve service from context or injected instance
            service = resolve_service(ctx, easypost_service)

            # Validate inputs
            to_addr = AddressModel(**to_address)
            from_addr = AddressModel(**from_address)
            parcel_obj = ParcelModel(**parcel)

            if ctx:
                await ctx.info("Calculating rates...")

            # Add timeout to prevent SSE timeout errors
            result = await asyncio.wait_for(
                service.get_rates(
                    to_addr.model_dump(),
                    from_addr.model_dump(),
                    parcel_obj.model_dump(),
                ),
                timeout=STANDARD_TIMEOUT,
            )

            if ctx:
                await ctx.report_progress(1, 1)

            return result
        except TimeoutError:
            logger.error(
                f"Rates calculation timed out after {STANDARD_TIMEOUT} seconds"
            )
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
