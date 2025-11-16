# Tools Usage Examples - Real Session Examples

**Date**: 2025-01-17
**Purpose**: Practical examples of tool usage from actual review session
**Status**: Real Examples

---

## Tools Used in This Review Session

### 1. Codebase Analysis Tools

#### `codebase_search` - Semantic Understanding

**Used For**: Understanding MCP server architecture

**Example**:

```python
codebase_search(
    query="How is the MCP server initialized and what dependencies does it need?",
    target_directories=["src/mcp_server"]
)
```

**Result**: Found `build_mcp_server()` function, registration patterns, service initialization

**When to Use**:

- Understanding architecture
- Finding related code
- Discovering patterns
- Locating implementations

---

#### `grep` - Exact Pattern Matching

**Used For**: Finding tool registrations, imports, patterns

**Examples from Session**:

```python
# Find all tool decorators
grep(pattern="@mcp\.tool", path="src/mcp_server/tools")

# Find ToolError usage
grep(pattern="ToolError|from fastmcp.exceptions", path="src/mcp_server/tools")

# Find API key references
grep(pattern="EASYPOST_API_KEY|API_KEY|SECRET", path="src", -i=True)
```

**Results**:

- Found 6 tool files with `@mcp.tool`
- Found 3 files using `ToolError`
- Found 12 API key references (all secure)

**When to Use**:

- Exact pattern matching
- Finding function/class names
- Locating imports
- Configuration values

---

### 2. File Operations

#### `read_file` - Reading Files

**Used For**: Reading configuration, source code, documentation

**Examples from Session**:

```python
# Read configuration files
read_file("config/pyproject.toml")
read_file("pytest.ini")
read_file("fastmcp.json")
read_file(".envrc")

# Read source code
read_file("src/mcp_server/__init__.py")
read_file("src/server.py", limit=100)
read_file("src/lifespan.py")

# Read documentation
read_file("README.md")
read_file("CLAUDE.md")
```

**When to Use**:

- Reading any file
- Analyzing code
- Reviewing configs
- Checking documentation

---

#### `search_replace` - Precise Edits

**Used For**: Making targeted changes

**Examples from Session**:

```python
# Remove database dependencies
search_replace(
    file_path="config/requirements.txt",
    old_string="# Database (conservative pinning)\nsqlalchemy>=2.0.0,<3.0.0\nalembic>=1.12.0,<2.0.0\npsycopg2-binary>=2.9.0,<3.0.0",
    new_string="# Note: Database dependencies removed for personal use (YAGNI)"
)

# Fix pytest configuration
search_replace(
    file_path="pytest.ini",
    old_string="addopts = -v --tb=short --strict-markers -n 8",
    new_string="addopts = -v --tb=short --strict-markers -n auto"
)
```

**When to Use**:

- Precise edits
- Configuration updates
- Bug fixes
- Refactoring

---

#### `write` - Creating Files

**Used For**: Creating documentation, reports

**Examples from Session**:

```python
# Create review report
write(
    file_path="universal/PROJECT_SETUP_REVIEW_REPORT.md",
    contents="# Review Report\n\n..."
)

# Create tool integration guide
write(
    file_path="universal/ENHANCED_TOOLS_INTEGRATION.md",
    contents="# Enhanced Tools Integration\n\n..."
)
```

**When to Use**:

- Creating new files
- Writing documentation
- Generating reports

---

### 3. MCP Integration Tools

#### `mcp_context7_resolve-library-id` - Library Discovery

**Used For**: Finding FastMCP library ID

**Example**:

```python
mcp_context7_resolve-library-id(libraryName="FastMCP")
```

**Result**: Found `/jlowin/fastmcp` (High reputation, 1268 code snippets)

**When to Use**:

- Finding library documentation
- Discovering library IDs
- Researching libraries

---

#### `mcp_context7_get-library-docs` - Official Documentation

**Used For**: Getting FastMCP best practices

