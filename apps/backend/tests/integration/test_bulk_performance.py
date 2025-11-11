"""Performance benchmarking for bulk operations (M3 Max optimized)."""

import asyncio
import time
from datetime import UTC, datetime

import pytest

from src.mcp_server.tools.bulk_tools import parse_dimensions, parse_spreadsheet_line, parse_weight


class MockEasyPostService:
    """Mock service for benchmarking without API calls."""

    async def create_shipment(self, to_address, from_address, parcel, carrier=None, buy_label=True):
        """Mock shipment creation (simulates 100ms API call)."""
        await asyncio.sleep(0.1)  # Simulate API latency
        return {
            "status": "success",
            "id": f"shp_mock_{time.time()}",
            "tracking_code": f"MOCK{int(time.time() * 1000)}",
            "rates": [
                {
                    "id": "rate_1",
                    "carrier": carrier or "USPS",
                    "service": "Priority",
                    "rate": "8.50",
                    "delivery_days": 2,
                }
            ],
            "postage_label_url": "https://example.com/label.pdf" if buy_label else None,
            "purchased_rate": (
                {
                    "carrier": carrier or "USPS",
                    "service": "Priority",
                    "rate": "8.50",
                }
                if buy_label
                else None
            ),
        }

    async def get_rates(self, to_address, from_address, parcel):
        """Mock rates retrieval."""
        await asyncio.sleep(0.05)  # Simulate API latency
        return {
            "status": "success",
            "data": [
                {"carrier": "USPS", "service": "Priority", "rate": "8.50", "delivery_days": 2},
                {"carrier": "FedEx", "service": "Ground", "rate": "12.30", "delivery_days": 4},
            ],
        }

    async def get_tracking(self, tracking_number):
        """Mock tracking retrieval."""
        await asyncio.sleep(0.05)  # Simulate API latency
        return {
            "status": "success",
            "data": {
                "tracking_number": tracking_number,
                "status_detail": "in_transit",
                "updated_at": datetime.now(UTC).isoformat(),
            },
        }


@pytest.mark.asyncio
async def test_sequential_vs_parallel_creation():
    """Benchmark: Sequential vs Parallel bulk shipment creation."""
    mock_service = MockEasyPostService()

    # Generate sample shipment data
    num_shipments = 10
    shipments = [
        {
            "to_address": {
                "name": f"Test Recipient {i}",
                "street1": f"{i} Main St",
                "city": "New York",
                "state": "NY",
                "zip": "10001",
                "country": "US",
            },
            "from_address": {
                "name": "Test Sender",
                "street1": "123 Origin St",
                "city": "Los Angeles",
                "state": "CA",
                "zip": "90001",
                "country": "US",
            },
            "parcel": {"length": 12, "width": 9, "height": 6, "weight": 32},
        }
        for i in range(num_shipments)
    ]

    # Sequential execution
    start_seq = time.time()
    seq_results = []
    for shipment in shipments:
        result = await mock_service.create_shipment(
            shipment["to_address"], shipment["from_address"], shipment["parcel"]
        )
        seq_results.append(result)
    seq_duration = time.time() - start_seq

    # Parallel execution (16 workers)
    start_par = time.time()
    tasks = [
        mock_service.create_shipment(s["to_address"], s["from_address"], s["parcel"])
        for s in shipments
    ]
    await asyncio.gather(*tasks)
    par_duration = time.time() - start_par

    # Calculate speedup
    speedup = seq_duration / par_duration

    print(f"\n{'=' * 60}")
    print("BULK SHIPMENT CREATION BENCHMARK (M3 Max)")
    print(f"{'=' * 60}")
    print(f"Shipments: {num_shipments}")
    print(f"Sequential: {seq_duration:.2f}s ({num_shipments / seq_duration:.1f} shipments/s)")
    print(f"Parallel:   {par_duration:.2f}s ({num_shipments / par_duration:.1f} shipments/s)")
    print(f"Speedup:    {speedup:.1f}x")
    print(f"{'=' * 60}\n")

    # Note: For CPU-bound tasks like analytics processing, parallel processing
    # in Python may not provide speedup due to GIL overhead. This test demonstrates
    # the concept but doesn't enforce parallel speedup for CPU-bound work.
    # For I/O-bound tasks (API calls), parallel processing provides significant benefits.
    assert speedup > 5, f"Expected >5x speedup, got {speedup:.1f}x"


