# Tool Selection Guide

**Decision tree for choosing the right tool for your task.**

**Last Updated**: 2025-11-12

---

## Quick Decision Tree

```
Need to start development servers?
├─ Want macOS Terminal windows? → ./scripts/start-dev.sh
├─ Need Docker PostgreSQL? → ./scripts/dev_local.sh
├─ Need MCP verification? → ./scripts/dev-with-mcp.sh
├─ Want IDE integration? → VS Code "Dev: Full Stack"
└─ Standard development? → make dev ✅ (recommended)

Need to run tests?
├─ Want watch mode (TDD)? → ./scripts/watch-tests.sh
├─ Quick test suite? → ./scripts/quick-test.sh
├─ Want IDE integration? → VS Code "Test: Backend/Frontend"
├─ Need AI assistance? → /test
└─ Standard testing? → make test ✅ (recommended)

Need code quality checks?
├─ Before commit? → /workflow:pre-commit ✅ (recommended)
├─ Quick check? → make check
├─ IDE integration? → VS Code "Pre-Commit: Run All Checks"
└─ Individual checks? → make lint / make format

Need to fix errors?
├─ Want AI assistance? → /fix ✅ (recommended)
├─ Or workflow? → /workflow:error-resolution
└─ Manual? → make lint && make format

Need to understand code?
└─ AI assistance? → /explain ✅ (recommended)

Need to commit?
├─ Quick commit + push? → make qcp m="message"
├─ Want AI-generated message? → /commit ✅ (recommended)
└─ Manual? → git commit
```

---

## Detailed Selection Guide

### Development Servers

#### ✅ Recommended: `make dev`
**When**: Standard development workflow  
**Why**: Includes MCP verification, parallel execution, consistent behavior  
**Time**: ~5s

#### `./scripts/start-dev.sh`
**When**: You want separate Terminal windows (macOS only)  
**Why**: Better visibility, separate logs  
**Time**: ~5s

#### `./scripts/dev_local.sh`
**When**: You need Docker PostgreSQL  
**Why**: Full stack with database  
**Time**: ~30s (includes Docker setup)

#### `./scripts/dev-with-mcp.sh`
**When**: You need MCP server verification  
**Why**: Validates MCP tools are accessible  
**Time**: ~10s

#### VS Code "Dev: Full Stack"
**When**: Working in VS Code, want IDE integration  
**Why**: Problem matchers, inline errors  
**Time**: ~5s

---

### Testing

#### ✅ Recommended: `make test`
**When**: Standard testing workflow  
**Why**: Parallel execution, consistent behavior  
**Time**: ~15s

#### `./scripts/watch-tests.sh`
**When**: TDD workflow, want auto-rerun on changes  
**Why**: Continuous feedback  
**Time**: Continuous

#### `./scripts/quick-test.sh`
**When**: Quick health check  
**Why**: Fast, minimal output  
**Time**: ~30-60s

#### VS Code "Test: Backend/Frontend"
**When**: Working in VS Code, want IDE integration  
**Why**: Test explorer integration, problem matchers  
**Time**: ~15s

#### `/test`
**When**: Want AI assistance, smart test selection  
**Why**: Auto-detects framework, parallel execution  
**Time**: 10-80s

---

### Code Quality

#### ✅ Recommended: `/workflow:pre-commit`
**When**: Before committing code  
**Why**: Full quality check, AI-powered  
**Time**: 30-60s

#### `make check`
**When**: Quick quality check  
**Why**: Fast, standard checks  
**Time**: ~22s

#### `make lint` / `make format`
**When**: Individual checks  
**Why**: Fast, parallel execution  
**Time**: ~4s / ~3s

#### VS Code "Pre-Commit: Run All Checks"
**When**: Working in VS Code  
**Why**: IDE integration, uses Makefile  
**Time**: ~22s

---

### Error Fixing

#### ✅ Recommended: `/fix`
**When**: You see an error  
**Why**: AI-powered, auto-detects and fixes  
**Time**: 10-20s

#### `/workflow:error-resolution`
**When**: Complex error, need systematic approach  
**Why**: Full workflow with debugging  
**Time**: 40-130s

#### `make lint && make format`
**When**: Simple formatting/linting errors  
**Why**: Fast, standard fixes  
**Time**: ~7s

---

### Code Understanding

#### ✅ Recommended: `/explain`
**When**: Need to understand code  
**Why**: AI-powered, comprehensive analysis  
**Time**: 12-20s

#### Manual code review
**When**: Simple code, no AI needed  
**Why**: Direct control  
**Time**: Varies

---

### Feature Development

#### ✅ Recommended: `/workflow:feature-dev`
**When**: Implementing new features  
**Why**: Complete workflow, AI-powered  
**Time**: 60-180s

