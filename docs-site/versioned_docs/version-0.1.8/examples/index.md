---
title: Examples / Recipes
description: Minimal, runnable snippets for common tasks.
slug: /examples
---

- List sources

```python
from nexla_sdk import NexlaClient
client = NexlaClient()
print(client.sources.list(per_page=5))
```

- Get a destination

```python
from nexla_sdk import NexlaClient
client = NexlaClient()
print(client.destinations.get(123))
```

## End-to-End Pipeline (S3 → Nexset → S3)

Prerequisites:
- A Nexla service key with access to manage credentials, sources, nexsets, and destinations.
- An S3 location for reading (`s3://my-ingest-bucket/data/`) and one for writing (`s3://my-analytics-bucket/exports/`).

```python
from datetime import datetime, timedelta

from nexla_sdk import NexlaClient
from nexla_sdk.models.credentials.requests import CredentialCreate
from nexla_sdk.models.sources.requests import SourceCreate
from nexla_sdk.models.nexsets.requests import NexsetCreate
from nexla_sdk.models.destinations.requests import DestinationCreate

client = NexlaClient(service_key="<SERVICE_KEY>")

# 1. Register reusable credentials for Amazon S3.
credential = client.credentials.create(CredentialCreate(
    name="Analytics S3",
    credentials_type="s3",
    credentials={
        "access_key_id": "AKIA...",
        "secret_access_key": "***",
        "region": "us-east-1"
    }
))

# 2. Create and activate an S3 source that reads JSON files nightly.
source = client.sources.create(SourceCreate(
    name="Orders Raw",
    source_type="s3",
    data_credentials_id=credential.id,
    source_config={
        "path": "my-ingest-bucket/data/",
        "file_format": "json",
        "start.cron": "0 2 * * *"  # 02:00 UTC daily pull
    }
))
client.sources.activate(source.id)

# 3. Discover the detected nexset (dataset) produced by the source.
detected = client.nexsets.list()
source_nexsets = [n for n in detected if n.data_source_id == source.id]
if not source_nexsets:
    raise RuntimeError("Source has not emitted data yet; rerun after the first poll.")

parent = source_nexsets[0]

# 4. Create a derived nexset with a light transform (pass-through in this example).
transformed = client.nexsets.create(NexsetCreate(
    name="Orders Clean",
    parent_data_set_id=parent.id,
    has_custom_transform=True,
    transform={
        "version": 1,
        "operations": [
            {
                "operation": "shift",
                "spec": {"*": "&"}  # passthrough schema until custom mapping is required
            }
        ]
    }
))

# 5. Land the transformed data back to S3 and activate the sink.
destination = client.destinations.create(DestinationCreate(
    name="Orders S3 Export",
    sink_type="s3",
    data_set_id=transformed.id,
    data_credentials_id=credential.id,
    sink_config={
        "path": "my-analytics-bucket/exports/orders/",
        "data_format": "parquet",
        "file_compression": "snappy"
    }
))
client.destinations.activate(destination.id)

# 6. Monitor operational health with metrics.
date_to = datetime.utcnow().date()
date_from = date_to - timedelta(days=1)
stats = client.metrics.get_resource_daily_metrics(
    resource_type="data_sources",
    resource_id=source.id,
    from_date=str(date_from),
    to_date=str(date_to)
)
print(stats.status)
```

The same pattern works for other connectors: swap `source_type`/`sink_type` and adjust the `source_config`/`sink_config` payloads to match the Nexla UI fields for the integration you are targeting.
