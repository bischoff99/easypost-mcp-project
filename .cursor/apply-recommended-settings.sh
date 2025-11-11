#!/usr/bin/env bash
#
# Apply Recommended Cursor User Settings
# 
# This script backs up your current settings and applies the recommended configuration
# based on the sequential thinking analysis and official Cursor documentation.
#

set -e

USER_SETTINGS_PATH="$HOME/Library/Application Support/Cursor/User/settings.json"
BACKUP_PATH="$HOME/Library/Application Support/Cursor/User/settings.json.backup.$(date +%Y%m%d_%H%M%S)"
RECOMMENDED_PATH="$(dirname "$0")/recommended-user-settings.json"

echo "🔍 Cursor User Settings Update Script"
echo "======================================"
echo ""

# Check if current settings exist
if [ ! -f "$USER_SETTINGS_PATH" ]; then
    echo "❌ Error: User settings file not found at:"
    echo "   $USER_SETTINGS_PATH"
    exit 1
fi

# Check if recommended settings exist
if [ ! -f "$RECOMMENDED_PATH" ]; then
    echo "❌ Error: Recommended settings file not found at:"
    echo "   $RECOMMENDED_PATH"
    exit 1
fi

# Show current critical issue
echo "📋 Current Settings Analysis:"
echo ""
if grep -q '"python.languageServer": "None"' "$USER_SETTINGS_PATH"; then
    echo "❌ CRITICAL: python.languageServer is set to 'None' (disables IntelliSense)"
else
    echo "✅ python.languageServer looks okay"
fi

if grep -q '"security.workspace.trust.enabled"' "$USER_SETTINGS_PATH"; then
    echo "✅ Workspace trust is configured"
else
    echo "⚠️  security.workspace.trust.enabled not found"
fi

if grep -q '"editor.formatOnSave": true' "$USER_SETTINGS_PATH"; then
    echo "✅ Format on save is enabled"
else
    echo "⚠️  Format on save not configured"
fi

echo ""
echo "📦 Backup & Update Plan:"
echo "  1. Backup current settings to:"
echo "     $BACKUP_PATH"
echo "  2. Apply recommended settings from:"
echo "     $RECOMMENDED_PATH"
echo "  3. Reload Cursor window required after update"
echo ""

# Prompt for confirmation
read -p "❓ Do you want to proceed? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled. No changes made."
    exit 0
fi

# Create backup
echo "💾 Creating backup..."
cp "$USER_SETTINGS_PATH" "$BACKUP_PATH"
echo "✅ Backup created: $BACKUP_PATH"

# Apply recommended settings
echo "📝 Applying recommended settings..."
cp "$RECOMMENDED_PATH" "$USER_SETTINGS_PATH"
echo "✅ Settings updated successfully!"

echo ""
echo "🎉 Done! Next steps:"
echo ""
echo "1. Reload Cursor: Cmd + Shift + P → 'Reload Window'"
echo "2. Verify Python IntelliSense works:"
echo "   - Open a .py file"
echo "   - Type 'import ' and check autocomplete"
echo "3. Test format on save by editing and saving a file"
echo ""
echo "📄 Review the changes in:"
echo "   .cursor/USER_SETTINGS_REVIEW.md"
echo ""
echo "⚠️  If you need to revert:"
echo "   cp '$BACKUP_PATH' '$USER_SETTINGS_PATH'"
echo ""



