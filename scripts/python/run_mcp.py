#!/usr/bin/env python3
"""MCP Server runner for Claude Desktop integration."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILES = [PROJECT_ROOT / ".env", PROJECT_ROOT / "config" / ".env"]

for env_file in ENV_FILES:
    if env_file.exists():
        load_dotenv(env_file)
        print(f"Loaded environment from: {env_file}", file=sys.stderr)

sys.path.insert(0, str(PROJECT_ROOT))

from src.mcp_server import mcp  # noqa: E402

if __name__ == "__main__":
    mcp.run()
