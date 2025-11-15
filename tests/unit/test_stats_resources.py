"""Unit tests for statistics MCP resources."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.mcp_server.resources.stats_resources import register_stats_resources


class TestStatsResourcesRegistration:
    """Test statistics resources registration."""

    @pytest.fixture
    def mock_mcp(self):
        """Mock MCP server."""
        return MagicMock()

    @pytest.fixture
    def mock_easypost_service(self):
        """Mock EasyPost service."""
        service = MagicMock()
        service.get_shipments_list = AsyncMock()
        return service

    def test_register_stats_resources(self, mock_mcp, mock_easypost_service):
        """Test that stats resource is registered with MCP."""
        register_stats_resources(mock_mcp, mock_easypost_service)

        # Should register one resource
        assert mock_mcp.resource.call_count == 1

        # Check that the resource was registered with correct URI
        call_args = mock_mcp.resource.call_args
        assert call_args[0][0] == "easypost://stats/overview"


# Note: Direct testing of MCP-decorated functions is complex due to decorator registration.
# The registration test above verifies that resources are properly registered with MCP.
# Integration tests in test_server_endpoints.py cover the actual functionality.
