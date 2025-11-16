# Project Setup Review Report

**Date**: 2025-01-17
**Project**: EasyPost MCP Project
**Review Type**: Comprehensive Setup Analysis
**Status**: ✅ Complete

---

## Executive Summary

This comprehensive review analyzed the EasyPost MCP project setup across 11 phases, examining project structure, dependencies, environment configuration, source code organization, testing, MCP architecture, scripts, documentation, deployment, security, and quality assurance.

**Overall Assessment**: **A- (Excellent with minor improvements)**

The project demonstrates excellent organization and best practices, with a clear focus on personal use (YAGNI principle). The setup is well-structured, documented, and follows modern Python development patterns. Minor improvements are recommended for consistency and optimization.

### Key Strengths

- ✅ Clean, well-organized project structure
- ✅ Comprehensive MCP server architecture
- ✅ Excellent security practices (Keychain integration)
- ✅ Modern tooling (Ruff, FastMCP, FastAPI)
- ✅ Good test coverage and organization
- ✅ Clear documentation and guides

### Areas for Improvement

- ⚠️ Python version mismatch (requirements vs actual)
- ⚠️ FastMCP best practices alignment (tags, error handling)
- ⚠️ Some configuration inconsistencies
- ⚠️ Minor documentation gaps

---

## Phase 1: Project Foundation

### 1.1 Project Structure Analysis

**Status**: ✅ **Excellent**

```
easypost-mcp-project/
├── src/                          # Source code (41 Python files)
│   ├── mcp_server/              # MCP server (core product)
│   │   ├── tools/               # 10 tool modules (4903 lines)
│   │   ├── resources/           # Resource providers
│   │   ├── prompts/             # Prompt templates
│   │   ├── __init__.py          # Server initialization
│   │   └── server.py            # Standalone entrypoint
│   ├── routers/                 # FastAPI endpoints
│   ├── services/                # Business logic
│   ├── models/                  # Pydantic models
│   └── utils/                   # Utilities
├── tests/                        # Test suite (33 Python files)
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   ├── mcp/                     # MCP-specific tests
│   └── routers/                 # Router tests
├── config/                       # Configuration files
├── scripts/                      # Utility scripts
├── docs/                         # Documentation
├── deploy/                       # Deployment configs
└── universal/                    # Review/reference docs
```

**Findings**:

- ✅ Clear separation of concerns
- ✅ Well-organized MCP server structure
- ✅ Logical test organization
- ✅ All major directories properly structured

**Recommendations**:

- ✅ Structure is excellent, no changes needed

---

### 1.2 Core Configuration Files

**Status**: ✅ **Good** (with minor issues)

#### `config/pyproject.toml`

**Findings**:

- ✅ Comprehensive Ruff configuration
- ✅ Strict mypy type checking
- ✅ Good per-file ignores for tests
- ⚠️ Still references `sqlalchemy` in isort known-third-party (line 52)
- ⚠️ References `alembic/versions/*.py` (line 47) but Alembic removed

**Recommendations**:

1. Remove `sqlalchemy` from known-third-party list
2. Remove Alembic migration patterns (lines 46-47)

#### `pytest.ini`

**Findings**:

- ✅ Auto-detection for parallel workers (`-n auto`)
- ✅ Good test markers (asyncio, integration, serial, slow, smoke)
- ✅ Coverage target: 70%
- ✅ Good filterwarnings configuration

**Recommendations**:

- ✅ Configuration is optimal, no changes needed

#### `fastmcp.json`

**Findings**:

- ✅ Valid FastMCP configuration
- ✅ Correct entrypoint path
- ✅ Environment variable support
- ✅ Version aligned with requirements.txt (fastmcp>=2.0.0,<3.0.0)

**Recommendations**:

- ✅ Configuration is correct, no changes needed

#### `.envrc`

**Findings**:

- ✅ Excellent Keychain integration for API keys
- ✅ Environment-specific .env loading
- ✅ Proper PYTHONPATH configuration
- ✅ Good comments explaining behavior

**Recommendations**:

- ✅ Environment setup is excellent, no changes needed

#### `.gitignore`

**Findings**:

- ✅ Comprehensive exclusions
- ✅ Proper handling of secrets
- ✅ Good IDE/Tooling patterns
- ✅ Sensible data directory exclusions

**Recommendations**:

- ✅ Gitignore is comprehensive, no changes needed

---

### 1.3 Dependencies Management

**Status**: ✅ **Good** (recently cleaned)

