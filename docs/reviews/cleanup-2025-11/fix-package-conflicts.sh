#!/usr/bin/env zsh
#
# Package Manager Conflict Remediation Script
# Generated: 2025-11-11
#
# This script resolves conflicts between mise, pyenv, homebrew, and shell configs.
# Review each section before running. You can comment out sections you don't want.
#
# Usage:
#   chmod +x fix-package-conflicts.sh
#   ./fix-package-conflicts.sh
#

set -euo pipefail

# Colours for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Colour

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Backup function
backup_file() {
    local file="$1"
    if [[ -f "$file" ]]; then
        local backup="${file}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$file" "$backup"
        log_info "Backed up $file to $backup"
    fi
}

echo "======================================"
echo "Package Manager Conflict Remediation"
echo "======================================"
echo ""

# ============================================================================
# SECTION 1: Fix pnpm version mismatch
# ============================================================================
log_info "SECTION 1: Fixing pnpm version mismatch"
echo "Current pnpm version: $(pnpm --version)"
echo "Expected: 10.20.0 or later"
echo ""

read -q "REPLY?Reinstall pnpm via mise? (y/n) "
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Uninstalling pnpm..."
    mise uninstall pnpm || log_warn "Failed to uninstall pnpm (may not be installed)"

    log_info "Installing pnpm@latest..."
    mise install pnpm@latest

    log_info "Verifying pnpm installation..."
    mise exec -- pnpm --version

    log_info "✓ pnpm reinstalled"
else
    log_warn "Skipped pnpm reinstall"
fi
echo ""

# ============================================================================
# SECTION 2: Remove pyenv (conflicting Python manager)
# ============================================================================
log_info "SECTION 2: Remove pyenv (conflicts with mise)"
echo "Pyenv is installed but shadowed by mise. Mise is the preferred manager."
echo "Pyenv versions: $(pyenv versions 2>/dev/null | tr '\n' ' ')"
echo ""

read -q "REPLY?Remove pyenv and its Python installations? (y/n) "
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Removing pyenv via Homebrew..."
    brew uninstall pyenv || log_warn "Pyenv not installed via brew"

    log_info "Removing pyenv directory..."
    if [[ -d "$HOME/.pyenv" ]]; then
        rm -rf "$HOME/.pyenv"
        log_info "✓ Removed ~/.pyenv"
    fi

    log_info "✓ pyenv removed"
else
    log_warn "Skipped pyenv removal (will continue to conflict with mise)"
fi
echo ""

# ============================================================================
# SECTION 3: Remove duplicate Node.js from Homebrew
# ============================================================================
log_info "SECTION 3: Remove homebrew Node.js (use mise instead)"
echo "Homebrew node version: $(brew list --versions node 2>/dev/null || echo 'not found')"
echo "Mise manages node already: $(mise list node 2>/dev/null | grep '25.1.0')"
echo ""

read -q "REPLY?Remove homebrew node? (y/n) "
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Removing node from Homebrew..."
    brew uninstall node --ignore-dependencies || log_warn "Node not installed via brew"

    log_info "✓ Homebrew node removed"
else
    log_warn "Skipped node removal (will waste disk space)"
fi
echo ""

# ============================================================================
# SECTION 4: Clean up unused Homebrew Python versions (optional)
# ============================================================================
log_info "SECTION 4: Clean up Homebrew Python versions (optional)"
echo "Homebrew Python installations:"
brew list --versions | grep python || echo "None found"
echo ""
echo "Mise manages Python 3.14.0. Homebrew versions are redundant."
echo ""

read -q "REPLY?Remove python@3.12 and python@3.13 from Homebrew? (y/n) "
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Removing python@3.12..."
    brew uninstall python@3.12 --ignore-dependencies || log_warn "python@3.12 not found"

    log_info "Removing python@3.13..."
    brew uninstall python@3.13 --ignore-dependencies || log_warn "python@3.13 not found"

    log_info "Keeping python@3.14 (may be used by other brew packages)"
    log_info "✓ Old Python versions removed"
else
    log_warn "Skipped Python cleanup (will waste ~300MB disk space)"
fi
echo ""

# ============================================================================
# SECTION 5: Fix shell configuration
# ============================================================================
log_info "SECTION 5: Fix shell configuration"
echo "Issues found:"
echo "  - Duplicate LMStudio PATH entry (.zprofile + .zshrc)"
echo "  - Redundant mise activation in .zshrc"
echo ""

read -q "REPLY?Fix shell configuration files? (y/n) "
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Fix .zshrc
    backup_file "$HOME/.zshrc"

    log_info "Removing duplicate LMStudio PATH from .zshrc..."
    sed -i.tmp '/export PATH=.*\.lmstudio/d' "$HOME/.zshrc"

    log_info "Removing redundant mise activation from .zshrc..."
    # Remove the redundant mise activation block (4 lines)
    sed -i.tmp '/if ! command -v mise/,/fi/d' "$HOME/.zshrc"

    rm -f "$HOME/.zshrc.tmp"

    log_info "✓ Shell configuration fixed"
    log_warn "You need to restart your shell or run: source ~/.zshrc"
else
    log_warn "Skipped shell config fixes"
fi
echo ""

# ============================================================================
# SECTION 6: Verify PATH deduplication
# ============================================================================
log_info "SECTION 6: Verify final configuration"
echo ""

log_info "Current PATH (after changes, requires shell restart):"
echo $PATH | tr ':' '\n' | nl

echo ""
log_info "Duplicate PATH entries:"
echo $PATH | tr ':' '\n' | sort | uniq -d | nl || echo "  None (good!)"

echo ""
log_info "Active tool versions:"
echo "  node:   $(which node) -> $(node --version)"
echo "  python: $(which python) -> $(python --version)"
echo "  pip:    $(which pip) -> $(pip --version | cut -d' ' -f1-2)"
echo "  npm:    $(which npm) -> $(npm --version)"
echo "  pnpm:   $(which pnpm) -> $(pnpm --version)"

echo ""
echo "======================================"
echo "Remediation Complete"
echo "======================================"
echo ""
log_warn "IMPORTANT: Restart your terminal or run: exec zsh"
log_info "Then verify with: ./verify-package-managers.sh"
echo ""
