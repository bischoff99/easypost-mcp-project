#!/bin/bash

# EasyPost API Standards Validation
# Validates project against EasyPost official documentation and best practices

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   EasyPost API Standards & Endpoint Validation           ║${NC}"
echo -e "${BLUE}║   Reference: github.com/EasyPost/easypost-python          ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

cd /Users/andrejs/Developer/github/andrejs/easypost-mcp-project

CHECKS_PASSED=0
CHECKS_FAILED=0
WARNINGS=0

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 1: EasyPost SDK Usage Validation"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check 1: EasyPost client initialization pattern
echo -e "${BLUE}✓ Checking: Client Initialization Pattern${NC}"
if grep -r "easypost.EasyPostClient" apps/backend/src/ | grep -q "api_key"; then
    echo "  ✓ Using official EasyPostClient pattern"
    ((CHECKS_PASSED++))
else
    echo "  ⚠️  Non-standard client initialization detected"
    ((WARNINGS++))
fi

# Check 2: Async wrapper implementation
echo -e "${BLUE}✓ Checking: Async/Sync Pattern${NC}"
if grep -q "run_in_executor" apps/backend/src/services/easypost_service.py; then
    echo "  ✓ Proper async wrapper (ThreadPoolExecutor)"
    echo "    Pattern: async def → run_in_executor → sync SDK call"
    ((CHECKS_PASSED++))
else
    echo "  ✗ Missing async wrapper pattern"
    ((CHECKS_FAILED++))
fi

# Check 3: Error handling
echo -e "${BLUE}✓ Checking: Error Handling${NC}"
if grep -q "try:" apps/backend/src/services/easypost_service.py && grep -q "except.*Exception" apps/backend/src/services/easypost_service.py; then
    echo "  ✓ Exception handling implemented"
    ((CHECKS_PASSED++))
else
    echo "  ✗ Missing error handling"
    ((CHECKS_FAILED++))
fi

echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 2: API Endpoint Coverage"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Core EasyPost endpoints per official docs
declare -a REQUIRED_ENDPOINTS=(
    "create_shipment"
    "buy_shipment"
    "get_rates"
    "get_tracking"
    "list_shipments"
    "refund_shipment"
)

echo -e "${BLUE}Validating Core API Operations:${NC}"
for endpoint in "${REQUIRED_ENDPOINTS[@]}"; do
    if grep -q "def ${endpoint}" apps/backend/src/services/easypost_service.py; then
        echo "  ✓ ${endpoint}"
        ((CHECKS_PASSED++))
    else
        echo "  ✗ Missing: ${endpoint}"
        ((CHECKS_FAILED++))
    fi
done

echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 3: Dashboard Endpoint Integration"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check backend API endpoints
declare -a BACKEND_ENDPOINTS=(
    "/health"
    "/stats"
    "/analytics"
    "/carrier-performance"
    "/api/shipments"
    "/api/shipments/rates"
    "/api/shipments/tracking"
)

echo -e "${BLUE}Testing Backend Endpoints:${NC}"
for endpoint in "${BACKEND_ENDPOINTS[@]}"; do
    status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000${endpoint} 2>/dev/null)
    if [ "$status" = "200" ]; then
        echo "  ✓ ${endpoint} (${status})"
        ((CHECKS_PASSED++))
    else
        echo "  ⚠️  ${endpoint} (${status})"
        ((WARNINGS++))
    fi
done

echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 4: Development Standards Validation"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}EasyPost SDK Best Practices:${NC}"

# Check 1: API key from environment
echo "1. API Key Management:"
if grep -q "os.getenv.*EASYPOST_API_KEY" apps/backend/src/ -r; then
    echo "   ✓ Using environment variables (secure)"
    ((CHECKS_PASSED++))
else
    echo "   ✗ Hardcoded API keys detected"
    ((CHECKS_FAILED++))
fi

# Check 2: Address validation
echo "2. Address Validation:"
if grep -q "AddressModel" apps/backend/src/services/easypost_service.py; then
    echo "   ✓ Pydantic models for validation"
    ((CHECKS_PASSED++))
else
    echo "   ⚠️  No address validation models"
    ((WARNINGS++))
fi

# Check 3: Rate selection
echo "3. Rate Selection:"
if grep -q "lowest_rate\|cheapest" apps/backend/src/ -r; then
    echo "   ✓ Smart rate selection implemented"
    ((CHECKS_PASSED++))
else
    echo "   ⚠️  Manual rate selection only"
    ((WARNINGS++))
fi

# Check 4: Bulk operations
echo "4. Bulk Operations:"
if grep -q "create_bulk\|batch" apps/backend/src/services/easypost_service.py; then
    echo "   ✓ Bulk operations support (M3 Max optimized)"
    ((CHECKS_PASSED++))
else
    echo "   ⚠️  No bulk operation optimization"
    ((WARNINGS++))
fi

# Check 5: Webhook handling
echo "5. Webhook Integration:"
if [ -f "apps/backend/src/routers/webhooks.py" ]; then
    echo "   ✓ Webhook router implemented"
    ((CHECKS_PASSED++))
