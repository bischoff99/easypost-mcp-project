#!/usr/bin/env python3
"""Get bulk rates using the MCP bulk parser tool.

Usage: python scripts/python/get-bulk-rates.py
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Load environment variables before other imports
from dotenv import load_dotenv

load_dotenv(project_root / ".env")

# Imports after environment setup
from fastmcp import FastMCP

from src.mcp_server.tools.bulk_tools import register_shipment_tools
from src.services.easypost_service import EasyPostService
from src.utils.config import settings

# Formatted bulk data
bulk_data = """New York		Marie	Lenaerts	+32488003329	marsiekke1@outlook.com	Recollettenstraat 39		Nieuwpoort		8620	Belgium		13x13x7	4.5 lbs	Women's cotton Sweater Quantity: 2 Total Price: $34
New York		Thibo	Van Dyck	+32478933888	oceanIn.5@outlook.com	Parijsstraat 12		Middelkerke		8430	Belgium		13x13x13	6lb 5oz	Custom Soccer Cleats Quantity: 2 Price: $55"""


async def main():
    """Call get_shipment_rates tool directly."""
    # Create service instance
    service = EasyPostService(api_key=settings.EASYPOST_API_KEY)

    # Create MCP instance and register tools
    mcp = FastMCP("test")
    register_shipment_tools(mcp, service)

    # Access the tool via mcp's internal registry
    # Note: This accesses internal FastMCP API - may need adjustment if FastMCP changes
    try:
        # Try to access via tools attribute (if available)
        tools_dict = getattr(mcp, "_tools", None) or getattr(mcp, "tools", {})
        tool_func = None

        for tool_name, tool_obj in tools_dict.items():
            if tool_name == "get_shipment_rates":
                # Get the actual function from the tool object
                tool_func = getattr(tool_obj, "fn", tool_obj)
                if callable(tool_func):
                    break

        if not tool_func:
            # Fallback: try to call directly if registered as attribute
            tool_func = getattr(mcp, "get_shipment_rates", None)

        if not tool_func:
            print("Error: Could not access get_shipment_rates tool", file=sys.stderr)
            print(
                "Available tools:",
                list(tools_dict.keys()) if tools_dict else "none",
                file=sys.stderr,
            )
            sys.exit(1)

        # Call the tool function directly
        result = await tool_func(spreadsheet_data=bulk_data, ctx=None)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error calling tool: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
