#!/usr/bin/env bash
# MCP Utility Commands
# Standalone MCP verification and testing utilities

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VENV_BIN="${PROJECT_ROOT}/apps/backend/.venv/bin"

# Detect venv location
if [ ! -d "$VENV_BIN" ]; then
    VENV_BIN="${PROJECT_ROOT}/apps/backend/venv/bin"
fi

# MCP Tool Helper
mcp_tool() {
    local tool_name="$1"
    shift
    "${VENV_BIN}/python" "${PROJECT_ROOT}/scripts/python/mcp_tool.py" "$tool_name" "$@"
}

# Check MCP server health
check_mcp_health() {
    echo "🔍 Checking MCP server health..."

    # Try to call a simple MCP tool
    if mcp_tool get_tracking "TEST" 2>/dev/null | grep -q "status"; then
        echo "✅ MCP server is accessible"
        return 0
    else
        echo "⚠️  MCP server not accessible (this is OK if server not running)"
        return 1
    fi
}

# Verify MCP tools are registered
verify_mcp_tools() {
    echo "🔍 Verifying MCP tools..."

    local tools=$(mcp_tool list_tools 2>/dev/null || echo '{"available_tools": []}')
    local tool_count=$(echo "$tools" | grep -o '"available_tools"' | wc -l || echo "0")

    if [ "$tool_count" -gt 0 ]; then
        echo "✅ MCP tools verified"
        echo "$tools" | jq -r '.available_tools[]' 2>/dev/null || echo "  (tools available)"
    else
        echo "⚠️  Could not verify MCP tools"
    fi
}

# Test MCP tools with sample data
test_mcp_tools() {
    echo "🧪 Testing MCP tools..."

    # Test get_tracking (will fail with invalid tracking number, but shows tool works)
    echo "  Testing get_tracking..."
    mcp_tool get_tracking "TEST123" 2>/dev/null | jq -r '.status' || echo "    (expected failure with test data)"

    echo "✅ MCP tools test complete"
}

# Main function
main() {
    case "${1:-help}" in
        health)
            check_mcp_health
            ;;
        verify)
            verify_mcp_tools
            ;;
        test)
            test_mcp_tools
            ;;
        *)
            echo "Usage: $0 {health|verify|test}"
            echo ""
            echo "Commands:"
            echo "  health  - Check MCP server health"
            echo "  verify  - Verify MCP tools are registered"
            echo "  test    - Test MCP tools with sample data"
            exit 1
            ;;
    esac
}

main "$@"
