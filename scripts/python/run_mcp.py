#!/usr/bin/env python3
"""MCP Server runner for Claude Desktop integration."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILES = [PROJECT_ROOT / ".env", PROJECT_ROOT / "config" / ".env"]

# Load .env files first
for env_file in ENV_FILES:
    if env_file.exists():
        load_dotenv(env_file)
        print(f"Loaded environment from: {env_file}", file=sys.stderr)

# Load API key from Keychain if not already set (matches .envrc behaviour)
if not os.getenv("EASYPOST_API_KEY"):
    environment = os.getenv("ENVIRONMENT", "test")
    keychain_service = "easypost-prod" if environment == "production" else "easypost-test"

    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", keychain_service, "-w"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            api_key = result.stdout.strip()
            os.environ["EASYPOST_API_KEY"] = api_key
            print(f"Loaded API key from Keychain: {keychain_service}", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Could not load API key from Keychain: {e}", file=sys.stderr)

sys.path.insert(0, str(PROJECT_ROOT))

# Import from standalone server entrypoint (FastMCP compliant)
from src.mcp_server.server import mcp  # noqa: E402

if __name__ == "__main__":
    mcp.run()
