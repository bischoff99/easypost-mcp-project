#!/bin/bash

# Setup uv package manager for 100x faster Python package management
# uv is the fastest Python package installer and resolver, written in Rust

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Setting up uv - 100x faster Python package management${NC}"

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}Installing uv...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo -e "${GREEN}uv is already installed${NC}"
fi

# Create virtual environment with uv (much faster than venv)
echo -e "${YELLOW}Creating virtual environment with uv...${NC}"
uv venv

# Install dependencies with uv (blazing fast)
echo -e "${YELLOW}Installing dependencies with uv...${NC}"
uv pip install -r requirements.txt

echo -e "${GREEN}✅ uv setup complete!${NC}"
echo -e "${BLUE}Usage:${NC}"
echo "  uv pip install <package>    # Install packages"
echo "  uv pip compile requirements.in -o requirements.txt  # Update requirements"
echo "  uv run python src/server.py  # Run scripts"
echo ""
echo -e "${YELLOW}Performance comparison:${NC}"
echo "  pip install requests: ~2-3 seconds"
echo "  uv pip install requests: ~0.1 seconds (20x faster)"
