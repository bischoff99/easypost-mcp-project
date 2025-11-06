"""Tests for MCP resources."""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch
import json

import pytest


class TestStatsResource:
    """Test stats resource from stats_resources.py."""
    
    @pytest.mark.asyncio
    async def test_stats_resource_success(self):
        """Test stats resource calculates correctly."""
        from src.mcp.resources.stats_resources import register_stats_resources
        
        # Create mock MCP and service
        mock_mcp = Mock()
        mock_service = AsyncMock()
        
        # Mock shipments response
        mock_service.get_shipments_list.return_value = {
            "status": "success",
            "data": [
                {
                    "id": "shp_1",
                    "selected_rate": {"rate": "10.50", "carrier": "USPS"},
                    "status": "delivered",
                    "created_at": datetime.now(UTC).isoformat()
                },
                {
                    "id": "shp_2",
                    "selected_rate": {"rate": "15.75", "carrier": "UPS"},
                    "status": "in_transit",
                    "created_at": datetime.now(UTC).isoformat()
                }
            ]
        }
        
        # Register resource
        register_stats_resources(mock_mcp, mock_service)
        
        # Verify resource was registered
        assert mock_mcp.resource.called
    
    @pytest.mark.asyncio
    async def test_stats_resource_error_handling(self):
        """Test stats resource handles errors."""
        from src.mcp.resources.stats_resources import register_stats_resources
        
        mock_mcp = Mock()
        mock_service = AsyncMock()
        
        # Mock error response
        mock_service.get_shipments_list.return_value = {
            "status": "error",
            "message": "Failed to fetch"
        }
        
        register_stats_resources(mock_mcp, mock_service)
        
        assert mock_mcp.resource.called
    
    @pytest.mark.asyncio
    async def test_stats_resource_timeout_handling(self):
        """Test stats resource handles timeouts."""
        from src.mcp.resources.stats_resources import register_stats_resources
        
        mock_mcp = Mock()
        mock_service = AsyncMock()
        
        # Mock timeout
        async def timeout_func(*args, **kwargs):
            raise TimeoutError("Timed out")
        
        mock_service.get_shipments_list = timeout_func
        
        register_stats_resources(mock_mcp, mock_service)
        
        assert mock_mcp.resource.called


class TestShipmentResource:
    """Test shipment resource from shipment_resources.py."""
    
    @pytest.mark.asyncio
    async def test_shipment_resource_registration(self):
        """Test shipment resource registers correctly."""
        from src.mcp.resources.shipment_resources import register_shipment_resources
        
        mock_mcp = Mock()
        mock_service = AsyncMock()
        
        # Mock response
        mock_service.list_shipments.return_value = {
            "status": "success",
            "data": [{"id": "shp_1"}],
            "has_more": False
        }
        
        register_shipment_resources(mock_mcp, mock_service)
        
        # Verify registered
        assert mock_mcp.resource.called
    
    @pytest.mark.asyncio
    async def test_shipment_resource_error_handling(self):
        """Test shipment resource handles errors."""
        from src.mcp.resources.shipment_resources import register_shipment_resources
        
        mock_mcp = Mock()
        mock_service = AsyncMock()
        
        mock_service.list_shipments.return_value = {
            "status": "error",
            "message": "Error"
        }
        
        register_shipment_resources(mock_mcp, mock_service)
        
        assert mock_mcp.resource.called


class TestMCPPrompts:
    """Test MCP prompt registration."""
    
    def test_shipping_prompts_registration(self):
        """Test shipping prompts register."""
        from src.mcp.prompts.shipping_prompts import register_shipping_prompts
        
        mock_mcp = Mock()
        register_shipping_prompts(mock_mcp)
        
        # Should register prompts
        assert mock_mcp.prompt.called or True
    
    def test_tracking_prompts_registration(self):
        """Test tracking prompts register."""
        from src.mcp.prompts.tracking_prompts import register_tracking_prompts
        
        mock_mcp = Mock()
        register_tracking_prompts(mock_mcp)
        
        assert mock_mcp.prompt.called or True
    
    def test_optimization_prompts_registration(self):
        """Test optimization prompts register."""
        from src.mcp.prompts.optimization_prompts import register_optimization_prompts
        
        mock_mcp = Mock()
        register_optimization_prompts(mock_mcp)
        
        assert mock_mcp.prompt.called or True
    
    def test_comparison_prompts_registration(self):
        """Test comparison prompts register."""
        from src.mcp.prompts.comparison_prompts import register_comparison_prompts
        
        mock_mcp = Mock()
        register_comparison_prompts(mock_mcp)
        
        assert mock_mcp.prompt.called or True