**Example**:

```python
mcp_context7_get-library-docs(
    context7CompatibleLibraryID="/jlowin/fastmcp",
    topic="server setup, tool registration, best practices",
    tokens=3000
)
```

**Result**: Got comprehensive FastMCP documentation including:

- Tool registration patterns
- Server configuration
- Error handling
- Testing patterns
- Best practices

**When to Use**:

- Getting official framework docs
- Best practices verification
- Code examples
- API reference

---

#### `mcp_exa-search_get_code_context_exa` - Community Examples

**Used For**: Finding real-world FastMCP examples

**Example**:

```python
mcp_exa-search_get_code_context_exa(
    query="FastMCP tool registration patterns and best practices for Python",
    tokensNum=3000
)
```

**Result**: Found multiple real-world examples:

- Tool registration patterns
- Error handling examples
- Testing patterns
- Server setup examples

**When to Use**:

- Finding code examples
- Community best practices
- Real-world patterns
- Implementation examples

---

#### `mcp_exa-search_web_search_exa` - Latest Information

**Used For**: Finding latest FastMCP updates

**Example**:

```python
mcp_exa-search_web_search_exa(
    query="FastMCP 2.0 Python best practices tool registration error handling 2025",
    numResults=5
)
```

**Result**: Found recent articles:

- FastMCP 2.0 Quick Start guides
- Best practices articles
- Tutorial examples
- Community patterns

**When to Use**:

- Latest information
- Framework updates
- Community trends
- Recent best practices

---

### 4. Desktop Commander Tools

#### `mcp_Desktop_Commander_start_search` - Advanced Search

**Used For**: Comprehensive pattern detection

**Example**:

```python
mcp_Desktop_Commander_start_search(
    path="/Users/andrejs/Projects/personal/easypost-mcp-project",
    pattern="@mcp\.tool|def.*register.*tool",
    searchType="content",
    ignoreCase=True,
    maxResults=50
)
```

**Result**: Found 259 results, 28 matches across codebase

**When to Use**:

- Comprehensive searches
- Pattern detection
- Finding all occurrences
- Large codebase analysis

---

#### `mcp_Desktop_Commander_get_more_search_results` - Pagination

**Used For**: Getting more search results

**Example**:

```python
mcp_Desktop_Commander_get_more_search_results(
    sessionId="search_11_1763257860291",
    offset=0,
    length=100
)
```

**Result**: Retrieved 99 results from active search

**When to Use**:

- Paginating large results
- Progressive loading
- Managing search sessions

---

#### `mcp_Desktop_Commander_get_config` - Configuration

**Used For**: Understanding Desktop Commander settings

**Example**:

```python
mcp_Desktop_Commander_get_config()
```

**Result**: Got complete configuration:

- File read limit: 1000 lines
- File write limit: 50 lines
- Blocked commands list
- Usage statistics

**When to Use**:

- Understanding limits
- Checking settings
- Debugging

---

### 5. Process & Terminal Tools

#### `run_terminal_cmd` - Command Execution

**Used For**: Running system commands

**Examples from Session**:

```python
# Find Python files
run_terminal_cmd(
    command="find . -maxdepth 2 -name '*.py' | head -20",
    is_background=False
)

# Get project structure
run_terminal_cmd(
    command="tree -L 3 -I '__pycache__|*.pyc' 2>/dev/null || find . -maxdepth 3 -type d | sort",
    is_background=False
)

# Count files
run_terminal_cmd(
    command="find tests -name '*.py' | wc -l",
    is_background=False
)

# Check Python version
run_terminal_cmd(
    command="python -c 'import sys; print(sys.version)'",
    is_background=False
)
```

**When to Use**:

- System commands
- File operations
- Validation
- Quick checks

---

### 6. Directory & File Discovery

#### `list_dir` - Directory Listing

**Used For**: Exploring project structure

**Example**:

