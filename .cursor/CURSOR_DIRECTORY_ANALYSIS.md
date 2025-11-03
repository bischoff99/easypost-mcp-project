# Cursor.Directory Analysis for EasyPost MCP Project

Source: https://cursor.directory

## Overview

Cursor.directory is a community platform (61.7k+ members) with:
- Curated cursor rules/templates
- MCP server directory (Featured MCPs)
- Job board for Cursor-focused positions
- Community board for news and updates
- Rule generator

## Key Differences: cursor.directory vs CursorList

| Feature | cursor.directory | CursorList |
|---------|-----------------|------------|
| **Focus** | Community + Rules + MCPs | Pure rules repository |
| **MCP Servers** | ✅ Featured MCP directory | ❌ Not included |
| **Community** | ✅ 61.7k members, board | ❌ Just rules |
| **Jobs** | ✅ Cursor-specific jobs | ❌ None |
| **Generator** | ✅ Rule generator tool | ❌ Manual only |
| **Format** | Interactive, searchable | Static list |

**Winner for this project**: cursor.directory - has MCP examples and community

## Most Relevant Sections

### 1. Featured MCP Servers ⭐⭐⭐⭐⭐

**Critical for learning MCP best practices**

Featured MCPs shown:
- **Postman** - API testing integration
- **Mailtrap Email Sending** - Email service MCP
- **Midday** - Unknown (finance/time tracking?)
- **Peekaboo** - Unknown
- **Postmark MCP** - Transactional email
- **Agent Evals by Galileo** - AI agent evaluation
- **GibsonAI** - Unknown

**Why this matters**:
- See how other teams structure MCP servers
- Learn naming conventions for tools
- Understand real-world MCP patterns
- Get inspiration for tool descriptions

**Action**: Explore these MCP servers to improve our EasyPost MCP implementation

### 2. Python + FastAPI Rules ⭐⭐⭐⭐

**Directly applicable to backend**

Rules available:
```
"You are an expert in Python, FastAPI, and scalable API development..."
- FastAPI Python Cursor Rules
- FastAPI Python Microservices Serverless Cursor Rules
- Django Python Cursor Rules (if we consider switching)
```

**Key patterns**:
- FastAPI best practices
- Microservices architecture
- Async/await patterns
- API scalability

**Relevant for**:
- `backend/src/server.py`
- `backend/src/services/easypost_service.py`
- FastAPI/FastMCP integration patterns

### 3. React + JavaScript Rules ⭐⭐⭐⭐

**Directly applicable to frontend**

Available rules:
```
"You are an expert in JavaScript, React, Node.js, Next.js..."
- Next.js React Standard.js Cursor Rules
- Next.js React Generalist Cursor Rules
- React Three Fiber Rules (not relevant)
```

**Patterns for our React/Vite app**:
- Component structure
- State management (Zustand mentioned)
- Error handling
- Loading states
- API integration

### 4. TypeScript Rules ⭐⭐⭐

**Future migration consideration**

Top TypeScript rules:
```
"You are an expert in TypeScript, Node.js, Next.js App Router, React..."
- Next.js React TypeScript Cursor Rules
- Expo React Native TypeScript Cursor Rules
- Modern Web Development (TypeScript focus)
```

**If we migrate to TypeScript**:
- Type safety for API responses
- Better IDE support
- Fewer runtime errors
- Better documentation through types

**Current status**: Using vanilla JS, but TS migration could help

### 5. Chrome Extension Rules ⭐

**Interesting parallels to MCP**

Not directly applicable but architectural patterns overlap:
```
- Message passing (like MCP stdio)
- Background scripts (like MCP server)
- Content scripts (like MCP tools)
- State management (like MCP resources)
```

## Unique Advantages of cursor.directory

### 1. MCP Server Examples

**No other platform has this** - can browse real MCP implementations:
- See tool naming conventions
- Understand description patterns
- Learn error handling approaches
- Get inspiration for features

**TODO**: Browse these MCP servers and document patterns

### 2. Community Board

61.7k+ members sharing:
- Tips and tricks
- Implementation patterns
- Problem solutions
- New MCP ideas

**Recent posts visible**:
- "Publish your AI tool" - API tool directory
- "7 Cursor Tricks for Rock-Solid API Loops" - API patterns
- "A New Imperative for Developer-facing UIs" - MCP design philosophy

