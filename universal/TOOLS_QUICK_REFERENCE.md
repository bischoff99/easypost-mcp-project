# Tools Quick Reference

**Quick lookup guide for AI assistant tools**

---

## 🔍 Search & Discovery

| Tool                                 | Purpose               | When to Use                                      |
| ------------------------------------ | --------------------- | ------------------------------------------------ |
| `codebase_search`                    | Semantic search       | Understanding concepts, finding related code     |
| `grep`                               | Exact pattern match   | Finding specific patterns, imports, functions    |
| `mcp_Desktop_Commander_start_search` | Advanced search       | Comprehensive pattern detection, large codebases |
| `glob_file_search`                   | Find files by pattern | Locating files by extension, name pattern        |

---

## 📖 Read & Analyze

| Tool                                   | Purpose          | When to Use                        |
| -------------------------------------- | ---------------- | ---------------------------------- |
| `read_file`                            | Read files       | Reading code, configs, docs        |
| `mcp_Desktop_Commander_read_file`      | Advanced reading | Tail operations, URLs, large files |
| `list_dir`                             | List directory   | Exploring structure                |
| `mcp_Desktop_Commander_list_directory` | Detailed listing | Recursive, with metadata           |

---

## ✏️ Edit & Write

| Tool                               | Purpose         | When to Use                     |
| ---------------------------------- | --------------- | ------------------------------- |
| `search_replace`                   | Precise edits   | Single/multiple replacements    |
| `mcp_Desktop_Commander_edit_block` | Surgical edits  | Multiple small changes          |
| `write`                            | Create files    | New files, documentation        |
| `mcp_Desktop_Commander_write_file` | Chunked writing | Large files (25-30 line chunks) |

---

## 📚 Documentation & Knowledge

| Tool                                  | Purpose        | When to Use                             |
| ------------------------------------- | -------------- | --------------------------------------- |
| `mcp_context7_get-library-docs`       | Official docs  | Framework documentation, best practices |
| `mcp_exa-search_get_code_context_exa` | Code examples  | Community patterns, real-world examples |
| `mcp_exa-search_web_search_exa`       | Latest info    | Framework updates, community trends     |
| `web_search`                          | General search | Broad information, tutorials            |

---

## ⚙️ Process & Execution

| Tool                                          | Purpose            | When to Use                            |
| --------------------------------------------- | ------------------ | -------------------------------------- |
| `run_terminal_cmd`                            | Simple commands    | Quick commands, validation             |
| `mcp_Desktop_Commander_start_process`         | Advanced execution | REPLs, interactive sessions            |
| `mcp_Desktop_Commander_interact_with_process` | REPL interaction   | Python/Node.js sessions, data analysis |
| `mcp_Desktop_Commander_read_process_output`   | Read output        | Getting command results                |

---

## ✅ Quality & Validation

| Tool                                  | Purpose       | When to Use                  |
| ------------------------------------- | ------------- | ---------------------------- |
| `read_lints`                          | Linter errors | After edits, quality checks  |
| `mcp_Desktop_Commander_get_file_info` | File metadata | Size, timestamps, line count |

---

## 🎯 Common Workflows

### Understand Code

```
codebase_search → grep → read_file
```

### Find Patterns

```
grep → mcp_Desktop_Commander_start_search → read_file
```

### Best Practices

```
mcp_context7_get-library-docs → mcp_exa-search_get_code_context_exa → compare
```

### Edit & Validate

```
search_replace → read_lints → run_terminal_cmd (test)
```

---

## 💡 Pro Tips

1. **Always combine tools**: Semantic + exact = complete picture
2. **Use grep before read_file**: Find relevant sections first
3. **Cross-reference**: Official docs + community examples
4. **Validate with multiple tools**: Better accuracy

---

**See**: `AI_TOOLS_INVENTORY.md` for detailed documentation
**See**: `TOOLS_USAGE_EXAMPLES.md` for real examples
