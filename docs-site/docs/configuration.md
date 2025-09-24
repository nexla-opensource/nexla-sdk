---
id: configuration
title: Configuration
description: Environment variables, defaults, and precedence.
slug: /configuration
---

The client reads configuration from constructor parameters first, then environment variables.

Priority:

1. Explicit constructor args
2. Environment variables
3. SDK defaults

Environment variables:

- `NEXLA_SERVICE_KEY`: used when no explicit `service_key` is provided.
- `NEXLA_ACCESS_TOKEN`: used when no `service_key` and `access_token` are provided.
- `NEXLA_API_URL`: used when no `base_url` is provided. Default: `https://dataops.nexla.io/nexla-api`.
- OpenTelemetry: `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`, `OTEL_EXPORTER_JAEGER_AGENT_HOST`, `OTEL_EXPORTER_ZIPKIN_ENDPOINT`, `OTEL_SERVICE_NAME`.

Traceability:

- nexla_sdk/client.py:88
- nexla_sdk/telemetry.py:100

