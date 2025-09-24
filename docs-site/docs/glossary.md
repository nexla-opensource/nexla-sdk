---
id: glossary
title: Glossary
description: Common terms used in the Nexla SDK and platform.
slug: /glossary
---

- **Credential** — Secure connection details (username/password, keys, OAuth tokens) referenced by sources and destinations. Managed through `client.credentials` and modelled by `nexla_sdk.models.credentials.*`.
- **Source** — An ingress connector (`source_type`/`connector_type`) that ingests data into Nexla. Surfaces detected nexsets and run history (`client.sources`).
- **Destination** — An egress connector (`sink_type`) that delivers nexset data downstream (`client.destinations`).
- **Nexset (Dataset)** — A curated dataset produced by a source or transform. Defined via `NexsetCreate` and consumed by destinations (`client.nexsets`).
- **Transform** — Declarative operations (`transform.operations`) that map, filter, or enrich records before they become a nexset.
- **Flow / Flow Node** — A graph linking sources, nexsets, and destinations. Use `client.flows` to inspect activation state and run metrics.
- **Connector** — A concrete integration template (S3, Snowflake, Kafka, REST, etc.) referenced by type enums in `nexla_sdk.models.sources.enums` and `.destinations.enums`.
- **Ingest Method** — How a source acquires data (`BATCH`, `STREAMING`, `REAL_TIME`, etc.); see `Source.ingest_method`.
- **Run** — An execution instance of a source, nexset transform, or destination delivery. Accessible via `run_ids` on models and `client.metrics.get_resource_metrics_by_run`.
- **Project / Team / Organization** — Access-control constructs for scoping resources. Managed via `client.projects`, `client.teams`, and `client.organizations`.
- **Lookup (Data Map)** — Key/value reference data used in transforms (`client.lookups`).
- **Notification** — Alert definitions and events retrievable from `client.notifications`.
- **Rate Limit** — API quota enforced per tenant. Inspect via `client.metrics.get_rate_limits()`; violations raise `RateLimitError`.
- **Service Key** — Long-lived secret used to authenticate automation with `NexlaClient(service_key=...)`.
- **Telemetry** — Optional OpenTelemetry spans emitted when `trace_enabled=True` or global tracing is configured (`nexla_sdk/telemetry.py`).