#### `config/requirements.txt`

**Findings**:

- ✅ Version ranges properly specified
- ✅ Database dependencies removed (recent cleanup)
- ✅ Core framework properly pinned
- ✅ Testing dependencies well-organized
- ✅ Code quality tools included

**Dependencies Summary**:

- **Core Framework**: fastmcp>=2.0.0, fastapi>=0.100.0, easypost>=10.0.0
- **Testing**: pytest>=7.4.3, pytest-asyncio, pytest-cov, pytest-xdist
- **Code Quality**: ruff>=0.1.0, black>=23.0.0
- **Database**: ✅ Removed (personal use - YAGNI)

**Recommendations**:

- ✅ Dependencies are well-managed, no changes needed

---

## Phase 2: Environment Setup

### 2.1 Environment Variables

**Status**: ✅ **Excellent**

**Configuration Strategy**:

1. Root `.env` (optional, for shared overrides)
2. Environment-specific `.env.<env>` (test/production)
3. Local `.env` (highest priority, overrides all)

**Keychain Integration**:

- ✅ API keys loaded from macOS Keychain
- ✅ Environment-specific key loading
- ✅ Fallback to `.env` if Keychain unavailable
- ✅ Secure by default

**Findings**:

- ✅ Excellent security practices
- ✅ Clear environment variable precedence
- ✅ Good error handling

**Recommendations**:

- ✅ Environment setup is excellent, no changes needed

---

### 2.2 Virtual Environment

**Status**: ✅ **Good**

**Findings**:

- ✅ Venv located at project root (`venv/`)
- ✅ Python 3.14.0 detected (note: requirements target 3.13)
- ✅ Proper activation via `.envrc` (PATH_add venv/bin)
- ✅ Dependencies properly installed

**Recommendations**:

1. ⚠️ Align Python version documentation (3.13 vs 3.14)
2. Consider pinning Python version more explicitly in `.python-version`

---

### 2.3 Development Tools Setup

**Status**: ✅ **Excellent**

**Makefile**:

- ✅ Well-organized with clear targets
- ✅ Helpful shortcuts (d, t, l, f, c)
- ✅ Good error handling
- ✅ Comprehensive help system

**Pre-commit Hooks**:

- ✅ Comprehensive hook configuration
- ✅ Ruff for linting/formatting
- ✅ Secret detection
- ✅ Good exclusions for generated files

**Recommendations**:

- ✅ Tooling setup is excellent, no changes needed

---

## Phase 3: Source Code Organization

### 3.1 Source Structure (`src/`)

**Status**: ✅ **Excellent**

**Key Files**:

- `server.py`: FastAPI app with MCP integration ✅
- `lifespan.py`: Application lifecycle management ✅
- `dependencies.py`: Dependency injection ✅
- `exceptions.py`: Error handling ✅

**Findings**:

- ✅ Clean separation of concerns
- ✅ Proper async/await patterns
- ✅ Good error handling
- ✅ Clear module organization

**Recommendations**:

- ✅ Source structure is excellent, no changes needed

---

### 3.2 MCP Server Architecture (`src/mcp_server/`)

**Status**: ✅ **Excellent** (with minor improvements)

#### Server Initialization (`__init__.py`)

**Findings**:

- ✅ Well-structured `build_mcp_server()` function
- ✅ Proper tool/resource/prompt registration
- ✅ Good environment awareness
- ✅ Lifespan support for FastAPI integration

**Code Quality**:

```python
def build_mcp_server(
    *, lifespan: LifespanHook | None = None, name_suffix: str | None = None
) -> tuple[FastMCP, EasyPostService]:
    """Construct a fully registered FastMCP server instance."""
    # ✅ Good type hints
    # ✅ Clear documentation
    # ✅ Proper error handling
```

#### Tools (`src/mcp_server/tools/`)

**Statistics**:

- **Total Tools**: 7 registered tools
- **Tool Modules**: 10 files
- **Total Lines**: ~4,903 lines in tools/

**Tool Categories**:

1. **Core Tools**: `get_tracking`, `get_rates` (simple operations)
2. **Bulk Tools**: `get_shipment_rates`, `create_shipment`, `buy_shipment_label`
3. **Management Tools**: `download_shipment_documents`, `refund_shipment`

**Findings**:

- ✅ Well-organized tool registration
- ✅ Good use of FastMCP decorators (`@mcp.tool`)
- ✅ Consistent tool patterns
- ⚠️ Missing some FastMCP best practices (tags, annotations)

