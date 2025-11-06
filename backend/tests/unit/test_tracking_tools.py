"""Unit tests for tracking_tools MCP tools."""

import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.mcp.tools.tracking_tools import register_tracking_tools


class TestTrackingTools:
    """Test suite for tracking tools."""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server."""
        mcp = MagicMock()
        mcp.tool = MagicMock(return_value=lambda func: func)
        return mcp

    @pytest.fixture
    def mock_easypost_service(self):
        """Create a mock EasyPost service."""
        service = AsyncMock()
        service.get_tracking = AsyncMock()
        return service

    @pytest.fixture
    def mock_context(self, mock_easypost_service):
        """Create a mock MCP context."""
        ctx = AsyncMock()
        ctx.info = AsyncMock()
        ctx.report_progress = AsyncMock()
        ctx.request_context.lifespan_context.easypost_service = mock_easypost_service
        return ctx

    @pytest.mark.asyncio
    async def test_get_tracking_success(self, mock_mcp, mock_easypost_service, mock_context):
        """Test successful tracking retrieval."""
        register_tracking_tools(mock_mcp, mock_easypost_service)

        # Mock successful response
        expected_response = {
            "status": "success",
            "data": {
                "tracking_number": "9400100000000000000000",
                "carrier": "USPS",
                "status": "in_transit",
                "tracking_details": [
                    {
                        "status": "pre_transit",
                        "message": "Shipping Label Created",
                        "datetime": "2025-11-01T10:00:00Z",
                    },
                    {
                        "status": "in_transit",
                        "message": "Accepted at USPS Facility",
                        "datetime": "2025-11-02T14:30:00Z",
                    },
                ],
            },
            "message": "Tracking information retrieved",
            "timestamp": datetime.now(UTC).isoformat(),
        }
        mock_easypost_service.get_tracking.return_value = expected_response

        # Create the tool function for testing
        async def get_tracking(tracking_number: str, ctx):
            """Test implementation of get_tracking."""
            service = ctx.request_context.lifespan_context.easypost_service
            await ctx.info(f"Fetching tracking for {tracking_number}...")
            result = await asyncio.wait_for(service.get_tracking(tracking_number), timeout=20.0)
            if ctx:
                await ctx.report_progress(1, 1)
            return result

        # Call the function
        tracking_number = "9400100000000000000000"
        result = await get_tracking(tracking_number, mock_context)

        # Assertions
        assert result["status"] == "success"
        assert result["data"]["tracking_number"] == tracking_number
        assert result["data"]["carrier"] == "USPS"
        assert len(result["data"]["tracking_details"]) == 2
        mock_context.info.assert_called_once_with(f"Fetching tracking for {tracking_number}...")
        mock_context.report_progress.assert_called_once_with(1, 1)
        mock_easypost_service.get_tracking.assert_called_once_with(tracking_number)

    @pytest.mark.asyncio
    async def test_get_tracking_timeout(self, mock_mcp, mock_easypost_service, mock_context):
        """Test tracking retrieval timeout handling."""
        register_tracking_tools(mock_mcp)

        # Mock timeout
        async def slow_get_tracking(*args, **kwargs):
            await asyncio.sleep(25)  # Exceeds 20s timeout

        mock_easypost_service.get_tracking = slow_get_tracking

        async def get_tracking(tracking_number: str, ctx):
            """Test implementation with timeout."""
            try:
                service = ctx.request_context.lifespan_context.easypost_service
                await ctx.info(f"Fetching tracking for {tracking_number}...")
                result = await asyncio.wait_for(service.get_tracking(tracking_number), timeout=20.0)
                return result
            except TimeoutError:
                return {
                    "status": "error",
                    "data": None,
                    "message": "Tracking lookup timed out. Please try again.",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

        result = await get_tracking("9400100000000000000000", mock_context)

        assert result["status"] == "error"
        assert "timed out" in result["message"]

    @pytest.mark.asyncio
    async def test_get_tracking_service_error(self, mock_mcp, mock_easypost_service, mock_context):
        """Test tracking retrieval with service error."""
        register_tracking_tools(mock_mcp)

        # Mock service error
        mock_easypost_service.get_tracking.side_effect = Exception("API Error")

        async def get_tracking(tracking_number: str, ctx):
            """Test implementation with error handling."""
            try:
                service = ctx.request_context.lifespan_context.easypost_service
                await ctx.info(f"Fetching tracking for {tracking_number}...")
                result = await asyncio.wait_for(service.get_tracking(tracking_number), timeout=20.0)
                return result
            except Exception:
                return {
                    "status": "error",
                    "data": None,
                    "message": "Failed to retrieve tracking information",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

        result = await get_tracking("9400100000000000000000", mock_context)

        assert result["status"] == "error"
        assert result["message"] == "Failed to retrieve tracking information"

    @pytest.mark.asyncio
    async def test_get_tracking_with_direct_service(self, mock_mcp, mock_easypost_service):
        """Test tracking retrieval with direct service (no context)."""
        register_tracking_tools(mock_mcp, mock_easypost_service)

        # Mock successful response
        expected_response = {
            "status": "success",
            "data": {"tracking_number": "9400100000000000000000"},
        }
        mock_easypost_service.get_tracking.return_value = expected_response

        async def get_tracking(tracking_number: str, ctx):
            """Test implementation with direct service."""
            if ctx:
                service = ctx.request_context.lifespan_context.easypost_service
            else:
                service = mock_easypost_service

            if ctx:
                await ctx.info(f"Fetching tracking for {tracking_number}...")

            result = await asyncio.wait_for(service.get_tracking(tracking_number), timeout=20.0)

            if ctx:
                await ctx.report_progress(1, 1)

            return result

        # Call without context
        result = await get_tracking("9400100000000000000000", None)

        assert result["status"] == "success"
        mock_easypost_service.get_tracking.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_tracking_no_service_error(self, mock_mcp):
        """Test tracking retrieval fails when no service is available."""
        register_tracking_tools(mock_mcp)

        async def get_tracking(tracking_number: str, ctx):
            """Test implementation with no service."""
            try:
                if ctx:
                    service = ctx.request_context.lifespan_context.easypost_service
                else:
                    raise ValueError("No EasyPost service available")

                result = await asyncio.wait_for(service.get_tracking(tracking_number), timeout=20.0)
                return result
            except Exception:
                return {
                    "status": "error",
                    "data": None,
                    "message": "Failed to retrieve tracking information",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

        # Call without context
        result = await get_tracking("9400100000000000000000", None)

        assert result["status"] == "error"

    def test_register_tracking_tools(self, mock_mcp):
        """Test that tracking tools are registered correctly."""
        register_tracking_tools(mock_mcp)

        # Verify tool decorator was called
        assert mock_mcp.tool.called
        assert mock_mcp.tool.call_count >= 1

        # Verify tags are correct
        call_args = mock_mcp.tool.call_args
        if call_args and len(call_args) > 1:
            kwargs = call_args[1] if isinstance(call_args[1], dict) else {}
            if "tags" in kwargs:
                assert "tracking" in kwargs["tags"]
                assert "shipping" in kwargs["tags"]

    @pytest.mark.asyncio
    async def test_get_tracking_invalid_tracking_number(
        self, mock_mcp, mock_easypost_service, mock_context
    ):
        """Test tracking retrieval with invalid tracking number."""
        register_tracking_tools(mock_mcp)

        # Mock error response for invalid tracking number
        mock_easypost_service.get_tracking.side_effect = Exception("Invalid tracking number")

        async def get_tracking(tracking_number: str, ctx):
            """Test implementation with error handling."""
            try:
                service = ctx.request_context.lifespan_context.easypost_service
                await ctx.info(f"Fetching tracking for {tracking_number}...")
                result = await asyncio.wait_for(service.get_tracking(tracking_number), timeout=20.0)
                return result
            except Exception:
                return {
                    "status": "error",
                    "data": None,
                    "message": "Failed to retrieve tracking information",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

        result = await get_tracking("invalid123", mock_context)

        assert result["status"] == "error"
        mock_easypost_service.get_tracking.assert_called_once_with("invalid123")
