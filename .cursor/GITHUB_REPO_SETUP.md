# GitHub Repository Setup Guide

## 🚀 Quick Setup (3 Steps)

### Step 1: Authenticate GitHub CLI
```bash
gh auth login
```

Follow the prompts:
1. Choose: **GitHub.com**
2. Choose: **HTTPS** (recommended)
3. Authenticate with: **Login with a web browser** (easiest)
4. Copy the one-time code shown
5. Press Enter to open browser
6. Paste code and authorize

### Step 2: Create Repository
```bash
cd /Users/andrejs/easypost-mcp-project

# Create public repo
gh repo create easypost-mcp-project --public --source=. --remote=origin --push

# OR create private repo
gh repo create easypost-mcp-project --private --source=. --remote=origin --push
```

### Step 3: Done!
Your repository will be created at:
`https://github.com/YOUR_USERNAME/easypost-mcp-project`

---

## 📋 Detailed Options

### Create with Description
```bash
gh repo create easypost-mcp-project \
  --public \
  --description "EasyPost MCP Server - FastAPI backend + React frontend for shipping operations" \
  --source=. \
  --remote=origin \
  --push
```

### Create with Custom Settings
```bash
gh repo create easypost-mcp-project \
  --public \
  --description "EasyPost MCP Server with M3 Max optimizations" \
  --homepage "https://easypost-mcp.example.com" \
  --add-readme \
  --license mit \
  --source=. \
  --remote=origin \
  --push
```

### Just Create (Don't Push Yet)
```bash
gh repo create easypost-mcp-project \
  --public \
  --description "EasyPost MCP Server" \
  --source=. \
  --remote=origin

# Then push when ready:
git push -u origin master
```

---

## 🔧 Alternative: Manual Creation

If you prefer the GitHub website:

### 1. Create on GitHub.com
1. Go to https://github.com/new
2. Repository name: `easypost-mcp-project`
3. Description: "EasyPost MCP Server - FastAPI + React"
4. Choose Public or Private
5. **Don't** initialize with README (you have files)
6. Click "Create repository"

### 2. Connect Local to Remote
```bash
cd /Users/andrejs/easypost-mcp-project
git remote add origin https://github.com/YOUR_USERNAME/easypost-mcp-project.git
git branch -M main
git push -u origin main
```

---

## 📝 Before Pushing - Checklist

### ✅ Files to Keep Private
Make sure these are in `.gitignore`:
- `backend/.env` (contains API keys)
- `backend/.env.production`
- `backend/venv/`
- `node_modules/`
- `__pycache__/`
- `*.pyc`

### ✅ Files to Commit
These should be committed:
- `README.md` ✅
- `backend/.env.example` ✅
- `backend/requirements.txt` ✅
- `frontend/package.json` ✅
- All source code ✅
- Tests ✅
- Documentation ✅

### Check .gitignore
```bash
cat .gitignore | grep -E "(\.env$|venv|node_modules)"
```

---

## 🎯 Recommended Repository Settings

### After Creation, Configure:

#### 1. Add Topics (for discoverability)
```bash
gh repo edit --add-topic easypost
gh repo edit --add-topic mcp
gh repo edit --add-topic fastapi
gh repo edit --add-topic react
gh repo edit --add-topic shipping
gh repo edit --add-topic python
gh repo edit --add-topic javascript
```

#### 2. Set Homepage
```bash
gh repo edit --homepage "https://easypost.com"
```

#### 3. Enable Features
```bash
# Enable issues
gh repo edit --enable-issues=true

# Enable wiki
gh repo edit --enable-wiki=true

# Enable discussions (optional)
gh repo edit --enable-discussions=true
```

---

## 📊 Repository Details

### Suggested Configuration:

**Name:** `easypost-mcp-project`

**Description:**
```
EasyPost MCP Server - Model Context Protocol integration for shipping operations
FastAPI backend + React frontend with M3 Max optimizations
```

**Topics:**
- easypost
- mcp
- model-context-protocol
- fastapi
- react
- shipping
- logistics
- python
- javascript
- m3-max

**Features:**
- ✅ Issues
- ✅ Projects
- ✅ Wiki
- ⚠️ Discussions (optional)
- ✅ Security advisories

**Visibility:**
- 🔓 Public (recommended for portfolio)
- 🔒 Private (if contains sensitive logic)

---

## 🚀 Quick Commands Reference

```bash
# Authenticate
gh auth login

# Create public repo and push
gh repo create easypost-mcp-project --public --source=. --push

# Create private repo and push
gh repo create easypost-mcp-project --private --source=. --push

# View repo in browser
gh repo view --web

# Clone (for others)
gh repo clone YOUR_USERNAME/easypost-mcp-project
```

---

## 🔒 Security Best Practices

### 1. Add .env to .gitignore
```bash
echo ".env" >> .gitignore
echo ".env.production" >> .gitignore
git add .gitignore
git commit -m "chore: ensure .env files are ignored"
```

### 2. Create .env.example
```bash
cat > backend/.env.example << 'EOF'
# EasyPost API
EASYPOST_API_KEY=your_api_key_here

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
EOF

git add backend/.env.example
git commit -m "docs: add .env.example template"
```

### 3. Add Repository Secrets (for CI/CD)
```bash
# After repo creation:
gh secret set EASYPOST_API_KEY --body "your_key_here"
gh secret set DATABASE_URL --body "your_db_url_here"
```

---

## 📖 After Creation

### 1. Update README Badges
Add to `README.md`:
```markdown
[![GitHub](https://img.shields.io/github/license/YOUR_USERNAME/easypost-mcp-project)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.115-green.svg)](https://fastapi.tiangolo.com/)
```

### 2. Set Up Branch Protection
```bash
gh api repos/YOUR_USERNAME/easypost-mcp-project/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":[]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":1}'
```

### 3. Add Collaborators (if team project)
```bash
gh repo add-collaborator YOUR_USERNAME/easypost-mcp-project COLLABORATOR_USERNAME
```

---

## 🎯 Next Steps After Pushing

1. **Set up GitHub Actions** (if you have workflows)
2. **Add repository description and topics**
3. **Create initial release/tag**
4. **Set up GitHub Pages** (for docs)
5. **Configure branch protection**
6. **Add contributors**

---

## 🆘 Troubleshooting

### "Failed to create repository"
- Check if name is already taken
- Verify authentication: `gh auth status`
- Try different name

### "Permission denied"
- Re-authenticate: `gh auth logout && gh auth login`
- Check SSH keys: `gh ssh-key list`

### "Xcode license" error
- This affects `git` commands but not `gh` commands
- Use `gh` commands instead of `git`
- Or run: `sudo xcodebuild -license` (requires admin)

### Files not pushing
- Check `.gitignore` isn't too aggressive
- Verify files are staged: `git status`
- Check file sizes (GitHub has 100MB limit per file)

---

## ✅ Verification

After creation, verify:
```bash
# Check remote is set
gh repo view

# Check online
gh repo view --web

# Verify files pushed
gh browse
```

---

**Ready to create your repository! Run the commands above to get started.** 🚀

