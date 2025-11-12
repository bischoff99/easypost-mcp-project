Clean up project by removing unnecessary files, build artifacts, temporary files, dead code, unused dependencies, and cleaning project structure with comprehensive code analysis.

**Context-aware**: No arguments needed - automatically scans for cleanup targets. Works seamlessly with `/simplify` to remove files identified as overbloat. Provides comprehensive cleanup including code quality improvements, dependency cleanup, and configuration optimization with safety checks.

## How It Works

**Complete MCP Workflow (13 Stages):**

**Stage 1 - Scan for Cleanup Targets**:
- Identifies temporary files (`.tmp`, `.log`, `.cache`, `.swp`, `.bak`)
- Finds build artifacts (`dist/`, `build/`, `*.pyc`, `__pycache__/`, `.next/`, `target/`)
- Detects unused files (orphaned files, dead code files)
- Scans for duplicate files
- Identifies large files that might be unnecessary
- Scans configuration files for unused settings
- Reads `/simplify` recommendations if available
- Scans Git repository for cleanup opportunities

**Stage 1.5 - Deep Code Analysis**:
- AST parsing for unused imports (Python/JS/TS)
- Dead code detection (unreachable code analysis)
- Function/class usage analysis
- Import dependency graph building
- Code duplication detection
- Complexity metrics calculation

**Stage 1.6 - Script Redundancy Analysis**:
- Parses Makefile to extract all targets and commands
- Compares scripts with Makefile targets
- Identifies scripts that duplicate Makefile functionality
- Checks script usage frequency (git history, references)
- Flags scripts that are never referenced

**Stage 1.7 - Root-Level Organization Analysis**:
- Identifies files at root level that should be in `docs/`
- Checks if root-level markdown files are referenced
- Identifies root-level config files that could be organized
- Flags files that belong in subdirectories

**Stage 1.8 - Large File Analysis**:
- Scans for files >1MB that aren't build artifacts
- Identifies test data files (images, PDFs, large JSON)
- Checks if large files are in `.gitignore`
- Flags large files that could be moved to external storage or removed

**Stage 2 - Analyze File Dependencies**:
- Checks if files are imported/referenced
- Verifies files aren't in `.gitignore` (should be ignored, not deleted)
- Identifies safe-to-delete files
- Groups files by cleanup category
- Builds import dependency graph

**Stage 2.5 - Dependency Analysis**:
- Parses package files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`)
- Maps imports to packages (which packages are actually used)
- Checks for outdated dependencies
- Identifies unused packages (not imported anywhere)
- Detects duplicate dependencies
- Analyzes dev dependency usage

**Stage 3 - Get Cleanup Patterns**:
- Loads best practices via Context7
- Gets cleanup patterns for project type
- Caches patterns for reuse

**Stage 4 - Classify Cleanup Targets**:
- Categorizes (temporary, build artifacts, unused, duplicate, documentation, code quality, dependencies, configuration, tests, git, script redundancy, root organization, large files, README consolidation)
- Calculates impact scores (1-10) for each cleanup action
- Prioritizes by safety, impact, and effort
- Groups related files
- Determines safe deletion order
- Identifies code improvement opportunities

**Stage 5 - Generate Cleanup Plan**:
- Creates prioritized cleanup plan
- Estimates space savings
- Suggests safe deletion order
- Includes structure optimization

**Stage 6 - Backup Critical Files**:
- Backs up files before deletion
- Stores metadata for rollback
- Creates cleanup log

**Stage 7 - Apply Cleanup** (Optional):
- Deletes temporary files safely
- Removes build artifacts
- Deletes unused files
- Removes duplicates (keeps one)
- Cleans empty directories
- Removes unused imports (code quality cleanup)
- Removes dead code (unreachable code)
- Removes unused dependencies
- Cleans configuration files
- Applies code refactoring cleanup (extract duplicates, simplify complexity)
- Removes redundant scripts
- Moves root-level files to appropriate directories
- Removes or gitignores large test data files
- Consolidates README files
- Optimizes project structure (Stage 7.5)

**Stage 7.5 - Structure Optimization**:
- Consolidates empty directories
- Moves files to correct directories
- Standardizes naming conventions
- Removes orphaned directories
- Organizes files by type/function

**Stage 8 - Verify**:
- Checks for broken imports/references
- Verifies dependency integrity (no missing packages)
- Verifies code quality (no syntax errors)
- Runs tests to ensure project still works
- Reports cleanup results with impact metrics

## Cleanup Categories

**Temporary Files:**
- `.tmp`, `.temp`, `.swp`, `.bak`, `.backup`
- `*.log` (except important logs)
- `.cache/`, `.vscode/`, `.idea/`
- OS files (`.DS_Store`, `Thumbs.db`)

**Build Artifacts:**
- `dist/`, `build/`, `.next/`, `target/`
- `*.pyc`, `__pycache__/`, `.pyo`
- `node_modules/.cache/`
- Coverage reports (`htmlcov/`, `coverage/`)

**Unused Files:**
- Orphaned files (not imported/referenced)
- Dead code files
- Old migration files (if safe)
- Unused test fixtures

**Duplicate Files (Enhanced):**
- Identical files in different locations
- Backup copies (`.bak`, `.old`)
- Version duplicates
- Content-based duplicates (similar files with minor differences)
- Duplicate data files (test fixtures, sample data)
- Files with same content but different names

**Documentation Bloat (Enhanced):**
- Temporary fix summaries
- Redundant documentation
- Old changelogs
- Duplicate content across markdown files
- Outdated documentation (check modification dates vs project state)
- Documentation referencing non-existent files/code
- Review files covering similar topics (consolidate)
- Multiple cleanup summaries (consolidate into archive)

**Code Quality Cleanup:**
- Unused imports (detected via AST analysis)
- Dead code within files (unreachable code, unused functions/classes)
- Commented-out code blocks
- TODO/FIXME comments without context (optional)
- Formatting inconsistencies
- Code duplication patterns

**Dependency Cleanup:**
- Unused packages (not imported anywhere)
- Outdated dependencies (check for updates)
- Duplicate dependencies (same package in multiple places)
- Unused dev dependencies
- Unused transitive dependencies

**Configuration Cleanup:**
- Unused config files
- Redundant configuration settings
- Environment-specific configs not in use
- Duplicate config entries
- Unused environment variables

**Test Cleanup:**
- Dead test code (tests that never run)
- Unused test fixtures
- Duplicate test cases
- Orphaned test files
- Unused test utilities

**Git Cleanup:**
- Unused branches (merged, stale)
- Large files in history (optional)
- Unused remotes
- Stale tags

**Script Redundancy:**
- Scripts that duplicate Makefile targets
- Unused scripts (never referenced)
- Scripts with no git history
- Scripts that can be replaced by Makefile

**Root Organization:**
- Root-level documentation files that should be in `docs/`
- Root-level analysis/review files
- Root-level config files that could be organized
- Temporary files at root level

**Large Files:**
- Test data files (images >500KB, PDFs >1MB)
- Large JSON fixtures (>100KB)
- Database dumps (>5MB)
- Large log files (>10MB)
- Build artifacts not in .gitignore

**README Consolidation:**
- Redundant README files with duplicate content
- Outdated README files
- README files that can be consolidated
- Missing README files in important directories

## MCP Integration

### Stage 1 - Scan for Cleanup Targets

```yaml
Tool: mcp_desktop-commander_list_directory
Path: Project root (recursive, depth=3)
Find:
  - Temporary files: *.tmp, *.log, *.swp, *.bak
  - Build artifacts: dist/, build/, __pycache__/, .next/
  - OS files: .DS_Store, Thumbs.db
  - Cache: .cache/, node_modules/.cache/

