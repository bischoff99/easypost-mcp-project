# direnv Setup Guide

## What is direnv?

**direnv** automatically loads environment variables when you `cd` into the project directory. No need to manually activate venv or source `.env` files.

## Setup Commands

### 1. Install direnv (if not installed)

```bash
brew install direnv
```

### 2. Add to shell config (if not already added)

**For zsh** (add to `~/.zshrc`):
```bash
eval "$(direnv hook zsh)"
```

Then reload shell:
```bash
source ~/.zshrc
```

### 3. Allow .envrc in this project

```bash
cd /Users/andrejs/Developer/github/andrejs/easypost-mcp-project
direnv allow
```

You only need to run `direnv allow` **once per project**. After that, direnv will automatically load `.envrc` whenever you `cd` into the project.

## What .envrc Does

When you `cd` into the project, `.envrc` automatically:

1. ✅ Activates Python virtual environment (`backend/venv`)
2. ✅ Loads `.env` file (environment variables)
3. ✅ Adds `backend/venv/bin` to PATH
4. ✅ Adds `node_modules/.bin` to PATH
5. ✅ Sets `PYTHONPATH` for Python imports
6. ✅ Falls back to macOS Keychain for `DATABASE_URL` if needed

## Verify Setup

```bash
cd /Users/andrejs/Developer/github/andrejs/easypost-mcp-project
# Should see: "direnv: loading .envrc"
# Then check:
echo $PYTHONPATH
which python  # Should point to backend/venv/bin/python
```

## Troubleshooting

**If direnv doesn't load:**
```bash
# Check if hook is in shell config
grep direnv ~/.zshrc

# Reload shell
source ~/.zshrc

# Manually allow
direnv allow
```

**If you see "direnv: error .envrc is blocked":**
```bash
direnv allow
```

## Optional: Disable direnv

If you don't want to use direnv, you can:
1. Remove `.envrc` file
2. Manually activate venv: `source backend/venv/bin/activate`
3. Backend app still works (loads `.env` via `config.py`)
