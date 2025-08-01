# Nexla SDK Testing Framework

This comprehensive testing framework provides multiple testing strategies for the Nexla SDK:

## 🏗️ Testing Architecture

### 1. **Unit Tests** (Primary Testing Strategy)
### 1. **Unit Tests** (Primary Testing Strategy)
- **Location**: `tests/unit/test_*.py`
- **Purpose**: Test business logic with mocked HTTP responses
- **Benefits**: Fast, reliable, no external dependencies
- **Coverage**: 90%+ of functionality

### 2. **Integration Tests** (Secondary Testing Strategy)
- **Location**: `tests/integration/test_*.py`
- **Purpose**: Test against real Nexla API with credentials
- **Benefits**: Validates actual API compatibility
- **Usage**: Run with `pytest -m integration`
- **Usage**: Run with `pytest -m integration`
### 3. **Property-Based Tests** (Fuzz Testing)
- **Location**: `tests/property/test_*.py`
- **Purpose**: Test with randomly generated data using Hypothesis
- **Benefits**: Discovers edge cases and validates model robustness
- **Coverage**: Input validation, serialization, edge cases
- **Benefits**: Discovers edge cases and validates model robustness
- **Coverage**: Input validation, serialization, edge cases

## 🚀 Quick Start

### Run All Unit Tests (Default)
```bash
python -m pytest
# or
python tests/run_tests.py
```

### Run Integration Tests (Requires API Credentials)
```bash
python tests/run_tests.py --integration
```

### Run Specific Test Categories
```bash
python -m pytest -m unit          # Unit tests only
python -m pytest -m integration   # Integration tests only
python -m pytest -m performance   # Performance tests only
```

### Run with Coverage
```bash
python tests/run_tests.py --coverage
```

## 📊 Test Categories

### Unit Tests (`test_*_unit.py`)
- ✅ **Resource Operations**: CRUD operations with mocked responses
- ✅ **Error Handling**: HTTP errors, validation errors, network errors
- ✅ **Model Validation**: Pydantic model creation and validation
- ✅ **Authentication**: Token handling and refresh logic
- ✅ **Serialization**: JSON serialization/deserialization

### Integration Tests (`test_*_integration.py`)
- ✅ **Real API Calls**: Test against actual Nexla API endpoints
- ✅ **End-to-End Workflows**: Complete user scenarios
- ✅ **Response Validation**: Verify real API response structures
- ✅ **Credential Management**: Test with actual credentials

### Property-Based Tests (`test_*_properties.py`)
- ✅ **Random Data Generation**: Test with generated valid/invalid data
- ✅ **Invariant Testing**: Verify properties hold across all inputs
- ✅ **Edge Case Discovery**: Find boundary conditions automatically
- ✅ **Serialization Round-Trip**: Ensure data integrity

## 🔧 Test Configuration

### Environment Variables for Integration Tests
Create a `.env` file in the `tests/` directory:
```bash
# Required: Nexla API URL
NEXLA_TEST_API_URL=https://dataops.nexla.io/nexla-api

# Required: Authentication (choose one)
NEXLA_TEST_SERVICE_KEY=your-service-key
# OR
NEXLA_TEST_ACCESS_TOKEN=your-access-token

# Optional: Configuration
NEXLA_TEST_API_VERSION=v1
NEXLA_TEST_LOG_LEVEL=INFO
```

### Check Environment Setup
```bash
python tests/run_tests.py --check-env
```

tests/
├── unit/test_credentials.py          # Unit tests with mocks
├── integration/test_credentials.py   # Integration tests with real API
├── property/test_credentials.py      # Property-based tests
└── ...
├── test_credentials_properties.py    # Property-based tests
└── ...
```

### Test Classes Organization
```python
class TestCredentialsResourceUnit:
    """Unit tests for CRUD operations"""
    
class TestCredentialsErrorHandling:
    """Error handling and exception tests"""
    
