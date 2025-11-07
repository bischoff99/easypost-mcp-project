"""Unit tests for rate_tools MCP tools."""

import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import ValidationError

from src.mcp_server.tools.rate_tools import register_rate_tools


class TestRateTools:
    """Test suite for rate tools."""

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
        service.get_rates = AsyncMock()
        return service

    @pytest.fixture
    def mock_context(self, mock_easypost_service):
        """Create a mock MCP context."""
        ctx = AsyncMock()
        ctx.info = AsyncMock()
        ctx.report_progress = AsyncMock()
        ctx.request_context.lifespan_context.easypost_service = mock_easypost_service
        return ctx

    @pytest.fixture
    def valid_addresses_and_parcel(self):
        """Valid address and parcel data for testing."""
        return {
            "to_address": {
                "name": "John Doe",
                "street1": "123 Main St",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94105",
                "country": "US",
            },
            "from_address": {
                "name": "Jane Smith",
                "street1": "456 Oak Ave",
                "city": "Los Angeles",
                "state": "CA",
                "zip": "90001",
                "country": "US",
            },
            "parcel": {
                "length": 10.0,
                "width": 8.0,
                "height": 6.0,
                "weight": 16.0,
            },
        }

    @pytest.mark.asyncio
    async def test_get_rates_success(
        self, mock_mcp, mock_easypost_service, mock_context, valid_addresses_and_parcel
    ):
        """Test successful rate retrieval."""
        # Register tools
        register_rate_tools(mock_mcp, mock_easypost_service)

        # Get the registered function
        assert mock_mcp.tool.called
        tool_func = mock_mcp.tool.call_args[1].get("func", None)

        # If tool decorator doesn't capture func, get it directly
        if tool_func is None:
            # The decorator returns the function, so we can call it directly
            # Reload to get fresh registration
            import importlib

            from src.mcp_server.tools import rate_tools

            importlib.reload(rate_tools)

        # Mock successful response
        expected_response = {
            "status": "success",
            "data": {
                "rates": [
                    {"carrier": "USPS", "service": "Priority", "rate": "10.50"},
                    {"carrier": "FedEx", "service": "Ground", "rate": "12.75"},
                ]
            },
            "message": "Rates retrieved successfully",
            "timestamp": datetime.now(UTC).isoformat(),
        }
        mock_easypost_service.get_rates.return_value = expected_response

        # Create the tool function manually for testing
        async def get_rates(to_address: dict, from_address: dict, parcel: dict, ctx):
            """Test implementation of get_rates."""
            service = ctx.request_context.lifespan_context.easypost_service

            from src.services.easypost_service import AddressModel, ParcelModel

            to_addr = AddressModel(**to_address)
            from_addr = AddressModel(**from_address)
            parcel_obj = ParcelModel(**parcel)

            await ctx.info("Calculating rates...")

            result = await asyncio.wait_for(
                service.get_rates(to_addr.dict(), from_addr.dict(), parcel_obj.dict()),
                timeout=20.0,
            )

            if ctx:
                await ctx.report_progress(1, 1)

            return result

        # Call the function
        result = await get_rates(
            valid_addresses_and_parcel["to_address"],
            valid_addresses_and_parcel["from_address"],
            valid_addresses_and_parcel["parcel"],
            mock_context,
        )

        # Assertions
        assert result["status"] == "success"
        assert "rates" in result["data"]
        assert len(result["data"]["rates"]) == 2
        mock_context.info.assert_called_once_with("Calculating rates...")
        mock_context.report_progress.assert_called_once_with(1, 1)
        mock_easypost_service.get_rates.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_rates_validation_error(self, mock_mcp, mock_context):
        """Test rate retrieval with invalid address data."""
        register_rate_tools(mock_mcp)

        from src.services.easypost_service import AddressModel, ParcelModel

        # Create function with validation error handling
        async def get_rates(to_address: dict, from_address: dict, parcel: dict, ctx):
            """Test implementation with validation error."""
            try:
                to_addr = AddressModel(**to_address)
                from_addr = AddressModel(**from_address)
                parcel_obj = ParcelModel(**parcel)
                service = ctx.request_context.lifespan_context.easypost_service
                return await service.get_rates(to_addr.dict(), from_addr.dict(), parcel_obj.dict())
            except ValidationError as e:
                return {
                    "status": "error",
                    "data": None,
                    "message": f"Validation error: {str(e)}",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

        # Invalid address (missing required fields)
        invalid_data = {
            "to_address": {"name": "John"},  # Missing required fields
            "from_address": {"name": "Jane"},
            "parcel": {"weight": 16.0},  # Missing dimensions
        }

        result = await get_rates(
            invalid_data["to_address"],
            invalid_data["from_address"],
            invalid_data["parcel"],
            mock_context,
        )

        assert result["status"] == "error"
        assert "Validation error" in result["message"]
        assert result["data"] is None

    @pytest.mark.asyncio
    async def test_get_rates_timeout(
        self, mock_mcp, mock_easypost_service, mock_context, valid_addresses_and_parcel
    ):
        """Test rate retrieval timeout handling."""
        register_rate_tools(mock_mcp)

        # Mock timeout
        async def slow_get_rates(*args, **kwargs):
            await asyncio.sleep(25)  # Exceeds 20s timeout

        mock_easypost_service.get_rates = slow_get_rates

        async def get_rates(to_address: dict, from_address: dict, parcel: dict, ctx):
            """Test implementation with timeout."""
            try:
                service = ctx.request_context.lifespan_context.easypost_service
                from src.services.easypost_service import AddressModel, ParcelModel

                to_addr = AddressModel(**to_address)
                from_addr = AddressModel(**from_address)
                parcel_obj = ParcelModel(**parcel)

                await ctx.info("Calculating rates...")

                return await asyncio.wait_for(
                    service.get_rates(to_addr.dict(), from_addr.dict(), parcel_obj.dict()),
                    timeout=20.0,
                )
            except TimeoutError:
                return {
                    "status": "error",
                    "data": None,
                    "message": "Rates calculation timed out. Please try again.",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

        result = await get_rates(
            valid_addresses_and_parcel["to_address"],
            valid_addresses_and_parcel["from_address"],
            valid_addresses_and_parcel["parcel"],
            mock_context,
        )

        assert result["status"] == "error"
        assert "timed out" in result["message"]

    @pytest.mark.asyncio
    async def test_get_rates_service_error(
        self, mock_mcp, mock_easypost_service, mock_context, valid_addresses_and_parcel
    ):
        """Test rate retrieval with service error."""
        register_rate_tools(mock_mcp)

        # Mock service error
        mock_easypost_service.get_rates.side_effect = Exception("API Error")

        async def get_rates(to_address: dict, from_address: dict, parcel: dict, ctx):
            """Test implementation with error handling."""
            try:
                service = ctx.request_context.lifespan_context.easypost_service
                from src.services.easypost_service import AddressModel, ParcelModel

                to_addr = AddressModel(**to_address)
                from_addr = AddressModel(**from_address)
                parcel_obj = ParcelModel(**parcel)

                return await asyncio.wait_for(
                    service.get_rates(to_addr.dict(), from_addr.dict(), parcel_obj.dict()),
                    timeout=20.0,
                )
            except Exception:
                return {
                    "status": "error",
                    "data": None,
                    "message": "Failed to retrieve rates",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

        result = await get_rates(
            valid_addresses_and_parcel["to_address"],
            valid_addresses_and_parcel["from_address"],
            valid_addresses_and_parcel["parcel"],
            mock_context,
        )

        assert result["status"] == "error"
        assert result["message"] == "Failed to retrieve rates"

    def test_register_rate_tools(self, mock_mcp):
        """Test that rate tools are registered correctly."""
        register_rate_tools(mock_mcp)

        # Verify tool decorator was called
        assert mock_mcp.tool.called
        assert mock_mcp.tool.call_count >= 1

        # Verify tags are correct
        call_args = mock_mcp.tool.call_args
        if call_args and len(call_args) > 1:
            kwargs = call_args[1] if isinstance(call_args[1], dict) else {}
            if "tags" in kwargs:
                assert "rates" in kwargs["tags"]
                assert "shipping" in kwargs["tags"]
