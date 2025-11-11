#!/usr/bin/env zsh
set -euo pipefail

# DB
docker ps --format '{{.Names}}' | rg -qx 'ep-pg' || docker run --name ep-pg -e POSTGRES_USER=dev -e POSTGRES_PASSWORD=devpass -e POSTGRES_DB=easypost -p 5432:5432 -d postgres:16

# Backend
pushd apps/backend >/dev/null
python -m venv .venv; . .venv/bin/activate
pip install -U pip wheel; pip install -e .
alembic upgrade head || true
UVICORN_CMD="uvicorn src.server:app --host 0.0.0.0 --port 8000"
($UVICORN_CMD) &
BEPID=$!
popd >/dev/null

# Frontend
pushd apps/frontend >/dev/null
pnpm i || npm i
(pnpm dev || npm run dev) &
FEPID=$!
popd >/dev/null

trap "kill $BEPID $FEPID 2>/dev/null || true" INT TERM
wait
