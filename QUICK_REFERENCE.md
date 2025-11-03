# ⚡ Quick Reference Card - Universal Slash Commands

**Print this and keep it handy!**

---

## 🎯 Most Used Commands

### Code Generation (5-10s each)
```
/api [path] [method]        → API endpoint
/component [Name]           → UI component  
/model [Name]               → Data model
/service [Name]             → Service class
/hook [name]                → Custom hook
```

### Full Features (30-60s each)
```
/crud [Model]               → Complete CRUD
/feature [name]             → Full feature stack
/page [Name]                → Complete page
/form [name] [fields]       → Form with validation
```

### Testing (10-20s each)
```
/test [file]                → Generate tests
/mock [dependency]          → Mock external API
/bench [function]           → Performance benchmark
```

### Smart Helpers (5-15s each)
```
/fix                        → Auto-fix errors
/explain                    → Explain selected code
/improve                    → Suggest improvements
/refactor [pattern]         → Smart refactoring
```

### Performance (15-30s each)
```
/optimize [file]            → M3 Max optimizations
/parallel [file]            → Parallel processing
/profile [function]         → Performance profiling
```

### Security (10-20s each)
```
/secure [file]              → Security audit
/auth [type]                → Authentication system
/validate [model]           → Input validation
```

---

## 💡 Usage Tips

### Be Specific
✅ `/api /users/profile GET with JWT auth`  
❌ `/api`

### Use Context
- Open relevant files first
- AI uses visible code

### Chain Commands
```
/model User
/crud User  
/test user_service.py
```

### Quick Iteration
```
/component Card
/improve         # AI suggests changes
/test Card.jsx   # Generate tests
```

---

## 🔧 Customization

**Edit `.dev-config.json`** to change:
- Stack (Python→Go, React→Vue)
- Conventions (snake_case→camelCase)
- Hardware (M3 Max→M1)
- Paths (custom structure)

**Commands adapt automatically!**

---

## ⌨️ VS Code Shortcuts

Type these + Tab:
```
rfc         → React component
api         → API call
us          → useState
ue          → useEffect
cl          → console.log
log         → logger
```

---

## 🛠️ Makefile Commands

```bash
make dev        # Start dev servers
make test       # Run all tests
make test-fast  # Parallel tests (3s)
make build      # Production build
make clean      # Clean artifacts
make help       # Show all commands
```

---

## 🎯 Common Workflows

### New Feature
```
1. /feature user-notifications
2. Review generated code
3. make test
4. make dev (test manually)
5. git commit
```

### Fix Bug
```
1. Run code → see error
2. /fix (reads error automatically)
3. make test
4. Done!
```

### Add CRUD
```
1. /crud Product
2. Review 50+ generated files
3. Customize as needed
4. make test
5. Ship it!
```

### Optimize Performance
```
1. Open slow file
2. /optimize filename
3. /bench function_name
4. Compare metrics
5. Done!
```

---

## 📊 M3 Max Performance

| Hardware | Simple Command | Complex Command |
|----------|----------------|-----------------|
| M3 Max | 5-8s | 30-40s |
| M2 | 8-12s | 45-60s |
| M1 | 10-15s | 60-90s |
| Intel | 15-25s | 90-120s |

**Your M3 Max is 2-5x faster!** ⚡

---

## 🚀 Pro Tips

1. **Keep .dev-config.json updated** as project evolves
2. **Add custom commands** in .cursorrules
3. **Use /explain** on unfamiliar code
4. **Chain /test after /api or /component**
5. **Run /optimize on bottlenecks**
6. **Use make benchmark** to track performance

---

## 📦 Portable to New Projects

```bash
# Copy system to new project
./install-universal-commands.sh /path/to/new-project

# Or create alias:
alias dev-init='./install-universal-commands.sh'

# Then:
cd new-project && dev-init
```

---

## 📚 Full Documentation

- `UNIVERSAL_COMMANDS.md` - Complete guide
- `.cursorrules` - All command definitions
- `.dev-config.template.json` - Config options
- `.ai-templates/` - Code examples

---

**Questions?** Check `UNIVERSAL_COMMANDS.md` or type `/explain` in Cursor!
