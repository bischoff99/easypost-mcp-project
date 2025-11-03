#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting EasyPost MCP Backend...${NC}"

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
# M3 Max 14-core: 29 workers for maximum concurrency
WORKERS=$(python -c "import multiprocessing; print((2 * multiprocessing.cpu_count()) + 1)")
echo -e "${BLUE}Detected $(python -c "import multiprocessing; print(multiprocessing.cpu_count())") CPU cores, using ${WORKERS} workers${NC}"

# Run server with multi-worker setup and uvloop
echo -e "${GREEN}MCP Server running at http://localhost:8000${NC}"
echo -e "${GREEN}Health check: http://localhost:8000/health${NC}"
echo -e "${GREEN}Using ${WORKERS} workers with uvloop for optimal M3 Max performance${NC}"

uvicorn src.server:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers $WORKERS \
  --loop uvloop \
  --log-level info
