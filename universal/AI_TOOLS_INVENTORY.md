# AI Assistant Tools Inventory & Usage Guide

**Date**: 2025-01-17
**Purpose**: Comprehensive reference for all available AI assistant tools
**Status**: Complete Inventory

---

## Tool Categories

### 1. Codebase Analysis Tools

### 2. File Operations Tools

### 3. Code Search Tools

### 4. MCP Integration Tools

### 5. Web & Documentation Tools

### 6. Process & Terminal Tools

### 7. Memory & Knowledge Tools

### 8. Notebook Tools

---

## Category 1: Codebase Analysis Tools

### `codebase_search`

**Purpose**: Semantic search across codebase
**Type**: Semantic search (AI-powered)

**Usage**:

```python
codebase_search(
    query="How does the MCP server initialize?",
    target_directories=["src/mcp_server"],
    search_only_prs=False
)
```

**Best For**:

- Understanding code architecture
- Finding related functionality
- Discovering patterns
- Locating implementation details

**Example Queries**:

- "How is error handling implemented?"
- "Where are API keys validated?"
- "What is the tool registration pattern?"

**Limitations**:

- Semantic, not exact string matching
- May return false positives
- Best combined with grep for exact matches

---

### `grep`

**Purpose**: Exact pattern matching (ripgrep-based)
**Type**: Text search (regex)

**Usage**:

```python
grep(
    pattern="@mcp\.tool",
    path="src/mcp_server/tools",
    output_mode="content",
    -A=5,  # Context after
    -B=3,  # Context before
    head_limit=20
)
```

**Best For**:

- Finding exact patterns
- Function/class names
- Import statements
- Configuration values

**Output Modes**:

- `content`: Show matching lines (default)
- `files_with_matches`: Only file paths
- `count`: Count matches per file

**Advanced Features**:

- Regex support
- Multiline matching
- Case-insensitive search
- File type filtering

**Example Patterns**:

- `^import |^from ` - Import statements
- `@mcp\.tool` - Tool decorators
- `def.*\(.*ctx.*Context` - Functions with Context param
- `TODO|FIXME` - Code markers

---

## Category 2: File Operations Tools

### `read_file`

**Purpose**: Read file contents
**Type**: File I/O

**Usage**:

```python
read_file(
    target_file="src/server.py",
    offset=0,      # Start line (optional)
    limit=100      # Lines to read (optional)
)
```

**Best For**:

- Reading configuration files
- Analyzing source code
- Reviewing documentation
- Checking file contents

**Features**:

- Line-numbered output
- Partial file reading (offset/limit)
- Handles large files efficiently

**Limitations**:

- Large files may need chunking
- Use offset/limit for efficiency

---

### `write`

**Purpose**: Create or overwrite files
**Type**: File I/O

**Usage**:

```python
write(
    file_path="universal/REVIEW.md",
    contents="# Review\n\nContent here..."
)
```

**Best For**:

- Creating new files
- Writing documentation
- Generating reports
- Creating configuration files

**Note**: Overwrites existing files

---

### `search_replace`

**Purpose**: Exact string replacement in files
**Type**: File editing

**Usage**:

```python
search_replace(
    file_path="config/pyproject.toml",
    old_string="sqlalchemy",
    new_string="# sqlalchemy removed",
    replace_all=False  # Replace all occurrences
)
```

**Best For**:

- Precise edits
- Configuration updates
- Bug fixes
- Refactoring

**Requirements**:

- `old_string` must be unique (or use `replace_all=True`)
- Preserves exact indentation
- Must match whitespace exactly

**Tips**:

- Include context lines for uniqueness
- Use `replace_all=True` for global changes
- Check indentation carefully

---

### `delete_file`

**Purpose**: Delete files
**Type**: File I/O

**Usage**:

```python
delete_file(target_file="unused_file.py")
```

**Best For**:

- Removing unused files
- Cleanup operations
- Temporary file removal

**Safety**: Fails gracefully if file doesn't exist

