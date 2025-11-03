---
name: clear
category: session
description: Reset conversation context to start fresh
allowed-tools: []
requires-approval: false
context-aware: false
arguments: []
estimated-time: <1s
estimated-tokens: 0
version: 2.0
---

# /session:clear

Reset the conversation context to start with a clean slate. Useful between unrelated tasks to save tokens and improve AI focus.

## Usage

```bash
/session:clear
```

## When to Use

- **Between major tasks**: Switching from backend to frontend work
- **Context pollution**: Too much irrelevant history affecting responses
- **Token optimization**: Fresh start uses fewer tokens
- **Privacy**: Clear sensitive information from context

## What Gets Cleared

- ✅ Conversation history
- ✅ Cached file references
- ✅ Previous command outputs
- ❌ Your `.dev-config.json` settings (preserved)
- ❌ Open files in editor (preserved)

## Industry Standard

**Source**: Claude Code, GitHub Copilot
- Both provide `/clear` for context management
- Recommended every 10-15 interactions for optimal performance

## Example Workflow

```bash
# Working on authentication
/gen:api /auth/login POST
/test:run backend/tests/test_auth.py
# ... more auth work ...

# Now switching to UI work - clear context
/session:clear

# Start fresh with frontend
/gen:component LoginForm
/test:run frontend/src/components/
```

## Alternative: Partial Clear

If you want to keep some context:
```bash
/session:compact "Keep only authentication-related code and test results"
```

## Performance

- **Time**: Instant (<1s)
- **Tokens**: 0 (no API call)
- **Effect**: Next command starts with minimal context

## Tips

1. **Use before major context switches** - backend → frontend, feature A → feature B
2. **Check token usage first** - Run `/session:cost` to see if clear is needed
3. **Save important info** - Use `/session:checkpoint` before clearing if you might need to resume
4. **Don't overuse** - Context can be helpful; clear only when truly needed

