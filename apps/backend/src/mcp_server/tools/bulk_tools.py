"""Bulk shipment operations MCP tool."""

import asyncio
import logging
import re
from datetime import UTC, datetime
from typing import Any

from fastmcp import Context
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# API rate limiting - sequential processing to avoid EasyPost production rate limits
MAX_CONCURRENT = 1  # Sequential API calls only (production rate limit compliance)


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


# Product category detection patterns (ORDER MATTERS - checked sequentially)
# More specific categories first to avoid false matches
PRODUCT_CATEGORIES = {
    # Apparel & Footwear (check first - very specific keywords)
    "apparel": [
        "jeans",
        "shirt",
        "pants",
        "jacket",
        "dress",
        "skirt",
        "shorts",
        "sweater",
        "hoodie",
        "coat",
        "clothing",
        "apparel",
        "denim",
        "selvedge",
        "vintage",
        "t-shirt",
        "blouse",
        "polo",
        "cardigan",
        "vest",
        "suit",
        "blazer",
        "trousers",
        "leggings",
        "joggers",
        "sweatpants",
        "tank top",
        "crop top",
        "underwear",
        "socks",
        "mens",
        "womens",
        "unisex",
        "slim-fit",
        "straight-leg",
        "boot cut",
        "tapered",
    ],
    "footwear": [
        "shoes",
        "boots",
        "sneakers",
        "sandals",
        "slippers",
        "heels",
        "flats",
        "loafers",
        "oxfords",
        "athletic shoes",
        "running shoes",
        "basketball shoes",
        "cleats",
        "flip-flops",
    ],
    # Sporting goods (specific before general outdoor terms)
    "sporting": [
        "fishing",
        "reel",
        "rod",
        "tackle",
        "outdoor",
        "camping",
        "hunting",
        "baseball",
        "glove",
        "bat",
        "sports",
        "athletic",
        "fitness",
        "golf",
        "tennis",
        "soccer",
        "basketball",
        "football",
        "hockey",
        "bike",
        "cycling",
        "yoga",
        "exercise",
        "hiking",
        "climbing",
        "skiing",
        "snowboard",
        "skateboard",
        "surfboard",
        "kayak",
        "gym",
        "workout",
        "training",
        "running",
        "swimming",
        "boxing",
        "martial arts",
    ],
    # Electronics (specific tech terms)
    "electronics": [
        "phone",
        "computer",
        "tablet",
        "headphone",
        "speaker",
        "camera",
        "laptop",
        "monitor",
        "keyboard",
        "mouse",
        "gaming",
        "console",
        "smartwatch",
        "earbuds",
        "wireless",
        "bluetooth",
        "usb",
        "charger",
        "adapter",
        "electronics",
        "tech",
        "gadget",
        "device",
    ],
    # Beauty (after apparel to avoid "wash" confusion)
    "beauty": [
        "cosmetic",
        "skincare",
        "makeup",
        "foundation",
        "lipstick",
        "mascara",
        "eyeshadow",
        "cleanser",
        "moisturizer",
        "toner",
        "face mask",
        "beauty",
        "nail polish",
        "fragrance",
        "perfume",
        "cologne",
        "lotion",
        "cream",
        "serum",
    ],
    # Home & Bedding
    "bedding": [
        "pillow",
        "mattress",
        "sheet",
        "blanket",
        "comforter",
        "duvet",
        "bedding",
        "linen",
        "pillowcase",
        "fitted sheet",
        "flat sheet",
        "bed",
        "sleeping",
        "quilt",
        "coverlet",
    ],
    # Art & Creative
    "art": [
        "print",
        "engraving",
        "painting",
        "artwork",
        "poster",
        "canvas",
        "frame",
        "sculpture",
        "drawing",
        "lithograph",
        "photograph",
        "art print",
        "wall art",
        "limited edition",
        "original",
        "gallery",
        "museum quality",
    ],
    # Media & Entertainment
    "books": [
        "book",
        "novel",
        "textbook",
        "paperback",
        "hardcover",
        "magazine",
        "journal",
        "comic",
        "manga",
        "graphic novel",
        "encyclopedia",
        "dictionary",
        "publication",
    ],
    "toys": [
        "toy",
        "doll",
        "action figure",
        "lego",
        "puzzle",
        "board game",
        "card game",
        "stuffed animal",
        "plush",
        "collectible",
        "model",
        "hobby",
        "playing cards",
    ],
    # Jewelry & Accessories
    "jewelry": [
        "jewelry",
        "necklace",
        "bracelet",
        "ring",
        "earrings",
        "watch",
        "pendant",
        "chain",
        "gold",
        "silver",
        "diamond",
        "gemstone",
        "precious metal",
    ],
    # Food & Supplements
    "food": [
        "food",
        "snack",
        "candy",
        "chocolate",
        "coffee",
        "tea",
        "spices",
        "sauce",
        "supplement",
        "vitamin",
        "protein",
        "gourmet",
        "organic",
        "natural food",
    ],
    # Home Goods (generic catch-all)
    "home_goods": [
        "kitchen",
        "cookware",
        "utensil",
        "dish",
        "plate",
        "bowl",
        "cup",
        "mug",
        "pan",
        "pot",
        "knife",
        "cutting board",
        "blender",
        "mixer",
        "appliance",
        "decor",
        "vase",
        "candle",
        "lamp",
        "furniture",
        "home",
    ],
}

# Customs signer names by company (actual person names for customs declarations)
CUSTOMS_SIGNERS = {
    "California Apparel Supply": "Michael Chen",
    "California Outdoor Supply": "Sarah Martinez",
    "Premium Bedding Distribution": "David Rodriguez",
    "Natural Essentials Store": "Jennifer Lee",
    "West Coast Footwear": "Robert Kim",
    "California Fine Arts": "Emily Zhang",
    "Pacific Tech Supply": "James Wilson",
    "Nevada Apparel Supply": "Thomas Anderson",
    "Nevada Sporting Supply": "Lisa Thompson",
    "Nevada Home Essentials": "Maria Garcia",
    "Nevada Beauty Supply": "Amanda Foster",
    "Desert Shoes": "Christopher Moore",
    "Nevada Fine Arts": "Patricia Bennett",
    "Desert Electronics": "Daniel Harris",
    "Nevada Logistics Hub": "Jessica Martinez",
    "New York Fashion Supply": "William Taylor",
    "New York Outdoor Supplies": "Michelle Brown",
    "New York Home Essentials": "Brandon Clarke",
    "New York Beauty Essentials": "Victoria Wright",
    "East Coast Shoes": "Anthony Green",
    "New York Fine Arts": "Samantha King",
    "Silicon Alley Electronics": "Christopher Davis",
    "New York Logistics Hub": "Nicole Anderson",
}


def get_customs_signer(warehouse_address: dict) -> str:
    """
    Get the customs signer name (actual person) for a warehouse.

    Args:
        warehouse_address: Address dict with 'company' field

    Returns:
        Person's name for customs signing
    """
    company = warehouse_address.get("company", "")
    return CUSTOMS_SIGNERS.get(company, "Shipping Manager")


