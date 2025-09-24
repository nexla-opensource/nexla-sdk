---
title: Create & Monitor a Pipeline
description: End-to-end example to create a flow and monitor it.
slug: /guides/pipeline
---

The SDK can provision the entire flow graph—credential → source → nexset transform → destination—and then poll run metrics. The example below wires an S3 ingestion source to an S3 analytics sink and captures health signals.

```python
from datetime import datetime, timedelta

from nexla_sdk import NexlaClient
from nexla_sdk.models.credentials.requests import CredentialCreate
from nexla_sdk.models.sources.requests import SourceCreate
from nexla_sdk.models.nexsets.requests import NexsetCreate
from nexla_sdk.models.destinations.requests import DestinationCreate

client = NexlaClient(service_key="<SERVICE_KEY>")

# Step 1: credential
s3_creds = client.credentials.create(CredentialCreate(
    name="Ops S3",
    credentials_type="s3",
    credentials={
        "access_key_id": "AKIA...",
        "secret_access_key": "***",
        "region": "us-east-1"
    }
))

# Step 2: source
source = client.sources.create(SourceCreate(
    name="Orders Raw",
    source_type="s3",
    data_credentials_id=s3_creds.id,
    source_config={
        "path": "ingest/orders/",
        "file_format": "json",
        "start.cron": "0 1 * * *"  # pull nightly
    }
))
client.sources.activate(source.id)

# Step 3: nexset transform
parent = next(
    (n for n in client.nexsets.list() if n.data_source_id == source.id),
    None
)
if parent is None:
    raise RuntimeError("Source has not emitted a nexset yet; re-run after first ingestion.")

transformed = client.nexsets.create(NexsetCreate(
    name="Orders Curated",
    parent_data_set_id=parent.id,
    has_custom_transform=True,
    transform={
        "version": 1,
        "operations": [
            {"operation": "flatten", "path": "line_items"},
            {"operation": "rename", "fields": {"line_items.sku": "sku"}},
            {"operation": "filter", "condition": "status != 'CANCELLED'"}
        ]
    }
))

# Step 4: destination
sink = client.destinations.create(DestinationCreate(
    name="Orders Analytics",
    sink_type="s3",
    data_set_id=transformed.id,
    data_credentials_id=s3_creds.id,
    sink_config={
        "path": "analytics/orders/",
        "data_format": "parquet",
        "file_compression": "snappy"
    }
))
client.destinations.activate(sink.id)

# Step 5: flow health
flow = client.flows.get_by_resource("data_sets", transformed.id)
client.flows.activate(flow.flows[0].id, all=True)

# Monitor daily volume and latest run status
window_end = datetime.utcnow().date()
window_start = window_end - timedelta(days=7)
metrics = client.metrics.get_resource_daily_metrics(
    resource_type="data_sets",
    resource_id=transformed.id,
    from_date=str(window_start),
    to_date=str(window_end)
)
print(metrics.status)

run_metrics = client.metrics.get_resource_metrics_by_run(
    resource_type="data_sets",
    resource_id=transformed.id,
    groupby="runId"
)
print(run_metrics.metrics[:3])
```

Tips:
- Use `client.credentials.probe_*` to validate connectors before activating the flow.
- `FlowCopyOptions(copy_entire_tree=True)` can clone the pipeline to a new project or environment.
- When automating, wrap activations in try/except and surface `RateLimitError.retry_after` for backoff guidance.