Tool: mcp_desktop-commander_start_search
Pattern: Check for simplify recommendations
SearchType: "file"
Find: .simplify-recommendations.json or simplify output

Tool: mcp_desktop-commander_get_file_info
Path: Each potential cleanup target
Get: File size, modification date, permissions

Progress: await ctx.report_progress(0, 10, "Scanning for cleanup targets")
State: ctx.set_state("cleanup_targets", {
  "temporary": [...],
  "build_artifacts": [...],
  "unused": [...],
  "duplicates": [],
  "large": [],
  "code_quality": [],
  "dependencies": [],
  "configuration": [],
  "tests": [],
  "git": []
})

### Stage 1.5 - Deep Code Analysis

```yaml
Tool: mcp_desktop-commander_start_process
Command: AST parsing for code analysis
  Python: "python -c 'import ast; ...'" (parse AST)
  JavaScript: "node -e 'require(\"@babel/parser\").parse(...)'" or "npx eslint --format json"
  TypeScript: "npx tsc --noEmit --listFiles" (get all imports)

Parallel: True (analyze multiple files simultaneously)

For each code file:
  Tool: mcp_desktop-commander_read_file
  Path: Code file (absolute path)
  Read: File content

  # AST Analysis
  Tool: mcp_desktop-commander_start_process
  Command: Parse AST and detect unused imports
    Python: Use `ast` module to parse, detect unused imports
    JS/TS: Use ESLint or Babel parser to detect unused imports
  Timeout: 30000ms

  # Dead Code Detection
  Tool: mcp_sequential-thinking_sequentialthinking
  Input: AST + file content
  Thoughts: 8-10
  Analyze:
    1. Which functions/classes are defined?
    2. Which functions/classes are called/imported?
    3. Which imports are used?
    4. What code is unreachable?
    5. What code is duplicated?

  # Import Dependency Graph
  Tool: mcp_desktop-commander_start_search
  Pattern: Import statements
  SearchType: "content"
  Find: All imports in file

  Build dependency graph:
    - Map imports to files
    - Identify circular dependencies
    - Find orphaned imports

Progress: await ctx.report_progress(1, 10, "Deep code analysis")
State: ctx.set_state("code_analysis", {
  "unused_imports": [
    {
      "file": "src/services/user.py",
      "import": "from models.old import OldModel",
      "line": 5,
      "safe_to_remove": True
    }
  ],
  "dead_code": [
    {
      "file": "src/utils/helpers.py",
      "function": "unused_helper",
      "line": 42,
      "safe_to_remove": True,
      "reason": "Never called"
    }
  ],
  "code_duplication": [
    {
      "files": ["src/services/a.py", "src/services/b.py"],
      "pattern": "duplicate_function",
      "lines": [10, 15],
      "can_extract": True
    }
  ],
  "complexity": [
    {
      "file": "src/services/complex.py",
      "function": "long_function",
      "cyclomatic_complexity": 25,
      "can_simplify": True
    }
  ],
  "import_graph": {
    "nodes": [...],
    "edges": [...],
    "circular": [...],
    "orphaned": [...]
  }
})

Logging:
  await ctx.info(f"Found {len(unused_imports)} unused imports")
  await ctx.info(f"Found {len(dead_code)} dead code items")
  await ctx.info(f"Found {len(code_duplication)} code duplication patterns")
```

### Stage 1.6 - Script Redundancy Analysis

```yaml
Tool: mcp_desktop-commander_read_file
Path: Makefile (absolute path)
Read: Makefile content
Extract: All targets and their commands

Tool: mcp_desktop-commander_list_directory
Path: scripts/ (absolute path)
List: All script files (*.sh, *.py)

For each script file:
  Tool: mcp_desktop-commander_read_file
  Path: Script file (absolute path)
  Read: Script content

  Tool: mcp_desktop-commander_start_search
  Pattern: Script filename or function name
  SearchType: "content"
  Find: References to script in code/docs/Makefile

  Tool: mcp_sequential-thinking_sequentialthinking
  Input: Script content + Makefile targets + references
  Thoughts: 8-10
  Analyze:
    1. Does script name match a Makefile target?
    2. Does script functionality duplicate a Makefile command?
    3. Is script referenced anywhere (code, docs, other scripts)?
    4. Is script actively used (check git history frequency)?
    5. Can script functionality be replaced by Makefile?
    6. Is script an alternative implementation or primary?

  Classify:
    - Redundant (duplicates Makefile, can be removed)
    - Unused (never referenced, safe to remove)
    - Alternative (provides alternative implementation, keep)
    - Primary (actively used, no Makefile equivalent, keep)

Progress: await ctx.report_progress(1.6, 13, "Analyzing script redundancy")
State: ctx.set_state("script_analysis", {
  "redundant": [
    {
      "script": "scripts/start-backend.sh",
      "makefile_target": "backend",
      "reason": "Duplicates 'make backend' functionality",
      "safe_to_remove": True,
      "impact_score": 3,
      "references": 0
    }
  ],
  "unused": [
    {
      "script": "scripts/old-script.sh",
      "reason": "Never referenced, no git history",
      "safe_to_remove": True,
      "impact_score": 2,
      "references": 0
    }
  ],
  "alternative": [
    {
      "script": "scripts/start-backend-jit.sh",
      "reason": "Provides JIT optimization alternative",
      "safe_to_remove": False,
      "impact_score": 1
    }
  ],
  "primary": [
    {
      "script": "scripts/mcp_tool.py",
      "reason": "No Makefile equivalent, actively used",
      "safe_to_remove": False,
      "impact_score": 1
    }
  ]
})

Logging:
  await ctx.info(f"Found {len(redundant)} redundant scripts")
  await ctx.info(f"Found {len(unused)} unused scripts")
  await ctx.info(f"Found {len(alternative)} alternative scripts")
  await ctx.info(f"Found {len(primary)} primary scripts")
```

