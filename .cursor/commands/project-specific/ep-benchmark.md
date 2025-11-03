Run EasyPost performance benchmarks (M3 Max validation).

**Domain**: Performance testing
**Performance**: Validates M3 Max optimizations

## Usage

```bash
# Run all benchmarks
/ep-benchmark

# Specific benchmark
/ep-benchmark bulk-creation
/ep-benchmark tracking
/ep-benchmark analytics
/ep-benchmark parsing

# Compare with baseline
/ep-benchmark --compare

# Export results
/ep-benchmark --export=json
```

## What It Does

**Performance Validation:**
1. Runs benchmark tests from `test_bulk_performance.py`
2. Measures sequential vs parallel performance
3. Calculates speedup ratios
4. Validates M3 Max optimizations working
5. Generates performance report

## Benchmarks

### 1. Bulk Shipment Creation
**Test**: Sequential vs 16 parallel workers
**Expected**: >5x speedup
**Validates**: ThreadPoolExecutor, asyncio.gather()

### 2. Batch Tracking
**Test**: Sequential vs 16 parallel tracking calls
**Expected**: >8x speedup
**Validates**: Parallel API calls

### 3. Analytics Processing
**Test**: Sequential vs 16-chunk parallel aggregation
**Expected**: 5x+ speedup
**Validates**: asyncio.gather() for CPU tasks

### 4. Parsing Performance
**Test**: 1000 iterations of parsing functions
**Expected**: <1s total
**Validates**: Parsing efficiency

## MCP Integration

**Server**: Desktop Commander
**Tool**: `start_process` with pytest

**Execution**:
```bash
cd backend
source venv/bin/activate
python tests/integration/test_bulk_performance.py
```

## Output Format

```
╔═══════════════════════════════════════════════════════════╗
║       EASYPOST PERFORMANCE BENCHMARKS (M3 Max)           ║
╚═══════════════════════════════════════════════════════════╝

Hardware: M3 Max (16 cores, 128GB RAM)
Workers: 16 parallel (pytest-xdist)

Running benchmarks...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BULK SHIPMENT CREATION BENCHMARK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Shipments: 10
Sequential: 1.05s (9.5 shipments/s)
Parallel:   0.11s (90.9 shipments/s)
Speedup:    9.5x ✅

Target: >5x | Achieved: 9.5x | Status: PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BATCH TRACKING BENCHMARK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Packages: 50
Sequential: 2.51s (19.9 packages/s)
Parallel:   0.28s (178.6 packages/s)
Speedup:    9.0x ✅

Target: >8x | Achieved: 9.0x | Status: PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANALYTICS PROCESSING BENCHMARK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Shipments: 10000
Sequential: 45.2ms (221,238 shipments/s)
Parallel:   8.7ms (1,149,425 shipments/s)
Speedup:    5.2x ✅

Target: >1x | Achieved: 5.2x | Status: PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARSING PERFORMANCE BENCHMARK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Iterations: 1000
parse_spreadsheet_line: 24.15ms (41,406/s) ✅
parse_dimensions:       6.82ms (146,628/s) ✅
parse_weight:           5.43ms (184,162/s) ✅
Total:                  36.40ms (27,472/s) ✅

Target: <1000ms | Achieved: 36ms | Status: PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ BENCHMARK SUMMARY

All benchmarks: PASSED (4/4)
Total duration: 3.8s

Performance Gains:
  Bulk Creation:   9.5x faster (16 workers)
  Batch Tracking:  9.0x faster (16 workers)
  Analytics:       5.2x faster (16 chunks)
  Parsing:         Fast (36ms/1000 iterations)

M3 Max Utilization: OPTIMAL ✅

Recommendations:
  ✓ Parallel processing working as expected
  ✓ ThreadPoolExecutor configured correctly
  ✓ asyncio.gather() providing speedup
  ✓ No bottlenecks detected
```

## Baseline Comparison

With `--compare` flag:

```
📊 COMPARISON WITH BASELINE

Benchmark              Current   Baseline   Change
─────────────────────  ────────  ─────────  ──────
Bulk Creation (10)     0.11s     0.12s      +8%
Batch Tracking (50)    0.28s     0.30s      +7%
Analytics (10000)      8.7ms     9.2ms      +5%
Parsing (1000)         36.4ms    38.1ms     +4%

Overall Performance: +6% improvement ⬆️

Last baseline: 2025-11-02 14:30:00
```

## Export Results

**JSON Export** (`--export=json`):
```json
{
  "timestamp": "2025-11-03T17:30:00Z",
  "hardware": {
    "model": "M3 Max",
    "cores": 16,
    "ram": "128GB"
  },
  "benchmarks": {
    "bulk_creation": {
      "shipments": 10,
      "sequential": 1.05,
      "parallel": 0.11,
      "speedup": 9.5,
      "target": 5.0,
      "pass": true
    },
    "batch_tracking": {
      "packages": 50,
      "sequential": 2.51,
      "parallel": 0.28,
      "speedup": 9.0,
      "target": 8.0,
      "pass": true
    }
  }
}
```

## Performance Regression Detection

Automatically detects if performance degrades:

```
⚠️ PERFORMANCE REGRESSION DETECTED

Benchmark: Bulk Creation
Expected: >5x speedup
Actual: 3.2x speedup

Possible causes:
  - ThreadPoolExecutor workers reduced
  - Async code made synchronous
  - GIL contention introduced
  - CPU throttling active

Run with --debug for detailed analysis
```

## Related Commands

```bash
/ep-benchmark          # Run benchmarks (this)
/ep-test               # Run all tests
/ep-dev                # Start dev environment
/clean                 # Clean build artifacts
```

**Validate M3 Max optimizations - prove the speedup!**

