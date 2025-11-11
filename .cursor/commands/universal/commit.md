Smart git commits with conventional commit messages, automatic change detection, and intelligent commit type determination.

**Context-aware**: No arguments needed - automatically detects changes from git status and generates appropriate commit messages. Supports conventional commits, automatic staging, and optional push.

## How It Works

**Complete MCP Workflow (5 Stages):**

**Stage 1 - Detect Changes**:
- Reads git status for modified, added, deleted files
- Gets staged changes if any
- Analyzes git diff for change scope

**Stage 2 - Analyze Changes**:
- Uses Sequential-thinking to determine commit type
- Identifies scope (module/component)
- Detects breaking changes
- Generates commit summary

**Stage 3 - Generate Message**:
- Creates conventional commit message
- Formats with type, scope, description, body, footer
- Validates message format

**Stage 4 - Stage Files**:
- Stages all changes or selective staging
- Verifies files staged correctly

**Stage 5 - Commit**:
- Creates commit with generated message
- Optionally pushes to remote
- Verifies commit created successfully

## Conventional Commit Types

**Standard Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, config)

**Special Types:**
- `build`: Build system changes
- `ci`: CI/CD changes
- `revert`: Revert previous commit

## MCP Integration

### Stage 1 - Detect Changes

```yaml
Tool: mcp_desktop-commander_start_process
Command: "git status --porcelain"
Timeout: 5000ms

Parse output:
  - Modified files (M)
  - Added files (A)
  - Deleted files (D)
  - Renamed files (R)
  - Untracked files (??)

Tool: mcp_desktop-commander_start_process
Command: "git diff --staged"
Timeout: 5000ms

Get: Staged changes (if any)

Tool: mcp_desktop-commander_start_process
Command: "git diff HEAD"
Timeout: 10000ms

Get: Unstaged changes

Progress: await ctx.report_progress(0, 5, "Detecting changes")
State: ctx.set_state("changes", {
  "modified": [list of modified files],
  "added": [list of added files],
  "deleted": [list of deleted files],
  "staged": [list of staged files],
  "diff": git_diff_output
})

Logging:
  await ctx.info(f"Found {len(modified)} modified, {len(added)} added, {len(deleted)} deleted files")

Error handling:
  If git not initialized:
    await ctx.error("Git repository not initialized")
    return {"status": "error", "message": "Not a git repository"}
  
  If no changes:
    await ctx.warning("No changes detected")
    return {"status": "info", "message": "Working tree clean"}
```

### Stage 2 - Analyze Changes

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Git diff + file list
Thoughts: 8-12
Determine:
  1. What changed (features, bugs, docs, refactor, etc.)
  2. Scope (which module/component)
  3. Breaking changes (yes/no)
  4. Conventional commit type (feat|fix|docs|style|refactor|test|chore)
  5. Impact assessment
  6. Related issues or tickets

Analysis patterns:
  - New files with "test" → test
  - New files with "api", "endpoint" → feat
  - Changes to README, docs → docs
  - Import changes, formatting → style
  - Function renaming, restructuring → refactor
  - Bug fixes, error handling → fix
  - Dependency updates → chore
  - Performance improvements → perf

Progress: await ctx.report_progress(1, 5, "Analyzing changes")
State: ctx.set_state("commit_analysis", {
  "type": "feat",  # Conventional commit type
  "scope": "api",  # Module/component scope
  "breaking": false,  # Breaking change indicator
  "summary": "Add rate limiting middleware",
  "body": "Implements rate limiting for API endpoints...",
  "footer": "Closes #123"
})

Logging:
  await ctx.info(f"Commit type: {type}({scope})")
  if breaking:
    await ctx.warning("Breaking change detected")
