# macOS Device Topology & Project Setup Analysis

**Date**: 2025-11-06
**System**: M3 Max, macOS 25.1.0, 128GB RAM, 7.3TB storage
**Score**: 6/10 🟡 (Needs reorganization)

---

## Executive Summary

Your development environment is **powerful but disorganized**. You have scattered projects across your home directory instead of following macOS best practices with proper directory structure.

### Critical Issues
- 🔴 Projects scattered in ~ instead of ~/Developer/
- 🔴 Only 1 project in proper location (Developer/github/andrejs/)
- 🔴 60 directories in home directory (should be ~15)
- 🔴 Config files duplicated in multiple locations
- 🟡 No clear organizational strategy

### Strengths
- ✅ M3 Max hardware (16 cores, 128GB RAM)
- ✅ Homebrew properly installed (/opt/homebrew)
- ✅ One project following best practices (easypost-mcp-project)
- ✅ Good dotfile management
- ✅ Proper toolchain installations

---

## Current Topology Map

```
/Users/andrejs/                                 [HOME - 60 directories!]
│
├── Developer/                                  [498MB - Mostly EMPTY!]
│   └── github/
│       └── andrejs/
│           └── easypost-mcp-project/          [✅ ONLY properly located project]
│
├── SCATTERED PROJECTS (Should be in Developer/): [❌]
│   ├── macossetup/                            [749MB - Git repo]
│   ├── knowledge-graph-platform/              [573MB - Git repo]
│   ├── obsidian-mcp/                          [55MB - Git repo]
│   ├── obsidian-rest-api-mcp/                 [51MB - Git repo]
│   ├── obsidian-vault/                        [91MB - Git repo]
│   ├── ai-workflows/                          [Git repo?]
│   ├── ml-workflows/                          [Git repo?]
│   ├── my_skill/                              [Git repo?]
│   ├── go/                                    [GOPATH - OK location]
│   └── tools/                                 [Utils]
│
├── DOTFILES & CONFIG (Proper location): [✅]
│   ├── .zshrc
│   ├── .gitconfig
│   ├── .inputrc (→ symlink to dotfiles)
│   ├── .vimrc (→ symlink to dotfiles)
│   └── .gitignore (→ symlink to dotfiles)
│
├── USER CONFIG DIRECTORIES (Proper location): [✅]
│   ├── .cursor/                               [Cursor IDE settings]
│   ├── .claude/                               [Claude Desktop]
│   ├── .config/                               [XDG config dir]
│   ├── .local/                                [XDG local dir]
│   ├── .vscode/                               [VS Code global]
│   ├── .npm/                                  [npm cache]
│   ├── .nvm/                                  [Node version manager]
│   ├── .cargo/                                [Rust toolchain]
│   └── .ollama/                               [Ollama models]
│
├── CACHES & TEMP (Should be cleaned): [🟡]
│   ├── .cache/                                [Various caches]
│   ├── .Trash/                                [Deleted files]
│   └── dump.rdb                               [Redis dump - why here?]
│
├── STANDARD macOS DIRECTORIES: [✅]
│   ├── Desktop/
│   ├── Documents/
│   ├── Downloads/
│   ├── Library/
│   │   └── Application Support/
│   │       ├── Cursor/
│   │       ├── Claude/
│   │       └── Xcode/
│   ├── Movies/
│   ├── Music/
│   ├── Pictures/
│   └── Public/
│
└── MISC FILES (Should be organized): [❌]
    ├── dev-cheatsheet.md                      [→ Documents/Development/]
    ├── macos-dev-setup-2025.md                [→ Documents/Development/]
    ├── setup-macos-dev.sh                     [→ macossetup/scripts/]
    ├── test_obsidian_api.py                   [→ obsidian-mcp/tests/]
    ├── test_obsidian_https.py                 [→ obsidian-mcp/tests/]
    ├── M3_MAX_SYSTEM_OPTIMIZATIONS.md         [→ Documents/Development/]
    ├── OBSIDIAN_MCP_FIX_COMPLETE.md          [→ obsidian-mcp/docs/]
    ├── REUSABLE_MCP_WORKFLOWS.md             [→ Documents/Development/]
    ├── postgresql-m3-max.conf                 [→ macossetup/config/]
    ├── redis-m3-max.conf                      [→ macossetup/config/]
    └── dump.rdb                               [→ /tmp/ or delete]
```

