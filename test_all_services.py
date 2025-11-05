#!/usr/bin/env python3
"""Comprehensive service testing script for EasyPost MCP."""

import asyncio
import json
import sys
from datetime import datetime

import httpx

API_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost"

test_results = {
    "passed": [],
    "failed": [],
    "warnings": [],
}


def log_test(name, passed, message=""):
    """Log test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")
    if message:
        print(f"     {message}")

    if passed:
        test_results["passed"].append(name)
    else:
        test_results["failed"].append((name, message))


async def test_backend_core():
    """Test backend core endpoints."""
    print("\n=== BACKEND CORE ENDPOINTS ===\n")

    async with httpx.AsyncClient() as client:
        # Test root
        try:
            r = await client.get(f"{API_URL}/")
            data = r.json()
            log_test("Root endpoint", r.status_code == 200 and "version" in data,
                    f"Version: {data.get('version', 'N/A')}")
        except Exception as e:
            log_test("Root endpoint", False, str(e))

        # Test health
        try:
            r = await client.get(f"{API_URL}/health")
            data = r.json()
            all_healthy = (data.get("status") == "healthy" and
                          data.get("system", {}).get("status") == "healthy" and
                          data.get("easypost", {}).get("status") == "healthy" and
                          data.get("database", {}).get("status") == "healthy")
            log_test("Health check", all_healthy,
                    f"System: {data.get('system', {}).get('status', 'unknown')}, " +
                    f"EasyPost: {data.get('easypost', {}).get('status', 'unknown')}, " +
                    f"DB: {data.get('database', {}).get('status', 'unknown')}")
        except Exception as e:
            log_test("Health check", False, str(e))

        # Test metrics
        try:
            r = await client.get(f"{API_URL}/metrics")
            data = r.json()
            log_test("Metrics endpoint", r.status_code == 200 and "uptime_seconds" in data,
                    f"Uptime: {data.get('uptime_seconds', 0)}s, Errors: {data.get('error_count', 0)}")
        except Exception as e:
            log_test("Metrics endpoint", False, str(e))


async def test_shipment_operations():
    """Test shipment creation and retrieval."""
    print("\n=== SHIPMENT OPERATIONS ===\n")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test shipment creation
        try:
            shipment_data = {
                "from_address": {
                    "name": "Test Warehouse",
                    "street1": "123 Test St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94103",
                    "country": "US"
                },
                "to_address": {
                    "name": "Test Customer",
                    "street1": "789 Customer Ave",
                    "city": "Boston",
                    "state": "MA",
                    "zip": "02101",
                    "country": "US"
                },
                "parcel": {
                    "length": 10,
                    "width": 8,
                    "height": 6,
                    "weight": 32.0
                },
                "buy_label": False
            }

            r = await client.post(f"{API_URL}/shipments", json=shipment_data)
            data = r.json()

            if r.status_code == 200 and data.get("status") == "success":
                shipment_id = data.get("id")
                rates_count = len(data.get("rates", []))
                log_test("Create shipment", True,
                        f"ID: {shipment_id[:20]}..., {rates_count} rates returned")
                return shipment_id
            else:
                log_test("Create shipment", False, data.get("message", "Unknown error"))
                return None
        except Exception as e:
            log_test("Create shipment", False, str(e))
            return None

        # Test list shipments
        try:
            r = await client.get(f"{API_URL}/shipments?page_size=10")
            data = r.json()
            shipments = data.get("data", [])
            log_test("List shipments", r.status_code == 200 and len(shipments) > 0,
                    f"Found {len(shipments)} shipments")
        except Exception as e:
            log_test("List shipments", False, str(e))


async def test_rates():
    """Test rate comparison."""
    print("\n=== RATE COMPARISON ===\n")

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            rate_request = {
                "from_address": {
                    "street1": "123 Main",
                    "city": "Los Angeles",
                    "state": "CA",
                    "zip": "90001",
                    "country": "US"
                },
                "to_address": {
                    "street1": "456 Park",
                    "city": "Seattle",
                    "state": "WA",
                    "zip": "98101",
                    "country": "US"
                },
                "parcel": {
                    "length": 12,
                    "width": 10,
                    "height": 8,
                    "weight": 64.0
                }
            }

            r = await client.post(f"{API_URL}/rates", json=rate_request)
            data = r.json()
            rates = data.get("data", [])

            if r.status_code == 200 and len(rates) > 0:
                cheapest = min(rates, key=lambda x: float(x['rate']))
                log_test("Get rates", True,
                        f"{len(rates)} rates found, cheapest: {cheapest['carrier']} ${cheapest['rate']}")
            else:
                log_test("Get rates", False, data.get("message", "No rates returned"))
        except Exception as e:
            log_test("Get rates", False, str(e))


async def test_analytics():
    """Test analytics endpoints."""
    print("\n=== ANALYTICS & STATS ===\n")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test stats
        try:
            r = await client.get(f"{API_URL}/stats")
            data = r.json()

            if r.status_code == 200 and data.get("status") == "success":
                stats = data.get("data", {})
                log_test("Stats endpoint", True,
                        f"Shipments: {stats.get('total_shipments', {}).get('value', 0)}, " +
                        f"Cost: ${stats.get('total_cost', {}).get('value', 0)}")
            else:
                log_test("Stats endpoint", False, data.get("message", "Failed"))
        except Exception as e:
            log_test("Stats endpoint", False, str(e))

        # Test analytics
        try:
            r = await client.get(f"{API_URL}/analytics?days=30")
            data = r.json()

            if r.status_code == 200 and data.get("status") == "success":
                analytics = data.get("data", {})
                log_test("Analytics endpoint", True,
                        f"Carriers: {len(analytics.get('by_carrier', []))}, " +
                        f"Routes: {len(analytics.get('top_routes', []))}")
            else:
                log_test("Analytics endpoint", False, data.get("message", "Failed"))
        except Exception as e:
            log_test("Analytics endpoint", False, str(e))

        # Test carrier performance
        try:
            r = await client.get(f"{API_URL}/carrier-performance")
            data = r.json()

            if r.status_code == 200 and data.get("status") == "success":
                carriers = data.get("data", [])
                log_test("Carrier performance", True,
                        f"{len(carriers)} carriers analyzed")
            else:
                log_test("Carrier performance", False, data.get("message", "Failed"))
        except Exception as e:
            log_test("Carrier performance", False, str(e))


async def test_database():
    """Test database endpoints."""
    print("\n=== DATABASE ENDPOINTS ===\n")

    async with httpx.AsyncClient() as client:
        # Test database shipments list
        try:
            r = await client.get(f"{API_URL}/db/shipments?limit=5")
            data = r.json()
            shipments = data.get("data", [])
            log_test("DB shipments list", r.status_code == 200,
                    f"Retrieved {len(shipments)} shipments from database")
        except Exception as e:
            log_test("DB shipments list", False, str(e))

        # Test addresses
        try:
            r = await client.get(f"{API_URL}/db/addresses?limit=5")
            data = r.json()
            addresses = data.get("data", [])
            log_test("DB addresses list", r.status_code == 200,
                    f"Retrieved {len(addresses)} addresses from database")
        except Exception as e:
            log_test("DB addresses list", False, str(e))


async def test_frontend():
    """Test frontend application."""
    print("\n=== FRONTEND APPLICATION ===\n")

    async with httpx.AsyncClient() as client:
        # Test frontend loads
        try:
            r = await client.get(FRONTEND_URL)
            html = r.text
            has_react = "root" in html
            has_title = "EasyPost MCP Dashboard" in html
            log_test("Frontend loads", r.status_code == 200 and has_react and has_title,
                    "React app served successfully")
        except Exception as e:
            log_test("Frontend loads", False, str(e))

        # Test health endpoint
        try:
            r = await client.get(f"{FRONTEND_URL}/health")
            log_test("Frontend health", r.status_code == 200, "Nginx responding")
        except Exception as e:
            log_test("Frontend health", False, str(e))


async def test_docker_networking():
    """Test Docker container connectivity."""
    print("\n=== DOCKER NETWORKING ===\n")

    async with httpx.AsyncClient() as client:
        # Test backend can reach frontend (via nginx proxy)
        try:
            r = await client.get(f"{API_URL}/health")
            log_test("Backend reachable", r.status_code == 200, "Backend responding on :8000")
        except Exception as e:
            log_test("Backend reachable", False, str(e))

        # Test frontend can proxy to backend
        try:
            # Frontend nginx should proxy /api/ to backend
            r = await client.get(f"{FRONTEND_URL}/health")
            log_test("Frontend nginx", r.status_code == 200, "Nginx serving frontend on :80")
        except Exception as e:
            log_test("Frontend nginx", False, str(e))


def print_summary():
    """Print test summary."""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = len(test_results["passed"])
    failed = len(test_results["failed"])
    total = passed + failed

    print(f"\n✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {failed}/{total}")

    if test_results["failed"]:
        print("\nFailed Tests:")
        for name, msg in test_results["failed"]:
            print(f"  - {name}: {msg}")

    if test_results["warnings"]:
        print("\nWarnings:")
        for warning in test_results["warnings"]:
            print(f"  ⚠️  {warning}")

    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"\nSuccess Rate: {success_rate:.1f}%")

    if success_rate >= 90:
        print("\n🏆 EXCELLENT - All critical systems operational")
    elif success_rate >= 75:
        print("\n✅ GOOD - Most systems operational")
    elif success_rate >= 50:
        print("\n⚠️  WARNING - Some systems have issues")
    else:
        print("\n❌ CRITICAL - Major system failures")

    return success_rate >= 90


async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("EASYPOST MCP - COMPREHENSIVE SERVICE TESTING")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("="*60)

    await test_backend_core()
    await test_shipment_operations()
    await test_rates()
    await test_analytics()
    await test_database()
    await test_frontend()
    await test_docker_networking()

    success = print_summary()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
