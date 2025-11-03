#!/bin/bash

# Structure Optimization Script
# Safely reorganizes project structure

set -e

echo "🏗️  Project Structure Optimization"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Safety check
read -p "This will reorganize files. Have you committed recent changes? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please commit your changes first, then run this script again."
    exit 1
fi

echo ""
echo "${YELLOW}Step 1: Creating directory structure${NC}"

# Create new directories
mkdir -p docs/{setup,guides,reports,architecture}
mkdir -p backend/tests/{unit,integration}
mkdir -p backend/scripts
mkdir -p frontend/scripts
mkdir -p scripts/archive

echo "${GREEN}✓${NC} Directories created"

echo ""
echo "${YELLOW}Step 2: Moving test files to correct location${NC}"

# Move misplaced test files
if ls backend/test_*.py 1> /dev/null 2>&1; then
    mv backend/test_*.py backend/tests/integration/ 2>/dev/null || true
    echo "${GREEN}✓${NC} Test files moved to backend/tests/integration/"
else
    echo "  No test files to move"
fi

echo ""
echo "${YELLOW}Step 3: Organizing backend tests by type${NC}"

# Organize unit vs integration tests
if [ -f "backend/tests/test_easypost_service.py" ]; then
    mv backend/tests/test_easypost_service.py backend/tests/unit/ 2>/dev/null || true
fi
if [ -f "backend/tests/test_bulk_tools.py" ]; then
    mv backend/tests/test_bulk_tools.py backend/tests/unit/ 2>/dev/null || true
fi
if ls backend/tests/test_live_*.py 1> /dev/null 2>&1; then
    mv backend/tests/test_live_*.py backend/tests/integration/ 2>/dev/null || true
fi
if ls backend/tests/test_raw_*.py 1> /dev/null 2>&1; then
    mv backend/tests/test_raw_*.py backend/tests/integration/ 2>/dev/null || true
fi

echo "${GREEN}✓${NC} Tests organized by type (unit/integration)"

echo ""
echo "${YELLOW}Step 4: Consolidating documentation${NC}"

# Move documentation files to appropriate folders
mv SETUP*.md docs/setup/ 2>/dev/null || true
mv START*.md docs/setup/ 2>/dev/null || true
mv QUICK_START*.md docs/setup/ 2>/dev/null || true

mv *COMMANDS*.md docs/guides/ 2>/dev/null || true
mv M3MAX*.md docs/guides/ 2>/dev/null || true
mv DEPLOYMENT*.md docs/guides/ 2>/dev/null || true
mv UNIVERSAL*.md docs/guides/ 2>/dev/null || true

mv *REPORT*.md docs/reports/ 2>/dev/null || true
mv *STATUS*.md docs/reports/ 2>/dev/null || true
mv *SUMMARY*.md docs/reports/ 2>/dev/null || true
mv *COMPLETE*.md docs/reports/ 2>/dev/null || true
mv *RESULTS*.md docs/reports/ 2>/dev/null || true
mv VERIFICATION*.md docs/reports/ 2>/dev/null || true
mv COMPARISON*.md docs/reports/ 2>/dev/null || true

mv *STRUCTURE*.md docs/architecture/ 2>/dev/null || true
mv MCP_TOOLS*.md docs/architecture/ 2>/dev/null || true
mv REFACTORING*.md docs/architecture/ 2>/dev/null || true

echo "${GREEN}✓${NC} Documentation organized"

echo ""
echo "${YELLOW}Step 5: Moving .cursor documentation${NC}"

