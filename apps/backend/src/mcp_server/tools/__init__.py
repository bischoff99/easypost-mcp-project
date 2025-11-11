"""MCP Tools registration."""

from src.mcp_server.tools.bulk_creation_tools import register_shipment_creation_tools
from src.mcp_server.tools.bulk_tools import register_shipment_tools
from src.mcp_server.tools.download_tools import register_download_tools
from src.mcp_server.tools.tracking_tools import register_tracking_tools


def register_tools(mcp, easypost_service):
    """
    Register all MCP tools with the server.

    Tools registered (5 total):
    - get_tracking: Get tracking information
    - get_shipment_rates: Get rates for single/multiple shipments
    - create_shipment: Create shipments (spreadsheet format, optional purchase)
    - buy_shipment_label: Purchase labels for pre-created shipments
    - download_shipment_documents: Download labels and customs forms for shipments
    """
    register_tracking_tools(mcp, easypost_service)
    register_shipment_tools(mcp, easypost_service)  # get_shipment_rates
    register_shipment_creation_tools(mcp, easypost_service)  # create_shipment, buy_shipment_label
    register_download_tools(mcp, easypost_service)  # download_shipment_documents
