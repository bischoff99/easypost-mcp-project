# Contributing to EasyPost MCP

## Quick Start

1. **Fork and clone**

```bash
git clone https://github.com/andrejs/easypost-mcp-project.git
cd easypost-mcp-project
```

2. **Install dependencies**

```bash
make install
```

3. **Run tests**

```bash
/test  # or: make test
```

## Development Workflow

### 1. Create a branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make changes

Follow coding standards in `.cursor/rules/`

### 3. Test

```bash
/test                # Run all tests
make test-cov        # With coverage
```

### 4. Format and lint

```bash
make format          # Auto-format code
make lint            # Check linting
```

### 5. Commit

```bash
git commit -m "feat: your feature description"
```

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Maintenance

### 6. Push and create PR

```bash
git push origin feature/your-feature-name
```

## Code Standards

### Python

- snake_case functions
- PascalCase classes
- Type hints required
- Async for I/O operations
- 100 char line length
- Google-style docstrings

## Testing

- Write tests for new features
- Maintain 80%+ coverage (backend)
- Use mocks for external APIs (EasyPost)
- Run `/test` before committing

## Documentation

- Update README for new features
- Add docstrings/JSDoc comments
- Update API docs if endpoints change
- Add examples for complex features

## M3 Max Optimizations

When adding bulk operations:

- Use 16-32 parallel workers
- Use asyncio.gather for concurrency
- Test with `/ep-benchmark`
- Document performance expectations

## Pull Request Process

1. Fill out PR template
2. Link related issues
3. Request review from @andrejs
4. Address review comments
5. Ensure CI passes

## Questions?

See:

- `.cursor/START_HERE.md` - Quick start guide
- `.cursor/COMMANDS.md` - Command reference
- `docs/reviews/CLAUDE.md` - Comprehensive guide