### Stage 1.7 - Root-Level Organization Analysis

```yaml
Tool: mcp_desktop-commander_list_directory
Path: Project root (absolute path)
Depth: 1
List: All files and directories at root level

Standard root files (keep):
  - README.md (main project readme)
  - LICENSE (standard location)
  - .gitignore (standard location)
  - Makefile (standard location)
  - package.json, pnpm-workspace.yaml (monorepo config)
  - CODE_OF_CONDUCT.md (standard location)
  - CONTRIBUTING.md (standard location)
  - SECURITY.md (standard location)
  - CLAUDE.md (project documentation)

For each root-level file:
  Tool: mcp_desktop-commander_start_search
  Pattern: Filename or content reference
  SearchType: "content"
  Find: References to file

  Tool: mcp_desktop-commander_get_file_info
  Path: Root file (absolute path)
  Get: File size, modification date, type

  Tool: mcp_sequential-thinking_sequentialthinking
  Input: File info + references + file type
  Thoughts: 5-7
  Analyze:
    1. Is file a standard root file (README, LICENSE, etc.)?
    2. Should file be in docs/ directory?
    3. Is file referenced from root location?
    4. Would moving file break references?
    5. What is the appropriate location?

  Classify:
    - Keep at root (standard location)
    - Move to docs/ (documentation file)
    - Move to .config/ (config file)
    - Delete (temporary/analysis file)

Progress: await ctx.report_progress(1.7, 13, "Analyzing root-level organization")
State: ctx.set_state("root_organization", {
  "keep_at_root": [
    {
      "file": "README.md",
      "reason": "Standard root location",
      "action": "keep"
    },
    {
      "file": "CLAUDE.md",
      "reason": "Project documentation, standard location",
      "action": "keep"
    }
  ],
  "move_to_docs": [
    {
      "file": "CLEANUP_ANALYSIS.md",
      "target": "docs/reviews/CLEANUP_ANALYSIS.md",
      "reason": "Analysis document belongs in docs/reviews/",
      "safe_to_move": True,
      "impact_score": 2,
      "references": 0
    }
  ],
  "move_to_config": [],
  "delete": []
})

Logging:
  await ctx.info(f"Found {len(keep_at_root)} files to keep at root")
  await ctx.info(f"Found {len(move_to_docs)} files to move to docs/")
  await ctx.info(f"Found {len(move_to_config)} files to move to config/")
  await ctx.info(f"Found {len(delete)} files to delete")
```

### Stage 1.8 - Large File Analysis

```yaml
Tool: mcp_desktop-commander_list_directory
Path: Project root (recursive, depth=5)
List: All files

For each file:
  Tool: mcp_desktop-commander_get_file_info
  Path: File (absolute path)
  Get: File size

  If file_size > threshold:
    Thresholds:
      - Images: >500KB (test data)
      - PDFs: >1MB (test invoices)
      - JSON: >100KB (test fixtures)
      - Logs: >10MB
      - Database dumps: >5MB
      - Other: >1MB

    Tool: mcp_desktop-commander_start_search
    Pattern: Filename or content reference
    SearchType: "content"
    Find: References to large file

    Tool: mcp_sequential-thinking_sequentialthinking
    Input: File size + type + references + path
    Thoughts: 5-7
    Analyze:
      1. Is file a build artifact (should be in .gitignore)?
      2. Is file test/sample data?
      3. Is file referenced in code/tests?
      4. Can file be regenerated?
      5. Should file be moved to external storage?
      6. Should file be added to .gitignore?

    Classify:
      - Test data (can be removed or moved to .gitignore)
      - Sample data (can be removed)
      - Build artifact (should be in .gitignore)
      - Required file (keep, but may need optimization)
      - Large log (can be deleted)

Progress: await ctx.report_progress(1.8, 13, "Analyzing large files")
State: ctx.set_state("large_files", {
  "test_data": [
    {
      "file": "data/shipping-labels/UPS_Express_1Z09E1D36626453915_label.png",
      "size": 245760,
      "type": "image",
      "reason": "Test/sample shipping label",
      "safe_to_remove": True,
      "impact_score": 2,
      "action": "delete_or_gitignore"
    },
    {
      "file": "data/shipping-labels/UPS_Express_1Z09E1D36634440520_official_invoice.pdf",
      "size": 1048576,
      "type": "pdf",
      "reason": "Test invoice",
      "safe_to_remove": True,
      "impact_score": 2,
      "action": "delete_or_gitignore"
    }
  ],
  "build_artifacts": [
    {
      "file": "apps/frontend/dist/bundle.js",
      "size": 2097152,
      "type": "build",
      "reason": "Build artifact, should be in .gitignore",
      "safe_to_remove": True,
      "impact_score": 1,
      "action": "verify_gitignore"
    }
  ],
  "required": [
    {
      "file": "apps/backend/tests/captured_responses/large_response.json",
      "size": 153600,
      "type": "test_fixture",
      "reason": "Required for tests",
      "safe_to_remove": False,
      "impact_score": 1,
      "action": "keep"
    }
  ]
})

Logging:
  await ctx.info(f"Found {len(test_data)} test data files ({total_size} bytes)")
  await ctx.info(f"Found {len(build_artifacts)} build artifacts")
  await ctx.info(f"Found {len(required)} required large files")
```

### Stage 2 - Analyze File Dependencies

```yaml
Tool: mcp_desktop-commander_start_search
Pattern: Import/reference patterns for each file
SearchType: "content"
Find: All references to cleanup targets

For each file:
  Tool: mcp_desktop-commander_start_search
  Pattern: Import/reference to file
  SearchType: "content"
  Find: References

  If referenced:
    Mark as "keep" (not safe to delete)
  Else:
    Mark as "safe_to_delete"

Tool: mcp_desktop-commander_read_file
Path: .gitignore
Read: Ignore patterns

If file matches .gitignore:
  Mark as "should_be_ignored" (not deleted, should be in .gitignore)

Progress: await ctx.report_progress(2, 13, "Analyzing file dependencies")
State: ctx.set_state("dependency_analysis", {
  "safe_to_delete": [list of files],
  "keep": [list of referenced files],
  "should_be_ignored": [list of files matching .gitignore]
})

### Stage 2.5 - Dependency Analysis

```yaml
# Detect package manager and read package files
Tool: mcp_desktop-commander_start_search
Pattern: Package files
SearchType: "file"
Find: package.json, pyproject.toml, Cargo.toml, go.mod, requirements.txt

