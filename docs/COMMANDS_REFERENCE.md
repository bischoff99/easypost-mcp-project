# Commands Reference (Backend Only)

Complete view of supported commands now that the project is a single FastAPI + MCP backend. Anything referencing the removed frontend is archived for history.

**Last Updated**: 2025-11-14
**Scope**: Backend + MCP tooling only

---

## 1. Makefile Commands

| Command | Description |
| --- | --- |
| `make setup` | Create venv + install backend dependencies |
| `make dev` | Start uvicorn with reload (`http://localhost:8000`) |
| `make test` | Pytest with auto-detected workers |
| `make test COV=1` | Pytest + coverage + `htmlcov/` |
| `make lint` | Ruff lint (`src/`, `tests/`) |
| `make format` | Ruff format + autofix |
| `make check` | `lint` + `test` combo |
| `make build` | Compile `.pyc` and run mypy (best-effort) |
| `make prod` | Execute `scripts/dev/start-prod.sh` |
| `make clean` | Remove caches, `htmlcov`, `.coverage` |
| `make qcp m="message"` | Git add/commit/push |
| `make help-all` | Aggregated reference (Makefile + scripts + workflows) |

---

## 2. Scripts

### Development

| Script | Purpose |
| --- | --- |
| `./scripts/dev/start-backend.sh [--jit] [--mcp-verify]` | Activate venv, install deps, launch uvicorn (multi-worker JIT optional) |
| `./scripts/dev/start-dev.sh` | macOS helper: opens Terminal window and runs backend server |
| `./scripts/dev/start-prod.sh` | Production launcher (uvicorn workers, logging, health wait) |

### Testing & Utilities

| Script | Purpose |
| --- | --- |
| `./scripts/test/quick-test.sh` | Health check → MCP verification → sample API call → unit tests |
| `./scripts/test/watch-tests.sh` | `ptw tests/ -- -v` watcher |
| `./scripts/test/benchmark.sh` | Performance profiling of backend |
| `./scripts/test/test-full-functionality.sh` | Full pytest suite (serial) |
| `./scripts/python/mcp_tool.py <tool>` | Invoke MCP tool directly |
| `./scripts/utils/mcp-utils.sh {health|verify|test}` | Shell shortcuts for MCP checks |

Removed scripts (`dev_local.sh`, frontend starters) live in `docs/setup/archive/` for reference only.

---

## 3. VS Code Tasks

Only backend tasks remain active:

| Task | Description |
| --- | --- |
| `Dev: Backend` | Run uvicorn with reload inside venv |
| `🧪 Test: Backend` | `pytest -v -n auto` |
| `✅ Pre-Commit: Run All Checks` | Format + lint + test |
| `🗄️ Database: Create Migration` | *Legacy* – ignore unless Alembic is reintroduced |
| `🚀 Dev: Full Stack` | **Archived** (frontend removed) |

Update `.vscode/tasks.json` if additional backend-only tasks are needed.

---

## 4. Cursor Workflows

| Workflow | When to Use |
| --- | --- |
| `/workflow:pre-commit` | Review → fix → test → commit |
| `/workflow:feature-dev` | Guided feature implementation |
| `/workflow:error-resolution` | Debug failing tests or runtime issues |
| `/workflow:code-improvement` | Refactors, cleanups |
| `/workflow:cleanup` | Large structural cleanups |
| `/workflow:pre-push` | Final verification before push |

No workflow references the old frontend; everything assumes backend-only repo.

---

## 5. Universal Commands

| Command | Summary |
| --- | --- |
| `/test` | Smart pytest runner |
| `/fix` | Apply suggested patches |
| `/explain` | Summaries of code sections |
| `/commit` | Generate commit messages |
| `/review` | Automated review before merge |
| `/refactor` | Guided refactors |
| `/docs` | Generate/update Markdown docs |
| `/debug` | Interactive debugger |
| `/clean` | Repo cleanup suggestions |
| `/workflow` | Workflow chooser |

---

## 6. Command Selection Guide

1. **Need a backend quickly?**
   - `make dev` (single terminal) or `./scripts/dev/start-backend.sh --jit` (multi-worker + optional MCP verification).

2. **Production-like test?**
   - `make prod` → runs `start-prod.sh`, waits for health check, streams logs.

3. **Validate MCP tools?**
   - `python scripts/python/mcp_tool.py list_tools` or `./scripts/utils/mcp-utils.sh verify`.

4. **CI-equivalent locally?**
   - `make check` ensures lint + tests.

5. **TDD loop?**
   - `scripts/test/watch-tests.sh` for automatic reruns.

6. **One-line smoke test?**
   - `./scripts/test/quick-test.sh`.

Everything else (pnpm, frontend builds, dockerised Postgres) is intentionally removed to keep the project lean for personal use.
