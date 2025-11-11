# Workspace Structure Review (Nov 2025)

## Executive Summary

This review examines the EasyPost MCP project structure against November 2025 development standards. The project follows a **monorepo pattern** with separate `backend/` (FastAPI/Python) and `frontend/` (React/Vite) directories. Recent cleanup has improved organization, but several standardization opportunities remain.

**Key Findings:**
- ✅ Good separation of concerns (backend/frontend)
- ✅ Modern tooling (Ruff, ESLint 9, Vite 7, React 19)
- ⚠️ Dockerfiles scattered (should consolidate)
- ⚠️ Configuration files inconsistent placement
- ⚠️ Missing `.dockerignore` files
- ⚠️ Duplicate config files (`.eslintrc.json` + `eslint.config.js`)

---

## 1. Standards Reference

### General Project Structure (2025)
- **Source:** [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices), [Python Project Template](https://github.com/pypa/sampleproject)
- **Key Points:**
  - `src/` for source code (or language-specific root)
  - `tests/` at root or per-service
  - `docs/` for documentation
  - `scripts/` for utility scripts
  - `config/` or `.config/` for configuration files
  - Root-level config files (`.gitignore`, `README.md`, `LICENSE`)

### Node.js/JavaScript/TypeScript (2025)
- **Source:** [ESLint 9 Flat Config](https://eslint.org/docs/latest/use/configure/configuration-files-new), [Vite 7 Best Practices](https://vite.dev/guide/)
- **Key Points:**
  - ESLint 9 uses `eslint.config.js` (flat config) - legacy `.eslintrc.json` deprecated
  - Prettier config: `.prettierrc` or `prettier.config.js` at root or per-service
  - `package.json` at service root
  - `tsconfig.json` for TypeScript projects (not present - JS only)

### Docker/Container Standards (2025)
- **Source:** [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/), [Docker Compose V2](https://docs.docker.com/compose/)
- **Key Points:**
  - Dockerfiles at service root (`backend/Dockerfile`, `frontend/Dockerfile`)
  - `.dockerignore` alongside each Dockerfile
  - Compose files in `docker/` directory (✅ already done)
  - Multi-stage builds for production (✅ already implemented)

### Frontend Framework (React 2025)
- **Source:** [React 19 Docs](https://react.dev/), [Vite React Template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react)
- **Key Points:**
  - `src/` for source code
  - `src/components/` for reusable components
  - `src/pages/` or `src/routes/` for page components
  - `public/` for static assets
  - `e2e/` for end-to-end tests (✅ already renamed)

### Monorepo Patterns (2025)
- **Source:** [Turborepo](https://turbo.build/repo/docs), [Nx](https://nx.dev/), [pnpm workspaces](https://pnpm.io/workspaces)
- **Key Points:**
  - Service-specific directories (`backend/`, `frontend/`)
  - Shared configs at root (`.prettierrc`, `.gitignore`)
  - Service-specific configs in service directories
  - Root-level `Makefile` for orchestration (✅ present)

---

## 2. Current Layout Audit

### Directory Tree (Top Level)

```
easypost-mcp-project/
├── backend/                    # Python/FastAPI service
│   ├── src/                   # ✅ Source code
│   ├── tests/                 # ✅ Tests (recently organized)
│   ├── alembic/               # ✅ Database migrations
│   ├── Dockerfile             # ⚠️ Should have .dockerignore
│   ├── Dockerfile.prod        # ⚠️ Should consolidate or document
│   ├── pyproject.toml         # ✅ Modern Python config
│   └── requirements.txt       # ✅ Dependencies
├── frontend/                   # React/Vite service
│   ├── src/                   # ✅ Source code
│   ├── e2e/                   # ✅ E2E tests (recently renamed)
│   ├── Dockerfile             # ⚠️ Should have .dockerignore
│   ├── Dockerfile.prod        # ⚠️ Should consolidate or document
│   ├── eslint.config.js       # ✅ ESLint 9 flat config
│   ├── .eslintrc.json         # ❌ Legacy config (duplicate)
│   ├── package.json           # ✅ Dependencies
│   └── vite.config.js         # ✅ Build config
├── docker/                     # ✅ Docker Compose files (recently moved)
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   └── nginx-local.conf
├── docs/                      # ✅ Documentation
├── scripts/                   # ✅ Utility scripts
├── data/                      # ✅ Generated data (recently created)
├── .prettierrc                # ✅ Root-level config
├── .gitignore                 # ✅ Root-level ignore
├── Makefile                   # ✅ Orchestration
├── README.md                  # ✅ Project docs
└── LICENSE                    # ✅ License file
```

### Configuration Files Analysis

| File | Location | Standard Expected | Status |
|------|----------|-------------------|--------|
| `Dockerfile` | `backend/`, `frontend/` | Service root | ✅ Correct |
| `.dockerignore` | Missing | Alongside Dockerfile | ❌ Missing |
| `docker-compose.yml` | `docker/` | `docker/` or root | ✅ Correct (recently moved) |
| `eslint.config.js` | `frontend/` | Service root | ✅ Correct |
| `.eslintrc.json` | `frontend/` | Deprecated (ESLint 9) | ❌ Duplicate/legacy |
| `.prettierrc` | Root + `frontend/` | Root only (monorepo) | ⚠️ Duplicate |
| `pyproject.toml` | `backend/` | Service root | ✅ Correct |
| `package.json` | `frontend/` | Service root | ✅ Correct |
| `.gitignore` | Root | Root | ✅ Correct |

---

## 3. Comparative Analysis

### ✅ Matches Standards

1. **Monorepo Structure**: Clear separation of `backend/` and `frontend/` services
2. **Source Organization**: `src/` directories properly structured
3. **Test Organization**: `tests/` directories with `unit/` and `integration/` subdirectories
4. **Docker Compose**: Recently moved to `docker/` directory (best practice)
5. **Modern Tooling**: ESLint 9 flat config, Ruff for Python, Vite 7
6. **Documentation**: Comprehensive `docs/` structure

### ⚠️ Partially Matches Standards

1. **Dockerfiles**: Present but missing `.dockerignore` files (performance/security impact)
2. **Prettier Config**: Duplicate at root and `frontend/` (should be root-only for monorepo)
3. **ESLint Config**: Both `eslint.config.js` (modern) and `.eslintrc.json` (legacy) present

### ❌ Deviations from Standards

1. **Missing `.dockerignore`**: 
   - Impact: Larger Docker build context, slower builds, potential security issues
   - Standard: Each Dockerfile should have `.dockerignore` alongside

2. **Duplicate ESLint Config**:
   - Impact: Confusion about which config is active, potential conflicts
   - Standard: ESLint 9 uses `eslint.config.js` only, `.eslintrc.json` deprecated

3. **Duplicate Prettier Config**:
   - Impact: Inconsistent formatting, maintenance overhead
   - Standard: Monorepo should have single root-level `.prettierrc`

4. **Dockerfile.prod Files**:
   - Impact: Unclear when to use which Dockerfile
   - Standard: Either consolidate or document clearly, or use build args

5. **Missing CI/CD Config**:
   - Impact: No automated testing/deployment
   - Note: May be intentional for personal project

---

## 4. Improvement & Standardisation Plan

### Milestone 1: Docker Standardisation (15 min)

#### Issue 1.1: Add `.dockerignore` Files

**Goal:** Reduce Docker build context size and improve build performance.

**Proposed Change:** Create `.dockerignore` files alongside each Dockerfile.

**Sequential Steps:**
1. Create `backend/.dockerignore`:
```bash
cat > backend/.dockerignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
env/
.venv
*.egg-info/
.pytest_cache/
htmlcov/
.coverage

# IDE
.vscode/
.idea/
*.swp

# Logs
logs/
*.log

# Tests
tests/
test_*.py

# Development
.env
.env.local
*.md
!README.md
EOF
```

2. Create `frontend/.dockerignore`:
```bash
cat > frontend/.dockerignore << 'EOF'
# Dependencies
node_modules/
npm-debug.log*

# Build outputs
dist/
coverage/
*.log

# IDE
.vscode/
.idea/
*.swp

# Tests
e2e/
src/tests/
*.test.js
*.test.jsx

# Development
.env
.env.local
*.md
!README.md
EOF
```

3. Validate: `docker compose -f docker/docker-compose.yml build --dry-run` (if supported) or check build context size.

---

#### Issue 1.2: Document Dockerfile.prod Usage

**Goal:** Clarify when to use `Dockerfile` vs `Dockerfile.prod`.

**Proposed Change:** Add comments to Dockerfiles or create `docker/README.md`.

**Sequential Steps:**
1. Create `docker/README.md`:
```markdown
# Docker Configuration

## Files

- `docker-compose.yml` - Development environment
- `docker-compose.prod.yml` - Production environment
- `nginx-local.conf` - Nginx configuration for local development

## Dockerfiles

- `backend/Dockerfile` - Development build
- `backend/Dockerfile.prod` - Production build (multi-stage, optimized)
- `frontend/Dockerfile` - Development build
- `frontend/Dockerfile.prod` - Production build (multi-stage, nginx)

## Usage

Development:
```bash
docker compose -f docker/docker-compose.yml up
```

Production:
```bash
docker compose -f docker/docker-compose.prod.yml up
```
```

2. Validate: Verify README is clear and accurate.

---

### Milestone 2: Configuration Cleanup (10 min)

#### Issue 2.1: Remove Legacy ESLint Config

**Goal:** Eliminate confusion and use only ESLint 9 flat config.

**Proposed Change:** Remove `frontend/.eslintrc.json` (already using `eslint.config.js`).

**Sequential Steps:**
1. Verify `eslint.config.js` is complete:
```bash
cd frontend && npm run lint
```

2. Remove legacy config:
```bash
rm frontend/.eslintrc.json
```

3. Validate: `cd frontend && npm run lint` (should still work).

---

#### Issue 2.2: Consolidate Prettier Config

**Goal:** Single source of truth for formatting in monorepo.

**Proposed Change:** Remove `frontend/.prettierrc`, use root `.prettierrc` only.

**Sequential Steps:**
1. Verify root `.prettierrc` exists and is complete:
```bash
cat .prettierrc
```

2. Remove duplicate:
```bash
rm frontend/.prettierrc
```

3. Validate: `cd frontend && npm run format:check` (should use root config).

---

### Milestone 3: Documentation Updates (5 min)

#### Issue 3.1: Update README Structure Section

**Goal:** Document final project structure.

**Proposed Change:** Add "Project Structure" section to root `README.md`.

**Sequential Steps:**
1. Read current `README.md`:
```bash
cat README.md
```

2. Add structure section:
```markdown
## Project Structure

```
easypost-mcp-project/
├── backend/          # FastAPI/Python backend service
├── frontend/         # React/Vite frontend service
├── docker/           # Docker Compose configurations
├── docs/             # Project documentation
├── scripts/          # Utility scripts
└── data/             # Generated data (gitignored)
```
```

3. Validate: Review README renders correctly.

---

## 5. Validation Summary

### Pre-Migration Checks

- [x] Docker Compose files accessible at `docker/`
- [x] ESLint 9 config (`eslint.config.js`) working
- [x] Prettier formatting working
- [x] Tests passing

### Post-Migration Validation

After completing milestones, run:

1. **Docker Build Test:**
```bash
docker compose -f docker/docker-compose.yml config
docker compose -f docker/docker-compose.yml build --no-cache backend
docker compose -f docker/docker-compose.yml build --no-cache frontend
```

2. **Linting Test:**
```bash
cd frontend && npm run lint
cd backend && ruff check src/
```

3. **Formatting Test:**
```bash
cd frontend && npm run format:check
cd backend && black --check src/
```

4. **Full Test Suite:**
```bash
make test
```

---

## 6. Timeline & Effort Estimate

| Milestone | Issues | Estimated Time | Priority |
|-----------|--------|----------------|----------|
| Milestone 1: Docker | 1.1, 1.2 | 15 min | High |
| Milestone 2: Config | 2.1, 2.2 | 10 min | Medium |
| Milestone 3: Docs | 3.1 | 5 min | Low |
| **Total** | **4 issues** | **30 min** | |

---

## 7. Risk Assessment

| Issue | Risk Level | Mitigation |
|-------|------------|------------|
| Removing `.eslintrc.json` | Low | Verify `eslint.config.js` works first |
| Removing `frontend/.prettierrc` | Low | Root config already exists |
| Adding `.dockerignore` | None | Only improves performance |
| Documentation updates | None | Non-breaking change |

---

## 8. Deliverables Checklist

- [ ] `backend/.dockerignore` created
- [ ] `frontend/.dockerignore` created
- [ ] `docker/README.md` created
- [ ] `frontend/.eslintrc.json` removed
- [ ] `frontend/.prettierrc` removed
- [ ] Root `README.md` updated with structure section
- [ ] All validation tests passing
- [ ] Changes committed with message: `chore: standardise project structure (Nov 2025)`

---

## Conclusion

The project structure is **well-organized** and follows most modern standards. The remaining improvements are **minor cleanup tasks** that will improve build performance, reduce confusion, and align with 2025 best practices. All changes are **low-risk** and can be completed in **~30 minutes**.

**Next Steps:** Execute milestones sequentially, validate after each, then commit changes.

