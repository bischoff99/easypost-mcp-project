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
    "New York": {
        "bedding": {
            "name": "NYC Home Goods Warehouse",
            "company": "New York Home Essentials",
            "street1": "246 E 116th St",
            "street2": "Suite 200",
            "city": "New York",
            "state": "NY",
            "zip": "10029",
            "country": "US",
            "phone": "646-600-6012",
            "email": "bedding@nyhomegoods.com",
        },
        "sporting": {
            "name": "NYC Outdoor Gear Hub",
            "company": "New York Sporting Supply",
            "street1": "246 E 116th St",
            "street2": "Suite 300",
            "city": "New York",
            "state": "NY",
            "zip": "10029",
            "country": "US",
            "phone": "646-600-6012",
            "email": "sporting@nyoutdoor.com",
        },
        "beauty": {
            "name": "NYC Beauty & Wellness",
            "company": "New York Beauty Essentials",
            "street1": "246 E 116th St",
            "street2": "Suite 400",
            "city": "New York",
            "state": "NY",
            "zip": "10029",
            "country": "US",
            "phone": "646-600-6012",
            "email": "beauty@nycwellness.com",
        },
        "default": {
            "name": "NYC Distribution Center",
            "company": "New York Logistics Hub",
            "street1": "246 E 116th St",
            "street2": "",
            "city": "New York",
            "state": "NY",
            "zip": "10029",
            "country": "US",
            "phone": "646-600-6012",
            "email": "shipping@nycdistro.com",
        },
    },
}

