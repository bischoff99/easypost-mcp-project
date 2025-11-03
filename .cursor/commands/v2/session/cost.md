---
name: cost
category: session
description: View token usage and estimated costs for current session
allowed-tools: []
requires-approval: false
context-aware: false
arguments: []
estimated-time: <1s
estimated-tokens: 0
version: 2.0
---

# /session:cost

Display token usage statistics and cost estimates for the current conversation session. Essential for monitoring API usage and optimizing prompts.

## Usage

```bash
/session:cost
```

## Output Example

```
📊 Session Token Usage

Input Tokens:    45,230
Output Tokens:   12,450
Total Tokens:    57,680

Estimated Cost:  $0.87
Model:           Claude Sonnet 4.5

Commands Run:    12
Avg per Command: 4,807 tokens
Most Expensive:  /gen:crud Product (12,500 tokens)

Recommendations:
• Consider /session:compact to reduce context
• 42,320 tokens remaining in context window
```

## When to Use

- **Budget tracking**: Monitor API spending
- **Optimization**: Identify expensive commands
- **Context management**: Know when to clear/compact
- **Before expensive operations**: Check budget first

## Cost Breakdown by Model

### Claude Sonnet 4.5
- Input:  $3 / 1M tokens
- Output: $15 / 1M tokens
- Context: 200K tokens

### Claude Opus 4
- Input:  $15 / 1M tokens
- Output: $75 / 1M tokens
- Context: 200K tokens

## Industry Standard

**Source**: Claude Code `/cost` command
- Standard feature in professional AI coding tools
- Helps prevent unexpected bills
- Enables cost-conscious development

## Integration with .dev-config.json

```json
{
  "session": {
    "tracking": {
      "enabled": true,
      "warnAt": 50000,     // Warn at 50K tokens
      "stopAt": 100000     // Suggest compact at 100K
    },
    "costAlerts": {
      "enabled": true,
      "warnAt": 1.00,      // Warn at $1.00
      "stopAt": 5.00       // Alert at $5.00
    }
  }
}
```

## Command History

```bash
/session:cost --history

Recent Commands:
1. /gen:api /users POST          3,200 tokens   $0.05
2. /test:run backend/            1,800 tokens   $0.03
3. /quality:fix @errors          5,400 tokens   $0.08
4. /gen:component UserCard       4,100 tokens   $0.06
5. /test:coverage backend/       2,900 tokens   $0.04

Total last 5 commands: 17,400 tokens ($0.26)
```

## Cost Optimization Tips

### 1. Use Context Variables
```bash
# Expensive (full codebase)
/quality:fix
→ 25,000 tokens ($0.38)

# Cheaper (specific file)
/quality:fix @file
→ 3,000 tokens ($0.05)

# Cheapest (selection only)
/quality:fix @selection
→ 800 tokens ($0.01)
```

### 2. Compact Regularly
```bash
# Every 10-15 commands
/session:compact "Keep only test results and fixes"
# Reduces context by 60-80%
```

### 3. Clear Between Tasks
```bash
# After completing a feature
/session:clear
# Starts fresh, minimal tokens
```

## Automatic Warnings

System automatically warns when:

```
⚠️ Token Warning
Current session: 52,000 tokens ($0.78)
Approaching context limit (200K)

Suggestions:
1. Run /session:compact to reduce context
2. Run /session:clear to start fresh
3. Continue (48K tokens remaining)

[Compact] [Clear] [Continue]
```

## Export Usage Report

```bash
/session:cost --export usage-report.json

# Creates JSON report:
{
  "session": {
    "start": "2025-11-03T09:15:00Z",
    "duration": "45min",
    "total_tokens": 57680,
    "estimated_cost": 0.87
  },
  "commands": [
    {
      "command": "/gen:crud Product",
      "tokens": 12500,
      "cost": 0.19,
      "timestamp": "2025-11-03T09:30:00Z"
    }
  ]
}
```

## Comparison with Manual Tracking

| Method | Accuracy | Realtime | Actionable |
|--------|----------|----------|------------|
| Manual calculation | 60% | No | No |
| API dashboard | 100% | Delayed | No |
| /session:cost | 95% | Yes | Yes |

## Related Commands

- `/session:compact` - Reduce token usage
- `/session:clear` - Reset to zero
- `/session:checkpoint` - Save current state
- `/session:stats` - Detailed analytics

## Best Practices

✅ **Check before expensive commands** - Know the cost upfront
✅ **Monitor during long sessions** - Prevent surprises
✅ **Compare command costs** - Optimize workflows
✅ **Use with checkpoints** - Save before risky operations
✅ **Export reports** - Track spending over time

## Performance Impact

- **Time**: Instant (<1s)
- **Tokens**: 0 (no API call)
- **Accuracy**: ±5% of actual cost

## Tips

1. **Run periodically** - Every 5-10 commands
2. **Before /gen:crud** - Most expensive command
3. **After errors** - Fixes can be token-heavy
4. **Compare alternatives** - @selection vs @file vs full context
5. **Budget your session** - Set token goals