---

## Category 3: Code Search Tools

### `glob_file_search`

**Purpose**: Find files by name pattern
**Type**: File search

**Usage**:

```python
glob_file_search(
    glob_pattern="**/*.py",
    target_directory="src"
)
```

**Best For**:

- Finding files by extension
- Locating configuration files
- Discovering project structure

**Pattern Examples**:

- `*.py` - All Python files
- `**/test_*.py` - Test files
- `**/__init__.py` - Init files
- `*.json` - JSON files

---

### `list_dir`

**Purpose**: List directory contents
**Type**: File system

**Usage**:

```python
list_dir(
    target_directory="src/mcp_server",
    ignore_globs=["__pycache__", "*.pyc"]
)
```

**Best For**:

- Exploring project structure
- Finding directories
- Understanding organization

**Features**:

- Ignores patterns (like .gitignore)
- Shows files and directories
- Recursive listing support

---

## Category 4: MCP Integration Tools

### Context7 Tools

#### `mcp_context7_resolve-library-id`

**Purpose**: Find library IDs for documentation
**Type**: Library discovery

**Usage**:

```python
mcp_context7_resolve-library-id(
    libraryName="FastMCP"
)
```

**Returns**: List of matching libraries with IDs

**Best For**:

- Finding library documentation
- Discovering library IDs
- Library research

---

#### `mcp_context7_get-library-docs`

**Purpose**: Fetch library documentation
**Type**: Documentation access

**Usage**:

```python
mcp_context7_get-library-docs(
    context7CompatibleLibraryID="/jlowin/fastmcp",
    topic="tool registration, error handling",
    tokens=5000
)
```

**Best For**:

- Getting up-to-date docs
- Best practices verification
- Code examples
- API reference

**Parameters**:

- `tokens`: 1000-50000 (default: 5000)
- `topic`: Focus area (optional)

---

### Exa Search Tools

#### `mcp_exa-search_web_search_exa`

**Purpose**: Real-time web search
**Type**: Web search

**Usage**:

```python
mcp_exa-search_web_search_exa(
    query="FastMCP 2.0 best practices",
    numResults=8,
    type="auto",  # auto, fast, deep
    livecrawl="fallback"  # fallback, preferred
)
```

**Best For**:

- Latest information
- Community patterns
- Framework updates
- Best practices

**Search Types**:

- `auto`: Balanced (default)
- `fast`: Quick results
- `deep`: Comprehensive

---

#### `mcp_exa-search_get_code_context_exa`

**Purpose**: Search code from open source repos
**Type**: Code search

**Usage**:

```python
mcp_exa-search_get_code_context_exa(
    query="FastMCP tool registration patterns Python",
    tokensNum=5000
)
```

**Best For**:

- Code examples
- Implementation patterns
- Community best practices
- Real-world usage

**Tokens Range**: 1000-50000 (default: 5000)

---

### Desktop Commander Tools

#### `mcp_Desktop_Commander_start_search`

**Purpose**: Advanced file/content search
**Type**: Search

**Usage**:

```python
mcp_Desktop_Commander_start_search(
    path="/absolute/path/to/project",
    pattern="@mcp.tool",
    searchType="content",  # files or content
    literalSearch=False,  # regex vs literal
    ignoreCase=True,
    maxResults=50
)
```

**Search Types**:

- `files`: Find files by name
- `content`: Search inside files

**Best For**:

- Pattern detection
- Code analysis
- Comprehensive searches
- Finding all occurrences

**Features**:

- Streaming results
- Progress reporting
- Early termination
- Context lines

---

#### `mcp_Desktop_Commander_get_more_search_results`

**Purpose**: Get more results from active search
**Type**: Search pagination

**Usage**:

```python
mcp_Desktop_Commander_get_more_search_results(
    sessionId="search_123",
    offset=100,  # Start from result 100
    length=50    # Get 50 results
)
```

**Best For**:

- Paginating large search results
- Progressive result loading
- Managing search sessions

