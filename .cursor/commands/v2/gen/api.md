---
name: api
category: gen
description: Generate API endpoint with validation, tests, and documentation
allowed-tools: [Read, Grep, FileEdit, codebase_search, mcp_context7_get-library-docs]
requires-approval: true
context-aware: true
arguments:
  - name: path
    type: string
    required: true
    description: API endpoint path (e.g., /users, /auth/login)
  - name: method
    type: string
    required: true
    description: HTTP method (GET, POST, PUT, DELETE, PATCH)
    enum: [GET, POST, PUT, DELETE, PATCH]
  - name: auth
    type: boolean
    required: false
    default: true
    description: Require authentication
estimated-time: 8-12s
estimated-tokens: 2500-3500
m3-max-optimized: true
version: 2.0
---

# /gen:api

Generate complete API endpoint with request/response models, validation, error handling, tests, and OpenAPI documentation. Framework-aware based on `.dev-config.json`.

## Usage

```bash
# Basic endpoint
/gen:api /users GET

# With authentication
/gen:api /users POST --auth

# Complex endpoint
/gen:api /orders/{id}/items POST

# Using context
/gen:api @selection POST
```

## What Gets Generated

### 1. Request/Response Models
**FastAPI (Python)**:
```python
from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime
```

**Express (TypeScript)**:
```typescript
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});
```

### 2. Route Handler
**FastAPI**:
```python
@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserResponse:
    """Create a new user account."""
    # Validation
    if await db.users.find_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    # Create user
    new_user = await db.users.create(user)

    # Log activity
    logger.info(f"User created: {new_user.id}", extra={"user_id": new_user.id})

    return UserResponse.from_orm(new_user)
```

### 3. Error Handling
- Input validation errors (422)
- Business logic errors (400, 404)
- Authentication errors (401, 403)
- Server errors (500)

### 4. Tests
```python
@pytest.mark.asyncio
async def test_create_user_success(client, auth_headers):
    response = await client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test User"},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
```

### 5. OpenAPI Documentation
- Endpoint description
- Request/response schemas
- Example payloads
- Error responses

## Context Variables

```bash
# Use selected code as model
/gen:api @selection POST

# Reference open file
/gen:api /users/@file POST

# Use Git changes
/gen:api @git-diff POST
```

## Smart Defaults from .dev-config.json

```json
{
  "stack": {
    "backend": {
      "framework": "fastapi",      → Generates FastAPI route
      "validation": "pydantic",     → Uses Pydantic models
      "database": "postgresql"      → Adds DB session dependency
    }
  },
  "conventions": {
    "functions": "snake_case",      → create_user()
    "files": "snake_case.py"        → user_routes.py
  }
}
```

## M3 Max Optimization

**Parallel Test Generation** (16 workers):
- Unit tests
- Integration tests
- Edge case tests
- Performance tests

**Time**: 8-12s total (vs 30-40s sequential)

## Agent Mode Workflow

```
User: /gen:api /users POST
AI: Analyzing requirements... (2s)

    📋 API Endpoint Plan:
    1. UserRequest model (email, name, password)
    2. UserResponse model (id, email, name, created_at)
    3. POST /users endpoint with validation
    4. Authentication required
    5. Tests (unit + integration)

    Proceed? [y/n/modify]

User: y

AI: Generating... (8s)
    ✅ backend/src/api/routes/users.py
    ✅ backend/src/models/user.py
    ✅ backend/tests/test_users.py

    Run tests? [y/n]

User: y

AI: Running tests with 16 workers...
    ✅ 12 tests passed (4.2s)

    Apply changes? [y/n/preview]

User: y

AI: Changes applied successfully.
```

## Framework Support

### FastAPI (Python)
- Async/await support
- Pydantic models
- OpenAPI auto-generation
- Dependency injection

### Express (TypeScript)
- Zod validation
- Middleware chains
- Error boundaries
- Type safety

### Django (Python)
- Django REST Framework
- Serializers
- ViewSets
- Permissions

### Go Gin
- Struct tags
- Middleware
- JSON binding
- Error handling

## Examples by Use Case

### CRUD Endpoint
```bash
/gen:api /products GET     # List products
/gen:api /products POST    # Create product
/gen:api /products/{id} GET    # Get product
/gen:api /products/{id} PUT    # Update product
/gen:api /products/{id} DELETE # Delete product
```

### Authentication
```bash
/gen:api /auth/login POST
/gen:api /auth/register POST
/gen:api /auth/refresh POST
/gen:api /auth/logout POST
```

### Nested Resources
```bash
/gen:api /users/{id}/orders GET
/gen:api /orders/{id}/items POST
```

## Tool Usage

**codebase_search**: Find existing patterns
**mcp_context7**: Get framework best practices
**Read**: Check existing endpoints
**FileEdit**: Create/modify files

## Performance Metrics

| Project Size | Generation Time | M3 Max Workers |
|--------------|----------------|----------------|
| Small (<100 endpoints) | 8-10s | 12 |
| Medium (100-500) | 10-12s | 16 |
| Large (500+) | 12-15s | 20 |

## Best Practices Applied

✅ Input validation (Pydantic/Zod)
✅ Error handling (HTTPException)
✅ Logging (with context)
✅ Authentication checks
✅ Rate limiting hooks
✅ OpenAPI documentation
✅ Comprehensive tests
✅ Type safety

## Related Commands

- `/gen:model` - Generate data models first
- `/gen:crud` - Generate full CRUD at once
- `/test:run` - Run generated tests
- `/quality:secure` - Security audit endpoint

## Tips

1. **Generate models first** - Run `/gen:model` before `/gen:api`
2. **Use context** - Select existing code for better results
3. **Review before applying** - Use agent mode preview
4. **Test immediately** - Run `/test:run` to verify
5. **Check security** - Follow up with `/quality:secure`