For each package file:
  Tool: mcp_desktop-commander_read_file
  Path: Package file (absolute path)
  Read: Dependencies list

  # Parse dependencies
  Parse:
    - Extract all dependencies (prod + dev)
    - Extract version constraints
    - Identify duplicate entries

# Map imports to packages
Tool: mcp_desktop-commander_start_search
Pattern: Import statements
SearchType: "content"
Find: All imports across codebase

For each dependency:
  # Check if package is imported
  Tool: mcp_desktop-commander_start_search
  Pattern: Package name in imports
  SearchType: "content"
  Find: References to package

  If not found:
    Mark as "unused"

  # Check for transitive dependencies
  Tool: mcp_sequential-thinking_sequentialthinking
  Input: Package + import graph
  Thoughts: 5-7
  Analyze:
    1. Is package directly imported?
    2. Is package used transitively?
    3. Is package a dev dependency used in build?
    4. Can package be safely removed?

# Check for outdated dependencies
Tool: mcp_desktop-commander_start_process
Command: Check for updates
  Python: "pip list --outdated" or "pip-audit"
  JavaScript: "npm outdated" or "pnpm outdated"
  Go: "go list -u -m all"
  Rust: "cargo outdated"
Timeout: 60000ms

Progress: await ctx.report_progress(3, 13, "Analyzing dependencies")
State: ctx.set_state("dependency_analysis", {
  "unused_packages": [
    {
      "package": "lodash",
      "version": "^4.17.21",
      "file": "package.json",
      "safe_to_remove": True,
      "reason": "Not imported anywhere"
    }
  ],
  "outdated_packages": [
    {
      "package": "fastapi",
      "current": "0.68.0",
      "latest": "0.104.0",
      "file": "pyproject.toml",
      "can_update": True
    }
  ],
  "duplicate_dependencies": [
    {
      "package": "react",
      "files": ["package.json", "apps/frontend/package.json"],
      "versions": ["^18.0.0", "^18.2.0"],
      "can_consolidate": True
    }
  ],
  "unused_dev_dependencies": [
    {
      "package": "@types/node",
      "file": "package.json",
      "safe_to_remove": True,
      "reason": "Not used in build"
    }
  ],
  "transitive_dependencies": {
    "used": [...],
    "unused": [...]
  }
})

Logging:
  await ctx.info(f"Found {len(unused_packages)} unused packages")
  await ctx.info(f"Found {len(outdated_packages)} outdated packages")
  await ctx.info(f"Found {len(duplicate_dependencies)} duplicate dependencies")
```

### Stage 3 - Get Cleanup Patterns

```yaml
Tool: mcp_Context7_resolve-library-id
Query: Detect project type from package.json/pyproject.toml
Examples:
  "fastapi" → /fastapi/fastapi
  "react" → /facebook/react
  "gin" → /gin-gonic/gin

Tool: mcp_Context7_get-library-docs
Library: Resolved ID
Topic: "project cleanup patterns temporary files build artifacts best practices"
Tokens: 3000

Progress: await ctx.report_progress(4, 13, "Loading cleanup patterns")
State: ctx.set_state("cleanup_patterns", patterns_content)

Error handling:
  from fastmcp.exceptions import ToolError
  try:
    patterns = await context7_call()
  except ToolError as e:
    await ctx.warning("Context7 unavailable, using generic patterns")
    patterns = None

Logging:
  if patterns:
    await ctx.info("Loaded cleanup patterns")
  else:
    await ctx.warning("Using generic cleanup patterns")
```

### Stage 4 - Classify Cleanup Targets

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Cleanup targets + dependency analysis + cleanup patterns
Thoughts: 10-12
Classify:
  1. Temporary vs build artifacts vs unused vs duplicates
  2. Priority (critical/high/medium/low)
  3. Safety (safe/risky/unsafe)
  4. Space savings potential
  5. Safe deletion order
  6. What breaks if deleted?
  7. Can it be regenerated?

Progress: await ctx.report_progress(5, 13, "Classifying cleanup targets")
State: ctx.set_state("classified_targets", {
  "temporary": [...],
  "build_artifacts": [...],
  "unused": [...],
  "code_quality": [
    {
      "path": "src/services/user.py",
      "type": "unused_import",
      "import": "from models.old import OldModel",
      "line": 5,
      "priority": "high",
      "safety": "safe",
      "impact_score": 2,
      "can_regenerate": False
    },
    {
      "path": "src/utils/helpers.py",
      "type": "dead_code",
      "function": "unused_helper",
      "line": 42,
      "priority": "medium",
      "safety": "safe",
      "impact_score": 3,
      "can_regenerate": False
    }
  ],
  "dependencies": [
    {
      "package": "lodash",
      "type": "unused",
      "priority": "high",
      "safety": "safe",
      "impact_score": 4,
      "space_savings": 500000
    }
  ],
  "configuration": [...],
  "tests": [...],
  "git": [...],
  "script_redundancy": [
    {
      "script": "scripts/start-backend.sh",
      "type": "redundant",
      "priority": "medium",
      "safety": "safe",
      "impact_score": 3,
      "reason": "Duplicates Makefile target"
    }
  ],
  "root_organization": [
    {
      "file": "CLEANUP_ANALYSIS.md",
      "type": "move_to_docs",
      "target": "docs/reviews/CLEANUP_ANALYSIS.md",
      "priority": "low",
      "safety": "safe",
      "impact_score": 2
    }
  ],
  "large_files": [
    {
      "file": "data/shipping-labels/label.png",
      "type": "test_data",
      "size": 245760,
      "priority": "medium",
      "safety": "safe",
      "impact_score": 2,
      "action": "delete_or_gitignore"
    }
  ],
  "readme_consolidation": [
    {
      "file": "docs/reviews/README.md",
      "type": "redundant",
      "priority": "low",
      "safety": "safe",
      "impact_score": 2,
      "reason": "Content overlaps with docs/README.md"
    }
  ]
})

Logging:
  await ctx.info(f"Classified {len(temporary)} temporary files")
  await ctx.info(f"Classified {len(build_artifacts)} build artifacts")
  await ctx.info(f"Classified {len(unused)} unused files")
  await ctx.info(f"Classified {len(code_quality)} code quality issues")
  await ctx.info(f"Classified {len(dependencies)} dependency issues")
  await ctx.info(f"Classified {len(configuration)} configuration issues")
  await ctx.info(f"Classified {len(tests)} test cleanup issues")
  await ctx.info(f"Classified {len(git)} git cleanup issues")
  await ctx.info(f"Classified {len(script_redundancy)} script redundancy issues")
  await ctx.info(f"Classified {len(root_organization)} root organization issues")
  await ctx.info(f"Classified {len(large_files)} large file issues")
  await ctx.info(f"Classified {len(readme_consolidation)} README consolidation issues")
```

