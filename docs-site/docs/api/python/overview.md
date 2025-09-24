---
id: api-python-overview
title: API Reference — Python
sidebar_label: Overview
description: Complete API reference for the Nexla Python SDK with detailed method documentation.
slug: /api/python/overview
keywords: [API, reference, methods, classes, documentation, Python SDK]
---

# API Reference — Python

Welcome to the complete API reference for the Nexla Python SDK. This documentation provides detailed information about all classes, methods, parameters, return types, and error handling.

## 📚 Documentation Structure

This API reference is **automatically generated** from the source code using Python introspection, ensuring it's always up-to-date with the latest SDK version.

### Organization

- **[Client](modules/nexla_sdk/client)** - Main `NexlaClient` class and initialization
- **[Resources](modules/nexla_sdk/resources)** - All API resource classes (flows, sources, destinations, etc.)
- **[Models](modules/nexla_sdk/models)** - Pydantic data models for requests and responses
- **[Exceptions](modules/nexla_sdk/exceptions)** - Error handling and exception classes
- **[Authentication](modules/nexla_sdk/auth)** - Authentication mechanisms
- **[HTTP Client](modules/nexla_sdk/http_client)** - Low-level HTTP communication

## 🔧 Core Components

### NexlaClient
The main entry point for all SDK operations. Provides access to all resource managers.

```python
from nexla_sdk import NexlaClient

client = NexlaClient(service_key="your_key")
```

### Resource Managers
Each resource type has its own manager with standard CRUD operations:

- **`client.flows`** - Data flow management
- **`client.sources`** - Data source operations  
- **`client.destinations`** - Destination management
- **`client.nexsets`** - Dataset operations
- **`client.projects`** - Project management
- **`client.users`** - User management
- **`client.organizations`** - Organization operations
- **`client.teams`** - Team management
- **`client.notifications`** - Notification handling
- **`client.metrics`** - Performance metrics
- **`client.lookups`** - Lookup table operations

### Standard Operations
Most resource managers support these operations:

- **`list()`** - Get all resources with optional filtering
- **`get(id)`** - Get a specific resource by ID
- **`create(data)`** - Create a new resource
- **`update(id, data)`** - Update an existing resource
- **`delete(id)`** - Delete a resource

## 📖 How to Read the Documentation

### Method Signatures
```python
def create_flow(
    name: str,
    description: Optional[str] = None,
    project_id: Optional[str] = None
) -> FlowResponse
```

### Parameter Documentation
- **name** (`str`, required) - The flow name
- **description** (`str`, optional) - Flow description  
- **project_id** (`str`, optional) - Target project ID

### Return Types
All methods return typed Pydantic models with full validation.

### Error Handling
Methods may raise:
- `AuthenticationError` - Invalid credentials
- `NexlaAPIError` - API-specific errors
- `ValidationError` - Invalid input data

## 🔍 Quick Navigation

### By Use Case
- **Getting Started**: [Client](modules/nexla_sdk/client) → [Projects](modules/nexla_sdk/resources/projects)
- **Data Pipelines**: [Flows](modules/nexla_sdk/resources/flows) → [Sources](modules/nexla_sdk/resources/sources) → [Destinations](modules/nexla_sdk/resources/destinations)
- **Monitoring**: [Metrics](modules/nexla_sdk/resources/metrics) → [Notifications](modules/nexla_sdk/resources/notifications)
- **Administration**: [Users](modules/nexla_sdk/resources/users) → [Teams](modules/nexla_sdk/resources/teams) → [Organizations](modules/nexla_sdk/resources/organizations)

### By Category
- **Core**: [Client](modules/nexla_sdk/client), [Auth](modules/nexla_sdk/auth), [Exceptions](modules/nexla_sdk/exceptions)
- **Data Flow**: [Flows](modules/nexla_sdk/resources/flows), [Nexsets](modules/nexla_sdk/resources/nexsets)
- **Connectivity**: [Sources](modules/nexla_sdk/resources/sources), [Destinations](modules/nexla_sdk/resources/destinations)
- **Management**: [Projects](modules/nexla_sdk/resources/projects), [Lookups](modules/nexla_sdk/resources/lookups)

## 📋 Model Reference

### Request Models
Located in `models/{resource}/requests.py`:
- Input validation and serialization
- Required and optional field definitions
- Type hints for IDE support

### Response Models  
Located in `models/{resource}/responses.py`:
- API response parsing and validation
- Nested object handling
- Computed properties and methods

### Enumeration Types
Located in `models/{resource}/enums.py`:
- Valid values for choice fields
- Status codes and types
- Configuration options

## 🔄 Regenerating Documentation

The API documentation is automatically generated from source code:

```bash
# From the docs-site directory
python3 scripts/gen_api_docs.py
```

This ensures the documentation always reflects the current codebase and includes:
- All public methods and their signatures
- Complete parameter documentation
- Return type information
- Exception specifications
- Usage examples where available

## 📊 Coverage and Quality

- **Coverage Status**: Tracked in project REPORT.md
- **Known Gaps**: Missing documentation is logged and prioritized
- **Updates**: Documentation regenerated on each release
- **Validation**: Type checking and example testing ensure accuracy

## 💡 Usage Tips

1. **Start with the Client**: Begin at [NexlaClient](modules/nexla_sdk/client) for initialization patterns
2. **Follow the Models**: Check request/response models for exact field requirements
3. **Handle Errors**: Review [Exceptions](modules/nexla_sdk/exceptions) for proper error handling
4. **Check Examples**: Many methods include usage examples in their documentation

## 🆘 Need Help?

- **Getting Started**: [Installation and Setup](../../getting-started)
- **Quick Examples**: [Quickstart Guide](../../quickstart)  
- **Core Concepts**: [Understanding Nexla](../../core-concepts)
- **Troubleshooting**: [Common Issues](../../errors)

---

:::info Auto-Generated Content
This documentation is automatically generated from the source code. For the most current information, always refer to the latest SDK version.
:::

