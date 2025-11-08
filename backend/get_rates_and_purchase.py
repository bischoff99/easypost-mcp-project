#!/usr/bin/env python3
"""Get rates and purchase shipments via API with data transformation."""

import re
import requests
import json
from typing import Any

BASE_URL = "http://localhost:8000"


def parse_weight(weight_str: str) -> float:
    """Convert weight string to ounces."""
    weight_str = weight_str.strip().lower()

    # Handle "lb" or "lbs"
    if "lb" in weight_str:
        parts = re.split(r"lb", weight_str)
        lbs = float(re.sub(r"[^\d.]", "", parts[0]) or 0)
        oz = 0
        if len(parts) > 1 and parts[1].strip():
            oz_str = re.sub(r"[^\d.]", "", parts[1])
            if oz_str:
                oz = float(oz_str)
        return (lbs * 16) + oz

    # Handle "oz"
    if "oz" in weight_str:
        oz_str = re.sub(r"[^\d.]", "", weight_str)
        return float(oz_str) if oz_str else 0

    # Try to parse as number (assume ounces)
    try:
        return float(re.sub(r"[^\d.]", "", weight_str))
    except ValueError:
        return 0


def parse_dimensions(dim_str: str) -> dict[str, float]:
    """Parse dimensions string like '13x13x7' to dict."""
    parts = dim_str.lower().replace("x", " ").split()
    if len(parts) >= 3:
        return {
            "length": float(parts[0]),
            "width": float(parts[1]),
            "height": float(parts[2]),
        }
    return {"length": 0, "width": 0, "height": 0}


def extract_customs_info(contents: str) -> dict[str, Any]:
    """Extract customs info from contents string."""
    # Try to extract quantity and price
    quantity = 1
    price = 50.0  # Default

    qty_match = re.search(r"quantity[:\s]+(\d+)", contents, re.IGNORECASE)
    if qty_match:
        quantity = int(qty_match.group(1))

    price_match = re.search(r"price[:\s]+\$?(\d+\.?\d*)", contents, re.IGNORECASE)
    if price_match:
        price = float(price_match.group(1))

    # Extract item description (first part before Quantity/Price)
    item_desc = contents.split("Quantity")[0].split("Price")[0].strip()
    if not item_desc:
        item_desc = contents.split(":")[-1].strip() if ":" in contents else contents

    return {
        "description": item_desc[:50],  # Max 50 chars
        "quantity": quantity,
        "value": price,
        "hs_tariff_number": None,  # Optional
        "origin_country": "US",
    }


def normalize_country_code(country: str) -> str:
    """Convert country name to ISO 2-letter code."""
    country_map = {
        "belgium": "BE",
        "united states": "US",
        "usa": "US",
        "us": "US",
    }
    normalized = country.strip().lower()
    return country_map.get(normalized, country[:2].upper() if len(country) >= 2 else country.upper())


def create_shipment_data(
    origin_state: str,
    recipient_name: str,
    recipient_phone: str,
    recipient_email: str,
    recipient_street: str,
    recipient_city: str,
    recipient_state: str,
    recipient_zip: str,
    recipient_country: str,
    dimensions: str,
    weight: str,
    contents: str,
    sender_name: str,
    sender_street: str,
    sender_city: str,
    sender_state: str,
    sender_zip: str,
    sender_country: str = "US",
    sender_phone: str = "",
    sender_email: str = "",
) -> dict[str, Any]:
    """Create shipment data with all transformations."""
    dims = parse_dimensions(dimensions)
    weight_oz = parse_weight(weight)

    to_address = {
        "name": recipient_name,
        "street1": recipient_street,
        "city": recipient_city,
        "state": recipient_state or "",  # Empty string for international if no state
        "zip": recipient_zip,
        "country": normalize_country_code(recipient_country),
    }
    if recipient_phone:
        to_address["phone"] = recipient_phone
    if recipient_email:
        to_address["email"] = recipient_email

    from_address = {
        "name": sender_name,
        "street1": sender_street,
        "city": sender_city,
        "state": sender_state,
        "zip": sender_zip,
        "country": normalize_country_code(sender_country),
    }
    if sender_phone:
        from_address["phone"] = sender_phone
    if sender_email:
        from_address["email"] = sender_email

    parcel = {
        "length": dims["length"],
        "width": dims["width"],
        "height": dims["height"],
        "weight": weight_oz,
    }

