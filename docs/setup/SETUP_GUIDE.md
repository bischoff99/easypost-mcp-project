# EasyPost MCP Setup Guide (Backend Only)

## Overview

Single FastAPI + MCP backend. No frontend, no database, no Node.js.

## Requirements

- macOS (tested on Sonoma)
- Python 3.11+
- EasyPost API key

Optional tools:

- direnv (auto env loading)
- uv (faster installs) or pip (default)

## 1. Clone and Configure

```bash
git clone <repo>
cd easypost-mcp-project
cp config/.env.example config/.env
```

Edit `config/.env`:

- `EASYPOST_API_KEY="<test_or_prod_key>"`
- Disable optional features by leaving unset

## 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel
pip install -r config/requirements.txt
```

> Tip: add `source venv/bin/activate` to `.envrc` if using direnv.

## 3. Development Commands

- `make setup` – create venv + install deps
- `make dev` – start FastAPI server (`http://localhost:8000`)
- `make test` – pytest with auto workers
- `make test COV=1` – coverage + htmlcov
- `make lint` / `make format` – Ruff

All commands run from repo root; Makefile handles paths internally.

## 4. MCP Server Usage

```json
{
  "command": "/path/to/repo/venv/bin/python",
  "args": ["-m", "src.mcp_server"],
  "env": { "EASYPOST_API_KEY": "..." }
}
```

Supports Claude Desktop stdio transport or HTTP via `/mcp`.

## 5. Optional Tools

### Direnv

1. `brew install direnv`
2. Add `eval "$(direnv hook zsh)"` to `.zshrc`
3. Create `.envrc` at repo root:
   ```
   layout python3
   source_env .
   ```
4. `direnv allow`

### Zsh Hardening

- Use `set -o pipefail`
- `export PYTHONWARNINGS="default"`
- Keep secrets in `.env`, never in shell history

## 6. Troubleshooting

- Missing venv: run `make setup`
- Import errors: deactivate + reactivate venv
- EasyPost errors: confirm API key + test mode
- MCP errors: run `python scripts/python/mcp_tool.py list_tools`

## 7. Next Actions

- Update `config/.env` when rotating keys
- Keep `requirements-lock.txt` in sync using `pip-compile`
- Use `make clean` to remove caches (`__pycache__`, `.pytest_cache`, `htmlcov`)
