# EasyPost MCP Frontend

React 18 frontend application for EasyPost shipping management with real-time tracking and analytics.

## Tech Stack

- **React**: 18.2
- **Build Tool**: Vite 7.1
- **Routing**: React Router DOM 6.30
- **State Management**: Zustand + TanStack Query
- **Styling**: Tailwind CSS 3.4
- **UI Components**: Radix UI primitives
- **Forms**: React Hook Form + Zod validation
- **Charts**: Recharts
- **Icons**: Lucide React
- **Testing**: Vitest + Testing Library

## Quick Start

### Setup

```bash
# Install dependencies
npm install

# Configure environment
cp .env.example .env.development
# Edit .env.development if needed (defaults to localhost:8000)
```

### Running

```bash
# Development server (hot reload)
npm run dev
# Opens http://localhost:5173

# Production build
npm run build
npm run preview

# Run tests
npm test

# Linting & formatting
npm run lint
npm run format
```

## Project Structure

```
frontend/
├── src/
│   ├── main.jsx               # App entry point
│   ├── App.jsx                # Root component with routing
│   ├── pages/                 # Page components
│   │   ├── DashboardPage.jsx     # Overview dashboard
│   │   ├── ShipmentsPage.jsx     # Create/manage shipments
│   │   ├── TrackingPage.jsx      # Track packages
│   │   └── SettingsPage.jsx      # App settings
│   ├── components/            # Reusable components
│   │   ├── ui/                   # Base UI components (Radix)
│   │   ├── layout/               # Layout components
│   │   ├── dashboard/            # Dashboard-specific
│   │   ├── analytics/            # Analytics components
│   │   └── shipments/            # Shipment components
│   ├── services/              # API integration
│   │   └── api.js                # Axios client + endpoints
│   ├── stores/                # Zustand stores
│   │   ├── useUIStore.js         # UI state (theme, etc)
│   │   └── useThemeStore.js      # Theme management
│   ├── hooks/                 # Custom React hooks
│   │   └── useShipmentForm.js    # Form logic
│   ├── lib/                   # Utilities
│   │   └── utils.js              # Helper functions
│   └── styles/                # Global styles
│       └── index.css             # Tailwind + custom CSS
├── public/                    # Static assets
├── tests/                     # Test files
└── package.json               # Dependencies & scripts
```

## Pages

### DashboardPage
- Overview statistics
- Quick actions (Create Shipment, Track Package)
- Recent shipments list
- Analytics charts

### ShipmentsPage
- Create new shipments
- Address validation
- Parcel information
- Carrier selection
- View shipment list with filters

### TrackingPage
- Search by tracking number
- Real-time tracking status
- Delivery timeline
- Location history
- Demo data fallback

### SettingsPage
- Theme toggle (light/dark)
- API configuration
- User preferences
- About information

## Components

### UI Components (`components/ui/`)

Base components built with Radix UI:
- `Button` - Primary, secondary, outline variants
- `Input` - Form inputs with validation
- `Card` - Content containers
- `Badge` - Status indicators
- `Select` - Dropdown selects
- `Tabs` - Tab navigation
- `Dialog` - Modal dialogs
- `Separator` - Visual dividers

### Layout Components (`components/layout/`)

- `Header` - Top navigation with logo and theme toggle
- `Sidebar` - Side navigation (if implemented)
- `Layout` - Page wrapper

### Feature Components

- `MetricCard` - Dashboard stats display
- `QuickActionCard` - Action buttons
- `ShipmentForm` - Multi-step shipment creation
- `TrackingTimeline` - Package tracking visualization
- `AnalyticsDashboard` - Charts and metrics

## State Management

### TanStack Query (Server State)

Used for API data caching and synchronization:

```javascript
import { useQuery, useMutation } from '@tanstack/react-query';
import { shipmentAPI } from '@/services/api';

// Fetch shipments with caching
const { data, isLoading } = useQuery({
  queryKey: ['shipments'],
  queryFn: shipmentAPI.list,
  refetchInterval: 30000, // Auto-refresh every 30s
});

// Create shipment with optimistic updates
const mutation = useMutation({
  mutationFn: shipmentAPI.create,
  onSuccess: () => {
    queryClient.invalidateQueries(['shipments']);
  },
});
```

### Zustand (Client State)

Used for UI state and preferences:

```javascript
import { useUIStore } from '@/stores/useUIStore';

const { theme, setTheme } = useUIStore();
```

## API Integration

### Configuration (`services/api.js`)

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

### Available Endpoints

```javascript
// Shipments
shipmentAPI.create(data)
shipmentAPI.list({ page_size, before_id })
shipmentAPI.get(id)

// Tracking
trackingAPI.track(trackingNumber)

// Rates
ratesAPI.get({ to_address, from_address, parcel })

// Analytics
analyticsAPI.get({ days, include_test })
```

### Error Handling