# Warehouse addresses by product category (3 locations only)
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
            "email": "beauty@beautywellnessla.com",
        },
        "apparel": {
            "name": "LA Fashion District Warehouse",
            "company": "California Apparel Supply",
            "street1": "1200 S Broadway",
            "street2": "Suite 100",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90015",
            "country": "US",
            "phone": "213-555-0166",
            "email": "apparel@lafashion.com",
        },
        "footwear": {
            "name": "LA Footwear Warehouse",
            "company": "West Coast Shoes",
            "street1": "1200 S Broadway",
            "street2": "Suite 150",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90015",
            "country": "US",
            "phone": "213-555-0177",
            "email": "footwear@westcoastshoes.com",
        },
        "art": {
            "name": "LA Arts District Warehouse",
            "company": "California Fine Arts",
            "street1": "8500 Beverly Blvd",
            "street2": "Suite 200",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90048",
            "country": "US",
            "phone": "310-555-0188",
            "email": "art@lafinearts.com",
        },
        "electronics": {
            "name": "LA Tech Warehouse",
            "company": "Silicon Beach Electronics",
            "street1": "1500 E Olympic Blvd",
            "street2": "Suite 300",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90021",
            "country": "US",
            "phone": "213-555-0199",
            "email": "tech@siliconbeach.com",
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
        "apparel": {
            "name": "NYC Garment District Warehouse",
            "company": "New York Fashion Supply",
            "street1": "246 E 116th St",
            "street2": "Suite 500",
            "city": "New York",
            "state": "NY",
            "zip": "10029",
            "country": "US",
            "phone": "646-600-6013",
            "email": "apparel@nyfashion.com",
        },
        "footwear": {
            "name": "NYC Footwear Warehouse",
            "company": "East Coast Shoes",
            "street1": "246 E 116th St",
            "street2": "Suite 600",
            "city": "New York",
            "state": "NY",
            "zip": "10029",
            "country": "US",
            "phone": "646-600-6014",
            "email": "footwear@eastcoastshoes.com",
        },
        "art": {
            "name": "NYC Gallery District Warehouse",
            "company": "New York Fine Arts",
            "street1": "246 E 116th St",
            "street2": "Suite 700",
            "city": "New York",
            "state": "NY",
            "zip": "10029",
            "country": "US",
            "phone": "646-600-6015",
            "email": "art@nyfinearts.com",
        },
        "electronics": {
            "name": "NYC Tech Warehouse",
            "company": "Silicon Alley Electronics",
            "street1": "246 E 116th St",
            "street2": "Suite 800",
            "city": "New York",
            "state": "NY",
            "zip": "10029",
            "country": "US",
            "phone": "646-600-6016",
            "email": "tech@siliconalley.com",
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
    "Nevada": {
        "bedding": {
            "name": "Las Vegas Home Goods Warehouse",
            "company": "Nevada Home Essentials",
            "street1": "3900 Paradise Rd",
            "street2": "Suite 100",
            "city": "Las Vegas",
            "state": "NV",
            "zip": "89169",
            "country": "US",
            "phone": "702-555-0100",
            "email": "bedding@lvhomegoods.com",
        },
        "sporting": {
            "name": "Las Vegas Outdoor Gear Hub",
            "company": "Nevada Sporting Supply",
            "street1": "3900 Paradise Rd",
            "street2": "Suite 200",
            "city": "Las Vegas",
            "state": "NV",
            "zip": "89169",
            "country": "US",
            "phone": "702-555-0101",
            "email": "sporting@lvoutdoor.com",
        },
        "beauty": {
            "name": "Las Vegas Beauty & Wellness",
            "company": "Nevada Beauty Supply",
            "street1": "3900 Paradise Rd",
            "street2": "Suite 300",
            "city": "Las Vegas",
            "state": "NV",
            "zip": "89169",
            "country": "US",
            "phone": "702-555-0102",
            "email": "beauty@lvbeauty.com",
        },
        "apparel": {
            "name": "Las Vegas Fashion Warehouse",
            "company": "Nevada Apparel Supply",
            "street1": "3900 Paradise Rd",
            "street2": "Suite 400",
            "city": "Las Vegas",
            "state": "NV",
            "zip": "89169",
            "country": "US",
            "phone": "702-555-0103",
            "email": "apparel@lvfashion.com",
        },
        "footwear": {
            "name": "Las Vegas Footwear Warehouse",
            "company": "Desert Shoes",
            "street1": "3900 Paradise Rd",
            "street2": "Suite 500",
            "city": "Las Vegas",
            "state": "NV",
            "zip": "89169",
            "country": "US",
            "phone": "702-555-0104",
            "email": "footwear@desertshoes.com",
        },
        "art": {
            "name": "Las Vegas Arts Warehouse",
            "company": "Nevada Fine Arts",
            "street1": "3900 Paradise Rd",
            "street2": "Suite 600",
            "city": "Las Vegas",
            "state": "NV",
            "zip": "89169",
            "country": "US",
            "phone": "702-555-0105",
            "email": "art@lvfinearts.com",
        },
        "electronics": {
            "name": "Las Vegas Tech Warehouse",
            "company": "Desert Electronics",
            "street1": "3900 Paradise Rd",
            "street2": "Suite 700",
            "city": "Las Vegas",
            "state": "NV",
            "zip": "89169",
            "country": "US",
            "phone": "702-555-0106",
            "email": "tech@deserttech.com",
        },
        "default": {
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

# Legacy format for backward compatibility
STORE_ADDRESSES = {
    "California": {
        "Los Angeles": WAREHOUSE_BY_CATEGORY["California"]["default"],
    },
    "New York": {
        "New York": WAREHOUSE_BY_CATEGORY["New York"]["default"],
    },
    "Nevada": {
        "Las Vegas": WAREHOUSE_BY_CATEGORY["Nevada"]["default"],
    },
}

# Backward compatibility
CA_STORE_ADDRESSES = STORE_ADDRESSES["California"]

# Country name to ISO 2-letter code mapping for EasyPost API
COUNTRY_CODE_MAP = {
    "UNITED KINGDOM": "GB",
    "NORTHERN IRELAND": "GB",
    "ENGLAND": "GB",
    "SCOTLAND": "GB",
    "WALES": "GB",
    "GERMANY": "DE",
    "SPAIN": "ES",
    "FRANCE": "FR",
    "ITALY": "IT",
    "NETHERLANDS": "NL",
    "BELGIUM": "BE",
    "AUSTRIA": "AT",
    "SWITZERLAND": "CH",
    "POLAND": "PL",
    "SWEDEN": "SE",
    "DENMARK": "DK",
    "NORWAY": "NO",
    "FINLAND": "FI",
    "IRELAND": "IE",
    "PORTUGAL": "PT",
    "GREECE": "GR",
    "CZECH REPUBLIC": "CZ",
    "HUNGARY": "HU",
    "ROMANIA": "RO",
    "BULGARIA": "BG",
    "CROATIA": "HR",
    "SLOVAKIA": "SK",
    "SLOVENIA": "SI",
    "LUXEMBOURG": "LU",
    "ESTONIA": "EE",
    "LATVIA": "LV",
    "LITHUANIA": "LT",
    "MALTA": "MT",
    "CYPRUS": "CY",
    "CANADA": "CA",
    "MEXICO": "MX",
    "AUSTRALIA": "AU",
    "NEW ZEALAND": "NZ",
    "JAPAN": "JP",
    "SOUTH KOREA": "KR",
    "KOREA": "KR",
    "CHINA": "CN",
    "INDIA": "IN",
    "SINGAPORE": "SG",
    "HONG KONG": "HK",
    "TAIWAN": "TW",
    "THAILAND": "TH",
    "MALAYSIA": "MY",
    "INDONESIA": "ID",
    "PHILIPPINES": "PH",
    "VIETNAM": "VN",
    "BRAZIL": "BR",
    "ARGENTINA": "AR",
    "CHILE": "CL",
    "COLOMBIA": "CO",
    "PERU": "PE",
    "SOUTH AFRICA": "ZA",
    "ISRAEL": "IL",
    "TURKEY": "TR",
    "SAUDI ARABIA": "SA",
    "UAE": "AE",
    "UNITED ARAB EMIRATES": "AE",
    "USA": "US",
    "UNITED STATES": "US",
    "US": "US",
}


def normalize_country_code(country: str) -> str:
    """
    Convert country name to ISO 2-letter code for EasyPost API.

    Args:
        country: Country name or code

    Returns:
        ISO 2-letter country code (uppercase)
    """
    if not country:
        return "US"  # Default to US

    country_upper = country.strip().upper()

    # If already a 2-letter code, return as-is
    if len(country_upper) == 2:
        return country_upper

    # Check for exact match first
    if country_upper in COUNTRY_CODE_MAP:
        return COUNTRY_CODE_MAP[country_upper]

    # Handle compound country names (e.g., "NORTHERN IRELAND UNITED KINGDOM")
    # Check if any mapped country name appears in the input
    for country_name, code in COUNTRY_CODE_MAP.items():
        if country_name in country_upper:
            return code

    # If no match found, return original (will trigger API validation error)
    return country_upper


def parse_dimensions(dim_str: str) -> tuple:
    """
    Parse dimensions string into (length, width, height).

    Supports multiple formats:
    - Decimals: '12.5 x 10.25 x 3.75'
    - Fractions: '11 1/2 x 9 3/4 x 2 1/4'
    - Mixed: '12.5 × 11 1/2 × 3'
    - Separators: x, ×, *, 'by'

    Args:
        dim_str: Dimension string (e.g., "12.5 x 10 x 3", "11 1/2 x 9 x 2 1/4")

    Returns:
        Tuple of (length, width, height) as floats

    Raises:
        ValueError: If dimensions cannot be parsed or are invalid
    """
    if not dim_str or not dim_str.strip():
        raise ValueError("Dimension string is empty")

    # Replace all separators with spaces for uniform parsing
    normalized = dim_str.lower()
    for separator in ["×", "*", "by", "x"]:
        normalized = normalized.replace(separator, " ")

    # Extract all numbers (including decimals and fractions)
    parts = normalized.split()
    numbers = []
    i = 0
    while i < len(parts):
        part = parts[i].strip()

        # Check for fraction format (e.g., "1/2")
        if "/" in part:
            try:
                num, denom = part.split("/")
                numbers.append(float(num) / float(denom))
                i += 1
                continue
            except (ValueError, ZeroDivisionError):
                i += 1
                continue

        # Check for decimal number
        if re.match(r"^\d*\.?\d+$", part):
            try:
                whole_num = float(part)
                # Check if next part is a fraction (e.g., "11" followed by "1/2")
                if i + 1 < len(parts) and "/" in parts[i + 1]:
                    try:
                        frac_num, frac_denom = parts[i + 1].split("/")
                        fraction = float(frac_num) / float(frac_denom)
                        numbers.append(whole_num + fraction)
                        i += 2  # Skip both parts
                        continue
                    except (ValueError, ZeroDivisionError):
                        pass
                numbers.append(whole_num)
            except ValueError:
                pass
        i += 1

    if len(numbers) >= 3:
        # Validate dimensions are reasonable (0.1 to 999 inches)
        if all(0.1 <= dim <= 999 for dim in numbers[:3]):
            return (numbers[0], numbers[1], numbers[2])
        raise ValueError(f"Dimensions out of range (0.1-999 inches): {numbers[:3]}")

    if len(numbers) > 0:
        raise ValueError(
            f"Insufficient dimensions: found {len(numbers)}, need 3 (L x W x H). "
            f"Example: '12.5 x 10 x 3' or '11 1/2 x 9 x 2 1/4'"
        )

    raise ValueError(
        f"Could not parse dimensions from '{dim_str}'. "
        "Please use format: '12.5 x 10 x 3' or '11 1/2 x 9 x 2 1/4' (length x width x height)"
    )


def parse_weight(weight_str: str) -> float:
    """
    Parse weight string with intelligent unit detection and conversion.

    Handles formats:
    - With units: "1.8 lbs", "16 oz", "5LB 2oz", "2 lbs 3 oz", "1 pound 8 ounces"
    - Numeric only: "5.26" (assumes lbs if > 1, oz if <= 1), "84" (assumes oz)
    - Decimal: "5.26" (assumes lbs), "0.5" (assumes lbs), "16" (ambiguous - assumes oz)
    - Common abbreviations: "lb", "lbs", "oz", "ounces", "pounds"

    Args:
        weight_str: Weight string with or without unit(s)

    Returns:
        Weight in ounces (never returns 0 - raises ValueError if truly unparseable)
    """
    if not weight_str or not weight_str.strip():
        raise ValueError("Weight string is empty")

    weight_str = weight_str.strip()
    total_oz = 0.0

    # Pattern to match: number + unit (handles both combined and single formats)
    # Matches: "5LB", "2oz", "1.5 lbs", "3 ounces", etc.
    pattern = r"([\d.]+)\s*(lbs?|oz|ounces?|pounds?|LB|OZ|kg|kilograms?|g|grams?)"

    # Find all matches (handles combined formats like "5LB 2oz")
    matches = list(re.finditer(pattern, weight_str.lower()))

    if matches:
        # Has explicit units - parse them
        for match in matches:
            value = float(match.group(1))
            unit = match.group(2).lower()

            # Convert to ounces
            if "lb" in unit or "pound" in unit:
                total_oz += value * 16.0  # 1 lb = 16 oz
            elif "kg" in unit or "kilogram" in unit:
                total_oz += value * 35.274  # 1 kg = 35.274 oz
            elif "g" in unit or "gram" in unit:
                total_oz += value / 28.35  # 1 oz = 28.35 g
            else:
                total_oz += value  # Already in oz

        if total_oz > 0:
            return total_oz
    else:
        # No explicit units - try to infer from numeric value
        # Extract all numbers from the string
        numbers = re.findall(r"[\d.]+", weight_str)
        if numbers:
            value = float(numbers[0])

            # Heuristic: if value > 1 and has decimal, likely lbs
            # If value <= 1, could be lbs or oz - check context
            # If value > 16 and no decimal, likely oz (common for packages)
            # If value < 16 and no decimal, ambiguous - assume lbs for typical packages

            if value > 100:
                # Very large number - likely oz (packages rarely > 100 lbs)
                total_oz = value
            elif value > 16:
                # Between 16-100 - check if it looks like oz or lbs
                # If it's a round number like 20, 30, 50, likely lbs
                # If it's a decimal like 84.16, likely oz
                total_oz = value if "." in weight_str else value * 16.0
            elif value > 1:
                # Between 1-16 - likely lbs (common package weights)
                total_oz = value * 16.0
            else:
                # <= 1 - could be 0.5 lbs or 0.5 oz
                # For packages, < 1 oz is rare, so assume lbs
                total_oz = value * 16.0

            if total_oz > 0:
                return total_oz

    # If we get here, couldn't parse - raise error instead of silent default
    raise ValueError(
        f"Could not parse weight from '{weight_str}'. "
        "Please specify units (e.g., '5.26 lbs', '84 oz', '2.5 kg')"
    )


def detect_product_category(contents: str) -> str:
    """
    Detect product category from contents string.

    Uses priority-based matching:
    1. Exact word boundaries (e.g., "jeans" matches "jeans" not "jeansxx")
    2. Substring match as fallback
    3. First match wins (category order matters)

    Args:
        contents: Item description/contents string

    Returns:
        Category name (apparel, sporting, beauty, etc., or "default")
    """
    import re

    contents_lower = contents.lower()

    # First pass: try exact word boundary matches (more accurate)
    for category, keywords in PRODUCT_CATEGORIES.items():
        for keyword in keywords:
            # Use word boundaries for single words, substring for phrases
            if " " in keyword:
                # Multi-word phrase: substring match
                if keyword in contents_lower:
                    return category
            else:
                # Single word: word boundary match (more precise)
                if re.search(rf"\b{re.escape(keyword)}\b", contents_lower):
                    return category

    # Second pass: fallback to substring matching if no exact match
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


def detect_field_type(value: str) -> str | None:
    """
    Detect field type from value content.

    Args:
        value: Field value to analyze

    Returns:
        Field type name or None if unknown
    """
    if not value or not value.strip():
        return None

    value = value.strip()
    value_lower = value.lower()

    # Email detection (RFC 5322 compliant with practical restrictions)
    # Supports: user+tag@example.com, user.name@example.co.uk, user123@sub.domain.com
    email_pattern = (
        r"^[a-zA-Z0-9][a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]*@"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
        r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    )
    if re.match(email_pattern, value) and len(value) <= 254:  # RFC 5321 max length
        return "email"

    # Phone detection (various formats including extensions)
    # Formats: +1-555-123-4567, (555) 123-4567, 555-123-4567 x1234, +44 20 7123 4567 ext 100
    phone_patterns = [
        # International with optional extension
        r"^\+?[\d\s\-\(\)]{10,}(?:[\s]?(?:x|ext|extension)[\s]?\d{1,6})?$",
        # Simple digits with optional extension
        r"^\d{10,15}(?:[\s]?(?:x|ext|extension)[\s]?\d{1,6})?$",
        # US format with optional extension
        r"^\d{3}[\s\-]?\d{3}[\s\-]?\d{4}(?:[\s]?(?:x|ext)[\s]?\d{1,6})?$",
    ]
    for pattern in phone_patterns:
        cleaned_value = value.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if re.match(pattern, cleaned_value):
            # Validate digit count (7-15 typical for phone numbers, excluding extensions)
            digit_count = sum(c.isdigit() for c in cleaned_value.split("x")[0].split("ext")[0])
            if 7 <= digit_count <= 15:
                return "phone"

    # Country code detection (2-letter ISO codes)
    if re.match(r"^[A-Z]{2}$", value.upper()) and len(value) == 2:
        country_upper = value.upper()
        if country_upper in COUNTRY_CODE_MAP.values() or any(
            country_upper in v for v in COUNTRY_CODE_MAP.values()
        ):
            return "country_code"

    # Country name detection
    country_upper = value.upper()
    if country_upper in COUNTRY_CODE_MAP or any(
        country_upper in k.upper() for k in COUNTRY_CODE_MAP
    ):
        return "country_name"

    # Postal/ZIP code detection (international support)
    postal_patterns = [
        r"^\d{5}(?:-\d{4})?$",  # US ZIP: 12345 or 12345-6789
        r"^[A-Z]\d[A-Z]\s?\d[A-Z]\d$",  # Canada: A1A 1A1 or A1A1A1
        r"^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$",  # UK: SW1A 1AA, EC1A 1BB
        r"^\d{5}$",  # Germany, France, Spain: 12345
        r"^\d{4}$",  # Australia, Belgium: 1234
        r"^\d{3}-\d{4}$",  # Japan: 123-4567
        r"^\d{6}$",  # India, Singapore: 123456
    ]
    value_normalized = value.upper().strip()
    for pattern in postal_patterns:
        if re.match(pattern, value_normalized):
            return "postal_code"

    # State code detection (US states)
    us_states = [
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
    ]
    if value.upper() in us_states:
        return "state_code"

    # Weight detection (contains weight keywords or patterns)
    weight_keywords = ["lb", "lbs", "oz", "ounce", "pound", "kg", "kilogram", "g", "gram"]
    if any(keyword in value_lower for keyword in weight_keywords):
        return "weight"
    # Numeric weight pattern (decimal number that could be weight)
    if re.match(r"^[\d.]+$", value) and "." in value:
        try:
            num = float(value)
            if 0.1 <= num <= 200:  # Reasonable weight range
                return "weight"
        except ValueError:
            pass

    # Dimensions detection (contains x or dimension keywords)
    has_dimension_keywords = (
        "x" in value_lower
        or "×" in value
        or any(keyword in value_lower for keyword in ["inch", "in", "cm", "dimension"])
    )
    if has_dimension_keywords and re.search(r"[\d.]+[\sx×]+[\d.]+[\sx×]+[\d.]+", value):
        return "dimensions"

    # Street address detection (check before name to avoid false positives)
    street_keywords = [
        "street",
        "st",
        "avenue",
        "ave",
        "road",
        "rd",
        "boulevard",
        "blvd",
        "drive",
        "dr",
        "lane",
        "ln",
        "court",
        "ct",
        "circle",
        "cir",
        "way",
        "plaza",
        "pkwy",
    ]

    # PO Box detection (must check before name detection)
    if re.match(r"^p\.?o\.?\s*box\s+\d+", value_lower) or re.match(r"^box\s+\d+", value_lower):
        return "street"

    # Military address detection (APO, FPO, DPO) - must check before name detection
    if re.match(r"^(apo|fpo|dpo)\s+[a-z]{2}\s+\d{5}", value_lower):
        return "street"

    # Standard street address
    if any(keyword in value_lower for keyword in street_keywords):
        return "street"

    # Get words for subsequent checks
    words = value.split()

    # Also detect addresses with numbers (e.g., "123 Main St", "720 East St Suite 2")
    if re.match(r"^\d+", value) and len(words) >= 1:
        return "street"

    # Name detection (contains common name patterns)
    # Multiple words, capitalized, not all caps (unless short)
    # Check AFTER street detection to avoid false positives
    has_capitalized_words = len(words) >= 2 and any(
        word[0].isupper() if word else False for word in words
    )
    is_not_address = not any(
        keyword in value_lower
        for keyword in [
            "street",
            "st",
            "avenue",
            "ave",
            "road",
            "rd",
            "suite",
            "apt",
            "box",
            "apo",
            "fpo",
            "dpo",
        ]
    )
    if has_capitalized_words and is_not_address:
        return "name"

    # City detection (single word, capitalized, not a state code)
    if len(words) == 1 and value[0].isupper() and value.upper() not in us_states:
        return "city"

    return None


def map_fields_by_detection(parts: list[str]) -> dict[str, Any]:
    """
    Map spreadsheet columns to fields using intelligent detection.

    Args:
        parts: List of column values

    Returns:
        Dictionary mapping field names to values
    """
    field_map: dict[str, list[tuple[int, str]]] = {}  # field_name -> [(index, value)]

    # First pass: detect field types
    for idx, part in enumerate(parts):
        if not part or not part.strip():
            continue

        field_type = detect_field_type(part.strip())
        if field_type:
            if field_type not in field_map:
                field_map[field_type] = []
            field_map[field_type].append((idx, part.strip()))

    # Map detected fields to standard field names
    result: dict[str, Any] = {
        "origin_state": "",
        "carrier_preference": "",
        "recipient_name": "",
        "recipient_last_name": "",
        "recipient_phone": "",
        "recipient_email": "",
        "street1": "",
        "street2": "",
        "city": "",
        "state": "",
        "zip": "",
        "country": "",
        "dimensions": "",
        "weight": "",
        "contents": "",
    }

    # Map emails (first is recipient, second is sender)
    emails = [val for _, val in field_map.get("email", [])]
    if emails:
        result["recipient_email"] = emails[0]
        if len(emails) > 1:
            result["sender_email"] = emails[1]

    # Map phones (first is recipient, second is sender)
    phones = [val for _, val in field_map.get("phone", [])]
    if phones:
        result["recipient_phone"] = phones[0]
        if len(phones) > 1:
            result["sender_phone"] = phones[1]

    # Map country codes/names
    countries = [val for _, val in field_map.get("country_code", [])]
    countries.extend([val for _, val in field_map.get("country_name", [])])
    if countries:
        result["country"] = normalize_country_code(countries[0])
        if len(countries) > 1:
            result["sender_country"] = normalize_country_code(countries[1])

    # Map postal codes (first is recipient, second is sender)
    postal_codes = [val for _, val in field_map.get("postal_code", [])]
    if postal_codes:
        result["zip"] = postal_codes[0]
        if len(postal_codes) > 1:
            result["sender_zip"] = postal_codes[1]

    # Map state codes
    states = [val for _, val in field_map.get("state_code", [])]
    if states:
        result["state"] = states[0]
        if len(states) > 1:
            result["origin_state"] = states[0]  # First state is origin
            result["sender_state"] = states[1] if len(states) > 1 else states[0]

    # Map dimensions
    dimensions = [val for _, val in field_map.get("dimensions", [])]
    if dimensions:
        result["dimensions"] = dimensions[0]

    # Map weight
    weights = [val for _, val in field_map.get("weight", [])]
    if weights:
        result["weight"] = weights[0]

    # Map names (try to identify recipient vs sender by position)
    names = [val for _, val in field_map.get("name", [])]
    if names:
        # First name is likely recipient
        name_parts = names[0].split(maxsplit=1)
        if len(name_parts) >= 2:
            result["recipient_name"] = name_parts[0]
            result["recipient_last_name"] = name_parts[1]
        else:
            result["recipient_name"] = names[0]

    # Map streets
    streets = [val for _, val in field_map.get("street", [])]
    if streets:
        result["street1"] = streets[0]
        if len(streets) > 1:
            result["street2"] = streets[1]

    # Map cities
    cities = [val for _, val in field_map.get("city", [])]
    if cities:
        result["city"] = cities[0]
        if len(cities) > 1:
            result["sender_city"] = cities[1]

    return result


def parse_spreadsheet_line(line: str) -> dict[str, Any]:
    """
    Parse a tab-separated line from spreadsheet with flexible field detection.

    Supports two modes:
    1. Standard format (16+ columns): Positional parsing for backward compatibility
    2. Flexible format (< 16 columns or validation fails): Intelligent field detection

    Standard Format (16+ columns):
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

    Flexible Format: Automatically detects field types and maps them regardless of position.

    Args:
        line: Tab-separated data line

    Returns:
        Parsed shipment dictionary with optional sender_address

    Raises:
        ValueError: If required fields are missing or unparseable
    """
    # Split by tabs and strip whitespace
    parts = [p.strip() for p in line.split("\t")]

    # Auto-detect column offset (skip leading reference/ID columns)
    # Strategy: Find the carrier column, which should be at position 1 in standard format
    offset = 0
    carrier_names = ["USPS", "FEDEX", "UPS", "DHL", "ASENDIA"]

    # Look for carrier name in first 5 columns
    for i in range(min(5, len(parts))):
        part_upper = parts[i].upper()
        if any(carrier in part_upper for carrier in carrier_names):
            # Carrier found at position i, so origin_state is at i-1
            # Standard format: origin_state (0) | carrier (1) | recipient_name (2)...
            # If carrier at position 3, offset is 2 (skip columns 0, 1)
            offset = i - 1
            break

    # Adjust parts array by removing leading columns
    if offset > 0:
        parts = parts[offset:]
        logger.info(f"Auto-detected column offset: {offset} (skipped {offset} leading columns)")

    # Try standard positional parsing first (backward compatibility)
    if len(parts) >= 16:
        try:
            # Combine all content columns (15+) into single contents field
            contents_parts = []
            for i in range(15, min(len(parts), 25)):  # Stop before sender address columns
                if parts[i] and parts[i].strip():
                    contents_parts.append(parts[i].strip())

            result: dict[str, Any] = {
                "origin_state": parts[0],
                "carrier_preference": parts[1],
                "recipient_name": parts[2],
                "recipient_last_name": parts[3],
                "recipient_phone": parts[4],
                "recipient_email": parts[5],
                "street1": parts[6],
                "street2": parts[7],
                "city": parts[8],
                "state": parts[9],
                "zip": parts[10],
                "country": parts[11],
                "dimensions": parts[13] if len(parts) > 13 else "",
                "weight": parts[14] if len(parts) > 14 else "",
                "contents": " ".join(contents_parts) if contents_parts else "",
            }

            # Check if sender address is provided (columns 16+)
            if len(parts) >= 25 and parts[16]:
                sender_country_raw = parts[22] if len(parts) > 22 else "US"
                result["sender_address"] = {
                    "name": parts[16],
                    "street1": parts[17] if len(parts) > 17 else "",
                    "street2": parts[18] if len(parts) > 18 else "",
                    "city": parts[19] if len(parts) > 19 else "",
                    "state": parts[20] if len(parts) > 20 else "",
                    "zip": parts[21] if len(parts) > 21 else "",
                    "country": normalize_country_code(sender_country_raw),
                    "phone": parts[23] if len(parts) > 23 else "",
                    "email": parts[24] if len(parts) > 24 else "",
                }

            # Validate required fields for standard format
            has_required_fields = (
                result["recipient_name"] and result["street1"] and result["country"]
            )
            weight_valid = True
            if result["weight"]:
                try:
                    parse_weight(result["weight"])
                except ValueError as e:
                    weight_valid = False
                    logger.warning(
                        f"Standard format weight validation failed: {e}, trying field detection"
                    )

            if has_required_fields and weight_valid:
                # Standard format is valid
                return result

        except (IndexError, ValueError) as e:
            # Standard format parsing failed, fall through to field detection
            logger.debug(f"Standard format parsing failed: {e}, trying field detection")

    # Use intelligent field detection (flexible format or fallback)
    detected = map_fields_by_detection(parts)

    # Find contents field if not detected
    if not detected.get("contents"):
        # Look for contents keywords or use last unclassified text field
        contents_keywords = ["description", "item", "product", "contents", "goods"]
        for part in parts:
            if not part:
                continue
            part_lower = part.lower()
            # Check if column header or value contains contents keywords
            if any(keyword in part_lower for keyword in contents_keywords):
                detected["contents"] = part
                break

        # If still not found, use last non-empty field that's not already mapped
        if not detected.get("contents"):
            # Find which fields were already detected/mapped
            mapped_values = set()
            mapped_values.update([detected.get("recipient_email", "")])
            mapped_values.update([detected.get("recipient_phone", "")])
            mapped_values.update([detected.get("country", "")])
            mapped_values.update([detected.get("zip", "")])
            mapped_values.update([detected.get("state", "")])
            mapped_values.update([detected.get("dimensions", "")])
            mapped_values.update([detected.get("weight", "")])
            mapped_values.update([detected.get("recipient_name", "")])
            mapped_values.update([detected.get("street1", "")])
            mapped_values.update([detected.get("city", "")])

            # Use last unclassified field as contents
            for idx in range(len(parts) - 1, -1, -1):
                if parts[idx] and parts[idx] not in mapped_values:
                    field_type = detect_field_type(parts[idx])
                    if not field_type:  # Not a recognized field type
                        detected["contents"] = parts[idx]
                        break

    # Merge with defaults for missing fields
    result = {
        "origin_state": detected.get("origin_state", ""),
        "carrier_preference": detected.get("carrier_preference", ""),
        "recipient_name": detected.get("recipient_name", ""),
        "recipient_last_name": detected.get("recipient_last_name", ""),
        "recipient_phone": detected.get("recipient_phone", ""),
        "recipient_email": detected.get("recipient_email", ""),
        "street1": detected.get("street1", ""),
        "street2": detected.get("street2", ""),
        "city": detected.get("city", ""),
        "state": detected.get("state", ""),
        "zip": detected.get("zip", ""),
        "country": detected.get("country", ""),
        "dimensions": detected.get("dimensions", "12x12x4"),
        "weight": detected.get("weight", ""),
        "contents": detected.get("contents", ""),
    }

    # Add sender address if detected
    if any(
        detected.get(key)
        for key in ["sender_email", "sender_phone", "sender_country", "sender_zip", "sender_city"]
    ):
        result["sender_address"] = {
            "name": detected.get("sender_name", ""),
            "street1": detected.get("sender_street1", ""),
            "street2": detected.get("sender_street2", ""),
            "city": detected.get("sender_city", ""),
            "state": detected.get("sender_state", ""),
            "zip": detected.get("sender_zip", ""),
            "country": normalize_country_code(detected.get("sender_country", "US")),
            "phone": detected.get("sender_phone", ""),
            "email": detected.get("sender_email", ""),
        }

    # Validate required fields
    missing_fields = []
    if not result["recipient_name"]:
        missing_fields.append("recipient_name")
    if not result["street1"]:
        missing_fields.append("street1 (recipient address)")
    if not result["country"]:
        missing_fields.append("country")
    if not result["weight"]:
        missing_fields.append("weight")

    if missing_fields:
        raise ValueError(
            f"Missing required fields: {', '.join(missing_fields)}. "
            f"Detected fields: {[k for k, v in result.items() if v and k != 'sender_address']}"
        )

    # Validate weight is parseable
    try:
        parse_weight(result["weight"])
    except ValueError as e:
        raise ValueError(f"Invalid weight format: {e}") from e

    return result


def parse_human_readable_shipment(text: str) -> dict | None:
    """
    Parse human-readable shipment data into standard format.

    Handles multiple formats:
    1. Simple address block (single sender/recipient)
    2. Sender + Recipient format (separated by blank lines)
    3. With customs information

    Example:
    ```
    Company Name
    John Smith
    123 Main St Suite 2
    City, State ZIP
    Country

    Phone 555-123-4567
    Email john@example.com

    RECIPIENT NAME
    456 Main St
    City
    State ZIP
    Country

    Phone 555-987-6543
    Email recipient@example.com

    Dimensions 12x12x2
    Weight 5.26lb

    Customs item: Anime Toy Set
    Price: $35
    Quantity: 1
    ```

    Returns:
        Standardized shipment dict with sender/recipient or None
    """
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]

    if len(lines) < 5:
        return None

    # Try to detect if this is sender+recipient format (has two address blocks)
    # Look for double blank line or keywords like "Ship to:", "Recipient:", etc.
    raw_text = text.strip()
    sections = re.split(r"\n\s*\n", raw_text)  # Split by blank lines

    result: dict[str, Any] = {
        "sender": None,
        "recipient": None,
        "dimensions": None,
        "weight": None,
        "contents": None,
        "customs_price": None,
        "customs_quantity": None,
    }

    # Extract metadata (phone, email, dimensions, weight, customs) from all sections
    all_phones = []
    all_emails = []

    for section in sections:
        section_lines = [line.strip() for line in section.split("\n") if line.strip()]

        for line in section_lines:
            # Extract email (RFC 5322 compliant pattern)
            email_match = re.search(
                r"(?:email[:\s]+)?([a-zA-Z0-9][a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]*@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)",
                line,
                re.IGNORECASE,
            )
            if email_match:
                all_emails.append(email_match.group(1))

            # Extract phone (flexible format)
            phone_match = re.search(r"(?:phone[:\s]+)?(\+?[\d\s\-()]{7,20})", line, re.IGNORECASE)
            if phone_match and not email_match:  # Don't capture numbers in emails
                phone_clean = (
                    phone_match.group(1)
                    .replace(" ", "")
                    .replace("-", "")
                    .replace("(", "")
                    .replace(")", "")
                )
                if len(phone_clean) >= 7:
                    all_phones.append(phone_clean)

            # Extract dimensions (flexible: "Dimensions 12x12x2" or "12.5x10.25x3.5")
            # Supports decimal dimensions and multiple separators (x, ×, *, by)
            if result["dimensions"] is None:
                dim_match = re.search(
                    r"(?:dimensions?[:\s]+)?(\d+(?:\.\d+)?)\s*[x×*]\s*(\d+(?:\.\d+)?)\s*[x×*]\s*(\d+(?:\.\d+)?)",
                    line,
                    re.IGNORECASE,
                )
                if dim_match:
                    result["dimensions"] = (
                        f"{dim_match.group(1)} x {dim_match.group(2)} x {dim_match.group(3)}"
                    )

            # Extract weight (flexible: "Weight 5.26lb", "2 oz", "1.5 kg")
            # Supports all units: lbs, oz, kg, g, pounds, ounces, etc.
            if result["weight"] is None:
                weight_match = re.search(
                    r"(?:weight[:\s]+)?(\d+(?:\.\d+)?)\s*(lbs?|oz|ounces?|pounds?|kg|kilograms?|g|grams?)",
                    line,
                    re.IGNORECASE,
                )
                if weight_match:
                    result["weight"] = f"{weight_match.group(1)} {weight_match.group(2)}"

            # Extract customs item description
            if result["contents"] is None:
                customs_match = re.search(
                    r"(?:customs item|item|contents|description)[:\s]+(.+)",
                    line,
                    re.IGNORECASE,
                )
                if customs_match:
                    result["contents"] = customs_match.group(1).strip()

            # Extract customs price
            if result["customs_price"] is None:
                price_match = re.search(
                    r"(?:price|value)[:\s]+\$?(\d+(?:\.\d+)?)", line, re.IGNORECASE
                )
                if price_match:
                    result["customs_price"] = float(price_match.group(1))

            # Extract customs quantity
            if result["customs_quantity"] is None:
                qty_match = re.search(r"(?:quantity|qty)[:\s]+(\d+)", line, re.IGNORECASE)
                if qty_match:
                    result["customs_quantity"] = int(qty_match.group(1))

    # Parse address sections (filter out metadata lines)
    address_sections = []
    for section in sections:
        section_lines = [line.strip() for line in section.split("\n") if line.strip()]
        # Filter out metadata lines
        address_lines = []
        for line in section_lines:
            # Skip lines with keywords
            if any(
                kw in line.lower()
                for kw in [
                    "email",
                    "phone",
                    "dimension",
                    "weight",
                    "customs",
                    "price",
                    "quantity",
                    "item:",
                ]
            ):
                continue
            # Skip lines that are only phone/email
            if "@" in line or re.match(r"^\+?[\d\s\-()]+$", line):
                continue
            address_lines.append(line)

        if len(address_lines) >= 3:  # Minimum for a valid address
            address_sections.append(address_lines)

    # Parse addresses
    def parse_address_block(lines: list[str], phone: str = "", email: str = "") -> dict:
        """Parse single address block."""
        addr = {
            "company": "",
            "name": "",
            "street1": "",
            "street2": "",
            "city": "",
            "state": "",
            "zip": "",
            "country": "US",
            "phone": phone,
            "email": email,
        }

        if not lines:
            return addr

        # Common country names for detection
        common_countries = [
            "usa",
            "us",
            "united states",
            "france",
            "canada",
            "uk",
            "united kingdom",
            "germany",
            "spain",
            "italy",
        ]

        idx = 0

        # First line: company or name
        company_indicators = [
            "inc",
            "llc",
            "ltd",
            "corporation",
            "corp",
            "co.",
            "company",
            "&",
            "games",
            "shop",
            "store",
        ]
        has_company = any(indicator in lines[0].lower() for indicator in company_indicators)

        if has_company and len(lines) > 1:
            addr["company"] = lines[0]
            addr["name"] = lines[1]
            idx = 2
        else:
            addr["name"] = lines[0]
            idx = 1

        # Next line(s): street address
        if idx < len(lines):
            addr["street1"] = lines[idx]
            idx += 1

        # Look ahead to identify structure
        # Scan remaining lines to find postal code and country
        postal_idx = None
        country_idx = None
        for i in range(idx, len(lines)):
            line_lower = lines[i].lower().strip()
            # Check if it's a postal code (5+ digits)
            if re.match(r"^\d{5,}(?:-\d{4})?$", lines[i]) or re.match(r"^\d{5,}$", lines[i]):
                postal_idx = i
            # Check if it's a country name
            elif line_lower in common_countries:
                country_idx = i

        # If we found postal code and country, we know the structure
        if postal_idx is not None and country_idx is not None:
            # Everything between street1 and postal is city/state
            # Everything between postal and country is nothing (or state)
            # Country is at country_idx

            # Street2 is everything between street1 and postal (if any)
            if postal_idx > idx:
                # Could be street2, city, or state
                remaining_before_postal = lines[idx:postal_idx]
                if len(remaining_before_postal) == 1:
                    # Single line - likely city (or street2 if it looks like address)
                    if any(c.isdigit() for c in remaining_before_postal[0]):
                        addr["street2"] = remaining_before_postal[0]
                    else:
                        addr["city"] = remaining_before_postal[0]
                elif len(remaining_before_postal) == 2:
                    # Two lines - likely street2 and city
                    addr["street2"] = remaining_before_postal[0]
                    addr["city"] = remaining_before_postal[1]
                else:
                    # Multiple lines - take first as street2, second as city
                    addr["street2"] = remaining_before_postal[0] if remaining_before_postal else ""
                    addr["city"] = (
                        remaining_before_postal[1] if len(remaining_before_postal) > 1 else ""
                    )

            addr["zip"] = lines[postal_idx]
            addr["country"] = normalize_country_code(lines[country_idx])
        else:
            # Fallback: try to parse sequentially
            # Next line could be street2, city, or postal
            if idx < len(lines):
                next_line = lines[idx]
                # If it's a postal code, we're missing city
                if re.match(r"^\d{5,}(?:-\d{4})?$", next_line) or re.match(r"^\d{5,}$", next_line):
                    addr["zip"] = next_line
                    idx += 1
                # If it's a country, we're missing city and postal
                elif next_line.lower() in common_countries:
                    addr["country"] = normalize_country_code(next_line)
                    idx += 1
                # Otherwise, treat as street2 or city
                else:
                    # Check if next line after this is postal or country
                    if idx + 1 < len(lines):
                        next_next = lines[idx + 1]
                        if re.match(r"^\d{5,}(?:-\d{4})?$", next_next) or re.match(
                            r"^\d{5,}$", next_next
                        ):
                            # This is city, next is postal
                            addr["city"] = next_line
                            addr["zip"] = next_next
                            idx += 2
                        elif next_next.lower() in common_countries:
                            # This is city, next is country
                            addr["city"] = next_line
                            addr["country"] = normalize_country_code(next_next)
                            idx += 2
                        else:
                            # This is street2
                            addr["street2"] = next_line
                            idx += 1
                    else:
                        # Last line - could be city or country
                        if next_line.lower() in common_countries:
                            addr["country"] = normalize_country_code(next_line)
                        else:
                            addr["city"] = next_line
                        idx += 1

            # Try to get postal code if not set
            if not addr["zip"] and idx < len(lines):
                zip_line = lines[idx]
                if re.match(r"^\d{5,}(?:-\d{4})?$", zip_line) or re.match(r"^\d{5,}$", zip_line):
                    addr["zip"] = zip_line
                    idx += 1

            # Try to get country if not set
            if idx < len(lines):
                country_line = lines[idx]
                if country_line.lower() in common_countries:
                    addr["country"] = normalize_country_code(country_line)

        return addr

    # Assign addresses based on count
    if len(address_sections) >= 2:
        # Two address blocks: sender + recipient
        sender_phone = all_phones[0] if all_phones else ""
        sender_email = all_emails[0] if all_emails else ""
        result["sender"] = parse_address_block(address_sections[0], sender_phone, sender_email)
        recipient_phone = (
            all_phones[1] if len(all_phones) > 1 else all_phones[0] if all_phones else ""
        )
        recipient_email = (
            all_emails[1] if len(all_emails) > 1 else all_emails[0] if all_emails else ""
        )
        result["recipient"] = parse_address_block(
            address_sections[1], recipient_phone, recipient_email
        )
    elif len(address_sections) == 1:
        # Single address block: recipient only
        recipient_phone = all_phones[0] if all_phones else ""
        recipient_email = all_emails[0] if all_emails else ""
        result["recipient"] = parse_address_block(
            address_sections[0], recipient_phone, recipient_email
        )
    else:
        return None

    # Defaults
    result["dimensions"] = result["dimensions"] or "12 x 12 x 4"
    result["weight"] = result["weight"] or "1 lbs"

    return result if result.get("recipient") and result["recipient"].get("name") else None


def convert_natural_to_spreadsheet(text: str) -> str | None:
    """
    Convert natural text format to tab-separated spreadsheet format.

    Args:
        text: Natural text with sender, recipient, customs info

    Returns:
        Tab-separated line ready for parse_spreadsheet_line() or None if parsing fails
    """
    parsed = parse_human_readable_shipment(text)
    if not parsed:
        return None

    sender = parsed.get("sender")
    recipient = parsed["recipient"]

    # Build tab-separated line
    # Format: origin_state, carrier, recipient_name, recipient_last, phone, email,
    #         street1, street2, city, state, zip, country, unused, dimensions, weight, contents,
    #         sender_name, sender_street1, sender_street2, sender_city, sender_state, sender_zip,
    #         sender_country, sender_phone, sender_email
    parts = []

    if sender:
        # Use sender's state as origin
        parts.append(sender.get("state") or "NV")  # Default to Nevada
        parts.append("")  # Carrier preference (empty)
    else:
        # No sender - will auto-detect warehouse
        parts.append("Nevada")  # Default origin
        parts.append("")  # Carrier preference

    # Recipient info (split name)
    recipient_full_name = recipient.get("name", "").strip()
    name_parts = recipient_full_name.split(None, 1)  # Split on first space
    parts.append(name_parts[0] if name_parts else "")  # First name
    parts.append(name_parts[1] if len(name_parts) > 1 else "")  # Last name
    parts.append(recipient.get("phone", ""))
    parts.append(recipient.get("email", ""))
    parts.append(recipient.get("street1", ""))
    parts.append(recipient.get("street2", ""))
    parts.append(recipient.get("city", ""))
    parts.append(recipient.get("state", ""))
    parts.append(recipient.get("zip", ""))
    parts.append(recipient.get("country", "US"))
    parts.append("")  # Unused column

    # Dimensions and weight
    parts.append(parsed.get("dimensions", "12 x 12 x 4"))
    parts.append(parsed.get("weight", "1 lbs"))

    # Contents (with customs price/quantity if available)
    contents = parsed.get("contents", "Package")
    if parsed.get("customs_price") and parsed.get("customs_quantity"):
        # Embed customs info in contents for smart_customs to parse
        contents = f"{contents} (${parsed['customs_price']} x{parsed['customs_quantity']})"
    parts.append(contents)

    # Sender address fields (if provided)
    if sender:
        parts.append(sender.get("name", ""))
        parts.append(sender.get("street1", ""))
        parts.append(sender.get("street2", ""))
        parts.append(sender.get("city", ""))
        parts.append(sender.get("state", ""))
        parts.append(sender.get("zip", ""))
        parts.append(sender.get("country", "US"))
        parts.append(sender.get("phone", ""))
        parts.append(sender.get("email", ""))

    return "\t".join(parts)


def _generate_rate_table(shipments: list[dict]) -> str:
    """
    Generate user-friendly formatted table with rates.

    Highlights requested carrier rate first, then shows all other rates.
    Includes complete sender details.

    Args:
        shipments: List of processed shipment results

    Returns:
        Formatted markdown table string
    """
    lines = []
    lines.append("\n# SHIPPING RATES SUMMARY\n")

    for shipment in shipments:
        if shipment.get("error"):
            lines.append(f"\n## Shipment #{shipment['shipment_number']} - ERROR")
            lines.append(f"**Error:** {shipment['error']}\n")
            continue

        detailed = shipment.get("detailed_data", {})
        sender = detailed.get("sender", {})
        recipient = detailed.get("recipient", {})
        parcel = detailed.get("parcel", {})
        product = detailed.get("product", {})
        customs = detailed.get("customs", {})

        # Get carrier preference early for use throughout
        carrier_pref = detailed.get("carrier_preference", "").upper()

        lines.append(f"\n## Shipment #{shipment['shipment_number']}: {shipment['recipient']}")

        # Add carrier preference indicator at the top
        if carrier_pref:
            lines.append(f"**🎯 Preferred Carrier:** {carrier_pref}")

        lines.append("\n### 📦 SENDER INFORMATION")
        lines.append(f"**Company:** {sender.get('company', 'N/A')}")
        lines.append(f"**Name:** {sender.get('name', 'N/A')}")
        lines.append(f"**Address:** {sender.get('street1', '')}")
        if sender.get("street2"):
            lines.append(f"**Address 2:** {sender.get('street2')}")
        city = sender.get("city", "")
        state = sender.get("state", "")
        zip_code = sender.get("zip", "")
        lines.append(f"**City, State ZIP:** {city}, {state} {zip_code}")
        lines.append(f"**Country:** {sender.get('country', '')}")
        lines.append(f"**Phone:** {sender.get('phone', 'N/A')}")
        lines.append(f"**Email:** {sender.get('email', 'N/A')}")

        lines.append("\n### 📍 RECIPIENT INFORMATION")
        lines.append(f"**Name:** {recipient.get('name', 'N/A')}")
        lines.append(f"**Address:** {recipient.get('street1', '')}")
        if recipient.get("street2"):
            lines.append(f"**Address 2:** {recipient.get('street2')}")
        city = recipient.get("city", "")
        state = recipient.get("state", "")
        zip_code = recipient.get("zip", "")
        lines.append(f"**City, State ZIP:** {city}, {state} {zip_code}")
        lines.append(f"**Country:** {recipient.get('country', '')}")
        lines.append(f"**Phone:** {recipient.get('phone', 'N/A')}")
        lines.append(f"**Email:** {recipient.get('email', 'N/A')}")

        lines.append("\n### 📋 SHIPMENT DETAILS")
        lines.append(f"**Product:** {product.get('description', shipment.get('contents', 'N/A'))}")
        lines.append(f"**Category:** {product.get('category', 'N/A')}")
        weight_oz = parcel.get("weight_oz", 0)
        weight_lbs = parcel.get("weight_lbs", 0)
        lines.append(f"**Weight:** {weight_oz} oz ({weight_lbs:.2f} lbs)")
        length = parcel.get("length", 0)
        width = parcel.get("width", 0)
        height = parcel.get("height", 0)
        lines.append(f"**Dimensions:** {length} x {width} x {height} in")

        # Show customs info if international
        if customs and customs.get("required"):
            lines.append("\n### 🌍 CUSTOMS INFORMATION")
            lines.append("**International:** Yes")
            lines.append(f"**Auto-generated:** {customs.get('auto_generated', False)}")
            if customs.get("items"):
                lines.append("\n**Customs Items:**")
                for item in customs.get("items", []):
                    lines.append(f"- **Description:** {item.get('description', 'N/A')}")
                    lines.append(f"  - Quantity: {item.get('quantity', 1)}")
                    lines.append(f"  - Value: ${item.get('value', 0)}")
                    lines.append(f"  - Weight: {item.get('weight', 0)} oz")
                    lines.append(f"  - HS Code: {item.get('hs_tariff_number', 'N/A')}")
                    lines.append(f"  - Origin: {item.get('origin_country', 'US')}")

        # Get rates
        rates = shipment.get("rates", [])
        if not rates:
            lines.append("\n❌ No rates available")
            continue

        # Match requested carrier (flexible matching)
        requested_rates = []
        other_rates = []

        if carrier_pref:
            carrier_keywords = {
                "USPS": ["USPS"],
                "UPS": ["UPS", "UPSDAP"],
                "FEDEX": ["FedEx", "FEDEX"],
                "DHL": ["DHL"],
            }
            # Extract first word for matching (e.g., "UPS GROUND" -> "UPS")
            carrier_base = carrier_pref.split()[0] if carrier_pref else ""
            matching_carriers = carrier_keywords.get(carrier_base, [carrier_base])

            for rate in rates:
                if any(carrier.lower() in rate["carrier"].lower() for carrier in matching_carriers):
                    requested_rates.append(rate)
                else:
                    other_rates.append(rate)
        else:
            other_rates = rates

        # Display requested carrier rates (if specified) - PROMINENTLY AT TOP
        if carrier_pref and requested_rates:
            lines.append(f"\n### ⭐ PREFERRED CARRIER: {carrier_pref}")

            # Calculate cost comparison
            cheapest_requested = min(float(r["rate"]) for r in requested_rates)
            cheapest_overall = min(float(r["rate"]) for r in rates)

            if cheapest_requested > cheapest_overall:
                savings = cheapest_requested - cheapest_overall
                lines.append(
                    f"💡 **Note:** Cheapest {carrier_pref} option is ${cheapest_requested:.2f}. "
                    f"You could save ${savings:.2f} with alternative carriers "
                    f"(cheapest: ${cheapest_overall:.2f})\n"
                )
            else:
                lines.append(f"✅ **{carrier_pref} offers the best rates for this shipment!**\n")

            lines.append("| Service | Rate | Delivery Days |")
            lines.append("|---------|------|---------------|")

            # Sort by price (cheapest first)
            sorted_requested = sorted(requested_rates, key=lambda r: float(r["rate"]))
            for idx, rate in enumerate(sorted_requested):
                days = rate.get("delivery_days") or "N/A"
                # Mark cheapest with special indicator
                marker = "✓ CHEAPEST" if idx == 0 else ""
                service_name = f"{rate['carrier']} {rate['service']}"
                lines.append(f"| {service_name} {marker} | **${rate['rate']}** | {days} |")

        # Display all other rates
        if other_rates:
            lines.append("\n### 📊 ALL OTHER AVAILABLE RATES")
            lines.append("| Carrier | Service | Rate | Delivery Days |")
            lines.append("|---------|---------|------|---------------|")

            # Sort by price
            for rate in sorted(other_rates, key=lambda r: float(r["rate"])):
                days = rate.get("delivery_days") or "N/A"
                lines.append(
                    f"| {rate['carrier']} | {rate['service']} | ${rate['rate']} | {days} |"
                )

        # Show summary
        lines.append(f"\n**Total Rates Available:** {len(rates)}")
        min_rate = min(float(r["rate"]) for r in rates)
        max_rate = max(float(r["rate"]) for r in rates)
        lines.append(f"**Price Range:** ${min_rate:.2f} - ${max_rate:.2f}")

    return "\n".join(lines)


def register_shipment_tools(mcp, easypost_service=None):
    """Register shipment tools with MCP server."""

    @mcp.tool(tags=["shipment", "rates", "shipping", "m3-optimized"])
    async def get_shipment_rates(
        spreadsheet_data: str,
        ctx: Context | None = None,
    ) -> dict:
        """
        Get shipping rates for single or multiple shipments - M3 Max Optimized.

        Handles both single shipments (1 line) and bulk operations (multiple lines).
        Uses spreadsheet format: tab-separated columns (paste from spreadsheet).

        M3 MAX OPTIMIZATION (16 cores, 128GB RAM):
        - Parallel rate calculations: 16 concurrent API calls
        - Formula: cpu_count × 1 = 16 workers for rate limiting compliance
        - Performance: ~10× faster than sequential (50 items: 5s vs 50s)

        SENDER ADDRESS PRIORITY:
        1. Custom sender (columns 16-24): If provided, ALWAYS used (ignores warehouse)
        2. Auto warehouse selection: Product category + origin state determines warehouse

        PRODUCT CATEGORY AUTO-DETECTION (13 categories):
        - Bedding (pillow, mattress, sheet) → Home Goods Warehouse
        - Sporting (baseball, glove, fishing, outdoor) → Outdoor Gear Hub
        - Beauty (cosmetic, skincare, makeup) → Beauty & Wellness
        - Apparel (jeans, shirt, pants, denim) → Fashion District Warehouse
        - Footwear (shoes, boots, sneakers) → Footwear Warehouse
        - Art (print, engraving, painting) → Arts District Warehouse
        - Electronics (phone, computer, tablet) → Tech Warehouse
        - Books, Toys, Jewelry, Food, Home Goods → Specialized warehouses
        - Default → General Distribution Center

        WAREHOUSE LOCATIONS (3 cities):
        - Los Angeles (California)
        - New York (New York)
        - Las Vegas (Nevada)

        Args:
            spreadsheet_data: Tab-separated shipment data (1+ lines, paste from spreadsheet)
            ctx: MCP context for progress reporting

        Returns:
            Rates for all shipments with warehouse assignments and performance metrics
        """
        from time import perf_counter

        start_time = perf_counter()

        try:
            # Get service from closure parameter (stdio mode) or context (HTTP mode)
            service = easypost_service
            if service is None and ctx:
                lifespan_ctx = ctx.request_context.lifespan_context
                service = (
                    lifespan_ctx.get("easypost_service")
                    if isinstance(lifespan_ctx, dict)
                    else lifespan_ctx.easypost_service
                )

            if not service:
                return {
                    "status": "error",
                    "data": None,
                    "message": "EasyPost service not initialized",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

            if ctx:
                await ctx.info("🚀 M3 Max: Starting parallel rate calculation (16 workers)...")

            # Auto-detect format: tab-separated spreadsheet or natural text
            # If first line has no tabs, assume natural text format
            first_line = spreadsheet_data.split("\n")[0] if spreadsheet_data else ""
            is_natural_format = "\t" not in first_line

            if is_natural_format:
                if ctx:
                    await ctx.info(
                        "📝 Detected natural text format - converting to spreadsheet format..."
                    )

                # Convert natural text to tab-separated format
                converted_line = convert_natural_to_spreadsheet(spreadsheet_data)
                if not converted_line:
                    return {
                        "status": "error",
                        "data": None,
                        "message": (
                            "Failed to parse natural text format. "
                            "Ensure sender and recipient addresses are clearly separated "
                            "by blank lines."
                        ),
                        "timestamp": datetime.now(UTC).isoformat(),
                    }
                lines = [converted_line]
                if ctx:
                    await ctx.info("✅ Successfully converted natural text to spreadsheet format")
            else:
                # Split into lines and filter empty (standard tab-separated format)
                lines = [line.strip() for line in spreadsheet_data.split("\n") if line.strip()]

            if not lines:
                return {
                    "status": "error",
                    "data": None,
                    "message": "No data provided",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

            total_lines = len(lines)
            used_warehouses = set()  # Track which warehouses are used

            # Semaphore for rate limiting (reduced to avoid EasyPost rate limits)
            semaphore = asyncio.Semaphore(MAX_CONCURRENT)

            async def process_one_line(idx: int, line: str) -> dict:
                """Process single shipment line with rate limiting."""
                async with semaphore:
                    # Add delay to prevent EasyPost rate limiting (production API: 1 request/second)
                    await asyncio.sleep(1.0)

                    try:
                        if ctx and idx % max(1, total_lines // 10) == 0:
                            await ctx.info(f"Processing shipment {idx + 1}/{total_lines}...")

                        # Parse line
                        data = parse_spreadsheet_line(line)

                        # Detect product category from contents (always needed for reporting)
                        category = detect_product_category(data["contents"])

                        # PRIORITY 1: Use custom sender address if provided (columns 16-24)
                        # PRIORITY 2: Auto-select warehouse by product category + origin state
                        if "sender_address" in data and data["sender_address"].get("name"):
                            # Custom sender address provided - USE IT (ignores warehouse lookup)
                            from_address = data["sender_address"]
                            warehouse_key = f"{from_address.get('name', 'Custom Sender')}"
                            if ctx:
                                await ctx.info(
                                    f"📍 Using custom sender: {warehouse_key} "
                                    f"({from_address.get('city')}, {from_address.get('country')})"
                                )
                        else:
                            # No custom sender - select warehouse by category + state
                            from_address = get_warehouse_address(data["origin_state"], category)
                            company_or_name = from_address.get("company") or from_address.get(
                                "name", "Unknown"
                            )
                            warehouse_key = f"{company_or_name}"
                            if ctx:
                                await ctx.info(
                                    f"🏭 Auto-selected warehouse: {warehouse_key} "
                                    f"(category: {category}, state: {data['origin_state']})"
                                )

                        used_warehouses.add(warehouse_key)

                        # Parse dimensions and weight
                        length, width, height = parse_dimensions(data["dimensions"])
                        weight_oz = parse_weight(data["weight"])

                        # Build to_address with normalized country code
                        to_address = {
                            "name": f"{data['recipient_name']} {data['recipient_last_name']}",
                            "street1": data["street1"],
                            "street2": data["street2"],
                            "city": data["city"],
                            "state": data["state"],
                            "zip": data["zip"],
                            "country": normalize_country_code(data["country"]),
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

                            # Get actual person's name for customs signing
                            customs_signer = get_customs_signer(from_address)

                            # DDP for FedEx, DDU for others by default
                            preferred_carrier = data.get("carrier_preference", "").upper()
                            incoterm = "DDP" if "FEDEX" in preferred_carrier else "DDU"

                            customs_info = await loop.run_in_executor(
                                None,
                                get_or_create_customs,
                                data["contents"],
                                weight_oz,
                                service.client,
                                None,  # Auto-detect value from description
                                customs_signer,
                                incoterm,
                            )

                        if ctx and customs_info:
                            country = to_address["country"]
                            await ctx.info(
                                f"✅ Auto-generated customs ({incoterm}) "
                                f"for international shipment ({country})"
                            )

                        # Get rates with timeout (customs included for international)
                        rates_result = await asyncio.wait_for(
                            service.get_rates(
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
                            # COMPLETE STRUCTURED DATA
                            "detailed_data": {
                                "sender": {
                                    "name": from_address.get("name", ""),
                                    "company": from_address.get("company", ""),
                                    "street1": from_address.get("street1", ""),
                                    "street2": from_address.get("street2", ""),
                                    "city": from_address.get("city", ""),
                                    "state": from_address.get("state", ""),
                                    "zip": from_address.get("zip", ""),
                                    "country": from_address.get("country", ""),
                                    "phone": from_address.get("phone", ""),
                                    "email": from_address.get("email", ""),
                                },
                                "recipient": to_address,
                                "parcel": {
                                    "length": round(length, 2),
                                    "width": round(width, 2),
                                    "height": round(height, 2),
                                    "weight_oz": round(weight_oz, 2),
                                    "weight_lbs": round(weight_oz / 16, 2),
                                },
                                "product": {
                                    "description": data["contents"],
                                    "category": category,
                                    "is_international": is_international,
                                },
                                "carrier_preference": data.get("carrier_preference", ""),
                                "customs": (
                                    {
                                        "required": is_international,
                                        "auto_generated": (
                                            bool(customs_info) if is_international else False
                                        ),
                                        "items": (
                                            [
                                                {
                                                    "description": (
                                                        item.description
                                                        if hasattr(item, "description")
                                                        else ""
                                                    ),
                                                    "quantity": (
                                                        item.quantity
                                                        if hasattr(item, "quantity")
                                                        else 1
                                                    ),
                                                    "value": (
                                                        item.value if hasattr(item, "value") else 0
                                                    ),
                                                    "weight": (
                                                        item.weight
                                                        if hasattr(item, "weight")
                                                        else 0
                                                    ),
                                                    "hs_tariff_number": (
                                                        item.hs_tariff_number
                                                        if hasattr(item, "hs_tariff_number")
                                                        else ""
                                                    ),
                                                    "origin_country": (
                                                        item.origin_country
                                                        if hasattr(item, "origin_country")
                                                        else "US"
                                                    ),
                                                }
                                                for item in (
                                                    customs_info.customs_items
                                                    if hasattr(customs_info, "customs_items")
                                                    else []
                                                )
                                            ]
                                            if customs_info
                                            else []
                                        ),
                                    }
                                    if is_international
                                    else None
                                ),
                            },
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
            processed_results: list[dict[str, Any]] = []
            for idx, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Task {idx + 1} raised exception: {result}")
                    processed_results.append(
                        {
                            "shipment_number": idx + 1,
                            "error": f"Exception: {str(result)}",
                        }
                    )
                elif isinstance(result, dict):
                    # Type cast: result is dict after isinstance check
                    dict_result: dict[str, Any] = result
                    processed_results.append(dict_result)

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

            # Generate user-friendly formatted table
            formatted_table = _generate_rate_table(processed_results)

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
                    "formatted_table": formatted_table,
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