# Move .cursor reports to docs
mv .cursor/*REPORT*.md docs/reports/ 2>/dev/null || true
mv .cursor/*SUMMARY*.md docs/reports/ 2>/dev/null || true
mv .cursor/*COMPLETE*.md docs/reports/ 2>/dev/null || true

echo "${GREEN}✓${NC} .cursor docs moved"

echo ""
echo "${YELLOW}Step 6: Removing duplicate directories${NC}"

# Remove redundant directories
if [ -d ".prompts" ]; then
    rm -rf .prompts/
    echo "${GREEN}✓${NC} Removed .prompts/ (redundant)"
fi

if [ -d ".cursor/prompts" ]; then
    rm -rf .cursor/prompts/
    echo "${GREEN}✓${NC} Removed .cursor/prompts/ (redundant)"
fi

# Keep only l.md if it exists, remove it too
if [ -f ".cursor/commands/l.md" ]; then
    rm .cursor/commands/l.md
    echo "${GREEN}✓${NC} Removed placeholder l.md"
fi

echo ""
echo "${YELLOW}Step 7: Organizing scripts${NC}"

# Move backend scripts
if [ -f "backend/watch-tests.sh" ]; then
    mv backend/watch-tests.sh backend/scripts/ 2>/dev/null || true
fi

# Move root-level scripts (except this one)
for script in *.sh; do
    if [ "$script" != "optimize-structure.sh" ] && [ -f "$script" ]; then
        mv "$script" scripts/ 2>/dev/null || true
    fi
done

echo "${GREEN}✓${NC} Scripts organized"

echo ""
echo "${YELLOW}Step 8: Cleaning cache files${NC}"

# Remove cache directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -not -path "./backend/venv/*" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

echo "${GREEN}✓${NC} Cache cleaned"

echo ""
echo "${YELLOW}Step 9: Updating .gitignore${NC}"

# Update .gitignore if needed
if ! grep -q "__pycache__/" .gitignore; then
    cat >> .gitignore << 'EOF'

# Test & Cache
.pytest_cache/
__pycache__/
*.pyc
*.pyo
.coverage
htmlcov/
.ruff_cache/

# Build artifacts
*.egg-info/
dist/
build/
EOF
    echo "${GREEN}✓${NC} .gitignore updated"
else
    echo "  .gitignore already configured"
fi

echo ""
echo "${YELLOW}Step 10: Creating docs README${NC}"

# Create docs/README.md
cat > docs/README.md << 'EOF'
# EasyPost MCP Documentation

## 📚 Documentation Structure

### `/setup` - Getting Started
- Setup instructions
- Quick start guide
- Installation requirements

### `/guides` - How-To Guides
- Slash commands usage
- M3 Max optimizations
- Testing strategies
- Deployment guide

### `/reports` - Status & Reports
- Performance benchmarks
- API verification results
- Test results
- Project status updates

### `/architecture` - Technical Design
- Backend architecture
- Frontend architecture
- MCP tools inventory
- System design decisions

## 🚀 Quick Links

- [Setup Instructions](./setup/SETUP_INSTRUCTIONS.md)
- [Slash Commands Guide](./guides/slash-commands.md)
- [M3 Max Optimization](./guides/m3max-optimization.md)
- [Testing Guide](./guides/testing.md)

## 📝 Contributing

When adding documentation:
1. Place in appropriate category folder
2. Use clear, descriptive filenames
3. Update this README with new links
4. Follow markdown best practices
EOF

echo "${GREEN}✓${NC} docs/README.md created"

echo ""
echo "${YELLOW}Step 11: Creating test conftest.py${NC}"

# Create shared test fixtures
cat > backend/tests/conftest.py << 'EOF'
"""
Shared pytest fixtures and configuration
"""
import pytest
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@pytest.fixture
def easypost_api_key():
    """EasyPost API key from environment."""
    return os.getenv("EASYPOST_API_KEY")


@pytest.fixture
def sample_address_domestic():
    """Sample US domestic address."""
    return {
        "name": "Test User",
        "street1": "123 Main St",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94105",
        "country": "US"
    }


@pytest.fixture
def sample_address_international():
    """Sample international address."""
    return {
        "name": "Test User",
        "street1": "123 Test Street",
        "city": "London",
        "state": "",
        "zip": "SW1A 1AA",
        "country": "GB"
    }


@pytest.fixture
def sample_parcel():
    """Sample parcel dimensions."""
    return {
        "length": 10,
        "width": 10,
        "height": 5,
        "weight": 16  # ounces
    }
EOF

echo "${GREEN}✓${NC} backend/tests/conftest.py created"

echo ""
echo "=================================="
echo "${GREEN}✓ Structure optimization complete!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Run: pytest backend/tests/ --collect-only  (verify tests)"
echo "2. Run: git status  (review changes)"
echo "3. Run: git add .  (stage changes)"
echo "4. Run: git commit -m 'refactor: optimize project structure'"
echo ""
echo "New structure:"
echo "  docs/          - All documentation organized"
echo "  scripts/       - All scripts centralized"
echo "  backend/tests/ - Tests organized by type"
echo ""
echo "Happy coding! 🚀"