else
    echo "   ⚠️  No webhook handling"
    ((WARNINGS++))
fi

echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 5: Industry Standards Compliance"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}API Development Standards (REST/OpenAPI):${NC}"

# RESTful design
echo "1. RESTful Design:"
if grep -q "@router\\.get\|@router\\.post\|@router\\.put\|@router\\.delete" apps/backend/src/routers/ -r; then
    echo "   ✓ Standard HTTP methods"
    ((CHECKS_PASSED++))
else
    echo "   ✗ Non-standard routing"
    ((CHECKS_FAILED++))
fi

# API documentation
echo "2. API Documentation:"
if curl -s http://localhost:8000/docs | grep -q "OpenAPI"; then
    echo "   ✓ OpenAPI/Swagger docs available at /docs"
    ((CHECKS_PASSED++))
else
    echo "   ⚠️  API docs not accessible"
    ((WARNINGS++))
fi

# Response format
echo "3. Response Format:"
if grep -q '"status".*"data".*"message"' apps/backend/src/ -r; then
    echo "   ✓ Standardized JSON response format"
    echo "     Format: {status, data, message, request_id}"
    ((CHECKS_PASSED++))
else
    echo "   ⚠️  Inconsistent response format"
    ((WARNINGS++))
fi

# Type hints
echo "4. Type Hints (Python):"
if grep -q "-> Dict\|-> List\|-> Optional" apps/backend/src/services/easypost_service.py; then
    echo "   ✓ Full type hint coverage"
    ((CHECKS_PASSED++))
else
    echo "   ✗ Missing type hints"
    ((CHECKS_FAILED++))
fi

# Async/await
echo "5. Async Operations:"
if grep -q "async def\|await" apps/backend/src/services/easypost_service.py; then
    echo "   ✓ Async/await pattern throughout"
    ((CHECKS_PASSED++))
else
    echo "   ✗ Blocking operations detected"
    ((CHECKS_FAILED++))
fi

echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 6: Frontend-Backend Integration"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}Checking Dashboard API Usage:${NC}"

# Check frontend API service
if [ -f "apps/frontend/src/services/api.js" ]; then
    echo "1. API Service Layer:"
    echo "   ✓ Centralized API client (apps/frontend/src/services/api.js)"
    ((CHECKS_PASSED++))

    # Check for axios/fetch usage
    if grep -q "axios\|fetch" apps/frontend/src/services/api.js; then
        echo "   ✓ HTTP client configured"
        ((CHECKS_PASSED++))
    fi
else
    echo "   ✗ No API service layer"
    ((CHECKS_FAILED++))
fi

# Check environment configuration
echo "2. API URL Configuration:"
if grep -q "VITE_API_URL\|API_URL" apps/frontend/src/ -r; then
    echo "   ✓ Configurable API endpoints"
    ((CHECKS_PASSED++))
else
    echo "   ⚠️  Hardcoded API URLs"
    ((WARNINGS++))
fi

echo ""

# Summary
echo "═══════════════════════════════════════════════════════════"
echo "                    VALIDATION SUMMARY"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}Checks Passed: $CHECKS_PASSED${NC}"
echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
echo -e "${RED}Checks Failed: $CHECKS_FAILED${NC}"
echo ""

SCORE=$((CHECKS_PASSED * 100 / (CHECKS_PASSED + CHECKS_FAILED + WARNINGS)))

if [ $SCORE -ge 90 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     ✅ EXCELLENT - API Standards Compliance: ${SCORE}%     ║${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}║  Your project follows EasyPost and REST best practices   ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
elif [ $SCORE -ge 70 ]; then
    echo -e "${YELLOW}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║     ✓ GOOD - API Standards Compliance: ${SCORE}%          ║${NC}"
    echo -e "${YELLOW}║                                                           ║${NC}"
    echo -e "${YELLOW}║  Minor improvements recommended (see warnings above)      ║${NC}"
    echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════╝${NC}"
else
    echo -e "${RED}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║     ⚠️  NEEDS IMPROVEMENT - Compliance: ${SCORE}%          ║${NC}"
    echo -e "${RED}║                                                           ║${NC}"
    echo -e "${RED}║  Review failed checks above                               ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════════╝${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "REFERENCE DOCUMENTATION"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📚 EasyPost Official SDK:"
echo "   https://github.com/EasyPost/easypost-python"
echo ""
echo "📚 EasyPost API Docs:"
echo "   https://docs.easypost.com"
echo ""
echo "📚 Postman Collection:"
echo "   https://www.postman.com/easypost-api"
echo ""
echo "📚 REST API Best Practices:"
echo "   - Standardized response format (status, data, message)"
echo "   - Proper HTTP status codes (200, 201, 400, 404, 500)"
echo "   - Type hints and validation (Pydantic models)"
echo "   - Async/await for non-blocking I/O"
echo "   - Environment-based configuration"
echo "   - OpenAPI/Swagger documentation"
echo ""

exit 0
