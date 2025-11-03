# Custom Cursor Commands

## 📂 Location
Commands must be in `.cursor/commands/` as `.md` files.

## 🚀 Available Commands

- **`/api`** - Generate API endpoint with tests
- **`/component`** - Generate React component
- **`/test`** - Generate comprehensive tests
- **`/optimize`** - Apply M3 Max optimizations
- **`/fix`** - Smart error fixing
- **`/crud`** - Generate full CRUD stack
- **`/refactor`** - Intelligent refactoring

## 💡 Usage

Type `/` in Cursor chat to see all commands.

Examples:
```
/api /users POST
/component UserCard
/test backend/src/services/easypost_service.py
/optimize backend/src/server.py
/fix
/crud Product
/refactor "extract service"
```

## ⚡ M3 Max Optimized

All commands leverage your hardware:
- 16 CPU cores
- 128GB RAM
- Parallel test execution (pytest -n 16)
- Optimized worker counts

## 📋 Context-Aware

All commands automatically read:
- `.dev-config.json` for project specs
- `.cursorrules` for conventions
- Current file context

## ➕ Adding New Commands

Create a new `.md` file in this directory:

```bash
touch .cursor/commands/yourcommand.md
```

Add your prompt with `{{variables}}` for parameters.

## 🔄 Refresh

After adding/modifying commands, **restart Cursor** or reload the window to see changes.