def create_shipment_data(
    origin_state: str,
    recipient_name: str,
    recipient_phone: str,
    recipient_email: str,
    recipient_street: str,
    recipient_city: str,
    recipient_state: str,
    recipient_zip: str,
    recipient_country: str,
    dimensions: str,
    weight: str,
    contents: str,
    sender_name: str,
    sender_street: str,
    sender_city: str,
    sender_state: str,
    sender_zip: str,
    sender_country: str = "US",
    sender_phone: str = "",
    sender_email: str = "",
) -> dict[str, Any]:
    """Create shipment data with all transformations."""
    dims = parse_dimensions(dimensions)
    weight_oz = parse_weight(weight)

    to_address = {
        "name": recipient_name,
        "street1": recipient_street,
        "city": recipient_city,
        "state": recipient_state or "",  # Empty string for international if no state
        "zip": recipient_zip,
        "country": normalize_country_code(recipient_country),
    }
    if recipient_phone:
        to_address["phone"] = recipient_phone
    if recipient_email:
        to_address["email"] = recipient_email

    from_address = {
        "name": sender_name,
        "street1": sender_street,
        "city": sender_city,
        "state": sender_state,
        "zip": sender_zip,
        "country": normalize_country_code(sender_country),
    }
    if sender_phone:
        from_address["phone"] = sender_phone
    if sender_email:
        from_address["email"] = sender_email

    parcel = {
        "length": dims["length"],
        "width": dims["width"],
        "height": dims["height"],
        "weight": weight_oz,
    }

    shipment = {
        "to_address": to_address,
        "from_address": from_address,
        "parcel": parcel,
        "carrier": "USPS",  # Will get all rates
    }

    # Add customs info for international shipments
    if normalize_country_code(recipient_country) != "US":
        customs_item = extract_customs_info(contents)
        shipment["customs_info"] = {
            "contents": [customs_item],
            "customs_certify": True,
            "customs_signer": from_address.get("name", "Sender"),
            "contents_type": "merchandise",
            "restriction_type": "none",
            "restriction_comments": "",
            "eel_pfc": "NOEEI 30.37(a)",
        }

    return shipment


def get_rates_for_shipment(shipment: dict[str, Any]) -> dict[str, Any]:
    """Get rates for a single shipment."""
    rates_payload = {
        "to_address": shipment["to_address"],
        "from_address": shipment["from_address"],
        "parcel": shipment["parcel"],
    }

    response = requests.post(f"{BASE_URL}/rates", json=rates_payload)
    response.raise_for_status()
    return response.json()


def create_shipment(shipment: dict[str, Any]) -> dict[str, Any]:
    """Create shipment (without purchasing) using bulk endpoint."""
    # Use bulk endpoint which sets buy_label=False
    bulk_payload = {
        "shipments": [{
            "to_address": shipment["to_address"],
            "from_address": shipment["from_address"],
            "parcel": shipment["parcel"],
            "carrier": shipment.get("carrier", "USPS"),
            "customs_info": shipment.get("customs_info"),  # Include customs_info
        }]
    }

    response = requests.post(f"{BASE_URL}/bulk-shipments", json=bulk_payload)
    if response.status_code != 200:
        error_detail = response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
        raise Exception(f"{response.status_code} Error: {error_detail}")

    result = response.json()
    if result.get("status") != "success":
        raise Exception(f"Bulk creation failed: {result.get('message')}")

    # Extract first shipment result
    results = result.get("data", {}).get("results", [])
    if not results:
        raise Exception("No shipment created")

    shipment_result = results[0].get("result", {})
    if shipment_result.get("status") != "success":
        raise Exception(f"Shipment creation failed: {shipment_result.get('message')}")

    return shipment_result


def buy_shipment(shipment_id: str, rate_id: str) -> dict[str, Any]:
    """Purchase existing shipment with selected rate."""
    response = requests.post(
        f"{BASE_URL}/shipments/{shipment_id}/buy?rate_id={rate_id}"
    )
    if response.status_code != 200:
        error_detail = response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
        raise Exception(f"{response.status_code} Error: {error_detail}")
    return response.json()


