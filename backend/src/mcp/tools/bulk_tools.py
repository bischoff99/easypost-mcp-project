"""Bulk shipment operations MCP tool."""

import asyncio
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict

from fastmcp import Context
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ShipmentLine(BaseModel):
    """Parsed shipment data from spreadsheet."""

    origin_state: str
    carrier_preference: str
    recipient_name: str
    recipient_last_name: str
    recipient_phone: str
    recipient_email: str
    street1: str
    street2: str = ""
    city: str
    state: str
    zip: str
    country: str
    dimensions: str  # e.g., "13 x 12 x 2"
    weight: str  # e.g., "1.8 lbs"
    contents: str


# Product category detection patterns
PRODUCT_CATEGORIES = {
    "bedding": ["pillow", "mattress", "sheet", "blanket", "comforter", "duvet"],
    "sporting": ["fishing", "reel", "rod", "tackle", "outdoor", "camping", "hunting"],
    "beauty": ["cosmetic", "skincare", "makeup", "lotion", "cream", "serum"],
    "electronics": ["phone", "computer", "tablet", "headphone", "speaker", "camera"],
}

# Warehouse addresses by product category
WAREHOUSE_BY_CATEGORY = {
    "California": {
        "bedding": {
            "name": "LA Home Goods Warehouse",
            "company": "Premium Bedding Distribution",
            "street1": "8500 Beverly Blvd",
            "street2": "Suite 120",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90048",
            "country": "US",
            "phone": "310-555-0199",
            "email": "bedding@lahomegoods.com",
        },
        "sporting": {
            "name": "LA Outdoor Gear Hub",
            "company": "California Outdoor Supply",
            "street1": "1200 S Broadway",
            "street2": "",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90015",
            "country": "US",
            "phone": "323-555-0155",
            "email": "sporting@laoutdoor.com",
        },
        "beauty": {
            "name": "Beauty & Wellness LA",
            "company": "Natural Essentials Store",
            "street1": "8500 Beverly Blvd",
            "street2": "Suite 120",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90048",
            "country": "US",
            "phone": "310-555-0199",
            "email": "shipping@beautywellnessla.com",
        },
        "default": {
            "name": "LA General Warehouse",
            "company": "California Distribution Center",
            "street1": "1500 E Olympic Blvd",
            "street2": "",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90021",
            "country": "US",
            "phone": "213-555-0100",
            "email": "shipping@ladistribution.com",
        },
    },
}

# Legacy format for backward compatibility
STORE_ADDRESSES = {
    "California": {
        "Los Angeles": WAREHOUSE_BY_CATEGORY["California"]["default"],
    },
    "Nevada": {
        "Las Vegas": {
            "name": "Las Vegas Distribution Center",
            "company": "Nevada Logistics Hub",
            "street1": "3900 Paradise Rd",
            "street2": "Suite 200",
            "city": "Las Vegas",
            "state": "NV",
            "zip": "89169",
            "country": "US",
            "phone": "702-555-0188",
            "email": "shipping@lasvegasdistro.com",
        },
    },
}

# Backward compatibility
CA_STORE_ADDRESSES = STORE_ADDRESSES["California"]


def parse_dimensions(dim_str: str) -> tuple:
    """
    Parse dimensions string like '13 x 12 x 2' into (length, width, height).

    Args:
        dim_str: Dimension string with x separators

    Returns:
        Tuple of (length, width, height) as floats
    """
    parts = [p.strip() for p in dim_str.lower().replace("x", " ").split()]
    numbers = [float(p) for p in parts if p.replace(".", "").isdigit()]

    if len(numbers) >= 3:
        return (numbers[0], numbers[1], numbers[2])
    return (12.0, 9.0, 6.0)  # Default box dimensions


def parse_weight(weight_str: str) -> float:
    """
    Parse weight string like '1.8 lbs' into ounces.

    Args:
        weight_str: Weight string with unit

    Returns:
        Weight in ounces
    """
    # Extract number from string
    match = re.search(r"([\d.]+)\s*(lbs?|oz|ounces?|pounds?)", weight_str.lower())
    if match:
        value = float(match.group(1))
        unit = match.group(2)

        # Convert to ounces
        if "lb" in unit or "pound" in unit:
            return value * 16.0  # 1 lb = 16 oz
        return value  # Already in oz

    return 16.0  # Default 1 lb


def detect_product_category(contents: str) -> str:
    """
    Detect product category from contents string.

    Args:
        contents: Item description/contents string

    Returns:
        Category name (bedding, sporting, beauty, electronics, default)
    """
    contents_lower = contents.lower()

    for category, keywords in PRODUCT_CATEGORIES.items():
        for keyword in keywords:
            if keyword in contents_lower:
                return category

    return "default"


def get_warehouse_address(state: str, category: str) -> dict:
    """
    Get warehouse address based on state and product category.

    Args:
        state: Origin state (e.g., "California")
        category: Product category

    Returns:
        Warehouse address dictionary
    """
    if state not in WAREHOUSE_BY_CATEGORY:
        state = "California"  # Default fallback

    state_warehouses = WAREHOUSE_BY_CATEGORY[state]

    if category in state_warehouses:
        return state_warehouses[category]

    return state_warehouses.get("default", state_warehouses[list(state_warehouses.keys())[0]])


