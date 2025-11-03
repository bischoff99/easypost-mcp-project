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

# Run server
echo -e "${GREEN}MCP Server running at http://localhost:8000${NC}"
echo -e "${GREEN}Health check: http://localhost:8000/health${NC}"
python src/server.py