def find_fedex_economy_ddp_rate(rates: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Find FedEx Economy DDP rate."""
    for rate in rates:
        carrier = rate.get("carrier", "").upper()
        service = rate.get("service", "").upper()

        if "FEDEX" in carrier and "ECONOMY" in service and "DDP" in service:
            return rate
        # Also check for FedEx International Economy
        if "FEDEX" in carrier and "ECONOMY" in service:
            return rate

    return None


def main():
    """Main execution."""
    print("=" * 60)
    print("Getting Rates and Purchasing Shipments via API")
    print("=" * 60)

    # Shipment 1: Marie Lenaerts
    print("\n[1] Processing Shipment 1: Marie Lenaerts")
    shipment1 = create_shipment_data(
        origin_state="NY",
        recipient_name="Marie Lenaerts",
        recipient_phone="+32488003329",
        recipient_email="marsiekke1@outlook.com",
        recipient_street="Recollettenstraat 39",
        recipient_city="Nieuwpoort",
        recipient_state="",
        recipient_zip="8620",
        recipient_country="Belgium",
        dimensions="13x13x7",
        weight="4.5 lbs",
        contents="Women's cotton Sweater Quantity: 2 Total Price: $34",
        sender_name="Anderson Foy",
        sender_street="1542 Pitkin Ave",
        sender_city="Brooklyn",
        sender_state="NY",
        sender_zip="11212",
    )

    # Shipment 2: Thibo Van Dyck
    print("[2] Processing Shipment 2: Thibo Van Dyck")
    shipment2 = create_shipment_data(
        origin_state="NY",
        recipient_name="Thibo Van Dyck",
        recipient_phone="+32478933888",
        recipient_email="oceanIn.5@outlook.com",
        recipient_street="Parijsstraat 12",
        recipient_city="Middelkerke",
        recipient_state="",
        recipient_zip="8430",
        recipient_country="Belgium",
        dimensions="13x13x13",
        weight="6lb 5oz",
        contents="Custom Soccer Cleats Quantity: 2 Price: $55",
        sender_name="Xavier Parker",
        sender_street="246 E 116th St",
        sender_city="New York",
        sender_state="NY",
        sender_zip="10029",
        sender_phone="6466006012",
        sender_email="Xavier@euromex.com",
    )

    shipments = [shipment1, shipment2]
    results = []

    # Step 1: Create shipments to get rates
    print("\n" + "=" * 60)
    print("STEP 1: Creating shipments to get rates")
    print("=" * 60)

    for idx, shipment in enumerate(shipments, 1):
        print(f"\n--- Shipment {idx} ---")
        print(f"To: {shipment['to_address']['name']}, {shipment['to_address']['city']}, {shipment['to_address']['country']}")
        print(f"From: {shipment['from_address']['name']}, {shipment['from_address']['city']}, {shipment['from_address']['state']}")
        print(f"Weight: {shipment['parcel']['weight']} oz")
        print(f"Dimensions: {shipment['parcel']['length']}x{shipment['parcel']['width']}x{shipment['parcel']['height']}")

        try:
            # Create shipment
            create_result = create_shipment(shipment)

            if create_result.get("status") != "success":
                print(f"ERROR: {create_result.get('message')}")
                results.append({"shipment": idx, "status": "error", "error": create_result.get("message")})
                continue

            # Extract shipment data from result
            shipment_data = create_result.get("data", {})
            shipment_id = shipment_data.get("id") or create_result.get("id")
            rates = shipment_data.get("rates", []) or create_result.get("rates", [])

            if not shipment_id:
                raise Exception("No shipment ID returned")

            print(f"✓ Shipment created: {shipment_id}")
            print(f"✓ Found {len(rates)} rates")

            # Find FedEx Economy DDP
            fedex_rate = find_fedex_economy_ddp_rate(rates)

            if not fedex_rate:
                print("⚠ No FedEx Economy DDP rate found. Available carriers:")
                carriers = set(r.get("carrier", "Unknown") for r in rates)
                print(f"  {', '.join(carriers)}")
                # Show sample rates
                print("\nSample rates:")
                for r in rates[:3]:
                    print(f"  {r.get('carrier')} {r.get('service')}: ${r.get('rate')} (ID: {r.get('id')})")
                results.append({
                    "shipment": idx,
                    "status": "no_rate",
                    "shipment_id": shipment_id,
                    "rates": rates[:5],  # Top 5
                })
                continue

            print(f"✓ Found FedEx Economy DDP rate: ${fedex_rate.get('rate')} (ID: {fedex_rate.get('id')})")

            # Step 2: Purchase
            print(f"\nPurchasing shipment {idx}...")
            buy_result = buy_shipment(shipment_id, fedex_rate.get("id"))

            if buy_result.get("status") == "success":
                print(f"✓ PURCHASED: Tracking {buy_result.get('tracking_code')}")
                print(f"  Label URL: {buy_result.get('postage_label_url')}")
                print(f"  Cost: ${buy_result.get('rate')}")

                results.append({
                    "shipment": idx,
                    "status": "purchased",
                    "shipment_id": shipment_id,
                    "tracking_code": buy_result.get("tracking_code"),
                    "label_url": buy_result.get("postage_label_url"),
                    "cost": buy_result.get("rate"),
                    "carrier": buy_result.get("carrier"),
                    "service": buy_result.get("service"),
                })
            else:
                print(f"✗ Purchase failed: {buy_result.get('message')}")
                results.append({
                    "shipment": idx,
                    "status": "purchase_failed",
                    "error": buy_result.get("message"),
                })

        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            results.append({"shipment": idx, "status": "error", "error": str(e)})

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(json.dumps(results, indent=2))

    purchased = sum(1 for r in results if r.get("status") == "purchased")
    print(f"\n✓ Purchased: {purchased}/{len(shipments)} shipments")


if __name__ == "__main__":
    main()