class TestCredentialsModels:
    """Model validation and serialization tests"""
```

## 🛠️ Mock Infrastructure

### Mock HTTP Client
```python
# Automatic mocking with fixtures
def test_example(mock_client, mock_http_client):
    # Setup mock response
    mock_response = [{"id": 1, "name": "Test"}]
    mock_http_client.add_response("/data_credentials", mock_response)
    
    # Test the client
    credentials = mock_client.credentials.list()
    assert len(credentials) == 1
```

### Mock Data Builders
```python
# Generate realistic test data
credential_data = MockResponseBuilder.credential(
    credential_id=123,
    name="Test Credential",
    credentials_type="s3"
)
```

## 🔍 Testing Best Practices

### 1. **Test Isolation**
- Each test is independent and can run in any order
- Mock client is reset between tests
- No shared state between tests

### 2. **Realistic Data**
- Use `MockResponseBuilder` for consistent test data
- Include edge cases (empty lists, null values, etc.)
- Test both success and failure scenarios

### 3. **Comprehensive Coverage**
- Test all CRUD operations
- Test error handling for all HTTP status codes
- Test model validation with valid/invalid data
- Test authentication scenarios

### 4. **Clear Test Names**
- Use descriptive test names that explain what's being tested
- Group related tests in classes
- Use parametrized tests for similar scenarios

## 📈 Test Metrics

### Current Coverage (as of latest run)
- **Unit Tests**: 31 tests, 100% pass rate
- **Integration Tests**: Depends on API credentials
- **Property Tests**: Hypothesis-based with 100+ examples each
- **Overall Coverage**: 85%+ code coverage target

### Test Performance
- **Unit Tests**: ~0.2 seconds (31 tests)
- **Integration Tests**: ~2-5 seconds (depends on API response time)
- **Property Tests**: ~3-4 seconds (depends on example count)

## 🧪 Adding New Tests

### 1. For New Resources
```python
# tests/test_newresource_unit.py
class TestNewResourceUnit:
    def test_list_success(self, mock_client, mock_http_client):
        # Setup mock response
        mock_response = [{"id": 1, "name": "Test"}]
        mock_http_client.add_response("/new_resources", mock_response)
        
        # Test
        result = mock_client.new_resource.list()
        assert len(result) == 1
```

### 2. For New Error Scenarios
```python
def test_new_error_case(self, mock_client, mock_http_client):
    error = create_http_error(422, "Validation failed")
    mock_http_client.add_response("/endpoint", error)
    
    with pytest.raises(NexlaValidationError):
        mock_client.resource.operation()
```

### 3. For New Models
```python
def test_new_model_validation(self):
    # Test valid data
    valid_data = {"required_field": "value"}
    model = NewModel(**valid_data)
    assert model.required_field == "value"
    
    # Test invalid data
    with pytest.raises(ValidationError):
        NewModel(required_field=None)
```

## 🎯 Test Markers

- `@pytest.mark.unit` - Unit tests (default)
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.performance` - Performance tests
- `@pytest.mark.slow` - Slow-running tests

## 📚 Additional Resources

- **Hypothesis Documentation**: https://hypothesis.readthedocs.io/
- **Pytest Documentation**: https://docs.pytest.org/
- **Pydantic Testing**: https://pydantic-docs.helpmanual.io/usage/validators/
- **Mock Strategies**: https://docs.python.org/3/library/unittest.mock.html

## 🔧 Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all test dependencies are installed
2. **Auth Errors**: Check environment variables for integration tests
3. **Mock Issues**: Verify mock responses match expected API structure
4. **Property Test Failures**: Review generated data and constraints

### Debug Commands
```bash
# Run tests with verbose output
pytest -v tests/test_credentials_unit.py

# Run specific test with debugging
pytest -v -s tests/test_credentials_unit.py::TestName::test_method

# Run tests with coverage and HTML report
pytest --cov=nexla_sdk --cov-report=html tests/
``` 