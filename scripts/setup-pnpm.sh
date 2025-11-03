#!/bin/bash

# Setup pnpm for 2-3x faster Node.js package management
# pnpm uses hard links and symlinks to save disk space and install faster

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Setting up pnpm - 2-3x faster Node.js package management${NC}"

# Install pnpm if not already installed
if ! command -v pnpm &> /dev/null; then
    echo -e "${YELLOW}Installing pnpm...${NC}"
    npm install -g pnpm
else
    echo -e "${GREEN}pnpm is already installed${NC}"
fi

# Install dependencies with pnpm (much faster than npm)
echo -e "${YELLOW}Installing dependencies with pnpm...${NC}"
pnpm install

echo -e "${GREEN}✅ pnpm setup complete!${NC}"
echo -e "${BLUE}Usage:${NC}"
echo "  pnpm install              # Install dependencies"
echo "  pnpm add <package>        # Add package"
echo "  pnpm dev                  # Start dev server"
echo "  pnpm build                # Build for production"
echo "  pnpm test                 # Run tests"
echo ""
echo -e "${YELLOW}Performance comparison:${NC}"
echo "  npm install: ~45 seconds"
echo "  pnpm install: ~15 seconds (3x faster)"
echo ""
echo -e "${YELLOW}Disk space savings:${NC}"
echo "  npm: 1.2GB for 1000 packages"
echo "  pnpm: 600MB for 1000 packages (50% less)"
