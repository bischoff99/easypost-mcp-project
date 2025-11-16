"""MCP Tools registration.

Organized by category:
1. Core Tools: Simple, single-purpose operations (dict inputs)
2. Bulk Tools: Advanced operations for multiple shipments (spreadsheet format)
3. Management Tools: Document management and refunds

Tool Categories:
- Core: get_tracking, get_rates (simple rate lookup)
- Bulk: get_shipment_rates, create_shipment, buy_shipment_label
- Management: download_shipment_documents, refund_shipment
"""

from fastmcp import FastMCP

from src.mcp_server.tools.bulk_creation_tools import register_shipment_creation_tools
from src.mcp_server.tools.bulk_tools import register_shipment_tools
from src.mcp_server.tools.download_tools import register_download_tools
from src.mcp_server.tools.rate_tools import register_rate_tools
from src.mcp_server.tools.refund_tools import register_refund_tools
from src.mcp_server.tools.tracking_tools import register_tracking_tools
from src.services.easypost_service import EasyPostService


def register_tools(mcp: FastMCP, easypost_service: EasyPostService | None) -> None:
    """
    Register all MCP tools with the server, organized by category.

    Tools registered (7 total):

    CORE TOOLS (Simple, single-purpose operations):
    - get_tracking: Get tracking information for a shipment
    - get_rates: Get shipping rates for a single shipment (dict inputs)

    BULK TOOLS (Advanced, spreadsheet-format operations):
    - get_shipment_rates: Get rates for single/multiple shipments (spreadsheet format)
    - create_shipment: Create shipments (spreadsheet format, Phase 1 - no purchase)
    - buy_shipment_label: Purchase labels for pre-created shipments (Phase 2 - destructive)

    MANAGEMENT TOOLS (Document and lifecycle management):
    - download_shipment_documents: Download labels and customs forms for shipments
    - refund_shipment: Refund single or multiple shipments (destructive)

    Registration order:
    1. Core tools (most commonly used)
    2. Bulk tools (advanced workflows)
    3. Management tools (post-creation operations)
    """
    # Core Tools: Simple, single-purpose operations
    register_tracking_tools(mcp, easypost_service)  # get_tracking
    register_rate_tools(mcp, easypost_service)  # get_rates

    # Bulk Tools: Advanced, spreadsheet-format operations
    register_shipment_tools(mcp, easypost_service)  # get_shipment_rates
    register_shipment_creation_tools(
        mcp, easypost_service
    )  # create_shipment, buy_shipment_label

    # Management Tools: Document and lifecycle management
    register_download_tools(mcp, easypost_service)  # download_shipment_documents
    register_refund_tools(mcp, easypost_service)  # refund_shipment
