# Cursor IDE Prompts

This directory is reserved for Cursor-specific prompts to enhance IDE interactions.

## Status

**Currently**: Placeholder directory (prompts defined in rules and commands instead)

## Purpose

Cursor-specific prompts are distinct from MCP prompts:
- **Cursor Prompts** (this directory): IDE behavior enhancement (future use)
- **MCP Prompts**: Server-side AI agent prompts in `backend/src/mcp_server/prompts/`

## Current Approach

Project uses:
1. **Cursor Rules** (`.cursor/rules/`) - Comprehensive coding standards
2. **Cursor Commands** (`.cursor/commands/`) - Slash command templates
3. **MCP Prompts** (`backend/src/mcp_server/prompts/`) - AI agent workflows

## Future

This directory can be populated with:
- Custom code generation prompts
- Refactoring workflow prompts  
- Documentation generation templates
- Debugging assistance prompts

## Related

- **MCP Prompts**: `backend/src/mcp_server/prompts/` (shipping, optimization, tracking)
- **Cursor Rules**: `.cursor/rules/` (auto-applied coding standards)
- **Cursor Commands**: `.cursor/commands/` (slash command templates)
