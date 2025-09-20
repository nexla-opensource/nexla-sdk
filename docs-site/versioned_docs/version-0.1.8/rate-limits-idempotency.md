---
id: rate-limits-idempotency
title: Rate Limits & Idempotency
description: Handling rate limiting and safe retries.
slug: /rate-limits
---

### Rate Limiting Signals

- The SDK raises `RateLimitError` for HTTP `429` responses. `retry_after` is populated from the `Retry-After` header or JSON body when available (`nexla_sdk/client.py`).
- `RequestsHttpClient` enables `urllib3.Retry` with exponential backoff (`backoff_factor=0.5`) for transient status codes `429`, `502`, `503`, and `504`, covering `GET/POST/PUT/DELETE/PATCH` calls (`nexla_sdk/http_client.py`).
- Call `client.metrics.get_rate_limits()` to inspect per-resource quotas returned by the API.

```python
from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import RateLimitError

def list_sources_with_backoff(client: NexlaClient):
    try:
        return client.sources.list(per_page=100)
    except RateLimitError as exc:
        wait = exc.retry_after or 30
        print(f"Hit rate limit, retrying in {wait}s")
        raise
```

When building automation, combine the SDK's retry hints with your own queueing or circuit breaker logic. The built-in retries cover only a handful of attempts; long-running jobs should still honour the server provided wait time.

### Idempotency Expectations

- `GET`, `PUT`, and `DELETE` endpoints exposed by each resource are idempotent; repeating the same call produces the same state (standard REST semantics).
- `POST` endpoints create new resources. If a duplicate is attempted, Nexla responds with `409 Conflict`, which the SDK maps to `ResourceConflictError`. You can treat that exception as a signal that the resource already exists.
- Use natural identifiers to avoid duplicate POSTs. For example, look up a source by name or metadata before calling `client.sources.create(...)`.
- Many resources expose copy helpers (`copy`, `copy_entire_tree`, etc.) that are idempotent if you supply the same options. Prefer those when cloning flows instead of scripting bespoke object creation.
- For streaming destinations, align retries with connector semantics: Kafka sinks are safe to retry because offsets are controlled server side, while file-based sinks may require manual cleanup of partially written files.

A pattern for safe create/update retries:

```python
from nexla_sdk.exceptions import ResourceConflictError

payload = {...}

try:
    destination = client.destinations.create(payload)
except ResourceConflictError:
    # Fallback to updating the existing resource instead of failing the workflow
    existing = client.destinations.list(name=payload["name"], per_page=1)
    if existing:
        destination = client.destinations.update(existing[0].id, payload)
    else:
        raise
```

Always log the `operation`, `resource_type`, and `resource_id` attributes exposed on exceptions; they originate from the SDK and speed up investigations when replays are required.
