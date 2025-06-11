# Nexla Python SDK

A Python SDK for interacting with the Nexla API.

## Installation

```bash
pip install nexla-sdk
```

## Authentication

The Nexla SDK requires a Service Key for authentication. You can create a service key from the Nexla UI:

1. Go to your Nexla UI instance (e.g., `https://dataops.nexla.io`)
2. Navigate to the **Authentication** screen in the **Settings** section
3. Click the **Create Service Key** button
4. Store the service key securely - it should be treated as highly sensitive since it is equivalent to your account password

## Quick Start

```python
from nexla_sdk import NexlaClient

# Initialize the client with your service key
client = NexlaClient(service_key="your_nexla_service_key")

# List flows - returns a FlowList object with typed items
flows = client.flows.list()
print(f"Found {flows.total} flows")

# Access Flow objects with proper typing
for flow in flows.items:
    print(f"Flow name: {flow.name}, ID: {flow.id}")
    print(f"Active: {flow.config.is_active}")

# Get a specific flow - returns a Flow object
flow = client.flows.get("flow_id")
print(f"Flow details: {flow.name}, type: {flow.flow_type}")

# Create a data source
source_data = {
    "name": "My New Source",
    "description": "Created via SDK",
    "config": {
        "connector_type": "file",
        # Additional configuration...
    }
}

# Returns a Source object with proper typing
new_source = client.sources.create(source_data)
print(f"Created source: {new_source.id}, name: {new_source.name}")
```

## Features

The SDK provides access to the following Nexla API features:

* Flows management
* Sources management
* Destinations (Data Sinks) management
* Nexsets (Data Sets) management
* Credentials management
* Data Maps (Lookups) management
* Transforms management
* Webhooks integration
* Organization management
* User management
* Teams management
* Projects management
* Audit Logs
* Metrics
* Notifications
* Schemas
* Quarantine Settings

## Type-Safe Models

The Nexla SDK uses Pydantic models to provide type safety and validation for API responses. All API methods return properly typed model objects instead of raw dictionaries:

```python
# Get a flow - returns a Flow object
flow = client.flows.get("flow_id")

# Access properties with proper typing
print(flow.name)
print(flow.config.is_active)
print(flow.status.status if flow.status else "No status")

# List sources - returns a SourceList object
sources = client.sources.list()

# Access typed items
for source in sources.items:
    print(f"Source: {source.name}")
    print(f"Connector type: {source.config.connector_type}")
```

## Examples

The Nexla SDK comes with a comprehensive set of examples in the `examples/api/` directory:

### Example Structure

- `examples/api/client.py` - Base client configuration used by all examples
- Resource-specific examples:
  - `examples/api/flows.py` - Flow operations (listing, retrieval, activation/pause)
  - `examples/api/sources.py` - Data source operations (listing, creation, updating, inspection)
  - `examples/api/destinations.py` - Data destination operations 
  - `examples/api/nexsets.py` - Nexset (dataset) operations
  - `examples/api/credentials.py` - Credential management
  - `examples/api/transforms.py` - Data transformation operations
  - `examples/api/lookups.py` - Data Maps (Lookups) examples
  - `examples/api/teams.py` - Team management examples
  - `examples/api/users.py` - User management examples
  - And more resource-specific examples (audit_logs, metrics, notifications, etc.)

### Running the Examples

To run these examples:

1. Clone the repository
2. Create a `.env` file with your Nexla credentials:
   ```
   NEXLA_SERVICE_KEY=your_service_key
   NEXLA_API_URL=your_api_url  # Optional, defaults to standard Nexla API URL
   ```
3. Run any example script, for instance:
   ```bash
   python examples/api/flows.py
   ```

### Example: Working with Flows

