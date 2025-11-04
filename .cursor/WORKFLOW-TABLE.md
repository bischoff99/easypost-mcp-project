# Complete Workflow Reference Table

## Universal Workflows

| Command | Time | Category | Purpose | Chain Example |
|---------|------|----------|---------|---------------|
| `/workflow:morning` | 10s | Daily | Clean + fast tests | `→ && /workflow:ep-dev` |
| `/workflow:tdd` | ∞ | Daily | Test watch mode | Continuous feedback |
| `/workflow:pre-commit` | 15s | Quality | Format + lint + test staged | Before `git commit` |
| `/workflow:pre-push` | 25s | Quality | Full tests + coverage | Before `git push` |
| `/workflow:pre-pr` | 40s | Quality | Complete PR validation | Before creating PR |
| `/workflow:full-check` | 60s | Quality | Complete codebase check | Before major release |
| `/workflow:debug` | 20s | Dev | Debug failing tests | `\|\| /explain` |
| `/workflow:optimize` | 30s | Dev | Performance optimization | `&& /test --benchmark` |
| `/workflow:ship` | 45s | Release | Deploy preparation | Final validation |
| `/workflow:security` | 25s | Release | Security audit | Regular checks |

## EasyPost-Specific Workflows

| Command | Time | Category | Purpose | Chain Example |
|---------|------|----------|---------|---------------|
| `/workflow:ep-dev` | 5s | Dev | Start servers | `&& /workflow:ep-test` |
| `/workflow:ep-mcp-tool` | 30s | Dev | Create MCP tool | Add $1 $2 args |
| `/workflow:ep-test` | 6s | Test | 16-worker pytest | Most used |
| `/workflow:ep-test-all` | 8s | Test | Unit + integration ∥ | `& /workflow:ep-benchmark` |
| `/workflow:ep-parallel-test` | 8s | Test | All tests ∥ | Max parallelization |
| `/workflow:ep-full` | 30s | Test | Complete suite | Pre-deployment |
| `/workflow:ep-benchmark` | 15s | Perf | Performance tests | After optimization |
| `/workflow:ep-optimize` | 25s | Perf | Optimize shipping | `&& /ep-benchmark` |
| `/workflow:ep-bulk-test` | 12s | Domain | Bulk operations | Shipping validation |
| `/workflow:ep-rate-check` | 18s | Domain | Rate accuracy | Carrier comparison |
| `/workflow:ep-debug` | 20s | Debug | API troubleshooting | `\|\| /explain` |
| `/workflow:ep-pre-release` | 60s | Release | Quality gate | Before release |

## Quick Reference

### By Time
```
Fast (< 10s):        7 workflows
Medium (10-30s):     11 workflows
Slow (30-60s):       4 workflows
```

### By Category
```
Daily:              2 workflows
Quality:            4 workflows
Development:        4 workflows
Testing:            4 workflows
Performance:        2 workflows
Domain:             2 workflows
Debug:              2 workflows
Release:            4 workflows
```

### Most Common Chains
```
Morning routine:    /workflow:morning && /workflow:ep-dev
Before commit:      /workflow:pre-commit
Before push:        /workflow:pre-commit && /workflow:pre-push
Before PR:          /workflow:pre-pr && /workflow:ep-full
Before release:     /workflow:ship && /workflow:ep-pre-release
Parallel testing:   /workflow:ep-test & /workflow:ep-benchmark
```

## Operators

| Op | Name | Behavior | Example |
|----|------|----------|---------|
| `&&` | Sequential | Stop on fail | `/test && /fix` |
| `\|\|` | Fallback | Run if prev fails | `/test \|\| /debug` |
| `;` | Always | Continue regardless | `/test ; /stats` |
| `&` | Parallel | Run simultaneously | `/test & /benchmark` |
| `\|` | Pipe | Pass output | `/debug \| /fix` |

**Total: 22 workflows, 5 operators, infinite combinations! 🚀**
