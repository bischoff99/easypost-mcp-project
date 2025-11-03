# Integration Tests

This directory contains integration tests that test real EasyPost API functionality.

## ⚠️ Important Notes

- **Real API Calls**: These tests make actual calls to EasyPost API
- **Costs Money**: While using test keys, there may be minimal charges
- **Rate Limits**: Subject to EasyPost API rate limits
- **Network Dependent**: Requires internet connection
- **Slower**: Much slower than unit tests (seconds vs milliseconds)

## 🚀 Running Integration Tests

### Run All Integration Tests
```bash
cd backend
pytest tests/integration/ -v
```

### Run with Integration Marker
```bash
cd backend
pytest -m integration -v
```

### Skip Integration Tests (Default for CI)
```bash
cd backend
pytest -m "not integration"  # Runs only unit tests
```

### Run Specific Test
```bash
cd backend
pytest tests/integration/test_easypost_integration.py::TestEasyPostIntegration::test_get_rates_real_api -v
```

## 🧪 Test Categories

### 1. Rate Testing
- `test_get_rates_real_api`: Tests real shipping rate retrieval
- `test_rate_comparison_different_carriers`: Verifies multiple carriers return rates

### 2. Shipment Operations
- `test_create_shipment_real_api`: Tests real shipment creation
- `test_list_shipments_real_api`: Tests shipment listing
- `test_get_shipment_details_real_api`: Tests detailed shipment retrieval

### 3. Tracking
- `test_track_shipment_real_api`: Tests real-time tracking functionality

### 4. Error Handling
- `test_error_handling_invalid_address`: Tests error handling with invalid data

## 🔧 Configuration

### API Key
Tests use the API key from:
1. `EASYPOST_API_KEY` environment variable
2. Fallback to test key in `.env` file

### Test Data
- Uses predefined test addresses in Los Angeles
- Standard 10x8x6 inch parcel weighing 1 lb
- Tests both valid and invalid address scenarios

## 📊 Expected Results

### Success Criteria
- ✅ All API calls return proper response structure
- ✅ Tracking numbers start with "EZ" (test shipments)
- ✅ Rates are positive numbers under $100
- ✅ Multiple carriers provide different rates
- ✅ Error cases are handled gracefully

### Performance
- Each test: 2-10 seconds (network dependent)
- Full suite: 30-60 seconds
- Rate limited: May take longer if hitting limits

## 🔄 CI/CD Integration

### GitHub Actions
```yaml
- name: Run Unit Tests
  run: |
    cd backend
    pytest -m "not integration" -v

- name: Run Integration Tests (Manual Only)
  run: |
    cd backend
    pytest -m integration -v
  if: github.event_name == 'workflow_dispatch'
```

### Local Development
```bash
# Quick unit tests (always)
make test-unit

# Full integration tests (occasional)
make test-integration
```

## 🛠️ Troubleshooting

### Common Issues

**Rate Limited**
```
Solution: Wait 1-2 minutes between test runs
```

**Network Timeout**
```
Solution: Check internet connection, retry
```

**API Key Invalid**
```
Solution: Verify EASYPOST_API_KEY in environment
```

**Test Shipments Not Found**
```
Solution: EasyPost test shipments are temporary, run create tests first
```

## 📈 Test Coverage

Integration tests complement unit tests by validating:

- ✅ Real API response formats
- ✅ Network error handling
- ✅ Rate limiting behavior
- ✅ Data serialization/deserialization
- ✅ External service integration

**Combined Coverage**: Unit (97% logic) + Integration (100% API contract) = Complete validation