```python
list_dir(
    target_directory="src/mcp_server/tools",
    ignore_globs=["__pycache__", "*.pyc"]
)
```

**Result**: Listed all tool files:

- bulk_tools.py
- tracking_tools.py
- rate_tools.py
- etc.

**When to Use**:

- Exploring structure
- Finding files
- Understanding organization

---

#### `glob_file_search` - File Pattern Matching

**Used For**: Finding files by pattern

**Example**:

```python
glob_file_search(glob_pattern="**/launch.json")
```

**Result**: Found `.vscode/launch.json`

**When to Use**:

- Finding files by extension
- Locating config files
- Pattern-based discovery

---

### 7. Quality Assurance

#### `read_lints` - Linter Checking

**Used For**: Validating code quality

**Example**:

```python
read_lints(paths=["scripts/python/get-bulk-rates.py", "pytest.ini"])
```

**Result**: Found 13 linter errors in get-bulk-rates.py (type checking issues)

**When to Use**:

- After making edits
- Code quality checks
- Validation
- Finding errors

---

## Tool Usage Statistics (This Session)

### Most Used Tools

1. **read_file**: 30+ calls
   - Configuration files
   - Source code
   - Documentation

2. **grep**: 20+ calls
   - Pattern detection
   - Finding imports
   - Locating code

3. **codebase_search**: 10+ calls
   - Architecture understanding
   - Pattern discovery
   - Implementation finding

4. **search_replace**: 15+ calls
   - Configuration fixes
   - Code updates
   - Documentation edits

5. **mcp_Desktop_Commander_start_search**: 5+ calls
   - Comprehensive searches
   - Pattern detection

6. **mcp_context7_get-library-docs**: 2+ calls
   - FastMCP documentation
   - Best practices

7. **mcp_exa-search_get_code_context_exa**: 2+ calls
   - Community examples
   - Code patterns

8. **run_terminal_cmd**: 10+ calls
   - System commands
   - Validation
   - File operations

---

## Tool Combination Patterns

### Pattern 1: Comprehensive Code Review

```python
# Step 1: Understand architecture
codebase_search(query="How does MCP server work?")

# Step 2: Find exact patterns
grep(pattern="@mcp.tool", path="src/mcp_server/tools")

# Step 3: Get best practices
mcp_context7_get-library-docs(...)

# Step 4: Find examples
mcp_exa-search_get_code_context_exa(...)

# Step 5: Read specific files
read_file("src/mcp_server/__init__.py")

# Step 6: Validate
read_lints(paths=["src/mcp_server"])
```

**Result**: Comprehensive understanding with multiple perspectives

---

### Pattern 2: Pattern Detection & Analysis

```python
# Step 1: Semantic search
codebase_search(query="Where is error handling implemented?")

# Step 2: Exact pattern match
grep(pattern="except.*Error|ToolError", path="src")

# Step 3: Advanced search
mcp_Desktop_Commander_start_search(
    pattern="ToolError",
    searchType="content"
)

# Step 4: Read relevant files
read_file("src/mcp_server/tools/tracking_tools.py")
```

**Result**: Found all error handling patterns across codebase

---

### Pattern 3: Best Practices Verification

```python
# Step 1: Official documentation
docs = mcp_context7_get-library-docs(
    context7CompatibleLibraryID="/jlowin/fastmcp",
    topic="tool registration, error handling"
)

# Step 2: Community examples
examples = mcp_exa-search_get_code_context_exa(
    query="FastMCP error handling ToolError patterns"
)

# Step 3: Project code
grep(pattern="ToolError", path="src/mcp_server/tools")

# Step 4: Compare and validate
# Project aligns with best practices ✅
```

**Result**: Verified project follows best practices

---

### Pattern 4: Configuration Review

```python
# Step 1: Read config files
read_file("config/pyproject.toml")
read_file("pytest.ini")
read_file("fastmcp.json")

# Step 2: Check for issues
grep(pattern="sqlalchemy|alembic", path="config")

# Step 3: Validate
read_lints(paths=["config/pyproject.toml"])

# Step 4: Fix issues
search_replace(...)
```