**FastMCP Best Practices Alignment**:

Based on Context7 FastMCP documentation, the project could benefit from:

1. **Tag-Based Filtering**: Tools should use tags for organization

   ```python
   # Current: @mcp.tool(tags=["shipment", "rates"])
   # ✅ Good - already implemented
   ```

2. **Tool Annotations**: Use annotations for tool hints

   ```python
   # Current: Some tools use annotations
   # ⚠️ Could be more consistent
   ```

3. **Error Handling**: Use FastMCP's `ToolError` for user-facing errors
   ```python
   # Current: Custom error dicts
   # ✅ Good - standardized responses
   ```

**Recommendations**:

1. ⚠️ Consider adding more tool tags for better organization
2. ⚠️ Ensure all tools use consistent annotation patterns
3. ✅ Error handling patterns are good

#### Resources (`src/mcp_server/resources/`)

**Findings**:

- ✅ Well-structured resource providers
- ✅ Good registration pattern
- ✅ Proper async patterns

**Recommendations**:

- ✅ Resources are well-implemented, no changes needed

#### Prompts (`src/mcp_server/prompts/`)

**Findings**:

- ✅ Organized prompt templates
- ✅ Good registration system
- ✅ Reusable patterns

**Recommendations**:

- ✅ Prompts are well-structured, no changes needed

---

### 3.3 Business Logic (`src/services/`)

**Status**: ✅ **Good**

**Services**:

- `easypost_service.py`: EasyPost API integration
- `smart_customs.py`: Customs information handling

**Findings**:

- ✅ Clean service layer
- ✅ Good abstraction from API details
- ✅ Proper error handling

**Recommendations**:

- ✅ Services are well-implemented, no changes needed

---

### 3.4 API Layer (`src/routers/`)

**Status**: ✅ **Good**

**Routers**:

- `analytics.py`: Analytics endpoints
- `shipments.py`: Shipment endpoints
- `tracking.py`: Tracking endpoints

**Findings**:

- ✅ Well-organized router structure
- ✅ Proper FastAPI patterns
- ✅ Good separation from business logic

**Recommendations**:

- ✅ Routers are well-structured, no changes needed

---

### 3.5 Data Models (`src/models/`)

**Status**: ✅ **Good**

**Models**:

- `analytics.py`: Analytics models
- `bulk_dto.py`: Bulk operation DTOs
- `requests.py`: Request models
- `responses.py`: Response models

**Findings**:

- ✅ Good use of Pydantic v2
- ✅ Clear model organization
- ✅ Proper validation

**Recommendations**:

- ✅ Models are well-structured, no changes needed

---

### 3.6 Utilities (`src/utils/`)

**Status**: ✅ **Good**

**Utilities**:

- `config.py`: Configuration management ✅
- `monitoring.py`: Health checks ✅
- `constants.py`: Constants ✅

**Findings**:

- ✅ Clean utility functions
- ✅ Good configuration management
- ✅ Proper health check implementation

**Recommendations**:

- ✅ Utilities are well-implemented, no changes needed

---

## Phase 4: Testing Setup

### 4.1 Test Structure

**Status**: ✅ **Excellent**

**Statistics**:

- **Total Test Files**: 33 Python files
- **Test Organization**: Unit, Integration, MCP, Routers
- **Test Discovery**: Properly configured

**Structure**:

```
tests/
├── unit/              # Unit tests (isolated)
├── integration/       # Integration tests (real API)
├── mcp/               # MCP-specific tests
└── routers/           # Router tests
```

**Findings**:

- ✅ Excellent test organization
- ✅ Clear separation between unit and integration tests
- ✅ Good test file naming conventions

**Recommendations**:

- ✅ Test structure is excellent, no changes needed

---

### 4.2 Test Configuration

**Status**: ✅ **Excellent**

**Configuration**:

- ✅ Auto-detected parallel workers (`-n auto`)
- ✅ Coverage target: 70%
- ✅ Good test markers
- ✅ Proper async test support

**Recommendations**:

- ✅ Test configuration is optimal, no changes needed

---

### 4.3 Test Patterns

**Findings**:

- ✅ AAA pattern (Arrange, Act, Assert)
- ✅ Good use of fixtures
- ✅ Proper mocking strategies
- ✅ Async test patterns

**Recommendations**:

- ✅ Test patterns are excellent, no changes needed

---

## Phase 5: MCP Server Details

### 5.1 MCP Tools

**Status**: ✅ **Good** (with minor improvements)

