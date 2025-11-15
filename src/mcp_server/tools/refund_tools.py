"""Refund shipment MCP tool."""

import asyncio
import logging
from datetime import UTC, datetime

from fastmcp import Context
from fastmcp.exceptions import ToolError

from src.utils.constants import STANDARD_TIMEOUT

logger = logging.getLogger(__name__)


def register_refund_tools(mcp, easypost_service=None):
    """Register refund-related tools with MCP server."""

    @mcp.tool(
        tags=["refund", "shipping", "core"],
        annotations={
            "destructiveHint": True,
        },
    )
    async def refund_shipment(
        shipment_ids: str | list[str], ctx: Context | None = None
    ) -> dict:
        """
        Refund one or more shipments.

        Accepts either a single shipment ID (string) or multiple shipment IDs (list).
        For bulk refunds, processes shipments in parallel for optimal performance.

        Args:
            shipment_ids: Single shipment ID (str) or list of shipment IDs to refund
            ctx: MCP context for progress reporting

        Returns:
            Standardised response with refund results:
            - Single shipment: Direct refund result
            - Multiple shipments: Aggregated results with success/failure counts

        Example:
            Single refund:
            >>> await refund_shipment("shp_123abc", ctx)
            {
                "status": "success",
                "data": {
                    "shipment_id": "shp_123abc",
                    "refund_status": "submitted",
                    "tracking_code": "EZ1234567890",
                    "carrier": "USPS",
                    "amount": "12.50"
                },
                "message": "Refund request submitted successfully",
                "timestamp": "2025-11-13T..."
            }

            Bulk refund:
            >>> await refund_shipment(["shp_123", "shp_456", "shp_789"], ctx)
            {
                "status": "success",
                "data": {
                    "total": 3,
                    "successful": 2,
                    "failed": 1,
                    "results": [...]
                },
                "message": "Refunded 2 of 3 shipments successfully",
                "timestamp": "2025-11-13T..."
            }
        """
        from src.utils.config import settings

        # Environment warning
        if settings.ENVIRONMENT == "production":
            logger.warning("⚠️  PRODUCTION MODE: Refunding real shipments!")
        else:
            logger.info(f"✓ {settings.ENVIRONMENT.upper()} mode: Processing refunds")

        try:
            # Get service from context or use provided
            if ctx:
                lifespan_ctx = ctx.request_context.lifespan_context
                service = (
                    lifespan_ctx.get("easypost_service")
                    if isinstance(lifespan_ctx, dict)
                    else lifespan_ctx.easypost_service
                )
            elif easypost_service:
                service = easypost_service
            else:
                raise ToolError(
                    "EasyPost service not available. Check server configuration."
                )

            # Handle single shipment ID
            if isinstance(shipment_ids, str):
                if ctx:
                    await ctx.info(f"Refunding shipment {shipment_ids}...")

                # Add timeout to prevent SSE timeout errors
                result = await asyncio.wait_for(
                    service.refund_shipment(shipment_ids), timeout=STANDARD_TIMEOUT
                )

                if ctx:
                    await ctx.report_progress(1, 1)

                return result

            # Handle bulk refunds
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

            # Process refunds in parallel with timeout per shipment
            async def refund_one(shipment_id: str) -> dict:
                try:
                    return await asyncio.wait_for(
                        service.refund_shipment(shipment_id), timeout=STANDARD_TIMEOUT
                    )
                except TimeoutError:
                    logger.error(f"Refund timed out for shipment {shipment_id}")
                    return {
                        "status": "error",
                        "data": {"shipment_id": shipment_id},
                        "message": "Refund request timed out",
                        "timestamp": datetime.now(UTC).isoformat(),
                    }
                except Exception as e:
                    logger.error(f"Refund failed for {shipment_id}: {str(e)}")
                    return {
                        "status": "error",
                        "data": {"shipment_id": shipment_id},
                        "message": str(e),
                        "timestamp": datetime.now(UTC).isoformat(),
                    }

            # Execute all refunds in parallel
            results = await asyncio.gather(
                *[refund_one(sid) for sid in shipment_ids], return_exceptions=False
            )

            # Aggregate results
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
                "message": (
                    f"Refunded {len(successful)} of {total} shipments successfully"
                    if successful
                    else f"All {total} refund requests failed"
                ),
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except TimeoutError:
            logger.error("Refund request timed out")
            return {
                "status": "error",
                "data": None,
                "message": "Refund request timed out. Please try again.",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except ToolError as e:
            logger.error(f"Tool error: {str(e)}")
            return {
                "status": "error",
                "data": None,
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            logger.error(f"Tool error: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "data": None,
                "message": f"Failed to process refund request: {str(e)}",
                "timestamp": datetime.now(UTC).isoformat(),
            }