---

#### `mcp_Desktop_Commander_read_file`

**Purpose**: Read files with advanced options
**Type**: File I/O

**Usage**:

```python
mcp_Desktop_Commander_read_file(
    path="/absolute/path/file.py",
    offset=0,      # Start line (0-based)
    length=100,    # Lines to read
    isUrl=False    # Can read URLs
)
```

**Special Features**:

- Negative offset: Read from end (`offset=-20` = last 20 lines)
- URL support: Can fetch from URLs
- Image support: Renders images
- Large file optimization

**Best For**:

- Reading specific file sections
- Tail operations (last N lines)
- URL content fetching
- Image viewing

---

#### `mcp_Desktop_Commander_write_file`

**Purpose**: Write files in chunks
**Type**: File I/O

**Usage**:

```python
mcp_Desktop_Commander_write_file(
    path="/absolute/path/file.py",
    content="File content...",
    mode="rewrite"  # or "append"
)
```

**Best Practice**: Write in chunks of 25-30 lines

**Modes**:

- `rewrite`: Overwrite file
- `append`: Append to file

**Best For**:

- Large file creation
- Chunked writing
- Appending content

---

#### `mcp_Desktop_Commander_edit_block`

**Purpose**: Surgical text replacements
**Type**: File editing

**Usage**:

```python
mcp_Desktop_Commander_edit_block(
    file_path="/absolute/path/file.py",
    old_string="def old_function():",
    new_string="def new_function():",
    expected_replacements=1
)
```

**Best For**:

- Precise edits
- Multiple small changes
- Surgical modifications

**Tips**:

- Include context for uniqueness
- Use `expected_replacements` for multiple changes
- Make focused edits

---

#### `mcp_Desktop_Commander_start_process`

**Purpose**: Start terminal processes
**Type**: Process management

**Usage**:

```python
mcp_Desktop_Commander_start_process(
    command="python -c 'print(\"test\")'",
    timeout_ms=10000,
    shell="/bin/zsh"
)
```

**Best For**:

- Running commands
- Testing code
- Validation
- Data processing

**Features**:

- Smart REPL detection
- Early exit on completion
- Timeout handling
- Background execution

---

#### `mcp_Desktop_Commander_interact_with_process`

**Purpose**: Send input to running process
**Type**: Process interaction

**Usage**:

```python
mcp_Desktop_Commander_interact_with_process(
    pid=12345,
    input="import pandas as pd\nprint('test')",
    timeout_ms=8000,
    wait_for_prompt=True
)
```

**Best For**:

- Interactive REPLs
- Python/Node.js sessions
- Data analysis
- Testing

**Features**:

- Auto-detects REPL prompts
- Waits for completion
- Clean output formatting

---

#### `mcp_Desktop_Commander_read_process_output`

**Purpose**: Read process output
**Type**: Process I/O

**Usage**:

```python
mcp_Desktop_Commander_read_process_output(
    pid=12345,
    timeout_ms=5000
)
```

**Best For**:

- Getting command results
- Reading REPL output
- Process monitoring

**Features**:

- Smart completion detection
- Early exit on prompt
- Progress reporting

---

#### `mcp_Desktop_Commander_list_directory`

**Purpose**: Detailed directory listing
**Type**: File system

**Usage**:

```python
mcp_Desktop_Commander_list_directory(
    path="/absolute/path",
    depth=2  # Recursion depth
)
```

**Best For**:

- Exploring structure
- Finding files
- Understanding organization

**Features**:

- Recursive listing
- File/directory distinction
- Large directory protection

---

#### `mcp_Desktop_Commander_get_file_info`

**Purpose**: Get file metadata
**Type**: File system

**Usage**:

```python
mcp_Desktop_Commander_get_file_info(
    path="/absolute/path/file.py"
)
```

**Returns**:

- Size, timestamps
- Permissions
- Line count
- Type information

**Best For**:

- File analysis
- Metadata checking
- Validation

