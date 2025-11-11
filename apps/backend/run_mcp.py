#!/usr/bin/env python3
"""
MCP Server runner for Claude Desktop integration.
This script runs the EasyPost MCP server in stdio mode.
"""
import os
import sys
from pathlib import Path

# Load .env file from project root before importing anything
project_root = Path(__file__).parent.parent.parent
env_file = project_root / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)
    print(f"Loaded environment from: {env_file}", file=sys.stderr)

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from src.mcp_server import mcp

if __name__ == "__main__":
    # Run in stdio mode for Claude Desktop
    mcp.run()
