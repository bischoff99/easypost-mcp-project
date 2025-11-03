Explain selected code using AI reasoning chain with MCP tools.

**Context-aware**: No arguments needed - automatically uses selected code in editor or current open file.

## How It Works

**Full MCP Reasoning Chain:**

**1. Sequential-thinking Analysis (10-15 thoughts)**
- Breaks down code logic step-by-step
- Identifies what each section does
- Traces data flow and dependencies
- Notes potential issues or optimizations

**2. Context7 Enhancement**
- Detects framework from imports
- Fetches official documentation
- Gets best practices and patterns
- Provides real-world examples

**3. Performance Analysis**
- Identifies bottlenecks
- Calculates complexity (Big O)
- Suggests M3 Max optimizations
- Compares with alternatives

**4. Architecture Context**
- Shows how code fits in project
- Maps dependencies and callers
- Explains design patterns used
- Suggests improvements

## What You Get

**Comprehensive Explanation:**
1. **What it does** (plain English)
2. **How it works** (step-by-step with Sequential-thinking)
3. **Why it's designed this way** (architectural context)
4. **Performance implications** (M3 Max optimization opportunities)
5. **Related code** (dependencies, callers)
6. **Best practices comparison** (Context7 framework docs)
7. **Improvement suggestions** (actionable recommendations)

## MCP Integration

**Stage 1 - Sequential Thinking**:
- Server: Sequential-thinking
- Thoughts: 10-15 steps
- Analyzes: Logic flow, edge cases, assumptions
- Output: Step-by-step breakdown

**Stage 2 - Framework Context**:
- Server: Context7
- Auto-detects: Framework from imports
  - `from fastapi import` → FastAPI docs
  - `import React` → React docs
  - `import gin` → Gin Go docs
- Topic: Auto-generated from code context
- Tokens: 3000-5000

**Stage 3 - Performance Analysis**:
- Identifies: O(n²) loops, blocking I/O
- Calculates: With M3 Max specs (16 cores, 128GB)
- Suggests: ThreadPool, async patterns, caching

**Stage 4 - Desktop Commander**:
- Finds: Related files and dependencies
- Maps: Call hierarchy
- Shows: Impact scope

## Auto-Detection

**Detects framework from code:**
```python
from fastapi import FastAPI    # → FastAPI
from django.http import        # → Django
const express = require        # → Express
import { useEffect } from      # → React
```

**Context7 libraries:**
- FastAPI: `/fastapi/fastapi`
- React: `/websites/react_dev`
- Django: `/django/django`
- Vue: `/vuejs/vue`
- Express: `/expressjs/express`
- Gin: `/gin-gonic/gin`

## Example Outputs

### Example 1: Explaining Backend Function

```bash
# Select this code in easypost_service.py:
async def create_shipment(self, to_address, from_address, parcel, carrier):
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            self.executor, self._create_shipment_sync, ...
        )
        return result
    except Exception as e:
        ...

# Run: /explain
```

**Output:**
```
🧠 Sequential-thinking Analysis (12 steps):

Step 1: Function creates shipping label via EasyPost API
Step 2: Uses async/await for non-blocking execution
Step 3: Offloads blocking I/O to ThreadPoolExecutor
Step 4: executor has 32 workers (M3 Max optimized)
Step 5: Calls synchronous _create_shipment_sync in thread
Step 6: await prevents blocking event loop
Step 7: Error handling catches all exceptions
Step 8: Returns standardized ShipmentResponse

Key insight: Hybrid async pattern - async wrapper around sync I/O

📚 Context7 - FastAPI Best Practices:
- Pattern: "Async wrapper + ThreadPoolExecutor" is recommended
- Use case: Wrapping synchronous SDK clients
- Performance: Allows concurrent request handling
- Alternative: Use httpx.AsyncClient if API supports

⚡ Performance Analysis (M3 Max):
- Current: 32 workers = optimal for 16 cores
- Throughput: 32 concurrent API calls
- Bottleneck: EasyPost API rate limits, not CPU
- Optimization: Already well-optimized for M3 Max

🏗️ Architecture Context:
- Called by: /api/shipments endpoint (server.py:110)
- Dependencies: easypost SDK, ThreadPoolExecutor
- Pattern: Service layer (good separation)
- Thread-safe: Yes (executor handles concurrency)

💡 Suggestions:
1. Add timeout to run_in_executor (prevent hanging)
2. Consider circuit breaker for API failures
3. Add retry logic with exponential backoff
4. Cache results for identical requests

🎯 Summary:
Well-designed async pattern that efficiently uses M3 Max's 16 cores
for parallel API calls. Main optimization opportunity is adding
resilience (retry, timeout, circuit breaker) rather than performance.
```

### Example 2: Explaining Frontend Component

```jsx
// Select in TrackingPage.jsx:
const [loading, setLoading] = useState(true);

useEffect(() => {
  const fetchDashboardData = async () => {
    const [statsResponse, recentResponse] = await Promise.all([
      shipmentAPI.getStats(),
      shipmentAPI.getRecentShipments(5),
    ]);
    setStats(statsResponse.data);
  };
  fetchDashboardData();
}, []);
```

**Output:**
```
🧠 Sequential-thinking Analysis (8 steps):

Step 1: Component fetches data on mount via useEffect
Step 2: Promise.all runs two API calls in parallel
Step 3: Destructures responses into variables
Step 4: Updates state with setStats()
Step 5: Empty dependency array [] = runs once on mount
Step 6: Loading state manages UI during fetch

Key insight: Parallel data fetching for better performance

📚 Context7 - React Best Practices:
- Pattern: "Parallel fetching with Promise.all"
- Recommended: Use React Query for caching
- Better: Extract to custom hook for reusability
- Example: useQuery() with staleTime for automatic caching

⚡ Performance Analysis:
- Parallel fetching: Good! Reduces load time 2x
- Missing: Request deduplication (both calls could cache)
- Missing: Error boundaries for failed fetches
- M3 Max: Browser can handle many parallel requests

💡 Suggestions:
1. Use React Query for automatic caching and retry
2. Extract to custom hook: useDashboardData()
3. Add error state handling
4. Add loading skeleton component
5. Consider SWR or TanStack Query

Example with React Query:
const { data: stats } = useQuery({
  queryKey: ['stats'],
  queryFn: shipmentAPI.getStats,
  staleTime: 30000
});
```

## Usage Examples

```bash
# Explain selected code (most common)
# 1. Select code in editor
# 2. Run:
/explain

# Explain entire open file
/explain

# Explain specific file
/explain backend/src/services/easypost_service.py

# Explain with focus
/explain --focus=performance
/explain --focus=security
/explain --focus=architecture
```

## Performance

- Sequential-thinking: 5-8s (10-15 thoughts)
- Context7 lookup: 2-4s (cached 24h)
- Analysis: 2-3s
- **Total: 10-15s** for comprehensive explanation

## Adapts To Any Language

Uses `.dev-config.json` to provide context:
- Language conventions
- Framework patterns
- Project architecture
- Performance targets (M3 Max specs)

**One command. Deep understanding. Any code.**

