#!/bin/bash
# Fix Persistent isort Errors in Cursor IDE
# This script helps resolve isort extension errors

set -e

echo "🔧 Fixing isort errors in Cursor IDE..."
echo ""

# Check if isort extension is installed
if code --list-extensions | grep -q "ms-python.isort"; then
    echo "⚠️  isort extension found. Uninstalling..."
    code --uninstall-extension ms-python.isort
    echo "✅ isort extension uninstalled"
else
    echo "✅ isort extension not installed"
fi

# Verify settings.json is valid
echo ""
echo "📋 Validating settings.json..."
if python3 -m json.tool .vscode/settings.json > /dev/null 2>&1; then
    echo "✅ settings.json is valid JSON"
else
    echo "❌ settings.json has syntax errors!"
    exit 1
fi

# Check for isort settings
echo ""
echo "🔍 Checking isort configuration..."
if grep -q '"isort.enable": false' .vscode/settings.json && \
   grep -q '"python.sortImports.provider": "none"' .vscode/settings.json; then
    echo "✅ isort is properly disabled in settings"
else
    echo "⚠️  Warning: isort settings may not be properly configured"
fi

echo ""
echo "📝 Next steps:"
echo "1. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows/Linux)"
echo "2. Type 'Developer: Reload Window'"
echo "3. Press Enter"
echo ""
echo "If errors persist after reload:"
echo "- Completely quit Cursor (Cmd+Q on Mac)"
echo "- Restart Cursor"
echo "- Reopen this workspace"
echo ""
echo "✅ Script completed!"
