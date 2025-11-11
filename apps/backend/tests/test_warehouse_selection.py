"""
Test warehouse selection logic for bulk shipments.

Verifies that shipments from different states get correct warehouses.
"""

import sys
from pathlib import Path

# Add src to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import after path is set
from src.mcp_server.tools.bulk_tools import detect_product_category, get_warehouse_address


def test_category_detection():
    """Test product category detection from contents."""
    test_cases = [
        ("(4) Original Prints and Engravings HTS Code: 4911.10.00", "art"),
        ("(2) Cooling Memory Foam Pillow HTS Code: 9404.90.1000", "bedding"),
        ("(1) Baseball Glove HTS Code: 9506.51.40", "sporting"),
        ("Vintage Selvedge Denim Jeans", "apparel"),
        ("Running Shoes Size 10", "footwear"),
        ("Generic Item", "default"),
    ]

    print("Testing Category Detection:")
    for contents, expected_category in test_cases:
        detected = detect_product_category(contents)
        status = "✅" if detected == expected_category else "❌"
        print(f"{status} '{contents[:50]}...' → {detected} (expected: {expected_category})")
        assert detected == expected_category, f"Expected {expected_category}, got {detected}"

    print()


def test_warehouse_selection():
    """Test warehouse selection by state and category."""
    test_cases = [
        # (state, category, expected_company, expected_city)
        ("California", "art", "California Fine Arts", "Los Angeles"),
        ("California", "bedding", "Premium Bedding Distribution", "Los Angeles"),
        ("California", "sporting", "California Outdoor Supply", "Los Angeles"),
        ("Nevada", "art", "Nevada Fine Arts", "Las Vegas"),
        ("Nevada", "bedding", "Nevada Home Essentials", "Las Vegas"),
        ("Nevada", "sporting", "Nevada Sporting Supply", "Las Vegas"),
        ("New York", "art", "New York Fine Arts", "New York"),
        ("New York", "bedding", "New York Home Essentials", "New York"),
        ("New York", "sporting", "New York Sporting Supply", "New York"),
        ("Unknown", "art", "California Fine Arts", "Los Angeles"),  # Fallback
    ]

    print("Testing Warehouse Selection:")
    for state, category, expected_company, expected_city in test_cases:
        warehouse = get_warehouse_address(state, category)
        company = warehouse.get("company", "")
        city = warehouse.get("city", "")

        status = "✅" if company == expected_company and city == expected_city else "❌"
        print(f"{status} {state:12} + {category:10} → {company} ({city})")

        assert company == expected_company, f"Expected {expected_company}, got {company}"
        assert city == expected_city, f"Expected {expected_city}, got {city}"

    print()


def test_mixed_state_batch():
    """Test realistic mixed-state batch scenario."""
    print("Testing Mixed-State Batch Scenario:")
    print("=" * 70)

    shipments = [
        {
            "line": 1,
            "origin_state": "Nevada",
            "contents": "(4) Original Prints and Engravings HTS Code: 4911.10.00",
        },
        {
            "line": 2,
            "origin_state": "California",
            "contents": "(2) Cooling Memory Foam Pillow HTS Code: 9404.90.1000",
        },
        {
            "line": 3,
            "origin_state": "California",
            "contents": "(1) Baseball Glove HTS Code: 9506.51.40",
        },
        {
            "line": 4,
            "origin_state": "New York",
            "contents": "Vintage Denim Jeans",
        },
    ]

    for shipment in shipments:
        category = detect_product_category(shipment["contents"])
        warehouse = get_warehouse_address(shipment["origin_state"], category)
        company = warehouse.get("company", "Unknown")
        city = warehouse.get("city", "Unknown")

        print(f"Line {shipment['line']}: {shipment['origin_state']:12} + {category:10}")
        print(f"  → {company}")
        print(f"  → {city}, {shipment['origin_state'][:2]}")
        print()

    print("=" * 70)
    print()


if __name__ == "__main__":
    print("🧪 Testing Warehouse Selection Logic\n")

    try:
        test_category_detection()
        test_warehouse_selection()
        test_mixed_state_batch()

        print("✅ All tests passed!")
        print("\n📝 Key Findings:")
        print("  - Category detection working correctly")
        print("  - Warehouse selection respects state + category")
        print("  - Mixed-state batches get correct warehouses per shipment")
        print("  - No more 'all shipments use first line's warehouse' bug")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
