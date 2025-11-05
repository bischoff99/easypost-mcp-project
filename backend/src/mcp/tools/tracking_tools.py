"""Tracking lookup MCP tool."""

import asyncio
import logging
from datetime import UTC, datetime

from fastmcp import Context

logger = logging.getLogger(__name__)


def register_tracking_tools(mcp, easypost_service=None):
    """Register tracking-related tools with MCP server."""

    @mcp.tool(tags=["tracking", "shipping", "core"])
    async def get_tracking(tracking_number: str, ctx: Context) -> dict:
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
                service = ctx.request_context.lifespan_context.easypost_service
            elif easypost_service:
                service = easypost_service
            else:
                raise ValueError("No EasyPost service available")

            await ctx.info(f"Fetching tracking for {tracking_number}...")

            # Add timeout to prevent SSE timeout errors
            result = await asyncio.wait_for(service.get_tracking(tracking_number), timeout=20.0)

            if ctx:
                await ctx.report_progress(1, 1)

            return result
        except TimeoutError:
            logger.error("Tracking lookup timed out after 20 seconds")
            return {
                "status": "error",
                "data": None,
                "message": "Tracking lookup timed out. Please try again.",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            logger.error(f"Tool error: {str(e)}")
            return {
                "status": "error",
                "data": None,
                "message": "Failed to retrieve tracking information",
                "timestamp": datetime.now(UTC).isoformat(),
            }
