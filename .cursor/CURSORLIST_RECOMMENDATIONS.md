# CursorList Recommendations for EasyPost MCP Project

Source: https://cursorlist.com

## Overview

This document outlines specific cursor rules from CursorList that can enhance the EasyPost MCP project.

## Applicable Rule Categories

### 1. Python Backend Rules ⭐⭐⭐

**Relevance**: High - Core backend is Python 3.12 with FastAPI/FastMCP

**Key Patterns to Adopt**:
- Type hints everywhere (already implemented ✓)
- Async/await best practices
- Pydantic models for validation (already using ✓)
- Error handling patterns
- Testing strategies

**From CursorList General Pattern**:
```
- Cut the fluff. Code or detailed explanations only.
- Don't be lazy - write all the code to implement features
- For code tweaks, show minimal context - a few lines around changes max
- Anticipate needs and suggest solutions I didn't think about
```

### 2. React + Vite Rules ⭐⭐⭐

**Relevance**: High - Frontend is React 18 with Vite

**Key Additions from CursorList**:
```javascript
// Performance Optimization
- Use React.memo, useMemo, useCallback for expensive operations
- Implement code splitting and lazy loading
- Use Vite's dynamic imports for routes
- Implement skeleton screens for loading states

// Component Patterns
- One component per file
- Custom hooks for reusable logic
- Error boundaries (already added ✓)
- Proper loading states
```

**Example Pattern**:
```jsx
// Custom hook pattern
function useShipment(shipmentId) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    fetchShipment(shipmentId)
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [shipmentId]);
  
  return { data, loading, error };
}
```

### 3. JavaScript/TypeScript Best Practices ⭐⭐

**Relevance**: Medium - Using vanilla JS but could benefit from TS patterns

**Key Takeaways**:
```
- Write concise, technical code with accurate examples
- Use modern JavaScript features (ES6+)
- Prefer functional programming patterns
- Descriptive variable names
- Focus on readability over performance (unless critical)
- Fully implement all requested functionality - no TODOs
```

**Consider Adding**:
- JSDoc comments for type safety
- More functional patterns (map, filter, reduce)
- Immutable data patterns

### 4. Node.js/Vite Configuration ⭐⭐

**Relevance**: Medium - Frontend build process

**From CursorList Node.js patterns**:
```
- Use latest Node.js LTS features
- Implement proper error handling in async operations
- Use environment variables consistently
- Optimize build configurations
```

**Vite-Specific**:
```javascript
// vite.config.js enhancements
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
        }
      }
    }
  },
  optimizeDeps: {
    include: ['axios', 'zustand']
  }
});
```

### 5. Chrome Extension Patterns ⭐

**Relevance**: Low - But message passing patterns could apply to MCP

**Interesting Patterns for MCP**:
- Message passing architecture (similar to MCP stdio)
- State management with chrome.storage (like MCP resources)
- Event-driven architecture

### 6. Tailwind CSS Rules ⭐

**Relevance**: Low-Medium - Currently using vanilla CSS

**Consider Adding**:
- Utility-first CSS approach
- Responsive design utilities
- Consistent spacing system

**Current Setup**: Using vanilla CSS - could enhance with Tailwind if desired

## Specific Improvements to Implement

### Backend Enhancement Checklist

- [x] Type hints on all functions (completed)
- [x] Pydantic models for validation (completed)
- [x] Standardized error responses (completed)
- [x] ThreadPoolExecutor for async wrappers (completed)
- [ ] Retry logic with exponential backoff for EasyPost API
- [ ] Request timeout configuration
- [ ] More comprehensive error logging
- [ ] Integration tests for MCP tools

### Frontend Enhancement Checklist

- [x] Error boundaries (completed)
- [ ] Custom hooks for shipment/tracking operations
- [ ] Loading skeleton screens
- [ ] Code splitting for routes
- [ ] Optimized re-renders with React.memo
- [ ] Form validation with react-hook-form (optional)
- [ ] Better error message display
- [ ] Responsive design improvements

### Testing Enhancement Checklist

