# EasyPost MCP Cheat Sheet (Backend Only)

## Quick Commands

| Action             | Command                                |
| ------------------ | -------------------------------------- |
| Setup once         | `make setup`                           |
| Start dev server   | `make dev`                             |
| Multi-worker dev   | `./scripts/dev/start-backend.sh --jit` |
| Quick health check | `./scripts/test/quick-test.sh`         |
| Watch tests        | `./scripts/test/watch-tests.sh`        |
| Lint + test        | `make check`                           |
| Production run     | `make prod`                            |
| Clean caches       | `make clean`                           |

---

## Daily Flow

1. `make dev`
2. Write code
3. `scripts/test/watch-tests.sh`
4. `make lint`
5. `make test`
6. Commit (`make qcp m="scope: msg"`)

---

## Testing

| Need          | Command                       |
| ------------- | ----------------------------- |
| Full suite    | `make test`                   |
| Coverage      | `make test COV=1`             |
| Targeted test | `pytest path::test_name -v`   |
| Watch mode    | `scripts/test/watch-tests.sh` |
| Smoke test    | `scripts/test/quick-test.sh`  |

---

## MCP Verification

```bash
python scripts/python/verify_mcp_server.py        # full check
python scripts/python/mcp_tool.py list_tools      # enumerate tools
python scripts/python/mcp_tool.py get_rates ...   # call tool directly
./scripts/utils/mcp-utils.sh {health|verify|test} # shell shortcuts
```

---

## Troubleshooting

| Problem                      | Fix                                       |
| ---------------------------- | ----------------------------------------- |
| `make dev` says venv missing | Run `make setup`                          |
| 401 from EasyPost            | Check `config/.env` for valid key         |
| Tests fail randomly          | `make clean && make test`                 |
| MCP tool missing             | `./scripts/python/mcp_tool.py list_tools` |
| Port 8000 busy               | `pkill -f "uvicorn.*src.server"`          |

---

## Production Dry Run

```bash
make build                    # compile + mypy
make prod                     # start backend with workers/logging
tail -f logs/production.log
curl http://localhost:8000/health
make clean
```

---

Keep it simple: single backend, single Makefile, no frontend, no database.**_ End Patch_** successfully? Need check log response. Actually apply_patch format? we provided JSON? oh yes—they expect string not json. I incorrectly used JSON-coded call. Need reapply properly. It's complaining? need check tool response? none. oh message? I think call may have been invalid; there is no response. We'll re-run properly. Need to ensure call structure as raw string. Use apply patch again. Need to create file since deleted. We'll call with ascii patch. Let's try again. We'll create new file with same content. Use patch. Use actual text.
