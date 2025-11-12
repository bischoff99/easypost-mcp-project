#!/usr/bin/env python3
"""
MCP Tool CLI - Call EasyPost MCP tools from bash scripts.

Usage:
    python scripts/python/mcp_tool.py <tool_name> [args...]

Examples:
    python scripts/python/mcp_tool.py get_tracking EZ1234567890
    python scripts/python/mcp_tool.py get_shipment_rates --data "John Doe\t123 Main St..."
    python scripts/python/mcp_tool.py create_shipment --data "..." --dry-run
"""

import asyncio
import json
import sys
from pathlib import Path

# Add backend to path (mcp_tool.py is now in scripts/python/, so go up two levels)
backend_path = Path(__file__).parent.parent.parent / "apps" / "backend"
sys.path.insert(0, str(backend_path))

from src.mcp_server import mcp, easypost_service
from fastmcp import Context


async def call_tool(tool_name: str, **kwargs):
    """Call an MCP tool and return JSON result."""
    try:
        # Get tool from MCP server
        tool = None
        for registered_tool in mcp.list_tools():
            if registered_tool.name == tool_name:
                tool = registered_tool
                break

        if not tool:
            return {
                "status": "error",
                "message": f"Tool '{tool_name}' not found",
                "available_tools": [t.name for t in mcp.list_tools()]
            }

        # Create a simple context
        class SimpleContext:
            async def info(self, msg):
                print(f"[INFO] {msg}", file=sys.stderr)

            async def report_progress(self, current, total):
                print(f"[PROGRESS] {current}/{total}", file=sys.stderr)

        ctx = SimpleContext()

        # Call the tool
        result = await tool.call(ctx=ctx, **kwargs)

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }


def parse_args():
    """Parse command line arguments."""
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    tool_name = sys.argv[1]
    kwargs = {}

    # Parse key=value arguments
    for arg in sys.argv[2:]:
        if arg.startswith("--"):
            if "=" in arg:
                key, value = arg[2:].split("=", 1)
                # Try to parse as JSON, fallback to string
                try:
                    kwargs[key] = json.loads(value)
                except json.JSONDecodeError:
                    kwargs[key] = value
            else:
                # Boolean flag
                kwargs[arg[2:].replace("-", "_")] = True
        elif arg.startswith("-"):
            # Short flag
            kwargs[arg[1:]] = True
        else:
            # Positional argument - use as first parameter
            if "data" not in kwargs and "spreadsheet_data" not in kwargs:
                kwargs["spreadsheet_data" if "shipment" in tool_name or "rate" in tool_name else "tracking_number"] = arg

    return tool_name, kwargs


async def main():
    """Main entry point."""
    tool_name, kwargs = parse_args()

    result = await call_tool(tool_name, **kwargs)

    # Output as JSON
    print(json.dumps(result, indent=2))

    # Exit with error code if failed
    if result.get("status") == "error":
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
