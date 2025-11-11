#!/usr/bin/env zsh
#
# normalize_project.sh
# Normalizes EasyPost MCP repo layout into standardized monorepo structure
# Works safely on macOS and Linux
# Uses zsh for better macOS compatibility
#
# Actions:
# - Convert backend/ → apps/backend/
# - Convert frontend/ → apps/frontend/
# - Convert docker/ → deploy/
# - Create packages/core/ for shared code (if needed)
# - Generate/update Makefile and .cursor/config.json
#

set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
BACKUP_DIR="$ROOT/.normalize_backup_$(date +%Y%m%d_%H%M%S)"
UNDO_SCRIPT="$ROOT/scripts/undo_normalize.sh"

echo "🧩 Normalizing EasyPost MCP repo at $ROOT"
echo "📦 Backup will be created at: $BACKUP_DIR"
echo ""

# Check if already normalized
if [ -d "apps/backend" ] && [ -d "apps/frontend" ]; then
  echo "⚠️  Project appears already normalized (apps/backend and apps/frontend exist)"
  read -p "Continue anyway? (yes/no): " confirm
  if [ "$confirm" != "yes" ]; then
    echo "Cancelled."
    exit 0
  fi
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"
echo "✅ Backup directory created"

# Create undo script header
cat > "$UNDO_SCRIPT" <<'EOF'
#!/usr/bin/env bash
# Undo script for project normalization
# Generated automatically - DO NOT EDIT MANUALLY
set -euo pipefail
EOF
chmod +x "$UNDO_SCRIPT"

# --- 1. Create new directory structure ----------------------------------

echo "→ Creating new directory structure..."
mkdir -p apps/backend apps/frontend packages/core/{py,ts} deploy scripts tests/e2e

# --- 2. Move backend/ → apps/backend/ ------------------------------------

if [ -d "backend" ] && [ ! -d "apps/backend/src" ]; then
  echo "→ Moving backend/ → apps/backend/..."
  
  # Backup
  cp -r backend "$BACKUP_DIR/backend" 2>/dev/null || true
  
  # Move with rsync (preserves timestamps, ownership)
  rsync -a --remove-source-files backend/ apps/backend/
  
  # Remove empty backend directory
  rmdir backend 2>/dev/null || rm -rf backend
  
  # Ensure src/ exists
  if [ ! -d "apps/backend/src" ]; then
    mkdir -p apps/backend/src
    # Move any loose files to src/
    find apps/backend -maxdepth 1 -type f -name "*.py" -exec mv {} apps/backend/src/ \; 2>/dev/null || true
  fi
  
  echo "  ✅ Backend moved to apps/backend/"
  
  # Add to undo script
  cat >> "$UNDO_SCRIPT" <<EOF
echo "→ Restoring backend/..."
rsync -a apps/backend/ backend/
rm -rf apps/backend
EOF
fi

# --- 3. Move frontend/ → apps/frontend/ ----------------------------------

