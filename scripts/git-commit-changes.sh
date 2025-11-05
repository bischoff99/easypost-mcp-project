#!/bin/bash

# Git Commit Script - Organizes changes with proper conventional commits
# Follows: https://www.conventionalcommits.org/

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

cd /Users/andrejs/easypost-mcp-project

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           Git Commit Workflow - EasyPost MCP             ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if we have changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${GREEN}✓ Changes detected${NC}"
else
    echo -e "${YELLOW}⚠ No changes to commit${NC}"
    exit 0
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 1: Stage Changes by Category"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 1. Documentation & cleanup files (already staged)
echo -e "${BLUE}1. Completing staged documentation reorganization...${NC}"
git status --short | grep "^R" | head -5
echo "  ✓ Documentation moved to archive"
echo ""

# 2. Add validation scripts
echo -e "${BLUE}2. Adding validation & monitoring scripts...${NC}"
git add scripts/validate-easypost-api.sh
git add scripts/validate-api-standards.sh
git add scripts/test-full-functionality.sh
git add scripts/monitor-database.sh
git add scripts/setup-nginx-proxy.sh
git add scripts/setup-shell-integration.sh
git add scripts/shell-integration.sh
git add scripts/validate-project-structure.py
git add scripts/completions/
echo "  ✓ 8 validation scripts added"
echo ""

# 3. Add reports
echo -e "${BLUE}3. Adding validation reports...${NC}"
git add API_VALIDATION_REPORT.md
git add PROJECT_AUDIT_*.md
git add AUDIT_SUMMARY_FINAL.md
echo "  ✓ 6 audit reports added"
echo ""

# 4. Add nginx config
echo -e "${BLUE}4. Adding nginx proxy configuration...${NC}"
git add nginx-local.conf
echo "  ✓ Nginx config added"
echo ""

# 5. Frontend fixes
echo -e "${BLUE}5. Adding frontend fixes...${NC}"
git add frontend/src/components/dashboard/StatsCard.jsx
git add frontend/src/components/dashboard/StatsCard.test.jsx
git add frontend/src/components/shipments/BulkUploadModal.jsx
git add frontend/src/pages/DashboardPage.jsx
git add frontend/src/pages/ShipmentsPage.jsx
git add frontend/src/tests/e2e/dashboard.test.jsx
git add frontend/src/tests/e2e/shipment-crud.test.js
git add frontend/src/tests/setup.js
git add frontend/vitest.config.js
git add frontend/src/services/endpoints.js
git add frontend/src/services/errors.js
git add frontend/package.json
git add frontend/package-lock.json
echo "  ✓ Frontend fixes added"
echo ""

# 6. Backend fixes
echo -e "${BLUE}6. Adding backend improvements...${NC}"
git add backend/src/server.py
git add backend/src/models/
git add backend/src/services/
git add backend/src/routers/
git add backend/src/database.py
git add backend/src/dependencies.py
git add backend/src/lifespan.py
git add backend/src/utils/
git add backend/tests/
git add backend/pytest.ini
git add backend/OPTIONAL_OPTIMIZATIONS.md
git add backend/alembic/versions/fc2aec2ac737_update_timestamp_defaults_to_server_side.py
echo "  ✓ Backend improvements added"
echo ""

# 7. Documentation updates
echo -e "${BLUE}7. Adding updated documentation...${NC}"
git add docs/
git add CLAUDE.md
git add README.md
git add Makefile
echo "  ✓ Documentation updated"
echo ""

# 8. Configuration updates
echo -e "${BLUE}8. Adding configuration updates...${NC}"
git add .cursor/
git add .cursorrules
git add .dev-config.json
git add .gitignore
git add .gitattributes
git add .pre-commit-config.yaml
git add .vscode/
echo "  ✓ Configuration updated"
echo ""

# 9. Clean up deleted files
echo -e "${BLUE}9. Removing deleted files...${NC}"
git add -u
echo "  ✓ Deleted files removed from index"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "STEP 2: Create Commits (Conventional Commits)"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Commit 1: Documentation reorganization (already staged)
echo -e "${BLUE}Commit 1: Documentation reorganization${NC}"
git commit -m "docs: reorganize documentation structure