```

### Stage 3 - Generate Message

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Commit analysis
Thoughts: 4-6
Generate: Conventional commit message

Format: "{type}({scope}): {description}\n\n{body}\n\n{footer}"

Examples:
  - feat(api): add rate limiting middleware
  - fix(auth): resolve token expiration bug
  - docs(readme): update installation instructions
  - refactor(service): extract validation logic
  - test(unit): add tests for rate calculation
  - chore(deps): update dependencies

Breaking changes format:
  "{type}({scope}): {description}\n\nBREAKING CHANGE: {description}\n\n{body}"

Progress: await ctx.report_progress(2, 5, "Generating commit message")
State: ctx.set_state("commit_message", generated_message)

Logging:
  await ctx.info(f"Generated commit message:\n{commit_message}")

Validation:
  - Type must be valid conventional commit type
  - Description must be imperative mood ("add" not "added")
  - Description must be <= 72 characters
  - Body optional but recommended for complex changes
```

### Stage 4 - Stage Files

```yaml
Tool: mcp_desktop-commander_start_process
Command: "git add -A" or selective staging
  If --selective flag:
    Command: "git add {file1} {file2} ..."
  Else:
    Command: "git add -A"

Timeout: 5000ms

Verify: Files staged correctly
Tool: mcp_desktop-commander_start_process
Command: "git status --porcelain"
Check: All intended files are staged (status starts with A, M, D, R)

Progress: await ctx.report_progress(3, 5, "Staging files")
State: ctx.set_state("staged_files", list_of_staged_files)

Logging:
  await ctx.info(f"Staged {len(staged_files)} files")

Error handling:
  If staging fails:
    await ctx.error("Failed to stage files")
    return {"status": "error", "message": "Staging failed"}
```

### Stage 5 - Commit

```yaml
Tool: mcp_desktop-commander_start_process
Command: 'git commit -m "{generated_message}"'
Timeout: 5000ms

Verify: Commit created
Tool: mcp_desktop-commander_start_process
Command: "git log -1 --pretty=format:%H"
Get: Commit hash

Tool: mcp_desktop-commander_start_process (optional, if --push flag)
Command: "git push"
Timeout: 30000ms

Progress: await ctx.report_progress(4, 5, "Creating commit")
State: ctx.set_state("commit_hash", commit_hash)

Logging:
  await ctx.info(f"Committed: {commit_hash}")
  await ctx.info(f"Message: {commit_message[:50]}...")
  if pushed:
    await ctx.info("Pushed to remote")

Error handling:
  If commit fails:
    await ctx.error("Failed to create commit")
    return {"status": "error", "message": "Commit failed"}
  
  If push fails:
    await ctx.warning("Commit created but push failed")
    return {"status": "partial", "message": "Committed locally, push failed"}

Progress: await ctx.report_progress(5, 5, "Complete")
```

## Support All Frameworks

**Python Projects:**
- Detects from: `requirements.txt`, `pyproject.toml`, `setup.py`
- Scope examples: `api`, `service`, `model`, `test`

**JavaScript Projects:**
- Detects from: `package.json`, `tsconfig.json`
- Scope examples: `component`, `api`, `util`, `test`

**Go Projects:**
- Detects from: `go.mod`, `go.sum`
- Scope examples: `handler`, `service`, `model`, `test`

**Rust Projects:**
- Detects from: `Cargo.toml`, `Cargo.lock`
- Scope examples: `api`, `service`, `model`, `test`

## Usage Examples

```bash
# No arguments - auto-detect and commit all changes
/commit

# Commit with push
/commit --push

# Selective staging
/commit --selective

# Override commit type
/commit --type=fix

# Override scope
/commit --scope=api

# Breaking change
/commit --breaking

# Skip staging (if already staged)
/commit --no-stage
```

## Output Format

### Success Output