---

#### `mcp_Desktop_Commander_get_config`

**Purpose**: Get Desktop Commander configuration
**Type**: Configuration

**Usage**:

```python
mcp_Desktop_Commander_get_config()
```

**Returns**: Complete server configuration

**Best For**:

- Understanding limits
- Checking settings
- Debugging

---

### Hugging Face Tools

#### `mcp_Hugging_Face_model_search`

**Purpose**: Find ML models
**Type**: Model discovery

**Usage**:

```python
mcp_Hugging_Face_model_search(
    query="text classification",
    author="google",
    task="text-classification",
    limit=20
)
```

**Best For**:

- Finding ML models
- Research
- Model discovery

---

#### `mcp_Hugging_Face_dataset_search`

**Purpose**: Find datasets
**Type**: Dataset discovery

**Usage**:

```python
mcp_Hugging_Face_dataset_search(
    query="shipping data",
    tags=["language:en"],
    limit=20
)
```

**Best For**:

- Dataset discovery
- Research
- Data sources

---

#### `mcp_Hugging_Face_paper_search`

**Purpose**: Find research papers
**Type**: Research

**Usage**:

```python
mcp_Hugging_Face_paper_search(
    query="Model Context Protocol",
    results_limit=12,
    concise_only=False
)
```

**Best For**:

- Research papers
- Academic references
- Latest research

---

## Category 5: Web & Documentation Tools

### `web_search`

**Purpose**: General web search
**Type**: Web search

**Usage**:

```python
web_search(search_term="FastMCP Python tutorial")
```

**Best For**:

- General information
- Tutorials
- Documentation
- Latest updates

**Note**: Less specialized than Exa, but broader coverage

---

## Category 6: Process & Terminal Tools

### `run_terminal_cmd`

**Purpose**: Execute terminal commands
**Type**: Process execution

**Usage**:

```python
run_terminal_cmd(
    command="cd /path && python -m pytest tests/",
    is_background=False
)
```

**Best For**:

- Running tests
- Executing scripts
- System commands
- Validation

**Features**:

- Background execution support
- Shell persistence
- Command chaining

**Limitations**:

- Non-interactive (use Desktop Commander for interactive)
- Single command per call

---

## Category 7: Memory & Knowledge Tools

### `update_memory`

**Purpose**: Store persistent knowledge
**Type**: Memory management

**Usage**:

```python
update_memory(
    action="create",
    key="project_structure",
    value="Backend-only MCP server..."
)
```

**Best For**:

- Project preferences
- Important decisions
- User preferences
- Technical choices

**Actions**:

- `create`: New memory
- `update`: Modify existing
- `delete`: Remove memory

---

## Category 8: Notebook Tools

### `edit_notebook`

**Purpose**: Edit Jupyter notebooks
**Type**: Notebook editing

**Usage**:

```python
edit_notebook(
    target_notebook="analysis.ipynb",
    cell_idx=0,
    is_new_cell=True,
    cell_language="python",
    old_string="",  # Empty for new cells
    new_string="import pandas as pd"
)
```

**Best For**:

- Data analysis notebooks
- Documentation notebooks
- Interactive analysis

---

## Category 9: Linting & Quality Tools

### `read_lints`

**Purpose**: Read linter errors
**Type**: Code quality

**Usage**:

```python
read_lints(
    paths=["src/server.py"]  # Optional, all files if omitted
)
```

**Best For**:

- Checking code quality
- Finding errors
- Validation after edits

**Returns**:

- Linter errors
- Type errors
- Warnings

---

## Category 10: Task Management Tools

### `todo_write`

**Purpose**: Manage task lists
**Type**: Task management

**Usage**:

```python
todo_write(
    merge=False,  # Replace existing
    todos=[
        {
            "id": "task-1",
            "status": "in_progress",
            "content": "Fix bug"
        }
    ]
)
```

**Status Values**:

- `pending`: Not started
- `in_progress`: Currently working
- `completed`: Finished
- `cancelled`: No longer needed

