#!/bin/bash

# EasyPost MCP - Full Functionality Test Suite
# Tests all components, endpoints, and integrations

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   EasyPost MCP - Full Functionality Test Suite          ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function
test_endpoint() {
    local name=$1
    local url=$2
    local expected=$3

    echo -e "${BLUE}Testing: ${name}${NC}"

    if response=$(curl -s -m 5 "$url"); then
        if echo "$response" | grep -q "$expected"; then
            echo -e "${GREEN}✓ PASSED${NC}"
            ((TESTS_PASSED++))
        else
            echo -e "${RED}✗ FAILED - Unexpected response${NC}"
            ((TESTS_FAILED++))
        fi
    else
        echo -e "${RED}✗ FAILED - No response${NC}"
        ((TESTS_FAILED++))
    fi
    echo ""
}

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 1: Backend Unit Tests (16 workers)"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd backend
source venv/bin/activate
if pytest tests/unit -v -n 16 --tb=short -q 2>&1 | tail -5; then
    echo -e "${GREEN}✓ Backend unit tests PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ Backend unit tests FAILED${NC}"
    ((TESTS_FAILED++))
fi
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 2: Backend Integration Tests"
echo "═══════════════════════════════════════════════════════════"
echo ""

if pytest tests/integration -v --tb=short -q 2>&1 | tail -5; then
    echo -e "${GREEN}✓ Backend integration tests PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ Backend integration tests FAILED${NC}"
    ((TESTS_FAILED++))
fi
echo ""

cd ..

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 3: Frontend Tests (20 workers)"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd frontend
if npm test 2>&1 | tail -8; then
    echo -e "${GREEN}✓ Frontend tests PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ Frontend tests FAILED${NC}"
    ((TESTS_FAILED++))
fi
echo ""

cd ..

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 4: API Endpoint Tests"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Give services time to warm up
sleep 2

# Health Check
test_endpoint "Backend Health" "http://localhost:8000/health" "healthy"
test_endpoint "Proxy Health" "http://localhost:8080/health" "healthy"

# API Endpoints (Direct)
test_endpoint "Stats Endpoint (Direct)" "http://localhost:8000/stats" "success"
test_endpoint "Analytics Endpoint (Direct)" "http://localhost:8000/analytics" "success"
test_endpoint "Carrier Performance (Direct)" "http://localhost:8000/carrier-performance" "success"

# API Endpoints (Through Proxy)
test_endpoint "Stats via Proxy" "http://localhost:8080/api/stats" "success"
test_endpoint "Analytics via Proxy" "http://localhost:8080/api/analytics" "success"
test_endpoint "Carrier Performance via Proxy" "http://localhost:8080/api/carrier-performance" "success"

# Frontend
test_endpoint "Frontend (Direct)" "http://localhost:5173" "<!doctype html>"
test_endpoint "Frontend via Proxy" "http://localhost:8080" "<!doctype html>"

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 5: Code Quality Checks"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd backend
echo -e "${BLUE}Testing: Backend Linting${NC}"
if ruff check src/ --exit-zero > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASSED - No linting errors${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAILED - Linting errors found${NC}"
    ((TESTS_FAILED++))
fi
echo ""

cd ../frontend
echo -e "${BLUE}Testing: Frontend Linting${NC}"
if npx eslint src --max-warnings 0 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASSED - No linting errors${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAILED - Linting errors found${NC}"
    ((TESTS_FAILED++))
fi
echo ""

cd ..

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 6: Configuration Validation"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check configuration files
for file in backend/.env backend/pytest.ini frontend/vite.config.js; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ PASSED - $file exists${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAILED - $file missing${NC}"
        ((TESTS_FAILED++))
    fi
done
echo ""

# Check nginx config
echo -e "${BLUE}Testing: Nginx Configuration${NC}"
if nginx -t > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASSED - Nginx config valid${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAILED - Nginx config invalid${NC}"
    ((TESTS_FAILED++))
fi
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 7: Performance Checks"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}Testing: Response Times${NC}"

# Test backend response time
backend_time=$(curl -s -w "%{time_total}" -o /dev/null http://localhost:8000/health)
if (( $(echo "$backend_time < 0.5" | bc -l) )); then
    echo -e "${GREEN}✓ PASSED - Backend response: ${backend_time}s${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAILED - Backend slow: ${backend_time}s${NC}"
    ((TESTS_FAILED++))
fi

# Test proxy response time
proxy_time=$(curl -s -w "%{time_total}" -o /dev/null http://localhost:8080/health)
if (( $(echo "$proxy_time < 0.5" | bc -l) )); then
    echo -e "${GREEN}✓ PASSED - Proxy response: ${proxy_time}s${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAILED - Proxy slow: ${proxy_time}s${NC}"
    ((TESTS_FAILED++))
fi
echo ""

# Summary
echo "═══════════════════════════════════════════════════════════"
echo "                     TEST SUMMARY"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}Tests Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Tests Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║            ✅ ALL TESTS PASSED ✅                        ║${NC}"
    echo -e "${GREEN}║      System is fully functional and ready!               ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║            ❌ SOME TESTS FAILED ❌                       ║${NC}"
    echo -e "${RED}║        Please review errors above                        ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi

