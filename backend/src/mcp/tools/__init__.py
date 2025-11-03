"""MCP Tools registration."""

from src.mcp.tools.shipment_tools import register_shipment_tools
from src.mcp.tools.tracking_tools import register_tracking_tools
from src.mcp.tools.rate_tools import register_rate_tools


def register_tools(mcp, easypost_service):
    """Register all MCP tools with the server."""
    register_shipment_tools(mcp, easypost_service)
    register_tracking_tools(mcp, easypost_service)
    register_rate_tools(mcp, easypost_service)

