---
id: index
title: Nexla Python SDK
description: A comprehensive Python SDK for building, operating, and observing data pipelines with the Nexla API.
slug: /
keywords: [Nexla, SDK, Python, data, integration, pipelines, ETL, data engineering]
---

# Nexla Python SDK

The **Nexla Python SDK** is a comprehensive, typed client library that enables developers to programmatically interact with the Nexla data platform. Built with modern Python practices, it provides an intuitive interface for building, operating, and monitoring data pipelines at scale.

## 🚀 Key Features

### **Complete API Coverage**
- **Resources**: Flows, sources, destinations, nexsets, lookups, users, organizations, teams, projects, notifications, and metrics
- **Full CRUD Operations**: Create, read, update, and delete operations for all supported resources
- **Bulk Operations**: Efficient batch processing capabilities

### **Developer Experience**
- **Type Safety**: Full type hints with Pydantic v2-based models for requests and responses
- **IDE Support**: Rich autocomplete and inline documentation
- **Validation**: Automatic request/response validation and error handling

### **Enterprise Ready**
- **Authentication**: Service Key (recommended) or Access Token authentication
- **Reliability**: Built-in retries, error mapping, and robust HTTP client
- **Observability**: Optional OpenTelemetry tracing for monitoring and debugging
- **Python 3.9+**: Compatible with modern Python versions

## 📋 What You Can Build

- **Data Pipelines**: Create and manage complex ETL/ELT workflows
- **Data Integration**: Connect disparate data sources and destinations
- **Monitoring & Alerting**: Set up notifications and track pipeline metrics
- **Automation**: Automate data operations and pipeline management
- **Analytics**: Query and analyze pipeline performance data

## 🏁 Quick Start

```python
from nexla_sdk import NexlaClient

# Initialize client (reads NEXLA_SERVICE_KEY from environment)
client = NexlaClient()

# List all your data flows
flows = client.flows.list()
print(f"Found {len(flows)} flows")

# Get flow details
flow = client.flows.get(flow_id="your-flow-id")
print(f"Flow '{flow.name}' status: {flow.status}")
```

## 📚 Documentation Structure

- **[Getting Started](getting-started)** - Installation, setup, and first request
- **[Quickstart](quickstart)** - Copy-paste examples to get running quickly
- **[Core Concepts](core-concepts)** - Understanding Nexla's data model
- **[API Reference](api/python/overview)** - Complete API documentation
- **[Examples](examples)** - Real-world use cases and patterns

## 🛠️ Installation

```bash
pip install nexla-sdk
```

**Requirements**: Python 3.9+ 

## 🔗 Next Steps

Ready to start building? Choose your path:

- **New to Nexla?** → [Core Concepts](core-concepts)
- **Ready to code?** → [Getting Started](getting-started)
- **Want examples?** → [Quickstart](quickstart)
- **Need API details?** → [API Reference](api/python/overview)
