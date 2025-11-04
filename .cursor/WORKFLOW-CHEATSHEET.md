# Workflow Cheatsheet

**Quick reference for 22 configured workflows**

---

## ⚡ Most Used (Top 5)

```bash
/workflow:morning           # Start of day (10s)
/workflow:pre-commit        # Before commits (15s)
/workflow:ep-dev            # Start dev servers (5s)
/workflow:ep-test           # Run tests fast (6s)
/workflow:ship              # Ready to deploy (45s)
```

---

## 📅 Daily Routine

```bash
# 1. Morning
/workflow:morning
# → Clean cache, fast tests

# 2. Start Development
/workflow:ep-dev
# → Backend + frontend servers

# 3. After Each Change
/workflow:ep-test
# → 16-worker parallel tests

# 4. Before Commit
/workflow:pre-commit
# → Format, lint, test staged files

# 5. End of Day
/workflow:pre-push
# → Full tests + coverage
```

---

## 🎯 By Use Case

### Feature Development
```bash
# Create MCP tool
/workflow:ep-mcp-tool RefundRequest refund

# Test it
/workflow:ep-test

# Optimize
/workflow:optimize

# Ship it
/workflow:pre-commit && /workflow:pre-push
```

### Debugging
```bash
# Quick debug
/workflow:debug

# EasyPost-specific
/workflow:ep-debug

# Full diagnostic
/workflow:ep-full
```

### Performance
```bash
# Quick benchmark
/workflow:ep-benchmark

# Full optimization
/workflow:ep-optimize

# Validate improvements
/workflow:ep-parallel-test
```

### Quality Assurance
```bash
# Before commit
/workflow:pre-commit

# Before push
/workflow:pre-push

# Before PR
/workflow:pre-pr

# Before release
/workflow:ep-pre-release
```

---

## 🔗 Chaining Examples

### Sequential (&&)
```bash
# Morning routine
/workflow:morning && /workflow:ep-dev && /workflow:ep-test
# Total: ~21s

# Full quality check
/workflow:pre-commit && /workflow:pre-push && /workflow:pre-pr
# Total: ~80s
```

### Parallel (&)
```bash
# Test everything simultaneously
/workflow:ep-test & /workflow:ep-benchmark
# Total: 15s (vs 21s sequential)

# Multiple tools
/workflow:ep-mcp-tool Refund refund & /workflow:ep-mcp-tool Customs customs
# Total: 30s (vs 60s sequential)
```

### Fallback (||)
```bash
# Test or debug
/workflow:ep-test || /workflow:ep-debug

# Optimize or explain
/workflow:optimize || /explain @selection
```

---

## ⏱️ Time Estimates

```
Fast (< 10s):
  morning, ep-dev, ep-test, ep-test-all, ep-parallel-test

Medium (10-30s):
  pre-commit, debug, pre-push, security, optimize, 
  ep-bulk-test, ep-rate-check, ep-debug, ep-optimize

Slow (30-60s):
  pre-pr, ship, ep-mcp-tool, ep-full, ep-pre-release, full-check
```

---

## 🚀 Pro Tips

1. **Chain smartly:** Use `&&` for validation pipelines
2. **Parallelize:** Use `&` for independent tasks
3. **Start small:** Run `/workflow:ep-test` not `/workflow:full-check`
4. **Monitor time:** If slower than estimate, investigate
5. **Customize:** Add your workflows to `.dev-config.json`

---

## 📊 Categories

**Universal (10):**
Daily (2), Quality (4), Development (2), Release (2)

**EasyPost (12):**
Development (2), Testing (4), Performance (2), Domain (2), Debug (1), Release (1)

---

**Type `/workflow:` to see autocomplete!**
