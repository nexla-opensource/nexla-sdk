---
id: quickstart
title: Quickstart
description: Copy-paste runnable Quickstart for Nexla Python SDK.
slug: /quickstart
---

```python
# Quickstart: List flows
import os
from nexla_sdk import NexlaClient

# Prefer service key authentication
os.environ.setdefault('NEXLA_SERVICE_KEY', 'REPLACE_WITH_YOUR_SERVICE_KEY')

client = NexlaClient()  # picks up NEXLA_SERVICE_KEY or NEXLA_ACCESS_TOKEN

# List flows (structure only)
flows = client.flows.list(flows_only=True)
for f in flows:
    print(f"Flow id={getattr(f, 'id', '?')} name={getattr(f, 'name', '?')}")
```

Notes:

- Set `NEXLA_API_URL` if you use a non-default endpoint.
- To enable tracing, set OTEL env vars as per your collector (see Observability).

