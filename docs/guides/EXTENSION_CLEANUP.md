# Extension Cleanup Guide

**Problem:** You have 64 extensions installed, but we've minimized to 13 essential ones.

**Solution:** Use one of these methods to remove unnecessary extensions.

## Method 1: Automated Script (Recommended)

Run the cleanup script:

```bash
./scripts/cleanup-extensions.sh
```

This script will:
- ✅ Keep the 13 essential extensions
- ❌ Remove 47+ unnecessary extensions
- 📊 Show you what will be removed before doing it

**Note:** Requires VS Code command line tools. If `code` command not found:
1. Open Cursor/VS Code
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
3. Type: `Shell Command: Install code command in PATH`
4. Run the script again

## Method 2: Manual Removal via Extension Manager

### Step 1: Open Extension Manager
- Press `Cmd+Shift+X` (Mac) or `Ctrl+Shift+X` (Windows/Linux)
- Or click the Extensions icon in the sidebar

### Step 2: Filter by "Installed"
- Click "Installed" in the sidebar
- You'll see all 64 installed extensions

### Step 3: Remove Unnecessary Extensions

**Quick removal list** (47 extensions to remove):

#### Deprecated Formatters (2)
- ❌ `ms-python.black-formatter`
- ❌ `ms-python.isort`

#### Deprecated Test Extensions (3)
- ❌ `hbenl.vscode-test-explorer`
- ❌ `ms-vscode.test-adapter-converter`
- ❌ `littlefoxteam.vscode-python-test-adapter`

#### Performance Issues (1)
- ❌ `wix.vscode-import-cost`

#### Redundant AI Assistants (6)
- ❌ `github.copilot`
- ❌ `github.copilot-chat`
- ❌ `google.gemini-cli-vscode-ide-companion`
- ❌ `google.gemini-codeassist`
- ❌ `openai.chatgpt`
- ❌ `rooveterinaryinc.roo-cline`

#### Nice-to-Have Productivity (9)
- ❌ `dsznajder.es7-react-js-snippets`
- ❌ `formulahendry.auto-rename-tag`
- ❌ `formulahendry.auto-close-tag`
- ❌ `wallabyjs.console-ninja`
- ❌ `njpwerner.autodocstring`
- ❌ `usernamehw.errorlens`
- ❌ `aaron-bond.better-comments`
- ❌ `gruntfuggly.todo-tree`
- ❌ `streetsidesoftware.code-spell-checker`

#### Redundant Tools (6)
- ❌ `christian-kohler.npm-intellisense`
- ❌ `davidanson.vscode-markdownlint`
- ❌ `ms-vscode.makefile-tools`
- ❌ `donjayamanne.githistory`
- ❌ `tamasfe.even-better-toml`
- ❌ `redhat.vscode-yaml`
- ❌ `ms-vscode.vscode-json`
- ❌ `bierner.markdown-mermaid`

**For each extension:**
1. Search for it in the Extension Manager
2. Click the gear icon ⚙️ next to it
3. Click "Uninstall"

### Step 4: Verify Essential Extensions

**Make sure these 13 are installed:**

#### Python/Backend (5)
- ✅ `ms-python.python`
- ✅ `ms-python.vscode-pylance`
- ✅ `ms-python.debugpy`
- ✅ `charliermarsh.ruff`
- ✅ `ms-python.mypy-type-checker`

#### Frontend (4)
- ✅ `dbaeumer.vscode-eslint`
- ✅ `esbenp.prettier-vscode`
- ✅ `bradlc.vscode-tailwindcss`
- ✅ `vitest.vitest`

#### Productivity (2)
- ✅ `eamodio.gitlens`
- ✅ `christian-kohler.path-intellisense`

#### DevOps (1)
- ✅ `ms-azuretools.vscode-docker`

#### Documentation (1)
- ✅ `yzhang.markdown-all-in-one`

## Method 3: Bulk Uninstall via Terminal

If you have VS Code command line tools installed:

```bash
# List all installed extensions
code --list-extensions

# Uninstall specific extension
code --uninstall-extension <extension-id>

# Example: Remove Error Lens
code --uninstall-extension usernamehw.errorlens
```

**Bulk uninstall script:**

```bash
# Run the cleanup script
./scripts/cleanup-extensions.sh
```

## Method 4: Reset Extensions (Nuclear Option)

If you want to start fresh:

1. **Backup your current extensions:**
   ```bash
   code --list-extensions > extensions-backup.txt
   ```

2. **Uninstall all extensions:**
   ```bash
   code --list-extensions | xargs -L 1 code --uninstall-extension
   ```

3. **Install only essential ones:**
   ```bash
   # Install from recommendations
   code --install-extension ms-python.python
   code --install-extension ms-python.vscode-pylance
   code --install-extension ms-python.debugpy
   code --install-extension charliermarsh.ruff
   code --install-extension ms-python.mypy-type-checker
   code --install-extension dbaeumer.vscode-eslint
   code --install-extension esbenp.prettier-vscode
   code --install-extension bradlc.vscode-tailwindcss
   code --install-extension vitest.vitest
   code --install-extension eamodio.gitlens
   code --install-extension christian-kohler.path-intellisense
   code --install-extension ms-azuretools.vscode-docker
   code --install-extension yzhang.markdown-all-in-one
   ```

## After Cleanup

1. **Reload Cursor/VS Code:**
   - Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
   - Type: `Developer: Reload Window`
   - Press Enter

2. **Verify:**
   - Open Extension Manager (`Cmd+Shift+X`)
   - Click "Installed"
   - You should see ~13 extensions (plus any system extensions)

3. **Test functionality:**
   - Python: Open a `.py` file, check IntelliSense works
   - Frontend: Open a `.jsx` file, check ESLint/Prettier work
   - Git: Check GitLens features in source control panel

## Troubleshooting

**"code command not found":**
- Install VS Code command line tools (see Method 1)
- Or use Method 2 (manual removal)

**Extensions still showing after uninstall:**
- Reload the window (`Cmd+Shift+P` → "Developer: Reload Window")
- Or restart Cursor/VS Code completely

**Some extensions won't uninstall:**
- They might be system extensions (built-in)
- Or required by other extensions
- Check the extension details for dependencies

## Expected Result

**Before:** 64 extensions installed  
**After:** ~13-15 extensions installed (13 essential + 2-3 system extensions)

**Benefits:**
- ✅ Faster startup time
- ✅ Lower memory usage
- ✅ Fewer conflicts
- ✅ Cleaner interface
- ✅ Easier onboarding

---

**Quick Command:**
```bash
./scripts/cleanup-extensions.sh
```