### Stage 5 - Generate Cleanup Plan

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Classified targets + cleanup patterns
Thoughts: 12-15
Generate: Prioritized cleanup plan

Plan structure:
  1. Delete temporary files (safe, high priority)
  2. Delete build artifacts (safe, medium priority)
  3. Delete unused files (safe, low priority)
  4. Remove duplicates (safe, medium priority)
  5. Clean empty directories (safe, low priority)

Progress: await ctx.report_progress(6, 13, "Generating cleanup plan")
State: ctx.set_state("cleanup_plan", {
  "plan": [
    {
      "step": 1,
      "action": "delete",
      "target": "apps/backend/.cache/",
      "reason": "Temporary cache, can be regenerated",
      "space_savings": 1024000,
      "impact_score": 1,
      "safe": True
    },
    {
      "step": 2,
      "action": "remove_import",
      "target": "src/services/user.py",
      "import": "from models.old import OldModel",
      "line": 5,
      "reason": "Unused import",
      "impact_score": 2,
      "safe": True
    },
    {
      "step": 3,
      "action": "remove_dead_code",
      "target": "src/utils/helpers.py",
      "function": "unused_helper",
      "line": 42,
      "reason": "Dead code, never called",
      "impact_score": 3,
      "safe": True
    },
    {
      "step": 4,
      "action": "remove_dependency",
      "target": "package.json",
      "package": "lodash",
      "reason": "Unused package",
      "space_savings": 500000,
      "impact_score": 4,
      "safe": True
    },
    {
      "step": 5,
      "action": "refactor_duplicate",
      "target": ["src/services/a.py", "src/services/b.py"],
      "pattern": "duplicate_function",
      "reason": "Code duplication, extract to shared function",
      "impact_score": 5,
      "safe": True
    }
  ],
  "summary": {
    "total_items": 35,
    "total_space": 53628800,
    "code_reduction": 250,
    "temporary": 10,
    "build_artifacts": 5,
    "unused": 8,
    "code_quality": 12,
    "dependencies": 5,
    "configuration": 3,
    "tests": 4,
    "git": 2,
    "script_redundancy": 3,
    "root_organization": 2,
    "large_files": 5,
    "readme_consolidation": 2,
    "estimated_time": "2-5 minutes",
    "risk": "low",
    "average_impact_score": 3.2
  }
})

Logging:
  await ctx.info(f"Generated cleanup plan: {len(plan)} items")
  await ctx.info(f"Estimated space savings: {total_space} bytes")
  await ctx.info(f"Estimated code reduction: {code_reduction} lines")
  await ctx.info(f"Average impact score: {average_impact_score}/10")
```

### Stage 6 - Backup Critical Files

```yaml
For each file to delete:
  If file_size < 10MB:
    Tool: mcp_desktop-commander_read_file
    Path: File to delete (absolute path)
    Read: File content

    State: ctx.set_state("backup", {
      "path": file_path,
      "content": file_content,
      "size": file_size,
      "timestamp": datetime.now().isoformat()
    })
  Else:
    # Large files: Store metadata only
    State: ctx.set_state("backup", {
      "path": file_path,
      "size": file_size,
      "timestamp": datetime.now().isoformat(),
      "note": "File too large to backup, metadata stored"
    })

For directories:
  Tool: mcp_desktop-commander_list_directory
  Path: Directory to delete
  List: All files in directory

  State: ctx.set_state("backup", {
    "path": directory_path,
    "files": [list of files],
    "size": total_size,
    "timestamp": datetime.now().isoformat()
  })

Progress: await ctx.report_progress(7, 13, "Backing up critical files")
Logging:
  await ctx.debug(f"Backed up {file_path}")
```

### Stage 7 - Apply Cleanup

```yaml
For each item in cleanup plan:
  If action == "delete":
    Tool: mcp_desktop-commander_delete_file
    Path: Target file/directory (absolute path)

    Progress: await ctx.report_progress(6, 8, f"Deleting {target}")
    Logging:
      await ctx.info(f"Deleted: {target}")

  If action == "remove_duplicate":
    # Keep newest, delete older
    Tool: mcp_desktop-commander_delete_file
    Path: Older duplicate file

    Logging:
      await ctx.info(f"Removed duplicate: {target}")

  If action == "remove_import":
    Tool: mcp_desktop-commander_read_file
    Path: Target file (absolute path)
    Read: File content

    Tool: mcp_desktop-commander_edit_block
    File: Target file
    Remove: Unused import line

    Logging:
      await ctx.info(f"Removed unused import: {import} from {target}")

  If action == "remove_dead_code":
    Tool: mcp_desktop-commander_read_file
    Path: Target file (absolute path)
    Read: File content

    Tool: mcp_desktop-commander_edit_block
    File: Target file
    Remove: Dead code block

    Logging:
      await ctx.info(f"Removed dead code: {function} from {target}")

  If action == "remove_dependency":
    Tool: mcp_desktop-commander_read_file
    Path: Package file (absolute path)
    Read: Package file content

    Tool: mcp_desktop-commander_edit_block
    File: Package file
    Remove: Dependency entry

    Logging:
      await ctx.info(f"Removed dependency: {package} from {target}")

  If action == "refactor_duplicate":
    Tool: mcp_sequential-thinking_sequentialthinking
    Input: Duplicate code pattern
    Thoughts: 10-12
    Generate: Refactored code (extract to shared function)

    Tool: mcp_desktop-commander_edit_block
    File: Target files
    Replace: Duplicate code with shared function call

    Logging:
      await ctx.info(f"Refactored duplicate code: {pattern} in {targets}")

  If action == "clean_config":
    Tool: mcp_desktop-commander_read_file
    Path: Config file (absolute path)
    Read: Config content

    Tool: mcp_desktop-commander_edit_block
    File: Config file
    Remove: Unused/redundant config entries

    Logging:
      await ctx.info(f"Cleaned configuration: {target}")

  If action == "remove_redundant_script":
    Tool: mcp_desktop-commander_delete_file
    Path: Redundant script (absolute path)

    Logging:
      await ctx.info(f"Removed redundant script: {target}")

  If action == "move_file":
    Tool: mcp_desktop-commander_read_file
    Path: Source file (absolute path)
    Read: File content

    Tool: mcp_desktop-commander_write_file
    Path: Destination file (absolute path)
    Content: File content

    Tool: mcp_desktop-commander_delete_file
    Path: Source file (absolute path)

    Logging:
      await ctx.info(f"Moved: {source} → {destination}")

  If action == "remove_large_file":
    Tool: mcp_desktop-commander_delete_file
    Path: Large file (absolute path)

    Logging:
      await ctx.info(f"Removed large file: {target} ({size} bytes)")

  If action == "add_to_gitignore":
    Tool: mcp_desktop-commander_read_file
    Path: .gitignore (absolute path)
    Read: Current .gitignore content

    Tool: mcp_desktop-commander_edit_block
    File: .gitignore
    Add: Pattern for large file

    Logging:
      await ctx.info(f"Added {pattern} to .gitignore")

  If action == "consolidate_readme":
    Tool: mcp_desktop-commander_read_file
    Path: README files (absolute paths)
    Read: All README content

    Tool: mcp_sequential-thinking_sequentialthinking
    Input: Multiple README contents
    Thoughts: 8-10
    Generate: Consolidated README content

    Tool: mcp_desktop-commander_edit_block
    File: Primary README
    Replace: With consolidated content

    Tool: mcp_desktop-commander_delete_file
    Path: Redundant README files

    Logging:
      await ctx.info(f"Consolidated README files: {redundant_readmes} → {primary_readme}")

