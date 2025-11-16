"""
Aggregation helpers for bulk shipment operations.

These functions handle result aggregation and summary generation.
"""

from datetime import datetime
from typing import Any


def aggregate_results(
    results: list[dict[str, Any]],
    start_time: datetime,
    end_time: datetime,
) -> dict[str, Any]:
    """
    Aggregate shipment results into summary.

    Pure function - no I/O operations.
    Complexity: 6
    """
    duration = (end_time - start_time).total_seconds()
    successful = [r for r in results if r.get("status") == "success"]
    failed = [r for r in results if r.get("status") == "error"]

    total_cost = sum(
        float(s.get("cost", 0)) for s in successful if s.get("cost") is not None
    )

    # Carrier breakdown
    carrier_stats: dict[str, dict[str, Any]] = {}
    for s in successful:
        carrier_name = s.get("carrier", "Unknown")
        if carrier_name not in carrier_stats:
            carrier_stats[carrier_name] = {"count": 0, "cost": 0.0}
        carrier_stats[carrier_name]["count"] += 1
        cost = s.get("cost")
        if cost is not None:
            carrier_stats[carrier_name]["cost"] += float(cost)

    return {
        "duration": duration,
        "successful": successful,
        "failed": failed,
        "total_cost": total_cost,
        "carrier_stats": carrier_stats,
        "summary": {
            "total": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "total_cost": total_cost,
            "carrier_breakdown": carrier_stats,
        },
    }
