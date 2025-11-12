#!/usr/bin/env zsh
#
# Environment Remediation Script (Enhanced)
# Generated: 2025-11-11
# Based on: environment-analysis-unified.json
#
# Resolves package manager conflicts, optimizes PATH, and cleans redundant installations.
#
# Usage:
#   ./resolve_env.sh                    # Interactive mode (default)
#   ./resolve_env.sh --dry-run          # Show what would be done without executing
#   ./resolve_env.sh --only=phase1      # Execute only Phase 1
#   ./resolve_env.sh --only=phase1,phase3  # Execute only Phases 1 and 3
#   ./resolve_env.sh --yes              # Non-interactive (auto-confirm all)
#   ./resolve_env.sh --help             # Show this help
#

set -eo pipefail

# Colours
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Colour

# Flags
DRY_RUN=false
AUTO_YES=false
ONLY_PHASES=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --yes)
            AUTO_YES=true
            shift
            ;;
        --only=*)
            ONLY_PHASES="${1#*=}"
            shift
            ;;
        --help)
            head -n 20 "$0" | tail -n +2 | sed 's/^# //'
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Helper functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_phase() { echo -e "${CYAN}[PHASE $1]${NC} $2"; }
log_action() { echo -e "${BLUE}  →${NC} $1"; }

# Backup function
backup_file() {
    local file="$1"
    if [[ -f "$file" ]]; then
        local backup="${file}.backup.$(date +%Y%m%d_%H%M%S)"
        if [[ "$DRY_RUN" == "true" ]]; then
            log_info "[DRY-RUN] Would backup $file to $backup"
        else
            cp "$file" "$backup"
            log_info "Backed up $file to $backup"
        fi
    fi
}

# Execute command with dry-run support
execute_cmd() {
    local cmd="$1"
    local description="$2"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_action "[DRY-RUN] $description"
        echo "          Command: $cmd"
    else
        log_action "$description"
        if eval "$cmd"; then
            echo "          ✓ Success"
        else
            echo "          ✗ Failed (continuing...)"
        fi
    fi
}

