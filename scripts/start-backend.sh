#!/usr/bin/env zsh
set -euo pipefail

echo "🔧 Setting up backend..."

cd apps/backend

# Detect venv location (prefers .venv, then venv)
if [ -d ".venv" ]; then
  VENV_PATH=".venv"
elif [ -d "venv" ]; then
  VENV_PATH="venv"
else
  echo "📁 Creating virtual environment..."
  python3 -m venv .venv
  VENV_PATH=".venv"
fi

# Activate virtual environment
source "${VENV_PATH}/bin/activate"

# Install dependencies
echo "📚 Installing dependencies..."
pip install -U pip setuptools wheel
pip install -r requirements.txt

# Start backend server
echo "🚀 Starting backend server on http://localhost:8000"
uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload
