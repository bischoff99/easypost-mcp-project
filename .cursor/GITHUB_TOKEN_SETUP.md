# GitHub Personal Access Token Setup for MCP

## Quick Setup (5 Minutes)

### Step 1: Generate Token

1. **Visit**: https://github.com/settings/tokens
2. **Click**: "Generate new token" → "Generate new token (classic)"
3. **Name**: `Cursor MCP - EasyPost Project`
4. **Expiration**: 90 days (or No expiration for convenience)
5. **Select Scopes**:
   - ✅ `repo` (Full control of private repositories)
     - repo:status
     - repo_deployment
     - public_repo
     - repo:invite
     - security_events
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `admin:org` (Full control of orgs and teams) - Optional
   - ✅ `gist` (Create gists) - Optional

6. **Click**: "Generate token"
7. **Copy**: Token starts with `ghp_...`

⚠️ **Important**: Copy token immediately - you won't see it again!

### Step 2: Add Token to mcp.json

**Edit**: `~/.cursor/mcp.json`

**Find this section**:
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": ""
  }
}
```

**Replace with your token**:
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_actual_token_here"
  }
}
```

### Step 3: Reload Cursor

**Method 1**: Command Palette
```
Cmd+Shift+P → "Reload Window"
```

**Method 2**: Restart Cursor completely

### Step 4: Verify

Ask Cursor in chat:
```
"List my GitHub repositories"
"What's the status of the easypost-mcp-project repo?"
```

Should work without errors.

## What You Can Do with GitHub MCP

### Repository Management

```
"Create a new branch called feature/add-resources"
"List all branches in this repo"
"Switch to main branch"
```

### Commit Operations

```
"Commit all changes with message: feat: add Context7 and GitHub MCP"
"Show me the last 5 commits"
"What changed in the last commit?"
```

### Pull Requests

```
"Create a PR from feature/add-resources to main"
"List open PRs"
"Merge PR #123"
```

### Issue Management

```
"Create an issue: Add webhook support for tracking updates"
"List open issues"
"Close issue #5"
```

### Code Search

```
"Search for all files using FastMCP in my repos"
"Find examples of Pydantic validation in my code"
"Show me how I implemented error handling in other projects"
```

### File Operations

```
"Show me the contents of backend/src/server.py"
"What's in the README of my other project?"
"List all Python files in the backend"
```

## Security Best Practices

### Token Storage

✅ **Do**:
- Store token in mcp.json (local file, not committed)
- Use scoped tokens (minimum permissions needed)
- Set expiration dates
- Regenerate tokens periodically

❌ **Don't**:
- Commit mcp.json to git (it's in .gitignore)
- Share tokens publicly
- Use tokens with excessive permissions
- Store tokens in code files

### Token Scopes Explained

**Minimum Required**:
- `repo` - Read/write access to repositories

**Recommended Additional**:
- `workflow` - Update GitHub Actions
- `gist` - Create code snippets

**Optional**:
- `admin:org` - Manage organization repos
- `read:user` - Read user profile

### If Token is Compromised

1. **Revoke immediately**: https://github.com/settings/tokens
2. **Generate new token** with same scopes
3. **Update mcp.json** with new token
4. **Reload Cursor**

## Alternative: Use GitHub CLI

If you have GitHub CLI installed:

```json
"github": {
  "command": "gh",
  "args": ["mcp"]
}
```

This uses your existing `gh` authentication (no token needed).

## Troubleshooting

### GitHub MCP Not Loading

**Check token format**:
```bash
echo $GITHUB_PERSONAL_ACCESS_TOKEN | grep "^ghp_"
```

Should start with `ghp_`

**Test token manually**:
```bash
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
```

Should return your user info.

**Check Cursor logs**:
- Look for MCP errors in Cursor developer tools
- Verify token permissions are correct

### "Authentication failed" Error

**Causes**:
- Token expired
- Token revoked
- Insufficient scopes

**Fix**:
1. Generate new token
2. Ensure correct scopes selected
3. Update mcp.json
4. Reload Cursor

### "Rate limit exceeded"

GitHub API has rate limits:
- Authenticated: 5,000 requests/hour
- Unauthenticated: 60 requests/hour

**If you hit limits**:
- Wait an hour
- Check if token is working (should give 5k limit)
- Reduce frequency of operations

## Quick Reference

**Token Generation**: https://github.com/settings/tokens

**Required Scopes**:
- ✅ repo
- ✅ workflow

**Token Format**: `ghp_...` (starts with ghp_)

**Config Location**: `~/.cursor/mcp.json`

**Reload Cursor**: `Cmd+Shift+P` → "Reload Window"

**Test Command**: `"List my GitHub repositories"`

## Next Steps After Setup

1. **Test basic operations**:
   ```
   "Show me the status of easypost-mcp-project"
   "What branches exist?"
   "Show recent commits"
   ```

2. **Start using in workflow**:
   ```
   "Commit these changes: feat: add MCP servers"
   "Create issue: Add retry logic to EasyPost service"
   "Search for MCP server examples in my repos"
   ```

3. **Combine with Context7**:
   ```
   "How do I use GitHub MCP to create PRs? use context7"
   "Show me FastMCP examples from my repos and use context7 for latest docs"
   ```

---

**Total Setup Time**: ~5 minutes  
**Value**: Massive - never leave Cursor for Git operations
