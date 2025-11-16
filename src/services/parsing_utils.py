"""Parsing helpers: dimensions, weight, country codes."""

from __future__ import annotations

import re
import logging

logger = logging.getLogger(__name__)

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
    "THE NETHERLANDS": "NL",
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
    "UNITED STATES OF AMERICA": "US",
    "US": "US",
}


def normalize_country_code(country: str) -> str:
    if not country:
        return "US"
    country_upper = country.strip().upper()
    if len(country_upper) == 2:
        return country_upper
    if country_upper in COUNTRY_CODE_MAP:
        return COUNTRY_CODE_MAP[country_upper]
    for country_name, code in COUNTRY_CODE_MAP.items():
        if country_name in country_upper:
            return code
    logger.warning(f"normalize_country_code: no match for '{country_upper}'")
    return country_upper


def parse_dimensions(dim_str: str) -> tuple[float, float, float]:
    if not dim_str or not dim_str.strip():
        raise ValueError("Dimension string is empty")
    normalized = dim_str.lower()
    for separator in ["×", "*", "by", "x"]:
        normalized = normalized.replace(separator, " ")
    parts = normalized.split()
    numbers: list[float] = []
    i = 0
    while i < len(parts):
        part = parts[i].strip()
        if "/" in part:
            try:
                num, denom = part.split("/")
                numbers.append(float(num) / float(denom))
                i += 1
                continue
            except (ValueError, ZeroDivisionError):
                i += 1
                continue
        if re.match(r"^\d*\.?\d+$", part):
            try:
                whole_num = float(part)
                if i + 1 < len(parts) and "/" in parts[i + 1]:
                    try:
                        frac_num, frac_denom = parts[i + 1].split("/")
                        fraction = float(frac_num) / float(frac_denom)
                        numbers.append(whole_num + fraction)
                        i += 2
                        continue
                    except (ValueError, ZeroDivisionError):
                        pass
                numbers.append(whole_num)
            except ValueError:
                pass
        i += 1
    if len(numbers) >= 3:
        if all(0.1 <= dim <= 999 for dim in numbers[:3]):
            return (numbers[0], numbers[1], numbers[2])
        raise ValueError(f"Dimensions out of range (0.1-999 inches): {numbers[:3]}")
    if len(numbers) > 0:
        raise ValueError(
            f"Insufficient dimensions: found {len(numbers)}, need 3 (L x W x H). "
            "Example: '12.5 x 10 x 3' or '11 1/2 x 9 x 2 1/4'"
        )
    raise ValueError(
        f"Could not parse dimensions from '{dim_str}'. "
        "Please use format: '12.5 x 10 x 3' or '11 1/2 x 9 x 2 1/4' (length x width x height)"
    )


def parse_weight(weight_str: str) -> float:
    if not weight_str or not weight_str.strip():
        raise ValueError("Weight string is empty")
    weight_str = weight_str.strip()
    total_oz = 0.0
    pattern = r"([\d.]+)\s*(lbs?|oz|ounces?|pounds?|LB|OZ|kg|kilograms?|g|grams?)"
    matches = list(re.finditer(pattern, weight_str.lower()))
    if matches:
        for match in matches:
            value = float(match.group(1))
            unit = match.group(2).lower()
            if "lb" in unit or "pound" in unit:
                total_oz += value * 16.0
            elif "kg" in unit or "kilogram" in unit:
                total_oz += value * 35.274
            elif "g" in unit or "gram" in unit:
                total_oz += value / 28.35
            else:
                total_oz += value
        if total_oz > 0:
            return total_oz
    else:
        numbers = re.findall(r"[\d.]+", weight_str)
        if numbers:
            value = float(numbers[0])
            if value > 100:
                total_oz = value
            elif value > 16:
                total_oz = value if "." in weight_str else value * 16.0
            elif value > 1:
                total_oz = value * 16.0
            else:
                total_oz = value * 16.0
            if total_oz > 0:
                return total_oz
    raise ValueError(
        f"Could not parse weight from '{weight_str}'. "
        "Please specify units (e.g., '5.26 lbs', '84 oz', '2.5 kg')"
    )
