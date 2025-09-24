---
id: getting-started
title: Getting Started
description: Install, configure, and make your first request with Nexla Python SDK.
slug: /getting-started
keywords: [install, setup, quickstart]
---

This guide walks you through installing the SDK, configuring credentials, and listing a resource.

Prerequisites:

- Python 3.9+
- A Nexla Service Key (recommended) or Access Token

Install:

```bash
pip install nexla-sdk
```

Set credentials via environment variables:

```bash
export NEXLA_SERVICE_KEY="REDACTED_SERVICE_KEY"  # or NEXLA_ACCESS_TOKEN
export NEXLA_API_URL="https://dataops.nexla.io/nexla-api"  # optional
```

Minimal example:

```python
from nexla_sdk import NexlaClient

client = NexlaClient()  # Reads env vars by default
flows = client.flows.list()
print(flows)
```

Next steps:

- Read Authentication & Credentials
- Explore Core Concepts
- Browse API Reference