- [x] Basic unit tests (9 tests passing)
- [ ] Integration tests for full workflows
- [ ] Frontend component tests with React Testing Library
- [ ] E2E tests with Playwright (optional)
- [ ] API mocking with MSW (Mock Service Worker)
- [ ] Load testing for backend endpoints

## Code Style Improvements

### From CursorList - "Brief Response" Pattern

**Apply to All Code**:
```
When showing code changes:
1. Show 2-3 lines before change
2. Show the actual change
3. Show 2-3 lines after change
4. Don't repeat entire file unless necessary
```

**Example**:
```python
# Instead of showing entire file, show:

    # ... existing code ...
    
    def get_rates(self, to_address, from_address, parcel):
-       return self._get_rates_sync(to_address, from_address, parcel)
+       rates = await self._get_rates_with_retry(to_address, from_address, parcel)
+       return {"status": "success", "data": rates}
    
    # ... rest of method ...
```

### Error Response Pattern from CursorList

**Standardize on**:
```python
from datetime import datetime

def create_error_response(message: str, data: Any = None) -> dict:
    return {
        "status": "error",
        "data": data,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
```

## AI Assistant Behavior Rules

From CursorList, apply these AI guidelines:

### Communication Style
```
✓ Cut the fluff - code or explanations only
✓ Answer first, explain later if needed
✓ Accuracy and depth matter
✓ Treat user as expert - skip obvious explanations
✓ Suggest solutions user didn't think about
✓ If uncertain, say so instead of guessing
✗ Don't repeat code unnecessarily
✗ No high-level suggestions without code
✗ No placeholders or TODOs
```

### Code Output Rules
```
✓ Write complete, working code
✓ Include all necessary imports
✓ Show minimal context for changes
✓ Provide brief comments for significant changes
✗ Don't output partial implementations
✗ Don't say "here's how you can..." - just do it
✗ Don't leave TODOs or placeholders
```

## Recommended Cursor Rules Update

**Create Enhanced .cursorrules**:

1. Keep existing project-specific rules
2. Add CursorList communication patterns
3. Add performance optimization guidelines
4. Add testing requirements
5. Add code review checklist

**File**: `.cursorrules_enhanced` (created above)

**To Apply**:
```bash
cd /Users/andrejs/easypost-mcp-project
cp .cursorrules .cursorrules.backup
cp .cursorrules_enhanced .cursorrules
```

## Rules NOT Applicable

### Skip These from CursorList:

1. **Solidity/Web3 Rules** - Not using blockchain
2. **Chrome Extension Rules** - Not building extensions
3. **SwiftUI Rules** - Not iOS development
4. **Angular Rules** - Using React
5. **Django Rules** - Using FastAPI
6. **SvelteKit Rules** - Using React

## Implementation Priority

### High Priority (Do Now)
1. ✅ Enhanced .cursorrules with CursorList patterns
2. ⚠️ Custom hooks for frontend (useShipment, useTracking)
3. ⚠️ Loading skeleton screens
4. ⚠️ Retry logic for EasyPost API calls

### Medium Priority (Next Sprint)
1. Code splitting for routes
2. React.memo optimization
3. Integration tests
4. Better error messages

### Low Priority (Nice to Have)
1. Tailwind CSS migration
2. TypeScript migration
3. E2E tests
4. Performance monitoring

## Resources

- **CursorList**: https://cursorlist.com
- **FastMCP Docs**: https://gofastmcp.com
- **React Patterns**: https://reactpatterns.com
- **Python Best Practices**: https://docs.python-guide.org

## Summary

The most valuable patterns from CursorList for this project:

1. ✅ **Communication Style**: Brief, code-first responses
2. ✅ **Type Safety**: Type hints everywhere (Python) + JSDoc (JS)
3. ⚠️ **Performance**: React optimization patterns needed
4. ⚠️ **Error Handling**: Standardized across backend/frontend
5. ⚠️ **Testing**: More comprehensive test coverage needed

**Next Step**: Apply enhanced .cursorrules and implement high-priority frontend improvements.