### 3. Rule Generator

Interactive tool to generate custom cursor rules based on your stack.

**Our stack input**:
```
- Python 3.12
- FastAPI
- FastMCP
- React 18
- Vite
- Axios
- Zustand
```

**Output**: Custom cursor rules tailored to exact tech stack

### 4. Job Board

Cursor-focused companies hiring:
- Speakeasy - Product Engineer (API infrastructure)
- Cursor - Community role
- Mixedbread - AI Software Engineer
- Shortwave - Staff AI Agent Engineer ($215k-$275k)

**Insight**: Shows where Cursor skills are valuable

## Specific Rules to Import

### Python FastAPI Rule (Most Relevant)

From cursor.directory Python section:
```
"You are an expert in Python, FastAPI, and scalable API development.

Key Principles:
- Write concise, technical responses with accurate Python examples
- Use functional, declarative programming; avoid classes where possible
- Prefer iteration and modularization over code duplication
- Use descriptive variable names with auxiliary verbs (e.g., is_active, has_permission)
- Use lowercase with underscores for directories and files (e.g. routers/user_routes.py)
- Favor named exports for routes and utility functions
- Use the Receive, Process, Send pattern for request handling

FastAPI Specific:
- Use def for synchronous operations, async def for asynchronous
- Use Pydantic models for request/response validation
- Implement proper error handling with HTTPException
- Use dependency injection for shared logic
- Implement proper logging throughout the application
```

**Apply to**: All backend code

### React JavaScript Rule (Frontend)

From cursor.directory React section:
```
"You are an expert in JavaScript, React, Node.js, Next.js App Router...

Key Principles:
- Write concise, technical JavaScript code with accurate examples
- Use functional and declarative programming patterns; avoid classes
- Prefer iteration and modularization over code duplication
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError)
- Structure files: exported component, subcomponents, helpers, static content, types

React Best Practices:
- Use functional components with hooks (useState, useEffect, useContext)
- Implement proper error boundaries
- Use Suspense for code splitting
- Optimize performance with memo, useMemo, useCallback
- Use custom hooks for reusable logic
```

**Apply to**: Frontend components

## Recommended Actions

### Immediate (High Priority)

1. **Explore Featured MCP Servers**
   - Browse 5-7 featured MCPs
   - Document their tool structures
   - Note naming conventions
   - Identify common patterns

2. **Import FastAPI Python Rules**
   - Add to `.cursorrules`
   - Focus on FastAPI-specific patterns
   - Integrate with existing MCP patterns

3. **Import React JavaScript Rules**
   - Add to `.cursorrules`
   - Focus on hooks and performance
   - Integrate with Vite-specific patterns

4. **Join Community Board**
   - Follow MCP-related discussions
   - Learn from others building MCP servers
   - Share our EasyPost MCP when ready

### Medium Priority

5. **Use Rule Generator**
   - Input our exact tech stack
   - Generate custom rules
   - Merge with existing `.cursorrules`

6. **Review Python FastAPI Microservices Rules**
   - If we need to scale beyond single server
   - Learn microservices patterns
   - Understand distributed MCP architectures

7. **Consider TypeScript Migration**
   - Review TypeScript rules
   - Evaluate benefits for our project
   - Plan migration path if worthwhile

### Low Priority

8. **Monitor Job Board**
   - See what MCP skills are valued
   - Understand market demand
   - Keep resume/skills current

9. **Contribute to Community**
   - Share EasyPost MCP patterns
   - Write about FastMCP + EasyPost integration
   - Help others building shipping/logistics tools

## MCP Server Pattern Analysis

### Common MCP Tool Naming Conventions

From featured MCPs, likely patterns:
```
Postman MCP:
- send_request
- create_collection
- run_tests

Postmark MCP:
- send_email
- send_template_email
- get_delivery_stats

Mailtrap MCP:
- send_test_email
- verify_email
- check_inbox
```

**Our EasyPost MCP** (already good ✓):
```
- create_shipment
- get_tracking
- get_rates
```

**Pattern**: Verb + noun format, clear action names

### MCP Tool Description Patterns

Likely format from other MCPs:
```
"Create a new [resource] and [action]"
"Get [data] for [context]"
"Update [resource] with [details]"
```

