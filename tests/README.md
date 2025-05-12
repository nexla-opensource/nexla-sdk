# Nexla SDK Tests

This directory contains tests for the Nexla SDK.

## Test Types

The test suite includes both unit tests and integration tests:

- **Unit tests**: Test SDK functionality without making actual API calls, marked with `@pytest.mark.unit`
- **Integration tests**: Test the SDK against a real Nexla API instance, marked with `@pytest.mark.integration`

## Self-Reliant Integration Tests

Integration tests are designed to be fully self-contained:

1. Each test creates its own resources (sources, flows, credentials, etc.)
2. Tests validate functionality using these resources
3. Tests clean up by deleting all created resources in teardown fixtures

This approach ensures tests won't interfere with production data and prevents orphaned resources.

## Test Coverage

The SDK tests cover these core API resources:

- Sources
- Destinations
- Flows
- Nexsets (Data Sets)
- Transforms
- Credentials
- Lookups (Data Maps)
- Teams
- Users
- Organizations
- Projects
- Audit Logs
- Metrics
- Notifications
- Quarantine Settings
- Schemas

Each resource has comprehensive lifecycle tests (create, read, update, delete).

## Configuration

### Environment Variables

Integration tests require these environment variables:

```
NEXLA_TEST_API_URL=https://your-nexla-instance.nexla.io/nexla-api
NEXLA_TEST_SERVICE_KEY=your-service-key
NEXLA_TEST_API_VERSION=v1  # Optional, defaults to v1
NEXLA_TEST_LOG_LEVEL=DEBUG  # Optional, defaults to INFO
```

You can set these in a `.env` file in the tests directory.

## Running Tests

### All tests
```bash
pytest
```

### Only unit tests
```bash
pytest -m unit
```

### Only integration tests
```bash
pytest -m integration
```

### Specific API tests
```bash
# Test sources API
pytest tests/api/test_sources_integration.py

# Specific test function
pytest tests/api/test_sources_integration.py::TestSourcesIntegration::test_source_lifecycle
```

### Debugging Options

```bash
# Show test output
pytest -v

# More verbose output
pytest -vv

# Show logs during test execution
pytest -s

# Combine flags for debugging
pytest -vvs
```

## Test Structure

- `conftest.py`: Shared fixtures and test configuration
- `test_client_init.py`: Unit tests for client initialization
- `api/`: Integration tests for specific API endpoints

## Fixtures

Common fixtures in `conftest.py`:

- `nexla_client`: Configured NexlaClient instance for testing
- `api_url`: API URL from environment
- `service_key`: Service key from environment
- `api_version`: API version from environment

Resource-specific fixtures in each test file create test resources for that specific API area.

## Writing New Tests

When writing integration tests:

1. Use `@pytest.mark.integration` to mark integration tests
2. Create resource-specific fixtures with proper cleanup
3. Follow the test lifecycle pattern (create → read → update → delete)
4. Add appropriate validation using assertion statements
5. Include helpful logging for debugging 