#!/usr/bin/env python3
"""
MCP Server runner for Claude Desktop integration.
This script runs the EasyPost MCP server in stdio mode.
"""
import os
import sys

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from src.mcp_server import mcp

if __name__ == "__main__":
    # Run in stdio mode for Claude Desktop
    mcp.run()
