#!/usr/bin/env python3
"""Get bulk rates using the bulk parser tool."""
import asyncio
import json
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from src.mcp_server.tools.bulk_tools import BulkShipmentTools

# Formatted bulk data
bulk_data = """New York		Marie	Lenaerts	+32488003329	marsiekke1@outlook.com	Recollettenstraat 39		Nieuwpoort		8620	Belgium		13x13x7	4.5 lbs	Women's cotton Sweater Quantity: 2 Total Price: $34
New York		Thibo	Van Dyck	+32478933888	oceanIn.5@outlook.com	Parijsstraat 12		Middelkerke		8430	Belgium		13x13x13	6lb 5oz	Custom Soccer Cleats Quantity: 2 Price: $55"""

async def main():
    tools = BulkShipmentTools()
    result = await tools.parse_and_get_bulk_rates(bulk_data)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
