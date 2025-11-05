#!/bin/bash

# Quick functionality test - runs in ~10 seconds

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

# 3. Nginx proxy
echo -e "${BLUE}3. Nginx Proxy...${NC}"
curl -s http://localhost:8080/health | jq -r '.status' && echo -e "${GREEN}✓${NC}" || echo "✗"

# 4. API through proxy
echo -e "${BLUE}4. API via Proxy...${NC}"
curl -s http://localhost:8080/api/stats | jq -r '.status' && echo -e "${GREEN}✓${NC}" || echo "✗"

# 5. Quick unit tests
echo -e "${BLUE}5. Quick Tests...${NC}"
cd backend && source venv/bin/activate && pytest tests/unit -q -x 2>&1 | tail -1
cd ..

echo ""
echo -e "${GREEN}✅ Quick test complete!${NC}"
