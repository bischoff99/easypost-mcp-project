"""
Template: FastMCP Tool
Usage: Copy pattern for new MCP tools

Replace:
- tool_name: Function name (snake_case)
- CATEGORY: Tool category (e.g., shipment, tracking)
- Parameters: Tool parameters
"""

from datetime import datetime, timezone
from fastmcp import Context
import logging

logger = logging.getLogger(__name__)


def register_CATEGORY_tools(mcp, service):
    """Register CATEGORY tools with MCP server."""

    @mcp.tool()
    async def tool_name(
        param1: str,
        param2: int = 10,
        ctx: Context = None,
    ) -> dict:
        """
        Tool description (shows in AI interface).

        Args:
            param1: Parameter description
            param2: Parameter description (default: 10)
            ctx: MCP context for progress reporting

        Returns:
            Standardized response with status, data, message, timestamp
        """
        try:
            if ctx:
                await ctx.info(f"Processing {param1}...")

            # TODO: Implement tool logic
            result = await service.process(param1, param2)

            if ctx:
                await ctx.info("Processing complete")

            return {
                "status": "success",
                "data": result,
                "message": "Operation completed successfully",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            logger.error(f"Tool error: {str(e)}")
            return {
                "status": "error",
                "data": None,
                "message": f"Failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
