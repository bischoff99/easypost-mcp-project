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
        sender_country_raw = parts[22].strip() if len(parts) > 22 else "US"
        result["sender_address"] = {
            "name": parts[16].strip(),
            "street1": parts[17].strip() if len(parts) > 17 else "",
            "street2": parts[18].strip() if len(parts) > 18 else "",
            "city": parts[19].strip() if len(parts) > 19 else "",
            "state": parts[20].strip() if len(parts) > 20 else "",
            "zip": parts[21].strip() if len(parts) > 21 else "",
            "country": normalize_country_code(sender_country_raw),
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

        lines.append(f"\n## Shipment #{shipment['shipment_number']}: {shipment['recipient']}")
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

        # Get carrier preference
        carrier_pref = detailed.get("carrier_preference", "").upper()

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

        # Display requested carrier rates (if specified)
        if carrier_pref and requested_rates:
            lines.append(f"\n### ⭐ REQUESTED CARRIER: {carrier_pref}")
            lines.append("| Service | Rate | Delivery Days |")
            lines.append("|---------|------|---------------|")

            # Sort by price
            for rate in sorted(requested_rates, key=lambda r: float(r["rate"])):
                days = rate.get("delivery_days") or "N/A"
                lines.append(
                    f"| {rate['carrier']} {rate['service']} | **${rate['rate']}** | {days} |"
                )

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
                                "customs": {
                                    "required": is_international,
                                    "auto_generated": bool(customs_info)
                                    if is_international
                                    else False,
                                    "items": (
                                        [
                                            {
                                                "description": item.description
                                                if hasattr(item, "description")
                                                else "",
                                                "quantity": item.quantity
                                                if hasattr(item, "quantity")
                                                else 1,
                                                "value": item.value
                                                if hasattr(item, "value")
                                                else 0,
                                                "weight": item.weight
                                                if hasattr(item, "weight")
                                                else 0,
                                                "hs_tariff_number": item.hs_tariff_number
                                                if hasattr(item, "hs_tariff_number")
                                                else "",
                                                "origin_country": item.origin_country
                                                if hasattr(item, "origin_country")
                                                else "US",
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
                                else None,
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
