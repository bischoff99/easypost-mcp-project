# Git Workflow Guide - EasyPost MCP

## Current Status

```bash
Branch: master
Remote: github.com/bischoff99/easypost-mcp-project
Status: 4 commits ahead, many uncommitted changes
```

## Quick Commands

### 1. **Commit All Changes** (Recommended)

```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "feat: add validation suite and dashboard improvements

- Add EasyPost API validation scripts
- Fix dashboard to show honest data
- Add nginx proxy configuration
- Reorganize documentation structure
- Add comprehensive audit reports
- Clean up unused code (8 ESLint warnings)
- Update backend endpoints for accuracy

Compliance: 79% (production-ready)
Closes #validation #dashboard-accuracy"

# Push to GitHub
git push origin master
```

### 2. **Commit by Category** (More organized)

```bash
# Option A: Use provided script
chmod +x scripts/git-commit-changes.sh
./scripts/git-commit-changes.sh

# Option B: Manual commits
git add backend/
git commit -m "feat(backend): improve API endpoints"

git add frontend/
git commit -m "fix(frontend): dashboard accuracy improvements"

git add scripts/
git commit -m "feat(scripts): add validation suite"

git add docs/ *.md
git commit -m "docs: add validation reports"

git push origin master
```

## Conventional Commits Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, semicolons)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Build/config changes

### Examples

```bash
git commit -m "feat(api): add bulk shipment endpoint"
git commit -m "fix(dashboard): correct delivery rate calculation"
git commit -m "docs: update API validation report"
git commit -m "test: add E2E tests for shipments"
git commit -m "chore: update dependencies"
```

## Branching Strategy

### Recommended: Git Flow (Simplified)

```
master (main)    → Production-ready code
  ↓
develop          → Integration branch
  ↓
feature/*        → New features
fix/*            → Bug fixes
docs/*           → Documentation updates
```

### Creating Branches

```bash
# Create feature branch
git checkout -b feature/user-authentication
git push -u origin feature/user-authentication

# Create fix branch
git checkout -b fix/analytics-error
git push -u origin fix/analytics-error

# Merge back to master
git checkout master
git merge feature/user-authentication
git push origin master
```

## GitHub Workflow

### 1. **Protect Master Branch** (Recommended)

On GitHub:
1. Settings → Branches → Add rule
2. Branch name pattern: `master`
3. Enable:
   - Require pull request reviews
   - Require status checks to pass
   - Include administrators

### 2. **Pull Request Process**

```bash
# Create feature branch
git checkout -b feature/real-time-updates

# Make changes and commit
git add .
git commit -m "feat: add WebSocket support"

# Push branch
git push -u origin feature/real-time-updates

# On GitHub: Create Pull Request
# After review: Merge PR
# Delete feature branch
git branch -d feature/real-time-updates
```

### 3. **Keeping Fork Updated**

```bash
# Add upstream (if forked)
git remote add upstream https://github.com/original/repo.git

# Fetch and merge
git fetch upstream
git merge upstream/master
git push origin master
```

## Git Aliases (Productivity)

Add to `~/.gitconfig`:

```ini
[alias]
    # Quick status
    st = status -sb

    # Better logs
    lg = log --oneline --graph --all --decorate

    # Quick commit
    cm = commit -m
    ca = commit -am

    # Branch management
    br = branch -v
    co = checkout

    # Undo last commit (keep changes)
    undo = reset HEAD~1 --soft

    # Clean up
    clean-merged = !git branch --merged | grep -v \"\\*\" | xargs -n 1 git branch -d
```

## Useful Git Commands

### View Changes

```bash
# See what changed
git diff

# See staged changes
git diff --staged

# See changes in specific file
git diff backend/src/server.py
```

### History

```bash
# View commit history
git log --oneline -10

# View changes in commit
git show <commit-hash>

# Find who changed a line
git blame backend/src/server.py
```

### Undo Changes

```bash
# Discard unstaged changes
git restore <file>

# Unstage file
git restore --staged <file>

# Undo last commit (keep changes)
git reset HEAD~1 --soft

# Undo last commit (discard changes) - DANGEROUS!
git reset HEAD~1 --hard
```

### Stash Changes

```bash
# Save changes temporarily
git stash

# List stashes
git stash list

# Apply stash
git stash apply

# Apply and delete stash
git stash pop
```

## .gitignore Essentials

Already configured, but for reference:

```gitignore
# Python
__pycache__/
*.py[cod]
venv/
.env

# Node
node_modules/
dist/
.cache/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*

# Testing
.coverage
htmlcov/
.pytest_cache/
```

## Pre-commit Hooks

Already configured in `.pre-commit-config.yaml`:

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

Runs on every commit:
- Trailing whitespace removal
- File endings normalization
- YAML validation
- Large files prevention
- Python syntax check
- JSON validation

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run tests
        run: |
          cd backend
          pytest tests/ -v
```

## Emergency Recovery

### Lost Changes?

```bash
# Find lost commits
git reflog

# Recover lost commit
git checkout <commit-hash>
git branch recovery-branch

# Or cherry-pick
git cherry-pick <commit-hash>
```

### Merge Conflicts

```bash
# During merge conflict
git status  # See conflicted files

# Edit files to resolve
# Then:
git add <resolved-file>
git commit

# Or abort merge
git merge --abort
```

## Best Practices

1. **Commit Often**
   - Small, focused commits
   - One logical change per commit
   - Makes debugging easier

2. **Write Good Messages**
   - Use conventional commits format
   - Explain WHY, not just WHAT
   - Reference issues: "Closes #123"

3. **Keep History Clean**
   - Avoid committing generated files
   - Don't commit secrets/credentials
   - Use .gitignore properly

4. **Pull Before Push**
   ```bash
   git pull --rebase origin master
   git push origin master
   ```

5. **Review Before Committing**
   ```bash
   git diff
   git status
   # Then commit
   ```

## Quick Reference Card

```bash
# Common workflow
git status                    # Check status
git add .                     # Stage all
git commit -m "message"       # Commit
git push origin master        # Push

# Branch workflow
git checkout -b feature/name  # Create branch
git add .                     # Stage
git commit -m "message"       # Commit
git push -u origin feature/name  # Push branch
# Create PR on GitHub
# Merge via GitHub UI

# Sync with remote
git fetch origin              # Download changes
git pull origin master        # Download + merge
git push origin master        # Upload changes

# Undo mistakes
git restore <file>            # Discard changes
git reset HEAD~1 --soft       # Undo commit
git stash                     # Save changes temporarily
```

## Your Current Changes

Run this to commit everything:

```bash
# Quick commit (all changes)
git add .
git commit -m "feat: add validation suite and dashboard improvements"
git push origin master

# Or use organized script
./scripts/git-commit-changes.sh
```

## Next Steps

1. **Commit your changes** (see commands above)
2. **Push to GitHub**: `git push origin master`
3. **Set up branch protection** (GitHub settings)
4. **Add GitHub Actions** (optional CI/CD)
5. **Create CONTRIBUTING.md** (collaboration guide)

---

**Resources**:
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Pro Git Book](https://git-scm.com/book/en/v2)
