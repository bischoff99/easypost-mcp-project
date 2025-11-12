<<<<<<< HEAD
# Cursor IDE Configuration

This directory contains configuration files and rules for Cursor IDE integration with this project.

## Directory Structure

```
.cursor/
├── mcp.json              # MCP server configuration for EasyPost integration
├── rules/                # Comprehensive coding standards and best practices
│   ├── 00-INDEX.mdc      # Rules index and quick reference
│   ├── 01-fastapi-python.mdc    # Backend Python/FastAPI standards
│   ├── 02-react-vite-frontend.mdc # Frontend React/Vite standards
│   ├── 03-testing-best-practices.mdc # Testing strategy
│   ├── 04-mcp-development.mdc   # MCP tool development patterns
│   ├── 05-m3-max-optimizations.mdc # Hardware-specific optimizations
│   ├── 06-quick-reference.mdc   # Quick templates and patterns
│   └── 07-learned-memories.mdc   # Project-specific knowledge and preferences
├── commands/             # Custom Cursor commands
│   ├── project-specific/ # Project-specific workflows
│   └── universal/       # Reusable commands
└── archive/              # Archived/old configurations
```

## MCP Server Configuration

**File**: `.cursor/mcp.json`

Configures the EasyPost MCP server for Cursor Desktop integration. The server provides AI agent tools for:
- Creating shipments
- Getting shipping rates
- Tracking shipments
- Bulk operations

**Entry Point**: `apps/backend/src/mcp_server/server.py`

**Environment Variables Required**:
- `EASYPOST_API_KEY` - Your EasyPost API key (test or production)

## Rules System

The `.cursor/rules/` directory contains comprehensive coding standards:

### 00-INDEX.mdc
Complete index of all rules with quick reference.

### 01-fastapi-python.mdc
Backend development standards:
- Functional programming patterns
- Type hints & Pydantic v2 validation
- Async/await patterns
- SQLAlchemy 2.0 async patterns
- Error handling
- Performance optimization

### 02-react-vite-frontend.mdc
Frontend development standards:
- Functional components with hooks
- State management (Zustand, React Query)
- TailwindCSS best practices
- Form handling
- Testing patterns

### 03-testing-best-practices.mdc
Testing strategy:
- Backend: pytest with parallel execution
- Frontend: vitest + React Testing Library
- AAA pattern (Arrange, Act, Assert)
- Coverage requirements (36% backend, 70% frontend)

### 04-mcp-development.mdc
MCP tool development:
- FastMCP server patterns
- Tool design for AI agents
- Batch operations
- Error handling for AI consumption
- 100% coverage requirement for tools

### 05-m3-max-optimizations.mdc
Hardware-specific optimizations:
- Leverage 16 CPU cores
- Parallel processing patterns
- Connection pooling
- Build optimizations

### 06-quick-reference.mdc
Quick templates and patterns (always applied).

### 07-learned-memories.mdc
Project-specific knowledge and preferences (always applied):
- Project-specific patterns and conventions
- User preferences and coding style choices
- Technical decisions and their rationale
- Recurring issues and solutions

## Commands

Custom Cursor commands are located in `.cursor/commands/`:
- **Project-specific**: EasyPost-specific workflows
- **Universal**: Reusable commands for any project

## Configuration Files

- **`.cursorignore`**: Files/directories to exclude from Cursor context
- **`.cursorrules`**: Core repository principles and anti-patterns

## Usage

Cursor IDE automatically loads these configurations when opening the project. The rules are applied contextually based on file types and project structure.

## Maintenance

- Rules are version-controlled and should be updated as patterns evolve
- MCP configuration should be updated if server entry point changes
- Commands can be added/modified based on common workflows

## Related Documentation

- `CLAUDE.md` - Comprehensive project overview for AI assistants
- `docs/guides/` - Development guides
- `README.md` - Project README
||||||| 7a576da
=======
# Cursor IDE Configuration

This directory contains configuration files and rules for Cursor IDE integration with this project.

## Directory Structure

```
.cursor/
├── mcp.json              # MCP server configuration for EasyPost integration
├── rules/                # Comprehensive coding standards and best practices
│   ├── 00-INDEX.mdc      # Rules index and quick reference
│   ├── 01-fastapi-python.mdc    # Backend Python/FastAPI standards
│   ├── 02-react-vite-frontend.mdc # Frontend React/Vite standards
│   ├── 03-testing-best-practices.mdc # Testing strategy
│   ├── 04-mcp-development.mdc   # MCP tool development patterns
│   ├── 05-m3-max-optimizations.mdc # Hardware-specific optimizations
│   └── 06-quick-reference.mdc   # Quick templates and patterns
├── commands/             # Custom Cursor commands
│   ├── project-specific/ # Project-specific workflows
│   └── universal/       # Reusable commands
└── archive/              # Archived/old configurations
```

## MCP Server Configuration

**File**: `.cursor/mcp.json`

Configures the EasyPost MCP server for Cursor Desktop integration. The server provides AI agent tools for:
- Creating shipments
- Getting shipping rates
- Tracking shipments
- Bulk operations

**Entry Point**: `apps/backend/src/mcp_server/server.py`

**Environment Variables Required**:
- `EASYPOST_API_KEY` - Your EasyPost API key (test or production)

## Rules System

The `.cursor/rules/` directory contains comprehensive coding standards:

### 00-INDEX.mdc
Complete index of all rules with quick reference.

### 01-fastapi-python.mdc
Backend development standards:
- Functional programming patterns
- Type hints & Pydantic v2 validation
- Async/await patterns
- SQLAlchemy 2.0 async patterns
- Error handling
- Performance optimization

### 02-react-vite-frontend.mdc
Frontend development standards:
- Functional components with hooks
- State management (Zustand, React Query)
- TailwindCSS best practices
- Form handling
- Testing patterns

### 03-testing-best-practices.mdc
Testing strategy:
- Backend: pytest with parallel execution
- Frontend: vitest + React Testing Library
- AAA pattern (Arrange, Act, Assert)
- Coverage requirements (36% backend, 70% frontend)

### 04-mcp-development.mdc
MCP tool development:
- FastMCP server patterns
- Tool design for AI agents
- Batch operations
- Error handling for AI consumption
- 100% coverage requirement for tools

### 05-m3-max-optimizations.mdc
Hardware-specific optimizations:
- Leverage 16 CPU cores
- Parallel processing patterns
- Connection pooling
- Build optimizations

### 06-quick-reference.mdc
Quick templates and patterns (always applied).

## Commands

Custom Cursor commands are located in `.cursor/commands/`:
- **Project-specific**: EasyPost-specific workflows
- **Universal**: Reusable commands for any project

## Configuration Files

- **`.cursorignore`**: Files/directories to exclude from Cursor context
- **`.cursorrules`**: Core repository principles and anti-patterns

## Usage

Cursor IDE automatically loads these configurations when opening the project. The rules are applied contextually based on file types and project structure.

## Maintenance

- Rules are version-controlled and should be updated as patterns evolve
- MCP configuration should be updated if server entry point changes
- Commands can be added/modified based on common workflows

## Related Documentation

- `CLAUDE.md` - Comprehensive project overview for AI assistants
- `docs/guides/` - Development guides
- `README.md` - Project README
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8
