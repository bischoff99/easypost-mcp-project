# Package Manager Maintenance Guide

**Generated:** 2025-11-11
**System:** macOS 25.1.0 with zsh

## Executive Summary

Your development environment uses **mise** as the primary version manager for Node.js, Python, npm, and pnpm. However, conflicts exist with:

- **pyenv** (shadowed Python manager)
- **Homebrew** (duplicate node and Python installations)
- **Shell configs** (duplicate PATH entries, redundant activations)
- **pnpm** (version mismatch: reports 9.0.0 but path shows 10.20.0)

## Quick Fix

```bash
# Make scripts executable
chmod +x fix-package-conflicts.sh verify-package-managers.sh

# Run remediation
./fix-package-conflicts.sh

# Verify results (after restarting shell)
./verify-package-managers.sh
```

## Current State (Before Fixes)

### ✅ Working Correctly

- **mise** is primary version manager (2025.11.3)
- **PATH priority** is correct (mise before Homebrew)
- **Active versions** match mise installations:
  - node: 25.1.0 ✓
  - python: 3.14.0 ✓
  - npm: 11.6.2 ✓

### ⚠️ Issues Found

| Issue | Severity | Impact |
|-------|----------|--------|
| Python managed by mise + pyenv + Homebrew | High | Confusion, wasted disk space (~500MB) |
| pnpm version mismatch (9.0.0 vs 10.20.0) | High | Unexpected behaviour, broken features |
| Node.js in Homebrew + mise | Medium | Disk waste (~80MB), potential confusion |
| Duplicate LMStudio PATH entry | Low | Redundant PATH lookups |
| Multiple Homebrew Python versions | Low | Disk waste (~300MB) |

## Detailed Conflict Analysis

### 1. Python Triple Installation

**Problem:** Three Python version managers compete:

```
mise:     Python 3.14.0 (active)         ~/.local/share/mise/installs/python/3.14.0/
pyenv:    Python 3.13.0 (shadowed)       ~/.pyenv/versions/3.13.0/
homebrew: Python 3.12.12, 3.13.9, 3.14.0 /opt/homebrew/Cellar/python@*/
```

**Solution:**
```bash
# Keep mise only
brew uninstall pyenv
rm -rf ~/.pyenv
brew uninstall python@3.12 python@3.13 --ignore-dependencies
```

**Rationale:** mise is modern, fast, and handles multiple languages. pyenv is redundant.

---

### 2. pnpm Version Mismatch

**Problem:** Binary at path `10.20.0` reports version `9.0.0`

```bash
$ which pnpm
/Users/andrejs/.local/share/mise/installs/pnpm/10.20.0/pnpm

$ pnpm --version
9.0.0  # Should be 10.20.0+
```

**Solution:**
```bash
mise uninstall pnpm
mise install pnpm@latest
mise exec -- pnpm --version  # Verify
```

**Rationale:** Mise installation failed or binary corrupted. Clean reinstall required.

---

### 3. Duplicate Node.js Installation

**Problem:** Both mise and Homebrew have Node 25.1.0

```
mise:     node 25.1.0 (active)
homebrew: node 25.1.0_1 (shadowed, ~80MB waste)
```

**Solution:**
```bash
brew uninstall node --ignore-dependencies
```

**Rationale:** mise is your version manager. Homebrew node is redundant.

---

### 4. Shell Configuration Issues

**Problem:** Duplicate PATH additions and redundant activations

**.zprofile** (login shells):
```zsh
export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"
eval "$(/opt/homebrew/bin/brew shellenv)"
eval "$(~/.local/bin/mise activate zsh)"
export PATH="$PATH:$HOME/.lmstudio/bin"  # LMStudio #1
```

**.zshrc** (interactive shells):
```zsh
export PATH="$HOME/.console-ninja/.bin:$PATH"
export PATH="$BUN_INSTALL/bin:$PATH"
export PATH="$PATH:$HOME/.lmstudio/bin"  # LMStudio #2 (DUPLICATE!)

# Redundant mise activation
if ! command -v mise >/dev/null 2>&1 && [[ -x ~/.local/bin/mise ]]; then
  eval "$(~/.local/bin/mise activate zsh)"
fi
```

**Solution:**
```zsh
# Remove from .zshrc:
# 1. LMStudio PATH export (already in .zprofile)
# 2. Redundant mise activation (already in .zprofile)

sed -i '' '/lmstudio/d' ~/.zshrc
sed -i '' '/if ! command -v mise/,/fi/d' ~/.zshrc
```

**Rationale:** PATH modifications belong in `.zprofile` (login shells). `.zshrc` should only have interactive shell setup.

---

## Ongoing Maintenance

### Weekly Checks (5 minutes)

```bash
# Run verification script
./verify-package-managers.sh

# Update mise tools
mise upgrade
mise install  # Install any new versions

# Check for Homebrew conflicts
brew list --versions | grep -E '(node|python@)'
```

### Monthly Maintenance (15 minutes)

```bash
# Update Homebrew
brew update && brew upgrade

# Clean Homebrew cache
brew cleanup

# Verify mise versions match project
cd /path/to/project
mise install  # Installs versions from .tool-versions or config.toml

# Check PATH health
echo $PATH | tr ':' '\n' | nl
# Ensure:
# - mise paths come before Homebrew
# - No duplicates
# - Length < 20 entries
```

### Quarterly Review (30 minutes)

1. **Review installed tools:**
   ```bash
   mise list
   brew list --versions | wc -l
   pip list | wc -l
   npm list -g --depth=0
   ```

2. **Remove unused tools:**
   ```bash
   mise uninstall <tool>@<version>
   brew uninstall <package>
   ```

