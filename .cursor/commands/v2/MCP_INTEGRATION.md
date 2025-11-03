# MCP Integration & Auto-Discovery

Seamless integration with Model Context Protocol (MCP) servers for enhanced command capabilities. Automatic discovery, dynamic command generation, and intelligent tool routing.

## Overview

MCP servers provide specialized tools, prompts, and resources that extend slash command capabilities. The v2 system automatically:
- Discovers available MCP servers
- Generates commands from MCP prompts
- Routes tool calls to appropriate servers
- Caches responses for performance
- Handles authentication and permissions

## Connected MCP Servers

### Current Connections

```bash
/mcp:status

📡 MCP Server Status:

✓ context7
  ├─ Tools: resolve-library-id, get-library-docs
  ├─ Status: Connected
  ├─ Latency: 45ms
  └─ Used by: /gen:*, /context:*, /quality:*

✓ Desktop Commander
  ├─ Tools: start_process, read_file, write_file, list_directory
  ├─ Status: Connected
  ├─ Latency: 12ms
  └─ Used by: /test:*, /quality:*, all file operations

✓ sequential-thinking
  ├─ Tools: sequentialthinking
  ├─ Status: Connected
  ├─ Latency: 120ms
  └─ Used by: /quality:fix, /context:explain, /quality:refactor

✓ exa-web-search
  ├─ Tools: web_search_exa, get_code_context_exa
  ├─ Status: Connected
  ├─ Latency: 350ms
  └─ Used by: /research:*, /context:* (when needed)

Total: 4 servers, 12 tools
```

## Auto-Discovery

MCP prompts are automatically converted to slash commands:

### Discovery Process
```
1. Scan connected MCP servers
2. Extract available prompts
3. Generate slash commands
4. Register with command system
5. Document in /mcp:list
```

### Example: Auto-Generated Commands

```bash
/mcp:discover

Discovering MCP prompts...

Found 3 new prompts:
✓ context7://research-best-practices
  → /mcp:research-best-practices [topic]
  
✓ sequential-thinking://analyze-complexity
  → /mcp:analyze-complexity [code]
  
✓ desktop-commander://parallel-file-ops
  → /mcp:parallel-file-ops [operation] [files]

Commands registered and ready to use!
```

## Dynamic Command Generation

MCP prompts become first-class commands:

### Format
```bash
/mcp:<server>:<prompt-name> [args]
```

### Examples

```bash
# Context7: Get library documentation
/mcp:context7:library-docs react hooks

# Sequential Thinking: Analyze code complexity
/mcp:sequential-thinking:analyze @selection

# Desktop Commander: Parallel file operations
/mcp:desktop-commander:batch-rename *.test.js *.spec.js
```

## Tool Routing Intelligence

Commands automatically route to optimal MCP tools:

### Routing Table

```javascript
Command: /quality:fix
├─ Needs: Code analysis
├─ Routes to: sequential-thinking:sequentialthinking
├─ Then: Desktop Commander:write_file
└─ Finally: Verification with read_file

Command: /gen:api
├─ Needs: Framework best practices
├─ Routes to: context7:get-library-docs
├─ Then: Desktop Commander:write_file
└─ Finally: Test generation

Command: /test:run
├─ Needs: Process execution
├─ Routes to: Desktop Commander:start_process
├─ Then: Parallel execution (16 workers)
└─ Finally: Result aggregation
```

### Smart Tool Selection

```bash
/gen:component UserCard

# AI determines:
1. Need React best practices
   → Use: context7:get-library-docs('react')
   
2. Need component template
   → Use: context7:resolve-library-id('react')
   
3. Need file creation
   → Use: Desktop Commander:write_file
   
4. Need test generation
   → Use: context7:get-library-docs('react-testing-library')

All automatic, optimal routing
```

## MCP-Enhanced Commands

Commands that leverage MCP servers:

### /gen:* (Code Generation)

```markdown
---
mcp-tools:
  - server: context7
    tool: get-library-docs
    usage: Fetch framework best practices
  - server: Desktop Commander
    tool: write_file
    usage: Create files
---
```

### /quality:fix (Error Fixing)

```markdown
---
mcp-tools:
  - server: sequential-thinking
    tool: sequentialthinking
    usage: Deep analysis of errors
  - server: Desktop Commander
    tool: start_process
    usage: Run linters, tests
  - server: context7
    tool: get-library-docs
    usage: Framework-specific fixes
---
```

### /test:run (Testing)

```markdown
---
mcp-tools:
  - server: Desktop Commander
    tool: start_process
    usage: Execute test runners
  - server: Desktop Commander
    tool: list_directory
    usage: Find test files
---
```

## Command Metadata with MCP

Enhanced command metadata includes MCP info:

```markdown
---
name: fix
category: quality
mcp-integration:
  primary: sequential-thinking
  secondary: [context7, Desktop Commander]
  tools:
    - name: sequentialthinking
      server: sequential-thinking
      purpose: Root cause analysis
      fallback: Basic pattern matching
    - name: get-library-docs
      server: context7
      purpose: Framework-specific fixes
      fallback: Generic fixes
    - name: write_file
      server: Desktop Commander
      purpose: Apply fixes
      required: true
---
```

## MCP Server Configuration

Configure MCP servers in `.dev-config.json`:

```json
{
  "mcp": {
    "servers": {
      "context7": {
        "enabled": true,
        "priority": "high",
        "cache": {
          "enabled": true,
          "ttl": 3600
        },
        "rateLimit": {
          "requestsPerMinute": 60
        }
      },
      "desktopCommander": {
        "enabled": true,
        "priority": "critical",
        "parallelism": {
          "maxWorkers": 32
        }
      },
      "sequentialThinking": {
        "enabled": true,
        "priority": "medium",
        "timeout": 30000
      }
    },
    "autoDiscovery": {
      "enabled": true,
      "scanInterval": 300,
      "generateCommands": true
    }
  }
}
```

