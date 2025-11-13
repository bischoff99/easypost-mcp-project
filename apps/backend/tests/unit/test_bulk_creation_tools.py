"""Unit tests for shipment creation tools."""

from unittest.mock import AsyncMock, MagicMock

from src.mcp_server.tools.bulk_creation_tools import register_shipment_creation_tools


class TestShipmentCreationToolsRegistration:
    """Test shipment creation tools registration."""

    def test_register_shipment_creation_tools(self):
        """Test that tools are registered with MCP."""
        mock_mcp = MagicMock()
        mock_easypost_service = MagicMock()
        mock_easypost_service.create_shipment = AsyncMock()
        mock_easypost_service.client = MagicMock()

        register_shipment_creation_tools(mock_mcp, mock_easypost_service)

        # Should register two tools
        assert mock_mcp.tool.call_count == 2


# Note: Direct testing of MCP-decorated functions is complex due to decorator registration.
# The registration test above verifies that tools are properly registered with MCP.
# Integration tests in test_server_endpoints.py cover the actual functionality.
# Database integration tests verify that batch operations and shipments are properly stored.
