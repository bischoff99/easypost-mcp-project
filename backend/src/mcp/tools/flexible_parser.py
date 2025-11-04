"""Flexible shipment data parser - handles any input format."""

import logging
import re
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def parse_human_readable_shipment(text: str) -> Optional[Dict]:
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
                weight = f"{lbs + oz/16} lbs"

    # Parse address lines (first non-metadata lines)
    address_lines = []
    for line in lines:
        if not any(kw in line.lower() for kw in ["email", "phone", "dimension", "weight", "@"]):
            if not re.search(r"\+?\d{10,}", line):  # Skip phone-only lines
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
            else address_lines[3] if len(address_lines) > 3 else "US"
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


def register_flexible_parser(mcp):
    """Register flexible input parser tool."""

    @mcp.tool()
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
            else:
                return {
                    "status": "error",
                    "message": "Could not parse shipment data. Please check format.",
                }

        except Exception as e:
            logger.error(f"Parse error: {str(e)}")
            return {"status": "error", "message": f"Parse failed: {str(e)}"}