```
🔍 Detecting Changes:
Found: 3 modified, 1 added, 0 deleted files
Modified: backend/src/services/easypost_service.py
Modified: backend/src/routers/shipments.py
Modified: backend/tests/unit/test_service.py
Added: backend/src/middleware/rate_limit.py

🧠 Analyzing Changes (Sequential-thinking):
Step 1: New middleware file added
Step 2: Service updated to use middleware
Step 3: Router updated to apply middleware
Step 4: Tests added for middleware
Step 5: This is a new feature
Step 6: Scope is "api" (affects API endpoints)
Step 7: Not a breaking change
Commit type: feat(api)

📝 Generated Commit Message:
feat(api): add rate limiting middleware

Implements rate limiting for API endpoints using token bucket
algorithm. Limits requests to 100 per minute per IP address.

- Add RateLimitMiddleware class
- Integrate middleware into FastAPI app
- Add configuration for rate limits
- Add tests for rate limiting

Closes #123

📦 Staging Files:
Staged 4 files:
  - backend/src/middleware/rate_limit.py (A)
  - backend/src/services/easypost_service.py (M)
  - backend/src/routers/shipments.py (M)
  - backend/tests/unit/test_service.py (M)

✅ Commit Created:
Commit: a1b2c3d4e5f6...
Message: feat(api): add rate limiting middleware

✅ Commit complete!
```

### Breaking Change Output

```
🔍 Detecting Changes:
Found: 5 modified files
Modified: backend/src/models/shipment.py
Modified: backend/src/services/easypost_service.py
...

🧠 Analyzing Changes:
Commit type: feat(api)
Breaking change detected: Response format changed

📝 Generated Commit Message:
feat(api): change shipment response format

BREAKING CHANGE: Shipment response now returns nested address
objects instead of flat structure. Update clients to access
address fields via response.shipment.to_address.street1.

- Update ShipmentResponse model
- Update service to use new format
- Update tests for new format

✅ Commit Created:
Commit: b2c3d4e5f6a7...
Message: feat(api): change shipment response format

⚠️ Breaking change committed
```

## Performance

- Change detection: 1-2s (git status + diff)
- Change analysis: 3-5s (Sequential-thinking with 8-12 thoughts)
- Message generation: 1-2s (Sequential-thinking with 4-6 thoughts)
- Staging: <1s (git add)
- Commit: <1s (git commit)
- Push: 2-5s (if --push flag)
- **Total: 6-15s** for complete commit cycle

## Desktop Commander Tools Used

**Primary Tools:**
- `mcp_desktop-commander_start_process` - Git commands (status, diff, add, commit, push)
- `mcp_sequential-thinking_sequentialthinking` - Change analysis, message generation

**Supporting Tools:**
- `mcp_desktop-commander_read_file` - Read git config if needed

## Error Handling

**Git Not Initialized:**
- Report error: "Not a git repository"
- Suggest: `git init`

**No Changes:**
- Report info: "Working tree clean"
- Exit gracefully

**Staging Failures:**
- Report error with file names
- Suggest manual staging

**Commit Failures:**
- Report error with git output
- Suggest checking git config (user.name, user.email)

**Push Failures:**
- Report warning
- Commit still created locally
- Suggest checking remote configuration

## Conventional Commit Format

**Structure:**
```
<type>(<scope>): <description>

<body>

<footer>
```

**Type Examples:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `perf`: Performance
- `test`: Tests
- `chore`: Maintenance

**Scope Examples:**
- `api`: API changes
- `auth`: Authentication
- `db`: Database
- `ui`: User interface
- `config`: Configuration

**Description Rules:**
- Use imperative mood ("add" not "added")
- Lowercase (except proper nouns)
- No period at end
- <= 72 characters

**Body (optional):**
- Explain what and why
- Wrap at 72 characters
- Can include multiple paragraphs

**Footer (optional):**
- Breaking changes: `BREAKING CHANGE: description`
- Issues: `Closes #123`, `Fixes #456`
- References: `Refs #789`

## Adapts To Any Project

Works automatically with:
- Python projects (detects from requirements.txt, pyproject.toml)
- JavaScript projects (detects from package.json)
- Go projects (detects from go.mod)
- Rust projects (detects from Cargo.toml)
- Any git repository

**One command. Smart commits. Conventional format. Any project.**