3. **Check shell startup time:**
   ```bash
   time zsh -i -c exit
   # Should be < 0.5s
   ```

4. **Audit shell configs:**
   ```bash
   # Check for redundant PATH exports
   grep -n 'export PATH' ~/.zshenv ~/.zprofile ~/.zshrc

   # Check for duplicate activations
   grep -n 'eval.*mise' ~/.zshenv ~/.zprofile ~/.zshrc
   ```

---

## Automation Tools

### 1. Git Hook (Run on Pull)

Create `.git/hooks/post-merge`:

```bash
#!/usr/bin/env zsh
# Auto-install mise versions after pulling

if [[ -f .tool-versions ]] || [[ -f mise.toml ]]; then
    echo "🔧 Installing mise versions..."
    mise install
fi
```

```bash
chmod +x .git/hooks/post-merge
```

### 2. direnv Integration

Install direnv for per-project environments:

```bash
brew install direnv

# Add to ~/.zshrc (AFTER mise activation):
eval "$(direnv hook zsh)"
```

Create `.envrc` in projects:

```bash
# .envrc
use mise  # Automatically activates mise versions
```

### 3. Weekly Cron Job

```bash
# Add to crontab (crontab -e):
0 9 * * 1 /Users/andrejs/Projects/personal/easypost-mcp-project/verify-package-managers.sh > /tmp/package-check.log 2>&1 && cat /tmp/package-check.log
```

### 4. Alternative: asdf or Universal Version Manager

If managing many languages, consider consolidating with:

- **asdf** (community-driven, plugin-based)
- **proto** (modern, Rust-based, fast)

Both can replace mise if you need Ruby, Java, Terraform, etc.

---

## Troubleshooting

### Issue: "command not found: <tool>"

**Diagnosis:**
```bash
echo $PATH | grep mise
mise which <tool>
```

**Fix:**
```bash
# Ensure mise is activated
eval "$(~/.local/bin/mise activate zsh)"

# Reinstall tool
mise install <tool>@<version>
```

---

### Issue: Wrong version active

**Diagnosis:**
```bash
which <tool>
<tool> --version
mise current <tool>
```

**Fix:**
```bash
# Check for shadowing
type -a <tool>

# Set version globally
mise use --global <tool>@<version>

# Or per-project
mise use <tool>@<version>
```

---

### Issue: Slow shell startup

**Diagnosis:**
```bash
zsh -i -x -c exit 2>&1 | grep -E 'mise|brew|pyenv'
```

**Fix:**
```bash
# Move expensive operations to .zprofile (login shells only)
# Keep .zshrc minimal for interactive shells
```

---

### Issue: PATH too long (>20 entries)

**Diagnosis:**
```bash
echo $PATH | tr ':' '\n' | wc -l
echo $PATH | tr ':' '\n' | nl
```

**Fix:**
```bash
# Remove redundant entries
# Consolidate similar paths
# Use mise instead of per-tool managers
```

---

## Best Practices

### 1. One Version Manager Per Language

✅ **Good:** mise for Node, Python, Ruby
❌ **Bad:** nvm + mise + homebrew node

### 2. PATH Priority

Order (first = highest priority):

1. User tools (`~/.local/bin`)
2. Version manager shims (mise)
3. Homebrew (`/opt/homebrew/bin`)
4. System paths (`/usr/bin`, `/bin`)

### 3. Shell Configuration

- **`.zshenv`**: Environment variables (always sourced)
- **`.zprofile`**: PATH modifications (login shells)
- **`.zshrc`**: Interactive shell setup (aliases, prompts)

### 4. Project-Specific Versions

Use mise config files:

```toml
# ~/.config/mise/config.toml (global defaults)
[tools]
node = "25"
python = "3.14"

# project/mise.toml (project-specific)
[tools]
node = "20.10.0"  # Override for this project
python = "3.12"
```

### 5. Documentation

Keep a log of installed tools:

```bash
# Generate inventory
mise list > mise-inventory.txt
brew list --versions > brew-inventory.txt
pip list > pip-inventory.txt
```

---

## Migration to Unified Manager (Optional)

If you want to consolidate everything to **mise**:

```bash
# 1. Install all tools via mise
mise install node@latest python@latest ruby@latest

# 2. Remove competing managers
brew uninstall nvm pyenv rbenv node python@*

# 3. Clean up shell configs
# Remove nvm, pyenv, rbenv activation scripts

# 4. Update projects
# Add mise.toml or .tool-versions to each project

# 5. Verify
./verify-package-managers.sh
```

---

## Additional Resources

- **mise docs**: https://mise.jdx.dev
- **Homebrew docs**: https://docs.brew.sh
- **zsh docs**: https://zsh.sourceforge.io/Doc/
- **PATH management**: https://github.com/jdx/mise/blob/main/docs/configuration.md

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2025-11-11 | Initial analysis | Detected conflicts |
| 2025-11-11 | Created remediation scripts | Automated fixes |

---

## Quick Reference Commands

```bash
# Check active versions
mise current

# Install specific version
mise install node@20.10.0

# Set global default
mise use --global python@3.14

# List all versions
mise ls-remote node

# Upgrade mise itself
mise self-update

# Verify installation
./verify-package-managers.sh

# Fix conflicts
./fix-package-conflicts.sh
```

---

**Next Steps:**

1. Run `./fix-package-conflicts.sh` (review each section first)
2. Restart terminal: `exec zsh`
3. Verify: `./verify-package-managers.sh`
4. Set up automation (cron job or Git hook)
5. Schedule monthly maintenance check
