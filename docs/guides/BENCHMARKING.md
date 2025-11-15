# Performance Benchmarking Guide

This guide explains how to benchmark the EasyPost MCP project's performance and track improvements over time.

## Quick Start

Run the benchmark script:

```bash
make benchmark
# Or directly:
./scripts/benchmark.sh
```

## What Gets Benchmarked

### System Information
- CPU cores (physical and logical)
- Total memory
- Architecture (ARM64/x86_64)

### Backend Performance
- **ThreadPoolExecutor Workers**: Optimal worker count based on CPU cores
- **Uvicorn Workers**: Recommended worker configuration
- **Build Speed**: Python compilation time
- **Test Speed**: Parallel test execution time (pytest-xdist)

### Docker Performance
- **Build Speed**: Docker Compose parallel build time

## Expected Performance (M3 Max)

Based on 16-core M3 Max with 128GB RAM:

| Metric | Expected Value |
|--------|----------------|
| Backend startup | ~1.9x faster than single-threaded |
| MCP tool call | 1-3s including EasyPost latency |
| Test suite | ~5x faster with parallel execution |
| API requests/sec | ~5x higher throughput |
| Benchmark script | < 60s total runtime |

## Interpreting Results

### Backend Metrics

**ThreadPoolExecutor Workers**:
- Formula: `min(32, cpu_count * 2)`
- M3 Max (16 cores): 32 workers
- Optimal for I/O-bound operations

**Uvicorn Workers**:
- Formula: `(2 * cpu_count) + 1`
- M3 Max (16 cores): 33 workers
- Optimal for CPU-bound operations

**Test Speed**:
- Uses `pytest-xdist` with `-n auto`
- Automatically detects optimal worker count
- Compare against baseline: `pytest tests/ -n 1`

## Baseline Measurements

To establish a baseline, run benchmarks before optimizations:

```bash
# Save baseline results
./scripts/benchmark.sh > benchmarks/baseline-$(date +%Y%m%d).txt
```

## Performance Targets

### Backend & MCP
- **API Response Time**: < 100ms (p95) for lightweight endpoints
- **Test Suite**: < 2 minutes (all tests)
- **Build Time**: < 30 seconds
- **MCP Tool Turnaround**: < 3 seconds for single shipment flows

## Continuous Monitoring

### Integration with CI/CD

Add benchmark checks to CI pipeline:

```yaml
# .github/workflows/benchmark.yml
- name: Run benchmarks
  run: ./scripts/benchmark.sh
```

### Tracking Over Time

Create a `benchmarks/` directory to store historical results:

```bash
mkdir -p benchmarks
./scripts/benchmark.sh > benchmarks/$(date +%Y%m%d-%H%M%S).txt
```

## Troubleshooting

### Backend Tests Fail
- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Check pytest-xdist is installed: `pip install pytest-xdist`

### Docker Build Fails
- Ensure Docker is running: `docker ps`
- Check docker-compose version: `docker compose version`
- Review Dockerfile syntax

## Advanced Benchmarking

### Custom Benchmarks

Create custom benchmark scripts in `scripts/benchmarks/`:

```bash
# scripts/benchmarks/api_throughput.sh
ab -n 1000 -c 10 http://localhost:8000/health
```

### Profiling

Use profiling tools for deeper analysis:

**Backend**:
```bash
# Python profiling
python -m cProfile -o profile.stats src/server.py
```

## Related Documentation

- `.cursor/rules/05-m3-max-optimizations.mdc` - Hardware-specific optimizations
- `docs/architecture/OPTIMIZATION_SUMMARY.md` - Optimization details
- `Makefile` - Available benchmark commands

## Performance Tips

1. **Run benchmarks on clean system** - Close unnecessary applications
2. **Warm up before measuring** - Run tests once before timing
3. **Average multiple runs** - Run benchmarks 3-5 times and average
4. **Compare against baseline** - Always compare to previous measurements
5. **Monitor system resources** - Use Activity Monitor/Top during benchmarks

## Contributing

When adding new optimizations:
1. Run benchmark before changes
2. Implement optimization
3. Run benchmark after changes
4. Document improvement in commit message
5. Update this guide if new metrics are added
