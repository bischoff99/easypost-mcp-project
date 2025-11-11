#!/bin/bash
# Extension Cleanup Script
# Removes all non-essential extensions, keeping only the 13 essential ones

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

# Extensions to REMOVE (common clutter)
REMOVE=(
  # Deprecated formatters
  "ms-python.black-formatter"
  "ms-python.isort"
  
  # Deprecated test extensions
  "hbenl.vscode-test-explorer"
  "ms-vscode.test-adapter-converter"
  "littlefoxteam.vscode-python-test-adapter"
  
  # Performance issues
  "wix.vscode-import-cost"
  
  # Redundant AI assistants
  "github.copilot"
  "github.copilot-chat"
  "google.gemini-cli-vscode-ide-companion"
  "google.gemini-codeassist"
  "openai.chatgpt"
  "rooveterinaryinc.roo-cline"
  
  # Nice-to-have productivity (removed)
  "dsznajder.es7-react-js-snippets"
  "formulahendry.auto-rename-tag"
  "formulahendry.auto-close-tag"
  "wallabyjs.console-ninja"
  "njpwerner.autodocstring"
  "usernamehw.errorlens"
  "aaron-bond.better-comments"
  "gruntfuggly.todo-tree"
  "streetsidesoftware.code-spell-checker"
  "christian-kohler.npm-intellisense"
  "davidanson.vscode-markdownlint"
  "ms-vscode.makefile-tools"
  "donjayamanne.githistory"
  "tamasfe.even-better-toml"
  "redhat.vscode-yaml"
  "ms-vscode.vscode-json"
  "bierner.markdown-mermaid"
)

echo "🧹 Extension Cleanup Script"
echo "=========================="
echo ""
echo "✅ Keeping 13 essential extensions"
echo "❌ Removing ${#REMOVE[@]} unnecessary extensions"
echo ""

# Check if code command exists
if ! command -v code &> /dev/null; then
  echo "❌ Error: 'code' command not found"
  echo "   Please install VS Code command line tools:"
  echo "   Cmd+Shift+P → 'Shell Command: Install code command in PATH'"
  exit 1
fi

# List all installed extensions
echo "📋 Listing all installed extensions..."
INSTALLED=$(code --list-extensions)

# Count total
TOTAL=$(echo "$INSTALLED" | wc -l | tr -d ' ')
echo "   Found $TOTAL installed extensions"
echo ""

# Show what will be removed
echo "🗑️  Extensions to remove:"
REMOVED_COUNT=0
for ext in "${REMOVE[@]}"; do
  if echo "$INSTALLED" | grep -q "^${ext}$"; then
    echo "   ❌ $ext"
    REMOVED_COUNT=$((REMOVED_COUNT + 1))
  fi
done

if [ $REMOVED_COUNT -eq 0 ]; then
  echo "   ✅ No unnecessary extensions found to remove"
  echo ""
  echo "💡 To see all installed extensions:"
  echo "   code --list-extensions"
  exit 0
fi

echo ""
echo "📊 Summary:"
echo "   Total installed: $TOTAL"
echo "   To remove: $REMOVED_COUNT"
echo "   Will keep: $((TOTAL - REMOVED_COUNT))"
echo ""

# Ask for confirmation
if [ "$1" != "--yes" ]; then
  read -p "⚠️  Proceed with removal? (y/N): " -n 1 -r
  echo ""
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 0
  fi
fi

# Uninstall extensions
echo ""
echo "🗑️  Uninstalling extensions..."
UNINSTALLED=0
FAILED=0

for ext in "${REMOVE[@]}"; do
  if echo "$INSTALLED" | grep -q "^${ext}$"; then
    echo -n "   Removing $ext... "
    if code --uninstall-extension "$ext" &> /dev/null; then
      echo "✅"
      UNINSTALLED=$((UNINSTALLED + 1))
    else
      echo "❌ Failed"
      FAILED=$((FAILED + 1))
    fi
  fi
done

echo ""
echo "✅ Cleanup complete!"
echo "   Removed: $UNINSTALLED"
if [ $FAILED -gt 0 ]; then
  echo "   Failed: $FAILED"
fi
echo ""
echo "💡 Reload Cursor/VS Code window to see changes"
echo "   Cmd+Shift+P → 'Developer: Reload Window'"