```python
# List all flows - returns a FlowList
flows = client.flows.list()

# Get details of a specific flow - returns a Flow
flow = client.flows.get("flow_id")

# Activate a flow - returns the updated Flow
activated_flow = client.flows.activate("flow_id")
print(f"Flow activated: {activated_flow.config.is_active}")

# Pause a flow - returns the updated Flow
paused_flow = client.flows.pause("flow_id")
print(f"Flow active: {paused_flow.config.is_active}")

# Create a copy of a flow - returns the new Flow
new_flow = client.flows.copy("flow_id", new_name="Copy of my flow")
print(f"New flow created: {new_flow.id}, name: {new_flow.name}")
```

### Example: Working with Data Sources

```python
# List all data sources - returns a SourceList
sources = client.sources.list()

# Get details of a specific data source - returns a Source
source = client.sources.get("source_id")

# Create a new data source - returns a Source
source_config = {
    "name": "My API Source",
    "description": "Created via SDK",
    "config": {
        "connector_type": "rest_api",
        # Other configuration properties...
    }
}
new_source = client.sources.create(source_config)
print(f"New source ID: {new_source.id}")

# Activate a data source - returns the updated Source
activated_source = client.sources.activate("source_id")
```

### Example: Working with Credentials

```python
# List all credentials - returns a CredentialList
credentials = client.credentials.list()

# Create a new credential - returns a Credential
cred_config = {
    "name": "AWS S3 Credential",
    "credential_type": "aws_s3",
    "credential_details": {
        "credential_type": "aws_s3",
        "properties": {
            "access_key": "your_access_key",
            "secret_key": "your_secret_key",
            "region": "us-west-2"
        }
    }
}
new_credential = client.credentials.create(cred_config)
print(f"New credential ID: {new_credential.id}")

# Test a credential - returns a ProbeResult
probe_result = client.credentials.probe("credential_id")
print(f"Probe success: {probe_result.success}")

# Get a directory tree for a credential - returns a DirectoryTree
tree = client.credentials.probe_tree("credential_id", path="/some/path")
for item in tree.items:
    print(f"{item.name} ({item.type}): {item.path}")
```

## Additional Example Features

The SDK examples cover advanced operations such as:

- Audit logging and compliance tracking
- User and team permissions management
- Data transformation and schema handling
- Metrics collection and monitoring
- Notification systems integration
- Quarantine settings for data validation

See the `examples/api/` directory for detailed examples of these operations.

## Error Handling

The SDK provides specific error classes for different error types:

```python
from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError, NexlaAuthError, NexlaValidationError

client = NexlaClient(service_key="your_nexla_service_key")

try:
    flows = client.flows.list()
except NexlaAuthError:
    print("Authentication failed. Please check your service key.")
except NexlaAPIError as e:
    print(f"API error: {str(e)}, Status code: {e.status_code}")
except NexlaValidationError as e:
    print(f"Validation error: {str(e)}")
```

## License

This project is licensed under the terms of the MIT license. 

## Development

### Running Integration Tests

The SDK includes a comprehensive suite of integration tests that verify the functionality against a real Nexla API instance. These tests create temporary test resources, perform operations on them, and then clean up.

To run the integration tests:

1. Set up your environment variables:
   ```bash
   export NEXLA_TEST_API_URL="https://your-nexla-api-url"
   export NEXLA_TEST_SERVICE_KEY="your-nexla-service-key"
   export NEXLA_TEST_API_VERSION="v1"  # Optional, defaults to v1
   export NEXLA_TEST_LOG_LEVEL="INFO"  # Optional, defaults to INFO
   ```

   Alternatively, create a `.env` file in the project root or tests directory with these variables.

2. Run the tests using the provided script:
   ```bash
   ./run_integration_tests.py
   ```

   Or use pytest directly:
   ```bash
   pytest -v -m integration tests/api/
   ```

The integration tests cover:
- Flows API (create, get, update, delete, list, activate/pause, tags)
- Sources API (create, get, update, delete, list, activate/pause)
- Nexsets API (Data Sets) (create, get, update, delete, list, schema, samples)
- Projects API (create, get, update, delete, list, add/remove flows)
- Users API (get current user, preferences, list users, metrics)

*Note: These tests require API credentials with appropriate permissions to create and manage resources.* 