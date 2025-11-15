# Backend Workflows

Lean workflows for the backend-only EasyPost MCP project.

---

## 1. Development Loop

1. `make dev` (or `./scripts/dev/start-backend.sh --jit`)
2. Modify code in `src/`
3. `scripts/test/watch-tests.sh` for rapid feedback
4. `make lint` before staging files
5. `make test` (full run) → commit

---

## 2. Feature Delivery

1. `make setup` (first time)
2. Create feature branch
3. Build feature with TDD
4. `make check`
5. `./scripts/test/quick-test.sh`
6. `/workflow:pre-commit` (Cursor) for review + commit

---

## 3. MCP Tool Changes

1. Update tool in `src/mcp_server/tools/`
2. Add/adjust tests in `tests/mcp/`
3. `python scripts/python/mcp_tool.py list_tools`
4. `make test`
5. Document behaviour in `docs/guides/MCP_TOOLS_USAGE.md`

---

## 4. Cleanup / Refactor

1. `/workflow:cleanup` (analysis + plan)
2. Apply edits
3. `make format && make lint`
4. `make test`
5. Update docs if behaviour changed

---

## 5. Production Dry Run

1. `make build`
2. `make prod` (starts backend with production flags)
3. Hit health endpoints / MCP verify
4. `make clean`

---

## 6. Troubleshooting Checklist

| Issue                    | Action                                              |
| ------------------------ | --------------------------------------------------- |
| Server fails to start    | Confirm venv exists, rerun `make setup`             |
| 500 errors from EasyPost | Verify `EASYPOST_API_KEY` in `config/.env`          |
| Tests hang               | Run `pytest -vv --maxfail=1` to locate failing test |
| MCP tool missing         | `./scripts/python/mcp_tool.py list_tools`           |
| Coverage stale           | Delete `htmlcov/` then rerun `make test COV=1`      |

---

Keep workflows simple; anything referencing the old frontend lives in `docs/archive/`.
