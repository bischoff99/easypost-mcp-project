# Cursor IDE Prompts

This directory contains Cursor-specific prompts for enhanced IDE interactions.

## Structure

```
.cursor/prompts/
├── README.md                  # This file
├── code-generation/           # Prompts for generating code
├── refactoring/              # Prompts for refactoring tasks
├── documentation/            # Prompts for generating docs
└── debugging/                # Prompts for debugging assistance
```

## Usage

These prompts are separate from MCP prompts (located in `backend/src/mcp/prompts/`):
- **Cursor Prompts**: IDE-specific, enhance Cursor AI behavior
- **MCP Prompts**: Server-side, used by MCP tools/clients

## Adding New Prompts

1. Create a new `.md` file in the appropriate subdirectory
2. Use clear, descriptive names
3. Include context and examples
4. Test with Cursor AI before committing

## Related

- MCP Prompts: `backend/src/mcp/prompts/`
- Cursor Rules: `.cursor/rules/`
- Cursor Commands: `.cursor/commands/`
