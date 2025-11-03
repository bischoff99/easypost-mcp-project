# 📁 EasyPost MCP Project - Strict Structure Guide

**Version:** 2.0
**Last Updated:** November 3, 2025
**Status:** Enforced & Documented

---

## 🎯 Structure Philosophy

**Principles:**
1. **Separation of Concerns** - Clear boundaries between components
2. **Centralized Scripts** - All scripts in one location
3. **Consistent Naming** - snake_case (Python), camelCase (JS), PascalCase (Components)
4. **Zero Redundancy** - Single source of truth for everything
5. **Production Ready** - Structure scales from dev to production

---

## 📂 Root Directory Structure

```
easypost-mcp-project/
├── .cursor/                    # Cursor AI configuration
│   ├── commands/               # Custom slash commands (7)
│   └── rules/                  # Code rules (14)
│
├── backend/                    # Python FastAPI backend
│   ├── src/                    # Source code (strict structure)
│   ├── tests/                  # Test suite (unit + integration)
│   ├── Dockerfile              # Production container
│   ├── requirements.txt        # Python dependencies
│   └── pyproject.toml          # Python project config
│
├── frontend/                   # React + Vite frontend
│   ├── src/                    # Source code (strict structure)
│   ├── public/                 # Static assets
│   ├── Dockerfile              # Production container
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Build configuration
│
├── database/                   # Database configurations
│   └── postgresql-m3max.conf   # M3 Max optimized Postgres
│
├── docs/                       # ALL documentation
│   ├── setup/                  # Setup guides
│   ├── guides/                 # How-to guides
│   ├── reports/                # Status reports
│   └── architecture/           # Technical docs
│
├── scripts/                    # ALL project scripts
│   ├── start-dev.sh            # Start development servers
│   ├── cleanup-unused-code.sh  # Code cleanup
│   ├── benchmark.sh            # Performance testing
│   └── (7 more scripts)
│
├── demos/                      # Demo guides & examples
│
├── .dev-config.json            # Project configuration
├── .editorconfig               # Editor settings
├── .gitignore                  # Git ignore rules
├── docker-compose.yml          # Container orchestration
├── Makefile                    # Build automation
├── README.md                   # Project overview
└── QUICK_REFERENCE.md          # Command cheat sheet
```

