# Tool Selection Guide (Backend Only)

Decision tree for the lean backend-only setup.

---

## 1. Start Development

| Need                   | Use                                    |
| ---------------------- | -------------------------------------- |
| Fast single terminal   | `make dev`                             |
| Multi-worker + JIT     | `./scripts/dev/start-backend.sh --jit` |
| macOS Terminal windows | `./scripts/dev/start-dev.sh`           |
| Production-like run    | `make prod`                            |

---

## 2. Testing

| Need             | Use                             |
| ---------------- | ------------------------------- |
| Full suite       | `make test`                     |
| Coverage         | `make test COV=1`               |
| Watch mode       | `./scripts/test/watch-tests.sh` |
| Quick smoke test | `./scripts/test/quick-test.sh`  |
| Cursor AI run    | `/test`                         |

---

## 3. Code Quality

| Stage            | Tool                                 |
| ---------------- | ------------------------------------ |
| Before commit    | `/workflow:pre-commit`               |
| Quick check      | `make check`                         |
| Individual fixes | `make lint`, `make format`           |
| IDE task         | VS Code “Pre-Commit: Run All Checks” |

---

## 4. Error Handling

| Situation      | Tool                         |
| -------------- | ---------------------------- |
| Need AI fix    | `/fix`                       |
| Systemic issue | `/workflow:error-resolution` |
| Manual cleanup | `make lint && make format`   |

---

## 5. MCP & Observability

| Goal               | Tool                                         |
| ------------------ | -------------------------------------------- |
| Verify MCP tools   | `python scripts/python/verify_mcp_server.py` |
| Quick MCP health   | `./scripts/utils/mcp-utils.sh health`        |
| Call tool manually | `python scripts/python/mcp_tool.py <tool>`   |
| Watch logs         | `tail -f logs/production.log`                |

---

## 6. Commit & Review

| Need              | Tool                         |
| ----------------- | ---------------------------- |
| Quick commit/push | `make qcp m="scope: msg"`    |
| AI commit message | `/commit`                    |
| Automated review  | `/review`                    |
| Cleanup/refactor  | `/workflow:code-improvement` |

---

Everything referencing the old frontend is archived under `docs/archive/` and intentionally excluded here. Focus on the backend, keep commands simple, and lean on Cursor workflows for heavy lifts.
