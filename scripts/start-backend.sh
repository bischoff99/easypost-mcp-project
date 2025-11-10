#!/bin/bash
set -e

echo "🔧 Setting up backend..."

cd backend

# Install uv if not present
if ! command -v uv &> /dev/null; then
  echo "📦 Installing uv package manager..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
  echo "📁 Creating virtual environment..."
  uv venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
uv pip install -r requirements.txt

# Start backend server
echo "🚀 Starting backend server on http://localhost:8000"
uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload
