# UI Components Index

Quick reference guide for all UI components in the EasyPost MCP Frontend.

---

## 📋 Table of Contents

1. [Layout Components](#layout-components)
2. [Data Display](#data-display)
3. [Forms & Inputs](#forms--inputs)
4. [Feedback](#feedback)
5. [Navigation](#navigation)
6. [Utility](#utility)

---

## Layout Components

### Card
**Path:** `src/components/ui/Card.jsx`

Basic card container with header, content, and footer sections.

```javascript
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/Card';

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content here</CardContent>
  <CardFooter>Footer</CardFooter>
</Card>
```

### EnhancedCard
**Path:** `src/components/ui/EnhancedCard.jsx`

Card with hover effects, gradients, and animations.

```javascript
<EnhancedCard
  title="Revenue"
  description="Monthly total"
  icon={DollarSign}
  gradient
  hoverable
  onClick={handleClick}
  delay={0.1}
>
  <div>$12,345</div>
</EnhancedCard>
```

**Props:**
- `title` (string): Card title
- `description` (string): Card description
- `icon` (Component): Icon component
- `gradient` (boolean): Enable gradient overlay
- `hoverable` (boolean): Enable hover effects
- `onClick` (function): Click handler
- `delay` (number): Animation delay

---

## Data Display

### DataTable
**Path:** `src/components/ui/DataTable.jsx`

Advanced table with sorting, filtering, pagination, and row selection.

```javascript
<DataTable
  columns={[
    { key: 'name', header: 'Name', sortable: true },
    { key: 'status', header: 'Status', render: (row) => <Badge>{row.status}</Badge> }
  ]}
  data={items}
  onRowClick={handleClick}
  onRowSelect={handleSelect}
  searchPlaceholder="Search..."
  pageSize={10}
/>
```

**Props:**
- `columns` (array): Column definitions
  - `key` (string): Data key
  - `header` (string): Column header
  - `sortable` (boolean): Enable sorting
  - `render` (function): Custom cell renderer
  - `className` (string): Header class
  - `cellClassName` (string): Cell class
- `data` (array): Table data
- `onRowClick` (function): Row click handler
- `onRowSelect` (function): Selection handler
- `isLoading` (boolean): Loading state
- `emptyMessage` (string): Empty state message
- `searchPlaceholder` (string): Search placeholder
- `pageSize` (number): Rows per page

**Features:**
- ✅ Column sorting (asc/desc)
- ✅ Global search
- ✅ Row selection
- ✅ Pagination
- ✅ Custom rendering
- ✅ Loading states
- ✅ Empty states

### Table
**Path:** `src/components/ui/Table.jsx`

Basic table components (primitives).

```javascript
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/Table';

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>John</TableCell>
      <TableCell>Active</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### Badge
**Path:** `src/components/ui/Badge.jsx`

Status indicator badges.

```javascript
<Badge variant="default">Default</Badge>
<Badge variant="success">Success</Badge>
<Badge variant="warning">Warning</Badge>
<Badge variant="destructive">Error</Badge>
```

---

## Forms & Inputs

### Button
**Path:** `src/components/ui/Button.jsx`

Versatile button component.

```javascript
<Button variant="default" size="md" onClick={handleClick}>
  Click Me
</Button>
```

**Variants:**
- `default` - Primary button
- `secondary` - Secondary button
- `outline` - Outlined button
- `ghost` - Transparent button
- `destructive` - Danger button

**Sizes:**
- `sm` - Small
- `md` - Medium
- `lg` - Large
- `icon` - Icon only

### Input
**Path:** `src/components/ui/Input.jsx`

Text input field.

```javascript
<Input
  type="text"
  placeholder="Enter value..."
  value={value}
  onChange={handleChange}
/>
```

---

## Feedback

### EmptyState
**Path:** `src/components/ui/EmptyState.jsx`

Beautiful empty state component.

```javascript
<EmptyState
  icon={Package}
  title="No items yet"
  description="Get started by creating your first item"
  action={handleCreate}
  actionLabel="Create"
  secondaryAction={handleImport}
  secondaryActionLabel="Import"
/>
```

**Props:**
- `icon` (Component): Icon component
- `title` (string): Title text
- `description` (string): Description text
- `action` (function): Primary action
- `actionLabel` (string): Primary button label
- `secondaryAction` (function): Secondary action
- `secondaryActionLabel` (string): Secondary button label

### LoadingSpinner
**Path:** `src/components/ui/LoadingSpinner.jsx`

Loading indicators.

```javascript
// Simple spinner
<LoadingSpinner size="md" variant="primary" />

// Full overlay
<LoadingOverlay message="Loading..." />

// Skeleton loader
<SkeletonLoader rows={5} className="h-12" />
```

**LoadingSpinner Props:**
- `size` (`sm|md|lg|xl`): Spinner size
- `variant` (`primary|secondary|muted`): Color variant

**LoadingOverlay Props:**
- `message` (string): Loading message

**SkeletonLoader Props:**
- `rows` (number): Number of skeleton rows
- `className` (string): Custom classes

### Progress
**Path:** `src/components/ui/Progress.jsx`

Progress indicators.

```javascript
// Linear progress
<Progress value={75} animated />

// Circular progress
<CircularProgress value={75} size={80} strokeWidth={6} />
```

**Progress Props:**
- `value` (number): Progress percentage (0-100)
- `animated` (boolean): Enable animation

**CircularProgress Props:**
- `value` (number): Progress percentage (0-100)
- `size` (number): Circle size in pixels
- `strokeWidth` (number): Stroke width

### Tooltip
**Path:** `src/components/ui/Tooltip.jsx`

Accessible tooltips (Radix UI).

```javascript
<TooltipProvider>
  <Tooltip>
    <TooltipTrigger>Hover me</TooltipTrigger>
    <TooltipContent>
      <p>Tooltip content</p>
    </TooltipContent>
  </Tooltip>
</TooltipProvider>
```

### Toast (Sonner)
**Library:** `sonner`

Toast notifications.

```javascript
import { toast } from 'sonner';

toast.success('Success message');
toast.error('Error message');
toast.info('Info message');
toast.warning('Warning message');

// With description
toast.success('Title', {
  description: 'Detailed message'
});
```

---

## Navigation

### SearchModal
**Path:** `src/components/ui/SearchModal.jsx`

Global search with ⌘K shortcut.

```javascript
<SearchModal />
```

**Features:**
- ✅ Keyboard shortcut (⌘K / Ctrl+K)
- ✅ Real-time search
- ✅ Debounced (300ms)
- ✅ ESC to close

### NotificationsDropdown
**Path:** `src/components/ui/NotificationsDropdown.jsx`

Notifications dropdown.

```javascript
<NotificationsDropdown />
```

**Features:**
- ✅ Unread badge count
- ✅ Mark as read
- ✅ Clear all
- ✅ Persistent state

---

## Utility

### Skeleton
**Path:** `src/components/ui/Skeleton.jsx`

Skeleton loading placeholders.

```javascript
<Skeleton className="h-12 w-full" />
<SkeletonCard />
<SkeletonStats />
<SkeletonText rows={3} />
```

### Separator
**Path:** `src/components/ui/Separator.jsx`

Visual separator line.

```javascript
<Separator orientation="horizontal" />
<Separator orientation="vertical" />
```

### SuspenseBoundary
**Path:** `src/components/ui/SuspenseBoundary.jsx`

React Suspense wrapper with navigation loading.

```javascript
<NavigationLoader />

<PageSuspense fallback={<CustomLoader />}>
  <Component />
</PageSuspense>
```

### ErrorBoundary
**Path:** `src/components/ui/ErrorBoundary.jsx`

Error boundary for React errors.

```javascript
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

---

## 🎨 Design Tokens

### Colors

**Status Colors:**
- `success`: Green (delivered, completed)
- `warning`: Yellow (pending, in progress)
- `destructive`: Red (cancelled, error)
- `default`: Blue (in transit, active)

**Semantic Colors:**
- `primary`: Brand color
- `secondary`: Secondary brand
- `muted`: Subdued text
- `accent`: Highlight color

### Spacing

```css
gap-1  /* 0.25rem - 4px */
gap-2  /* 0.5rem - 8px */
gap-3  /* 0.75rem - 12px */
gap-4  /* 1rem - 16px */
gap-6  /* 1.5rem - 24px */
gap-8  /* 2rem - 32px */
```

### Border Radius

```css
rounded-sm  /* 0.125rem - 2px */
rounded     /* 0.25rem - 4px */
rounded-md  /* 0.375rem - 6px */
rounded-lg  /* 0.5rem - 8px */
rounded-xl  /* 0.75rem - 12px */
rounded-full /* 9999px - circle */
```

---

## 🎭 Animation Presets

### Framer Motion Variants

**Fade In:**
```javascript
initial={{ opacity: 0 }}
animate={{ opacity: 1 }}
transition={{ duration: 0.3 }}
```

**Slide Up:**
```javascript
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 0.4 }}
```

**Scale In:**
```javascript
initial={{ scale: 0.95, opacity: 0 }}
animate={{ scale: 1, opacity: 1 }}
transition={{ duration: 0.3 }}
```

**Stagger Children:**
```javascript
{items.map((item, i) => (
  <motion.div
    key={item.id}
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: i * 0.05 }}
  >
    {item.content}
  </motion.div>
))}
```

---

## 📱 Responsive Breakpoints

```javascript
// Tailwind breakpoints
sm: '640px',   // Small devices
md: '768px',   // Medium devices
lg: '1024px',  // Large devices
xl: '1280px',  // Extra large
2xl: '1536px'  // 2X large
```

**Usage:**
```javascript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive grid */}
</div>
```

---

## ♿ Accessibility

### ARIA Labels

```javascript
<button aria-label="Close modal">
  <X className="h-4 w-4" />
</button>
```

### Keyboard Navigation

- **Tab**: Navigate between elements
- **Enter/Space**: Activate buttons
- **Escape**: Close modals/dropdowns
- **Arrow keys**: Navigate lists/tables

### Screen Reader Support

```javascript
<span className="sr-only">
  Screen reader only text
</span>
```

---

## 🔗 Related Documentation

- [UI Upgrade Report](./UI_UPGRADE_REPORT.md)
- [Frontend Modernization Report](./MODERNIZATION_REPORT.md)
- [Header Implementation Report](./HEADER_IMPLEMENTATION_REPORT.md)

---

## 💡 Tips & Best Practices

1. **Always use semantic HTML** (button, nav, header, etc.)
2. **Add ARIA labels** for icon-only buttons
3. **Use loading states** for async operations
4. **Provide empty states** for better UX
5. **Test keyboard navigation**
6. **Check color contrast** (WCAG AA)
7. **Use proper heading hierarchy** (h1-h6)
8. **Avoid animation overuse** (prefer reduced motion)

---

**Last Updated:** November 9, 2025
**Version:** 2.0.0
