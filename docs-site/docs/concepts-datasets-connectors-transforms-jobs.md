---
id: concepts-datasets-connectors-transforms-jobs
title: Datasets, Connectors, Transforms, Jobs
description: SDK nouns and how they relate.
slug: /concepts/datasets-connectors-transforms-jobs
---

### Connectors
- Identify integrations via `source_type`/`connector_type` (`nexla_sdk.models.sources.enums.SourceType`) and `sink_type` (`nexla_sdk.models.destinations.enums.DestinationType`).
- Credentials decouple secrets from resources; they are passed by ID on create/update APIs.
- Inspect connector metadata through `Source.connector`/`Destination.connector` to surface friendly names in tooling.

### Datasets (Nexsets)
- Every active source emits one or more nexsets recorded on `Source.data_sets` (list of `DataSetBrief`).
- Derived nexsets extend upstream datasets using `NexsetCreate` with either an embedded `transform` payload or a reusable `transform_id`.
- Nexsets expose linkage to destinations via `Nexset.data_sinks`.

```python
source = client.sources.get(source_id, expand=True)
print([ds.name for ds in source.data_sets])

nexset = client.nexsets.get(nexset_id)
print({sink.id: sink.sink_type for sink in nexset.data_sinks})
```

### Transforms
- Transform operations (`transform.operations`) describe how records are flattened, renamed, computed, and filtered.
- Store shared logic as templates, then reference it with `transform_id` to avoid duplication.
- Validation hooks (`output_schema_validation_enabled`, `output_validation_schema`) let you enforce schemas before data is delivered.

### Jobs & Runs
- A flow run corresponds to a specific execution of a source, nexset, or destination. Run metadata is exposed on models as `run_ids` (`RunInfo`).
- Pull operational metrics with `client.metrics.get_resource_metrics_by_run(...)` or `get_resource_daily_metrics(...)`.
- The `flows` endpoint can include run summaries when `include_run_metrics=True`.

```python
runs = client.metrics.get_resource_metrics_by_run(
    resource_type="data_sets",
    resource_id=nexset.id,
    groupby="runId"
)
for metric in runs.metrics:
    print(metric.run_id, metric.status, metric.records_processed)
```

By combining connector metadata, nexset lineage, and run metrics you can build lineage diagrams, orchestration dashboards, or data product catalogs entirely from the SDK without manual lookups in the Nexla UI.