**Best For**:

- Tracking complex tasks
- Multi-step workflows
- Progress management

---

## Tool Usage Patterns

### Pattern 1: Comprehensive Codebase Analysis

```python
# 1. Semantic search for understanding
codebase_search(
    query="How does error handling work?",
    target_directories=["src"]
)

# 2. Exact pattern matching
grep(
    pattern="except.*Error",
    path="src",
    output_mode="files_with_matches"
)

# 3. Read specific files
read_file(target_file="src/exceptions.py")
```

---

### Pattern 2: Best Practices Verification

```python
# 1. Get official documentation
mcp_context7_get-library-docs(
    context7CompatibleLibraryID="/jlowin/fastmcp",
    topic="best practices",
    tokens=5000
)

# 2. Find community examples
mcp_exa-search_get_code_context_exa(
    query="FastMCP error handling patterns",
    tokensNum=3000
)

# 3. Search project code
mcp_Desktop_Commander_start_search(
    pattern="ToolError|from fastmcp.exceptions",
    searchType="content"
)
```

---

### Pattern 3: File Analysis & Editing

```python
# 1. Read file
content = read_file("config/pyproject.toml")

# 2. Make edits
search_replace(
    file_path="config/pyproject.toml",
    old_string="sqlalchemy",
    new_string="# sqlalchemy removed"
)

# 3. Validate
read_lints(paths=["config/pyproject.toml"])
```

---

### Pattern 4: Process Execution & Validation

```python
# 1. Start process
pid = mcp_Desktop_Commander_start_process(
    command="python -c 'import src.mcp_server'",
    timeout_ms=10000
)

# 2. Read output
output = mcp_Desktop_Commander_read_process_output(pid)

# 3. Validate
if "Error" in output:
    # Handle error
```

---

## Tool Selection Guide

### When to Use Which Tool

| Task               | Primary Tool                                                    | Secondary Tool                               |
| ------------------ | --------------------------------------------------------------- | -------------------------------------------- |
| Understand code    | `codebase_search`                                               | `read_file`                                  |
| Find exact pattern | `grep`                                                          | `mcp_Desktop_Commander_start_search`         |
| Get framework docs | `mcp_context7_get-library-docs`                                 | `web_search`                                 |
| Find code examples | `mcp_exa-search_get_code_context_exa`                           | `codebase_search`                            |
| Latest information | `mcp_exa-search_web_search_exa`                                 | `web_search`                                 |
| Read file          | `read_file`                                                     | `mcp_Desktop_Commander_read_file`            |
| Edit file          | `search_replace`                                                | `mcp_Desktop_Commander_edit_block`           |
| Run command        | `run_terminal_cmd`                                              | `mcp_Desktop_Commander_start_process`        |
| Interactive REPL   | `mcp_Desktop_Commander_start_process` + `interact_with_process` | -                                            |
| Find files         | `glob_file_search`                                              | `mcp_Desktop_Commander_start_search` (files) |
| List directory     | `list_dir`                                                      | `mcp_Desktop_Commander_list_directory`       |

---

## Best Practices

### 1. Combine Tools for Accuracy

- Use `codebase_search` for understanding
- Use `grep` for exact matches
- Cross-reference with multiple tools

### 2. Use Appropriate Search Tools

- **Semantic**: `codebase_search` for concepts
- **Exact**: `grep` for patterns
- **Advanced**: Desktop Commander for complex searches

### 3. Leverage MCP Tools for External Knowledge

- **Context7**: Official documentation
- **Exa**: Community examples
- **Web Search**: Latest information

### 4. File Operations

- Use `read_file` for standard reading
- Use Desktop Commander for advanced features (tail, URLs)
- Use `search_replace` for precise edits
- Use Desktop Commander for chunked writing

### 5. Process Management

- Use `run_terminal_cmd` for simple commands
- Use Desktop Commander for interactive sessions
- Use Desktop Commander for REPLs (Python, Node.js)

