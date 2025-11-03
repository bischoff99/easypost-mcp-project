---
name: component
category: gen
description: Generate frontend component with framework-specific patterns
allowed-tools: [Read, Grep, FileEdit, mcp_context7_get-library-docs]
requires-approval: true
context-aware: true
arguments:
  - name: name
    type: string
    required: true
    description: Component name in PascalCase
  - name: type
    type: string
    required: false
    default: "functional"
    options: ["functional", "class", "server", "client"]
    description: Component type
  - name: props
    type: string
    required: false
    description: Props specification (comma-separated)
estimated-time: 6-10s
estimated-tokens: 2000-3500
m3-max-optimized: true
version: 2.0
---

# /gen:component

Generate production-ready frontend components with framework-specific patterns, TypeScript support, tests, and documentation. Automatically detects your framework from codebase or `.dev-config.json`.

## Usage

```bash
# Basic component
/gen:component UserCard

# With props
/gen:component ProductList "items:Product[], onSelect:Function"

# Specific type
/gen:component LoginForm --type=functional

# From selection (extract)
/gen:component @selection NewComponent
```

## Auto-Detection

Automatically detects framework and applies patterns:

### React
```bash
/gen:component Dashboard

# Generates:
# ✅ Functional component with hooks
# ✅ TypeScript interfaces
# ✅ Loading/error states
# ✅ Tailwind CSS (if configured)
# ✅ Zustand integration (if used)
# ✅ Component test
```

### Vue
```bash
/gen:component UserProfile

# Generates:
# ✅ Composition API setup
# ✅ <script setup> syntax
# ✅ TypeScript support
# ✅ Pinia integration
# ✅ Scoped styles
# ✅ Component test
```

### Svelte
```bash
/gen:component TodoList

# Generates:
# ✅ Svelte component
# ✅ TypeScript in script tag
# ✅ Reactive declarations ($:)
# ✅ Store integration
# ✅ Component test
```

## Context7 Integration

Uses `mcp_context7_get-library-docs` for framework-specific best practices:

```
Fetching React 18.3 best practices...
✓ Hooks patterns
✓ Server components
✓ Error boundaries
✓ Accessibility

Generating component with latest patterns...
```

## Component Types

### Type: Functional (Default)
```typescript
// UserCard.tsx
import { useState } from 'react';

interface UserCardProps {
  user: User;
  onAction?: (action: string) => void;
}

export default function UserCard({ user, onAction }: UserCardProps) {
  const [loading, setLoading] = useState(false);

  return (
    <div className="user-card">
      {/* Component JSX */}
    </div>
  );
}
```

### Type: Server Component (Next.js)
```typescript
// ProductList.tsx (Server Component)
async function ProductList({ category }: ProductListProps) {
  const products = await fetchProducts(category);

  return (
    <div className="products">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

### Type: Client Component (Next.js)
```typescript
'use client';

// InteractiveForm.tsx
export default function InteractiveForm() {
  const [state, setState] = useState();
  // Client-side interactivity
}
```

## Generated Files

```
frontend/src/components/UserCard/
├── UserCard.tsx              # Component logic
├── UserCard.css              # Styles (if not Tailwind)
├── UserCard.test.tsx         # Component tests
├── UserCard.stories.tsx      # Storybook (if configured)
└── index.ts                  # Barrel export
```

## Smart Defaults from .dev-config.json

```json
{
  "stack": {
    "frontend": {
      "framework": "react",
      "styling": "tailwindcss",
      "stateManagement": "zustand",
      "components": "shadcn-ui"
    }
  },
  "conventions": {
    "javascript": {
      "components": "PascalCase",
      "files": "PascalCase.tsx"
    }
  },
  "generation": {
    "component": {
      "includeTests": true,
      "includeStories": false,
      "typescript": true,
      "propTypes": false
    }
  }
}
```

## Framework-Specific Patterns

### React Best Practices
✅ Hooks for state/effects
✅ Error boundaries
✅ Memo for optimization
✅ Proper key props
✅ Accessibility attributes

### Vue Best Practices
✅ Composition API
✅ defineProps/defineEmits
✅ Computed properties
✅ Watchers when needed
✅ Teleport for modals

### Svelte Best Practices
✅ Reactive declarations
✅ Stores for state
✅ Actions for behavior
✅ Transitions/animations
✅ Slots for composition

## State Management Integration

### With Zustand (React)
```typescript
import { useStore } from '@/stores/userStore';

