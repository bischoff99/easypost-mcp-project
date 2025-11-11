Interactive debugging assistance with intelligent breakpoint placement and output analysis.

**Context-aware**: No arguments needed - automatically analyzes code and suggests debugging strategies. Adds debug instrumentation, captures output, and identifies root causes.

## How It Works

**Complete MCP Workflow (4 Stages):**

**Stage 1 - Identify Issue**:
- Reads code with bug
- Analyzes error context
- Identifies debugging points

**Stage 2 - Add Debug Instrumentation**:
- Adds debug logging at strategic points
- Inserts variable inspection points
- Adds execution flow markers

**Stage 3 - Execute + Capture**:
- Runs code with debug logging
- Captures output and errors
- Records execution flow

**Stage 4 - Analyze Output**:
- Analyzes debug output using Sequential-thinking
- Identifies root cause
- Suggests fixes

## MCP Integration

### Stage 1 - Identify Issue

```yaml
Tool: mcp_desktop-commander_read_file
Read: Code with bug (absolute path)
  If file specified: Read that file
  If no args: Read current open file or selected code

Tool: mcp_sequential-thinking_sequentialthinking
Thoughts: 8-10
Identify:
  1. Where to add debug prints
  2. What variables to inspect
  3. Which paths to trace
  4. Execution flow points
  5. Error handling points
  6. Data transformation points
  7. API call points
  8. State changes

Progress: await ctx.report_progress(0, 4, "Analyzing code")
State: ctx.set_state("debug_plan", {
  "breakpoints": [
    {
      "line": 50,
      "type": "variable_inspection",
      "variables": ["shipment_id", "response"],
      "description": "Inspect API response"
    },
    {
      "line": 80,
      "type": "execution_flow",
      "description": "Track function entry"
    }
  ],
  "variables_to_watch": ["shipment_id", "response", "error"],
  "execution_paths": ["main", "create_shipment", "handle_error"]
})

Logging:
  await ctx.info(f"Identified {len(breakpoints)} debug points")
  await ctx.debug(f"Watching {len(variables_to_watch)} variables")
```

### Stage 2 - Add Debug Instrumentation

```yaml
Tool: mcp_desktop-commander_edit_block
Insert: Debug logging at strategic points

Language-specific patterns:

Python:
  import logging
  logger = logging.getLogger(__name__)
  
  # At function entry
  logger.debug(f"[DEBUG] Entering {function_name}")
  logger.debug(f"[DEBUG] Args: {args}, Kwargs: {kwargs}")
  
  # Variable inspection
  logger.debug(f"[DEBUG] shipment_id: {shipment_id}")
  logger.debug(f"[DEBUG] response: {response}")
  
  # Execution flow
  logger.debug(f"[DEBUG] Execution path: {current_path}")
  
  # Error points
  logger.debug(f"[DEBUG] Error occurred: {error}")

JavaScript:
  // Variable inspection
  console.log("[DEBUG] shipmentId:", shipmentId);
  console.log("[DEBUG] response:", JSON.stringify(response, null, 2));
  
  // Execution flow
  console.log("[DEBUG] Entering function:", functionName);
  console.log("[DEBUG] Execution path:", currentPath);
  
  // Error points
  console.error("[DEBUG] Error:", error);

Go:
  import "log"
  
  // Variable inspection
  log.Printf("[DEBUG] shipmentID: %v", shipmentID)
  log.Printf("[DEBUG] response: %+v", response)
  
  // Execution flow
  log.Printf("[DEBUG] Entering function: %s", functionName)
  
  // Error points
  log.Printf("[DEBUG] Error: %v", err)

Rust:
  use log::debug;
  
  // Variable inspection
  debug!("[DEBUG] shipment_id: {:?}", shipment_id);
  debug!("[DEBUG] response: {:?}", response);
  
  // Execution flow
  debug!("[DEBUG] Entering function: {}", function_name);
  
  // Error points
  debug!("[DEBUG] Error: {:?}", error);

For each breakpoint:
  Tool: mcp_desktop-commander_edit_block
  Parameters:
    file_path: Absolute path
    old_string: Code at breakpoint location
    new_string: Code + debug logging

Progress: await ctx.report_progress(1, 4, "Adding debug logging")
Logging:
  await ctx.info(f"Added debug logging at {len(breakpoints)} points")
```

### Stage 3 - Execute + Capture

```yaml
Tool: mcp_desktop-commander_start_process
Run: Code with debug logging
  Python: "python {file}" or "pytest {test_file}"
  JS: "node {file}" or "npm test"
  Go: "go run {file}" or "go test"
  Rust: "cargo run" or "cargo test"

Timeout: 60000ms
Capture: All output (stdout + stderr)

Progress: await ctx.report_progress(2, 4, "Running code")
State: ctx.set_state("debug_output", {
  "stdout": stdout_content,
  "stderr": stderr_content,
  "exit_code": exit_code,
  "execution_time": duration
})

Tool: mcp_desktop-commander_read_process_output
PID: Process PID
Timeout: 10000ms
Read: Complete output

Logging:
  await ctx.info("Captured debug output")
  await ctx.debug(f"Exit code: {exit_code}")
  if stderr_content:
    await ctx.warning(f"Errors: {stderr_content[:200]}...")
```