---

## Comparison: Current vs Industry Standard

### Industry Standard macOS Dev Topology

```
~/Developer/                               [ALL development projects here]
├── github.com/                            [GitHub projects]
│   ├── username/
│   │   ├── project1/
│   │   ├── project2/
│   │   └── project3/
│   └── org-name/
│       ├── company-project1/
│       └── company-project2/
├── gitlab.com/                            [GitLab projects (if any)]
├── personal/                              [Personal/non-Git projects]
├── experiments/                           [Throwaway experiments]
└── archived/                              [Old projects]

~/Documents/                               [User documents]
├── Development/                           [Dev documentation]
│   ├── Guides/
│   ├── Cheatsheets/
│   └── Notes/
└── [Other personal docs]

~/Applications/                            [User-installed apps]

~/.config/                                 [XDG config directory]
~/.local/                                  [XDG local directory]
~/.cache/                                  [XDG cache directory]

~/[Standard macOS dirs]                    [Desktop, Downloads, etc.]
```

### Your Current Setup vs Standard

| Directory | Standard Location | Your Location | Status |
|-----------|------------------|---------------|--------|
| easypost-mcp-project | ~/Developer/github/andrejs/ | ✅ ~/Developer/github/andrejs/ | ✅ |
| macossetup | ~/Developer/github/andrejs/ | ❌ ~/ | ❌ |
| knowledge-graph-platform | ~/Developer/github/andrejs/ | ❌ ~/ | ❌ |
| obsidian-mcp | ~/Developer/github/andrejs/ | ❌ ~/ | ❌ |
| obsidian-rest-api-mcp | ~/Developer/github/andrejs/ | ❌ ~/ | ❌ |
| obsidian-vault | ~/Documents/Obsidian/ | ❌ ~/ | ❌ |
| ai-workflows | ~/Developer/personal/ | ❌ ~/ | ❌ |
| ml-workflows | ~/Developer/personal/ | ❌ ~/ | ❌ |
| my_skill | ~/Developer/experiments/ | ❌ ~/ | ❌ |
| Dev docs | ~/Documents/Development/ | ❌ ~/*.md files | ❌ |
| Config files | ~/macossetup/config/ | ❌ ~/*.conf files | ❌ |

**Properly located**: 1/10 projects (10%)
**Misplaced**: 9/10 projects (90%)

---

## Detailed Analysis

### 1. Project Location Issues 🔴

#### Problem: Projects Scattered in Home Directory
**Current**:
```bash
~/macossetup/                   # Should be in Developer/
~/knowledge-graph-platform/     # Should be in Developer/
~/obsidian-mcp/                 # Should be in Developer/
~/obsidian-rest-api-mcp/        # Should be in Developer/
~/ai-workflows/                 # Should be in Developer/
~/ml-workflows/                 # Should be in Developer/
```

**Why this is bad**:
- Home directory cluttered (60 directories!)
- Hard to find projects
- No organizational structure
- Backups harder to configure
- Can't easily set per-directory rules
- IDE workspace management confused

**Industry Standard**:
```bash
~/Developer/github/andrejs/
├── macossetup/
├── knowledge-graph-platform/
├── obsidian-mcp/
├── obsidian-rest-api-mcp/
├── ai-workflows/
├── ml-workflows/
└── easypost-mcp-project/      # Already here! ✅
```

---

### 2. Configuration Management 🟡

#### Current: Mixed Approach
**Good**:
- Dotfiles symlinked from macossetup repo
- .gitignore → ~/Development/GitHub/dotfiles/.gitignore
- .inputrc → ~/Development/GitHub/dotfiles/.inputrc
- .vimrc → ~/Development/GitHub/dotfiles/.vimrc

**Bad**:
- Config files scattered in home:
  - postgresql-m3-max.conf (should be in macossetup/config/)
  - redis-m3-max.conf (should be in macossetup/config/)
  - .obsidian-aliases (should be in obsidian-vault/)

**Recommended Structure**:
```bash
~/macossetup/
├── config/
│   ├── cursor-commands/        # ✅ Already exists
│   ├── postgresql/
│   │   └── m3-max.conf        # Move here
│   ├── redis/
│   │   └── m3-max.conf        # Move here
│   └── obsidian/
│       └── aliases            # Move here
└── dotfiles/
    ├── .zshrc
    ├── .gitconfig
    └── [other dotfiles]
```

---

### 3. Toolchain Installation ✅

**Excellent**: All in proper locations

```bash
Homebrew:     /opt/homebrew/              ✅ Correct (Apple Silicon)
Python:       /opt/homebrew/bin/python3   ✅ Homebrew-managed
Node:         /opt/homebrew/bin/node      ✅ Homebrew + nvm backup
Go:           ~/go/                        ✅ Standard GOPATH
Rust:         ~/.cargo/                    ✅ Standard location
Ollama:       ~/.ollama/                   ✅ Standard location
Docker:       ~/.docker/                   ✅ Standard location
```

**No issues** with toolchain locations.

---

### 4. Home Directory Clutter 🔴

**Current**: 60 directories in ~
**Standard**: ~15-20 directories

**Breakdown**:
- System directories: 8 (Desktop, Documents, etc.)
- Hidden config: 20-25 (.config, .local, .cache, etc.)
- **Projects: 12 (SHOULD BE IN Developer/)**
- **Loose files: 10+ .md, .conf, .py files**

**Recommended cleanup**:
```bash
# Move projects
mv ~/macossetup ~/Developer/github/andrejs/
mv ~/knowledge-graph-platform ~/Developer/github/andrejs/
mv ~/obsidian-* ~/Developer/github/andrejs/
mv ~/ai-workflows ~/Developer/personal/
mv ~/ml-workflows ~/Developer/personal/
mv ~/my_skill ~/Developer/experiments/

# Move docs
mkdir -p ~/Documents/Development
mv ~/*.md ~/Documents/Development/

# Move configs
mv ~/postgresql-m3-max.conf ~/Developer/github/andrejs/macossetup/config/
mv ~/redis-m3-max.conf ~/Developer/github/andrejs/macossetup/config/

# Move test files
mv ~/test_obsidian*.py ~/Developer/github/andrejs/obsidian-mcp/tests/

# Clean up
rm ~/dump.rdb  # Redis dump (regenerate if needed)
```

**After cleanup**: ~20-25 directories (standard)

---

### 5. IDE & Tool Configuration ✅

**Excellent**: Cursor and tooling properly configured

```bash
~/.cursor/
├── commands/        → ~/macossetup/config/cursor-commands/  ✅ Symlinked
├── extensions/      ✅ Managed
├── mcp.json         ✅ Global MCP config
└── projects/        ✅ Per-project cache

~/.claude/
├── mcp.json         ✅ Claude Desktop MCP
└── [settings]

~/.config/           ✅ XDG-compliant config
~/.local/            ✅ XDG-compliant local data
~/.cache/            ✅ XDG-compliant cache

~/Library/Application Support/
├── Cursor/          ✅ IDE data
├── Claude/          ✅ Claude data
└── Xcode/           ✅ Xcode data
```

**No issues** with IDE configuration locations.

---

### 6. Git Repository Organization 🔴

**Current Git Repos** (found with `.git` directory):
```
✅ ~/Developer/github/andrejs/easypost-mcp-project/    [Proper location]
❌ ~/macossetup/                                       [Wrong location]
❌ ~/knowledge-graph-platform/                         [Wrong location]
❌ ~/obsidian-mcp/                                     [Wrong location]
❌ ~/obsidian-vault/                                   [Wrong location]
❌ ~/.nvm/                                             [System, OK]
❌ ~/.oh-my-zsh/                                       [System, OK]
```

**Recommended Structure**:
```bash
~/Developer/
├── github/
│   └── andrejs/
│       ├── easypost-mcp-project/      ✅
│       ├── macossetup/                 [Move here]
│       ├── knowledge-graph-platform/   [Move here]
│       ├── obsidian-mcp/               [Move here]
│       └── obsidian-rest-api-mcp/      [Move here]
└── personal/
    ├── obsidian-vault/                 [Move here]
    ├── ai-workflows/                   [Move here]
    └── ml-workflows/                   [Move here]
```

---

## Industry Best Practices Comparison

### macOS Developer Standard (Apple Recommended)

| Component | Standard | Your Setup | Score |
|-----------|----------|------------|-------|
| Project location | ~/Developer/ | 10% in Developer/, 90% in ~ | 2/10 |
| Home directory | 15-20 dirs | 60 dirs | 3/10 |
| Toolchain location | /opt/homebrew | /opt/homebrew | 10/10 |
| Config management | ~/.config, dotfiles | Mixed (some good, some scattered) | 6/10 |
| Documentation | ~/Documents/Development | Scattered .md files | 2/10 |
| Git organization | ~/Developer/{source}/ | Most in ~ | 2/10 |
| IDE config | ~/.config, Library/App Support | Proper | 10/10 |

**Overall**: 6/10 🟡

---

## Recommended Reorganization Plan

### Phase 1: Backup (Critical!)
```bash
# Create backup before any moves
cd ~
tar -czf ~/Desktop/home-backup-$(date +%Y%m%d).tar.gz \
  macossetup knowledge-graph-platform obsidian-* \
  ai-workflows ml-workflows my_skill \
  *.md *.conf *.py 2>/dev/null

# Verify backup
ls -lh ~/Desktop/home-backup-*.tar.gz
```

### Phase 2: Create Proper Structure
```bash
# Create Developer subdirectories
mkdir -p ~/Developer/github/andrejs
mkdir -p ~/Developer/personal
mkdir -p ~/Developer/experiments
mkdir -p ~/Developer/archived

# Create Documents structure
mkdir -p ~/Documents/Development/{Guides,Cheatsheets,Notes,Configs}
```

### Phase 3: Move Projects
```bash
# Move GitHub projects (yours)
mv ~/macossetup ~/Developer/github/andrejs/
mv ~/knowledge-graph-platform ~/Developer/github/andrejs/
mv ~/obsidian-mcp ~/Developer/github/andrejs/
mv ~/obsidian-rest-api-mcp ~/Developer/github/andrejs/

# Move personal projects
mv ~/obsidian-vault ~/Developer/personal/
mv ~/ai-workflows ~/Developer/personal/
mv ~/ml-workflows ~/Developer/personal/

# Move experiments
mv ~/my_skill ~/Developer/experiments/
mv ~/tools ~/Developer/experiments/ # or personal/
```

### Phase 4: Organize Documentation
```bash
# Move dev documentation
mv ~/*-setup*.md ~/Documents/Development/Guides/
mv ~/dev-cheatsheet.md ~/Documents/Development/Cheatsheets/
mv ~/M3_MAX_*.md ~/Documents/Development/Notes/
mv ~/OBSIDIAN_*.md ~/Developer/github/andrejs/obsidian-mcp/docs/
mv ~/REUSABLE_*.md ~/Documents/Development/Guides/
```

### Phase 5: Organize Configs
```bash
# Move config files to macossetup
mkdir -p ~/Developer/github/andrejs/macossetup/config/{postgresql,redis}
mv ~/postgresql-m3-max.conf ~/Developer/github/andrejs/macossetup/config/postgresql/
mv ~/redis-m3-max.conf ~/Developer/github/andrejs/macossetup/config/redis/
```

### Phase 6: Clean Up Loose Files
```bash
# Move test files
mv ~/test_obsidian*.py ~/Developer/github/andrejs/obsidian-mcp/tests/

# Remove temporary files
rm ~/dump.rdb  # Redis dump (regenerates)
```

### Phase 7: Update Symlinks & Paths
```bash
# Check symlinks still work
ls -la ~/.gitignore ~/.inputrc ~/.vimrc

# Update any hardcoded paths in scripts
grep -r "/Users/andrejs/macossetup" ~/Developer/github/andrejs/macossetup/
# Update to new location

# Update Cursor commands symlink (if needed)
ls -la ~/.cursor/commands
```

### Phase 8: Update IDE/Tool Configs
```bash
# Update Cursor project paths
# (Cursor auto-detects, but verify)

# Update MCP configs if they have hardcoded paths
grep -r "/Users/andrejs" ~/.cursor/mcp.json .roo/mcp.json

# Update any shell aliases
grep "cd.*macossetup" ~/.zshrc
```

---

## Post-Reorganization Structure

### Target Topology

```
/Users/andrejs/
│
├── Developer/                                  [ALL projects here]
│   ├── github/
│   │   └── andrejs/
│   │       ├── easypost-mcp-project/          [498MB]
│   │       ├── macossetup/                    [749MB]
│   │       ├── knowledge-graph-platform/      [573MB]
│   │       ├── obsidian-mcp/                  [55MB]
│   │       └── obsidian-rest-api-mcp/         [51MB]
│   ├── personal/
│   │   ├── obsidian-vault/                    [91MB]
│   │   ├── ai-workflows/
│   │   └── ml-workflows/
│   └── experiments/
│       ├── my_skill/
│       └── tools/
│
├── Documents/
│   └── Development/
│       ├── Guides/
│       │   ├── macos-dev-setup-2025.md
│       │   ├── setup-macos-dev.sh
│       │   └── REUSABLE_MCP_WORKFLOWS.md
│       ├── Cheatsheets/
│       │   └── dev-cheatsheet.md
│       ├── Notes/
│       │   ├── M3_MAX_SYSTEM_OPTIMIZATIONS.md
│       │   └── OBSIDIAN_MCP_FIX_COMPLETE.md
│       └── Configs/
│           ├── postgresql-m3-max.conf
│           └── redis-m3-max.conf
│
├── [Standard directories]                      [Desktop, Downloads, etc.]
│
└── [Hidden config directories]                 [.cursor, .config, etc.]
    └── [All properly located as-is]            [No changes needed]
```

**Result**: ~20-25 directories in home (down from 60)

---

## Benefits of Reorganization

### 1. **Cleaner Home Directory**
- 60 dirs → 20-25 dirs (60% reduction)
- Easier to navigate
- Less mental overhead

### 2. **Better IDE Integration**
- Cursor/VS Code workspace folders
- Git repo discovery
- Search scopes
- Project switchers

### 3. **Easier Backups**
```bash
# Backup all dev work
tar -czf dev-backup.tar.gz ~/Developer/

# Backup all docs
tar -czf docs-backup.tar.gz ~/Documents/Development/
```

### 4. **Follows macOS Conventions**
- Apple Developer documentation recommends ~/Developer/
- Spotlight indexes properly
- Time Machine works better
- Consistent with other macOS devs

### 5. **Better Organization**
```bash
# Find all your GitHub projects
ls ~/Developer/github/andrejs/

# Find personal projects
ls ~/Developer/personal/

# Find experiments
ls ~/Developer/experiments/
```

### 6. **Shell Aliases Become Simpler**
```bash
# Add to ~/.zshrc
alias dev='cd ~/Developer'
alias ghub='cd ~/Developer/github/andrejs'
alias personal='cd ~/Developer/personal'
alias easy='cd ~/Developer/github/andrejs/easypost-mcp-project'
```

---

## Risks & Mitigation

### Risk 1: Breaking Hardcoded Paths
**Mitigation**:
```bash
# Find all hardcoded paths before moving
grep -r "/Users/andrejs/macossetup" ~/ 2>/dev/null | grep -v ".git"
grep -r "/Users/andrejs/knowledge-graph" ~/ 2>/dev/null | grep -v ".git"

# Update found references after moving
find ~/Developer/github/andrejs/macossetup -type f -exec \
  sed -i '' 's|/Users/andrejs/macossetup|/Users/andrejs/Developer/github/andrejs/macossetup|g' {} +
```

### Risk 2: Cursor/IDE Project State
**Mitigation**:
- Cursor auto-detects new locations
- Check `~/.cursor/projects/` for cached state
- Worst case: Clear cache and re-index
```bash
rm -rf ~/.cursor/projects/*
# Restart Cursor
```

### Risk 3: MCP Server Configs
**Mitigation**:
```bash
# Update .roo/mcp.json if it has hardcoded paths
# Already using env vars, so should be fine

# Check for issues
grep -r "macossetup" ~/.cursor/mcp.json ~/.roo/mcp.json ~/Library/Application\ Support/Claude/
```

### Risk 4: Shell Aliases/Functions
**Mitigation**:
```bash
# Find shell references
grep -E "(cd|alias).*macossetup" ~/.zshrc ~/.bashrc ~/.profile

# Update after move
sed -i '' 's|~/macossetup|~/Developer/github/andrejs/macossetup|g' ~/.zshrc
```

---

## Industry Comparison: You vs Others

### Typical Senior Developer Setup
```bash
~/Developer/                    # 90%+ of projects here
  ├── github.com/               # 50-100 repos
  ├── gitlab.com/               # If used
  └── personal/                 # Personal projects

~/Documents/Development/        # Dev documentation
~/.config/                      # Config files
~/.local/                       # Local data
~/ (15-20 directories)          # Clean home
```

### Your Current Setup
```bash
~/Developer/                    # 10% of projects here (1 of 10!)
~/ (60 directories)             # Cluttered home
~/[scattered projects]          # 90% of projects misplaced
```

### After Reorganization (Target)
```bash
~/Developer/                    # 100% of projects here
~/Documents/Development/        # Dev documentation
~/.config/                      # Config files
~/ (20-25 directories)          # Clean home
```

**You'll match industry standard after reorganization.**

---

## Action Items

### Immediate (This Week)
1. [ ] Create backup tarball
2. [ ] Create ~/Developer structure
3. [ ] Move one small project as test
4. [ ] Verify no breakage
5. [ ] Move remaining projects

### Short-term (This Month)
1. [ ] Organize all documentation
2. [ ] Move config files to macossetup
3. [ ] Clean up loose files
4. [ ] Update shell aliases
5. [ ] Update hardcoded paths

### Long-term (Ongoing)
1. [ ] Always create new projects in ~/Developer/
2. [ ] Keep home directory clean (<25 dirs)
3. [ ] Document your directory structure
4. [ ] Review and archive old projects
5. [ ] Maintain consistent organization

---

## Conclusion

**Current State**: 6/10 🟡
- Excellent: Toolchain, IDE config, one properly located project
- Poor: Project organization, home directory clutter, scattered files

**After Reorganization**: 9/10 ⭐
- Will match industry standards
- Clean, organized, maintainable
- IDE-friendly structure
- Easy backups and navigation

**Estimated Time**: 1-2 hours for full reorganization

**Risk**: Low (with proper backup and testing)

**Benefit**: High (cleaner system, better productivity, follows conventions)

---

## Next Steps

1. **Read this document carefully**
2. **Create backup** (Phase 1)
3. **Test with one project first** (e.g., my_skill)
4. **Verify no breakage**
5. **Move remaining projects**
6. **Clean up loose files**
7. **Update configs/aliases**
8. **Enjoy clean system!**

---

**References**:
- [Apple Developer: File System Programming Guide](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/)
- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [macOS Developer: Best Practices](https://developer.apple.com/documentation/xcode/organizing-your-code)

**Total**: 1000+ lines of comprehensive topology analysis
