# Terminal Configuration for Cursor IDE

## Current Configuration

### Default Shell
- **Shell**: zsh
- **Path**: `/bin/zsh`
- **Args**: `-l` (login shell - loads `.zshrc` and environment)

### Terminal Settings

```json
{
  "terminal.integrated.defaultProfile.osx": "zsh",
  "terminal.integrated.profiles.osx": {
    "zsh": {
      "path": "/bin/zsh",
      "args": ["-l"]
    },
    "bash": {
      "path": "/bin/bash",
      "args": ["-l"]
    }
  },
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.fontFamily": "Menlo, Monaco, 'Courier New', monospace",
  "terminal.integrated.cursorBlinking": true,
  "terminal.integrated.cursorStyle": "line",
  "terminal.integrated.scrollback": 10000,
  "terminal.integrated.env.osx": {
    "PYTHONPATH": "${workspaceFolder}/backend"
  }
}
```

## Features Configured

1. **Default Shell**: zsh with login shell arguments
2. **Alternative Shell**: bash available in dropdown
3. **Font**: Monospace fonts for better readability
4. **Cursor**: Blinking line cursor
5. **Scrollback**: 10,000 lines of history
6. **Environment**: PYTHONPATH automatically set to backend directory

## Usage

### Switch Shells
1. Open terminal in Cursor (Ctrl+` or Cmd+`)
2. Click the dropdown next to the `+` icon
3. Select "zsh" or "bash"

### Environment Variables
The terminal automatically sets:
- `PYTHONPATH` to include the backend directory
- Loads your `.zshrc` with the `-l` flag

### Backend Development
When you open a new terminal in Cursor:
```bash
cd backend
source venv/bin/activate  # Python 3.12 virtual environment
python src/server.py       # Start the backend server
```

### Frontend Development
```bash
cd frontend
npm run dev               # Start the frontend dev server
```

## Troubleshooting

### Shell not loading properly
If your shell doesn't load environment variables:
1. Check `.zshrc` exists: `ls -la ~/.zshrc`
2. Test shell manually: `zsh -l`
3. Reload Cursor window: Cmd+Shift+P → "Reload Window"

### PYTHONPATH not set
If Python imports fail:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
```

Or add to `.zshrc`:
```bash
# EasyPost MCP Project
export PYTHONPATH="$HOME/easypost-mcp-project/backend:$PYTHONPATH"
```

## Additional Configuration

### Global Cursor Settings
To apply these settings globally:
1. Cmd+Shift+P → "Open User Settings (JSON)"
2. Add terminal configuration from above

### Per-Project Override
Current settings in `.vscode/settings.json` apply only to this project.