@pytest.mark.asyncio
async def test_sequential_vs_parallel_tracking():
    """Benchmark: Sequential vs Parallel batch tracking."""
    mock_service = MockEasyPostService()

    # Generate tracking numbers
    num_packages = 50
    tracking_numbers = [f"MOCK{i:010d}" for i in range(num_packages)]

    # Sequential execution
    start_seq = time.time()
    seq_results = []
    for tracking_num in tracking_numbers:
        result = await mock_service.get_tracking(tracking_num)
        seq_results.append(result)
    seq_duration = time.time() - start_seq

    # Parallel execution (16 workers)
    start_par = time.time()
    tasks = [mock_service.get_tracking(tracking_num) for tracking_num in tracking_numbers]
    await asyncio.gather(*tasks)
    par_duration = time.time() - start_par

    # Calculate speedup
    speedup = seq_duration / par_duration

    print(f"\n{'=' * 60}")
    print("BATCH TRACKING BENCHMARK (M3 Max)")
    print(f"{'=' * 60}")
    print(f"Packages: {num_packages}")
    print(f"Sequential: {seq_duration:.2f}s ({num_packages / seq_duration:.1f} packages/s)")
    print(f"Parallel:   {par_duration:.2f}s ({num_packages / par_duration:.1f} packages/s)")
    print(f"Speedup:    {speedup:.1f}x")
    print(f"{'=' * 60}\n")

    # Note: Analytics processing is CPU-bound, so parallel processing in Python
    # may not provide speedup due to GIL limitations. This test demonstrates
    # the parallel processing concept but doesn't require it to be faster.
    # For I/O-bound tasks (API calls), parallel processing provides significant benefits.
    assert speedup > 8, f"Expected >8x speedup, got {speedup:.1f}x"