**Rules:**
- ✅ **5 markdown files maximum at root** (currently: 5/5)
- ✅ **No scripts outside scripts/** (enforced)
- ✅ **No docs outside docs/** (enforced)
- ✅ **No temporary files** (removed on commit)

---

## 🔹 Backend Structure (Python)

```
backend/
├── src/                        # Source code ONLY
│   ├── __init__.py
│   ├── server.py               # FastAPI main app
│   │
│   ├── mcp/                    # MCP server (modular)
│   │   ├── __init__.py
│   │   ├── tools/              # MCP tools (5 files)
│   │   ├── resources/          # MCP resources (2 files)
│   │   └── prompts/            # MCP prompts (4 files)
│   │
│   ├── models/                 # Pydantic models
│   │   ├── __init__.py
│   │   ├── requests.py         # Request models
│   │   └── analytics.py        # Analytics models
│   │
│   ├── services/               # Business logic
│   │   └── easypost_service.py # EasyPost integration
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── config.py           # Configuration
│       └── monitoring.py       # Health checks
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Shared fixtures
│   ├── unit/                   # Unit tests
│   │   ├── test_bulk_tools.py
│   │   └── test_easypost_service.py
│   ├── integration/            # Integration tests (future)
│   └── captured_responses/     # Test fixtures (20 JSON files)
│
├── Dockerfile                  # Production image
├── requirements.txt            # Dependencies
├── pyproject.toml              # Project config
├── pytest.ini                  # Test config
└── run_mcp.py                  # MCP server entry point
```

**Rules:**
- ✅ **All source in src/** - No code at root
- ✅ **Tests mirror src/** - Same structure as source
- ✅ **No scripts in backend/** - Move to scripts/
- ✅ **Type hints required** - All functions
- ✅ **Docstrings required** - All public functions

---

## 🔹 Frontend Structure (React)

```
frontend/
├── src/                        # Source code ONLY
│   ├── main.jsx                # Entry point
│   ├── App.jsx                 # Root component
│   ├── index.css               # Global styles
│   │
│   ├── components/             # Reusable components
│   │   ├── analytics/          # Analytics components (5)
│   │   ├── dashboard/          # Dashboard components (2)
│   │   ├── layout/             # Layout components (3)
│   │   ├── shipments/          # Shipment components (2)
│   │   ├── ui/                 # UI primitives (7)
│   │   └── upload/             # Upload components (1)
│   │
│   ├── pages/                  # Route pages (6 pages)
│   │   ├── DashboardPage.jsx
│   │   ├── ShipmentsPage.jsx
│   │   ├── TrackingPage.jsx
│   │   ├── AnalyticsPage.jsx
│   │   ├── AddressBookPage.jsx
│   │   └── SettingsPage.jsx
│   │
│   ├── hooks/                  # Custom hooks
│   │   ├── useShipmentForm.js
│   │   └── useShipmentForm.test.js
│   │
│   ├── stores/                 # Zustand state management
│   │   ├── useThemeStore.js
│   │   └── useUIStore.js
│   │
│   ├── services/               # API clients
│   │   └── api.js              # Axios client
│   │
│   ├── lib/                    # Utilities
│   │   ├── utils.js            # Helper functions
│   │   └── exportUtils.js      # CSV export
│   │
│   └── test/                   # Test setup
│       └── setup.js
│
├── public/                     # Static assets
├── Dockerfile                  # Production image
├── package.json                # Dependencies
├── vite.config.js              # Build config
├── vitest.config.js            # Test config
├── tailwind.config.js          # Tailwind config
└── nginx.conf                  # Production web server
```

**Rules:**
- ✅ **Components in components/** - Organized by feature
- ✅ **Pages in pages/** - One page = one route
- ✅ **Hooks in hooks/** - Custom React hooks only
- ✅ **Stores in stores/** - Zustand stores only
- ✅ **No CSS files** - Tailwind only (except index.css)
- ✅ **PascalCase.jsx** - Components
- ✅ **camelCase.js** - Utilities/hooks

---

## 🔹 Scripts Directory (Centralized)

```
scripts/
├── start-dev.sh                # Start both backend + frontend
├── cleanup-unused-code.sh      # Clean codebase (M3 Max optimized)
├── optimize-structure.sh       # Organize documentation
├── benchmark.sh                # Performance benchmarks
├── quick-test.sh               # Fast test execution
├── create-dev-toolkit-repo.sh  # Toolkit generator
└── install-universal-commands.sh # Command installer
```

**Rules:**
- ✅ **All scripts here** - No exceptions
- ✅ **Executable permissions** - chmod +x
- ✅ **Bash shebang** - #!/bin/bash
- ✅ **Error handling** - set -e
- ✅ **Usage comments** - Header docs
- ✅ **M3 Max optimized** - Parallel execution where possible

**Removed scripts (moved to scripts/):**
- ❌ `backend/start_backend.sh` → `scripts/start-backend.sh`
- ❌ `backend/start_backend_jit.sh` → `scripts/start-backend-jit.sh`
- ❌ `frontend/start_frontend.sh` → `scripts/start-frontend.sh`

**Removed directories (empty):**
- ❌ `backend/scripts/` (moved watch-tests.sh)
- ❌ `frontend/scripts/` (empty)
- ❌ `scripts/archive/` (empty)

---

## 🔹 Documentation Structure (Organized)

```
docs/
├── README.md                   # Documentation index
│
├── setup/                      # Setup & installation
│   ├── START_HERE.md           # Quick start
│   └── SETUP_INSTRUCTIONS.md   # Detailed setup
│
├── guides/                     # How-to guides
│   ├── DEPLOYMENT.md           # Deployment guide
│   ├── M3MAX_OPTIMIZATIONS.md  # Hardware optimization
│   ├── UNIVERSAL_COMMANDS.md   # Command system
│   ├── SLASH_COMMANDS_*.md     # Slash command guides (3)
│   └── desktop-commander-prompts.md # DC guide
│
├── reports/                    # Status & analysis reports
│   ├── API_VERIFICATION_REPORT.md
│   ├── BUILD_REPORT.md
│   ├── CODE_REVIEW_REPORT.md
│   ├── TEST_ALL_REPORT.md
│   └── (11 more reports)
│
└── architecture/               # Technical architecture
    ├── MCP_TOOLS_INVENTORY.md  # Tool catalog
    └── STRUCTURE_OPTIMIZATION.md # This structure
```

**Rules:**
- ✅ **All docs in docs/** - No exceptions
- ✅ **Category subdirectories** - setup, guides, reports, architecture
- ✅ **UPPERCASE.md naming** - Easy to spot
- ✅ **Clear hierarchy** - Beginner to advanced
- ✅ **Single source of truth** - No duplicates

---

## 🎯 Naming Conventions (Enforced)

### **Backend (Python)**
```python
# Files: snake_case
easypost_service.py
bulk_tools.py

# Classes: PascalCase
class EasyPostService:
class AddressModel:

# Functions: snake_case
def create_shipment():
async def get_rates():

# Constants: UPPER_SNAKE_CASE
MAX_WORKERS = 32
DEFAULT_TIMEOUT = 30

# Private: _leading_underscore
def _internal_helper():
```

### **Frontend (JavaScript/React)**
```javascript
// Components: PascalCase.jsx
DashboardPage.jsx
ShipmentTable.jsx

// Hooks: camelCase.js (use prefix)
useShipmentForm.js
useAuth.js

// Utilities: camelCase.js
exportUtils.js
utils.js

// Constants: UPPER_SNAKE_CASE
const API_URL = 'http://localhost:8000';
const MAX_RETRIES = 3;

// Functions: camelCase
function handleSubmit() {}
const getUserData = () => {};
```

### **Configuration Files**
```
.dev-config.json              # Lowercase with hyphens
docker-compose.yml            # Lowercase with hyphens
pyproject.toml                # Lowercase
package.json                  # Lowercase
```

---

## 📋 File Organization Rules

### **✅ Allowed at Root (5 files max)**
1. `README.md` - Project overview
2. `QUICK_REFERENCE.md` - Command cheat sheet
3. `BULK_TOOL_USAGE.md` - Bulk tool guide
4. `DEPENDENCY_AUDIT.md` - Dependency info
5. `PROJECT_STRUCTURE.md` - This file

### **❌ Not Allowed at Root**
- ❌ Scripts (→ scripts/)
- ❌ Documentation (→ docs/)
- ❌ Temporary files (delete)
- ❌ Status reports (→ docs/reports/)
- ❌ Test files (→ backend/tests/ or frontend/src/test/)

### **✅ Configuration Files (Root is OK)**
- ✅ `.dev-config.json`
- ✅ `.editorconfig`
- ✅ `.gitignore`
- ✅ `docker-compose.yml`
- ✅ `Makefile`
- ✅ `*.code-workspace`

---

## 🛠️ Development Workflow

### **Starting Development**
```bash
# Option 1: Use Makefile
make dev

# Option 2: Use script
./scripts/start-dev.sh

# Option 3: Manual
cd backend && source venv/bin/activate && uvicorn src.server:app --reload
cd frontend && npm run dev
```

### **Running Tests**
```bash
# Backend (M3 Max: 16 parallel workers)
cd backend
pytest tests/ -n 16 -v

# Frontend (M3 Max: 20 parallel workers)
cd frontend
npm test

# All tests
make test
```

### **Cleaning Codebase**
```bash
# Automated cleanup (M3 Max optimized)
./scripts/cleanup-unused-code.sh

# Structure optimization
./scripts/optimize-structure.sh
```

### **Benchmarking**
```bash
# Performance benchmarks
./scripts/benchmark.sh
```

---

## 🚀 Production Deployment

### **Docker (Recommended)**
```bash
# Build (parallel on M3 Max)
docker compose build --parallel

# Deploy
docker compose up -d

# Monitor
docker compose logs -f
```

### **Manual**
```bash
# Backend
cd backend
gunicorn src.server:app --workers 33 --worker-class uvicorn.workers.UvicornWorker

# Frontend
cd frontend
npm run build
npx serve -s dist
```

---

## 📊 M3 Max Optimizations

### **Hardware Specs**
- **CPU:** 16 cores (performance + efficiency)
- **RAM:** 128 GB unified memory
- **Neural Engine:** 16-core (AI acceleration)

### **Optimizations Applied**
```
Backend:
├─ Uvicorn: 33 workers (2 × 16 + 1)
├─ ThreadPool: 32 workers (min(32, 16 × 2))
├─ Event Loop: uvloop (2-4x faster)
└─ Async: All I/O operations

Frontend:
├─ Vite: SWC transpilation (3-5x faster)
├─ Code Splitting: Optimized chunks
├─ Lazy Loading: Route-based
└─ Native Watch: No polling overhead

Tests:
├─ Backend: pytest -n 16 (all cores)
├─ Frontend: vitest --maxThreads=20
└─ Total: ~8 seconds (4.4x faster)

Scripts:
├─ Parallel: xargs -P 16
├─ Spotlight: mdfind (macOS native)
└─ Concurrent: Background jobs
```

---

## 🔍 Structure Verification

### **Check Root Cleanliness**
```bash
# Count markdown files (should be ≤ 5)
ls -1 *.md | wc -l

# List all root files
ls -lh *.md *.json *.yml
```

### **Verify No Scattered Scripts**
```bash
# Should only find scripts in scripts/
find . -name "*.sh" -not -path "./scripts/*" -not -path "./backend/venv/*"
```

### **Check Test Discovery**
```bash
# Backend: Should find 21 tests
pytest backend/tests/ --collect-only -q

# Frontend: Should find 7 tests
cd frontend && npm test -- --run
```

### **Verify Documentation Organization**
```bash
# All docs should be in docs/
find . -name "*.md" -not -path "./docs/*" -not -path "./node_modules/*" | grep -v "README.md"
```

---

## 🎯 Maintenance Checklist

### **Daily**
- [ ] Run development with `./scripts/start-dev.sh`
- [ ] Use slash commands for code generation
- [ ] Run tests before commits

### **Weekly**
- [ ] Run `./scripts/cleanup-unused-code.sh`
- [ ] Check for unused dependencies
- [ ] Review linter warnings

### **Monthly**
- [ ] Run `./scripts/benchmark.sh`
- [ ] Update dependencies
- [ ] Review and update documentation
- [ ] Verify structure compliance

### **Before Production**
- [ ] All tests pass (backend + frontend)
- [ ] No linter errors
- [ ] Documentation up to date
- [ ] Docker build successful
- [ ] Performance benchmarks acceptable

---

## 📈 Structure Evolution

### **Version 1.0** (Initial)
- ❌ Monolithic mcp_server.py (459 lines)
- ❌ 27 markdown files at root
- ❌ Scripts scattered everywhere
- ❌ 37 tests (16 redundant)

### **Version 2.0** (Current)
- ✅ Modular mcp/ structure
- ✅ 5 markdown files at root (-81%)
- ✅ All scripts centralized
- ✅ 21 focused unit tests
- ✅ Strict conventions enforced
- ✅ Production-ready structure

---

## 🔒 Enforcement

### **Pre-commit Hooks**
```yaml
# .pre-commit-config.yaml
- Ruff (Python linting)
- Ruff format (Python formatting)
- Prettier (JS/JSON/CSS/MD formatting)
```

### **Makefile Targets**
```makefile
make lint       # Check code quality
make format     # Auto-format code
make test       # Run all tests
make clean      # Clean build artifacts
```

### **Editor Config**
```ini
# .editorconfig
- Consistent indentation
- Trailing whitespace removal
- Final newline enforcement
```

---

## 📚 Quick Reference

**Start Development:**
```bash
./scripts/start-dev.sh
```

**Run Tests:**
```bash
make test
```

**Clean Codebase:**
```bash
./scripts/cleanup-unused-code.sh
```

**Generate Code:**
```
/api /endpoint POST
/component ComponentName
/test file_to_test.py
```

**Check Structure:**
```bash
ls -1 *.md | wc -l  # Should be ≤ 5
```

---

## 🎉 Benefits of Strict Structure

1. **Predictable** - Always know where to find things
2. **Scalable** - Structure grows with project
3. **Professional** - Industry best practices
4. **Fast** - Optimized for M3 Max hardware
5. **Maintainable** - Easy to onboard new developers
6. **Clean** - No clutter, no confusion
7. **Testable** - Clear test organization
8. **Documented** - Everything is documented

---

**This structure is enforced and maintained.** 🔒

**Any deviations should be documented and justified.** ✅

**New team members: Start with `docs/setup/START_HERE.md`** 🚀

