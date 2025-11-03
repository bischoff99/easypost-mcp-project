---
name: explain
category: context
description: Deep explanation of code with reasoning chain using Sequential Thinking
allowed-tools: [Read, Grep, codebase_search, mcp_sequential-thinking_sequentialthinking, mcp_context7_get-library-docs]
requires-approval: false
context-aware: true
arguments:
  - name: target
    type: string
    required: false
    default: "@selection || @file"
    description: What to explain (file path, @selection, @function)
  - name: depth
    type: string
    required: false
    default: "detailed"
    enum: ["brief", "detailed", "comprehensive"]
    description: Explanation depth level
estimated-time: 5-10s
estimated-tokens: 1500-3000
m3-max-optimized: false
version: 2.0
---

# /context:explain

Deep, reasoning-based explanation of code using Sequential Thinking MCP. Goes beyond surface-level descriptions to explain why code works, potential issues, and architectural context.

## Usage

```bash
# Explain selected code
/context:explain @selection

# Explain current file
/context:explain @file

# Explain specific function
/context:explain calculateShippingRate

# Brief explanation
/context:explain @selection --brief

# Comprehensive with architecture
/context:explain @file --comprehensive
```

## Explanation Levels

### Brief (~500 tokens, 5s)
- What it does
- Key functions/classes
- One-line purpose

### Detailed (~2000 tokens, 7s) **DEFAULT**
- What it does + why
- How it works (logic flow)
- Dependencies and relationships
- Potential issues
- Performance considerations

### Comprehensive (~3000+ tokens, 10s)
- Everything in Detailed +
- Architectural context
- Design patterns used
- Alternative approaches
- Testing recommendations
- Performance deep-dive

## Sequential Thinking Analysis

Uses `mcp_sequential-thinking` for deep reasoning:

```
User: /context:explain @selection

AI: Analyzing selected code with Sequential Thinking...

Thought 1/8: Identifying code purpose
→ This is a rate calculation function for shipping

Thought 2/8: Analyzing input parameters
→ Takes weight, destination, service_type
→ All required, no defaults

Thought 3/8: Examining logic flow
→ Step 1: Validates input ranges
→ Step 2: Queries carrier APIs in parallel
→ Step 3: Applies business rules
→ Step 4: Returns sorted rates

Thought 4/8: Checking error handling
→ Good: Validates inputs upfront
→ Issue: No timeout on API calls
→ Missing: Retry logic for API failures

Thought 5/8: Performance analysis
→ Parallel API calls: Good (uses asyncio.gather)
→ No caching: Could cache by weight/destination
→ O(n) sorting: Acceptable for small n (<100 rates)

Thought 6/8: Dependencies identified
→ Uses EasyPost API
→ Depends on rate_calculator module
→ Database session for audit logging

Thought 7/8: Testing gaps
→ Missing: Edge case tests (zero weight, invalid dest)
→ Missing: Performance test (>1000 rates)
→ Good: Has unit tests for happy path

Thought 8/8: Recommendations
→ Add API call timeouts (suggest: 5s)
→ Implement caching layer (LRU, 10K entries)
→ Add retry logic (3 attempts, exponential backoff)
→ Expand test coverage to 85%+

Generating comprehensive explanation...
```

## Example Output

### Input Code
```python
async def calculate_shipping_rates(
    weight: float,
    destination: str,
    service_type: str = "ground"
) -> List[Rate]:
    rates = await asyncio.gather(*[
        carrier.get_rate(weight, destination, service_type)
        for carrier in CARRIERS
    ])
    return sorted(rates, key=lambda r: r.price)
```

### Detailed Explanation
```markdown
## Purpose
Calculates shipping rates from multiple carriers concurrently
and returns them sorted by price ascending.

## How It Works

1. **Input Validation** (implicit via type hints):
   - weight: float (grams or ounces based on config)
   - destination: str (zip code, postal code, or full address)
   - service_type: str (defaults to "ground")

2. **Parallel API Calls** (asyncio.gather):
   Queries all configured carriers simultaneously for rates.
   Configured carriers in CARRIERS constant (line 12).
   Uses asyncio for non-blocking I/O.

3. **Sorting**:
   Returns rates sorted by price (cheapest first).
   Uses lambda function for clean syntax.

## Dependencies

- **CARRIERS**: Module-level constant (imported from config)
- **asyncio**: Python standard library for async operations
- **Rate**: Data model from models.shipping
- **carrier.get_rate()**: Each carrier implements this interface

## Potential Issues

⚠️ **No timeout**: API calls could hang indefinitely
   Fix: Add timeout to asyncio.gather()
   ```python
   rates = await asyncio.wait_for(
       asyncio.gather(*[...]),
       timeout=5.0
   )
   ```

⚠️ **No error handling**: If one carrier fails, entire function fails
   Fix: Use return_exceptions=True in gather()
   ```python
   results = await asyncio.gather(*[...], return_exceptions=True)
   rates = [r for r in results if not isinstance(r, Exception)]
   ```

⚠️ **No caching**: Repeated calls for same parameters hit APIs
   Fix: Add LRU cache with TTL
   ```python
   @lru_cache(maxsize=1000, ttl=300)  # 5 min cache
   ```

## Performance

**Current**: O(n) where n = number of carriers
- Parallel calls: Good (not sequential)
- Sorting: O(n log n) but n typically <10 carriers

**Optimization Opportunities**:
1. Cache results (5-10x faster for repeated queries)
2. Stream results as they arrive (lower perceived latency)
3. Circuit breaker for failing carriers

## Architectural Context

Located in: `backend/src/services/shipping.py`
Called by: RateComparisonTool (MCP), ShippingController (API)
Related: CarrierService, RateCalculator, ShipmentService

**Design Pattern**: Strategy pattern
- Each carrier implements get_rate() interface
- Easy to add new carriers without changing this function

## Testing Recommendations

```python
# Edge cases to test
test_zero_weight()           # Should handle or raise clear error
test_invalid_destination()   # Should validate format
test_all_carriers_fail()     # Should not crash, return empty or error
test_partial_carrier_failure()  # Should return available rates
test_timeout_scenario()      # Should not hang forever