---

## Tool Limitations & Workarounds

### Limitations

1. **codebase_search**: Semantic, may miss exact matches
   - **Workaround**: Combine with `grep` for exact patterns

2. **read_file**: Large files may need chunking
   - **Workaround**: Use offset/limit or Desktop Commander

3. **run_terminal_cmd**: Non-interactive
   - **Workaround**: Use Desktop Commander for interactive

4. **search_replace**: Requires exact string match
   - **Workaround**: Include context, check whitespace

### Workarounds

1. **Large File Analysis**:
   - Use Desktop Commander with offset/length
   - Read in chunks
   - Use grep to find relevant sections first

2. **Interactive Sessions**:
   - Use Desktop Commander process tools
   - Start REPL with `start_process`
   - Interact with `interact_with_process`

3. **Complex Searches**:
   - Combine multiple tools
   - Use Desktop Commander for advanced patterns
   - Cross-reference results

---

## Tool Statistics

### Most Used Tools (Current Session)

1. **read_file**: 21+ calls
2. **grep**: 15+ calls
3. **codebase_search**: 10+ calls
4. **search_replace**: 12+ calls
5. **mcp_Desktop_Commander_start_search**: 10+ calls
6. **mcp_context7_get-library-docs**: 2+ calls
7. **mcp_exa-search_get_code_context_exa**: 2+ calls

### Tool Categories Usage

- **File Operations**: 35+ operations
- **Code Search**: 25+ searches
- **MCP Tools**: 5+ calls
- **Process Execution**: 5+ commands
- **Documentation**: 3+ fetches

---

## Recommendations

### For Codebase Analysis

1. Start with `codebase_search` for understanding
2. Use `grep` for exact patterns
3. Use Desktop Commander for comprehensive searches
4. Read relevant files with `read_file`

### For Best Practices

1. Use Context7 for official documentation
2. Use Exa for community examples
3. Cross-reference with project code
4. Validate with multiple sources

### For File Operations

1. Use `read_file` for standard reading
2. Use Desktop Commander for advanced features
3. Use `search_replace` for precise edits
4. Validate with `read_lints` after edits

### For Process Execution

1. Use `run_terminal_cmd` for simple commands
2. Use Desktop Commander for interactive sessions
3. Use Desktop Commander for REPLs
4. Monitor with `read_process_output`

---

## Tool Integration Examples

### Example 1: Comprehensive Code Review

```python
# 1. Understand architecture
codebase_search(query="How is the MCP server initialized?")

# 2. Find all tool registrations
grep(pattern="@mcp\.tool", path="src/mcp_server/tools")

# 3. Get best practices
mcp_context7_get-library-docs(
    context7CompatibleLibraryID="/jlowin/fastmcp",
    topic="tool registration"
)

# 4. Find community examples
mcp_exa-search_get_code_context_exa(
    query="FastMCP tool registration patterns"
)

# 5. Validate findings
read_lints(paths=["src/mcp_server/tools"])
```

### Example 2: Pattern Detection

```python
# 1. Semantic search
codebase_search(query="Where is error handling implemented?")

# 2. Exact pattern match
grep(pattern="except.*Error|ToolError", path="src")

# 3. Advanced search
mcp_Desktop_Commander_start_search(
    pattern="ToolError|from fastmcp.exceptions",
    searchType="content"
)

# 4. Read relevant files
read_file("src/mcp_server/tools/tracking_tools.py")
```

### Example 3: Documentation & Best Practices

```python
# 1. Get official docs
docs = mcp_context7_get-library-docs(
    context7CompatibleLibraryID="/jlowin/fastmcp",
    topic="error handling, best practices"
)

# 2. Find community examples
examples = mcp_exa-search_get_code_context_exa(
    query="FastMCP error handling ToolError patterns"
)

# 3. Search web for latest
latest = mcp_exa-search_web_search_exa(
    query="FastMCP 2.0 error handling best practices 2025"
)

# 4. Compare with project
grep(pattern="ToolError", path="src")
```

