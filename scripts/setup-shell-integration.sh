#!/bin/bash
# Setup Shell Integration for EasyPost MCP
# Installs aliases, functions, and completions

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHELL_INTEGRATION="$PROJECT_ROOT/scripts/shell-integration.sh"
COMPLETION_FILE="$PROJECT_ROOT/scripts/completions/_easypost-make"

echo "🔧 Setting up EasyPost MCP shell integration..."
echo ""

# Detect shell
SHELL_TYPE=$(basename "$SHELL")
if [ "$SHELL_TYPE" != "zsh" ] && [ "$SHELL_TYPE" != "bash" ]; then
    echo "⚠️  Unsupported shell: $SHELL_TYPE"
    echo "    This script supports zsh and bash only"
    exit 1
fi

echo "✓ Detected shell: $SHELL_TYPE"

# Shell config file
if [ "$SHELL_TYPE" = "zsh" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ "$SHELL_TYPE" = "bash" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

echo "✓ Config file: $SHELL_RC"

# Check if already installed
if grep -q "# EasyPost MCP Shell Integration" "$SHELL_RC" 2>/dev/null; then
    echo ""
    echo "⚠️  Shell integration already installed in $SHELL_RC"
    read -p "   Reinstall? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Cancelled."
        exit 0
    fi
    # Remove old installation
    sed -i.bak '/# EasyPost MCP Shell Integration/,/# End EasyPost MCP/d' "$SHELL_RC"
    echo "✓ Removed old installation"
fi

# Add to shell config
echo "" >> "$SHELL_RC"
echo "# EasyPost MCP Shell Integration" >> "$SHELL_RC"
echo "export EASYPOST_PROJECT_ROOT=\"$PROJECT_ROOT\"" >> "$SHELL_RC"
echo "source \"$SHELL_INTEGRATION\"" >> "$SHELL_RC"
echo "# End EasyPost MCP" >> "$SHELL_RC"

echo "✓ Added to $SHELL_RC"

# Setup completions for zsh
if [ "$SHELL_TYPE" = "zsh" ]; then
    COMPLETION_DIR="$HOME/.zsh/completions"
    mkdir -p "$COMPLETION_DIR"

    # Copy completion file
    cp "$COMPLETION_FILE" "$COMPLETION_DIR/_make"
    echo "✓ Installed completions to $COMPLETION_DIR"

    # Add fpath if not already there
    if ! grep -q "$COMPLETION_DIR" "$SHELL_RC"; then
        sed -i.bak "1i\\
fpath=($COMPLETION_DIR \$fpath)
" "$SHELL_RC"
        echo "✓ Added completion directory to fpath"
    fi

    # Add autoload if not already there
    if ! grep -q "autoload -Uz compinit" "$SHELL_RC"; then
        echo "autoload -Uz compinit && compinit" >> "$SHELL_RC"
        echo "✓ Enabled zsh completion system"
    fi
fi

echo ""
echo "✅ Shell integration installed successfully!"
echo ""
echo "📋 Available commands:"
echo "  ep                - Go to project root"
echo "  epdev             - Start development"
echo "  eptest            - Run fast tests"
echo "  ep-morning        - Morning routine"
echo "  ep-commit         - Pre-commit checks"
echo "  ep-qcp \"message\"  - Quick commit + push"
echo "  ep-help           - Show all commands"
echo ""
echo "🔄 To activate now, run:"
echo "   source $SHELL_RC"
echo ""
echo "Or open a new terminal window."