if [ -d "frontend" ] && [ ! -d "apps/frontend/src" ]; then
  echo "→ Moving frontend/ → apps/frontend/..."
  
  # Backup
  cp -r frontend "$BACKUP_DIR/frontend" 2>/dev/null || true
  
  # Move with rsync
  rsync -a --remove-source-files frontend/ apps/frontend/
  
  # Remove empty frontend directory
  rmdir frontend 2>/dev/null || rm -rf frontend
  
  # Ensure src/ exists
  if [ ! -d "apps/frontend/src" ]; then
    mkdir -p apps/frontend/src
    # Move any loose files to src/
    find apps/frontend -maxdepth 1 -type f \( -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" \) -exec mv {} apps/frontend/src/ \; 2>/dev/null || true
  fi
  
  echo "  ✅ Frontend moved to apps/frontend/"
  
  # Add to undo script
  cat >> "$UNDO_SCRIPT" <<EOF
echo "→ Restoring frontend/..."
rsync -a apps/frontend/ frontend/
rm -rf apps/frontend
EOF
fi

# --- 4. Move docker/ → deploy/ -------------------------------------------

if [ -d "docker" ] && [ ! -d "deploy" ]; then
  echo "→ Moving docker/ → deploy/..."
  
  # Backup
  cp -r docker "$BACKUP_DIR/docker" 2>/dev/null || true
  
  # Move with rsync
  rsync -a --remove-source-files docker/ deploy/
  
  # Remove empty docker directory
  rmdir docker 2>/dev/null || rm -rf docker
  
  echo "  ✅ Docker configs moved to deploy/"
  
  # Add to undo script
  cat >> "$UNDO_SCRIPT" <<EOF
echo "→ Restoring docker/..."
rsync -a deploy/ docker/
rm -rf deploy
EOF
fi

# --- 5. Update Makefile paths --------------------------------------------

if [ -f "Makefile" ]; then
  echo "→ Updating Makefile paths..."
  
  # Backup Makefile
  cp Makefile "$BACKUP_DIR/Makefile" 2>/dev/null || true
  
  # Update paths (macOS and Linux compatible)
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' 's|backend/|apps/backend/|g' Makefile 2>/dev/null || true
    sed -i '' 's|frontend/|apps/frontend/|g' Makefile 2>/dev/null || true
    sed -i '' 's|docker/|deploy/|g' Makefile 2>/dev/null || true
  else
    # Linux
    sed -i 's|backend/|apps/backend/|g' Makefile 2>/dev/null || true
    sed -i 's|frontend/|apps/frontend/|g' Makefile 2>/dev/null || true
    sed -i 's|docker/|deploy/|g' Makefile 2>/dev/null || true
  fi
  
  echo "  ✅ Makefile paths updated"
  
  # Add to undo script
  cat >> "$UNDO_SCRIPT" <<EOF
echo "→ Restoring Makefile..."
cp "$BACKUP_DIR/Makefile" Makefile
EOF
fi

# --- 6. Update Docker Compose paths --------------------------------------

if [ -f "deploy/docker-compose.yml" ] || [ -f "deploy/docker-compose.prod.yml" ]; then
  echo "→ Updating Docker Compose paths..."
  
  for compose_file in deploy/docker-compose*.yml; do
    if [ -f "$compose_file" ]; then
      # Backup
      cp "$compose_file" "$BACKUP_DIR/$(basename $compose_file)" 2>/dev/null || true
      
      # Update paths
      if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' 's|../backend|../apps/backend|g' "$compose_file" 2>/dev/null || true
        sed -i '' 's|../frontend|../apps/frontend|g' "$compose_file" 2>/dev/null || true
        sed -i '' 's|./backend|./apps/backend|g' "$compose_file" 2>/dev/null || true
        sed -i '' 's|./frontend|./apps/frontend|g' "$compose_file" 2>/dev/null || true
      else
        sed -i 's|../backend|../apps/backend|g' "$compose_file" 2>/dev/null || true
        sed -i 's|../frontend|../apps/frontend|g' "$compose_file" 2>/dev/null || true
        sed -i 's|./backend|./apps/backend|g' "$compose_file" 2>/dev/null || true
        sed -i 's|./frontend|./apps/frontend|g' "$compose_file" 2>/dev/null || true
      fi
    fi
  done
  
  echo "  ✅ Docker Compose paths updated"
fi

# --- 7. Update .cursor/config.json if exists ------------------------------

if [ -f ".cursor/config.json" ]; then
  echo "→ Updating .cursor/config.json..."
  cp .cursor/config.json "$BACKUP_DIR/.cursor_config.json" 2>/dev/null || true
  
  # Update ignore paths if needed
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' 's|"backend/|"apps/backend/|g' .cursor/config.json 2>/dev/null || true
    sed -i '' 's|"frontend/|"apps/frontend/|g' .cursor/config.json 2>/dev/null || true
  else
    sed -i 's|"backend/|"apps/backend/|g' .cursor/config.json 2>/dev/null || true
    sed -i 's|"frontend/|"apps/frontend/|g' .cursor/config.json 2>/dev/null || true
  fi
  
  echo "  ✅ Cursor config updated"
fi

# --- 8. Create/update .cursor/config.json if missing ---------------------

if [ ! -f ".cursor/config.json" ]; then
  echo "→ Creating .cursor/config.json..."
  mkdir -p .cursor
  cat > .cursor/config.json <<'EOF'
{
  "indexing": {
    "ignore": ["deploy", "__pycache__", ".venv", "node_modules", ".git"],
    "include": ["apps", "packages"]
  },
  "contextWindow": 128000
}
EOF
  echo "  ✅ Created Cursor configuration"
fi

# --- 9. Add __init__.py placeholders --------------------------------------

echo "→ Adding Python package markers..."
touch apps/backend/src/__init__.py 2>/dev/null || true
touch packages/core/py/__init__.py 2>/dev/null || true
touch packages/core/ts/.gitkeep 2>/dev/null || true
touch tests/e2e/.gitkeep 2>/dev/null || true

# --- 10. Update shell integration script ----------------------------------

if [ -f "scripts/shell-integration.sh" ]; then
  echo "→ Updating shell integration paths..."
  cp scripts/shell-integration.sh "$BACKUP_DIR/shell-integration.sh" 2>/dev/null || true
  
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' 's|backend/|apps/backend/|g' scripts/shell-integration.sh 2>/dev/null || true
    sed -i '' 's|frontend/|apps/frontend/|g' scripts/shell-integration.sh 2>/dev/null || true
  else
    sed -i 's|backend/|apps/backend/|g' scripts/shell-integration.sh 2>/dev/null || true
    sed -i 's|frontend/|apps/frontend/|g' scripts/shell-integration.sh 2>/dev/null || true
  fi
  
  echo "  ✅ Shell integration updated"
fi

# --- 11. Update GitHub workflows ------------------------------------------

if [ -d ".github/workflows" ]; then
  echo "→ Updating GitHub workflows..."
  
  # Backup workflows directory
  cp -r .github/workflows "$BACKUP_DIR/.github_workflows" 2>/dev/null || true
  
  # Update all workflow YAML files
  find .github/workflows -name "*.yml" -o -name "*.yaml" | while read workflow_file; do
    if [ -f "$workflow_file" ]; then
      if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS sed
        sed -i '' 's|backend/|apps/backend/|g' "$workflow_file" 2>/dev/null || true
        sed -i '' 's|frontend/|apps/frontend/|g' "$workflow_file" 2>/dev/null || true
        sed -i '' 's|docker/|deploy/|g' "$workflow_file" 2>/dev/null || true
      else
        # Linux sed
        sed -i 's|backend/|apps/backend/|g' "$workflow_file" 2>/dev/null || true
        sed -i 's|frontend/|apps/frontend/|g' "$workflow_file" 2>/dev/null || true
        sed -i 's|docker/|deploy/|g' "$workflow_file" 2>/dev/null || true
      fi
    fi
  done
  
  echo "  ✅ GitHub workflows updated"
  
  # Add to undo script
  cat >> "$UNDO_SCRIPT" <<EOF
echo "→ Restoring GitHub workflows..."
cp -r "$BACKUP_DIR/.github_workflows"/* .github/workflows/
EOF
fi

# --- 12. Update .gitignore ------------------------------------------------

if [ -f ".gitignore" ]; then
  echo "→ Updating .gitignore paths..."
  
  # Backup .gitignore
  cp .gitignore "$BACKUP_DIR/.gitignore" 2>/dev/null || true
  
  # Update paths (macOS and Linux compatible)
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' 's|^backend/|apps/backend/|g' .gitignore 2>/dev/null || true
    sed -i '' 's|^frontend/|apps/frontend/|g' .gitignore 2>/dev/null || true
    sed -i '' 's|^docker/|deploy/|g' .gitignore 2>/dev/null || true
  else
    sed -i 's|^backend/|apps/backend/|g' .gitignore 2>/dev/null || true
    sed -i 's|^frontend/|apps/frontend/|g' .gitignore 2>/dev/null || true
    sed -i 's|^docker/|deploy/|g' .gitignore 2>/dev/null || true
  fi
  
  echo "  ✅ .gitignore paths updated"
  
  # Add to undo script
  cat >> "$UNDO_SCRIPT" <<EOF
echo "→ Restoring .gitignore..."
cp "$BACKUP_DIR/.gitignore" .gitignore
EOF
fi

# --- 13. Update other scripts in scripts/ directory -----------------------

if [ -d "scripts" ]; then
  echo "→ Updating scripts in scripts/ directory..."
  
  # Backup scripts directory
  cp -r scripts "$BACKUP_DIR/scripts_backup" 2>/dev/null || true
  
  # Update common patterns in shell scripts
  find scripts -name "*.sh" -type f | while read script_file; do
    if [ -f "$script_file" ] && [ "$script_file" != "scripts/normalize_project.sh" ]; then
      if [[ "$OSTYPE" == "darwin"* ]]; then
        # Update cd commands and path references
        sed -i '' 's|cd backend|cd apps/backend|g' "$script_file" 2>/dev/null || true
        sed -i '' 's|cd frontend|cd apps/frontend|g' "$script_file" 2>/dev/null || true
        sed -i '' 's|backend/|apps/backend/|g' "$script_file" 2>/dev/null || true
        sed -i '' 's|frontend/|apps/frontend/|g' "$script_file" 2>/dev/null || true
        sed -i '' 's|docker/|deploy/|g' "$script_file" 2>/dev/null || true
      else
        sed -i 's|cd backend|cd apps/backend|g' "$script_file" 2>/dev/null || true
        sed -i 's|cd frontend|cd apps/frontend|g' "$script_file" 2>/dev/null || true
        sed -i 's|backend/|apps/backend/|g' "$script_file" 2>/dev/null || true
        sed -i 's|frontend/|apps/frontend/|g' "$script_file" 2>/dev/null || true
        sed -i 's|docker/|deploy/|g' "$script_file" 2>/dev/null || true
      fi
    fi
  done
  
  echo "  ✅ Scripts updated (excluding normalize_project.sh)"
fi

# --- 14. Validation step ---------------------------------------------------

echo "→ Validating updates..."

VALIDATION_FAILED=0

# Check Makefile
if grep -q "cd backend" Makefile 2>/dev/null; then
  echo "  ⚠️  Warning: Makefile may still contain 'cd backend' references"
  VALIDATION_FAILED=1
fi

# Check Docker Compose
if [ -f "deploy/docker-compose.yml" ]; then
  if grep -q "context: ./backend" deploy/docker-compose.yml 2>/dev/null; then
    echo "  ⚠️  Warning: Docker Compose may still reference ./backend"
    VALIDATION_FAILED=1
  fi
fi

# Check GitHub workflows
if [ -d ".github/workflows" ]; then
  if grep -r "paths:.*backend/\*\*" .github/workflows/ 2>/dev/null | grep -v "apps/backend" >/dev/null; then
    echo "  ⚠️  Warning: Some GitHub workflows may still reference backend/**"
    VALIDATION_FAILED=1
  fi
fi

if [ $VALIDATION_FAILED -eq 0 ]; then
  echo "  ✅ Validation passed"
else
  echo "  ⚠️  Validation warnings found - please review manually"
fi

# --- 15. Finalize undo script --------------------------------------------

cat >> "$UNDO_SCRIPT" <<EOF

echo ""
echo "✅ Undo complete. Original structure restored from backup."
echo "📦 Backup location: $BACKUP_DIR"
echo ""
echo "To permanently remove backup:"
echo "  rm -rf $BACKUP_DIR"
EOF

# --- 16. Summary ----------------------------------------------------------

echo ""
echo "✅ Normalization complete!"
echo ""
echo "New structure:"
if command -v tree >/dev/null 2>&1; then
  tree -L 3 -I "node_modules|__pycache__|.venv|venv|.git" apps packages deploy 2>/dev/null || true
else
  echo "apps/"
  ls -la apps/ 2>/dev/null | head -10 || true
  echo ""
  echo "packages/"
  ls -la packages/ 2>/dev/null | head -10 || true
  echo ""
  echo "deploy/"
  ls -la deploy/ 2>/dev/null | head -10 || true
fi

echo ""
echo "📦 Backup location: $BACKUP_DIR"
echo "↩️  Undo script: $UNDO_SCRIPT"
echo ""
echo "Next steps:"
echo "  1. Review changes: git status"
echo "  2. Test build: make dev"
echo "  3. Review updated scripts in scripts/ directory"
echo "  4. Update documentation (README.md, docs/) if desired"
echo "  5. If issues: bash $UNDO_SCRIPT"
echo "  6. Commit: git add -A && git commit -m 'chore: normalize project structure'"
echo ""
echo "📝 Note: Documentation files (README.md, docs/) were not automatically updated."
echo "   Update them manually to reflect the new structure."
echo ""

