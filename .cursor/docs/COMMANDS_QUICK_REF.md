# Universal Slash Commands - Quick Reference Card

## 🚀 SETUP (5 MIN)
```bash
cp .dev-config.template.json .dev-config.json
# Edit project details
# Use any command immediately!
```

---

## ⚡ TIER 1: LIGHT (1-4 cores, <5s)

| Command | Usage | Adapts To | MCP |
|---------|-------|-----------|-----|
| `/lint [path]` | Auto-fix code | Python/JS/Go/Rust | DC |
| `/format [path]` | Format code | Black/Prettier/gofmt | DC |
| `/explain` | AI explain code | Any language | ST+C7 |
| `/doc [target]` | Generate docs | Any framework | C7 |

---

## 🔥 TIER 2: MEDIUM (4-8 cores, 5-20s)

| Command | Usage | M3 Max | MCP |
|---------|-------|--------|-----|
| `/test [path]` | Parallel tests | 16 workers, 4-6s | DC+C7 |
| `/api [path] [method]` | Generate endpoint | 10-15s | ST+C7+DC |
| `/component [Name]` | Generate UI | 8-12s | C7+DC |
| `/model [name]` | Generate model | 5-10s | C7+DC |
| `/service [name]` | Generate service | 10-15s | C7+DC |
| `/refactor [pattern]` | Smart refactor | 10-20s | ST+DC |

---

## 💪 TIER 3: HEAVY (8-16 cores, 20-60s)

| Command | Usage | M3 Max | MCP |
|---------|-------|--------|-----|
| `/optimize [file]` | Apply M3 optimizations | 15-30s | ST+C7+DC |
| `/bench [function]` | Comprehensive benchmark | 30-60s | DC+ST |
| `/test-all` | Full test suite | 4-6s (15x faster) | DC |
| `/build` | Optimized build | 10-20s | DC |
| `/deploy [env]` | Full pipeline | 60-90s | DC+GH |

---

## 📊 VARIABLES

```json
{{hardware.cpuCores}}       // 16
{{hardware.workers.pytest}} // 16
{{stack.backend.framework}} // "fastapi"
{{paths.tests}}             // "backend/tests"
{{conventions.python.*}}    // "snake_case"
```

---

## 🔧 MCP SERVERS

| Server | Purpose | Commands |
|--------|---------|----------|
| **DC** (Desktop Commander) | File ops, execution | All |
| **C7** (Context7) | Best practices | api, component, optimize |
| **ST** (Sequential-thinking) | AI reasoning | explain, optimize, refactor |
| **GH** (GitHub) | Git operations | deploy, commit |
| **EX** (Exa) | Web search | research |

---

## 🎯 WORKFLOWS

### Development
```bash
/api /users POST      # Generate (10s)
/test .              # Test (4s)
/optimize src/       # Optimize (20s)
```

### Code Quality
```bash
/lint .              # Fix issues (3s)
/format .            # Format (2s)
/test-all            # Full tests (5s)
```

### Deployment
```bash
/test-all            # Test (5s)
/build               # Build (15s)
/deploy staging      # Deploy (75s)
```

---

## 📈 PERFORMANCE (M3 MAX)

| Operation | Time | Speedup |
|-----------|------|---------|
| Test Suite | 4s | 15x |
| Full Build | 12s | 3.3x |
| Optimization | 20s | 3x |
| Deployment | 75s | 2.4x |
| Bulk Process (100) | 20s | 10x |

---

## 🔒 BEST PRACTICES

✅ Use variables: `/test {{paths.tests}}`
✅ Cache responses (Context7: 24h)
✅ Monitor with `--verbose-timing`
✅ Chain commands for workflows
✅ Let MCP tools do the heavy lifting

---

## 🚀 PROJECT SETUP

```json
// .dev-config.json
{
  "project": { "name": "My Project" },
  "stack": {
    "backend": { "framework": "fastapi" },
    "frontend": { "framework": "react" }
  },
  "hardware": { "cpuCores": 16 }
}
```

**That's it!** All commands adapt automatically.

---

## 📦 PORTABILITY

```bash
# Copy to new project
cp .cursor/universal-commands.json new-project/
cp .dev-config.template.json new-project/.dev-config.json

# Edit config
vim new-project/.dev-config.json

# Same commands work!
```

---

## 🎓 CHEAT SHEET

```bash
# Quick commands
/t .                 # Test (short alias)
/l .                 # Lint (short alias)
/e                   # Explain (short alias)
/opt src/            # Optimize (short alias)

# With options
/test --workers=8    # Override workers
/build --minify      # Build with minify
/deploy --dry-run    # Test deployment

# Context-aware
/explain             # Explains selected code
/fix                 # Fixes visible error
/improve             # Suggests improvements
```

---

## 💡 TIPS

1. **Open relevant files** - Commands use context
2. **Chain commands** - Build workflows
3. **Custom commands** - Add to universal-commands.json
4. **Check performance** - Use `/bench` regularly
5. **Update config** - Keep .dev-config.json current

---

## 🆘 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Command not found | Check .dev-config.json exists |
| Slow execution | Verify worker count |
| MCP error | Check Claude Desktop config |
| Variable not resolved | Check config syntax |

---

## ✅ QUICK TEST

```bash
# 1. Test basic command
/test backend/tests/

# Expected: 4-6s with 16 workers
# If slower: Check CPU, workers config

# 2. Test MCP integration
/explain

# Expected: Detailed explanation with Context7
# If fails: Check MCP servers running

# 3. Test generation
/api /test GET

# Expected: Generated endpoint + tests
# If fails: Check stack config
```

---

**Version:** 1.0.0
**Hardware:** M3 Max (16 cores, 128GB)
**Compatibility:** ANY project

**Full Guide:** `.cursor/UNIVERSAL_COMMANDS_GUIDE.md`

