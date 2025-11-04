# EasyPost-Specific Workflows

Execute domain-specific workflow chains for shipping/logistics operations.

## Quick Reference

```bash
/workflow:ep-dev              # Start development (5s)
/workflow:ep-test             # Run tests 16 workers (6s)
/workflow:ep-test-all         # Unit + integration parallel (8s)
/workflow:ep-benchmark        # Performance benchmarks (15s)
/workflow:ep-mcp-tool         # Create MCP tool (30s)
/workflow:ep-bulk-test        # Test bulk operations (12s)
/workflow:ep-rate-check       # Verify rate accuracy (18s)
/workflow:ep-debug            # Debug API issues (20s)
/workflow:ep-optimize         # Optimize shipping ops (25s)
/workflow:ep-full             # Complete test suite (30s)
/workflow:ep-pre-release      # Release quality gate (60s)
/workflow:ep-parallel-test    # All tests parallel (8s)
```

## Detailed Workflows

### Development
```bash
/workflow:ep-dev
# Starts: Backend FastMCP server + React frontend
# Command: make dev
# Ports: 8000 (backend), 5173 (frontend)
```

### Testing
```bash
/workflow:ep-test
# Runs: pytest -n 16 backend/tests/
# Workers: 16 (M3 Max optimized)
# Time: ~6s

/workflow:ep-test-all
# Runs: Unit tests & Integration tests in parallel
# Command: /ep-test unit & /ep-test integration
# Time: ~8s (vs 14s sequential)

/workflow:ep-parallel-test
# Runs: All test suites simultaneously
# Command: /test backend/tests/unit & /test backend/tests/integration & /ep-benchmark
# Time: ~8s
```

### Performance
```bash
/workflow:ep-benchmark
# Runs: Performance benchmarks for bulk operations
# Tests: Parsing, creation, tracking, analytics
# Generates: Benchmark report with speedup metrics
# Time: ~15s

/workflow:ep-optimize
# Runs: Shipping operation optimization
# Command: /shipping-optimize && /ep-benchmark
# Time: ~25s
```

### Bulk Operations
```bash
/workflow:ep-bulk-test
# Tests: Bulk shipment creation + batch tracking
# Command: /bulk-create test-data.csv && /track-batch tracking-numbers.txt
# Time: ~12s

/workflow:ep-rate-check
# Tests: Rate comparison across carriers
# Command: /carrier-compare test-shipment && /analytics-deep rates
# Time: ~18s
```

### MCP Tool Development
```bash
/workflow:ep-mcp-tool <ModelName> <tool_name>
# Creates: Complete MCP tool with EasyPost patterns
# Generates: Model, tool function, tests, registration
# Command: /ep-mcp $1 $2 && /test backend/tests/
# Time: ~30s

# Example:
/workflow:ep-mcp-tool RefundRequest refund_shipment
```

### Debugging
```bash
/workflow:ep-debug
# Runs: Lint check → Integration tests → Error explanation
# Command: /ep-lint && /test integration || /explain @errors
# Time: ~20s
```

### Release Preparation
```bash
/workflow:ep-pre-release
# Runs: Complete quality gate for releases
# Steps:
#   1. Format code
#   2. Lint check
#   3. Full test suite with coverage
#   4. Performance benchmarks
#   5. Security audit
# Command: make format && make lint && /ep-test --coverage && /ep-benchmark && /secure backend/src/
# Time: ~60s
```

### Complete Suite
```bash
/workflow:ep-full
# Runs: All EasyPost functionality tests
# Command: /ep-test && /ep-benchmark && /bulk-create test && /track-batch test
# Time: ~30s
```

## Parallel Execution Examples

```bash
# Test all layers simultaneously
/test unit/ & /test integration/ & /ep-benchmark
# Time: 8s (vs 25s sequential)

# Generate multiple tools
/ep-mcp RefundRequest refund & /ep-mcp CustomsInfo customs
# Time: 30s (vs 60s sequential)

# Check multiple files
/optimize service.py & /optimize tools.py & /secure server.py
# Time: 15s (vs 45s sequential)
```

## Chaining Examples

```bash
# Development pipeline
/workflow:ep-dev && /workflow:ep-test

# Quality pipeline
/workflow:pre-commit && /workflow:ep-test-all

# Release pipeline
/workflow:full-check && /workflow:ep-pre-release

# Debug pipeline
/workflow:ep-test || /workflow:ep-debug
```

## M3 Max Performance

All workflows optimized for 16-core M3 Max:
- Parallel test execution (16 workers)
- Concurrent workflow steps (& operator)
- Optimized batch processing
- Cached results when possible

**Expected speedup: 4-9x vs sequential execution**

## Configuration

All workflows defined in `.dev-config.json` → `workflows.easypost`

Add custom workflows:
```json
{
  "workflows": {
    "easypost": {
      "my-workflow": {
        "description": "Custom workflow",
        "commands": "/command1 && /command2",
        "estimated_time": "20s",
        "category": "custom"
      }
    }
  }
}
```

**EasyPost workflows ready! Type `/workflow:ep-` to see all options.**
