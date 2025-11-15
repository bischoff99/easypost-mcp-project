"""Tracking lookup MCP tool."""

import asyncio
import logging
from datetime import UTC, datetime

from fastmcp import Context
from fastmcp.exceptions import ToolError

from src.utils.constants import STANDARD_TIMEOUT

logger = logging.getLogger(__name__)


def register_tracking_tools(mcp, easypost_service=None):
    """Register tracking-related tools with MCP server."""

    @mcp.tool(
        tags=["tracking", "shipping", "core"],
        annotations={
            "readOnlyHint": True,
            "idempotentHint": True,
        },
    )
    async def get_tracking(tracking_number: str, ctx: Context | None = None) -> dict:
        """
        Get real-time tracking information for a shipment.

        Args:
            tracking_number: The tracking number to look up

        Returns:
            Standardized response with tracking data
        """
        try:
            # Get service from context or use provided
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

            if ctx:
                await ctx.info(f"Fetching tracking for {tracking_number}...")

            # Add timeout to prevent SSE timeout errors
            result = await asyncio.wait_for(service.get_tracking(tracking_number), timeout=STANDARD_TIMEOUT)

            if ctx:
                await ctx.report_progress(1, 1)

            return result
        except TimeoutError:
            logger.error(f"Tracking lookup timed out after {STANDARD_TIMEOUT} seconds")
            return {
                "status": "error",
                "data": None,
                "message": "Tracking lookup timed out. Please try again.",
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
                "message": f"Failed to retrieve tracking information: {str(e)}",
                "timestamp": datetime.now(UTC).isoformat(),
            }