Progress: await ctx.report_progress(8, 13, f"Applying cleanup {i}/{total}")
```

### Stage 7.5 - Structure Optimization

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: File structure + cleanup plan + classified targets
Thoughts: 12-15
Generate: Structure optimization plan

Analyze:
  1. Which directories are empty or contain only empty subdirectories?
  2. Which files are in wrong directories?
  3. Are there inconsistent naming conventions?
  4. Can directories be consolidated?
  5. Are there orphaned directories (no files, only empty subdirs)?
  6. What is the optimal directory structure?

Actions:
  1. Move root-level docs to docs/
  2. Consolidate empty directories
  3. Standardize naming conventions
  4. Create missing directory structure
  5. Remove orphaned directories
  6. Organize files by type/function

For each optimization:
  Tool: mcp_desktop-commander_list_directory
  Path: Directory to optimize
  List: Current structure

  Tool: mcp_sequential-thinking_sequentialthinking
  Input: Current structure + best practices
  Thoughts: 5-7
  Generate: Optimized structure plan

  Apply optimizations:
    - Move files to correct directories
    - Consolidate empty directories
    - Standardize naming
    - Remove orphaned directories

Progress: await ctx.report_progress(7.5, 13, "Optimizing project structure")
State: ctx.set_state("structure_optimization", {
  "file_moves": [
    {
      "source": "CLEANUP_ANALYSIS.md",
      "destination": "docs/reviews/CLEANUP_ANALYSIS.md",
      "reason": "Analysis document belongs in docs/reviews/",
      "safe": True
    }
  ],
  "directory_consolidations": [
    {
      "directories": ["docs/temp/", "docs/old/"],
      "target": "docs/archive/",
      "reason": "Consolidate temporary/old docs",
      "safe": True
    }
  ],
  "empty_directories": [
    {
      "directory": "apps/backend/temp/",
      "action": "remove",
      "reason": "Empty directory",
      "safe": True
    }
  ],
  "naming_fixes": [
    {
      "file": "docs/API.md",
      "target": "docs/API_REFERENCE.md",
      "reason": "Standardize naming convention",
      "safe": True
    }
  ]
})

Logging:
  await ctx.info(f"Planned {len(file_moves)} file moves")
  await ctx.info(f"Planned {len(directory_consolidations)} directory consolidations")
  await ctx.info(f"Planned {len(empty_directories)} empty directory removals")
  await ctx.info(f"Planned {len(naming_fixes)} naming fixes")
```

### Stage 8 - Verify

```yaml
Tool: mcp_desktop-commander_start_process
Command: Verify dependency integrity
  Python: "pip check" or "pip install --dry-run"
  JavaScript: "npm ls" or "pnpm install --dry-run"
  Go: "go mod verify"
  Rust: "cargo check"
Timeout: 60000ms

Tool: mcp_desktop-commander_start_process
Command: Verify code quality
  Python: "ruff check ." or "mypy ."
  JavaScript: "eslint ." or "tsc --noEmit"
  Go: "go vet ./..."
  Rust: "cargo clippy"
Timeout: 120000ms

Tool: mcp_desktop-commander_start_process
Command: Run tests (quick check)
  Python: "pytest -x -q" (fail fast, quiet)
  JS: "vitest run --reporter=verbose" (quick)
  Go: "go test ./..." (quick)
  Rust: "cargo test" (quick)

Progress: await ctx.report_progress(9, 13, "Verifying cleanup")

Success path:
  if no_broken_imports and dependency_integrity_ok and code_quality_ok and tests_pass:
    await ctx.info("Cleanup verified, project still works")
    return {
      "status": "success",
      "deleted": count_deleted,
      "space_freed": total_space,
      "code_reduced": code_reduction,
      "dependencies_removed": dependencies_removed,
      "tests": "passed",
      "impact_score": average_impact_score
    }

Failure path:
  await ctx.error("Some cleanup broke project")
  # Report which deletions caused issues
  return {
    "status": "partial",
    "deleted": count_deleted,
    "failed": count_failed,
    "issues": [list of issues]
  }
```

## Integration with `/simplify` and `/code-improvement`

**Workflow Options:**

**Option 1: Simplify → Clean**
```bash
# Step 1: Identify overbloat
/simplify

# Step 2: Clean up files identified
/clean --from-simplify
```

**Option 2: Clean → Code Improvement → Test → Commit**
```bash
# Enhanced cleanup with code improvements
/clean --with-code-improvement
```

**Option 3: Full Workflow Chain**
```bash
# Complete cleanup workflow
/workflow:cleanup
# Chain: simplify → clean → test → commit
```

**Option 4: Enhanced Cleanup Workflow**
```bash
# With code improvement integration
/workflow:cleanup --with-code-improvement
# Chain: simplify → clean → code-improvement → test → commit
```

**Reading Simplify Output:**
- Reads `.simplify-recommendations.json` if exists
- Parses simplify recommendations for file deletions
- Prioritizes files marked for removal by simplify
- Applies cleanup with same safety checks

