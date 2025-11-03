#!/usr/bin/env python3
"""
Test script for MCP tools functionality.
Tests the EasyPost MCP server tools and resources.
"""

import asyncio
import json
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from backend.src.services.easypost_service import EasyPostService
from backend.src.utils.config import settings


async def test_mcp_tools():
    """Test MCP tools functionality."""
    print("🧪 Testing MCP Tools Functionality")
    print("=" * 50)

    # Initialize service
    try:
        service = EasyPostService(api_key=settings.EASYPOST_API_KEY)
        print("✅ EasyPost service initialized")
    except Exception as e:
        print(f"❌ Failed to initialize service: {e}")
        return

    # Test 1: Get shipments list
    print("\n📦 Testing get_shipments_list...")
    try:
        result = await service.get_shipments_list(page_size=5, purchased=True)
        if result["status"] == "success":
            print(f"✅ Shipments list retrieved: {len(result['data'])} shipments")
            if result["data"]:
                print(
                    f"   Sample shipment: {result['data'][0]['id']} - {result['data'][0]['status']}"
                )
        else:
            print(f"⚠️  Shipments list failed: {result['message']}")
    except Exception as e:
        print(f"❌ Shipments list error: {e}")

    # Test 2: Get rates (mock data since we don't want to create real shipments)
    print("\n💰 Testing get_rates...")
    try:
        mock_to_address = {
            "name": "Test Recipient",
            "street1": "123 Test St",
            "city": "Test City",
            "state": "CA",
            "zip": "90210",
            "country": "US",
        }
        mock_from_address = {
            "name": "Test Sender",
            "street1": "456 Sender Ave",
            "city": "Sender City",
            "state": "NY",
            "zip": "10001",
            "country": "US",
        }
        mock_parcel = {"length": 10.0, "width": 8.0, "height": 5.0, "weight": 2.0}

        result = await service.get_rates(
            mock_to_address, mock_from_address, mock_parcel
        )
        if result["status"] == "success":
            print(f"✅ Rates retrieved: {len(result['data'])} rate options")
            if result["data"]:
                print(
                    f"   Sample rate: {result['data'][0]['carrier']} - ${result['data'][0]['rate']}"
                )
        else:
            print(f"⚠️  Rates failed: {result['message']}")
    except Exception as e:
        print(f"❌ Rates error: {e}")

    # Test 3: Test tracking with a mock tracking number
    print("\n📍 Testing get_tracking...")
    try:
        # Use a test tracking number that should work in test mode
        test_tracking = "EZ1000000001"
        result = await service.get_tracking(test_tracking)
        if result["status"] == "success":
            print(f"✅ Tracking retrieved for {test_tracking}")
            if result.get("data"):
                print(f"   Status: {result['data'].get('status_detail', 'unknown')}")
        else:
            print(f"⚠️  Tracking failed: {result['message']}")
    except Exception as e:
        print(f"❌ Tracking error: {e}")

    print("\n🎉 MCP Tools Testing Complete!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
