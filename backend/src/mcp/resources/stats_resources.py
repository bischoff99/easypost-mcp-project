"""Statistics MCP resources."""

import asyncio
import json
import logging
from datetime import UTC, datetime, timedelta

logger = logging.getLogger(__name__)


def register_stats_resources(mcp, easypost_service):
    """Register statistics resources with MCP server."""

    @mcp.resource("easypost://stats/overview")
    async def get_stats_resource() -> str:
        """Get shipping statistics overview calculated from real EasyPost data."""
        try:
            # Fetch recent shipments (last 30 days worth, up to 100)
            thirty_days_ago = (datetime.now(UTC) - timedelta(days=30)).isoformat()

            # Add timeout to prevent SSE timeout errors
            result = await asyncio.wait_for(
                easypost_service.get_shipments_list(
                    page_size=100, purchased=True, start_datetime=thirty_days_ago
                ),
                timeout=20.0,
            )

            if result["status"] == "error":
                return json.dumps(result, indent=2)

            shipments = result.get("data", [])  # data is direct list, not {"shipments": [...]}

            # Calculate real statistics
            total_shipments = len(shipments)
            total_cost = 0.0
            carriers_used_set = set()
            delivered_count = 0

            for shipment in shipments:
                # Calculate total cost from selected rate
                if shipment.get("selected_rate") and shipment["selected_rate"].get("rate"):
                    total_cost += float(shipment["selected_rate"]["rate"])

                # Track carriers used
                if shipment.get("selected_rate") and shipment["selected_rate"].get("carrier"):
                    carriers_used_set.add(shipment["selected_rate"]["carrier"])

                # Track delivery success
                if shipment.get("status") == "delivered":
                    delivered_count += 1

            average_cost = round(total_cost / total_shipments, 2) if total_shipments > 0 else 0
            delivery_success_rate = (
                round(delivered_count / total_shipments, 2) if total_shipments > 0 else 0
            )

            stats = {
                "total_shipments": total_shipments,
                "total_cost": round(total_cost, 2),
                "average_cost": average_cost,
                "carriers_used": sorted(carriers_used_set),
                "delivery_success_rate": delivery_success_rate,
                "period": "last_30_days",
                "timestamp": datetime.now(UTC).isoformat(),
            }

            return json.dumps(
                {"status": "success", "data": stats, "message": "Statistics calculated"},
                indent=2,
            )
        except TimeoutError:
            logger.error("Stats calculation timed out after 20 seconds")
            return json.dumps(
                {
                    "status": "error",
                    "message": "Stats calculation timed out. Please try again.",
                    "timestamp": datetime.now(UTC).isoformat(),
                },
                indent=2,
            )
        except Exception as e:
            logger.error(f"Resource error: {str(e)}")
            return json.dumps(
                {
                    "status": "error",
                    "message": f"Failed to calculate stats: {str(e)}",
                    "timestamp": datetime.now(UTC).isoformat(),
                },
                indent=2,
            )
