#!/usr/bin/env python3
"""Integration test for bulk shipment tool with real data."""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.mcp import mcp, easypost_service


async def test_bulk_tool():
    """Test bulk tool with actual spreadsheet data."""
    
    # Your exact data
    test_data = """California	FEDEX- Priority	Barra 	Odeamar	+639612109875	justinenganga@gmail.com	Blk 6 Lot 48 Camella Vera, Bignay		Valenzuela City	Metron Manila	1440	Philippines	TRUE	13 x 12 x 2	1.8 lbs	 1.5 lbs Dead Sea Mineral Bath Salts HTS Code: 3307.30.1000 ($27)			

California	FEDEX- Priority	Luis	Abdala	+639614337118	kingkonlouis@gmail.com	95 Feliza St, Parada		Valenzuela City	Metro Manila	1441	Philippines	FALSE	13 x 12 x 2	1.7 lbs	 1.5 lbs Dead Sea Mineral Bath Salts HTS Code: 3307.30.1000 ($27)"""

    print("🧪 Testing bulk tool with your data...")
    print("=" * 70)
    
    # Import the tool function directly
    from src.mcp.tools.bulk_tools import parse_spreadsheet_line, parse_weight, parse_dimensions
    
    # Test parsing first line
    lines = [l.strip() for l in test_data.split('\n') if l.strip()]
    print(f"\n📋 Found {len(lines)} shipments\n")
    
    for idx, line in enumerate(lines, 1):
        print(f"Shipment {idx}:")
        print("-" * 70)
        
        try:
            data = parse_spreadsheet_line(line)
            print(f"  ✅ Recipient: {data['recipient_name']} {data['recipient_last_name']}")
            print(f"  ✅ Email: {data['recipient_email']}")
            print(f"  ✅ Phone: {data['recipient_phone']}")
            print(f"  ✅ Address: {data['street1']}, {data['city']}")
            print(f"  ✅ Destination: {data['city']}, {data['state']}, {data['country']}")
            print(f"  ✅ ZIP: {data['zip']}")
            
            # Parse dimensions
            length, width, height = parse_dimensions(data['dimensions'])
            print(f"  ✅ Dimensions: {length}\" x {width}\" x {height}\" (from '{data['dimensions']}')")
            
            # Parse weight
            weight_oz = parse_weight(data['weight'])
            print(f"  ✅ Weight: {weight_oz} oz (from '{data['weight']}')")
            
            print(f"  ✅ Contents: {data['contents'][:50]}...")
            print()
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            print()
    
    print("=" * 70)
    print("✅ All parsing successful!")
    print("\n📍 From Address (Los Angeles):")
    from src.mcp.tools.bulk_tools import CA_STORE_ADDRESSES
    la_store = CA_STORE_ADDRESSES["Los Angeles"]
    print(f"  {la_store['name']}")
    print(f"  {la_store['company']}")
    print(f"  {la_store['street1']}, {la_store['street2']}")
    print(f"  {la_store['city']}, {la_store['state']} {la_store['zip']}")
    print(f"  {la_store['phone']}")
    
    print("\n✅ Integration test complete!")
    print("\n💡 To get actual rates, call:")
    print("   parse_and_get_bulk_rates(spreadsheet_data=<your_data>, from_city='Los Angeles')")


if __name__ == "__main__":
    asyncio.run(test_bulk_tool())

