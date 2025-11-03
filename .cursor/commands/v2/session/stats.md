---
name: stats
category: session
description: Display detailed session analytics and performance metrics
allowed-tools: [Read]
requires-approval: false
context-aware: false
arguments:
  - name: export
    type: boolean
    required: false
    default: false
    description: Export metrics to JSON
estimated-time: <1s
estimated-tokens: 0
version: 2.0
---

# /session:stats

Comprehensive session analytics showing command usage patterns, performance metrics, cost tracking, and optimization recommendations.

## Usage

```bash
# View stats
/session:stats

# Export to file
/session:stats --export
```

## Output Example

```
📊 Session Analytics

Session Info:
├─ Started: 2025-11-03 09:15:00
├─ Duration: 2h 15m
├─ Commands: 47
└─ Status: Active

Token Usage:
├─ Input: 45,230 tokens
├─ Output: 12,450 tokens
├─ Total: 57,680 tokens
└─ Remaining: 142,320 tokens (71%)

Cost Analysis:
├─ Current: $0.87
├─ Projected: $1.20 (if session continues)
└─ Budget: $5.00 (17% used)

Performance:
├─ Avg Command Time: 8.4s
├─ Fastest: /test:run (4.2s)
├─ Slowest: /gen:crud (18.5s)
└─ M3 Max Usage: 68% (16 cores avg)

Command Breakdown:
├─ Code Generation: 15 (32%)
│   ├─ /gen:api: 6
│   ├─ /gen:component: 5
│   └─ /gen:crud: 4
├─ Testing: 18 (38%)
│   ├─ /test:run: 12
│   ├─ /test:coverage: 4
│   └─ /test:watch: 2
├─ Quality: 9 (19%)
│   ├─ /quality:fix: 5
│   ├─ /quality:optimize: 3
│   └─ /quality:refactor: 1
├─ Context: 3 (6%)
│   └─ /context:explain: 3
└─ Session: 2 (4%)
    ├─ /session:cost: 1
    └─ /session:checkpoint: 1

Context Variables Usage:
├─ @file: 23 times (most used)
├─ @selection: 12 times
├─ @git-diff: 8 times
├─ @errors: 5 times
└─ None: 9 times (auto-detect)

Success Rate:
├─ Successful: 44 (94%)
├─ Errors: 2 (4%)
└─ Cancelled: 1 (2%)

Optimization Opportunities:
⚠️  Consider using @selection more (saves 60% tokens)
✓  Good use of @git-diff for testing
⚠️  /gen:crud is expensive - use @selection where possible
✓  Excellent parallelization on /test:run
```

## Detailed Metrics

### Command History
```bash
/session:stats --history

Recent Commands (last 10):
┌────┬──────────────────┬────────┬─────────┬──────────┐
│ #  │ Command          │ Time   │ Tokens  │ Status   │
├────┼──────────────────┼────────┼─────────┼──────────┤
│ 47 │ /test:run        │ 4.2s   │ 1,200   │ ✓ Pass   │
│ 46 │ /quality:fix     │ 10.5s  │ 3,400   │ ✓ Pass   │
│ 45 │ /gen:component   │ 8.1s   │ 2,800   │ ✓ Pass   │
│ 44 │ /test:run        │ 4.1s   │ 1,150   │ ✓ Pass   │
│ 43 │ /context:explain │ 6.2s   │ 1,800   │ ✓ Pass   │
│ 42 │ /gen:api         │ 7.3s   │ 2,200   │ ✓ Pass   │
│ 41 │ /test:run        │ 4.3s   │ 1,220   │ ✗ Fail   │
│ 40 │ /quality:fix     │ 12.1s  │ 4,100   │ ✓ Pass   │
│ 39 │ /gen:crud        │ 18.5s  │ 6,500   │ ✓ Pass   │
│ 38 │ /test:coverage   │ 5.8s   │ 1,600   │ ✓ Pass   │
└────┴──────────────────┴────────┴─────────┴──────────┘
```

### Cost Breakdown by Category
```bash
/session:stats --costs

Cost Analysis by Category:
┌──────────────────┬──────────┬─────────┬───────┐
│ Category         │ Commands │ Tokens  │ Cost  │
├──────────────────┼──────────┼─────────┼───────┤
│ Code Generation  │ 15       │ 28,400  │ $0.43 │
│ Testing          │ 18       │ 15,200  │ $0.23 │
│ Quality          │ 9        │ 12,100  │ $0.18 │
│ Context          │ 3        │ 1,980   │ $0.03 │
│ Session          │ 2        │ 0       │ $0.00 │
├──────────────────┼──────────┼─────────┼───────┤
│ Total            │ 47       │ 57,680  │ $0.87 │
└──────────────────┴──────────┴─────────┴───────┘

Top 3 Most Expensive:
1. /gen:crud Product         $0.10 (6,500 tokens)
2. /gen:api /users POST      $0.05 (3,200 tokens)
3. /quality:fix @file        $0.06 (4,100 tokens)
```

