# E2E Test Suite

## Overview

Comprehensive end-to-end tests for the EasyPost MCP Dashboard.

## Test Files

### `dashboard.test.js`

Tests all dashboard pages:

- Dashboard overview with stats and quick actions
- Shipments list page
- Tracking page
- Analytics page with charts and metrics
- Address book page
- Settings page
- Navigation between pages

### `shipment-crud.test.js`

Tests complete shipment CRUD operations:

- Create shipment with addresses
- Get rates from multiple carriers
- Buy label with selected rate
- Track shipment by tracking number
- List shipments with pagination
- Complete workflow end-to-end

## Running Tests

### Run all E2E tests

```bash
npm test -- src/tests/e2e/
```

### Run specific test file

```bash
npm test -- src/tests/e2e/dashboard.test.js
npm test -- src/tests/e2e/shipment-crud.test.js
```

### Run with coverage

```bash
npm run test:coverage -- src/tests/e2e/
```

### M3 Max Optimized (Parallel Execution)

```bash
npm test -- src/tests/e2e/ --threads=20
```

## Test Strategy

### Unit Tests

- Component rendering
- User interactions
- State management
- Error handling

### Integration Tests

- API calls
- Data flow
- Navigation
- Form submissions

### E2E Tests

- Complete workflows
- Multi-step processes
- Real API interactions
- Cross-page functionality

## Configuration

Tests use:

- **Vitest** - Test framework
- **Testing Library** - Component testing
- **MSW** - API mocking (when needed)
- **React Router** - Navigation testing

## Best Practices

1. **Isolation** - Each test is independent
2. **Cleanup** - Unmount components after tests
3. **Async** - Use `waitFor` for async operations
4. **Mocking** - Mock external dependencies
5. **Parallel** - Run tests in parallel for speed

## Performance

M3 Max optimization:

- 20 parallel test threads
- ~2-3 seconds for full E2E suite
- Memory efficient test execution

## Troubleshooting

### Tests failing locally

1. Ensure backend is running on `http://localhost:8000`
2. Check EasyPost API key is configured
3. Clear test cache: `npm test -- --clearCache`

### Slow test execution

1. Increase parallel threads: `--threads=28`
2. Run specific test suites instead of all
3. Check for unnecessary `waitFor` delays

### Flaky tests

1. Add explicit waits for async operations
2. Check for race conditions
3. Verify test data consistency

## CI/CD Integration

Tests run automatically on:

- Pull requests
- Pre-commit hooks (critical tests only)
- Pre-push (full suite)
- Production deployment (full suite + coverage)

## Coverage Goals

- **Unit tests**: 80%+ coverage
- **Integration tests**: 70%+ coverage
- **E2E tests**: Critical paths covered

## Future Improvements

- [ ] Visual regression testing
- [ ] Performance benchmarking
- [ ] Accessibility testing
- [ ] Load testing
- [ ] Browser compatibility testing
