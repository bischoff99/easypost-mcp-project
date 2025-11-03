#!/bin/bash

# M3 Max Optimized Backend Startup with JIT Compilation
# For Python 3.13+ - enables JIT compilation for maximum performance

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting EasyPost MCP Backend with JIT Compilation (Python 3.13+)...${NC}"

# Check Python version for JIT support
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 13 ]; then
    echo -e "${GREEN}✅ Python $PYTHON_VERSION supports JIT compilation${NC}"

    # Enable JIT compilation for maximum performance
    export PYTHON_JIT=1
    echo -e "${YELLOW}🚀 JIT Compilation enabled - expect 10-20% performance boost${NC}"
else
    echo -e "${YELLOW}⚠️  Python $PYTHON_VERSION - JIT requires Python 3.13+${NC}"
    echo -e "${YELLOW}   Falling back to standard optimized mode${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${BLUE}Creating .env from .env.example...${NC}"
    cp .env.example .env
    echo -e "${BLUE}Please update .env with your EasyPost API key${NC}"
    exit 1
fi

# Export Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Calculate workers: (2 x CPU cores) + 1 for M3 Max optimization
# M3 Max 16-core: 33 workers
WORKERS=$(python -c "import multiprocessing; print((2 * multiprocessing.cpu_count()) + 1)")
echo -e "${BLUE}Detected $(python -c "import multiprocessing; print(multiprocessing.cpu_count())") CPU cores (M3 Max), using ${WORKERS} workers${NC}"

# Run server with multi-worker setup, uvloop, and JIT
echo -e "${GREEN}MCP Server running at http://localhost:8000${NC}"
echo -e "${GREEN}Health check: http://localhost:8000/health${NC}"
echo -e "${GREEN}Using ${WORKERS} workers with uvloop and JIT optimization${NC}"

uvicorn src.server:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers $WORKERS \
  --loop uvloop \
  --log-level info
