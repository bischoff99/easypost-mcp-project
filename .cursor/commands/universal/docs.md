Generate comprehensive documentation for code, including docstrings, README sections, and API documentation.

**Context-aware**: No arguments needed - automatically analyzes code and generates appropriate documentation. Supports multiple documentation styles and formats.

## How It Works

**Complete MCP Workflow (4 Stages):**

**Stage 1 - Analyze Code**:
- Reads target file(s)
- Identifies undocumented functions/classes
- Determines documentation needs

**Stage 2 - Generate Docstrings**:
- Creates docstrings for functions/classes
- Uses language-specific formats
- Includes parameters, returns, examples

**Stage 3 - Generate README Sections** (if --readme):
- Creates README sections
- Includes installation, usage, API reference
- Adds examples and code snippets

**Stage 4 - Verify**:
- Checks documentation completeness
- Validates format
- Ensures all public APIs documented

## Documentation Styles Supported

**Python:**
- Google style
- NumPy style
- Sphinx style

**JavaScript/TypeScript:**
- JSDoc format
- TypeScript documentation comments

**Go:**
- GoDoc format
- Standard Go documentation conventions

**Rust:**
- Rustdoc format
- Standard Rust documentation style

## MCP Integration

### Stage 1 - Analyze Code

```yaml
Tool: mcp_desktop-commander_read_file
Read: Target file(s)
  If file specified: Read that file
  If no args: Read current open file or selected code

Tool: mcp_sequential-thinking_sequentialthinking
Thoughts: 8-10
Identify:
  1. Public functions/classes needing docstrings
  2. Module-level documentation needed
  3. README sections missing
  4. API documentation gaps
  5. Parameter descriptions needed
  6. Return value documentation
  7. Example code needed
  8. Error documentation needed

Progress: await ctx.report_progress(0, 4, "Analyzing documentation needs")
State: ctx.set_state("doc_needs", {
  "functions": [
    {
      "name": "create_shipment",
      "line": 50,
      "params": ["to_address", "from_address", "parcel"],
      "returns": "ShipmentResponse",
      "needs_docstring": True,
      "needs_examples": True
    }
  ],
  "classes": [
    {
      "name": "EasyPostService",
      "line": 20,
      "methods": ["create_shipment", "track_shipment"],
      "needs_docstring": True
    }
  ],
  "module": {
    "needs_docstring": True,
    "description": "Service for EasyPost API integration"
  }
})

Logging:
  await ctx.info(f"Found {len(functions)} functions, {len(classes)} classes needing documentation")
```

### Stage 2 - Generate Docstrings

```yaml
For each function/class:
  Tool: mcp_Context7_resolve-library-id
  Detect: Language/framework from file
  
  Tool: mcp_Context7_get-library-docs
  Get: Documentation style guide for language
  Topic: "docstring format style guide examples"
  Tokens: 2000
  
  Tool: mcp_sequential-thinking_sequentialthinking
  Generate: Proper docstring
    Python (Google style):
      """
      Brief description.
      
      Longer description if needed.
      
      Args:
          param1: Description of param1
          param2: Description of param2
      
      Returns:
          Description of return value
      
      Raises:
          ExceptionType: When this exception is raised
      
      Example:
          >>> result = create_shipment(...)
          >>> print(result.id)
      """
    
    JS (JSDoc):
      /**
       * Brief description.
       * 
       * @param {Object} param1 - Description
       * @param {string} param2 - Description
       * @returns {Promise<ShipmentResponse>} Description
       * @throws {Error} When error occurs
       * 
       * @example
       * const result = await createShipment(...);
       * console.log(result.id);
       */
    
    Go (GoDoc):
      // CreateShipment creates a new shipment.
      //
      // Parameters:
      //   toAddress: Destination address
      //   fromAddress: Origin address
      //
      // Returns:
      //   ShipmentResponse with shipment details
      //
      // Example:
      //   result, err := CreateShipment(to, from, parcel)
    
    Rust (Rustdoc):
      /// Creates a new shipment.
      ///
      /// # Arguments
      /// * `to_address` - Destination address
      /// * `from_address` - Origin address
      ///
      /// # Returns
      /// `ShipmentResponse` with shipment details
      ///
      /// # Example
      /// ```
      /// let result = create_shipment(to, from, parcel)?;
      /// ```

  Tool: mcp_desktop-commander_edit_block
  Insert: Generated docstring above function/class
  Parameters:
    file_path: Absolute path
    old_string: Function/class definition (without docstring)
    new_string: Docstring + function/class definition

Progress: await ctx.report_progress(1, 4, f"Documenting {i}/{total} items")
Logging:
  await ctx.info(f"Added docstring for {function_name}")
```

### Stage 3 - Generate README Sections (if --readme)

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Analyze: Project structure
Generate: README sections
  1. Installation
     - Dependencies
     - Setup steps
     - Configuration
  
  2. Usage
     - Basic examples
     - Common patterns
     - Code snippets
  
  3. API Reference
     - Public functions/classes
     - Parameters
     - Return values
     - Examples
  
  4. Examples
     - Complete examples
     - Use cases
     - Integration examples

Tool: mcp_desktop-commander_read_file
Path: README.md (if exists)
Read: Current content

Tool: mcp_desktop-commander_edit_block
Update: README.md
  If exists: Append/update sections
  If not exists: Create new README.md

Progress: await ctx.report_progress(2, 4, "Generating README sections")
Logging:
  await ctx.info("Updated README.md with new sections")
```

### Stage 4 - Verify

