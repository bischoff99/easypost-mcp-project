#!/usr/bin/env zsh
set -euo pipefail

# Backend Startup Script
# Usage: ./scripts/start-backend.sh [--jit] [--mcp-verify]
#   --jit: Enable JIT compilation (Python 3.13+, multi-worker mode)
#   --mcp-verify: Enable enhanced MCP tool verification after startup

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BACKEND_DIR="${PROJECT_ROOT}/apps/backend"
SCRIPTS_DIR="${PROJECT_ROOT}/scripts"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check for flags
JIT_MODE=false
MCP_VERIFY=false
if [[ "$*" == *"--jit"* ]]; then
  JIT_MODE=true
fi
if [[ "$*" == *"--mcp-verify"* ]]; then
  MCP_VERIFY=true
fi

# MCP Tool Helper
mcp_tool() {
    local tool_name="$1"
    shift
    local venv_bin="${BACKEND_DIR}/.venv/bin"
    if [ ! -d "$venv_bin" ]; then
        venv_bin="${BACKEND_DIR}/venv/bin"
    fi
    "${venv_bin}/python" "${SCRIPTS_DIR}/python/mcp_tool.py" "$tool_name" "$@"
}

# Enhanced MCP verification
verify_mcp_tools() {
    echo -e "${BLUE}🔍 Verifying MCP tools...${NC}"

    # Check if mcp_tool.py exists
    if [ ! -f "${SCRIPTS_DIR}/python/mcp_tool.py" ]; then
        echo -e "${YELLOW}⚠️  MCP tool script not found${NC}"
        return 1
    fi

    # Try to call a simple MCP tool
    if mcp_tool get_tracking "TEST" 2>/dev/null | grep -q "status"; then
        echo -e "${GREEN}✅ MCP tools accessible${NC}"

        # Try to verify tools are registered (if list_tools exists)
        local tools_output=$(mcp_tool list_tools 2>/dev/null || echo "")
        if [ -n "$tools_output" ] && echo "$tools_output" | grep -q "available_tools"; then
            local tool_count=$(echo "$tools_output" | grep -o '"available_tools"' | wc -l || echo "0")
            if [ "$tool_count" -gt 0 ]; then
                echo -e "${GREEN}✅ MCP tools registered${NC}"
                echo "$tools_output" | jq -r '.available_tools[]' 2>/dev/null | head -5 || echo "  (tools available)"
            fi
        fi
        return 0
    else
        echo -e "${YELLOW}⚠️  MCP tools not yet accessible (server may still be starting)${NC}"
        return 1
    fi
}

echo "🔧 Setting up backend..."

cd "${BACKEND_DIR}"

# Detect venv location (prefers .venv, then venv)
if [ -d ".venv" ]; then
  VENV_PATH=".venv"
elif [ -d "venv" ]; then
  VENV_PATH="venv"
else
  echo "📁 Creating virtual environment..."
  python3 -m venv .venv
  VENV_PATH=".venv"
fi

# Activate virtual environment
source "${VENV_PATH}/bin/activate"

# Install dependencies
echo "📚 Installing dependencies..."
pip install -U pip setuptools wheel
pip install -e .

# JIT mode: Multi-worker setup with JIT compilation
if [ "$JIT_MODE" = true ]; then
  # Check Python version for JIT support
  PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
  PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
  PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

  if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 13 ]; then
    echo -e "${GREEN}✅ Python $PYTHON_VERSION supports JIT compilation${NC}"
    export PYTHON_JIT=1
    echo -e "${YELLOW}🚀 JIT Compilation enabled - expect 10-20% performance boost${NC}"
  else
    echo -e "${YELLOW}⚠️  Python $PYTHON_VERSION - JIT requires Python 3.13+${NC}"
    echo -e "${YELLOW}   Falling back to standard optimized mode${NC}"
  fi

  # Calculate workers: (2 x CPU cores) + 1
  WORKERS=$(python -c "import multiprocessing; print((2 * multiprocessing.cpu_count()) + 1)")
  CPU_COUNT=$(python -c "import multiprocessing; print(multiprocessing.cpu_count())")
  echo -e "${BLUE}Detected ${CPU_COUNT} CPU cores, using ${WORKERS} workers${NC}"

  # Export Python path
  export PYTHONPATH="${PYTHONPATH}:$(pwd)"

  echo -e "${GREEN}MCP Server running at http://localhost:8000${NC}"
  echo -e "${GREEN}Health check: http://localhost:8000/health${NC}"
  echo -e "${GREEN}Using ${WORKERS} workers with uvloop and JIT optimization${NC}"

  uvicorn src.server:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers $WORKERS \
    --loop uvloop \
    --log-level info &
  UVICORN_PID=$!

  # Wait for server to start, then verify MCP tools
  echo -e "${BLUE}⏳ Waiting for server to start...${NC}"
  sleep 5

  # Verify MCP tools are accessible
  if [ "$MCP_VERIFY" = true ]; then
    verify_mcp_tools
  else
    # Basic verification
    if command -v python >/dev/null 2>&1; then
      if python "${SCRIPTS_DIR}/python/mcp_tool.py" get_tracking TEST 2>/dev/null | grep -q "status"; then
        echo -e "${GREEN}✅ MCP tools verified${NC}"
      else
        echo -e "${YELLOW}⚠️  MCP tools not yet accessible (server may still be starting)${NC}"
      fi
    fi
  fi

  # Wait for uvicorn process
  wait $UVICORN_PID
else
  # Standard mode: Single worker with reload
  echo "🚀 Starting backend server on http://localhost:8000"
  uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload &
  UVICORN_PID=$!

  # Wait for server to start, then verify MCP tools
  echo "⏳ Waiting for server to start..."
  sleep 3

  # Verify MCP tools are accessible
  if [ "$MCP_VERIFY" = true ]; then
    verify_mcp_tools
  else
    # Basic verification
    if command -v python >/dev/null 2>&1; then
      if python "${SCRIPTS_DIR}/python/mcp_tool.py" get_tracking TEST 2>/dev/null | grep -q "status"; then
        echo -e "${GREEN}✅ MCP tools verified${NC}"
      else
        echo -e "${YELLOW}⚠️  MCP tools not yet accessible (server may still be starting)${NC}"
      fi
    fi
  fi

  # Wait for uvicorn process
  wait $UVICORN_PID
fi