export default function UserProfile() {
  const { user, updateUser } = useStore();
  // Auto-integrated
}
```

### With Pinia (Vue)
```typescript
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
// Auto-integrated
```

### With Svelte Stores
```typescript
import { user } from '$lib/stores/user';
// Auto-integrated with $ syntax
```

## Example Workflows

### Workflow 1: New Feature Component
```bash
# Generate main component
/gen:component ProductDashboard "products:Product[], filters:Filters"

# Generate child components
/gen:component ProductCard "product:Product"
/gen:component ProductFilters "onFilterChange:Function"

# Test all
/test:run frontend/src/components/
```

### Workflow 2: Extract from Selection
```bash
# Select complex JSX in editor
# Extract to new component
/gen:component @selection CheckoutForm

# AI analyzes selection, creates reusable component
```

### Workflow 3: Design System Component
```bash
# Generate with Shadcn UI patterns
/gen:component Button "variant:string, size:string, onClick:Function"

# Includes all variants, accessibility, tests
```

## Context-Aware Generation

### From @selection
```bash
# User selects:
<div className="user-profile">
  <img src={user.avatar} />
  <h2>{user.name}</h2>
  <p>{user.email}</p>
</div>

# Command:
/gen:component @selection UserProfileCard

# AI extracts:
# ✅ Props needed (user)
# ✅ Styles used
# ✅ Reusable component
```

### From @config
```bash
/gen:component ProductCard

# Reads .dev-config.json:
# ✓ React + TypeScript + Tailwind
# ✓ Zustand for state
# ✓ shadcn-ui components
# Generates with all integrations
```

## Testing Generated

```typescript
// UserCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import UserCard from './UserCard';

describe('UserCard', () => {
  const mockUser = {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com'
  };

  it('renders user information', () => {
    render(<UserCard user={mockUser} />);
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('handles action click', () => {
    const onAction = vi.fn();
    render(<UserCard user={mockUser} onAction={onAction} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(onAction).toHaveBeenCalledWith('click');
  });

  it('shows loading state', () => {
    render(<UserCard user={mockUser} loading />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });
});
```

## Storybook Integration (Optional)

```typescript
// UserCard.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import UserCard from './UserCard';

const meta: Meta<typeof UserCard> = {
  title: 'Components/UserCard',
  component: UserCard,
  parameters: { layout: 'centered' },
};

export default meta;
type Story = StoryObj<typeof UserCard>;

export const Default: Story = {
  args: {
    user: {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com'
    }
  }
};

export const Loading: Story = {
  args: { ...Default.args, loading: true }
};
```

## Accessibility Built-in

```typescript
// Generated with proper a11y
<button 
  aria-label="Edit user profile"
  aria-pressed={isEditing}
  onClick={handleEdit}
>
  Edit
</button>

<img 
  src={user.avatar} 
  alt={`${user.name}'s profile picture`}
/>

<form onSubmit={handleSubmit} role="form">
  <label htmlFor="email">Email</label>
  <input 
    id="email"
    type="email"
    aria-required="true"
    aria-invalid={!!errors.email}
  />
</form>
```

## Performance Optimizations

### React.memo
```typescript
export default memo(UserCard, (prevProps, nextProps) => {
  return prevProps.user.id === nextProps.user.id;
});
```

### Vue computed
```typescript
const computedValue = computed(() => {
  return expensiveCalculation(props.data);
});
```

### Svelte reactive
```typescript
$: computedValue = expensiveCalculation(data);
```

## M3 Max Optimization

**Parallel Generation**:
- Component + Tests + Styles generated simultaneously
- Uses Context7 for patterns (cached)
- 16-core optimization for large components

**Performance**: 6-10s vs 20-30s sequential

## Related Commands

- `/test:run @file` - Test generated component
- `/quality:optimize @file` - Optimize component
- `/context:explain @file` - Understand component
- `/gen:api` - Generate matching API

## Best Practices

✅ **Use TypeScript** - Type safety prevents bugs
✅ **Include tests** - Always generate with tests
✅ **Follow framework patterns** - Let AI apply best practices
✅ **Extract when complex** - Use @selection to refactor
✅ **Verify with tests** - Run `/test:run` after generation

## Tips

1. **Be specific with props** - Better type inference
2. **Use context variables** - @selection extracts components
3. **Check generated tests** - Ensure coverage
4. **Review accessibility** - AI includes it, verify it works
5. **Run immediately** - `/gen:component X && /test:run X`


