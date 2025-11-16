from __future__ import annotations

from typing import Any

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
    """Convert country name to ISO 2-letter code for EasyPost API."""
    if not country:
        return "US"
    country_upper = country.strip().upper()
    if len(country_upper) == 2:
        return country_upper
    return COUNTRY_CODE_MAP.get(country_upper, country_upper)


def normalize_address(address: dict[str, Any]) -> dict[str, Any]:
    """Normalize address fields and country codes."""
    if not address:
        return address
    normalized = address.copy()
    if "country" in normalized:
        normalized["country"] = normalize_country_code(normalized["country"])
    for key, value in normalized.items():
        if isinstance(value, str):
            normalized[key] = value.strip()
        elif value is None:
            pass
    return normalized


def preprocess_address_for_fedex(address: dict[str, Any]) -> dict[str, Any]:
    """Reformat address to meet FedEx/UPS international API requirements."""
    result = address.copy()
    street1 = result.get("street1", "").strip()
    street2 = result.get("street2", "").strip()
    country = result.get("country", "").upper()

    if country and country != "US" and "state" in result:
        del result["state"]

    if street2:
        if len(street2.split()) <= 3 and len(street1) + len(street2) + 2 <= 35:
            result["street1"] = f"{street1}, {street2}"
            result["street2"] = ""
        elif len(street2.split()) <= 3:
            result["street2"] = ""
        else:
            result["street1"] = street1[:35]
            result["street2"] = street2[:35]

    return result
