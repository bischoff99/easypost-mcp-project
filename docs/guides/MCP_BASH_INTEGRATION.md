# Bash Commands Enhanced with MCP Tools

This document describes how bash commands and scripts have been enhanced with MCP tool integration for project development.

## Overview

MCP (Model Context Protocol) tools are now accessible from bash scripts, Makefile commands, and development workflows. This enables:

- **Automated testing** of MCP tools from CI/CD
- **Health checks** that verify MCP server functionality
- **Development workflows** that use MCP tools for setup/verification
- **Integration testing** that exercises MCP tools alongside API endpoints

## MCP Tool CLI Wrapper

**File**: `scripts/mcp_tool.py`

A Python CLI wrapper that allows calling MCP tools from bash scripts:

```bash
# Call MCP tool directly
python scripts/mcp_tool.py get_tracking EZ1234567890

# With named parameters
python scripts/mcp_tool.py create_shipment --data "John Doe\t123 Main St..." --dry-run

# Get JSON output
python scripts/mcp_tool.py get_shipment_rates --data "..." | jq '.data'
```

**Usage**:
```bash
python scripts/mcp_tool.py <tool_name> [--key=value] [--flag]
```

**Available Tools**:
- `get_tracking` - Get tracking information
- `get_shipment_rates` - Get shipping rates
- `create_shipment` - Create shipments
- `buy_shipment_label` - Purchase labels
- `download_shipment_documents` - Download labels/forms

## Enhanced Makefile Commands

### `make dev`
Now includes MCP tool verification after server startup:
- Starts backend and frontend servers
- Verifies MCP tools are accessible after 3 seconds
- Shows status: ✅ MCP tools verified or ⚠️ MCP tools not yet accessible

### `make health`
Enhanced health check that includes MCP verification:
- Checks backend health endpoint
- Checks frontend accessibility
- **NEW**: Verifies MCP tools are accessible

### `make benchmark`
Now includes MCP tool performance testing:
- Runs standard benchmarks
- **NEW**: Tests MCP tool call performance
- Shows timing for MCP tool calls

## Enhanced Bash Scripts

### `scripts/dev-with-mcp.sh`
New script for development with MCP integration:

```bash
# Start backend with MCP verification
./scripts/dev-with-mcp.sh start

# Check MCP server health
./scripts/dev-with-mcp.sh health

# Verify MCP tools are registered
./scripts/dev-with-mcp.sh verify

# Test MCP tools with sample data
./scripts/dev-with-mcp.sh test
```

**Features**:
- Starts backend server
- Verifies MCP tools after startup
- Provides MCP-specific health checks
- Tests MCP tools with sample data

### `scripts/test-full-functionality.sh`
Enhanced test suite that includes MCP tool verification:

**New Phase 7: MCP Tools Verification**
- Tests MCP tool availability
- Verifies MCP tool response format
- Validates JSON structure
- Includes MCP tool call timing

## Integration Examples

### Example 1: Health Check Script
```bash
#!/bin/bash
# Check all services including MCP

echo "Checking backend..."
curl -s http://localhost:8000/health || echo "Backend down"

echo "Checking MCP tools..."
python scripts/mcp_tool.py get_tracking TEST 2>/dev/null | grep -q "status" && echo "MCP OK" || echo "MCP down"
```

### Example 2: Test Setup Script
```bash
#!/bin/bash
# Setup test data using MCP tools

# Create test shipment
python scripts/mcp_tool.py create_shipment \
    --data "Test User\t123 Test St\tTest City\tCA\t90210\t..." \
    --dry-run

# Get tracking for test shipment
TRACKING=$(python scripts/mcp_tool.py get_tracking "EZ1234567890" | jq -r '.data.tracking_number')
echo "Test tracking: $TRACKING"
```

### Example 3: CI/CD Integration
```yaml
# .github/workflows/test.yml
- name: Test MCP Tools
  run: |
    python scripts/mcp_tool.py get_tracking TEST
    python scripts/mcp_tool.py get_shipment_rates --data "test"
```

## Benefits

1. **Automated Verification**: MCP tools are automatically verified during development
2. **Health Monitoring**: Health checks include MCP tool status
3. **Integration Testing**: MCP tools can be tested alongside API endpoints
4. **Development Workflows**: Scripts can use MCP tools for setup/teardown
5. **CI/CD Integration**: MCP tools can be tested in automated pipelines

## Usage in Development

### Quick MCP Tool Test
```bash
# Test a single MCP tool
make health  # Includes MCP verification

# Test MCP tools directly
python scripts/mcp_tool.py get_tracking EZ1234567890
```

### Development Workflow
```bash
# Start dev environment (includes MCP verification)
make dev

# Run full test suite (includes MCP tool tests)
./scripts/test-full-functionality.sh

# Check MCP health separately
./scripts/dev-with-mcp.sh health
```

## Future Enhancements

Potential additions:
- MCP tool benchmarking script
- MCP tool mock server for testing
- MCP tool performance monitoring
- Automated MCP tool documentation generation
- MCP tool integration tests in pytest

## Files Modified

- `Makefile` - Enhanced `dev`, `health`, `benchmark` commands
- `scripts/mcp_tool.py` - New MCP tool CLI wrapper
- `scripts/dev-with-mcp.sh` - New development script with MCP integration
- `scripts/test-full-functionality.sh` - Added MCP tool verification phase

## See Also

- `docs/architecture/MCP_TOOLS_INVENTORY.md` - Complete MCP tools documentation
- `apps/backend/src/mcp_server/` - MCP server implementation
- `scripts/verify_mcp_server.py` - MCP server verification script