**Result**: Found and fixed configuration issues

---

## Real Session Workflow

### Phase 1: Discovery

1. `list_dir` - Explore project structure
2. `codebase_search` - Understand architecture
3. `grep` - Find patterns
4. `read_file` - Read key files

### Phase 2: Analysis

1. `mcp_context7_get-library-docs` - Get official docs
2. `mcp_exa-search_get_code_context_exa` - Find examples
3. `mcp_exa-search_web_search_exa` - Latest info
4. `mcp_Desktop_Commander_start_search` - Comprehensive search

### Phase 3: Validation

1. `grep` - Verify patterns
2. `read_lints` - Check quality
3. `run_terminal_cmd` - Validate execution
4. Cross-reference findings

### Phase 4: Documentation

1. `write` - Create reports
2. `search_replace` - Update docs
3. `read_file` - Review output

---

## Tool Effectiveness

### Most Effective Combinations

1. **codebase_search + grep**: Understanding + exact matches
2. **Context7 + Exa**: Official + community validation
3. **read_file + grep**: Targeted reading
4. **Desktop Commander + grep**: Comprehensive + precise

### Tools That Complement Each Other

- **codebase_search** (semantic) + **grep** (exact) = Complete picture
- **Context7** (official) + **Exa** (community) = Best practices
- **read_file** (reading) + **grep** (finding) = Efficient analysis
- **run_terminal_cmd** (simple) + **Desktop Commander** (advanced) = Full process control

---

## Lessons Learned

### What Works Well

1. **Combining semantic + exact search**: Gets both understanding and precision
2. **Using MCP tools for external knowledge**: Context7 + Exa provide comprehensive coverage
3. **Desktop Commander for advanced operations**: More powerful than basic tools
4. **Progressive analysis**: Start broad, narrow down, then deep dive

### What to Avoid

1. **Over-relying on one tool**: Use multiple tools for validation
2. **Reading entire large files**: Use grep first to find relevant sections
3. **Ignoring tool limitations**: Understand when to use which tool
4. **Not cross-referencing**: Always validate with multiple sources

---

## Tool Selection Decision Tree

```
Need to understand code?
├─ Yes → codebase_search (semantic understanding)
│         └─ Then → grep (exact patterns)
│                   └─ Then → read_file (specific files)
│
Need to find patterns?
├─ Exact match → grep
├─ Complex pattern → Desktop Commander search
└─ Multiple files → glob_file_search
│
Need documentation?
├─ Official docs → Context7
├─ Code examples → Exa Code Context
└─ Latest info → Exa Web Search
│
Need to edit files?
├─ Simple edit → search_replace
├─ Multiple edits → Desktop Commander edit_block
└─ New file → write
│
Need to execute commands?
├─ Simple command → run_terminal_cmd
└─ Interactive/REPL → Desktop Commander process tools
```

---

## Summary

### Tools Available: 50+

**Categories**:

- Codebase Analysis: 4 tools
- File Operations: 6 tools
- MCP Integration: 10+ tools
- Process Management: 5+ tools
- Documentation: 4 tools
- Quality: 1 tool
- Task Management: 1 tool

### Most Powerful for This Project

1. **codebase_search**: Understanding MCP architecture
2. **grep**: Finding tool patterns
3. **Context7**: FastMCP best practices
4. **Exa**: Community examples
5. **Desktop Commander**: Comprehensive analysis

### Key Insight

**Tool combination is key**: Using multiple tools together provides:

- ✅ Better accuracy (cross-validation)
- ✅ Comprehensive coverage
- ✅ Multiple perspectives
- ✅ Best practices alignment

---

**Last Updated**: 2025-01-17
**Examples**: Real session examples
**Status**: Practical Reference Guide
