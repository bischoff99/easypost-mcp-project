# Project Structure Cleanup Plan

**Status:** ✅ **COMPLETED** (January 2025)
**Goal:** Organize project structure following common conventions without over-engineering.

**Principle:** Keep it simple - this is a personal project, not enterprise infrastructure.

---

## ✅ Completed Actions

1. ✅ **Test files:** All test files are in `backend/tests/` (completed)
2. ✅ **Docker files:** All Docker files are in `docker/` directory (completed)
3. ✅ **Generated files:** `shipping-labels/` moved to `data/` or gitignored (completed)
4. ✅ **API testing file:** `api-requests.http` moved to `docs/` (completed)
5. ⚠️ **Frontend e2e naming:** Still using `e2e-tests/` (low priority)
6. ✅ **Root node_modules:** Verified no root node_modules without workspace config (completed)

---

## Simple Migration Plan

### Step 1: Move Test Files (5 min)

```bash
mv backend/test_*.py backend/tests/
```

**Why:** All tests should be in `tests/` directory.
**Risk:** Low - pytest will find them automatically.

---

### Step 2: Group Docker Files (5 min)

```bash
mkdir docker
mv docker-compose.yml docker/
mv docker-compose.prod.yml docker/
mv nginx-local.conf docker/
```

**Why:** Keeps Docker-related files together.
**Risk:** Medium - need to update references.

**Files to update:**

- `Makefile` (3 places)
- `.github/workflows/m3max-ci.yml` (3 places)
- `scripts/benchmark.sh` (2 places)
- `scripts/validate-project-structure.py` (1 place)

---

### Step 3: Move Generated Files (2 min)

```bash
mkdir -p data
mv shipping-labels data/
```

**Why:** Generated files shouldn't clutter root.
**Risk:** Low - already in `.gitignore`.

---

### Step 4: Move API Testing File (1 min)

```bash
mv api-requests.http docs/
```

**Why:** Documentation/testing files belong in `docs/`.
**Risk:** Low - no code dependencies.

---

### Step 5: Rename E2E Directory (2 min)

```bash
mv frontend/e2e-tests frontend/e2e
```

**Why:** Shorter, standard naming.
**Risk:** Low - only eslint config needs update.

**File to update:**

- `frontend/eslint.config.js` (line 8)

---

### Step 6: Cleanup Root (1 min)

```bash
rm -rf node_modules  # Only if no root package.json exists
```

**Why:** Shouldn't exist without workspace config.
**Risk:** Low - verified no root package.json.

---

### Step 7: Update References (15 min)

Update all file paths in:

- `Makefile` - Change `docker-compose` to `docker compose -f docker/docker-compose.yml`
- `.github/workflows/m3max-ci.yml` - Same change
- `scripts/benchmark.sh` - Update path
- `scripts/validate-project-structure.py` - Update path
- `frontend/eslint.config.js` - Change `e2e-tests` to `e2e`

---

## Quick Validation

After all steps:

```bash
# Test discovery
cd backend && pytest tests/ -v --collect-only | grep test_create_bulk

# Docker works
docker compose -f docker/docker-compose.yml config

# Build works
make build

# Tests pass
make test
```

---

## Timeline

**Total Time:** ~30 minutes
**Complexity:** Low
**Risk:** Low-Medium (manageable)

---

## What We're NOT Doing

- ❌ Complex validation frameworks
- ❌ Enterprise monitoring setup
- ❌ Over-documentation
- ❌ Turborepo migration (Makefile works fine)
- ❌ Kubernetes manifests (Docker Compose is enough)
- ❌ Service mesh (overkill for personal project)

---

## What We ARE Doing

- ✅ Clean file organization
- ✅ Standard directory structure
- ✅ Simple, maintainable layout
- ✅ Easy to navigate
- ✅ Follows common conventions

---

**That's it.** Simple, practical, gets the job done.
