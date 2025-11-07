"""MCP Resources registration."""

from src.mcp_server.resources.shipment_resources import register_shipment_resources
from src.mcp_server.resources.stats_resources import register_stats_resources


def register_resources(mcp, easypost_service):
    """Register all MCP resources with the server."""
    register_shipment_resources(mcp, easypost_service)
    register_stats_resources(mcp, easypost_service)
