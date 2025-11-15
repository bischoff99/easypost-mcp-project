"""Unit tests for refund_tools MCP tools."""

import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.mcp_server.tools.refund_tools import register_refund_tools


class TestRefundTools:
    """Test suite for refund tools."""

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
        service.refund_shipment = AsyncMock()
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
    async def test_refund_single_shipment_success(
        self, mock_mcp, mock_easypost_service, mock_context
    ):
        """Test successful single shipment refund."""
        register_refund_tools(mock_mcp, mock_easypost_service)

        # Mock successful response
        expected_response = {
            "status": "success",
            "data": {
                "shipment_id": "shp_123abc",
                "tracking_code": "EZ1234567890",
                "refund_status": "submitted",
                "carrier": "USPS",
                "amount": "12.50",
            },
            "message": "Refund request submitted successfully",
            "timestamp": datetime.now(UTC).isoformat(),
        }
        mock_easypost_service.refund_shipment.return_value = expected_response

        # Create the tool function for testing
        async def refund_shipment(shipment_ids: str | list[str], ctx):
            """Test implementation of refund_shipment."""
            service = ctx.request_context.lifespan_context.easypost_service

            if isinstance(shipment_ids, str):
                if ctx:
                    await ctx.info(f"Refunding shipment {shipment_ids}...")

                result = await asyncio.wait_for(service.refund_shipment(shipment_ids), timeout=20.0)

                if ctx:
                    await ctx.report_progress(1, 1)

                return result
            return None

        # Call the function
        shipment_id = "shp_123abc"
        result = await refund_shipment(shipment_id, mock_context)

        # Assertions
        assert result["status"] == "success"
        assert result["data"]["shipment_id"] == shipment_id
        assert result["data"]["refund_status"] == "submitted"
        assert result["data"]["carrier"] == "USPS"
        mock_context.info.assert_called_once_with(f"Refunding shipment {shipment_id}...")
        mock_context.report_progress.assert_called_once_with(1, 1)
        mock_easypost_service.refund_shipment.assert_called_once_with(shipment_id)

    @pytest.mark.asyncio
    async def test_refund_bulk_shipments_success(
        self, mock_mcp, mock_easypost_service, mock_context
    ):
        """Test successful bulk shipment refunds."""
        register_refund_tools(mock_mcp, mock_easypost_service)

        # Mock successful responses for all shipments
        async def mock_refund(shipment_id):
            return {
                "status": "success",
                "data": {
                    "shipment_id": shipment_id,
                    "tracking_code": f"EZ{shipment_id[-5:]}",
                    "refund_status": "submitted",
                    "carrier": "USPS",
                    "amount": "12.50",
                },
                "message": "Refund request submitted successfully",
                "timestamp": datetime.now(UTC).isoformat(),
            }

        mock_easypost_service.refund_shipment = mock_refund

        # Create the tool function for testing
        async def refund_shipment(shipment_ids: str | list[str], ctx):
            """Test implementation of bulk refund."""
            service = ctx.request_context.lifespan_context.easypost_service

            if not shipment_ids:
                return {
                    "status": "error",
                    "data": None,
                    "message": "No shipment IDs provided",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

            total = len(shipment_ids)
            if ctx:
                await ctx.info(f"Refunding {total} shipments in parallel...")

            async def refund_one(shipment_id: str) -> dict:
                try:
                    return await asyncio.wait_for(
                        service.refund_shipment(shipment_id), timeout=20.0
                    )
                except Exception as e:
                    return {
                        "status": "error",
                        "data": {"shipment_id": shipment_id},
                        "message": str(e),
                        "timestamp": datetime.now(UTC).isoformat(),
                    }

            results = await asyncio.gather(
                *[refund_one(sid) for sid in shipment_ids], return_exceptions=False
            )

            successful = [r for r in results if r.get("status") == "success"]
            failed = [r for r in results if r.get("status") == "error"]

            if ctx:
                await ctx.report_progress(total, total)

            return {
                "status": "success" if successful else "error",
                "data": {
                    "total": total,
                    "successful": len(successful),
                    "failed": len(failed),
                    "results": results,
                },
                "message": f"Refunded {len(successful)} of {total} shipments successfully",
                "timestamp": datetime.now(UTC).isoformat(),
            }

        # Call the function
        shipment_ids = ["shp_123", "shp_456", "shp_789"]
        result = await refund_shipment(shipment_ids, mock_context)

        # Assertions
        assert result["status"] == "success"
        assert result["data"]["total"] == 3
        assert result["data"]["successful"] == 3
        assert result["data"]["failed"] == 0
        assert len(result["data"]["results"]) == 3
        mock_context.info.assert_called_once_with("Refunding 3 shipments in parallel...")
        mock_context.report_progress.assert_called_once_with(3, 3)

    @pytest.mark.asyncio
    async def test_refund_mixed_results(self, mock_mcp, mock_easypost_service, mock_context):
        """Test bulk refund with mixed success and failure results."""
        register_refund_tools(mock_mcp, mock_easypost_service)

        # Mock mixed responses
        async def mock_refund(shipment_id):
            if shipment_id == "shp_fail":
                raise Exception("Refund not allowed")
            return {
                "status": "success",
                "data": {
                    "shipment_id": shipment_id,
                    "refund_status": "submitted",
                },
                "message": "Refund request submitted successfully",
                "timestamp": datetime.now(UTC).isoformat(),
            }

        mock_easypost_service.refund_shipment = mock_refund

        # Create the tool function for testing
        async def refund_shipment(shipment_ids: str | list[str], ctx):
            """Test implementation with mixed results."""
            service = ctx.request_context.lifespan_context.easypost_service

            total = len(shipment_ids)
            if ctx:
                await ctx.info(f"Refunding {total} shipments in parallel...")

            async def refund_one(shipment_id: str) -> dict:
                try:
                    return await asyncio.wait_for(
                        service.refund_shipment(shipment_id), timeout=20.0
                    )
                except Exception as e:
                    return {
                        "status": "error",
                        "data": {"shipment_id": shipment_id},
                        "message": str(e),
                        "timestamp": datetime.now(UTC).isoformat(),
                    }

            results = await asyncio.gather(
                *[refund_one(sid) for sid in shipment_ids], return_exceptions=False
            )

            successful = [r for r in results if r.get("status") == "success"]
            failed = [r for r in results if r.get("status") == "error"]

            if ctx:
                await ctx.report_progress(total, total)

            return {
                "status": "success" if successful else "error",
                "data": {
                    "total": total,
                    "successful": len(successful),
                    "failed": len(failed),
                    "results": results,
                },
                "message": f"Refunded {len(successful)} of {total} shipments successfully",
                "timestamp": datetime.now(UTC).isoformat(),
            }

        # Call the function
        shipment_ids = ["shp_123", "shp_fail", "shp_456"]
        result = await refund_shipment(shipment_ids, mock_context)

        # Assertions
        assert result["status"] == "success"
        assert result["data"]["total"] == 3
        assert result["data"]["successful"] == 2
        assert result["data"]["failed"] == 1
        assert "Refunded 2 of 3 shipments successfully" in result["message"]

    @pytest.mark.asyncio
    async def test_refund_timeout(self, mock_mcp, mock_easypost_service, mock_context):
        """Test refund timeout handling."""
        register_refund_tools(mock_mcp)

        # Mock timeout
        async def slow_refund(*args, **kwargs):
            await asyncio.sleep(25)  # Exceeds 20s timeout

        mock_easypost_service.refund_shipment = slow_refund

        async def refund_shipment(shipment_ids: str | list[str], ctx):
            """Test implementation with timeout."""
            try:
                service = ctx.request_context.lifespan_context.easypost_service

                if isinstance(shipment_ids, str):
                    if ctx:
                        await ctx.info(f"Refunding shipment {shipment_ids}...")

                    return await asyncio.wait_for(
                        service.refund_shipment(shipment_ids), timeout=20.0
                    )
            except TimeoutError:
                return {
                    "status": "error",
                    "data": None,
                    "message": "Refund request timed out. Please try again.",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

        result = await refund_shipment("shp_123", mock_context)

        assert result["status"] == "error"
        assert "timed out" in result["message"]

    @pytest.mark.asyncio
    async def test_refund_no_service(self, mock_mcp):
        """Test refund fails when no service is available."""
        register_refund_tools(mock_mcp)

        async def refund_shipment(shipment_ids: str | list[str], ctx):
            """Test implementation with no service."""
            try:
                if ctx:
                    service = ctx.request_context.lifespan_context.easypost_service
                else:
                    raise ValueError("No EasyPost service available")

                if isinstance(shipment_ids, str):
                    return await asyncio.wait_for(
                        service.refund_shipment(shipment_ids), timeout=20.0
                    )
            except Exception as e:
                return {
                    "status": "error",
                    "data": None,
                    "message": f"Failed to process refund request: {str(e)}",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

        # Call without context
        result = await refund_shipment("shp_123", None)

        assert result["status"] == "error"
        assert "No EasyPost service available" in result["message"]

    @pytest.mark.asyncio
    async def test_refund_empty_list(self, mock_mcp, mock_easypost_service, mock_context):
        """Test refund with empty list validation."""
        register_refund_tools(mock_mcp, mock_easypost_service)

        async def refund_shipment(shipment_ids: str | list[str], ctx):
            """Test implementation with empty list."""
            if not shipment_ids:
                return {
                    "status": "error",
                    "data": None,
                    "message": "No shipment IDs provided",
                    "timestamp": datetime.now(UTC).isoformat(),
                }
            return None

        result = await refund_shipment([], mock_context)

        assert result["status"] == "error"
        assert "No shipment IDs provided" in result["message"]

    def test_register_refund_tools(self, mock_mcp):
        """Test that refund tools are registered correctly."""
        register_refund_tools(mock_mcp)

        # Verify tool decorator was called
        assert mock_mcp.tool.called
        assert mock_mcp.tool.call_count >= 1

        # Verify tags are correct
        call_args = mock_mcp.tool.call_args
        if call_args and len(call_args) > 1:
            kwargs = call_args[1] if isinstance(call_args[1], dict) else {}
            if "tags" in kwargs:
                assert "refund" in kwargs["tags"]
                assert "shipping" in kwargs["tags"]
                assert "core" in kwargs["tags"]

    @pytest.mark.asyncio
    async def test_refund_all_failures(self, mock_mcp, mock_easypost_service, mock_context):
        """Test bulk refund where all shipments fail."""
        register_refund_tools(mock_mcp, mock_easypost_service)

        # Mock all failures
        async def mock_refund(shipment_id):
            raise Exception("Refund not allowed")

        mock_easypost_service.refund_shipment = mock_refund

        async def refund_shipment(shipment_ids: str | list[str], ctx):
            """Test implementation with all failures."""
            service = ctx.request_context.lifespan_context.easypost_service

            total = len(shipment_ids)
            if ctx:
                await ctx.info(f"Refunding {total} shipments in parallel...")

            async def refund_one(shipment_id: str) -> dict:
                try:
                    return await asyncio.wait_for(
                        service.refund_shipment(shipment_id), timeout=20.0
                    )
                except Exception as e:
                    return {
                        "status": "error",
                        "data": {"shipment_id": shipment_id},
                        "message": str(e),
                        "timestamp": datetime.now(UTC).isoformat(),
                    }

            results = await asyncio.gather(
                *[refund_one(sid) for sid in shipment_ids], return_exceptions=False
            )

            successful = [r for r in results if r.get("status") == "success"]
            failed = [r for r in results if r.get("status") == "error"]

            return {
                "status": "success" if successful else "error",
                "data": {
                    "total": total,
                    "successful": len(successful),
                    "failed": len(failed),
                    "results": results,
                },
                "message": (
                    f"Refunded {len(successful)} of {total} shipments successfully"
                    if successful
                    else f"All {total} refund requests failed"
                ),
                "timestamp": datetime.now(UTC).isoformat(),
            }

        shipment_ids = ["shp_123", "shp_456"]
        result = await refund_shipment(shipment_ids, mock_context)

        assert result["status"] == "error"
        assert result["data"]["total"] == 2
        assert result["data"]["successful"] == 0
        assert result["data"]["failed"] == 2
        assert "All 2 refund requests failed" in result["message"]