# Legacy format for backward compatibility
STORE_ADDRESSES = {
    "California": {
        "Los Angeles": WAREHOUSE_BY_CATEGORY["California"]["default"],
    },
    "New York": {
        "New York": WAREHOUSE_BY_CATEGORY["New York"]["default"],
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
    Parse weight string like '1.8 lbs', '5LB 2oz', '2 lbs 3 oz' into ounces.

    Handles formats:
    - Single unit: "1.8 lbs", "16 oz", "2 pounds"
    - Combined: "5LB 2oz", "2 lbs 3 oz", "1 pound 8 ounces"

    Args:
        weight_str: Weight string with unit(s)

    Returns:
        Weight in ounces
    """
    weight_str = weight_str.strip()
    total_oz = 0.0

    # Pattern to match: number + unit (handles both combined and single formats)
    # Matches: "5LB", "2oz", "1.5 lbs", "3 ounces", etc.
    pattern = r"([\d.]+)\s*(lbs?|oz|ounces?|pounds?|LB|OZ)"

    # Find all matches (handles combined formats like "5LB 2oz")
    matches = re.finditer(pattern, weight_str.lower())

    for match in matches:
        value = float(match.group(1))
        unit = match.group(2).lower()

        # Convert to ounces
        if "lb" in unit or "pound" in unit:
            total_oz += value * 16.0  # 1 lb = 16 oz
        else:
            total_oz += value  # Already in oz

    # If no matches found, return default 1 lb (16 oz)
    if total_oz == 0.0:
        return 16.0

    return total_oz


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

    Format (16+ columns):
    0. origin_state (or sender_name if sender address provided)
    1. carrier_preference (or sender_street1 if sender address provided)
    2. recipient_name
    3. recipient_last_name
    4. recipient_phone
    5. recipient_email
    6. recipient_street1
    7. recipient_street2
    8. recipient_city
    9. recipient_state
    10. recipient_zip
    11. recipient_country
    12. (unused)
    13. dimensions
    14. weight
    15. contents
    16+. sender fields (optional): sender_name, sender_street1, sender_city,
        sender_state, sender_zip, sender_country, sender_phone, sender_email

    If sender fields are provided (columns 16+), use those instead of warehouse lookup.

    Args:
        line: Tab-separated data line

    Returns:
        Parsed shipment dictionary with optional sender_address
    """
    # Split by tabs
    parts = line.split("\t")

    if len(parts) < 16:
        raise ValueError(f"Invalid line format: expected at least 16 columns, got {len(parts)}")

    result = {
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

    # Check if sender address is provided (columns 16+)
    # Format: sender_name, sender_street1, sender_street2, sender_city,
    # sender_state, sender_zip, sender_country, sender_phone, sender_email
    if len(parts) >= 25 and parts[16].strip():
        result["sender_address"] = {
            "name": parts[16].strip(),
            "street1": parts[17].strip() if len(parts) > 17 else "",
            "street2": parts[18].strip() if len(parts) > 18 else "",
            "city": parts[19].strip() if len(parts) > 19 else "",
            "state": parts[20].strip() if len(parts) > 20 else "",
            "zip": parts[21].strip() if len(parts) > 21 else "",
            "country": parts[22].strip() if len(parts) > 22 else "US",
            "phone": parts[23].strip() if len(parts) > 23 else "",
            "email": parts[24].strip() if len(parts) > 24 else "",
        }

    return result


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

    @mcp.tool(tags=["bulk", "rates", "shipping", "m3-optimized"])
    async def parse_and_get_bulk_rates(
        spreadsheet_data: str,
        ctx: Context = None,
    ) -> dict:
        """
        Get shipping rates for single or multiple shipments - M3 Max Optimized.

        Handles both single shipments (1 line) and bulk operations (multiple lines).
        Uses spreadsheet format: tab-separated columns (paste from spreadsheet).

        M3 MAX OPTIMIZATION (16 cores, 128GB RAM):
        - Parallel rate calculations: 16 concurrent API calls
        - Formula: cpu_count × 1 = 16 workers for rate limiting compliance
        - Performance: ~10× faster than sequential (50 items: 5s vs 50s)

        Automatically detects product category from contents and uses appropriate warehouse:
        - Bedding items (pillows, mattresses) → Home Goods Warehouse
        - Sporting goods (fishing, outdoor) → Outdoor Gear Hub
        - Beauty products → Beauty & Wellness
        - Default → General Warehouse

        Supports sender addresses: Include sender info in columns 16+ to use custom sender
        instead of warehouse lookup.

        Args:
            spreadsheet_data: Tab-separated shipment data (1+ lines, paste from spreadsheet)
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

                        # Detect product category from contents (always needed for reporting)
                        category = detect_product_category(data["contents"])

                        # Use sender address if provided, otherwise use warehouse lookup
                        if "sender_address" in data and data["sender_address"].get("name"):
                            # Use provided sender address
                            from_address = data["sender_address"]
                            warehouse_key = f"{from_address.get('name', 'Custom Sender')}"
                        else:
                            # Get appropriate warehouse address
                            from_address = get_warehouse_address(data["origin_state"], category)
                            company_or_name = from_address.get("company") or from_address.get(
                                "name", "Unknown"
                            )
                            warehouse_key = f"{company_or_name}"

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

                        # Check if international and auto-generate customs if needed
                        is_international = to_address["country"] != from_address.get(
                            "country", "US"
                        )
                        customs_info = None

                        if is_international:
                            # Auto-generate customs info for international shipments
                            from src.services.smart_customs import get_or_create_customs

                            loop = asyncio.get_running_loop()
                            customs_info = await loop.run_in_executor(
                                None,
                                get_or_create_customs,
                                data["contents"],
                                weight_oz,
                                easypost_service.client,
                                None,  # Auto-detect value from description
                            )

                            if ctx and customs_info:
                                await ctx.info(
                                    f"✅ Auto-generated customs for international shipment "
                                    f"({to_address['country']})"
                                )

                        # Get rates with timeout (customs included for international)
                        rates_result = await asyncio.wait_for(
                            easypost_service.get_rates(
                                to_address, from_address, parcel, customs_info=customs_info
                            ),
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
                            "from_warehouse": (
                                from_address.get("company", from_address.get("name", "Unknown"))
                            ),
                            "from_city": from_address.get("city", "Unknown"),
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
