#!/usr/bin/env zsh
#
# Package Manager Verification Script
# Generated: 2025-11-11
#
# Checks for conflicts and validates package manager configuration.
# Run this periodically to ensure environment stays clean.
#
# Usage: ./verify-package-managers.sh
#

set -eo pipefail

# Colours
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASS=0
WARN=0
FAIL=0

check_pass() {
    echo -e "  ${GREEN}✓${NC} $1"
    PASS=$((PASS + 1))
}

check_warn() {
    echo -e "  ${YELLOW}⚠${NC} $1"
    WARN=$((WARN + 1))
}

check_fail() {
    echo -e "  ${RED}✗${NC} $1"
    FAIL=$((FAIL + 1))
}

echo "======================================"
echo "Package Manager Health Check"
echo "======================================"
echo ""

# ============================================================================
# Check 1: PATH duplicates
# ============================================================================
echo -e "${BLUE}[1] Checking for PATH duplicates...${NC}"
duplicates=$(echo $PATH | tr ':' '\n' | sort | uniq -d)
if [[ -z "$duplicates" ]]; then
    check_pass "No duplicate PATH entries"
else
    check_warn "Duplicate PATH entries found"
    echo "$duplicates" | while IFS= read -r dup; do
        if [[ -n "$dup" ]]; then
            echo "      - $dup"
        fi
    done
fi
echo ""

# ============================================================================
# Check 2: Version manager conflicts
# ============================================================================
echo -e "${BLUE}[2] Checking for version manager conflicts...${NC}"

# Check mise
if command -v mise &>/dev/null; then
    check_pass "mise installed ($(mise --version | head -1))"
else
    check_fail "mise not found"
fi

# Check pyenv
if command -v pyenv &>/dev/null; then
    check_warn "pyenv installed (conflicts with mise)"
    echo "      Run: brew uninstall pyenv && rm -rf ~/.pyenv"
elif [[ -d "$HOME/.pyenv" ]]; then
    check_warn "pyenv directory exists but not in PATH"
    echo "      Run: rm -rf ~/.pyenv"
else
    check_pass "pyenv not installed (good)"
fi

# Check nvm
if [[ -d "$HOME/.nvm" ]] || command -v nvm &>/dev/null; then
    check_warn "nvm installed (mise preferred)"
else
    check_pass "nvm not installed (good)"
fi

# Check rbenv
if command -v rbenv &>/dev/null; then
    check_warn "rbenv installed (mise preferred)"
else
    check_pass "rbenv not installed (good)"
fi
echo ""

# ============================================================================
# Check 3: Tool versions match expected
# ============================================================================
echo -e "${BLUE}[3] Checking active tool versions...${NC}"

# Node
if [[ "$(which node)" =~ "mise" ]]; then
    check_pass "node managed by mise: $(node --version)"
else
    check_warn "node not from mise: $(which node)"
fi

# Python
if [[ "$(which python)" =~ "mise" ]]; then
    check_pass "python managed by mise: $(python --version)"
else
    check_warn "python not from mise: $(which python)"
fi

