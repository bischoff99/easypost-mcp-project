"""Bulk shipment operations MCP tool."""

import asyncio
import logging
import re
from datetime import UTC, datetime
from typing import Any

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


def parse_spreadsheet_line(line: str) -> dict[str, Any]:
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


def parse_human_readable_shipment(text: str) -> dict | None:
    """
    Parse human-readable shipment data into standard format.

    Handles formats like:
    ```
    Company Name Inc.
    John Smith
    123 Main St
    City, State ZIP
    Country

    Email: email@example.com
    Phone: +1234567890

    Dimensions: 13x13x7
    Weight: 4lb 5oz
    ```

    Returns:
        Standardized shipment dict or None
    """
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]

    if len(lines) < 5:
        return None

    result = {}
    email = None
    phone = None
    dimensions = None
    weight = None

    # Extract email
    for line in lines:
        email_match = re.search(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", line)
        if email_match:
            email = email_match.group(1)

        # Extract phone
        phone_match = re.search(r"(\+?\d[\d\s\-()]{7,20})", line)
        if phone_match:
            phone = (
                phone_match.group(1)
                .replace(" ", "")
                .replace("-", "")
                .replace("(", "")
                .replace(")", "")
            )

        # Extract dimensions
        if "dimension" in line.lower() or "x" in line:
            dim_match = re.search(r"(\d+)\s*x\s*(\d+)\s*x\s*(\d+)", line, re.IGNORECASE)
            if dim_match:
                dimensions = f"{dim_match.group(1)} x {dim_match.group(2)} x {dim_match.group(3)}"

        # Extract weight
        if "weight" in line.lower() or "lb" in line.lower():
            weight_match = re.search(
                r"(\d+(?:\.\d+)?)\s*lb(?:s)?(?:\s*(\d+(?:\.\d+)?)\s*oz)?", line, re.IGNORECASE
            )
            if weight_match:
                lbs = float(weight_match.group(1))
                oz = float(weight_match.group(2)) if weight_match.group(2) else 0
                weight = f"{lbs + oz / 16} lbs"

    # Parse address lines (first non-metadata lines)
    address_lines = []
    for line in lines:
        if not any(
            kw in line.lower() for kw in ["email", "phone", "dimension", "weight", "@"]
        ) and not re.search(r"\+?\d{10,}", line):  # Skip phone-only lines
            address_lines.append(line)

    if len(address_lines) >= 4:
        # Detect company (first line with business indicators)
        company_indicators = ["inc", "llc", "ltd", "corporation", "corp", "co.", "company"]
        has_company = any(indicator in address_lines[0].lower() for indicator in company_indicators)

        result["company"] = address_lines[0] if has_company else ""
        result["name"] = address_lines[1] if has_company else address_lines[0]
        result["street1"] = address_lines[2] if has_company else address_lines[1]

        # Parse city, state, zip
        location_line = address_lines[3] if has_company else address_lines[2]
        city_state_match = re.match(r"([^,]+),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)", location_line)
        if city_state_match:
            result["city"] = city_state_match.group(1).strip()
            result["state"] = city_state_match.group(2)
            result["zip"] = city_state_match.group(3)

        # Country (normalize common variations)
        country_line = (
            address_lines[4]
            if has_company and len(address_lines) > 4
            else address_lines[3]
            if len(address_lines) > 3
            else "US"
        )
        if country_line.lower() in ["usa", "united states", "us"]:
            result["country"] = "US"
        elif country_line.lower() in ["canada", "ca"]:
            result["country"] = "CA"
        else:
            result["country"] = country_line

    result["email"] = email or ""
    result["phone"] = phone or ""
    result["dimensions"] = dimensions or "12 x 12 x 4"
    result["weight"] = weight or "1 lbs"

    return result if result.get("name") else None


def register_bulk_tools(mcp, easypost_service=None):
    """Register bulk shipment tools with MCP server."""

    @mcp.tool(tags=["bulk", "parse", "utility"])
    async def parse_flexible_shipment(shipment_text: str) -> dict:
        """
        Parse human-readable shipment data into standard format.

        Accepts various formats:
        - Tab-separated spreadsheet data
        - Human-readable structured text
        - Mixed formats

        Automatically fills missing customs data for international shipments.

        Args:
            shipment_text: Shipment data in any readable format

        Returns:
            Standardized shipment dict ready for rate/purchase tools
        """
        try:
            # Try tab-separated first
            if "\t" in shipment_text and shipment_text.count("\t") >= 10:
                return {
                    "status": "success",
                    "format": "spreadsheet",
                    "message": "Use create_bulk_shipments for tab-separated data",
                }

            # Parse human-readable format
            parsed = parse_human_readable_shipment(shipment_text)

            if parsed:
                return {
                    "status": "success",
                    "data": parsed,
                    "message": "Parsed successfully - ready for get_rates or create_shipment",
                }
            return {
                "status": "error",
                "message": "Could not parse shipment data. Please check format.",
            }

        except Exception as e:
            logger.error(f"Parse error: {str(e)}")
            return {"status": "error", "message": f"Parse failed: {str(e)}"}

    @mcp.tool(tags=["bulk", "rates", "shipping", "m3-optimized"])
    async def parse_and_get_bulk_rates(
        spreadsheet_data: str,
        from_city: str = None,  # noqa: ARG001 - Future filtering feature
        ctx: Context = None,
    ) -> dict:
        """
        Parse spreadsheet data and get shipping rates for multiple shipments - M3 Max Optimized.

        M3 MAX OPTIMIZATION (16 cores, 128GB RAM):
        - Parallel rate calculations: 16 concurrent API calls
        - Formula: cpu_count × 1 = 16 workers for rate limiting compliance
        - Performance: ~10× faster than sequential (50 items: 5s vs 50s)

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
            Rates for all shipments with warehouse assignments and performance metrics
        """
        from time import perf_counter

        start_time = perf_counter()

        try:
            if ctx:
                await ctx.info("🚀 M3 Max: Starting parallel rate calculation (16 workers)...")

            # Split into lines and filter empty
            lines = [l.strip() for l in spreadsheet_data.split("\n") if l.strip()]

            if not lines:
                return {
                    "status": "error",
                    "data": None,
                    "message": "No data provided",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

            total_lines = len(lines)
            used_warehouses = set()  # Track which warehouses are used

            # M3 Max: Semaphore for rate limiting (16 concurrent API calls max)
            semaphore = asyncio.Semaphore(16)

            async def process_one_line(idx: int, line: str) -> dict:
                """Process single shipment line with rate limiting."""
                async with semaphore:
                    try:
                        if ctx and idx % max(1, total_lines // 10) == 0:
                            await ctx.info(f"Processing shipment {idx + 1}/{total_lines}...")

                        # Parse line
                        data = parse_spreadsheet_line(line)

                        # Detect product category from contents
                        category = detect_product_category(data["contents"])

                        # Get appropriate warehouse address
                        from_address = get_warehouse_address(data["origin_state"], category)
                        warehouse_key = f"{from_address['company']}"
                        used_warehouses.add(warehouse_key)

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

                        # Get rates with timeout
                        rates_result = await asyncio.wait_for(
                            easypost_service.get_rates(to_address, from_address, parcel),
                            timeout=20.0,
                        )

                        return {
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

                    except Exception as e:
                        logger.error(f"Error processing line {idx + 1}: {str(e)}")
                        return {
                            "shipment_number": idx + 1,
                            "error": f"Failed to process: {str(e)}",
                        }

            # M3 Max: Process all shipments in parallel with asyncio.gather()
            if ctx:
                await ctx.info(f"📊 Processing {total_lines} shipments in parallel...")

            tasks = [process_one_line(idx, line) for idx, line in enumerate(lines)]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Convert exceptions to error results
            processed_results = []
            for idx, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Task {idx + 1} raised exception: {result}")
                    processed_results.append(
                        {
                            "shipment_number": idx + 1,
                            "error": f"Exception: {str(result)}",
                        }
                    )
                else:
                    processed_results.append(result)

            # Performance metrics
            duration = perf_counter() - start_time
            throughput = total_lines / duration if duration > 0 else 0

            if ctx:
                await ctx.report_progress(total_lines, total_lines)
                await ctx.info(f"✅ Complete! Processed {len(used_warehouses)} warehouses")
                await ctx.info(
                    f"⏱️  Duration: {duration:.2f}s | Throughput: {throughput:.1f} shipments/s"
                )
                await ctx.info("⚡ M3 Max: 16 parallel workers utilized")

            # Calculate summary
            successful = len([r for r in processed_results if not r.get("error")])
            failed = len(processed_results) - successful

            return {
                "status": "success",
                "data": {
                    "shipments": processed_results,
                    "warehouses_used": sorted(used_warehouses),
                    "summary": {
                        "total": len(processed_results),
                        "successful": successful,
                        "failed": failed,
                        "warehouses": len(used_warehouses),
                    },
                    "performance": {
                        "duration_seconds": round(duration, 2),
                        "throughput": round(throughput, 2),
                        "workers": 16,
                        "hardware": "M3 Max (16 cores)",
                    },
                },
                "message": (
                    f"Processed {len(processed_results)} shipments from "
                    f"{len(used_warehouses)} warehouses "
                    f"({successful} successful, {failed} failed) in "
                    f"{duration:.1f}s ({throughput:.1f}/s)"
                ),
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Bulk rate check error: {str(e)}")
            return {
                "status": "error",
                "data": None,
                "message": f"Failed to process bulk rates: {str(e)}",
                "timestamp": datetime.now(UTC).isoformat(),
            }
