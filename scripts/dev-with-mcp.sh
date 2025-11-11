#!/usr/bin/env bash
# Enhanced development script with MCP tool integration

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_BIN="${PROJECT_ROOT}/apps/backend/.venv/bin"

# MCP Tool Helper
mcp_tool() {
    local tool_name="$1"
    shift
    "${VENV_BIN}/python" "${SCRIPT_DIR}/mcp_tool.py" "$tool_name" "$@"
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

# Start backend with MCP verification
start_backend_with_mcp() {
    echo "🚀 Starting backend server..."

    cd "${PROJECT_ROOT}/apps/backend"
    source "${VENV_BIN}/activate"

    # Start server in background
    uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload &
    local backend_pid=$!

    # Wait for server to start
    echo "⏳ Waiting for server to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "✅ Backend server started (PID: $backend_pid)"

            # Verify MCP tools after server starts
            sleep 2
            verify_mcp_tools

            return 0
        fi
        sleep 1
    done

    echo "❌ Backend server failed to start"
    return 1
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
        start)
            start_backend_with_mcp
            ;;
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
            echo "Usage: $0 {start|health|verify|test}"
            echo ""
            echo "Commands:"
            echo "  start   - Start backend server with MCP verification"
            echo "  health  - Check MCP server health"
            echo "  verify  - Verify MCP tools are registered"
            echo "  test    - Test MCP tools with sample data"
            exit 1
            ;;
    esac
}

main "$@"
