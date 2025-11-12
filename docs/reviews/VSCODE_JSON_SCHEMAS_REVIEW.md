# VS Code JSON Schema References Review

**Date**: 2025-11-12  
**Reference**: [VS Code JSON Schemas Documentation](https://code.visualstudio.com/docs/languages/json#_json-schemas-and-settings)  
**Goal**: Add schema references to all JSON config files for IntelliSense and validation

---

## Current Status

### ✅ Files with Schema References

1. **`.vscode/tasks.json`** ✅ - Has schema reference
2. **`.prettierrc`** ✅ - Has schema reference

### ⚠️ Files Missing Schema References

1. **`.vscode/settings.json`** - No schema reference
2. **`.vscode/launch.json`** - No schema reference
3. **`.vscode/extensions.json`** - No schema reference
4. **`.vscode/keybindings.json`** - No schema reference
5. **`apps/frontend/tsconfig.json`** - No schema reference

---

## Schema URLs for VS Code Config Files

### Standard VS Code Schemas

| File | Schema URL | Source |
|------|------------|--------|
| `settings.json` | Auto-detected (built-in) | VS Code |
| `launch.json` | Auto-detected (built-in) | VS Code |
| `tasks.json` | `https://raw.githubusercontent.com/microsoft/vscode/main/src/vs/workbench/contrib/tasks/common/tasks.json.schema.json` | VS Code |
| `extensions.json` | `https://raw.githubusercontent.com/microsoft/vscode/main/src/vs/workbench/contrib/extensions/common/extensions.json.schema.json` | VS Code |
| `keybindings.json` | `https://raw.githubusercontent.com/microsoft/vscode/main/src/vs/workbench/services/keybinding/common/keybindingService.json.schema.json` | VS Code |

### External Schemas

| File | Schema URL | Source |
|------|------------|--------|
| `tsconfig.json` | `https://json.schemastore.org/tsconfig.json` | Schema Store |
| `.prettierrc` | `https://json.schemastore.org/prettierrc.json` | Schema Store |

---

## Benefits of Adding Schema References

### 1. **IntelliSense**
- Auto-completion for properties
- Valid values suggestions
- Property descriptions on hover

### 2. **Validation**
- Red squiggles for invalid properties
- Type checking
- Required field validation

### 3. **Documentation**
- Hover descriptions for properties
- Examples in IntelliSense
- Schema-based help

### 4. **Error Prevention**
- Catch typos early
- Prevent invalid configurations
- Ensure correct structure

---

## Implementation Plan

### Files to Update

1. **`.vscode/launch.json`**
   - Add debug configuration schema
   - Benefits: Better IntelliSense for debug configs

2. **`.vscode/extensions.json`**
   - Add extensions schema
   - Benefits: Validate extension IDs

3. **`.vscode/keybindings.json`**
   - Add keybindings schema
   - Benefits: Validate key combinations

4. **`apps/frontend/tsconfig.json`**
   - Add TypeScript config schema
   - Benefits: Validate compiler options

5. **`.vscode/settings.json`**
   - Note: Auto-detected, but can add explicit reference
   - Benefits: Explicit schema for offline mode

---

## Schema Reference Format

According to [VS Code documentation](https://code.visualstudio.com/docs/languages/json#_json-schemas-and-settings), add `$schema` at the top of JSON files:

```json
{
  "$schema": "https://schema-url-here",
  ...
}
```

**Note**: For JSON with Comments (jsonc) files like `settings.json`, `tasks.json`, and `launch.json`, VS Code automatically uses jsonc mode and supports comments.

---

## Best Practices

### ✅ DO
- Add `$schema` attribute for explicit schema reference
- Use official schema URLs from Schema Store or VS Code
- Keep schema references up to date
- Use jsonc mode for config files (supports comments)

### ❌ DON'T
- Add `$schema` if it breaks JSON consumers (check first)
- Use deprecated schema URLs
- Add schemas to files that don't benefit (e.g., data files)

---

## Files Analysis

### `.vscode/settings.json`

**Current**: No schema reference  
**Status**: Auto-detected by VS Code  
**Recommendation**: Optional - can add explicit reference for offline mode

**Schema**: Built-in (no explicit URL needed, but can use):
```json
{
  "$schema": "https://raw.githubusercontent.com/microsoft/vscode/main/src/schemas/json/settings.schema.json",
  ...
}
```

### `.vscode/launch.json`

**Current**: No schema reference  
**Status**: Auto-detected by VS Code  
**Recommendation**: ✅ **Add explicit schema**

**Schema**:
```json
{
  "$schema": "https://raw.githubusercontent.com/microsoft/vscode/main/src/schemas/json/launch.schema.json",
  ...
}
```

### `.vscode/extensions.json`

**Current**: No schema reference  
**Status**: Auto-detected by VS Code  
**Recommendation**: ✅ **Add explicit schema**

**Schema**:
```json
{
  "$schema": "https://raw.githubusercontent.com/microsoft/vscode/main/src/schemas/json/extensions.schema.json",
  ...
}
```

### `.vscode/keybindings.json`

**Current**: No schema reference  
**Status**: Auto-detected by VS Code  
**Recommendation**: ✅ **Add explicit schema**

**Schema**:
```json
[
  {
    "$schema": "https://raw.githubusercontent.com/microsoft/vscode/main/src/schemas/json/keybindings.schema.json",
    ...
  }
]
```

**Note**: Keybindings is an array, so schema reference goes in first object or as comment.

### `apps/frontend/tsconfig.json`

**Current**: No schema reference  
**Status**: Auto-detected by VS Code  
**Recommendation**: ✅ **Add explicit schema**

**Schema**:
```json
{
  "$schema": "https://json.schemastore.org/tsconfig.json",
  ...
}
```

---

## Implementation Notes

### Keybindings.json Special Case

Keybindings.json is an **array**, not an object. Schema reference can be added as:
1. Comment at top (recommended)
2. First object property (if schema supports it)

**Recommended approach**: Use comment since it's an array:
```json
// Schema: https://raw.githubusercontent.com/microsoft/vscode/main/src/schemas/json/keybindings.schema.json
[
  {
    "key": "...",
    ...
  }
]
```

---

## References

- [VS Code JSON Schemas Documentation](https://code.visualstudio.com/docs/languages/json#_json-schemas-and-settings)
- [JSON Schema Store](https://www.schemastore.org/json/)
- [VS Code Settings Schema](https://raw.githubusercontent.com/microsoft/vscode/main/src/schemas/json/settings.schema.json)
- [VS Code Launch Schema](https://raw.githubusercontent.com/microsoft/vscode/main/src/schemas/json/launch.schema.json)
- [TypeScript Config Schema](https://json.schemastore.org/tsconfig.json)

---

**Reviewer**: AI Assistant (Claude)  
**Date**: 2025-11-12  
**Status**: Ready for implementation

