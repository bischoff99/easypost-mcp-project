"""MCP Tools registration."""

from src.mcp_server.tools.bulk_creation_tools import register_bulk_creation_tools
from src.mcp_server.tools.bulk_tools import register_bulk_tools
from src.mcp_server.tools.rate_tools import register_rate_tools
from src.mcp_server.tools.shipment_tools import register_shipment_tools
from src.mcp_server.tools.tracking_tools import register_tracking_tools


def register_tools(mcp, easypost_service):
    """
    Register all MCP tools with the server.

    Tools registered:
    - create_shipment, get_tracking, get_rates (single operations)
    - parse_flexible_shipment, parse_and_get_bulk_rates (bulk parsing)
    - create_bulk_shipments, buy_bulk_shipments (bulk operations)
    """
    register_shipment_tools(mcp, easypost_service)
    register_tracking_tools(mcp, easypost_service)
    register_rate_tools(mcp, easypost_service)
    register_bulk_tools(mcp, easypost_service)  # Now includes parse_flexible_shipment
    register_bulk_creation_tools(mcp, easypost_service)
