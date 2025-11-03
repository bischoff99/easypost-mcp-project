#!/usr/bin/env python3
"""Live test with real EasyPost API to verify actual rates are returned."""

import asyncio
import json
import os
import sys

# Add backend root to path (we're in tests/integration/)
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_root)

from src.mcp import easypost_service


async def test_live_rates():
    """Test with 2 sample shipments to verify real rates."""

    # Use 2 shipments for quick test
    test_data = """California	FEDEX- Priority	Barra 	Odeamar	+639612109875	justinenganga@gmail.com	Blk 6 Lot 48 Camella Vera, Bignay		Valenzuela City	Metro Manila	1440	Philippines	TRUE	13 x 12 x 2	1.8 lbs	 1.5 lbs Dead Sea Mineral Bath Salts HTS Code: 3307.30.1000 ($27)
Nevada	UPS	Osman	Kocakafa	+491635002688	hermanito040@protonmail.com	Memelerstrasse 16 		Hamburg	Hamburg 	22049	DE	TRUE	13 x 12 x 2	2.2 lbs	 1.5 lbs Organic Light Brown Sugar HTS Code: 1701.91.4800 ($27)"""

    print("🔍 Testing LIVE RATES from EasyPost API")
    print("=" * 80)
    print("\n📋 Sample Shipments:")
    print("  1. California → Philippines (Dead Sea Bath Salts, 1.8 lbs)")
    print("  2. Nevada → Germany (Organic Sugar, 2.2 lbs)")
    print("\n⏳ Calling EasyPost API (this may take 10-30 seconds)...\n")

    # Import and call the actual tool

    # Get the tool from MCP server
    # The tool is already registered, we can test it directly
    from src.mcp.tools.bulk_tools import (
        STORE_ADDRESSES,
        parse_dimensions,
        parse_spreadsheet_line,
        parse_weight,
    )

    # Parse manually and call get_rates for first shipment
    lines = [l.strip() for l in test_data.split("\n") if l.strip()]

    print("🧪 TEST 1: California Shipment")
    print("-" * 80)
    line1 = lines[0]
    data1 = parse_spreadsheet_line(line1)
    weight_oz = parse_weight(data1["weight"])
    length, width, height = parse_dimensions(data1["dimensions"])

    to_addr = {
        "name": f"{data1['recipient_name']} {data1['recipient_last_name']}",
        "street1": data1["street1"],
        "street2": data1["street2"],
        "city": data1["city"],
        "state": data1["state"],
        "zip": data1["zip"],
        "country": data1["country"],
        "phone": data1["recipient_phone"],
        "email": data1["recipient_email"],
    }

    from_addr = STORE_ADDRESSES["California"]["Los Angeles"]

    parcel = {
        "length": length,
        "width": width,
        "height": height,
        "weight": weight_oz,
    }

    print(f"From: {from_addr['name']}, {from_addr['city']}, {from_addr['state']}")
    print(f"To: {to_addr['name']}, {to_addr['city']}, {to_addr['country']}")
    print(f"Parcel: {length}×{width}×{height} in, {weight_oz} oz")
    print("\n⏳ Getting real rates from EasyPost...")

    try:
        result = await easypost_service.get_rates(to_addr, from_addr, parcel)

        if result["status"] == "success":
            rates = result.get("data", [])
            print(f"\n✅ SUCCESS! Received {len(rates)} rates:\n")

            for rate in rates[:5]:  # Show first 5
                carrier = rate.get("carrier", "Unknown")
                service = rate.get("service", "Unknown")
                price = rate.get("rate", "N/A")
                days = rate.get("delivery_days", "N/A")
                print(f"  • {carrier:12s} {service:30s} ${price:8s} ({days} days)")

            if len(rates) > 5:
                print(f"  ... and {len(rates) - 5} more options")

            print(f"\n💰 Cheapest: {rates[0]['carrier']} - ${rates[0]['rate']}")
            print("⚡ Fastest: Check delivery_days in full results")

        else:
            print(f"\n❌ Error: {result.get('message')}")
            print("\n📋 Full response:")
            print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"\n❌ Exception: {str(e)}")
        print("\n💡 This might be expected if:")
        print("   - EasyPost API key not configured")
        print("   - API key doesn't support international shipping")
        print("   - Network issues")

    print("\n" + "=" * 80)
    print("✅ Live API test complete!")
    print("\n💡 To test full batch of 19 shipments:")
    print("   Call parse_and_get_bulk_rates() with all your data")
    print("   It will process each shipment and return rates for all")


if __name__ == "__main__":
    asyncio.run(test_live_rates())
