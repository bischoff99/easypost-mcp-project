#!/usr/bin/env zsh
set -euo pipefail

# DB
if ! docker info >/dev/null 2>&1; then
  echo "❌ Docker Desktop not running. Please start Docker Desktop first."
  exit 1
fi

echo "🐘 Starting PostgreSQL container..."
docker rm -f ep-pg 2>/dev/null || true

docker run --name ep-pg \
  -e POSTGRES_USER=dev -e POSTGRES_PASSWORD=devpass -e POSTGRES_DB=easypost \
  -p 5432:5432 -v ep_pg_data:/var/lib/postgresql/data \
  -d postgres:16

echo "⏳ Waiting for PostgreSQL to be ready..."
until docker exec ep-pg pg_isready -U dev -d easypost >/dev/null 2>&1; do
  sleep 0.5
done
echo "✅ PostgreSQL ready"

# Backend
echo "📦 Setting up backend..."
pushd apps/backend >/dev/null

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

. .venv/bin/activate
pip install -U pip wheel >/dev/null 2>&1
pip install -e . >/dev/null 2>&1

echo "🔄 Running migrations..."
alembic upgrade head || true

echo "🚀 Starting backend server..."
(uvicorn src.server:app --host 0.0.0.0 --port 8000) &
BEPID=$!

popd >/dev/null

# Frontend
echo "⚡ Setting up frontend..."
pushd apps/frontend >/dev/null

(pnpm i >/dev/null 2>&1 || npm i >/dev/null 2>&1) || true

echo "🚀 Starting frontend server..."
(pnpm dev >/dev/null 2>&1 || npm run dev >/dev/null 2>&1) &
FEPID=$!

popd >/dev/null

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Development servers started"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

trap "echo ''; echo '🛑 Shutting down...'; kill $BEPID $FEPID 2>/dev/null || true; docker stop ep-pg >/dev/null 2>&1 || true; exit" INT TERM

wait