**Tools Registered**:

1. `get_tracking` - Core tool
2. `get_rates` - Core tool
3. `get_shipment_rates` - Bulk tool
4. `create_shipment` - Bulk tool
5. `buy_shipment_label` - Bulk tool
6. `download_shipment_documents` - Management tool
7. `refund_shipment` - Management tool

**FastMCP Best Practices**:

- ✅ Good use of `@mcp.tool` decorator
- ✅ Proper Context parameter handling
- ✅ Consistent response formats
- ⚠️ Could use more comprehensive tags
- ⚠️ Could add more tool annotations (readOnlyHint, destructiveHint)

**Recommendations**:

1. Add comprehensive tags to all tools for better organization
2. Use FastMCP annotations consistently (readOnlyHint, destructiveHint)
3. Consider tool categories for better discovery

---

### 5.2 MCP Resources

**Status**: ✅ **Good**

**Resources**:

- Shipment resources
- Stats resources

**Findings**:

- ✅ Well-implemented resource providers
- ✅ Good registration pattern

**Recommendations**:

- ✅ Resources are well-implemented, no changes needed

---

### 5.3 MCP Prompts

**Status**: ✅ **Good**

**Prompts**:

- Shipping prompts
- Tracking prompts
- Comparison prompts
- Optimization prompts

**Findings**:

- ✅ Well-organized prompt templates
- ✅ Good registration system

**Recommendations**:

- ✅ Prompts are well-structured, no changes needed

---

## Phase 6: Scripts and Utilities

### 6.1 Python Scripts

**Status**: ✅ **Good**

**Scripts**:

- `run_mcp.py`: MCP server runner ✅
- `mcp_tool.py`: Tool CLI ✅
- `get-bulk-rates.py`: Bulk rates testing ✅
- `verify_mcp_server.py`: Server verification ✅

**Findings**:

- ✅ Well-structured scripts
- ✅ Good Keychain integration
- ✅ Proper environment handling

**Recommendations**:

- ✅ Scripts are well-implemented, no changes needed

---

### 6.2 Shell Scripts

**Status**: ✅ **Good**

**Scripts**:

- Development scripts
- Test scripts
- Utility scripts

**Findings**:

- ✅ Well-organized script structure
- ✅ Good helper functions

**Recommendations**:

- ✅ Scripts are well-structured, no changes needed

---

## Phase 7: Documentation

### 7.1 Main Documentation

**Status**: ✅ **Excellent**

**Files**:

- `README.md`: Comprehensive project overview ✅
- `CLAUDE.md`: Excellent AI assistant guide ✅

**Findings**:

- ✅ Clear documentation
- ✅ Good examples
- ✅ Comprehensive guides

**Recommendations**:

- ✅ Documentation is excellent, no changes needed

---

### 7.2 Architecture Documentation

**Status**: ✅ **Good**

**Findings**:

- ✅ Good architecture documentation
- ✅ Decision records available
- ⚠️ Some outdated docs (PostgreSQL removed but docs remain)

**Recommendations**:

1. ⚠️ Update or remove PostgreSQL architecture docs
2. Add current architecture diagrams

---

### 7.3 Guide Documentation

**Status**: ✅ **Good**

**Findings**:

- ✅ Comprehensive guides
- ✅ Good workflow documentation
- ✅ Clear usage examples

**Recommendations**:

- ✅ Guides are well-written, no changes needed

---

## Phase 8: Build and Deployment

### 8.1 Build Configuration

**Status**: ✅ **Good**

**Findings**:

- ✅ Makefile build targets
- ✅ Proper build scripts
- ✅ Good cleanup commands

**Recommendations**:

- ✅ Build configuration is good, no changes needed

---

### 8.2 Deployment Configuration

**Status**: ✅ **Good**

**Findings**:

- ✅ Docker configurations
- ✅ Docker Compose setup
- ✅ Good deployment docs

**Recommendations**:

- ✅ Deployment configuration is good, no changes needed

---

## Phase 9: Security and Secrets

### 9.1 Secrets Management

**Status**: ✅ **Excellent**

**Findings**:

- ✅ Excellent Keychain integration
- ✅ No hardcoded secrets
- ✅ Proper environment variable handling
- ✅ Good `.gitignore` for secrets

**Recommendations**:

- ✅ Security practices are excellent, no changes needed

---

### 9.2 Security Configuration

**Status**: ✅ **Excellent**

**Findings**:

- ✅ Comprehensive `.gitignore`
- ✅ Secret detection in pre-commit
- ✅ No exposed credentials

**Recommendations**:

- ✅ Security configuration is excellent, no changes needed

---

## Phase 10: Quality Assurance

### 10.1 Code Quality Tools

**Status**: ✅ **Excellent**

**Tools**:

- ✅ Ruff (linting + formatting)
- ✅ Black (backup formatter)
- ✅ mypy (type checking)
- ✅ Bandit (security)

**Recommendations**:

- ✅ Code quality tools are excellent, no changes needed

---

### 10.2 Pre-commit Hooks

**Status**: ✅ **Excellent**

**Findings**:

- ✅ Comprehensive hooks
- ✅ Good exclusions
- ✅ Proper secret detection

**Recommendations**:

- ✅ Pre-commit configuration is excellent, no changes needed

---

## Phase 11: Issues and Recommendations

### 11.1 Identified Issues

#### Critical Issues

- ❌ None found

#### High Priority Issues

1. ⚠️ **Python version mismatch**: Requirements target 3.13, actual is 3.14
   - **Impact**: Potential compatibility issues
   - **Fix**: Align documentation or pin version

2. ⚠️ **Outdated config references**: `pyproject.toml` still references removed dependencies
   - **Impact**: Confusing configuration
   - **Fix**: Remove SQLAlchemy/Alembic references

3. ⚠️ **FastMCP best practices**: Could use more comprehensive tags and annotations
   - **Impact**: Better tool organization
   - **Fix**: Add tags and annotations to all tools

#### Medium Priority Issues

1. ⚠️ **Documentation cleanup**: PostgreSQL architecture docs still present
   - **Impact**: Confusing documentation
   - **Fix**: Update or remove outdated docs

#### Low Priority Issues

1. ⚠️ **Tool organization**: Could benefit from tool categories
   - **Impact**: Better tool discovery
   - **Fix**: Add category-based organization

---

### 11.2 Recommendations

#### Immediate Actions (High Priority)

1. **Update `pyproject.toml`**:

   ```toml
   # Remove SQLAlchemy from known-third-party (line 52)
   known-third-party = ["fastapi", "pydantic", "easypost"]

   # Remove Alembic patterns (lines 46-47)
   # Remove these lines:
   # "**/migrations/**/*.py" = ["E501", "UP007"]
   # "alembic/versions/*.py" = ["E501", "UP007"]
   ```

2. **Align Python version**:
   - Update `.python-version` to match actual version (3.14)
   - Or document Python 3.13 requirement clearly

3. **Enhance FastMCP tool annotations**:
   ```python
   @mcp.tool(
       tags=["shipment", "rates", "core"],
       annotations={
           "readOnlyHint": True,  # For read-only tools
           "destructiveHint": False,  # For destructive operations
       }
   )
   ```

#### Short-term Improvements (Medium Priority)

1. **Update documentation**:
   - Remove or update PostgreSQL architecture docs
   - Add current architecture overview

2. **Tool organization**:
   - Add comprehensive tags to all tools
   - Consider tool categories for better discovery

#### Long-term Enhancements (Low Priority)

1. **Performance monitoring**:
   - Add tool performance metrics
   - Track API call patterns

2. **Documentation**:
   - Add architecture diagrams
   - Create tool usage examples

---

## Summary Statistics

### Codebase Metrics

- **Source Files**: 41 Python files
- **Test Files**: 33 Python files
- **MCP Tools**: 7 registered tools
- **Tool Modules**: 10 files (~4,903 lines)
- **Python Version**: 3.14.0 (target: 3.13)

### Configuration Quality

- **Dependencies**: ✅ Well-managed
- **Environment**: ✅ Excellent
- **Security**: ✅ Excellent
- **Tooling**: ✅ Excellent

### Test Coverage

- **Test Organization**: ✅ Excellent
- **Test Configuration**: ✅ Excellent
- **Coverage Target**: 70%

---

## Conclusion

The EasyPost MCP project demonstrates **excellent setup and organization**. The project follows modern best practices, has a clear focus on personal use (YAGNI), and maintains high code quality standards.

### Overall Grade: **A- (Excellent)**

**Strengths**:

- ✅ Clean, well-organized structure
- ✅ Excellent security practices
- ✅ Comprehensive MCP server architecture
- ✅ Good test coverage
- ✅ Clear documentation

**Areas for Improvement**:

- ⚠️ Minor configuration cleanup needed
- ⚠️ FastMCP best practices alignment
- ⚠️ Documentation updates

