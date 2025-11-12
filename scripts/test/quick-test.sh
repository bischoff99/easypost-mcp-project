#!/usr/bin/env zsh

# Quick functionality test - runs in ~10 seconds

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Quick Test Suite (Est. 10s)${NC}"
echo ""

# 1. Backend health
echo -e "${BLUE}1. Backend Health...${NC}"
curl -s http://localhost:8000/health | jq -r '.status' && echo -e "${GREEN}✓${NC}" || echo "✗"

# 2. Frontend responding
echo -e "${BLUE}2. Frontend...${NC}"
curl -s http://localhost:5173 | head -1 && echo -e "${GREEN}✓${NC}" || echo "✗"

# 3. Nginx proxy (if running)
echo -e "${BLUE}3. Nginx Proxy...${NC}"
if curl -s http://localhost:8080/health >/dev/null 2>&1; then
    curl -s http://localhost:8080/health | jq -r '.ok' && echo -e "${GREEN}✓${NC}" || echo "✗"
else
    echo -e "${GREEN}✓${NC} (not running, skipping)"
fi

# 4. API endpoint (analytics)
echo -e "${BLUE}4. API Endpoint...${NC}"
curl -s http://localhost:8000/api/analytics 2>/dev/null | jq -r '.status' && echo -e "${GREEN}✓${NC}" || echo "✗"

# 5. Quick unit tests
echo -e "${BLUE}5. Quick Tests...${NC}"
cd apps/backend && source venv/bin/activate && pytest tests/unit -q -x 2>&1 | tail -1
cd ..

echo ""
echo -e "${GREEN}✅ Quick test complete!${NC}"