### Stage 4 - Analyze Output

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Analyze: Debug output + original code
Thoughts: 8-10
Identify:
  1. Root cause of issue
  2. Where execution diverged from expected
  3. Variable values at failure point
  4. Execution flow issues
  5. Data transformation problems
  6. Error handling gaps
  7. Suggested fixes

Progress: await ctx.report_progress(3, 4, "Analyzing output")
State: ctx.set_state("analysis", {
  "root_cause": "API response is None but code expects dict",
  "failure_point": "Line 50: response['id']",
  "variable_values": {
    "shipment_id": "shp_123",
    "response": None,
    "error": None
  },
  "execution_flow": "Function called → API call made → Response None → Error",
  "suggested_fixes": [
    "Add None check before accessing response['id']",
    "Add error handling for API failures",
    "Check API response status before processing"
  ]
})

Output: Root cause + suggested fixes
Logging:
  await ctx.info(f"Root cause identified: {root_cause}")
  await ctx.info(f"Suggested {len(suggested_fixes)} fixes")

Progress: await ctx.report_progress(4, 4, "Complete")
```

## Usage Examples

```bash
# Debug selected code or open file
/debug

# Debug specific file
/debug backend/src/services/easypost_service.py

# Debug with test
/debug --test backend/tests/test_service.py

# Debug specific function
/debug --function=create_shipment

# Keep debug logging (don't remove after analysis)
/debug --keep-logs
```

## Output Format

### Debug Analysis Output

```
🔍 Identifying Issue:
File: backend/src/services/easypost_service.py
Analyzing: create_shipment function
Found: Potential issue at line 50

📝 Adding Debug Instrumentation:
Added debug logging at 5 points:
  ✅ Line 45: Function entry
  ✅ Line 50: Variable inspection (response)
  ✅ Line 55: Execution flow marker
  ✅ Line 60: Error handling point
  ✅ Line 65: Return value inspection

▶️ Executing Code:
Running: python backend/src/services/easypost_service.py
Captured output:
  [DEBUG] Entering create_shipment
  [DEBUG] Args: {'to_address': {...}, 'from_address': {...}}
  [DEBUG] shipment_id: shp_123
  [DEBUG] response: None
  [DEBUG] Error occurred: TypeError: 'NoneType' object is not subscriptable

🧠 Analyzing Output (Sequential-thinking):
Step 1: Function called with valid arguments
Step 2: API call made successfully (no exception)
Step 3: Response returned as None
Step 4: Code tries to access response['id'] at line 50
Step 5: TypeError occurs because response is None

Root Cause:
API response is None but code expects dict. The API call
succeeded but returned None, likely due to API error or
empty response.

Variable Values at Failure:
  shipment_id: "shp_123"
  response: None
  error: None

Execution Flow:
  1. Function entry → Args validated
  2. API call → Response None
  3. Access response['id'] → TypeError

💡 Suggested Fixes:
1. Add None check before accessing response:
   if response is None:
       raise ValueError("API returned None")
   
2. Add error handling for API failures:
   try:
       response = api_call()
       if response is None:
           raise APIError("Empty response")
   except APIError as e:
       logger.error(f"API error: {e}")
       raise

3. Check API response status:
   if response and 'id' in response:
       return response['id']
   else:
       raise ValueError("Invalid response format")

✅ Debug Analysis Complete
```

## Performance

- Issue identification: 2-3s (Sequential-thinking with 8-10 thoughts)
- Adding instrumentation: 2-5s (edit_block per breakpoint)
- Code execution: 3-10s (depends on code complexity)
- Output analysis: 3-5s (Sequential-thinking with 8-10 thoughts)
- **Total: 10-23s** for complete debug cycle

## Desktop Commander Tools Used

**Primary Tools:**
- `mcp_desktop-commander_read_file` - Read code to debug
- `mcp_desktop-commander_edit_block` - Add debug logging
- `mcp_desktop-commander_start_process` - Execute code
- `mcp_desktop-commander_read_process_output` - Capture output
- `mcp_sequential-thinking_sequentialthinking` - Issue identification, output analysis

## Error Handling

**Code Execution Failures:**
- Capture error output
- Analyze error message
- Report failure reason

**Debug Instrumentation Failures:**
- Report error with file/line
- Continue with remaining breakpoints
- Provide partial debugging

**Output Analysis Failures:**
- Report warning
- Provide raw debug output
- Suggest manual analysis

## Debug Patterns

**Variable Inspection:**
- Log variable values at key points
- Show data types and structures
- Track value changes

**Execution Flow:**
- Mark function entry/exit
- Track conditional branches
- Log loop iterations

**Error Tracking:**
- Capture exceptions
- Log error context
- Track error propagation

**Performance Debugging:**
- Add timing markers
- Measure execution time
- Identify bottlenecks

## Adapts To Any Language

Works automatically with:
- Python (logging module)
- JavaScript/TypeScript (console.log)
- Go (log package)
- Rust (log crate)

**One command. Smart debugging. Any language. Root cause identification.**