- Move implementation reports to docs/archive/2025-11-implementation/
- Consolidate PostgreSQL docs to docs/architecture/
- Remove redundant root-level documentation files
- Clean up outdated cursor command files
- Improve documentation discoverability

BREAKING CHANGE: Documentation paths have changed"

echo -e "${GREEN}✓ Committed${NC}"
echo ""

# Commit 2: Backend improvements
echo -e "${BLUE}Commit 2: Backend API improvements${NC}"
git add backend/
git commit -m "feat(backend): improve API endpoints and validation

- Fix analytics endpoint to use ShipmentMetricsResponse
- Update /stats endpoint with honest metrics (no fake trends)
- Fix /carrier-performance to show delivery rates
- Add routers/ directory for better organization
- Improve error handling with numeric status codes
- Add timestamp defaults migration

Closes #dashboard-accuracy"

echo -e "${GREEN}✓ Committed${NC}"
echo ""

# Commit 3: Frontend fixes
echo -e "${BLUE}Commit 3: Frontend dashboard improvements${NC}"
git add frontend/
git commit -m "fix(frontend): update dashboard to display honest data

- Remove hardcoded fake trends from dashboard
- Display real API data with explanatory notes
- Rename 'On-Time Rate' to 'Delivery Rate'
- Update StatsCard to support optional notes
- Fix E2E test file extensions (.jsx)
- Skip E2E tests requiring backend by default
- Remove unused variables (8 ESLint warnings)

Improves dashboard accuracy and user transparency"

echo -e "${GREEN}✓ Committed${NC}"
echo ""

# Commit 4: Validation scripts
echo -e "${BLUE}Commit 4: Add validation and monitoring tools${NC}"
git add scripts/ nginx-local.conf
git commit -m "feat(scripts): add comprehensive validation suite

- validate-easypost-api.sh: API connectivity tests
- validate-api-standards.sh: Standards compliance checks
- test-full-functionality.sh: Complete system validation
- setup-nginx-proxy.sh: Reverse proxy configuration
- monitor-database.sh: Database health monitoring
- setup-shell-integration.sh: Zsh/Bash completions
- validate-project-structure.py: Directory validation

Includes nginx config for unified port access (8080)"

echo -e "${GREEN}✓ Committed${NC}"
echo ""

# Commit 5: Documentation and reports
echo -e "${BLUE}Commit 5: Add validation and audit reports${NC}"
git add *.md docs/
git commit -m "docs: add API validation and audit reports

- API_VALIDATION_REPORT.md: 79% compliance, production-ready
- PROJECT_AUDIT_*.md: Complete project audit documentation
- AUDIT_SUMMARY_FINAL.md: Final audit summary
- Update CLAUDE.md with latest project state
- Update README.md with new validation commands
- Add M3_MAX_OPTIMIZATION_REPORT.md to guides/

Documents successful EasyPost API integration and standards compliance"

echo -e "${GREEN}✓ Committed${NC}"
echo ""

# Commit 6: Configuration updates
echo -e "${BLUE}Commit 6: Update configuration files${NC}"
git add .cursor/ .cursorrules .dev-config.json .gitignore .gitattributes .pre-commit-config.yaml .vscode/ Makefile
git commit -m "chore: update configuration files

- Update .cursor/ rules and commands
- Add .gitattributes for consistent line endings
- Update .dev-config.json with new workflows
- Enhance .gitignore patterns
- Add VSCode launch configurations
- Update Makefile with new targets
- Configure pre-commit hooks

Improves development environment consistency"

echo -e "${GREEN}✓ Committed${NC}"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "STEP 3: Review Commits"
echo "═══════════════════════════════════════════════════════════"
echo ""

git log --oneline -10

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 4: Push to GitHub"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo -e "${YELLOW}Ready to push to origin/master?${NC}"
echo ""
echo "Run: git push origin master"
echo ""
echo -e "${GREEN}✓ All changes committed and ready to push!${NC}"

