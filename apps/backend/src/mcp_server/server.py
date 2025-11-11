"""MCP Server entry point for Cursor Desktop integration.

This module provides the server entry point that Cursor Desktop will invoke
via `.cursor/mcp.json` configuration.
"""

from src.mcp_server import mcp

if __name__ == "__main__":
    # Run in stdio mode for Cursor Desktop
    mcp.run()
