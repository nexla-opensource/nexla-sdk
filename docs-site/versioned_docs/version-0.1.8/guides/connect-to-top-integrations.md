---
title: Connect to Top Integrations
description: Create sources/destinations with common connectors.
slug: /guides/integrations
---

Nexla exposes the same connector palette used in the UI. `source_type` and `sink_type` accept the enumerated values defined in `nexla_sdk.models.sources.enums.SourceType` and `nexla_sdk.models.destinations.enums.DestinationType`. Below are working patterns for common integrations.

## Amazon S3 (Batch Files)

```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.credentials.requests import CredentialCreate
from nexla_sdk.models.sources.requests import SourceCreate
from nexla_sdk.models.destinations.requests import DestinationCreate
from nexla_sdk.models.sources.enums import SourceType
from nexla_sdk.models.destinations.enums import DestinationType

client = NexlaClient(service_key="<SERVICE_KEY>")

# Reusable credential for both the source and destination
s3_cred = client.credentials.create(CredentialCreate(
    name="Ops S3",
    credentials_type="s3",
    credentials={
        "access_key_id": "AKIA...",
        "secret_access_key": "***",
        "region": "us-east-1"
    }
))

# Source reads JSON objects on an hourly schedule
orders_source = client.sources.create(SourceCreate(
    name="Orders Ingest",
    source_type=SourceType.S3.value,
    data_credentials_id=s3_cred.id,
    source_config={
        "path": "raw/orders/",
        "file_format": "json",
        "start.cron": "0 * * * *"  # hourly
    }
))

# Destination writes Parquet snapshots back to S3
orders_export = client.destinations.create(DestinationCreate(
    name="Orders Export",
    sink_type=DestinationType.S3.value,
    data_credentials_id=s3_cred.id,
    data_set_id=123456,  # nexset you want to publish
    sink_config={
        "path": "analytics/orders/",
        "data_format": "parquet",
        "file_compression": "snappy"
    }
))
```

Key fields map 1:1 with the Nexla UI: `path`, `file_format`, and the cron expression (`start.cron`) configure polling for S3 sources, while `data_format` and optional compression control sinks.

## Snowflake (Cloud Warehouse)

```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.credentials.requests import CredentialCreate
from nexla_sdk.models.destinations.requests import DestinationCreate
from nexla_sdk.models.destinations.enums import DestinationType

client = NexlaClient(service_key="<SERVICE_KEY>")

snowflake_cred = client.credentials.create(CredentialCreate(
    name="Snowflake Warehouse",
    credentials_type="snowflake",
    credentials={
        "account": "my_account",
        "user": "INGEST_SERVICE",
        "password": "***",
        "warehouse": "LOAD_WH",
        "database": "RAW",
        "schema": "STAGING",
        "role": "SYSADMIN"
    }
))

snowflake_sink = client.destinations.create(DestinationCreate(
    name="Orders to Snowflake",
    sink_type=DestinationType.SNOWFLAKE.value,
    data_credentials_id=snowflake_cred.id,
    data_set_id=123456,
    sink_config={
        "table": "RAW.STAGING.ORDERS",
        "load_type": "merge",  # or "append"
        "key_columns": ["order_id"],
        "role": "SYSADMIN"
    }
))
```

Specify the fully-qualified table and any primary keys used for merge operations. Credentials should mirror the UI prompts (account locator, role, and warehouse).

## REST / HTTP APIs (Templatized)

```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.sources.requests import SourceCreate
from nexla_sdk.models.sources.enums import SourceType

client = NexlaClient(service_key="<SERVICE_KEY>")

api_source = client.sources.create(SourceCreate(
    name="CRM Contacts API",
    source_type=SourceType.REST.value,
    ingest_method="POLL",
    template_config={
        "request": {
            "method": "GET",
            "url": "https://api.example.com/v1/contacts",
            "headers": {"Authorization": "Bearer ${CREDENTIAL.token}"},
            "query_params": {"updated_after": "${LAST_SUCCESS_AT}"}
        },
        "pagination": {"type": "cursor", "cursor_field": "next_page"}
    }
))
```

Templatized connectors use `template_config` to describe HTTP method, authentication placeholders resolved via credentials, and pagination strategy. Switch `ingest_method` to `REAL_TIME` or `STREAMING` when using push-based APIs.

Consult the `SourceType` and `DestinationType` enums for the canonical connector identifiers (Kafka, GCS, BigQuery, MongoDB, etc.) and supply the config keys exactly as prompted in the Nexla UI or REST API reference.
