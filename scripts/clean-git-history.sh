#!/bin/bash
# Clean API keys from git history using git-filter-repo
# WARNING: This rewrites git history and requires force push

set -e

echo "⚠️  WARNING: This script will rewrite git history!"
echo "⚠️  This requires force push and affects all collaborators."
echo ""
read -p "Are you sure you want to proceed? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# Check if git-filter-repo is installed
if ! command -v git-filter-repo &> /dev/null; then
    echo "❌ git-filter-repo not found. Install with:"
    echo "   pip install git-filter-repo"
    echo "   or"
    echo "   brew install git-filter-repo"
    exit 1
fi

# Remove file containing API keys from all history
echo "🧹 Removing .vscode/thunder-client-settings.json from git history..."
git filter-repo --path .vscode/thunder-client-settings.json --invert-paths

# Clean up reflog
echo "🧹 Cleaning up reflog..."
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Verify keys are removed
echo "✅ Verifying keys are removed from history..."
if git log --all --full-history -S "EZTK151720b5bbc44c08bd3c3f7a055b69ac" | grep -q .; then
    echo "❌ Test key still found in history!"
    exit 1
fi

if git log --all --full-history -S "EZAK151720b5bbc44c08bd3c3f7a055b69ac" | grep -q .; then
    echo "❌ Production key still found in history!"
    exit 1
fi

echo "✅ Keys successfully removed from git history!"
echo ""
echo "⚠️  Next steps:"
echo "1. Force push to remote: git push origin --force --all"
echo "2. Notify collaborators to re-clone repository"
echo "3. Rotate API keys at https://easypost.com/account/api-keys"