**Our current descriptions** (already good ✓):
```
- "Create a new shipment and purchase a label"
- "Get real-time tracking information for a shipment"
- "Get available shipping rates from multiple carriers"
```

### MCP Error Handling Patterns

Based on MCP best practices:
```python
@mcp.tool()
async def tool_name(param: str) -> dict:
    """Tool description"""
    try:
        # Validation
        if not param:
            return {
                "status": "error",
                "message": "Parameter required",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Operation
        result = await operation(param)
        
        # Success response
        return {
            "status": "success",
            "data": result,
            "message": "Operation successful",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        # Error response
        return {
            "status": "error",
            "message": "Operation failed",
            "timestamp": datetime.utcnow().isoformat()
        }
```

**We already follow this pattern** ✓

## Comparison: cursor.directory vs CursorList

### What cursor.directory Has That CursorList Doesn't

1. **MCP Server Directory** - Critical for our project
2. **Community Features** - Learn from others
3. **Interactive Search** - Better discovery
4. **Rule Generator** - Custom rule creation
5. **Job Board** - Career opportunities
6. **Trending Section** - Latest tips and tricks

### What CursorList Has That cursor.directory Doesn't

1. **More Rules** - Larger repository (appears to have more variety)
2. **Simpler Layout** - Easier to browse all rules
3. **Direct Rule Text** - Copy-paste ready
4. **No Account Needed** - Immediate access

### Which to Use?

**For MCP Development**: cursor.directory (has MCP examples)
**For Rule Browsing**: CursorList (simpler, more rules)
**For Community**: cursor.directory (61.7k members)
**For Quick Reference**: CursorList (faster to scan)

**Recommendation**: Use BOTH
- cursor.directory for MCP-specific learning
- CursorList for general cursor rules

## Integration with Our Project

### Current `.cursorrules` Status

✅ **Already have**:
- Python type hints
- Pydantic validation
- FastAPI patterns
- React component structure
- Error handling standards
- API response format

⚠️ **Missing from cursor.directory**:
- FastAPI-specific dependency injection
- React performance optimization patterns
- MCP-specific tool design guidelines
- Async/await best practices for FastAPI
- Custom hook patterns for React

### Proposed `.cursorrules` Enhancement

Merge patterns from:
1. CursorList (general patterns) ✓ Done
2. cursor.directory (FastAPI + React specific)
3. MCP examples (tool design patterns)

## Action Items Checklist

### Research Phase
- [ ] Browse 5 featured MCP servers on cursor.directory
- [ ] Document tool naming patterns
- [ ] Note error handling approaches
- [ ] Identify resource URI patterns
- [ ] Study tool description formats

### Implementation Phase
- [ ] Import FastAPI Python rules from cursor.directory
- [ ] Import React JavaScript rules
- [ ] Update `.cursorrules` with MCP patterns
- [ ] Test rule generator with our stack
- [ ] Join community board

### Community Phase
- [ ] Share EasyPost MCP on cursor.directory
- [ ] Post implementation learnings
- [ ] Help others with FastMCP questions
- [ ] Monitor for new MCP patterns

## Key Takeaways

1. **cursor.directory is essential for MCP development** - has actual MCP examples
2. **Community is valuable** - 61.7k members sharing knowledge
3. **Rule generator could save time** - custom rules for exact stack
4. **MCP patterns are emerging** - follow community for best practices
5. **Job market values MCP skills** - cursor.directory shows demand

## Resources

- **cursor.directory**: https://cursor.directory
- **CursorList**: https://cursorlist.com (complementary)
- **FastMCP Docs**: https://gofastmcp.com
- **MCP Specification**: Check community board for links

## Next Steps

**Immediate**:
1. Explore featured MCPs (30 min)
2. Import FastAPI rules (15 min)
3. Join community (5 min)

**This Week**:
1. Generate custom rules with our stack
2. Update `.cursorrules` with learnings
3. Test improved rules in Cursor

**Ongoing**:
1. Monitor community board weekly
2. Share our MCP patterns
3. Stay updated on MCP best practices

---

**Summary**: cursor.directory is MORE valuable than CursorList for MCP development due to:
- Featured MCP servers (learn from examples)
- Active community (61.7k members)
- Rule generator (custom rules)
- MCP-specific discussions

Use cursor.directory as primary resource, CursorList as supplement.