def parse_spreadsheet_line(line: str) -> Dict[str, Any]:
    """
    Parse a tab-separated line from spreadsheet.

    Args:
        line: Tab-separated data line

    Returns:
        Parsed shipment dictionary
    """
    # Split by tabs
    parts = line.split("\t")

    if len(parts) < 16:
        raise ValueError(f"Invalid line format: expected at least 16 columns, got {len(parts)}")

    return {
        "origin_state": parts[0].strip(),
        "carrier_preference": parts[1].strip(),
        "recipient_name": parts[2].strip(),
        "recipient_last_name": parts[3].strip(),
        "recipient_phone": parts[4].strip(),
        "recipient_email": parts[5].strip(),
        "street1": parts[6].strip(),
        "street2": parts[7].strip(),
        "city": parts[8].strip(),
        "state": parts[9].strip(),
        "zip": parts[10].strip(),
        "country": parts[11].strip(),
        "dimensions": parts[13].strip(),
        "weight": parts[14].strip(),
        "contents": parts[15].strip(),
    }


def register_bulk_tools(mcp, easypost_service):
    """Register bulk shipment tools with MCP server."""

    @mcp.tool()
    async def parse_and_get_bulk_rates(
        spreadsheet_data: str,
        from_city: str = None,
        ctx: Context = None,
    ) -> dict:
        """
        Parse spreadsheet data and get shipping rates for multiple shipments.

        Automatically detects product category from contents and uses appropriate warehouse:
        - Bedding items (pillows, mattresses) → Home Goods Warehouse
        - Sporting goods (fishing, outdoor) → Outdoor Gear Hub
        - Beauty products → Beauty & Wellness
        - Default → General Warehouse

        Args:
            spreadsheet_data: Tab-separated shipment data (paste from spreadsheet)
            from_city: DEPRECATED - Now auto-detects warehouse per item
            ctx: MCP context for progress reporting

        Returns:
            Rates for all shipments with warehouse assignments
        """
        try:
            if ctx:
                await ctx.info("Parsing spreadsheet data...")

            # Split into lines and filter empty
            lines = [l.strip() for l in spreadsheet_data.split("\n") if l.strip()]

            if not lines:
                return {
                    "status": "error",
                    "data": None,
                    "message": "No data provided",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

            results = []
            total_lines = len(lines)
            used_warehouses = set()  # Track which warehouses are used

            for idx, line in enumerate(lines):
                try:
                    if ctx:
                        await ctx.info(f"Processing shipment {idx + 1}/{total_lines}...")

                    # Parse line
                    data = parse_spreadsheet_line(line)

                    # Detect product category from contents
                    category = detect_product_category(data["contents"])

                    # Get appropriate warehouse address
                    from_address = get_warehouse_address(data["origin_state"], category)
                    warehouse_key = f"{from_address['company']}"
                    used_warehouses.add(warehouse_key)

                    if ctx:
                        await ctx.info(
                            f"Shipment {idx + 1}: {category} → {from_address['company']}"
                        )

                    # Parse dimensions and weight
                    length, width, height = parse_dimensions(data["dimensions"])
                    weight_oz = parse_weight(data["weight"])

                    # Build to_address
                    to_address = {
                        "name": f"{data['recipient_name']} {data['recipient_last_name']}",
                        "street1": data["street1"],
                        "street2": data["street2"],
                        "city": data["city"],
                        "state": data["state"],
                        "zip": data["zip"],
                        "country": data["country"],
                        "phone": data["recipient_phone"],
                        "email": data["recipient_email"],
                    }

                    # Build parcel
                    parcel = {
                        "length": length,
                        "width": width,
                        "height": height,
                        "weight": weight_oz,
                    }

                    if ctx:
                        await ctx.report_progress(idx, total_lines)

                    # Get rates
                    rates_result = await asyncio.wait_for(
                        easypost_service.get_rates(to_address, from_address, parcel),
                        timeout=20.0,
                    )

                    results.append(
                        {
                            "shipment_number": idx + 1,
                            "recipient": to_address["name"],
                            "destination": f"{data['city']}, {data['state']}, {data['country']}",
                            "weight_oz": round(weight_oz, 2),
                            "dimensions": f"{length} x {width} x {height} in",
                            "contents": data["contents"][:100],
                            "category": category,
                            "from_warehouse": from_address["company"],
                            "from_city": from_address["city"],
                            "rates": (
                                rates_result.get("data", [])
                                if rates_result.get("status") == "success"
                                else []
                            ),
                            "error": (
                                rates_result.get("message")
                                if rates_result.get("status") == "error"
                                else None
                            ),
                        }
                    )

                except Exception as e:
                    logger.error(f"Error processing line {idx + 1}: {str(e)}")
                    results.append(
                        {
                            "shipment_number": idx + 1,
                            "error": f"Failed to process: {str(e)}",
                        }
                    )

            if ctx:
                await ctx.report_progress(total_lines, total_lines)
                await ctx.info(
                    f"Processed {len(results)} shipments from {len(used_warehouses)} warehouses"
                )

            # Calculate summary
            successful = len([r for r in results if not r.get("error")])
            failed = len(results) - successful

            return {
                "status": "success",
                "data": {
                    "shipments": results,
                    "warehouses_used": sorted(used_warehouses),
                    "summary": {
                        "total": len(results),
                        "successful": successful,
                        "failed": failed,
                        "warehouses": len(used_warehouses),
                    },
                },
                "message": (
                    f"Processed {len(results)} shipments from {len(used_warehouses)} warehouses "
                    f"({successful} successful, {failed} failed)"
                ),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            logger.error(f"Bulk rate check error: {str(e)}")
            return {
                "status": "error",
                "data": None,
                "message": f"Failed to process bulk rates: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
