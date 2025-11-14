# EasyPost MCP Project - Complete Codebase Analysis

**Generated**: 2025-11-14  
**Project Type**: Personal-use shipping integration  
**Architecture**: FastAPI Backend + React Frontend + MCP Server

---

## 📊 Project Overview

### What This Project Does

EasyPost MCP is a **personal-use shipping management system** that integrates with the EasyPost API to:

1. **Create and manage shipments** (domestic & international)
2. **Compare shipping rates** across multiple carriers (USPS, FedEx, UPS, etc.)
3. **Track packages** with real-time updates
4. **Generate shipping labels** and customs forms
5. **Provide AI agent tools** via MCP (Model Context Protocol) for automation

### Key Philosophy

**Built for personal use, not enterprise scale:**
- YAGNI principle (You Aren't Gonna Need It)
- Simple > Complex
- Direct API calls > Database caching
- Single user > Multi-tenancy
- Maintainable by one person

---

## 🏗️ Architecture

### High-Level Structure

```
┌─────────────────────────────────────────────────────────┐
│                   CLAUDE DESKTOP                        │
│            (AI Assistant with MCP Client)               │
└────────────────────┬────────────────────────────────────┘
                     │ stdio transport
                     ▼
┌─────────────────────────────────────────────────────────┐
│              MCP SERVER (Core Product)                  │
│  FastMCP + Python - 6 Tools for AI Agents              │
│  Location: apps/backend/src/mcp_server/                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              FASTAPI BACKEND                            │
│  REST API + Business Logic + EasyPost Integration      │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│  EASYPOST API    │    │  REACT FRONTEND  │
│  (External SaaS) │    │  Vite + TailwindCSS│
└──────────────────┘    └──────────────────┘
```


### Technology Stack

**Backend (Python)**:
- **FastAPI** 0.100+ - Modern async web framework
- **FastMCP** 2.13.0 - MCP server implementation
- **EasyPost** 10.0+ - Shipping API client
- **Pydantic** 2.5+ - Data validation
- **SQLAlchemy** 2.0+ - Database ORM (minimal use)
- **Uvicorn** - ASGI server

**Frontend (JavaScript)**:
- **React** 19.2.0 - UI library
- **Vite** 7.2.1 - Build tool
- **TailwindCSS** 4.1.17 - Styling
- **Radix UI** - Accessible components
- **React Query** - Server state management
- **Zustand** - Client state management

**Development**:
- **pytest** 7.4.3 - Python testing (8 parallel workers)
- **Vitest** 4.0.8 - JavaScript testing
- **Ruff** - Python linting/formatting
- **ESLint** + **Prettier** - JavaScript quality

---

## 📁 Project Structure (Monorepo)


```
easypost-mcp-project/
├── apps/
│   ├── backend/              # Python FastAPI + MCP Server
│   │   ├── src/
│   │   │   ├── mcp_server/   # ⭐ Core Product: MCP Tools
│   │   │   │   ├── tools/    # 6 AI agent tools
│   │   │   │   ├── resources/# Dynamic data providers
│   │   │   │   └── prompts/  # Workflow templates
│   │   │   ├── routers/      # REST API endpoints
│   │   │   ├── services/     # Business logic
│   │   │   ├── models/       # Pydantic models
│   │   │   └── utils/        # Config, monitoring
│   │   ├── tests/            # Unit + Integration tests
│   │   ├── requirements.txt  # Python dependencies
│   │   └── run_mcp.py        # MCP server entry point
│   │
│   └── frontend/             # React Vite Application
│       ├── src/
│       │   ├── pages/        # Route components
│       │   ├── components/   # Reusable UI
│       │   ├── services/     # API client
│       │   └── tests/        # Component tests
│       └── package.json      # Node dependencies
│
├── deploy/                   # Docker configurations
├── docs/                     # Project documentation
├── scripts/                  # Utility bash scripts
├── .cursor/                  # Cursor IDE configuration
│   ├── mcp.json             # MCP server config
│   └── rules/               # Coding standards
└── Makefile                 # Development commands
```


---

## 🎯 Core Components

### 1. MCP Server (Core Product)

**Location**: `apps/backend/src/mcp_server/`

**Purpose**: AI agent tools for Claude Desktop and other MCP clients

**6 Tools Exposed**:

| Tool | Purpose | Parameters | Returns |
|------|---------|------------|---------|
| `get_tracking` | Track shipment | tracking_number | Status, location, history |
| `get_shipment_rates` | Get shipping rates | addresses, parcel, qty | Rates from all carriers |
| `create_shipment` | Create shipment | spreadsheet data | Shipment ID + rates |
| `buy_shipment_label` | Purchase label | shipment_id, rate_id | Tracking + label URL |
| `download_shipment_documents` | Download PDFs | shipment_ids, type | Local file paths |
| `refund_shipment` | Refund shipment | shipment_ids | Refund status |

**Architecture Pattern**: Two-Phase Workflow
- **Phase 1**: `create_shipment()` - Get rates, select best option
- **Phase 2**: `buy_shipment_label()` - Purchase selected rate

**Key Features**:
- Async-first design (all I/O operations)
- 20-second timeout protection (prevents SSE hangs)
- Standardized response format: `{"status", "data", "message", "timestamp"}`
- Context-aware progress reporting
- Bulk operations with parallel processing

**Example Usage**:
```python
# From Claude Desktop
"Create 10 shipments from Los Angeles to New York"
  → create_shipment() with spreadsheet data
  → Returns all available rates
  → User selects USPS Ground
  → buy_shipment_label() with rate ID
  → Returns tracking numbers and label URLs
```


### 2. FastAPI Backend

**Location**: `apps/backend/src/`

**Purpose**: REST API for React frontend + MCP HTTP transport

**Endpoints**:
```
GET  /                    # Root endpoint
GET  /health             # Health check
GET  /docs               # Swagger documentation

POST /api/rates          # Get shipping rates
POST /api/shipments      # Create shipment
GET  /api/shipments      # List shipments
GET  /api/tracking/{num} # Track package
GET  /api/analytics      # Dashboard stats

POST /mcp                # MCP HTTP transport (SSE)
```

**Service Layer** (`services/`):
- **EasyPostService** - Main integration with EasyPost API
  - Rate fetching
  - Shipment creation
  - Address verification
  - Label purchasing
  - Tracking
- **SmartCustoms** - Automatic customs form generation
  - EEL/PFC determination
  - HS code lookup
  - Value calculation

**Key Patterns**:
- Dependency injection with `Depends()`
- Pydantic request/response models
- Structured error responses
- Comprehensive logging with context
- Async database operations (minimal use)


### 3. React Frontend

**Location**: `apps/frontend/src/`

**Purpose**: User interface for shipment management

**Pages** (`pages/`):
- **Dashboard** - Overview, recent shipments, stats
- **Shipments** - Create and manage shipments
- **Analytics** - Charts and visualizations
- **Tracking** - Track packages
- **Settings** - Configuration

**Component Structure** (`components/`):
```
components/
├── layout/
│   ├── Header.jsx          # Navigation bar
│   └── Sidebar.jsx         # Side navigation
├── shipments/
│   ├── ShipmentForm.jsx    # Create shipment form
│   ├── ShipmentList.jsx    # List view
│   └── ShipmentCard.jsx    # Individual card
├── analytics/
│   ├── StatsCard.jsx       # Metric display
│   └── RateChart.jsx       # Recharts visualization
└── ui/                      # Radix UI primitives
    ├── Button.jsx
    ├── Input.jsx
    ├── Select.jsx
    └── Dialog.jsx
```

**State Management**:
- **React Query** - Server state (API data, caching)
- **Zustand** - Client state (UI state, preferences)
- Local state with `useState` for component-specific data

**API Integration** (`services/api.js`):
- Axios client with automatic retry (3 attempts)
- Exponential backoff on failures
- Request/response interceptors
- Error normalization


---

## 🔄 Data Flow

### Creating a Shipment (MCP Workflow)

```
┌──────────────┐
│ Claude Desktop│
└───────┬──────┘
        │ "Create shipment from LA to NYC"
        ▼
┌──────────────────┐
│  MCP Tool:       │
│ create_shipment()│  1. Parse request
└───────┬──────────┘  2. Validate addresses
        │             3. Call EasyPost API
        ▼
┌──────────────────┐
│ EasyPostService  │  1. Create shipment object
└───────┬──────────┘  2. Get all carrier rates
        │             3. Return rates for selection
        ▼
┌──────────────────┐
│  Return to AI    │  Rate options:
└───────┬──────────┘  - USPS: $8.50 (2-3 days)
        │             - FedEx: $12.00 (1-2 days)
        │             - UPS: $15.00 (1 day)
        ▼
┌──────────────────┐
│ AI Selects Rate  │  Choose USPS $8.50
└───────┬──────────┘
        │
        ▼
┌──────────────────┐
│  MCP Tool:       │  1. Purchase label
│buy_shipment_label│  2. Generate tracking
└───────┬──────────┘  3. Create label PDF
        │
        ▼
┌──────────────────┐
│ Return Results   │  Tracking: 9400...
└──────────────────┘  Label: shipment_123.pdf
```

### Creating a Shipment (Frontend Workflow)

```
┌──────────────┐
│  React Form  │  User fills form
└───────┬──────┘
        │ Submit
        ▼
┌──────────────────┐
│  API Client      │  POST /api/shipments
│  (axios)         │  with retry logic
└───────┬──────────┘
        │
        ▼
┌──────────────────┐
│ FastAPI Router   │  Validate request
└───────┬──────────┘  Extract parameters
        │
        ▼
┌──────────────────┐
│ EasyPostService  │  Same as MCP flow
└───────┬──────────┘
        │
        ▼
┌──────────────────┐
│ Response to UI   │  Update React Query cache
└───────┬──────────┘  Show success toast
        │             Navigate to tracking
        ▼
┌──────────────────┐
│  Dashboard       │  Display new shipment
└──────────────────┘
```


---

## 🧪 Testing Strategy

### Backend Tests

**Location**: `apps/backend/tests/`

**Structure**:
```
tests/
├── unit/                    # Fast, mocked tests
│   ├── test_easypost_service.py
│   ├── test_bulk_tools.py
│   ├── test_refund_tools.py
│   └── test_tracking_tools.py
└── integration/             # Real API tests
    ├── test_easypost_integration.py
    └── test_endpoints_async.py
```

**Configuration**: `pytest.ini`
- 8 parallel workers (pytest-xdist)
- `--dist loadgroup` for better distribution
- 52.23% coverage (exceeds 50% minimum)
- AsyncIO mode: auto

**Run Tests**:
```bash
pytest -n 8 -v --tb=short tests/     # Full suite (24s)
pytest tests/unit/ -v                 # Unit tests only (fast)
pytest -m integration                 # Integration tests only
```

### Frontend Tests

**Location**: `apps/frontend/src/tests/`

**Framework**: Vitest + React Testing Library

**Types**:
- Component tests (user interactions)
- Hook tests (custom hooks)
- E2E tests (Puppeteer)

**Run Tests**:
```bash
pnpm test                    # Watch mode
pnpm test:run               # Single run
pnpm test:coverage          # With coverage
```


---

## 📦 Dependencies Analysis

### Backend Critical Dependencies

```python
# Core Framework
fastmcp>=2.0.0              # MCP server implementation
fastapi>=0.100.0            # Web framework
easypost>=10.0.0            # EasyPost API client
pydantic>=2.5.0             # Data validation

# Async I/O
uvicorn>=0.24.0             # ASGI server
httpx>=0.25.0               # Async HTTP client
aiofiles>=23.2.1            # Async file operations

# Database (Minimal Use)
sqlalchemy>=2.0.0           # ORM
alembic>=1.12.0             # Migrations
psycopg2-binary>=2.9.0      # PostgreSQL driver

# Testing
pytest>=7.4.3               # Test framework
pytest-asyncio>=0.21.1      # Async test support
pytest-xdist>=3.5.0         # Parallel execution
pytest-cov>=4.0.0           # Coverage reporting

# Code Quality
ruff>=0.1.0                 # Linter + formatter
black>=23.0.0               # Code formatter (backup)
```

**Why These Choices?**:
- **FastMCP**: Official MCP implementation, well-maintained
- **FastAPI**: Best-in-class async Python framework
- **Pydantic**: Type-safe validation, FastAPI integration
- **Ruff**: Modern, fast linter (replaces flake8, isort, pyupgrade)
- **pytest-xdist**: Parallel test execution (8 workers = fast CI)


### Frontend Critical Dependencies

```json
{
  "dependencies": {
    "react": "^19.2.0",                      // UI library
    "react-dom": "^19.2.0",                  // DOM renderer
    "react-router-dom": "^7.9.5",            // Routing
    "@tanstack/react-query": "^5.90.7",      // Server state
    "zustand": "^5.0.8",                     // Client state
    "axios": "^1.13.2",                      // HTTP client
    "@radix-ui/react-*": "^1-2.x",          // Accessible components
    "tailwind-merge": "^3.3.1",              // Class merging
    "clsx": "^2.1.1",                        // Conditional classes
    "recharts": "^3.4.1",                    // Charts
    "sonner": "^2.0.7"                       // Toast notifications
  },
  "devDependencies": {
    "vite": "^7.2.1",                        // Build tool
    "@vitejs/plugin-react": "^5.1.0",       // React plugin
    "tailwindcss": "4.1.17",                 // CSS framework
    "vitest": "4.0.8",                       // Test framework
    "@testing-library/react": "^16.3.0",     // Testing utils
    "eslint": "^9.39.1",                     // Linter
    "prettier": "^3.6.2",                    // Formatter
    "puppeteer": "24.29.1"                   // E2E testing
  }
}
```

**Why These Choices?**:
- **React 19**: Latest version with concurrent features
- **React Query**: Best server state management
- **Radix UI**: Accessible, unstyled components (no JS bundle bloat)
- **TailwindCSS 4**: Utility-first CSS with excellent DX
- **Vite**: Fastest build tool, excellent HMR
- **Vitest**: Vite-native testing, faster than Jest


---

## 🎨 Key Design Decisions

### 1. Personal Use Focus

**Decision**: Optimize for single-user, personal use
- No multi-tenancy
- No complex caching
- No rate limiting
- Direct API calls > Database

**Result**: 
- Simpler codebase
- Easier maintenance
- Faster development
- Lower operational complexity

### 2. MCP as Core Product

**Decision**: Build MCP server tools first, web UI second
- MCP tools are primary interface
- Web UI is convenience layer
- Both share same service layer

**Result**:
- AI-first workflow automation
- Flexibility (CLI, web, or AI)
- Better separation of concerns

### 3. Two-Phase Shipment Creation

**Decision**: Separate rate fetching from label purchasing
- Phase 1: `create_shipment()` returns all rates
- Phase 2: `buy_shipment_label()` purchases selected rate

**Why**:
- User can compare rates before committing
- Prevents accidental purchases
- More control over carrier selection
- Follows EasyPost best practices

### 4. Async-First Architecture

**Decision**: All I/O operations are async
- Database queries
- API calls
- File operations

**Benefits**:
- Better performance
- Handle concurrent requests
- Non-blocking operations
- Scales to moderate load


### 5. Database Removed for Personal Use

**Decision**: Remove database persistence (YAGNI principle)
- All data fetched from EasyPost API on-demand
- No local caching or storage
- Simpler architecture

**Rationale**:
- Personal use doesn't need historical data
- EasyPost API is source of truth
- Fewer moving parts
- No migrations or schema management

**Trade-off**: Higher API usage, but within EasyPost limits for personal use

---

## 🛠️ Working with the Codebase

### Quick Start

```bash
# 1. Clone and setup
git clone <repo>
cd easypost-mcp-project

# 2. Setup environment
cp .env.example .env
# Edit .env with your EasyPost API key

# 3. Install dependencies
make setup

# 4. Run development servers
make dev
# Backend: http://localhost:8000
# Frontend: http://localhost:5173

# 5. Run tests
make test
```

### Common Operations

**Add a New MCP Tool**:
```bash
# 1. Create tool file
touch apps/backend/src/mcp_server/tools/my_tool.py

# 2. Implement tool with @mcp.tool() decorator
# 3. Register in tools/__init__.py
# 4. Write tests in tests/unit/test_my_tool.py
# 5. Test coverage must be 100% for MCP tools
```

**Add a New API Endpoint**:
```bash
# 1. Add route in routers/
# 2. Define Pydantic models in models/requests.py
# 3. Implement business logic in services/
# 4. Write tests in tests/integration/
# 5. Update frontend API client in src/services/api.js
```


**Add a New React Component**:
```bash
# 1. Create component in src/components/
# 2. Use Radix UI primitives from ui/
# 3. Style with TailwindCSS utility classes
# 4. Write tests in src/tests/components/
# 5. Export from component directory index
```

### Development Workflow

**Backend Development**:
```bash
cd apps/backend
source venv/bin/activate

# Run with auto-reload
uvicorn src.server:app --reload --host 0.0.0.0 --port 8000

# Run tests in watch mode
pytest-watch tests/ -v

# Format and lint
ruff format src/ tests/
ruff check src/ tests/ --fix

# Type check
mypy src/
```

**Frontend Development**:
```bash
cd apps/frontend

# Run with HMR
pnpm run dev

# Run tests in watch mode
pnpm test

# Format and lint
pnpm run format
pnpm run lint:fix

# Build for production
pnpm run build
```

### Configuration Files

**Backend**:
- `.env` - Environment variables (API keys, database URL)
- `pyproject.toml` - Ruff, Black, mypy configuration
- `pytest.ini` - Test configuration
- `alembic.ini` - Database migrations

**Frontend**:
- `vite.config.js` - Build configuration
- `tailwind.config.js` - TailwindCSS configuration
- `eslint.config.js` - Linting rules
- `.prettierrc` - Formatting rules


---

## ⚡ Performance Considerations

### Backend Optimizations

**Parallel Processing**:
- pytest with 8 workers (23s for 250 tests)
- Bulk operations use `asyncio.gather()`
- ThreadPoolExecutor for CPU-bound tasks

**Timeout Protection**:
- All API calls: 20-second timeout
- Prevents SSE connection hangs
- Graceful degradation on timeouts

**Connection Pooling**:
- SQLAlchemy: 10 connections + 5 overflow
- HTTP client connection reuse
- Thread-safe EasyPost client

**Caching Strategy**:
- No database caching (YAGNI)
- React Query caches API responses (5 min)
- Browser caches static assets

### Frontend Optimizations

**Code Splitting**:
```javascript
// vite.config.js
manualChunks: {
  'vendor-react': ['react', 'react-dom', 'react-router-dom'],
  'vendor-charts': ['recharts'],
  'vendor-ui': ['@radix-ui/*'],
  'vendor-data': ['@tanstack/react-query', 'zustand']
}
```

**Build Optimizations**:
- esbuild minification (fastest)
- Tree shaking enabled
- CSS code splitting
- Lazy loading for routes
- Pre-transform frequently accessed files

**Bundle Analysis**:
```bash
pnpm run build:analyze
# Opens Rollup bundle analyzer
```


---

## 🐛 Troubleshooting

### Common Issues

**Issue**: MCP server not responding
```bash
# Check if server is running
curl http://localhost:8000/health

# Check logs
tail -f apps/backend/logs/mcp_server.log

# Verify API key
echo $EASYPOST_API_KEY

# Restart server
make dev
```

**Issue**: Tests failing with "API key invalid"
```bash
# Solution: Load .env.test
cd apps/backend
cat .env.test | grep EASYPOST_API_KEY

# Verify conftest.py loads dotenv
grep "load_dotenv" tests/conftest.py
```

**Issue**: Frontend can't connect to backend
```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS configuration
grep CORS_ORIGINS apps/backend/.env

# Verify Vite proxy
grep proxy apps/frontend/vite.config.js
```

**Issue**: Coverage below 50%
```bash
# Run with coverage report
pytest --cov=src --cov-report=html

# Open report
open htmlcov/index.html

# Find uncovered lines
pytest --cov=src --cov-report=term-missing
```


---

## 📈 Project Metrics

### Codebase Size

```
Backend:
  Source:         3,077 lines (Python)
  Tests:          ~2,500 lines
  Coverage:       52.23%
  MCP Tools:      6 tools, ~841 lines
  
Frontend:
  Source:         ~5,000 lines (JSX)
  Tests:          ~800 lines
  Components:     40+ components
  
Total:          ~11,377 lines of code
```

### Performance Benchmarks

```
Backend:
  Test Suite:     24.17s (250 tests, 8 workers)
  API Response:   ~100-300ms average
  Build Time:     ~5s (production)

Frontend:
  Test Suite:     ~10s (vitest)
  Build Time:     ~15s (production)
  Bundle Size:    ~500KB (gzipped)
  HMR:           <100ms (development)

MCP Server:
  Tool Response:  1-3s (with EasyPost API)
  Bulk Ops:       10 shipments ~1.1s (parallel)
```

### Code Quality

```
Backend:
  Ruff:          ✅ 0 errors
  mypy:          ✅ Type-safe
  Black:         ✅ Formatted
  
Frontend:
  ESLint:        ✅ 0 errors
  Prettier:      ✅ Formatted
  TypeScript:    ⚠️  Using JSX (not TS)
```


---

## 🎯 Summary & Recommendations

### What This Codebase Does Well

✅ **Clean Architecture**: Clear separation of MCP tools, API, and UI
✅ **Modern Stack**: Latest versions of FastAPI, React, Vite
✅ **Async-First**: All I/O operations properly async
✅ **Type Safety**: Pydantic models everywhere
✅ **Test Coverage**: 52% (exceeds minimum)
✅ **MCP Compliance**: 95/100 score, production-ready
✅ **Personal Use Focus**: Simple, maintainable, no over-engineering

### Areas for Improvement (Optional)

**Short Term**:
1. Increase test coverage to 70% (currently 52%)
2. Add TypeScript to frontend (currently using JSX)
3. Add E2E tests for critical workflows

**Medium Term**:
1. Add performance monitoring (OpenTelemetry)
2. Implement request caching strategy
3. Add more MCP tools (address validation, batch tracking)

**Long Term**:
1. Add GraphQL API layer (optional)
2. Implement WebSocket for real-time tracking
3. Add mobile-responsive design improvements

### Getting Started Checklist

For new developers:

- [ ] Clone repository
- [ ] Install dependencies (`make setup`)
- [ ] Get EasyPost API key (test mode)
- [ ] Configure `.env` file
- [ ] Run tests (`make test`)
- [ ] Start dev servers (`make dev`)
- [ ] Read `CLAUDE.md` for AI assistant guide
- [ ] Review `.cursor/rules/` for coding standards

### Key Files to Understand

**Must Read**:
1. `README.md` - Project overview
2. `CLAUDE.md` - Comprehensive dev guide
3. `apps/backend/src/mcp_server/__init__.py` - MCP registration
4. `apps/backend/src/services/easypost_service.py` - Core logic
5. `apps/frontend/src/App.jsx` - Frontend entry point

**Architecture Docs**:
1. `docs/reviews/MCP_PROTOCOL_COMPLIANCE_REVIEW.md` - MCP analysis
2. `docs/architecture/POSTGRESQL_ARCHITECTURE.md` - Database design
3. `TEST_SUMMARY.md` - Latest test results

---

## 📚 Additional Resources

- **EasyPost API**: https://www.easypost.com/docs/api
- **FastMCP**: https://github.com/jlowin/fastmcp
- **FastAPI**: https://fastapi.tiangolo.com/
- **React Query**: https://tanstack.com/query/latest
- **Vite**: https://vitejs.dev/

---

**Analysis Complete** ✅  
**Generated**: 2025-11-14  
**Codebase Version**: 0.1.0  
**Status**: Production Ready
