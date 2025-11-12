<<<<<<< HEAD
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
||||||| 7a576da
=======
"""MCP Tools registration."""

from src.mcp_server.tools.bulk_creation_tools import register_bulk_creation_tools
from src.mcp_server.tools.bulk_tools import register_bulk_tools
from src.mcp_server.tools.tracking_tools import register_tracking_tools


def register_tools(mcp, easypost_service):
    """
    Register all MCP tools with the server.

    Tools registered (4 total):
    - get_tracking: Get tracking information
    - parse_and_get_bulk_rates: Get rates for single/multiple shipments
    - create_bulk_shipments: Create shipments (spreadsheet format, optional purchase)
    - buy_bulk_shipments: Purchase labels for pre-created shipments

    Note: Bulk tools handle single shipments (1 line = 1 shipment),
    so separate single tools removed.
    """
    register_tracking_tools(mcp, easypost_service)
    register_bulk_tools(mcp, easypost_service)  # parse_and_get_bulk_rates
    register_bulk_creation_tools(mcp, easypost_service)  # create_bulk_shipments, buy_bulk_shipments
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8
