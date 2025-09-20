---
id: getting-started
title: Getting Started
description: Install, configure, and make your first request with the Nexla Python SDK.
slug: /getting-started
keywords: [install, setup, quickstart, authentication, configuration]
---

# Getting Started with Nexla Python SDK

This comprehensive guide will walk you through installing the SDK, configuring authentication, and making your first API requests to the Nexla platform.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.9 or higher** installed on your system
- **A Nexla account** with API access
- **Credentials**: Either a Service Key (recommended) or Access Token from your Nexla dashboard

:::tip Service Key vs Access Token
**Service Keys** are recommended for production use as they provide better security and don't expire. **Access Tokens** are useful for development but have limited lifespans.
:::

## Step 1: Installation

Install the Nexla SDK using pip:

```bash
# Install the latest version
pip install nexla-sdk

# Or install a specific version
pip install nexla-sdk==0.1.8

# For development with additional dependencies
pip install nexla-sdk[dev]
```

### Verify Installation

```python
import nexla_sdk
print(f"Nexla SDK version: {nexla_sdk.__version__}")
```

## Step 2: Authentication Setup

### Option A: Environment Variables (Recommended)

Set your credentials using environment variables:

```bash
# Using Service Key (recommended)
export NEXLA_SERVICE_KEY="your_service_key_here"

# OR using Access Token
export NEXLA_ACCESS_TOKEN="your_access_token_here"

# Optional: Set custom API endpoint
export NEXLA_API_URL="https://your-instance.nexla.io/nexla-api"
```

### Option B: Direct Configuration

```python
from nexla_sdk import NexlaClient

# Using Service Key
client = NexlaClient(service_key="your_service_key_here")

# Using Access Token
client = NexlaClient(access_token="your_access_token_here")

# With custom API URL
client = NexlaClient(
    service_key="your_service_key_here",
    api_url="https://your-instance.nexla.io/nexla-api"
)
```

### Option C: Configuration File

Create a `.env` file in your project root:

```bash
# .env file
NEXLA_SERVICE_KEY=your_service_key_here
NEXLA_API_URL=https://your-instance.nexla.io/nexla-api
```

Then load it in your Python code:

```python
from dotenv import load_dotenv
from nexla_sdk import NexlaClient

load_dotenv()  # Load environment variables from .env
client = NexlaClient()  # Automatically picks up credentials
```

## Step 3: Your First Request

Let's start with a simple example to verify everything is working:

```python
from nexla_sdk import NexlaClient

# Initialize the client
client = NexlaClient()

try:
    # List all flows in your account
    flows = client.flows.list()
    print(f"✅ Successfully connected! Found {len(flows)} flows")
    
    # Display flow information
    for flow in flows[:3]:  # Show first 3 flows
        print(f"  - Flow: {flow.name} (ID: {flow.id})")
        print(f"    Status: {flow.status}")
        print(f"    Created: {flow.created_time}")
        print()
        
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

## Step 4: Exploring Resources

The SDK provides access to all major Nexla resources. Here are some common operations:

### Working with Sources

```python
# List all data sources
sources = client.sources.list()
print(f"Found {len(sources)} data sources")

# Get a specific source
if sources:
    source = client.sources.get(sources[0].id)
    print(f"Source: {source.name} ({source.type})")
```

### Working with Destinations

```python
# List all destinations
destinations = client.destinations.list()
print(f"Found {len(destinations)} destinations")

# Get destination details
if destinations:
    dest = client.destinations.get(destinations[0].id)
    print(f"Destination: {dest.name} ({dest.type})")
```

### Working with Projects

```python
# List all projects
projects = client.projects.list()
print(f"Found {len(projects)} projects")

# Get current project info
if projects:
    project = client.projects.get(projects[0].id)
    print(f"Project: {project.name}")
    print(f"Description: {project.description}")
```

## Step 5: Error Handling

The SDK provides comprehensive error handling:

```python
from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError, AuthenticationError

client = NexlaClient()

try:
    # This might fail if flow doesn't exist
    flow = client.flows.get("non-existent-flow-id")
except AuthenticationError:
    print("❌ Authentication failed - check your credentials")
except NexlaAPIError as e:
    print(f"❌ API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

## Next Steps

Now that you have the SDK set up and working, explore these areas:

### 🚀 **Quick Actions**
- **[Quickstart Guide](quickstart)** - Copy-paste examples for common tasks
- **[Core Concepts](core-concepts)** - Understand Nexla's data model
- **[API Reference](api/python/overview)** - Complete method documentation

### 📋 **Common Use Cases**
- **[Authentication & Credentials](authentication-credentials)** - Detailed auth setup
- **[Examples](examples)** - Real-world code examples
- **[Error Handling](error-handling-retries)** - Robust error management

### 🔧 **Advanced Topics**
- **[Configuration](configuration)** - Advanced client configuration
- **[Observability](observability-logging-metrics-tracing)** - Logging and monitoring
- **[Rate Limits](rate-limits-idempotency)** - Best practices for API usage

:::info Need Help?
If you encounter any issues, check our [FAQ](faq) or review the [Troubleshooting](errors) section.
:::