# Confirmation prompt
confirm() {
    local prompt="$1"
    if [[ "$AUTO_YES" == "true" ]]; then
        log_info "Auto-confirmed: $prompt"
        return 0
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would ask: $prompt"
        return 0
    fi

    echo -n -e "${YELLOW}$prompt (y/n)${NC} "
    read -r REPLY
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

# Check if phase should be executed
should_run_phase() {
    local phase_num="$1"

    if [[ -z "$ONLY_PHASES" ]]; then
        return 0  # Run all phases by default
    fi

    # Check if phase is in the ONLY_PHASES list
    if echo "$ONLY_PHASES" | grep -q "phase$phase_num\|$phase_num"; then
        return 0
    fi

    return 1
}

# Banner
echo "=========================================="
echo "Environment Remediation Script"
echo "=========================================="
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
    log_warn "DRY-RUN MODE: No changes will be made"
    echo ""
fi

if [[ -n "$ONLY_PHASES" ]]; then
    log_info "Executing only: $ONLY_PHASES"
    echo ""
fi

# ============================================================================
# PHASE 1: Critical Fixes (Functional Issues)
# ============================================================================
if should_run_phase 1; then
    log_phase 1 "Critical Fixes - Functional Issues"
    echo "This phase fixes issues that may cause immediate problems."
    echo ""

    # ACTION 1: Fix pnpm version mismatch
    log_info "ACTION: Fix pnpm version mismatch"
    echo "  Issue: pnpm reports version 9.0.0 but path shows 10.20.0"
    echo "  Impact: May cause package installation failures"
    echo "  Time: ~30 seconds"
    echo ""

    if confirm "Fix pnpm version mismatch?"; then
        execute_cmd "mise uninstall pnpm" "Uninstalling corrupted pnpm"
        execute_cmd "mise install pnpm@latest" "Installing pnpm@latest"
        execute_cmd "mise exec -- pnpm --version" "Verifying pnpm version"
        log_info "✓ pnpm reinstalled"
    else
        log_warn "Skipped pnpm fix"
    fi
    echo ""
else
    log_warn "Skipping Phase 1 (not in --only list)"
    echo ""
fi

# ============================================================================
# PHASE 2: Remove Competing Managers
# ============================================================================
if should_run_phase 2; then
    log_phase 2 "Remove Competing Managers"
    echo "This phase removes version managers that conflict with mise."
    echo ""

    # ACTION 2: Remove pyenv
    log_info "ACTION: Remove pyenv (competing Python manager)"
    echo "  Issue: pyenv conflicts with mise for Python management"
    echo "  Impact: Frees ~400MB, eliminates confusion"
    echo "  Time: ~15 seconds"
    echo ""

    if confirm "Remove pyenv and its directory?"; then
        execute_cmd "brew uninstall pyenv || true" "Uninstalling pyenv from Homebrew"
        execute_cmd "rm -rf ~/.pyenv" "Removing ~/.pyenv directory"
        log_info "✓ pyenv removed"
    else
        log_warn "Skipped pyenv removal (will continue to conflict with mise)"
    fi
    echo ""

    # ACTION 3: Remove nvm directory
    log_info "ACTION: Remove nvm directory"
    echo "  Issue: nvm directory present but not activated"
    echo "  Impact: Frees ~50MB, removes unused installation"
    echo "  Time: ~5 seconds"
    echo ""

    if confirm "Remove nvm directory?"; then
        execute_cmd "rm -rf ~/.nvm" "Removing ~/.nvm directory"
        log_info "✓ nvm directory removed"
    else
        log_warn "Skipped nvm removal"
    fi
    echo ""
else
    log_warn "Skipping Phase 2 (not in --only list)"
    echo ""
fi

# ============================================================================
# PHASE 3: Clean Redundant Installations
# ============================================================================
if should_run_phase 3; then
    log_phase 3 "Clean Redundant Installations"
    echo "This phase removes duplicate package installations to free disk space."
    echo ""

    # ACTION 4: Remove Homebrew Node.js
    log_info "ACTION: Remove Homebrew Node.js"
    echo "  Issue: Duplicate Node.js (mise + Homebrew)"
    echo "  Impact: Frees ~80MB, mise version already active"
    echo "  Time: ~10 seconds"
    echo "  Note: --ignore-dependencies keeps packages that depend on node"
    echo ""

    if confirm "Remove Homebrew node?"; then
        execute_cmd "brew uninstall node --ignore-dependencies || true" "Uninstalling Homebrew node"
        log_info "✓ Homebrew node removed"
    else
        log_warn "Skipped Homebrew node removal (will waste disk space)"
    fi
    echo ""

    # ACTION 5: Remove old Homebrew Python versions
    log_info "ACTION: Remove old Homebrew Python versions"
    echo "  Issue: Multiple Homebrew Python versions (3.12, 3.13, 3.14)"
    echo "  Impact: Frees ~300MB"
    echo "  Time: ~20 seconds"
    echo "  Note: Keeps python@3.14 as some brew packages may depend on it"
    echo ""

    if confirm "Remove python@3.12 and python@3.13 from Homebrew?"; then
        execute_cmd "brew uninstall python@3.12 --ignore-dependencies || true" "Removing python@3.12"
        execute_cmd "brew uninstall python@3.13 --ignore-dependencies || true" "Removing python@3.13"
        log_info "✓ Old Python versions removed (kept python@3.14)"
    else
        log_warn "Skipped Python cleanup (will waste ~300MB)"
    fi
    echo ""
else
    log_warn "Skipping Phase 3 (not in --only list)"
    echo ""
fi

# ============================================================================
# PHASE 4: Optimize Configuration
# ============================================================================
if should_run_phase 4; then
    log_phase 4 "Optimize Configuration"
    echo "This phase cleans up shell configuration files."
    echo ""

    # ACTION 6: Fix .zshrc duplicates
    log_info "ACTION: Fix .zshrc duplicates"
    echo "  Issue: Duplicate LMStudio PATH and redundant mise activation"
    echo "  Impact: Cleaner config, slightly faster shell startup"
    echo "  Time: ~5 seconds"
    echo ""

    if confirm "Fix .zshrc configuration?"; then
        backup_file "$HOME/.zshrc"

        # Remove LMStudio PATH export
        execute_cmd "sed -i '' '/lmstudio/d' ~/.zshrc" "Removing duplicate LMStudio PATH"

        # Remove redundant mise activation
        execute_cmd "sed -i '' '/if ! command -v mise/,/fi/d' ~/.zshrc" "Removing redundant mise activation"

        log_info "✓ .zshrc optimized"
    else
        log_warn "Skipped .zshrc fixes"
    fi
    echo ""

    # ACTION 7: PATH optimization (automatic after config fixes)
    log_info "ACTION: PATH optimization"
    echo "  Issue: PATH has 3 duplicate entries (27 total)"
    echo "  Impact: Automatic after shell restart"
    echo "  Note: Restart shell to apply changes: exec zsh"
    echo ""

    log_action "PATH will be deduplicated after shell restart"
    log_info "Run 'exec zsh' to apply changes"
    echo ""
else
    log_warn "Skipping Phase 4 (not in --only list)"
    echo ""
fi

# ============================================================================
# VERIFICATION
# ============================================================================
echo "=========================================="
echo "Verification"
echo "=========================================="
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "DRY-RUN MODE: Skipping verification"
else
    log_info "Running post-remediation checks..."
    echo ""

    # Verify pnpm
    if command -v pnpm &>/dev/null; then
        PNPM_VER=$(pnpm --version 2>/dev/null || echo "error")
        if [[ "$PNPM_VER" =~ ^[0-9]+\.[0-9]+ ]] && [[ ${PNPM_VER%%.*} -ge 10 ]]; then
            log_info "✓ pnpm version: $PNPM_VER (OK)"
        else
            log_warn "⚠ pnpm version: $PNPM_VER (expected 10.x+)"
        fi
    fi

    # Verify pyenv removed
    if command -v pyenv &>/dev/null; then
        log_warn "⚠ pyenv still present"
    else
        log_info "✓ pyenv removed"
    fi

    # Verify nvm removed
    if [[ -d "$HOME/.nvm" ]]; then
        log_warn "⚠ nvm directory still exists"
    else
        log_info "✓ nvm directory removed"
    fi

    # Verify Homebrew node
    if brew list node &>/dev/null; then
        log_warn "⚠ Homebrew node still installed"
    else
        log_info "✓ Homebrew node removed"
    fi

    # Verify Python versions
    if brew list python@3.12 &>/dev/null || brew list python@3.13 &>/dev/null; then
        log_warn "⚠ Old Homebrew Python versions still present"
    else
        log_info "✓ Old Homebrew Python versions removed"
    fi

    # Check PATH duplicates
    DUP_COUNT=$(echo $PATH | tr ':' '\n' | sort | uniq -d | wc -l | tr -d ' ')
    if [[ "$DUP_COUNT" -eq 0 ]]; then
        log_info "✓ No PATH duplicates (restart shell if not applied)"
    else
        log_warn "⚠ $DUP_COUNT duplicate PATH entries remain (restart shell)"
    fi
fi

echo ""

# ============================================================================
# SUMMARY & NEXT STEPS
# ============================================================================
echo "=========================================="
echo "Summary & Next Steps"
echo "=========================================="
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "DRY-RUN complete. No changes were made."
    echo ""
    log_info "To apply changes, run without --dry-run:"
    echo "  ./resolve_env.sh"
else
    log_info "Remediation complete!"
    echo ""
    log_info "Expected improvements:"
    echo "  • Disk space freed: ~880MB"
    echo "  • PATH entries: 27 → ~24"
    echo "  • Conflicts: 9 → 0"
    echo "  • Shell startup: ~50ms faster"
    echo ""
    log_warn "IMPORTANT: Restart your shell to apply PATH changes"
    echo "  Run: exec zsh"
    echo ""
    log_info "Next steps:"
    echo "  1. Restart shell: exec zsh"
    echo "  2. Verify: ./verify-package-managers.sh"
    echo "  3. Review: cat environment-analysis-unified.json"
fi

echo ""
echo "Documentation:"
echo "  • Full analysis: environment-analysis-unified.json"
echo "  • Maintenance guide: PACKAGE_MANAGER_MAINTENANCE.md"
echo "  • Summary: PACKAGE_CONFLICTS_SUMMARY.md"
echo ""

# ============================================================================
# ROLLBACK INFORMATION
# ============================================================================
if [[ "$DRY_RUN" == "false" ]] && [[ -f "$HOME/.zshrc.backup."* ]]; then
    echo "=========================================="
    echo "Rollback Information"
    echo "=========================================="
    echo ""
    log_info "Backups created:"
    ls -lt "$HOME"/.zshrc.backup.* 2>/dev/null | head -1 | awk '{print "  • " $NF}'
    echo ""
    log_info "To rollback changes:"
    echo "  1. Restore configs: cp ~/.zshrc.backup.* ~/.zshrc"
    echo "  2. Reinstall removed packages (see PACKAGE_MANAGER_MAINTENANCE.md)"
    echo "  3. Restart shell: exec zsh"
    echo ""
fi

exit 0