```yaml
Check documentation quality:
  1. All public APIs documented
  2. Examples provided
  3. Parameters described
  4. Return values documented
  5. Error cases documented
  6. Format correct

Tool: mcp_desktop-commander_start_search
Pattern: Function/class definitions
SearchType: "content"
Find: Undocumented public APIs

Progress: await ctx.report_progress(3, 4, "Verifying documentation")
State: ctx.set_state("verification", {
  "documented": count_documented,
  "undocumented": count_undocumented,
  "coverage": percentage_coverage
})

Logging:
  await ctx.info(f"Documentation coverage: {coverage}%")
  if undocumented > 0:
    await ctx.warning(f"{undocumented} items still need documentation")

Progress: await ctx.report_progress(4, 4, "Complete")
```

## Usage Examples

```bash
# Document selected code or open file
/docs

# Document specific file
/docs backend/src/services/easypost_service.py

# Document with README generation
/docs --readme

# Document specific style
/docs --style=google  # Python
/docs --style=jsdoc   # JavaScript

# Document with examples
/docs --examples
```

## Output Format

### Success Output

```
📋 Analyzing Documentation Needs:
File: backend/src/services/easypost_service.py
Found: 5 functions, 1 class needing documentation

📝 Generating Docstrings:

1/6: create_shipment()
  ✅ Added Google-style docstring
  ✅ Includes parameters, returns, examples

2/6: track_shipment()
  ✅ Added Google-style docstring
  ✅ Includes error handling documentation

3/6: get_rates()
  ✅ Added Google-style docstring
  ✅ Includes examples

4/6: EasyPostService class
  ✅ Added class docstring
  ✅ Documented all methods

5/6: _sanitize_error() (private, skipped)
6/6: Module-level docstring
  ✅ Added module description

📚 Generating README Sections (--readme):
  ✅ Installation section
  ✅ Usage examples
  ✅ API reference
  ✅ Code examples

✅ Verification:
Documentation coverage: 100%
All public APIs documented
Examples provided
Format validated

✅ Documentation complete!
```

## Performance

- Code analysis: 2-3s (Sequential-thinking with 8-10 thoughts)
- Docstring generation: 3-5s per item (Context7 + Sequential-thinking + edit_block)
- README generation: 2-4s (Sequential-thinking + edit_block)
- Verification: 1-2s (search + analysis)
- **Total: 8-20s** depending on number of items to document

## Desktop Commander Tools Used

**Primary Tools:**
- `mcp_desktop-commander_read_file` - Read code, README
- `mcp_desktop-commander_edit_block` - Insert docstrings, update README
- `mcp_desktop-commander_start_search` - Find undocumented APIs
- `mcp_sequential-thinking_sequentialthinking` - Analyze needs, generate content
- `mcp_Context7_resolve-library-id` - Language detection
- `mcp_Context7_get-library-docs` - Documentation style guides

## Error Handling

**File Not Found:**
- Report error: "File not found"
- Suggest checking file path

**Context7 Unavailability:**
- Use generic documentation templates
- Report warning
- Continue with basic docstrings

**Edit Failures:**
- Report error with file/line
- Continue with remaining items
- Provide partial results

## Documentation Formats

### Python (Google Style)

```python
def create_shipment(to_address: dict, from_address: dict, parcel: dict) -> dict:
    """Create a new shipment via EasyPost API.
    
    This function creates a shipping label for the given addresses
    and parcel information using the EasyPost API.
    
    Args:
        to_address: Destination address dictionary with keys:
            street1, city, state, zip, country
        from_address: Origin address dictionary with same format
        parcel: Parcel information with keys:
            length, width, height, weight
    
    Returns:
        Dictionary containing shipment details:
            - id: Shipment ID
            - tracking_code: Tracking number
            - label_url: Label download URL
            - rate: Shipping rate
    
    Raises:
        EasyPostError: If API call fails
        ValidationError: If address/parcel data invalid
    
    Example:
        >>> shipment = create_shipment(
        ...     to_address={"street1": "123 Main St", ...},
        ...     from_address={"street1": "456 Oak Ave", ...},
        ...     parcel={"length": 10, "width": 5, "height": 3, "weight": 1}
        ... )
        >>> print(shipment["tracking_code"])
    """
```

### JavaScript (JSDoc)

```javascript
/**
 * Creates a new shipment via EasyPost API.
 * 
 * @param {Object} toAddress - Destination address
 * @param {string} toAddress.street1 - Street address
 * @param {string} toAddress.city - City name
 * @param {string} toAddress.state - State code
 * @param {string} toAddress.zip - ZIP code
 * @param {string} toAddress.country - Country code
 * @param {Object} fromAddress - Origin address (same format)
 * @param {Object} parcel - Parcel information
 * @param {number} parcel.length - Length in inches
 * @param {number} parcel.width - Width in inches
 * @param {number} parcel.height - Height in inches
 * @param {number} parcel.weight - Weight in ounces
 * @returns {Promise<Object>} Shipment details
 * @throws {Error} If API call fails
 * 
 * @example
 * const shipment = await createShipment(
 *   { street1: "123 Main St", city: "San Francisco", ... },
 *   { street1: "456 Oak Ave", city: "Los Angeles", ... },
 *   { length: 10, width: 5, height: 3, weight: 16 }
 * );
 * console.log(shipment.trackingCode);
 */
```

## Adapts To Any Language

Works automatically with:
- Python (Google, NumPy, Sphinx styles)
- JavaScript/TypeScript (JSDoc)
- Go (GoDoc)
- Rust (Rustdoc)

**One command. Comprehensive docs. Any language. Professional format.**