### Performance Analysis
```bash
/session:stats --performance

Performance Metrics:
┌────────────────────┬─────────┬─────────┬─────────┐
│ Command            │ Avg     │ Min     │ Max     │
├────────────────────┼─────────┼─────────┼─────────┤
│ /test:run          │ 4.2s    │ 3.8s    │ 4.6s    │
│ /quality:fix       │ 11.3s   │ 10.5s   │ 12.1s   │
│ /gen:api           │ 7.5s    │ 7.0s    │ 8.2s    │
│ /gen:component     │ 8.4s    │ 7.8s    │  9.1s   │
│ /gen:crud          │ 17.2s   │ 16.5s   │ 18.5s   │
│ /context:explain   │ 6.8s    │ 6.2s    │ 7.5s    │
└────────────────────┴─────────┴─────────┴─────────┘

M3 Max Utilization:
├─ Average: 68% (10.9 cores)
├─ Peak: 95% (15.2 cores)
├─ /test:run: 100% (16 cores)
├─ /quality:fix: 75% (12 cores)
└─ /gen:api: 50% (8 cores)

Efficiency Score: 92/100
✓ Excellent parallelization
✓ Good context usage
⚠️ Consider /session:compact (context 71% full)
```

## Tracking Data

Metrics tracked per command:
- **Timestamp**: When command executed
- **Execution time**: Duration in milliseconds
- **Tokens**: Input, output, total
- **Cost**: Estimated in USD
- **Status**: Success, error, cancelled
- **Context**: Variables used, files modified
- **Hardware**: Workers, cores, execution tier

## Export Format

```bash
/session:stats --export

# Creates: .cursor/session-metrics-2025-11-03.json
```

```json
{
  "session": {
    "id": "sess_abc123",
    "started": "2025-11-03T09:15:00Z",
    "duration_minutes": 135,
    "total_commands": 47,
    "total_tokens": 57680,
    "total_cost": 0.87
  },
  "commands": [
    {
      "id": 47,
      "command": "/test:run",
      "category": "test",
      "timestamp": "2025-11-03T11:28:15Z",
      "execution_time_ms": 4200,
      "tokens": {"input": 800, "output": 400, "total": 1200},
      "cost": 0.018,
      "status": "success",
      "context": {
        "variables_used": ["@git-diff"],
        "files_modified": 0,
        "tests_run": 12
      },
      "hardware": {
        "workers": 16,
        "cores_used": 16,
        "execution_tier": "heavy"
      }
    }
  ],
  "analysis": {
    "most_used_command": "/test:run",
    "most_expensive_command": "/gen:crud",
    "average_execution_time_ms": 8400,
    "success_rate": 0.94,
    "token_efficiency": 0.78
  }
}
```

## Optimization Recommendations

```bash
/session:stats --optimize

💡 Optimization Recommendations:

High Token Commands:
⚠️  /gen:crud uses 6,500 tokens avg
    → Consider using @selection to scope
    → Savings: ~40% tokens

⚠️  /quality:fix on full files uses 4,000 tokens
    → Use @errors or @selection for targeted fixes
    → Savings: ~60% tokens

Context Usage:
✓  Good use of @git-diff (8 times)
✓  Efficient @selection usage (12 times)
⚠️  9 commands without context variables
    → Could save ~30% tokens with explicit context

Performance:
✓  Excellent M3 Max utilization (68% avg)
✓  Good parallelization on /test:run (16 workers)
✓  Efficient command sequencing

Cost Management:
✓  On track ($0.87 / $5.00 budget)
⚠️  Session context 71% full
    → Run /session:compact to optimize

Estimated Savings:
├─ Use more context variables: -$0.25 (~29%)
├─ Compact session now: -$0.15 (future commands)
└─ Total potential savings: $0.40 per session
```

## Comparison with Previous Sessions

```bash
/session:stats --compare

Session Comparison:
┌─────────────┬─────────┬─────────┬─────────┐
│ Date        │ Cmds    │ Tokens  │ Cost    │
├─────────────┼─────────┼─────────┼─────────┤
│ Today       │ 47      │ 57,680  │ $0.87   │
│ Yesterday   │ 52      │ 68,400  │ $1.03   │
│ 2 days ago  │ 38      │ 45,200  │ $0.68   │
│ Avg (7d)    │ 43      │ 52,800  │ $0.79   │
└─────────────┴─────────┴─────────┴─────────┘

Trends:
✓ Token efficiency improved 16% this week
✓ Faster avg execution (8.4s vs 10.2s)
⚠️ More /gen:crud usage (cost intensive)
```

## Integration with Other Commands

```bash
# Check stats before expensive operation
/session:stats
# 57K tokens used, safe to continue

/gen:crud Product
# Executes

/session:stats
# 64K tokens used, consider compacting
```

## Related Commands

- `/session:cost` - Quick token/cost view
- `/session:compact` - Reduce context
- `/session:checkpoint` - Save current state
- `/session:clear` - Reset session

## Best Practices

✅ **Check regularly** - Every 10-15 commands
✅ **Export weekly** - Track long-term patterns
✅ **Optimize from insights** - Use recommendations
✅ **Compare sessions** - Learn what works
✅ **Budget tracking** - Stay within limits

## Tips

1. **Use --export for reporting** - Share with team
2. **Check after expensive commands** - Monitor impact
3. **Optimize based on data** - Not guesses
4. **Track trends** - Improve over time
5. **Budget allocation** - Plan command usage