# Performance tests
test_100_parallel_calls()    # Verify no degradation
test_cache_effectiveness()   # Measure hit rate
```

## Recommended Changes

1. **Add timeout** (critical):
   ```python
   rates = await asyncio.wait_for(gather_call, timeout=5.0)
   ```

2. **Handle failures gracefully** (high):
   ```python
   results = await asyncio.gather(*calls, return_exceptions=True)
   rates = [r for r in results if isinstance(r, Rate)]
   if not rates:
       logger.warning("All carriers failed")
       raise NoRatesAvailable()
   ```

3. **Add caching** (medium):
   ```python
   @cached(ttl=300, key=lambda w,d,s: f"{w}:{d}:{s}")
   async def calculate_shipping_rates(...):
   ```

4. **Stream results** (low, UX improvement):
   ```python
   async for rate in stream_carrier_rates(...)
       yield rate  # Return rates as they arrive
   ```
```

## Context Variable Examples

### Explain Selection
```bash
# Select function in editor
/context:explain @selection

# Quick summary
What: Rate calculator
Why: Compare shipping costs
How: Async API calls, parallel
```

### Explain File
```bash
/context:explain @file

# Analyzes entire file
# Shows file purpose
# Lists all functions/classes
# Explains relationships
```

### Explain with Git Context
```bash
/context:explain @git-diff

# Explains recent changes
# Shows what changed and why
# Impact analysis
```

## Integration with Other MCPs

### Context7 Integration
```bash
/context:explain @selection

# AI checks Context7 for framework best practices
# Compares your code to recommended patterns
# Suggests improvements based on latest docs
```

### Codebase Search Integration
```bash
/context:explain calculate_rate

# AI searches entire codebase for:
# - Where function is called
# - Similar functions
# - Related utilities
# - Test coverage
```

## Smart Features

### Auto-Context Detection
```bash
# No argument? AI chooses best context:
/context:explain

Priority:
1. @selection (if code selected)
2. @errors (if errors visible)
3. @file (current file)
4. Prompts for target
```

### Architectural Awareness
```
AI knows project structure from .dev-config.json:
- FastAPI backend → Explains async patterns
- React frontend → Explains hooks, state
- Microservices → Explains service boundaries
```

### Example-Driven
```
AI provides runnable examples:
- How to use function
- How to test it
- How to improve it
```

## Use Cases

### 1. Understanding Legacy Code
```bash
# Inherited unfamiliar codebase
/context:explain backend/legacy/complex_algorithm.py --comprehensive

# Get architectural context, dependencies, risks
```

### 2. Code Review Preparation
```bash
# Before reviewing PR
/context:explain @git-diff --detailed

# Understand changes and their impact
```

### 3. Learning Project Patterns
```bash
# New to project, want to learn patterns
/context:explain backend/src/services/ --comprehensive

# See how services are structured
```

### 4. Debugging Complex Issues
```bash
# Bug in unfamiliar code
/context:explain @selection --comprehensive

# Deep dive into logic, find issues
```

## Performance

| Target | Tokens | Time | Workers |
|--------|--------|------|---------|
| @selection (10-50 lines) | 1500 | 5s | 4 |
| @file (<500 lines) | 2500 | 7s | 8 |
| @file (>500 lines) | 3000 | 10s | 12 |
| --comprehensive | 4000+ | 12s | 16 |

## Output Formats

### Markdown (default)
```bash
/context:explain @selection
# Formatted markdown with sections
```

### JSON (for tooling)
```bash
/context:explain @selection --format json
{
  "purpose": "...",
  "logic_flow": [...],
  "issues": [...],
  "recommendations": [...]
}
```

### Inline Comments
```bash
/context:explain @selection --format comments
# Adds explanation as code comments
```

## Best Practices

✅ **Start with @selection** - Explain specific unclear sections
✅ **Use --brief for quick checks** - Fast overview
✅ **Use --comprehensive for learning** - Deep understanding
✅ **Chain with /quality:fix** - Explain → Fix → Test
✅ **Save explanations** - Use for documentation

## Related Commands

- `/context:improve` - Explain + suggest improvements
- `/context:doc` - Explain + generate documentation
- `/quality:refactor` - Explain + refactor
- `/test:mock` - Explain + generate test mocks

## Tips

1. **Select specific code** - More focused explanations
2. **Use for learning** - Great for understanding patterns
3. **Check before modifying** - Understand before changing
4. **Compare approaches** - Explain old vs new code
5. **Generate docs** - Use explanation as doc foundation