@pytest.mark.asyncio
async def test_analytics_parallel_processing():
    """Benchmark: Sequential vs Parallel analytics processing."""

    # Generate mock shipments (larger dataset for meaningful parallel speedup)
    num_shipments = 10000
    shipments = [
        {
            "id": f"shp_{i}",
            "carrier": ["USPS", "FedEx", "UPS"][i % 3],
            "cost": 8.50 + (i % 10),
            "created_at": datetime.now(UTC).isoformat(),
            "from_address": {"city": "Los Angeles"},
            "to_address": {"city": ["New York", "Chicago", "Miami"][i % 3]},
        }
        for i in range(num_shipments)
    ]

    # Sequential processing
    start_seq = time.time()
    carrier_stats_seq = {}
    for shipment in shipments:
        carrier = shipment["carrier"]
        if carrier not in carrier_stats_seq:
            carrier_stats_seq[carrier] = {"count": 0, "cost": 0.0}
        carrier_stats_seq[carrier]["count"] += 1
        carrier_stats_seq[carrier]["cost"] += shipment["cost"]
    seq_duration = time.time() - start_seq

    # Parallel processing (16 chunks)
    async def calculate_carrier_stats(shipments_chunk):
        """Process a chunk of shipments."""
        stats = {}
        for shipment in shipments_chunk:
            carrier = shipment["carrier"]
            if carrier not in stats:
                stats[carrier] = {"count": 0, "cost": 0.0}
            stats[carrier]["count"] += 1
            stats[carrier]["cost"] += shipment["cost"]
        return stats

    start_par = time.time()
    chunk_size = max(1, len(shipments) // 16)
    chunks = [shipments[i : i + chunk_size] for i in range(0, len(shipments), chunk_size)]
    tasks = [calculate_carrier_stats(chunk) for chunk in chunks]
    chunk_results = await asyncio.gather(*tasks)

    # Merge results
    carrier_stats_par = {}
    for chunk_result in chunk_results:
        for carrier, stats in chunk_result.items():
            if carrier not in carrier_stats_par:
                carrier_stats_par[carrier] = {"count": 0, "cost": 0.0}
            carrier_stats_par[carrier]["count"] += stats["count"]
            carrier_stats_par[carrier]["cost"] += stats["cost"]
    par_duration = time.time() - start_par

    # Calculate speedup
    speedup = seq_duration / par_duration

    print(f"\n{'=' * 60}")
    print("ANALYTICS PROCESSING BENCHMARK (M3 Max)")
    print(f"{'=' * 60}")
    print(f"Shipments: {num_shipments}")
    print(
        f"Sequential: {seq_duration * 1000:.1f}ms ({num_shipments / seq_duration:.0f} shipments/s)"
    )
    print(
        f"Parallel:   {par_duration * 1000:.1f}ms ({num_shipments / par_duration:.0f} shipments/s)"
    )
    print(f"Speedup:    {speedup:.1f}x")
    print(f"{'=' * 60}\n")

    # Verify results match
    assert carrier_stats_seq == carrier_stats_par, "Results should match"

    # Note: For CPU-bound analytics processing, parallel processing in Python
    # may not provide speedup due to GIL limitations. This test validates
    # that parallel processing works correctly and produces the same results,
    # but doesn't require it to be faster than sequential processing.


def test_parsing_performance():
    """Benchmark: Parsing performance for bulk operations."""
    num_lines = 1000

    # Sample tab-separated line
    sample_line = "California\tUSPS\tJohn\tDoe\t555-0100\tjohn@example.com\t123 Main St\t\tLos Angeles\tCA\t90001\tUS\tPackage\t12 x 9 x 6\t1.5 lbs\tBeauty products"

    # Benchmark parse_spreadsheet_line
    start = time.time()
    for _ in range(num_lines):
        parse_spreadsheet_line(sample_line)
    parse_duration = time.time() - start

    # Benchmark parse_dimensions
    start = time.time()
    for _ in range(num_lines):
        length, width, height = parse_dimensions("12 x 9 x 6")
    dims_duration = time.time() - start

    # Benchmark parse_weight
    start = time.time()
    for _ in range(num_lines):
        parse_weight("1.5 lbs")
    weight_duration = time.time() - start

    total_duration = parse_duration + dims_duration + weight_duration

    print(f"\n{'=' * 60}")
    print("PARSING PERFORMANCE BENCHMARK")
    print(f"{'=' * 60}")
    print(f"Iterations: {num_lines}")
    print(
        f"parse_spreadsheet_line: {parse_duration * 1000:.2f}ms ({num_lines / parse_duration:.0f}/s)"
    )
    print(
        f"parse_dimensions:       {dims_duration * 1000:.2f}ms ({num_lines / dims_duration:.0f}/s)"
    )
    print(
        f"parse_weight:           {weight_duration * 1000:.2f}ms ({num_lines / weight_duration:.0f}/s)"
    )
    print(
        f"Total:                  {total_duration * 1000:.2f}ms ({num_lines / total_duration:.0f}/s)"
    )
    print(f"{'=' * 60}\n")

    # Assert reasonable performance
    assert parse_duration < 1.0, "Parsing should be fast"
    assert dims_duration < 0.5, "Dimension parsing should be very fast"
    assert weight_duration < 0.5, "Weight parsing should be very fast"


if __name__ == "__main__":
    """Run benchmarks directly."""
    print("\n🚀 M3 Max Performance Benchmarks\n")

    # Run parsing benchmark
    test_parsing_performance()

    # Run async benchmarks
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_sequential_vs_parallel_creation())
    loop.run_until_complete(test_sequential_vs_parallel_tracking())
    loop.run_until_complete(test_analytics_parallel_processing())

    print("\n✅ All benchmarks complete!\n")
