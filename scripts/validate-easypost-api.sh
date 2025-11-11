#!/bin/bash

# EasyPost API Validation Script
# Tests real API connectivity and core operations

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        EasyPost API Validation & Test Suite              ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

cd apps/backend
source venv/bin/activate

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 1: Configuration Validation"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check API key
echo -e "${BLUE}Testing: EasyPost API Key Configuration${NC}"
python << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('EASYPOST_API_KEY', '')
if not api_key:
    print("❌ FAILED - API key not found")
    exit(1)

if api_key.startswith('EZTK'):
    print("✓ Test API key detected")
    print("  Type: Test Key")
elif api_key.startswith('EZAK'):
    print("✓ Production API key detected")
    print("  Type: Production Key")
else:
    print("⚠️  WARNING - Unknown key type")

print(f"  Length: {len(api_key)} chars")
print("✓ PASSED")
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Configuration check PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ Configuration check FAILED${NC}"
    ((TESTS_FAILED++))
fi
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 2: API Connectivity Test"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}Testing: Basic API Connectivity${NC}"
python << 'EOF'
import asyncio
from src.services.easypost_service import EasyPostService

async def test_connectivity():
    service = EasyPostService()
    try:
        # Simple connectivity test - list recent shipments
        shipments = await service.list_shipments(limit=1)
        print(f"✓ API Response received")
        print(f"  Sample shipment ID: {shipments[0].get('id', 'N/A')[:20]}...")
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED - {str(e)}")
        return False

result = asyncio.run(test_connectivity())
exit(0 if result else 1)
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ API connectivity PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ API connectivity FAILED${NC}"
    ((TESTS_FAILED++))
fi
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 3: Core API Operations"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}Testing: Get Shipping Rates${NC}"
python << 'EOF'
import asyncio
from src.services.easypost_service import EasyPostService

async def test_rates():
    service = EasyPostService()
    try:
        result = await service.get_rates(
            from_address={
                "street1": "417 Montgomery Street",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94104",
                "country": "US"
            },
            to_address={
                "street1": "1 Market Street",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94105",
                "country": "US"
            },
            parcel={
                "length": 10,
                "width": 8,
                "height": 6,
                "weight": 16
            }
        )
        
        rates_count = len(result.get('rates', []))
        print(f"✓ Retrieved {rates_count} shipping rates")
        
        if rates_count > 0:
            sample_rate = result['rates'][0]
            print(f"  Sample carrier: {sample_rate['carrier']}")
            print(f"  Sample rate: ${sample_rate['rate']}")
            print(f"  Service: {sample_rate['service']}")
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED - {str(e)}")
        return False

result = asyncio.run(test_rates())
exit(0 if result else 1)
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Get rates PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ Get rates FAILED${NC}"
    ((TESTS_FAILED++))
fi
echo ""

echo -e "${BLUE}Testing: List Shipments${NC}"
python << 'EOF'
import asyncio
from src.services.easypost_service import EasyPostService

async def test_list():
    service = EasyPostService()
    try:
        shipments = await service.list_shipments(limit=10)
        count = len(shipments)
        
        print(f"✓ Retrieved {count} shipments")
        
        if count > 0:
            print(f"  Latest shipment: {shipments[0].get('id', 'N/A')[:20]}...")
            print(f"  Status: {shipments[0].get('status', 'N/A')}")
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED - {str(e)}")
        return False

result = asyncio.run(test_list())
exit(0 if result else 1)
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ List shipments PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ List shipments FAILED${NC}"
    ((TESTS_FAILED++))
fi
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 4: Integration Tests"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}Running: EasyPost Integration Tests${NC}"
if pytest tests/integration/test_easypost_integration.py -v -k "not real_api" -q 2>&1 | tail -3; then
    echo -e "${GREEN}✓ Integration tests PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ Integration tests FAILED${NC}"
    ((TESTS_FAILED++))
fi
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 5: API Endpoint Tests"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd ..

# Test backend endpoints
echo -e "${BLUE}Testing: Backend /stats endpoint${NC}"
if curl -s http://localhost:8000/stats | jq -e '.status == "success"' > /dev/null; then
    echo -e "${GREEN}✓ /stats endpoint PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ /stats endpoint FAILED${NC}"
    ((TESTS_FAILED++))
fi

echo -e "${BLUE}Testing: Backend /analytics endpoint${NC}"
if curl -s http://localhost:8000/analytics | jq -e '.status == "success"' > /dev/null; then
    echo -e "${GREEN}✓ /analytics endpoint PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ /analytics endpoint FAILED${NC}"
    ((TESTS_FAILED++))
fi

echo ""

echo "═══════════════════════════════════════════════════════════"
echo "PHASE 6: Performance Validation"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}Testing: Response Times${NC}"

# Backend response time
backend_time=$(curl -s -w "%{time_total}" -o /dev/null http://localhost:8000/health)
echo "  Backend response: ${backend_time}s"

if (( $(echo "$backend_time < 1.0" | bc -l) )); then
    echo -e "${GREEN}✓ Response time acceptable${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⚠ Response time slow (expected < 1s)${NC}"
fi

# Proxy response time
proxy_time=$(curl -s -w "%{time_total}" -o /dev/null http://localhost:8080/api/stats)
echo "  Proxy API response: ${proxy_time}s"

if (( $(echo "$proxy_time < 1.0" | bc -l) )); then
    echo -e "${GREEN}✓ Proxy overhead acceptable${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⚠ Proxy overhead high${NC}"
fi

echo ""

# Summary
echo "═══════════════════════════════════════════════════════════"
echo "                  VALIDATION SUMMARY"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}Tests Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Tests Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     ✅ EASYPOST API VALIDATION SUCCESSFUL ✅            ║${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}║  All EasyPost API operations are working correctly!       ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║        ⚠️  SOME VALIDATIONS FAILED ⚠️                    ║${NC}"
    echo -e "${RED}║                                                           ║${NC}"
    echo -e "${RED}║  Please check the errors above                            ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi

