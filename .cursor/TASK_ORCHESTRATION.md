# Task Orchestration Strategy - Cline Subagents

## Overview
This document outlines how improvements can be parallelized using Cline's subagent system. Each subagent can work independently on isolated tasks.

## Subagent Architecture

### Subagent 1: Frontend Security & Dependencies
**Isolation**: Frontend only, package.json + node_modules
**Tasks**:
- [x] Update Vite 5.4.21 → 7.1.12 (security)
- [ ] Update React Router 6.30.1 → 7.1.0
- [ ] Update TanStack Query 5.90.6 → latest
- [ ] Audit npm packages with `npm audit fix`

**Commands**:
```bash
cd frontend
npm install vite@^7.1.12 --save-dev
npm install react-router-dom@^7.1.0
npm install @tanstack/react-query@latest
npm audit fix
npm test -- --run
npm run build
```

**Conflicts**: None (frontend isolated)
**Time**: 30 minutes

---

### Subagent 2: Backend Security & Updates
**Isolation**: Backend only, requirements.txt + venv
**Tasks**:
- [ ] Update FastAPI 0.120.4 → 0.121.0
- [ ] Update Starlette 0.49.3 → 0.50.0
- [ ] Update pydantic 2.12.3 → 2.13.0
- [ ] Add input length limits to Pydantic models
- [ ] Add specific exception handlers

**Commands**:
```bash
cd backend
source venv/bin/activate
pip install --upgrade fastapi starlette pydantic
pytest tests/ -v
```

**Files to modify**:
- `backend/src/services/easypost_service.py` (add Field limits)
- `backend/src/mcp/tools/*.py` (specific exceptions)

**Conflicts**: None (backend isolated)
**Time**: 1 hour

---

### Subagent 3: Frontend Features (TODOs + Toasts)
**Isolation**: Frontend src/pages + src/services
**Tasks**:
- [ ] Implement TODO in SettingsPage.jsx (API call)
- [ ] Implement TODO in DashboardPage.jsx (navigation)
- [ ] Install and configure Sonner toast library
- [ ] Replace console.log with toast notifications
- [ ] Add loading states with skeletons

**Commands**:
```bash
cd frontend
npm install sonner
```

**Files to modify**:
- `frontend/src/pages/SettingsPage.jsx`
- `frontend/src/pages/DashboardPage.jsx`
- `frontend/src/App.jsx` (add Toaster component)
- `frontend/src/services/api.js` (add toast on errors)

**Conflicts**: Potential with Subagent 1 (package.json)
**Solution**: Run after Subagent 1 completes
**Time**: 1.5 hours

---

### Subagent 4: Frontend Performance (Splitting + Lazy)
**Isolation**: Frontend vite.config.js + App.jsx
**Tasks**:
- [ ] Add manual chunks to Vite config
- [ ] Implement lazy loading for routes
- [ ] Add React.Suspense with fallbacks
- [ ] Optimize bundle size

**Files to modify**:
- `frontend/vite.config.js` (manualChunks)
- `frontend/src/App.jsx` (lazy imports)

**Conflicts**: Potential with Subagent 3 (App.jsx)
**Solution**: Coordinate file edits or merge after
**Time**: 1 hour

---

### Subagent 5: Backend Features (Database Integration)
**Isolation**: Backend new files + server.py
**Tasks**:
- [ ] Install SQLAlchemy + asyncpg + alembic
- [ ] Create database models (Shipment, Address, Analytics)
- [ ] Add database connection management
- [ ] Create repository layer
- [ ] Update endpoints to use database

**Commands**:
```bash
cd backend
source venv/bin/activate
pip install sqlalchemy[asyncio] asyncpg alembic
alembic init alembic
```

**New files**:
- `backend/src/db/__init__.py`
- `backend/src/db/models.py`
- `backend/src/db/database.py`
- `backend/src/repositories/shipment_repo.py`
- `backend/alembic/versions/*.py`

**Conflicts**: Moderate with Subagent 2 (server.py)
**Solution**: Run after Subagent 2 or careful merge
**Time**: 4-6 hours

---

### Subagent 6: Monitoring & Error Tracking
**Isolation**: New middleware + config
**Tasks**:
- [ ] Install Sentry SDK (backend + frontend)
- [ ] Configure Sentry in backend server.py
- [ ] Configure Sentry in frontend main.jsx
- [ ] Add error boundaries with Sentry integration
- [ ] Add performance monitoring

**Commands**:
```bash
cd backend
pip install sentry-sdk[fastapi]

cd ../frontend
npm install @sentry/react @sentry/vite-plugin
```

**Files to modify**:
- `backend/src/server.py` (Sentry init)
- `frontend/src/main.jsx` (Sentry init)
- `frontend/vite.config.js` (Sentry plugin)
- `backend/src/utils/config.py` (SENTRY_DSN)

**Conflicts**: Low (new middleware/config)
**Time**: 2 hours

---

### Subagent 7: Testing Improvements
**Isolation**: Test files only
**Tasks**:
- [ ] Add component tests for ShipmentTable
- [ ] Add component tests for CSVUpload
- [ ] Add component tests for Dashboard cards
- [ ] Add integration tests for API endpoints
- [ ] Increase test coverage to 95%+

**New files**:
- `frontend/src/components/__tests__/*.test.jsx`
- `backend/tests/integration/*.py`

**Conflicts**: None (test files isolated)
**Time**: 3-4 hours

---

### Subagent 8: Frontend Data Integration
**Isolation**: Frontend pages + API service
**Tasks**:
- [ ] Connect Dashboard to real /metrics endpoint
- [ ] Connect Analytics to real shipment data
- [ ] Remove all mock data
- [ ] Add data refresh intervals
- [ ] Add error states for failed API calls

**Files to modify**:
- `frontend/src/pages/DashboardPage.jsx`
- `frontend/src/pages/AnalyticsPage.jsx`
- `frontend/src/services/api.js` (new endpoints)
- `frontend/src/mocks/*` (delete mock files)

**Conflicts**: Moderate with Subagent 3 (DashboardPage)
**Solution**: Coordinate or merge carefully
**Time**: 2-3 hours

---

## Execution Strategy

### Phase 1: Parallel (No Conflicts) - 30-60 mins
Run simultaneously:
- ✅ **Subagent 1**: Frontend dependencies
- ✅ **Subagent 2**: Backend updates
- ✅ **Subagent 7**: Testing improvements

### Phase 2: Sequential Frontend - 2-3 hours
After Phase 1:
1. **Subagent 3**: Frontend features (TODOs + toasts)
2. **Subagent 4**: Frontend performance (after 3)
3. **Subagent 8**: Data integration (after 3)

### Phase 3: Major Features - 4-8 hours
After Phase 2:
- **Subagent 5**: Database integration (backend)
- **Subagent 6**: Monitoring/Sentry (both)

### Phase 4: Validation - 1 hour
- Run all tests
- Build production
- Verify deployments
- Update documentation

---

## Cline Subagent Commands

### Create Subagent 1 (Frontend Deps)
```bash
cline create-subagent \
  --name "frontend-deps" \
  --scope "frontend/package*.json,frontend/vite.config.js" \
  --task "Update Vite to 7.1.12, run tests, verify build" \
  --timeout 30m
```

### Create Subagent 2 (Backend Updates)
```bash
cline create-subagent \
  --name "backend-updates" \
  --scope "backend/requirements.txt,backend/src/services/easypost_service.py" \
  --task "Update FastAPI/Starlette, add Field limits, run tests" \
  --timeout 60m
```

### Create Subagent 3 (Frontend Features)
```bash
cline create-subagent \
  --name "frontend-features" \
  --scope "frontend/src/pages/*.jsx,frontend/src/services/api.js" \
  --task "Implement TODOs, add Sonner toasts, remove console.log" \
  --timeout 90m \
  --depends-on frontend-deps
```

### Coordinate with Main Agent
```bash
cline coordinate \
  --merge-strategy "sequential" \
  --conflict-resolution "ask" \
  --notify-completion true
```

---

## File Ownership Map

### Backend (No Conflicts)
- **Subagent 2**: `requirements.txt`, `src/services/*.py`
- **Subagent 5**: `src/db/**`, `repositories/**`, `alembic/**`
- **Subagent 6**: `src/server.py` (monitoring section only)
- **Subagent 7**: `tests/**`

### Frontend (Potential Conflicts)
- **Subagent 1**: `package*.json`, `vite.config.js` (deps only)
- **Subagent 3**: `pages/*.jsx`, `services/api.js`
- **Subagent 4**: `vite.config.js` (config only), `App.jsx` (routes)
- **Subagent 6**: `main.jsx` (Sentry only)
- **Subagent 7**: `**/__tests__/**`
- **Subagent 8**: `pages/*.jsx` (data fetching)

### Conflict Resolution
1. **vite.config.js**: Subagent 1 first (deps), then Subagent 4 (config)
2. **App.jsx**: Subagent 3 (Toaster), then Subagent 4 (lazy routes)
3. **pages/*.jsx**: Subagent 3 (TODOs), then Subagent 8 (data)

---

## Progress Tracking

```bash
# Monitor all subagents
cline status --all

# Check specific subagent
cline status frontend-deps

# Merge completed work
cline merge frontend-deps --strategy rebase

# Handle conflicts
cline resolve-conflicts --interactive
```

---

## Success Criteria

### Phase 1 Complete
- ✅ All packages updated
- ✅ All tests passing
- ✅ No security warnings

### Phase 2 Complete
- ✅ TODOs implemented
- ✅ Toast notifications working
- ✅ Bundle size optimized
- ✅ Real data connected

### Phase 3 Complete
- ✅ Database integrated
- ✅ Sentry tracking errors
- ✅ 95%+ test coverage

### Final Validation
- ✅ Production build successful
- ✅ All endpoints responding
- ✅ Frontend loads < 2s
- ✅ No console errors
- ✅ Documentation updated

---

## Estimated Timeline

**With Cline Subagents (Parallel)**:
- Phase 1: 60 minutes
- Phase 2: 3 hours (sequential)
- Phase 3: 6 hours (parallel)
- Phase 4: 1 hour
**Total**: ~10 hours → Can be done in 1 day

**Without Subagents (Sequential)**:
- All tasks done serially
**Total**: ~18 hours → 2-3 days

**Speedup**: 45% faster with parallelization