**Simplify Integration Stage:**

```yaml
If --from-simplify flag:
  Tool: mcp_desktop-commander_start_search
  Pattern: Simplify recommendations or state
  SearchType: "file"
  Find: .simplify-recommendations.json or simplify state

  Tool: mcp_desktop-commander_read_file
  Path: Simplify recommendations file
  Read: Recommendations

  Parse: Extract files marked for deletion
  Priority: Add to cleanup_targets["unused"] with high priority

  Logging:
    await ctx.info(f"Loaded {len(simplify_files)} files from simplify recommendations")
```

## Usage Examples

```bash
# Clean up everything (default)
/clean

# Clean from simplify recommendations
/clean --from-simplify

# Clean specific category
/clean --category=temporary
/clean --category=build
/clean --category=unused
/clean --category=code-quality
/clean --category=dependencies
/clean --category=configuration
/clean --category=tests
/clean --category=git
/clean --category=script-redundancy
/clean --category=root-organization
/clean --category=large-files
/clean --category=readme-consolidation

# Enable code improvement integration
/clean --with-code-improvement

# Parallel analysis (faster)
/clean --parallel

# Dry-run mode (show what would be deleted)
/clean --dry-run

# Clean specific directory
/clean apps/backend/

# Aggressive cleanup (removes more, less safe)
/clean --aggressive
```

## Output Format

### Analysis Output

```
🔍 Scanning for Cleanup Targets:
Scanning project for temporary files, build artifacts, unused files...

📊 Scan Results:
Found: 35 cleanup targets
  - Temporary files: 10 (1.0 MB)
  - Build artifacts: 5 (50 MB)
  - Unused files: 8 (40 KB)
  - Duplicates: 2 (8 KB)
  - Code quality issues: 12 (unused imports, dead code)
  - Dependency issues: 5 (unused packages)
  - Configuration issues: 3 (redundant settings)
  - Test cleanup: 4 (unused fixtures)
  - Git cleanup: 2 (unused branches)
  - Script redundancy: 3 (redundant scripts)
  - Root organization: 2 (files to move)
  - Large files: 5 (test data files)
  - README consolidation: 2 (redundant READMEs)

🔍 Deep Code Analysis:
Analyzing code files for unused imports and dead code...
  - Found: 12 unused imports
  - Found: 8 dead code functions
  - Found: 3 code duplication patterns
  - Found: 2 high complexity functions

📦 Dependency Analysis:
Analyzing package dependencies...
  - Found: 5 unused packages
  - Found: 3 outdated packages
  - Found: 2 duplicate dependencies
  - Found: 2 unused dev dependencies

🔗 Analyzing Dependencies:
Checking file references...
  - 20 files safe to delete (not referenced)
  - 5 files kept (referenced in code)
  - 12 code quality issues safe to fix
  - 5 dependencies safe to remove

📋 Classifying Targets:
Temporary Files (10):
  1. apps/backend/.cache/ - 1.0 MB (safe, can regenerate)
  2. apps/frontend/.vite/ - 500 KB (safe, can regenerate)
  3. *.log files - 200 KB (safe, can regenerate)

Build Artifacts (5):
  1. apps/frontend/dist/ - 50 MB (safe, can regenerate)
  2. apps/backend/htmlcov/ - 2 MB (safe, can regenerate)
  3. __pycache__/ directories - 500 KB (safe, can regenerate)

Code Quality Issues (12):
  1. src/services/user.py:5 - Unused import: from models.old import OldModel (impact: 2/10)
  2. src/utils/helpers.py:42 - Dead code: unused_helper() function (impact: 3/10)
  3. src/services/complex.py:100 - High complexity: long_function() (impact: 5/10)
  4. Code duplication: duplicate_function in src/services/a.py and b.py (impact: 5/10)

Dependency Issues (5):
  1. lodash - Unused package (500 KB, impact: 4/10)
  2. fastapi - Outdated: 0.68.0 → 0.104.0 (impact: 3/10)
  3. react - Duplicate in package.json and apps/frontend/package.json (impact: 2/10)

Configuration Issues (3):
  1. .env.example - Unused environment variables (impact: 2/10)
  2. vite.config.js - Redundant settings (impact: 1/10)

Script Redundancy (3):
  1. scripts/start-backend.sh - Duplicates 'make backend' (impact: 3/10)
  2. scripts/old-script.sh - Never referenced (impact: 2/10)

Root Organization (2):
  1. CLEANUP_ANALYSIS.md → docs/reviews/ (impact: 2/10)

Large Files (5):
  1. data/shipping-labels/label.png - 245 KB test data (impact: 2/10)
  2. data/shipping-labels/invoice.pdf - 1 MB test invoice (impact: 2/10)

README Consolidation (2):
  1. docs/reviews/README.md - Overlaps with docs/README.md (impact: 2/10)

💡 Cleanup Plan:
Priority Order:
  1. Delete temporary files (1.0 MB freed, impact: 1/10)
  2. Remove unused imports (12 imports, impact: 2/10)
  3. Delete build artifacts (50 MB freed, impact: 1/10)
  4. Remove unused dependencies (500 KB freed, impact: 4/10)
  5. Remove dead code (8 functions, impact: 3/10)
  6. Refactor duplicate code (3 patterns, impact: 5/10)
  7. Delete unused files (40 KB freed, impact: 2/10)
  8. Remove duplicates (8 KB freed, impact: 2/10)
  9. Remove redundant scripts (3 scripts, impact: 3/10)
  10. Move root-level files (2 files, impact: 2/10)
  11. Remove large test data files (5 files, 1.5 MB freed, impact: 2/10)
  12. Consolidate README files (2 files, impact: 2/10)
  13. Optimize project structure (impact: 3/10)

Estimated Space Savings: 53.0 MB
Estimated Code Reduction: 250 lines
Estimated Time: 2-5 minutes
Risk Level: Low (all deletions are safe)
Average Impact Score: 3.2/10

✅ Analysis Complete
```

### Applied Cleanup Output

