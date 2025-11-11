#!/usr/bin/env python3
"""Test create_bulk_shipments to debug the from_address error."""

import asyncio
import os
import sys
import traceback

sys.path.insert(0, "src")

from fastmcp import FastMCP

from src.services.easypost_service import EasyPostService


class MockContext:
    """Mock context for testing."""

    async def info(self, message):
        print(f"ℹ️  {message}")

    async def report_progress(self, current, total):
        print(f"📊 Progress: {current}/{total}")


async def main():
    """Test create_bulk_shipments with the Nevada shipments."""

    # Check for API key
    api_key = os.getenv("EASYPOST_API_KEY")
    if not api_key:
        print("❌ EASYPOST_API_KEY not set")
        return

    # Initialize service
    service = EasyPostService(api_key)

    # Initialize MCP and register tools
    mcp = FastMCP("test")
    from src.mcp_server.tools.bulk_creation_tools import register_bulk_creation_tools

    register_bulk_creation_tools(mcp, service)

    # Test data
    spreadsheet_data = """Nevada\tUPS\tSiham\tFocken\t+33768021906\tsiham-sisi94@outlook.com\t115/002 Avenue de Canteleu\t\tVilleneuve-d'Ascq\tHauts-de-France\t59650\tFrance\tTRUE\t14 x 12 x 6\t5.4 lbs\t(4) Original Prints and Engravings HTS Code: 4911.10.00 ($22/each)
Nevada\tFEDEX\tSarah\tRani\t+33767493533\tsarah_rani93@outlook.com\t9/2 Rue Delobel\t\tTourcoing\tHauts-de-France\t59200\tFrance\tFALSE\t14 x 12 x 6\t5.7 lbs\t(2) Cooling Memory Foam Pillow HTS Code: 9404.90.1000 ($38 each)"""

    print("🚀 Testing create_bulk_shipments")
    print("=" * 70)

    ctx = MockContext()

    try:
        # Call the function directly by re-importing
        from src.mcp_server.tools.bulk_creation_tools import register_bulk_creation_tools

        # Create a fresh MCP instance
        test_mcp = FastMCP("test2")

        # Register - this will decorate the function
        register_bulk_creation_tools(test_mcp, service)

        # Get the registered function
        tools = test_mcp._tool_manager.get_tools()
        for tool_name, tool in tools.items():
            if tool_name == "create_bulk_shipments":
                # Call it
                result = await tool.fn(
                    spreadsheet_data=spreadsheet_data, purchase_labels=False, ctx=ctx
                )

                print("\n" + "=" * 70)
                print("📦 RESULT")
                print("=" * 70)
                print(f"Status: {result.get('status')}")
                if result.get("status") == "error":
                    print(f"Error: {result.get('message')}")
                else:
                    print(f"Success: {result.get('message')}")

                break

    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ ERROR")
        print("=" * 70)
        print(f"Exception: {e}")
        print("\nFull traceback:")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