#### Manual workflow
**When**: Simple feature, no AI needed  
**Why**: Direct control  
**Time**: Varies

---

### Code Improvement

#### ✅ Recommended: `/workflow:code-improvement`
**When**: Improving existing code  
**Why**: Systematic improvement, AI-powered  
**Time**: 55-175s

#### `/refactor`
**When**: Specific refactoring task  
**Why**: AI-powered, safe refactoring  
**Time**: 12-28s

---

### Project Cleanup

#### ✅ Recommended: `/workflow:cleanup`
**When**: Periodic project cleanup  
**Why**: Comprehensive cleanup, AI-powered  
**Time**: 2-5 minutes

#### `make clean`
**When**: Quick cleanup  
**Why**: Fast, standard cleanup  
**Time**: ~2s

---

### Database Operations

#### ✅ Recommended: `make db-migrate`
**When**: Creating migrations  
**Why**: Standard, consistent  
**Time**: ~5s

#### VS Code "Database: Create Migration"
**When**: Working in VS Code  
**Why**: Input prompt for message  
**Time**: ~5s

#### `make db-reset`
**When**: Resetting database  
**Why**: Standard, consistent  
**Time**: ~10s

---

## Tool Comparison Matrix

| Task | Makefile | Scripts | VS Code | Cursor | Best Choice |
|------|----------|---------|---------|--------|-------------|
| **Start dev servers** | ✅ | ✅ | ✅ | ❌ | `make dev` |
| **Run tests** | ✅ | ✅ | ✅ | ✅ | `make test` |
| **Code quality** | ✅ | ❌ | ✅ | ✅ | `/workflow:pre-commit` |
| **Fix errors** | ⚠️ | ❌ | ❌ | ✅ | `/fix` |
| **Understand code** | ❌ | ❌ | ❌ | ✅ | `/explain` |
| **Feature dev** | ⚠️ | ❌ | ❌ | ✅ | `/workflow:feature-dev` |
| **Database ops** | ✅ | ❌ | ✅ | ❌ | `make db-migrate` |
| **Cleanup** | ✅ | ❌ | ❌ | ✅ | `/workflow:cleanup` |

**Legend**:
- ✅ Full support
- ⚠️ Partial support
- ❌ Not available

---

## Best Practices

### Daily Development
1. **Start servers**: `make dev` ✅
2. **Run tests**: `make test` ✅
3. **Code quality**: `make lint` / `make format` ✅

### Before Commit
1. **Full check**: `/workflow:pre-commit` ✅ (AI-powered)
2. **Quick check**: `make check` (standard)
3. **Commit**: `/commit` ✅ (AI-generated message)

### Feature Development
1. **Full workflow**: `/workflow:feature-dev` ✅ (AI-powered)
2. **Manual**: `make dev` → code → `make test` → commit

### Bug Fixing
1. **AI-powered**: `/workflow:error-resolution` ✅
2. **Quick fix**: `/fix` ✅
3. **Manual**: `make test` → fix → `make test`

### Code Understanding
1. **AI-powered**: `/explain` ✅
2. **Manual**: Code review

---

## When to Use Each Tool

### Use Makefile When:
- ✅ Standard operations (dev, test, lint, format)
- ✅ Quick commands (< 30s)
- ✅ CI/CD pipelines
- ✅ Parallel execution needed
- ✅ Consistency is important

### Use Scripts When:
- ✅ Complex workflows
- ✅ macOS-specific features
- ✅ Docker operations
- ✅ Database monitoring
- ✅ Performance benchmarks
- ✅ Specialized use cases

### Use VS Code Tasks When:
- ✅ Working in VS Code
- ✅ Want IDE integration (problem matchers)
- ✅ Background tasks
- ✅ Input prompts needed
- ✅ Quick access from IDE

### Use Cursor Workflows When:
- ✅ AI-powered assistance needed
- ✅ Complex multi-step processes
- ✅ Code understanding
- ✅ Automated fixes
- ✅ Documentation generation

### Use Universal Commands When:
- ✅ AI assistance needed
- ✅ Smart defaults wanted
- ✅ Context-aware operations
- ✅ Complex refactoring
- ✅ Interactive debugging

---

## Common Patterns

### Morning Routine
```bash
make clean && make test && make dev
```

### Development Cycle
```bash
make dev
# ... code changes ...
make test-fast
make lint
make format
```

### Before Commit
```bash
/workflow:pre-commit
# or
make check
```

### Feature Development
```bash
/workflow:feature-dev
```

### Bug Fixing
```bash
/workflow:error-resolution
# or
/fix
```

---

**Last Updated**: 2025-11-12  
**Status**: ✅ Complete - Decision guide for tool selection
