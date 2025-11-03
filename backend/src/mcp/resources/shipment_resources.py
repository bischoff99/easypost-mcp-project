"""Shipment-related MCP resources."""

import asyncio
import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def register_shipment_resources(mcp, easypost_service):
    """Register shipment resources with MCP server."""

    @mcp.resource("easypost://shipments/recent")
    async def get_recent_shipments_resource() -> str:
        """Get list of recent shipments from EasyPost API."""
        try:
            # Add timeout to prevent SSE timeout errors
            result = await asyncio.wait_for(
                easypost_service.get_shipments_list(
                    page_size=10, purchased=True  # Get last 10 purchased shipments
                ),
                timeout=15.0,
            )
            return json.dumps(result, indent=2)
        except asyncio.TimeoutError:
            logger.error("Recent shipments resource timed out after 15 seconds")
            return json.dumps(
                {
                    "status": "error",
                    "message": "Request timed out. Please try again.",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
                indent=2,
            )
        except Exception as e:
            logger.error(f"Resource error: {str(e)}")
            return json.dumps(
                {
                    "status": "error",
                    "message": "Failed to retrieve recent shipments",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
                indent=2,
            )

