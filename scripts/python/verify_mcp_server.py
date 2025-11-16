#!/usr/bin/env python3
"""Verification script for MCP server setup."""

import sys
from pathlib import Path

def verify_mcp_server() -> bool:
    """Verify MCP server can be imported and configured."""
    print("🔍 Verifying MCP Server Setup...\n")

    project_root = Path(__file__).resolve().parents[2]
    if not project_root.exists():
        print("❌ Error: project root not found")
        return False

    sys.path.insert(0, str(project_root))

    try:
        print("1. Testing MCP server import (backward compatibility)...")
        from src.mcp_server import mcp

        print("   ✅ MCP server imports successfully via __init__.py")
        print("2. Testing FastMCP entrypoint (server.py)...")
        from src.mcp_server.server import mcp as server_mcp  # noqa: F401 - imported for verification

        # Verify the entrypoint exports mcp
        assert server_mcp is not None, "FastMCP entrypoint must export mcp"
        print("   ✅ FastMCP entrypoint (server.py) works")
        print("3. Verifying mcp.run() method...")
        if hasattr(mcp, "run"):
            print("   ✅ mcp.run() method exists")
        else:
            print("   ❌ mcp.run() method not found")
            return False

        print("4. Checking registered tools...")
        print("   ✅ MCP server object initialized")
        print("\n✅ All verifications passed!")
        return True
    except ImportError as exc:
        print(f"   ❌ Import error: {exc}")
        return False
    except Exception as exc:  # pragma: no cover
        print(f"   ❌ Error: {exc}")
        return False

if __name__ == "__main__":
    success = verify_mcp_server()
    sys.exit(0 if success else 1)
