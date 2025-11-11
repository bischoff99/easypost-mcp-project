#!/usr/bin/env zsh
#
# Fix venv path issues
# Recreates venv with correct paths and resolves direnv conflict
# Uses zsh for better macOS compatibility
#

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

echo "🔧 Fixing venv path issues..."

# Check current Python version
PYTHON_CMD=$(which python3.14 2>/dev/null || which python3.13 2>/dev/null || which python3)
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')

echo "→ Using Python: $PYTHON_VERSION ($PYTHON_CMD)"

# Backup current venv
if [ -d "apps/backend/venv" ]; then
    echo "→ Backing up current venv..."
    BACKUP_DIR="apps/backend/venv.backup.$(date +%Y%m%d_%H%M%S)"
    mv apps/backend/venv "$BACKUP_DIR"
    echo "  ✅ Backup created: $BACKUP_DIR"
fi

# Create new venv
echo "→ Creating new venv..."
cd apps/backend
$PYTHON_CMD -m venv venv

# Activate and upgrade pip
echo "→ Upgrading pip..."
source venv/bin/activate
pip install --upgrade pip setuptools wheel

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "→ Installing requirements..."
    pip install -r requirements.txt
    echo "  ✅ Requirements installed"
else
    echo "  ⚠️  requirements.txt not found"
fi

# Verify installation
echo "→ Verifying installation..."
python -c "import fastapi, easypost, fastmcp; print('✅ Core packages verified')" || echo "⚠️  Some packages missing"

# Check for conflicts
echo "→ Checking for dependency conflicts..."
pip check || echo "⚠️  Dependency conflicts found - review output above"

cd ..

echo ""
echo "✅ venv recreated successfully!"
echo ""
echo "Next steps:"
echo "  1. Test: cd apps/backend && source venv/bin/activate && python -c 'import fastapi'"
echo "  2. Update .envrc: Remove 'layout python python3' line if using apps/backend/venv"
echo "  3. Remove backup: rm -rf $BACKUP_DIR (after verifying new venv works)"
echo ""

