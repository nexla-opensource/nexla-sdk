---
id: sync-vs-streaming
title: Sync vs. Streaming
description: Data movement modes in Nexla.
slug: /concepts/sync-vs-streaming
---

Nexla resources expose scheduling metadata so you can reason about delivery patterns directly from the SDK.

### Batch & Scheduled Syncs
- `Source.ingest_method` reports `BATCH`, `POLL`, or `SCHEDULED` for time-based collection.
- File connectors (S3, GCS, Azure Blob, FTP, etc.) use cron expressions stored in `source.source_config["start.cron"]` and optional windowing fields.
- Destinations inherit the upstream cadence; use `client.metrics.get_resource_daily_metrics` to confirm volume per day.

### Streaming & Near Real-Time
- Streaming connectors (Kafka, Confluent Kafka, Google Pub/Sub) advertise `ingest_method="STREAMING"` and set `Source.flow_type` to `streaming`.
- Real-time API pushes (webhooks, event bridges) return `ingest_method="REAL_TIME"`.
- Destinations such as Kafka or Pub/Sub mirror the same mode with `Destination.flow_type` and push acknowledgements captured in run metrics.

```python
source = client.sources.get(source_id)
print(source.ingest_method, source.flow_type)

if source.ingest_method in {"STREAMING", "REAL_TIME"}:
    history = client.metrics.get_resource_metrics_by_run(
        resource_type="data_sources",
        resource_id=source.id,
        groupby="runId",
        orderby="-timestamp",
        size=5
    )
    for run in history.metrics:
        print(run.run_id, run.status, run.records_processed)
```

### Choosing the Right Mode
- Use batch/poll when reading from file systems or databases that expose periodic snapshots.
- Use streaming when the connector supports offsets or subscriptions (Kafka topics, Pub/Sub subscriptions).
- For webhook-style ingestion, register a Nexla endpoint and inspect deliveries through flow run metrics or the Nexla UI's webhook dashboard.

When migrating flows, validate that the `ingest_method` and `flow_type` values match the expected operational profile before activating destinations. These fields are the source of truth surfaced by the REST API and reflected in the SDK models.