The API client includes:
- Automatic toast notifications on errors
- Network error handling
- Timeout handling (30s)
- Request/response interceptors
- Development-only console logging

## Styling

### Tailwind CSS

Custom configuration in `tailwind.config.js`:
- Custom colors (primary, secondary, accent)
- Dark mode support
- Custom animations
- Component variants

### Theme System

```javascript
// Theme toggle
import useUIStore from '@/stores/useUIStore';

const { theme, toggleTheme } = useUIStore();
// theme: 'light' | 'dark'
```

### CSS Classes

Common patterns:
```javascript
// Card container
<div className="bg-card text-card-foreground rounded-lg border shadow-sm">

// Page layout
<div className="space-y-6 animate-fade-in">

// Form group
<div className="grid gap-4 md:grid-cols-2">
```

## Forms & Validation

### React Hook Form + Zod

```javascript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  name: z.string().min(1, 'Required'),
  email: z.string().email('Invalid email'),
});

const form = useForm({
  resolver: zodResolver(schema),
  defaultValues: { name: '', email: '' },
});
```

## Testing

### Run Tests

```bash
# Interactive mode (watch)
npm test

# Run once
npm test -- --run

# With coverage
npm run test:coverage
# View: open coverage/index.html

# UI mode
npm run test:ui
```

### Writing Tests

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Button from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick handler', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

## Development Workflow

### Creating a New Page

1. Create page component in `src/pages/`:
```javascript
export default function MyPage() {
  return (
    <div className="space-y-6">
      <h1>My Page</h1>
    </div>
  );
}
```

2. Add route in `App.jsx`:
```javascript
<Route path="/my-page" element={<MyPage />} />
```

3. Add navigation link in Header

### Creating a New Component

1. Create component in appropriate directory
2. Add PropTypes or TypeScript types
3. Create test file
4. Export from directory index

### Adding a New API Endpoint

1. Add function to `services/api.js`:
```javascript
export const myAPI = {
  myMethod: async (params) => {
    const response = await api.post('/my-endpoint', params);
    return response.data;
  },
};
```

2. Use with TanStack Query:
```javascript
const query = useQuery({
  queryKey: ['my-data', params],
  queryFn: () => myAPI.myMethod(params),
});
```

## Build & Deployment

### Production Build

```bash
# Build
npm run build
# Output: dist/

# Preview build locally
npm run preview

# Check bundle size
npm run build -- --report
```

### Environment Variables

```bash
# .env.development (gitignored)
VITE_API_URL=http://localhost:8000

# .env.production (gitignored)
VITE_API_URL=https://api.production.com
```

### Optimization

- Code splitting via React.lazy
- Image optimization
- Tree shaking
- CSS purging with Tailwind

## Code Quality

### Linting

```bash
# Check code
npm run lint

# Auto-fix
npm run lint:fix

# Format with Prettier
npm run format

# Check formatting
npm run format:check
```

### ESLint Configuration

- React hooks rules
- React refresh
- Best practices
- Custom rules (see `eslint.config.js`)

## Troubleshooting

### Common Issues

**Module not found:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Vite dev server issues:**
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

**API connection errors:**
- Check backend is running on `http://localhost:8000`
- Verify CORS configuration in backend
- Check `VITE_API_URL` in `.env.development`

**Build errors:**
```bash
# Check TypeScript/JSX errors
npm run build 2>&1 | less
```

## Performance

### Optimization Techniques

- React.memo for expensive components
- useCallback for event handlers
- useMemo for derived data
- Code splitting with lazy loading
- Image lazy loading
- Debounced search inputs
- Virtual scrolling for long lists (if needed)

### Monitoring

- React DevTools for component tree
- TanStack Query DevTools for cache
- Network tab for API calls
- Lighthouse for performance audit

## Best Practices

### Component Structure

```javascript
// 1. Imports
import { useState } from 'react';
import { Button } from '@/components/ui/button';

// 2. Types/PropTypes
MyComponent.propTypes = {
  title: PropTypes.string.isRequired,
};

// 3. Component
export default function MyComponent({ title }) {
  // Hooks
  const [state, setState] = useState();

  // Event handlers
  const handleClick = () => {};

  // Render
  return <div>{title}</div>;
}
```

### File Naming

- Components: PascalCase (`Button.jsx`)
- Utilities: camelCase (`formatDate.js`)
- Hooks: camelCase with 'use' prefix (`useShipmentForm.js`)
- Constants: UPPER_SNAKE_CASE

## Contributing

1. Run tests: `npm test`
2. Run linters: `npm run lint && npm run format`
3. Check types: Run build to verify
4. All checks pass: Tests + linters pass

## Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TanStack Query](https://tanstack.com/query)
- [Tailwind CSS](https://tailwindcss.com/)
- [Radix UI](https://www.radix-ui.com/)
- [React Router](https://reactrouter.com/)
