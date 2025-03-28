# Nexla Python SDK

A Python SDK for interacting with the Nexla API.

## Installation

```bash
pip install nexla-sdk
```

## Authentication

The Nexla SDK requires a Session Token for authentication. You can get this token from the Nexla UI:

1. Go to your Nexla UI instance (e.g., `https://dataops.nexla.io`)
2. Navigate to `/token` path in your browser (e.g., `https://dataops.nexla.io/token`)
3. Log in if prompted
4. Copy the access token provided

## Quick Start

```python
from nexla_sdk import NexlaClient

# Initialize the client with your token
client = NexlaClient(token="your_nexla_session_token")

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

### Working with Flows

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

### Working with Data Sources

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

### Working with Credentials

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

## Error Handling

The SDK provides specific error classes for different error types:

```python
from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError, NexlaAuthError, NexlaValidationError

client = NexlaClient(token="your_token")

try:
    flows = client.flows.list()
except NexlaAuthError:
    print("Authentication failed. Please check your token.")
except NexlaAPIError as e:
    print(f"API error: {str(e)}, Status code: {e.status_code}")
except NexlaValidationError as e:
    print(f"Validation error: {str(e)}")
```

## License

This project is licensed under the terms of the MIT license. 