# pnpm version check
pnpm_version=$(pnpm --version)
pnpm_path=$(which pnpm)
if [[ "$pnpm_path" =~ "mise" ]]; then
    if [[ "$pnpm_version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] && [[ ${pnpm_version%%.*} -ge 10 ]]; then
        check_pass "pnpm managed by mise: v${pnpm_version}"
    else
        check_warn "pnpm version mismatch: v${pnpm_version} (expected 10.x+)"
        echo "      Run: mise uninstall pnpm && mise install pnpm@latest"
    fi
else
    check_warn "pnpm not from mise: $pnpm_path"
fi
echo ""

# ============================================================================
# Check 4: Homebrew conflicts
# ============================================================================
echo -e "${BLUE}[4] Checking for Homebrew conflicts...${NC}"

if brew list node &>/dev/null; then
    check_warn "Homebrew node installed (redundant with mise)"
    echo "      Run: brew uninstall node --ignore-dependencies"
else
    check_pass "Homebrew node not installed (good)"
fi

python_versions=$(brew list --versions | grep -E '^python@' | wc -l | tr -d ' ')
if [[ $python_versions -gt 1 ]]; then
    check_warn "Multiple Homebrew Python versions installed ($python_versions)"
    brew list --versions | grep -E '^python@' | while read -r line; do
        echo "      - $line"
    done
    echo "      Consider: brew uninstall python@3.12 python@3.13 --ignore-dependencies"
elif [[ $python_versions -eq 1 ]]; then
    check_pass "Single Homebrew Python version (acceptable)"
else
    check_pass "No Homebrew Python versions (good)"
fi
echo ""

# ============================================================================
# Check 5: Shell configuration
# ============================================================================
echo -e "${BLUE}[5] Checking shell configuration...${NC}"

# Check for duplicate PATH additions
zshrc_lmstudio=$(grep -c 'lmstudio' ~/.zshrc 2>/dev/null || echo 0)
zprofile_lmstudio=$(grep -c 'lmstudio' ~/.zprofile 2>/dev/null || echo 0)

if [[ $zshrc_lmstudio -gt 0 ]] && [[ $zprofile_lmstudio -gt 0 ]]; then
    check_warn "LMStudio PATH added in both .zshrc and .zprofile"
    echo "      Remove from .zshrc: sed -i '' '/lmstudio/d' ~/.zshrc"
elif [[ $zprofile_lmstudio -gt 0 ]]; then
    check_pass "LMStudio PATH in .zprofile only (good)"
else
    check_pass "LMStudio PATH configuration OK"
fi

# Check mise activation
if grep -q 'mise activate' ~/.zprofile 2>/dev/null; then
    check_pass "mise activated in .zprofile (correct)"
else
    check_warn "mise not activated in .zprofile"
fi

if grep -q 'mise activate' ~/.zshrc 2>/dev/null; then
    check_warn "Redundant mise activation in .zshrc"
    echo "      Remove redundant activation from .zshrc"
fi
echo ""

# ============================================================================
# Check 6: PATH length and order
# ============================================================================
echo -e "${BLUE}[6] Checking PATH health...${NC}"

path_count=$(echo $PATH | tr ':' '\n' | wc -l | tr -d ' ')
if [[ $path_count -lt 15 ]]; then
    check_pass "PATH length optimal ($path_count entries)"
elif [[ $path_count -lt 20 ]]; then
    check_warn "PATH slightly long ($path_count entries, optimal: <15)"
else
    check_warn "PATH very long ($path_count entries, optimal: <15)"
fi

# Check if mise paths come before homebrew
mise_pos=$(echo $PATH | tr ':' '\n' | grep -n 'mise' | head -1 | cut -d: -f1)
brew_pos=$(echo $PATH | tr ':' '\n' | grep -n 'homebrew' | head -1 | cut -d: -f1)

if [[ -n "$mise_pos" ]] && [[ -n "$brew_pos" ]] && [[ $mise_pos -lt $brew_pos ]]; then
    check_pass "mise paths prioritised correctly (before Homebrew)"
else
    check_warn "PATH order may be incorrect"
fi
echo ""

# ============================================================================
# Check 7: Mise configuration
# ============================================================================
echo -e "${BLUE}[7] Checking mise configuration...${NC}"

if [[ -f "$HOME/.config/mise/config.toml" ]]; then
    check_pass "mise config file exists"

    # Check for pinned versions
    if grep -q 'node.*=' ~/.config/mise/config.toml; then
        node_ver=$(grep 'node.*=' ~/.config/mise/config.toml | sed 's/.*=\s*"\(.*\)"/\1/')
        check_pass "node pinned to: $node_ver"
    fi

    if grep -q 'python.*=' ~/.config/mise/config.toml; then
        python_ver=$(grep 'python.*=' ~/.config/mise/config.toml | sed 's/.*=\s*"\(.*\)"/\1/')
        check_pass "python pinned to: $python_ver"
    fi
else
    check_warn "mise config file not found"
fi
echo ""

# ============================================================================
# Summary
# ============================================================================
echo "======================================"
echo -e "${GREEN}Passed: $PASS${NC} | ${YELLOW}Warnings: $WARN${NC} | ${RED}Failed: $FAIL${NC}"
echo "======================================"
echo ""

if [[ $FAIL -gt 0 ]]; then
    echo -e "${RED}Critical issues found. Review failed checks above.${NC}"
    exit 1
elif [[ $WARN -gt 0 ]]; then
    echo -e "${YELLOW}Warnings found. Consider running fix-package-conflicts.sh${NC}"
    exit 0
else
    echo -e "${GREEN}All checks passed! Environment is clean.${NC}"
    exit 0
fi
