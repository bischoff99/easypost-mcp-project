# Execute Saved Workflows

Run predefined workflow chains from `.dev-config.json`.

## Usage

```bash
/workflow:<name>              # Run saved workflow
/workflow:list                # List all workflows
/workflow:<name> [args]       # Run with arguments
```

## Universal Workflows

### Daily Workflows
```bash
/workflow:morning             # Morning routine (10s)
  → /clean --cache-only && /test --fast

/workflow:pre-commit          # Before commit (15s)
  → make format && make lint && /test @git-staged

/workflow:pre-push            # Before push (25s)
  → /test --coverage && make lint && /fix

/workflow:pre-pr              # Before PR (40s)
  → make format && make lint && /test --coverage && /secure @git-diff
```

### Development Workflows
```bash
/workflow:tdd                 # TDD cycle (continuous)
  → /test @selection --watch

/workflow:debug               # Debug errors (20s)
  → /test || (/explain @errors && /fix @errors)

/workflow:optimize            # Optimize code (30s)
  → /optimize @selection && /test --benchmark

/workflow:ship                # Ready to ship (45s)
  → /fix && /test --coverage && /optimize && make lint
```

### Quality Workflows
```bash
/workflow:security            # Security audit (25s)
  → /secure @file && make lint && /test

/workflow:full-check          # Complete check (60s)
  → /clean && make format && make lint && /test --coverage && /optimize
```

## Project-Specific Workflows

Loaded from `.dev-config.json` → `workflows.easypost`

```bash
/workflow:ep-dev              # Start dev environment
/workflow:ep-test             # Run tests (16 workers)
/workflow:ep-benchmark        # Performance benchmarks
/workflow:ep-mcp-tool         # Create MCP tool
/workflow:ep-full             # Complete test suite
/workflow:ep-pre-release      # Release quality gate
```

## Chaining Operators

```bash
&&  Sequential (stop on fail)
||  Fallback (on error)
;   Always execute
&   Parallel execution
|   Pipe output
```

## Examples

```bash
# Use saved workflow
/workflow:ship

# With arguments
/workflow:ep-mcp-tool EmailNotify email_notify

# Chain workflows
/workflow:morning && /workflow:ep-dev

# Parallel workflows
/workflow:ep-test & /workflow:ep-benchmark
```

## Configuration

Workflows defined in `.dev-config.json`:

```json
{
  "workflows": {
    "universal": {
      "morning": {
        "description": "...",
        "commands": "...",
        "estimated_time": "10s"
      }
    },
    "easypost": {
      "ep-dev": {
        "description": "...",
        "commands": "..."
      }
    }
  }
}
```

## Performance

**M3 Max Optimization:**
- Parallel execution: 40-50% time savings
- Sequential validation ensures correctness
- Cached results when possible

**Ready to use! Type `/workflow:` to see all available workflows.**
