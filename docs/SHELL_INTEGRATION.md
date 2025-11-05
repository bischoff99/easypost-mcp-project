# Shell Integration Guide

**Quick access to EasyPost MCP commands from anywhere in your terminal.**

---

## Installation

### Automatic Setup

```bash
cd /Users/andrejs/easypost-mcp-project
chmod +x scripts/setup-shell-integration.sh
./scripts/setup-shell-integration.sh
source ~/.zshrc  # or source ~/.bashrc
```

### Manual Setup

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# EasyPost MCP Shell Integration
export EASYPOST_PROJECT_ROOT="$HOME/easypost-mcp-project"
source "$EASYPOST_PROJECT_ROOT/scripts/shell-integration.sh"
# End EasyPost MCP
```

Reload:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

---

## Available Commands

### Navigation

```bash
ep                # Go to project root
```

### Quick Development

```bash
epdev             # Start backend + frontend (make dev)
eptest            # Run fast tests (make test-fast)
epcheck           # Run quality checks (make check)
epclean           # Clean artifacts (make clean)
epmake <target>   # Run any make command
```

### Workflow Aliases

```bash
ep-morning        # Clean + test + dev (15s)
ep-commit         # Format + lint + test (9s)
ep-push           # Check + sync + push (20s)
ep-release        # Full pre-release pipeline (45s)
```

### Functions

```bash
ep-health                    # Check server health
ep-qcp "commit message"      # Quick commit + push
ep-db-reset                  # Reset database (with confirmation)
ep-test-file <path>          # Run specific test file
ep-shell                     # Open shell with backend venv
ep-help                      # Show available commands
```

---

## Usage Examples

### Morning Routine

```bash
# From anywhere:
ep-morning
# → Cleans cache, runs tests, starts servers (15s)
```

### Quick Iteration

```bash
# Make changes...
eptest                       # Fast tests (3s)

# More changes...
eptest                       # Fast tests (3s)

# Ready to commit
ep-commit                    # Format + lint + test (9s)
ep-qcp "feat: add feature"   # Commit + push (7s)
```

### Testing Specific Files

```bash
# Test one file
ep-test-file tests/unit/test_shipment.py

# Or multiple
ep
cd backend
source venv/bin/activate
pytest tests/unit/test_*.py -v
```

### Database Operations

```bash
# Reset database (asks for confirmation)
ep-db-reset

# Or without shell integration
ep
make db-reset
```

### Pre-Release Workflow

```bash
# Full validation before release
ep-release
# → Clean + format + lint + test + benchmark + build (45s)
```

---

## ZSH Completion

If you installed via the setup script, tab completion is enabled:

```bash
cd /Users/andrejs/easypost-mcp-project
make <TAB>        # Shows all 25 targets with descriptions

# Examples:
make te<TAB>      # Completes to test/test-fast/test-watch/test-cov
make d<TAB>       # Completes to dev/dev-mock/db-reset/db-migrate/db-upgrade
```

---

## Customization

### Add Your Own Aliases

Edit `~/.zshrc` after the EasyPost integration:

```bash
# Your custom aliases
alias ep-quick='ep && make format && make test-fast'
alias ep-frontend='ep && cd frontend && npm run dev'
alias ep-backend='ep && cd backend && source venv/bin/activate'
```

### Change Project Location

Update the environment variable:

```bash
export EASYPOST_PROJECT_ROOT="/path/to/your/easypost-mcp-project"
```

### Add Custom Functions

```bash
# Run tests for current git branch changes only
ep-test-branch() {
    ep
    git diff --name-only main... | grep test_ | xargs pytest -v
}

# Open project in VS Code
ep-code() {
    code "$EASYPOST_PROJECT_ROOT"
}
```

---

## Troubleshooting

### Commands Not Found

```bash
# Check if integration is loaded
type ep-help
# Should show: ep-help is a shell function

# If not found, reload:
source ~/.zshrc
```

### Wrong Project Path

```bash
# Check current path
echo $EASYPOST_PROJECT_ROOT

# Update in ~/.zshrc:
export EASYPOST_PROJECT_ROOT="/correct/path"

# Reload
source ~/.zshrc
```

### Completions Not Working (zsh)

```bash
# Check completion directory
ls -la ~/.zsh/completions

# Verify fpath
echo $fpath | grep .zsh/completions

# Rebuild completion cache
rm ~/.zcompdump
compinit
```

### Reinstall

```bash
# Remove from ~/.zshrc
vim ~/.zshrc
# Delete lines between "# EasyPost MCP" markers

# Reinstall
./scripts/setup-shell-integration.sh
source ~/.zshrc
```

---

## Uninstall

```bash
# Remove from shell config
vim ~/.zshrc  # or ~/.bashrc

# Delete these lines:
# # EasyPost MCP Shell Integration
# export EASYPOST_PROJECT_ROOT="..."
# source "..."
# # End EasyPost MCP

# Remove completions (zsh only)
rm ~/.zsh/completions/_make

# Reload
source ~/.zshrc
```

---

## Advanced Usage

### Chaining Commands

```bash
# Test, then start dev if tests pass
eptest && epdev

# Clean, test, and show health
epclean && eptest && ep-health

# Quick iteration loop
while true; do eptest && break; sleep 5; done
```

### Using with Git Hooks

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
source "$HOME/.zshrc"
ep-commit
```

### Terminal Multiplexer (tmux/screen)

```bash
# Session 1: Development
tmux new-session -s ep-dev -d
tmux send-keys -t ep-dev "epdev" C-m

# Session 2: Tests
tmux new-window -t ep-dev
tmux send-keys -t ep-dev "ep && make test-watch" C-m

# Attach
tmux attach -t ep-dev
```

### SSH Remote Development

On remote server:

```bash
# Clone and setup
git clone <repo> ~/easypost-mcp-project
cd ~/easypost-mcp-project
./scripts/setup-shell-integration.sh
source ~/.zshrc

# Now use all commands
ep-morning
```

---

## Performance Tips

### Fast Iteration

```bash
# Use fast tests during development
eptest                    # 3s

# Full tests before commit
ep-commit                 # 9s

# Comprehensive before push
ep-push                   # 20s
```

### Parallel Development

```bash
# Terminal 1: Backend
ep && make backend

# Terminal 2: Frontend
ep && make frontend

# Terminal 3: Tests
ep && make test-watch
```

### Background Processes

```bash
# Start backend in background
epdev &

# Wait for startup
sleep 3

# Run tests
eptest

# Kill background
kill %1
```

---

## Integration with IDEs

### VS Code

Add to `tasks.json`:

```json
{
  "label": "EP: Morning Routine",
  "type": "shell",
  "command": "ep-morning",
  "problemMatcher": []
}
```

### JetBrains (PyCharm, WebStorm)

External Tools → Add:
- **Name:** EP Morning
- **Program:** `/bin/zsh`
- **Arguments:** `-c "source ~/.zshrc && ep-morning"`

---

## Summary

**Installed Commands:**
- 5 navigation/dev aliases
- 4 workflow aliases
- 6 utility functions
- Tab completion (zsh)

**Time Saved:**
- No `cd` to project root
- No `make` prefix typing
- Quick access from anywhere
- Faster workflows

**Before:**
```bash
cd ~/easypost-mcp-project
make format
make lint
make test-fast
git add -A
git commit -m "feat: add feature"
git push
# ~45 keystrokes, 7 commands
```

**After:**
```bash
ep-commit
ep-qcp "feat: add feature"
# ~35 keystrokes, 2 commands
```

**22% fewer keystrokes, 71% fewer commands.**

---

Run `ep-help` anytime to see all available commands.