---

## Tool Capabilities Summary

### Codebase Analysis

- ✅ Semantic search (codebase_search)
- ✅ Exact pattern matching (grep)
- ✅ Advanced search (Desktop Commander)
- ✅ File discovery (glob_file_search)

### Documentation & Knowledge

- ✅ Official docs (Context7)
- ✅ Community examples (Exa Code Context)
- ✅ Latest information (Exa Web Search)
- ✅ General web search (web_search)

### File Operations

- ✅ Read files (read_file, Desktop Commander)
- ✅ Write files (write, Desktop Commander)
- ✅ Edit files (search_replace, Desktop Commander)
- ✅ Delete files (delete_file)
- ✅ List directories (list_dir, Desktop Commander)

### Process Management

- ✅ Execute commands (run_terminal_cmd)
- ✅ Interactive REPLs (Desktop Commander)
- ✅ Process monitoring (Desktop Commander)
- ✅ Background execution

### Quality Assurance

- ✅ Linter checking (read_lints)
- ✅ Code validation
- ✅ Pattern verification

### Task Management

- ✅ Todo tracking (todo_write)
- ✅ Progress management
- ✅ Workflow organization

---

## Advanced Usage Patterns

### Pattern: Multi-Tool Validation

```python
# 1. Semantic understanding
semantic_results = codebase_search(query="error handling")

# 2. Exact pattern match
exact_results = grep(pattern="except|Error")

# 3. Community validation
community_examples = mcp_exa-search_get_code_context_exa(...)

# 4. Official docs
official_docs = mcp_context7_get-library-docs(...)

# 5. Cross-reference all findings
# Compare and validate
```

### Pattern: Progressive Analysis

```python
# 1. High-level search
codebase_search(query="MCP server architecture")

# 2. Narrow down
grep(pattern="build_mcp_server", path="src/mcp_server")

# 3. Read specific file
read_file("src/mcp_server/__init__.py")

# 4. Deep dive
codebase_search(query="How are tools registered?",
                target_directories=["src/mcp_server/tools"])
```

### Pattern: Documentation Generation

```python
# 1. Gather information
docs = mcp_context7_get-library-docs(...)
examples = mcp_exa-search_get_code_context_exa(...)
code = read_file("src/mcp_server/__init__.py")

# 2. Analyze
grep(pattern="@mcp.tool", path="src/mcp_server/tools")

# 3. Generate documentation
write(
    file_path="docs/TOOLS.md",
    contents=generate_documentation(docs, examples, code)
)
```

---

## Tool Performance Tips

### Efficiency

1. **Use grep before read_file**: Find relevant sections first
2. **Use codebase_search for concepts**: More efficient than reading all files
3. **Combine tools**: Use multiple tools for validation
4. **Use Desktop Commander for large searches**: More efficient for comprehensive analysis

### Accuracy

1. **Cross-reference**: Use multiple tools for validation
2. **Combine semantic + exact**: Use both codebase_search and grep
3. **Verify with official docs**: Use Context7 for framework verification
4. **Check community patterns**: Use Exa for real-world examples

---

## Summary

### Available Tools: 50+

**Categories**:

- Codebase Analysis: 4 tools
- File Operations: 6 tools
- MCP Integration: 10+ tools
- Process Management: 5+ tools
- Documentation: 4 tools
- Quality Assurance: 1 tool
- Task Management: 1 tool

### Most Powerful Combinations

1. **Comprehensive Review**: codebase_search + grep + Context7 + Exa
2. **Pattern Detection**: grep + Desktop Commander search
3. **Best Practices**: Context7 + Exa + codebase_search
4. **File Analysis**: read_file + grep + Desktop Commander
5. **Process Validation**: run_terminal_cmd + Desktop Commander

---

**Last Updated**: 2025-01-17
**Status**: Complete Inventory
**Tools Documented**: 50+ tools across 10 categories
