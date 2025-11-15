# Project Structure and Codebase Review: Compliance with Universal Development Standards

## 1. Analyse

- **Project type**: Backend-only FastAPI + FastMCP server (Python 3.11+).
- **Detected stack indicators**: `config/pyproject.toml`, FastAPI, FastMCP, pytest, no frontend runtime.
- **Key deviations** (pre-refactor):
  1. Duplicate MCP initialisation paths under `src/server.py` vs. `src/mcp_server/__init__.py`.
  2. FastAPI app lacked explicit reference to the constructed `EasyPostService` instance.
  3. No lightweight smoke tests pinned to the HTTP surface.
  4. Legacy monorepo layout anchored under `apps/backend/`, making it harder to apply November 2025 FastMCP standards (`src/`, `tests/`, `config/`, `docs/`).

## 2. Plan (prioritised)

1. Extract a reusable MCP factory that encapsulates tool/resource registration and optional lifespan hooks.
2. Rewire `src/server.py` to consume the factory, attach the shared `EasyPostService` to `app.state`, and rely on a single configuration source.
3. Introduce lightweight smoke tests asserting `/`, `/health`, and `/mcp` stay mounted.
4. Reorganise the repository to the canonical FastMCP layout (`src/`, `tests/`, `config/`, `docs/`, top-level `fastmcp.json`).
5. Document findings, plan, and actions in this report.

## 3. Execute (Desktop Commander actions)

| #   | File(s)                                                                 | Action                                                                                                                                  | Rationale                                                                                                          |
| --- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1   | `src/mcp_server/__init__.py`                                            | Added `build_mcp_server()` factory, centralised logging, and registration before exporting the default instance.                        | Single source of truth for MCP initialisation; FastAPI + CLI share identical wiring.                               |
| 2   | `src/server.py`                                                         | Swapped ad-hoc FastMCP setup for the factory, stored the shared `EasyPostService` on `app.state`, removed duplicate registration calls. | Ensures dependency injection pulls the same service instance, improves maintainability.                            |
| 3   | `tests/test_server_routes.py`                                           | Added HTTP smoke tests for `/`, `/health`, `/mcp`.                                                                                      | Provides quick regression coverage without live EasyPost calls.                                                    |
| 4   | `src/utils/config.py`, `Makefile`, `scripts/**`, `deploy/**`, `docs/**` | Collapsed the repo into `src/`, `tests/`, `config/`, introduced `fastmcp.json`, updated tooling/scripts/docs to the new paths.          | Aligns directory layout with November 2025 FastMCP standards; straightens CLI, Make commands, and Docker contexts. |
| 5   | `README.md`, `scripts/README.md`, `refactoring-report.md`               | Documented the new structure, workflow updates, and outstanding tasks.                                                                  | Keeps team + AI assistants aligned on layout + tooling expectations.                                               |

All modifications (moves, rewrites, deletions) were executed with Desktop Commander per requirements.

## 4. Verify

- `cd /Users/andrejs/Projects/personal/easypost-mcp-project && ./venv/bin/pytest -q`
  - ❌ Integration tests that hit the live EasyPost API now fail under the placeholder key (`test_key_for_pytest`). Provide a valid EasyPost key via `config/.env` to reproduce the previous “all green” run (289 passed, 8 skipped, coverage 75.7 %).
  - ✅ Unit, router, MCP, and smoke suites execute under the new layout; async fixtures require `pytest.ini` at repo root (restored).

## 5. Remaining Risks / Follow-ups

- **Live API credentials**: populate `config/.env` with a working EasyPost key (or export `EASYPOST_API_KEY`) before running the full suite; without it, real-rate tests return 403 as observed.
- **Docs**: numerous historical guides still reference `apps/backend/*`. Update them progressively (tracked via `rg "apps/backend"`).
- **Scripts**: legacy helper scripts (`scripts/test/watch-tests.sh`, historic cleanup reports) still reference removed paths; audit or delete as needed.
- **CI/CD**: update workflows to run `pytest` from repo root now that `src/` + `tests/` live top-level. Docker contexts already point to `deploy/Dockerfile*`.

## 6. Git Summary

- Branch: `refactor/ai-standards-compliance`
- Pending changes include repository-wide moves (new `src/`, `tests/`, `config/`), FastMCP config (`fastmcp.json`), updated Make/scripts/deploy assets, and this report.
- Suggested commit message: `chore: adopt standard fastmcp layout and tooling`.

## 7. Comparison Snapshot (ours vs. reference)

| Aspect      | Reference FastMCP Shipping Project     | Updated Repo                                                        |
| ----------- | -------------------------------------- | ------------------------------------------------------------------- |
| Source tree | `src/` at root                         | ✅ `src/` at root                                                   |
| Tests       | `tests/` sibling to `src/`             | ✅ `tests/` top-level                                               |
| Config      | `fastmcp.json`, env/spec files grouped | ✅ `fastmcp.json`, `config/` holding env + requirements + pyproject |
| Tooling     | Declarative MCP config + uv env        | ✅ `fastmcp.json`, Make/scripts consume `venv/` + config            |
| Docs        | `docs/` root with architecture notes   | ✅ `docs/` retained; backlog to scrub legacy paths                  |