### Recommended Next Steps

1. **Immediate**: Clean up `pyproject.toml` (remove SQLAlchemy/Alembic references)
2. **Short-term**: Enhance FastMCP tool annotations and tags
3. **Medium-term**: Update architecture documentation
4. **Long-term**: Add performance monitoring and metrics

### Enhanced Tool Integration

**Tools Available for Future Reviews**:

- ✅ **Context7**: Library documentation (active)
- ✅ **Exa Code Context**: Community examples (active)
- ✅ **Exa Web Search**: Latest information (active)
- ✅ **Desktop Commander**: Advanced analysis (active)
- ⚠️ **Hugging Face**: ML models/datasets (requires auth)

**Benefits**:

- Up-to-date best practices verification
- Community pattern discovery
- Comprehensive codebase analysis
- Real-world example integration

**Integration Strategy**:

1. Use Context7 for framework documentation
2. Use Exa for community patterns and examples
3. Use Desktop Commander for advanced analysis
4. Cross-reference findings for accuracy

---

## Enhanced Tools Integration

### Tools Used in This Review

#### ✅ Context7 - Library Documentation

- **Purpose**: Up-to-date framework documentation
- **Usage**: FastMCP best practices, tool registration patterns
- **Benefits**: Official documentation, best practices verification

#### ✅ Exa Code Context - Community Code Examples

- **Purpose**: Real-world code examples from open source
- **Usage**: FastMCP patterns, error handling examples, tool registration
- **Benefits**: Community best practices, implementation examples

#### ✅ Exa Web Search - Latest Information

- **Purpose**: Real-time web search for latest updates
- **Usage**: FastMCP 2.0 best practices, community patterns
- **Benefits**: Latest information, community trends

#### ✅ Desktop Commander - Advanced Analysis

- **Purpose**: File operations, process management, search
- **Usage**: Codebase analysis, pattern detection, validation
- **Benefits**: Comprehensive search, process execution

### Enhanced Findings

**From Exa Code Context Analysis**:

- ✅ Project follows FastMCP best practices for tool registration
- ✅ Error handling patterns align with community examples
- ✅ Context parameter usage is correct (optional context)
- ✅ ToolError usage is appropriate for user-facing errors

**From Exa Web Search**:

- ✅ FastMCP 2.0 is actively maintained and production-ready
- ✅ Project architecture aligns with recommended patterns
- ✅ Tool registration patterns match community best practices

**From Desktop Commander Search**:

- ✅ 6 tool files using `@mcp.tool` decorator
- ✅ Consistent registration pattern across all tools
- ✅ Proper error handling with ToolError where appropriate

### Recommendations from Enhanced Tools

1. **Error Handling Enhancement** (from Exa examples):
   - Consider adding more specific exception types
   - Add retry logic for transient failures
   - Implement circuit breaker pattern for API calls

2. **Tool Annotations** (from Context7):
   - Already using `readOnlyHint` and `idempotentHint` ✅
   - Consider adding `destructiveHint` for destructive operations
   - Use tags more comprehensively for filtering

3. **Testing Patterns** (from Exa examples):
   - Consider using FastMCP Client for tool testing
   - Add integration tests with Client wrapper
   - Test error handling paths more thoroughly

---

## Appendix: FastMCP Best Practices Reference

Based on Context7 FastMCP documentation and Exa code examples, here are best practices aligned with the project:

### Tool Registration

```python
@mcp.tool(
    tags=["category", "subcategory"],
    annotations={
        "readOnlyHint": True,  # For read-only operations
        "destructiveHint": False,  # For destructive operations
    }
)
async def my_tool(param: str, ctx: Context | None = None) -> dict:
    """Tool description."""
    # Implementation
```

### Server Configuration

```python
mcp = FastMCP(
    name="Server Name",
    include_tags={"public"},  # Filter tools by tags
    exclude_tags={"internal"},  # Hide internal tools
    on_duplicate_tools="error",  # Handle duplicates
)
```

### Testing

```python
@pytest.fixture
def mcp_server():
    server = FastMCP("TestServer")
    # Register tools
    return server

async def test_tool(mcp_server):
    async with Client(mcp_server) as client:
        result = await client.call_tool("my_tool", {"param": "value"})
        assert result.data == expected
```

---

**Review Completed**: 2025-01-17
**Reviewer**: AI Assistant (Claude)
**Next Review**: Recommended in 3-6 months or after major changes
