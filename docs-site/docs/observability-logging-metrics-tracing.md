---
id: observability-logging-metrics-tracing
title: Observability (logging, metrics, tracing)
description: Enable OpenTelemetry tracing for HTTP calls; logging hooks.
slug: /observability
---

Tracing: When OpenTelemetry is configured globally, the SDK adds spans per HTTP request.

- Auto-detection via `is_tracing_configured()` checks tracer provider and common OTEL env vars.
- Attributes: `http.method`, `url.full`, `server.address`, `http.status_code`, `component=nexla-sdk`.
- Trace context propagation via W3C trace headers when OTEL is available.

To explicitly control tracing, pass `trace_enabled=True|False` to `NexlaClient`. If omitted, tracing auto-enables when a global OTEL tracer provider is detected.

Enable (example):

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_SERVICE_NAME=nexla-sdk-example
```

Programmatic enablement example:

```python
from nexla_sdk import NexlaClient

# Force enable tracing regardless of global config
client = NexlaClient(service_key="<SERVICE_KEY>", trace_enabled=True)
```
