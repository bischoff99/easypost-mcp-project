#!/bin/bash
# Aggressive Extension Cleanup Script
# Removes ALL extensions except the 13 essential ones

# Essential extensions to KEEP
ESSENTIAL=(
  "ms-python.python"
  "ms-python.vscode-pylance"
  "ms-python.debugpy"
  "charliermarsh.ruff"
  "ms-python.mypy-type-checker"
  "dbaeumer.vscode-eslint"
  "esbenp.prettier-vscode"
  "bradlc.vscode-tailwindcss"
  "vitest.vitest"
  "eamodio.gitlens"
  "christian-kohler.path-intellisense"
  "ms-azuretools.vscode-docker"
  "yzhang.markdown-all-in-one"
)

echo "🧹 Aggressive Extension Cleanup"
echo "=============================="
echo ""
echo "✅ Keeping ONLY these 13 essential extensions:"
for ext in "${ESSENTIAL[@]}"; do
  echo "   • $ext"
done
echo ""

# Check if code command exists
if ! command -v code &> /dev/null; then
  echo "❌ Error: 'code' command not found"
  exit 1
fi

# Get all installed extensions
echo "📋 Analyzing installed extensions..."
INSTALLED=$(code --list-extensions)
TOTAL=$(echo "$INSTALLED" | wc -l | tr -d ' ')
echo "   Found $TOTAL installed extensions"
echo ""

# Find extensions to remove (everything NOT in essential list)
echo "🗑️  Extensions to remove:"
TO_REMOVE=()
REMOVED_COUNT=0

while IFS= read -r ext; do
  # Check if extension is in essential list
  IS_ESSENTIAL=false
  for essential in "${ESSENTIAL[@]}"; do
    if [ "$ext" == "$essential" ]; then
      IS_ESSENTIAL=true
      break
    fi
  done
  
  # If not essential, add to removal list
  if [ "$IS_ESSENTIAL" = false ]; then
    echo "   ❌ $ext"
    TO_REMOVE+=("$ext")
    REMOVED_COUNT=$((REMOVED_COUNT + 1))
  else
    echo "   ✅ $ext (keeping)"
  fi
done <<< "$INSTALLED"

if [ $REMOVED_COUNT -eq 0 ]; then
  echo ""
  echo "✅ All extensions are essential! Nothing to remove."
  exit 0
fi

echo ""
echo "📊 Summary:"
echo "   Total installed: $TOTAL"
echo "   Essential (keeping): ${#ESSENTIAL[@]}"
echo "   To remove: $REMOVED_COUNT"
echo "   Will have after cleanup: ${#ESSENTIAL[@]}"
echo ""

# Ask for confirmation
if [ "$1" != "--yes" ]; then
  echo "⚠️  WARNING: This will remove $REMOVED_COUNT extensions!"
  read -p "   Proceed? (y/N): " -n 1 -r
  echo ""
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 0
  fi
fi

# Uninstall extensions
echo ""
echo "🗑️  Uninstalling $REMOVED_COUNT extensions..."
UNINSTALLED=0
FAILED=0

for ext in "${TO_REMOVE[@]}"; do
  echo -n "   Removing $ext... "
  if code --uninstall-extension "$ext" &> /dev/null; then
    echo "✅"
    UNINSTALLED=$((UNINSTALLED + 1))
  else
    echo "❌ Failed"
    FAILED=$((FAILED + 1))
  fi
done

echo ""
echo "✅ Cleanup complete!"
echo "   Removed: $UNINSTALLED"
if [ $FAILED -gt 0 ]; then
  echo "   Failed: $FAILED (may be system extensions)"
fi

# Verify final count
FINAL=$(code --list-extensions 2>/dev/null | wc -l | tr -d ' ')
echo "   Final count: $FINAL extensions"
echo ""
echo "💡 Reload Cursor window: Cmd+Shift+P → 'Developer: Reload Window'"