```
🔍 Scanning for Cleanup Targets:
Found: 25 cleanup targets

💡 Cleanup Plan Generated:
10 temporary, 5 build artifacts, 8 unused, 2 duplicates, 12 code quality, 5 dependencies, 3 config, 4 tests, 3 scripts, 2 root files, 5 large files, 2 READMEs

✅ Applying Cleanup:

Step 1/35: Deleting temporary cache...
  ✅ Deleted: apps/backend/.cache/ (1.0 MB freed, impact: 1/10)

Step 2/35: Removing unused imports...
  ✅ Removed: from models.old import OldModel from src/services/user.py:5 (impact: 2/10)

Step 3/35: Deleting build artifacts...
  ✅ Deleted: apps/frontend/dist/ (50 MB freed, impact: 1/10)

Step 4/35: Removing unused dependencies...
  ✅ Removed: lodash from package.json (500 KB freed, impact: 4/10)

Step 5/35: Removing dead code...
  ✅ Removed: unused_helper() from src/utils/helpers.py:42 (impact: 3/10)

Step 6/35: Refactoring duplicate code...
  ✅ Extracted: duplicate_function to shared module (impact: 5/10)

...

Step 35/47: Consolidating README files...
  ✅ Consolidated: docs/reviews/README.md → docs/README.md (impact: 2/10)

Step 36/47: Optimizing project structure...
  ✅ Moved: CLEANUP_ANALYSIS.md → docs/reviews/ (impact: 2/10)
  ✅ Removed: 2 empty directories (impact: 1/10)

🧪 Verifying Cleanup:
Checking imports...
Result: ✅ No broken imports

Checking dependency integrity...
Result: ✅ All dependencies valid

Checking code quality...
Result: ✅ No syntax errors

Running quick tests...
Result: ✅ All tests passed

✅ Cleanup Complete:
  - Deleted: 30 files/directories
  - Moved: 2 files
  - Code reduced: 250 lines
  - Dependencies removed: 5 packages
  - Scripts removed: 3 redundant scripts
  - Large files removed: 5 test data files
  - READMEs consolidated: 2 files
  - Space freed: 53.0 MB
  - Tests: ✅ All passed
  - Imports: ✅ All valid
  - Dependencies: ✅ All valid
  - Code quality: ✅ Improved
  - Structure: ✅ Optimized

Summary:
  - Temporary files: 10 removed
  - Build artifacts: 5 removed
  - Unused files: 8 removed
  - Code quality: 12 issues fixed
  - Dependencies: 5 removed
  - Configuration: 3 cleaned
  - Tests: 4 cleaned
  - Git: 2 branches removed
  - Script redundancy: 3 scripts removed
  - Root organization: 2 files moved
  - Large files: 5 files removed
  - README consolidation: 2 files consolidated
  - Structure optimization: Completed
  - Total time: 3.5 minutes
  - Average impact score: 3.2/10
```

## Performance

- Target scanning: 5-10s (recursive directory listing)
- Deep code analysis: 10-30s (AST parsing, parallel execution)
- Script redundancy analysis: 5-10s (Makefile parsing, script comparison)
- Root organization analysis: 3-5s (root file listing, classification)
- Large file analysis: 5-10s (file size checking, classification)
- Dependency analysis: 5-15s (package parsing, import mapping)
- File dependency analysis: 3-5s per file (search for references)
- Classification: 3-5s (Sequential-thinking, enhanced with impact scoring)
- Pattern loading: 2-4s (Context7, cached 24h)
- Plan generation: 5-8s (Sequential-thinking, enhanced planning)
- Backup: 1-5s (depends on file sizes)
- Cleanup: 30-90s (depends on number of files and code changes, includes structure optimization)
- Structure optimization: 10-20s (directory consolidation, file moves)
- Verification: 15-45s (dependency check, code quality, test execution)
- **Total: 85-225s** for analysis, **2-5 minutes** for full cleanup

**Performance Optimizations:**
- **Parallel Analysis**: AST parsing runs in parallel for multiple files
- **Caching**: AST parsing results cached for 24h, dependency graphs cached
- **Incremental Analysis**: Only analyzes changed files (uses Git diff)
- **Batch Processing**: Groups similar cleanup actions for efficiency

## Desktop Commander Tools Used

**Primary Tools:**
- `mcp_desktop-commander_list_directory` - Scan for cleanup targets
- `mcp_desktop-commander_delete_file` - Delete files/directories
- `mcp_desktop-commander_read_file` - Backup files, read .gitignore
- `mcp_desktop-commander_start_search` - Find file references
- `mcp_desktop-commander_get_file_info` - Get file metadata
- `mcp_desktop-commander_start_process` - Verify cleanup

**Supporting Tools:**
- `mcp_sequential-thinking_sequentialthinking` - Classification, plan generation, code analysis, refactoring
- `mcp_Context7_resolve-library-id` - Project type detection
- `mcp_Context7_get-library-docs` - Cleanup patterns, code improvement patterns

## Safety Features

- **Dry-run mode**: Show what would be deleted without applying
- **Dependency checking**: Verify files aren't referenced before deletion
- **Impact scoring**: Score each cleanup action (1-10), warn about high-impact changes
- **Dependency safety**: Check if package is used transitively, warn about breaking changes
- **Code quality safety**: Preserve important comments, don't remove TODO with context
- **Backup critical files**: Backup before deletion (small files <10MB)
- **Enhanced rollback**: Per-action rollback capability, cleanup log with restore instructions
- **Test verification**: Run tests after cleanup
- **Import checking**: Verify no broken imports
- **Dependency integrity**: Verify no missing packages after cleanup
- **Code quality verification**: Verify no syntax errors after cleanup
- **Rollback capability**: Can restore from backup if needed
- **Priority ordering**: Delete safest files first (lowest impact score)
- **Size warnings**: Warn before deleting large files
- **Confirmation prompts**: Require confirmation for high-impact changes (impact score >7)

## Error Handling

**File Not Found:**
- Report warning: "File already deleted or not found"
- Continue with next file

**Permission Errors:**
- Report error: "Permission denied"
- Suggest checking file permissions
- Skip file, continue with others

**Dependency Found:**
- Report warning: "File is referenced, skipping"
- Add to "keep" list
- Continue with next file

## Adapts To Any Project

Works automatically with:
- Python projects (detects `__pycache__/`, `.pyc`, `dist/`)
- JavaScript projects (detects `node_modules/.cache/`, `dist/`, `.next/`)
- Go projects (detects `target/`, build artifacts)
- Rust projects (detects `target/`, build artifacts)

**One command. Comprehensive cleanup. Safe deletion. Works with `/simplify`.**

---

## Integration Example

**Combined Workflow:**
```bash
# Step 1: Identify overbloat and enterprise features
/simplify

# Output: Identifies WebhookResponse model, unused endpoints, documentation bloat

# Step 2: Clean up files identified by simplify
/clean --from-simplify

# Output: Removes WebhookResponse files, unused endpoints, temporary docs

# Step 3: General cleanup
/clean

# Output: Removes build artifacts, temporary files, cache
```

**Result:** Clean, simplified project ready for personal use!