## Performance Optimization

### Caching Strategy

```javascript
MCP Response Cache:
├─ context7:get-library-docs('react')
│   └─ Cached for 1 hour (frequently used)
├─ sequential-thinking:analyze
│   └─ No cache (dynamic analysis)
└─ Desktop Commander:read_file
    └─ Cached for 5 minutes (file content)

Cache Hit Rate: 67%
Time Saved: 1.2s per cached call
```

### Parallel MCP Calls

```bash
/gen:component UserCard

# Parallel MCP calls:
[Call 1] context7:get-library-docs('react') - 450ms
[Call 2] context7:get-library-docs('typescript') - 420ms
[Call 3] context7:resolve-library-id('shadcn-ui') - 380ms

Total: 450ms (vs 1250ms sequential)
63% faster with parallelization
```

## MCP Command Examples

### Example 1: Research with Exa
```bash
# Auto-generated from MCP prompt
/mcp:exa:research "FastAPI best practices 2025"

# Uses: exa-web-search:web_search_exa
# Returns: Curated research with sources
# Time: ~2s
```

### Example 2: Deep Code Analysis
```bash
/mcp:sequential-thinking:analyze @selection --depth=5

# Uses: sequential-thinking:sequentialthinking
# Returns: Step-by-step reasoning (5 thoughts)
# Time: ~10s
```

### Example 3: Batch File Operations
```bash
/mcp:desktop-commander:parallel-find "test_*.py" --exec="pytest {}"

# Uses: Desktop Commander with 32 workers
# Returns: Parallel test execution
# Time: 4.2s (vs 45s sequential)
```

## Error Handling & Fallbacks

### MCP Server Unavailable

```bash
/quality:fix @errors

# Fallback chain:
1. Try: sequential-thinking (primary)
   ✗ Server timeout
   
2. Try: context7 (secondary)
   ✗ Rate limit exceeded
   
3. Try: Built-in patterns (fallback)
   ✓ Basic pattern matching
   
Fix applied using fallback method.
Warning: MCP servers unavailable, used basic patterns.
```

### Graceful Degradation

```javascript
Command Priority Levels:
├─ MCP Enhanced (best)
│   └─ Uses all MCP servers, best quality
├─ Partial MCP (good)
│   └─ Some MCP servers, good quality
└─ Fallback (acceptable)
    └─ No MCP, basic patterns
```

## MCP Tool Documentation

### Context7
```bash
/mcp:docs context7

Context7 MCP Server
===================

Tools:
1. resolve-library-id
   - Input: libraryName (string)
   - Output: Context7-compatible library ID
   - Usage: /gen:*, /context:*
   - Cache: 1 hour
   
2. get-library-docs
   - Input: libraryId (string), topic (optional)
   - Output: Documentation, patterns, examples
   - Usage: All code generation commands
   - Cache: 1 hour

Rate Limits: 60 requests/minute
Latency: ~300-500ms
Reliability: 99.2%
```

### Desktop Commander
```bash
/mcp:docs desktop-commander

Desktop Commander MCP Server
============================

Tools: 50+ file and process operations

Most Used:
1. start_process - Execute commands with smart detection
2. read_file - Read files with offset/length support
3. write_file - Write/append with chunking
4. list_directory - Recursive directory listing
5. edit_block - Surgical text replacements

Parallel Execution: Up to 32 workers (M3 Max)
Latency: ~10-50ms (local operations)
Reliability: 99.9%
```

### Sequential Thinking
```bash
/mcp:docs sequential-thinking

Sequential Thinking MCP Server
==============================

Tool: sequentialthinking

Purpose: Multi-step reasoning for complex problems
Input: thought, nextThoughtNeeded, thoughtNumber, totalThoughts
Output: Reasoning chain with verification

Usage:
- /quality:fix (complex errors)
- /context:explain (deep analysis)
- /quality:refactor (planning)

Latency: ~100-300ms per thought (3-10 thoughts typical)
Reliability: 98.5%
```

## Best Practices

✅ **Let auto-discovery work** - New MCP prompts become commands
✅ **Use MCP-enhanced commands** - Better quality than fallbacks
✅ **Configure caching** - Reduce latency for repeated calls
✅ **Monitor MCP status** - Check `/mcp:status` if issues
✅ **Leverage parallelism** - Multiple MCP calls simultaneously

## Monitoring

```bash
/mcp:stats

MCP Usage Statistics (Session):

Calls by Server:
├─ Desktop Commander: 342 calls (67%)
├─ context7: 89 calls (17%)
├─ sequential-thinking: 52 calls (10%)
└─ exa-web-search: 28 calls (6%)

Performance:
├─ Avg Latency: 85ms
├─ Cache Hit Rate: 64%
├─ Failures: 3 (0.6%)
└─ Fallbacks Used: 2

Top Commands Using MCP:
1. /test:run (Desktop Commander)
2. /gen:component (context7)
3. /quality:fix (sequential-thinking)
```

## Tips

1. **Check MCP status first** - Ensure servers connected
2. **Use caching** - Dramatically faster for repeated queries
3. **Parallel when possible** - Independent MCP calls
4. **Monitor failures** - Fallbacks work but are lower quality
5. **Discover regularly** - New MCP prompts added automatically

## Related Commands

- `/mcp:status` - Check MCP server health
- `/mcp:discover` - Find new MCP prompts
- `/mcp:docs [server]` - Server documentation
- `/mcp:stats` - Usage analytics
- `/mcp:cache:clear` - Clear MCP cache


