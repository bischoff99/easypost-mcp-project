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

    # Email detection
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
        return "email"

    # Phone detection (various formats)
    phone_patterns = [
        r"^\+?[\d\s\-\(\)]{10,}$",  # International format
        r"^\d{10,}$",  # Simple digits
        r"^\d{3}[\s\-]?\d{3}[\s\-]?\d{4}$",  # US format
    ]
    for pattern in phone_patterns:
        cleaned_value = value.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if re.match(pattern, cleaned_value):
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

    # Postal/ZIP code detection
    if re.match(r"^\d{5,}(?:-\d{4})?$", value) or re.match(r"^[A-Z0-9\s]{3,10}$", value.upper()):
        return "postal_code"

    # State code detection (US states)
    us_states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
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
    has_dimension_keywords = "x" in value_lower or "×" in value or any(
        keyword in value_lower for keyword in ["inch", "in", "cm", "dimension"]
    )
    if has_dimension_keywords and re.search(r"[\d.]+[\sx×]+[\d.]+[\sx×]+[\d.]+", value):
        return "dimensions"

    # Name detection (contains common name patterns)
    # Multiple words, capitalized, not all caps (unless short)
    words = value.split()
    has_capitalized_words = len(words) >= 2 and any(
        word[0].isupper() if word else False for word in words
    )
    is_not_address = not any(
        keyword in value_lower
        for keyword in ["street", "st", "avenue", "ave", "road", "rd", "suite", "apt"]
    )
    if has_capitalized_words and is_not_address:
        return "name"

    # Street address detection
    street_keywords = [
        "street", "st", "avenue", "ave", "road", "rd",
        "boulevard", "blvd", "drive", "dr", "lane", "ln",
    ]
    if any(keyword in value_lower for keyword in street_keywords):
        return "street"
    # Also detect addresses with numbers (e.g., "123 Main St", "720 East St Suite 2")
    if re.match(r"^\d+", value) and len(words) >= 1:
        return "street"

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

    # Try standard positional parsing first (backward compatibility)
    if len(parts) >= 16:
        try:
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
                "contents": parts[15] if len(parts) > 15 else "",
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
                result["recipient_name"]
                and result["street1"]
                and result["country"]
            )
            weight_valid = True
            if result["weight"]:
                try:
                    parse_weight(result["weight"])
                except ValueError as e:
                    weight_valid = False
                    logger.warning(
                        f"Standard format weight validation failed: {e}, "
                        "trying field detection"
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
    lines = [
        line.strip()
        for line in text.strip().split("\n")
        if line.strip()
    ]

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
        section_lines = [
            line.strip()
            for line in section.split("\n")
            if line.strip()
        ]

        for line in section_lines:
            # Extract email
            email_match = re.search(
                r"(?:email[:\s]+)?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
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

            # Extract dimensions (flexible: "Dimensions 12x12x2" or "12x12x2")
            if result["dimensions"] is None:
                dim_match = re.search(
                    r"(?:dimensions?[:\s]+)?(\d+)\s*x\s*(\d+)\s*x\s*(\d+)",
                    line,
                    re.IGNORECASE,
                )
                if dim_match:
                    result["dimensions"] = (
                        f"{dim_match.group(1)} x {dim_match.group(2)} x {dim_match.group(3)}"
                    )

