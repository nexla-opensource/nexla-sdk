---
id: error-handling-retries
title: Error Handling & Retries
description: Error classes, HTTP mapping, and retry semantics.
slug: /error-handling
---

HTTP errors are mapped to rich exceptions with context:

- 400 → `ValidationError`
- 401 → `AuthenticationError`
- 403 → `AuthorizationError`
- 404 → `NotFoundError`
- 409 → `ResourceConflictError`
- 429 → `RateLimitError` (with `retry_after` if available)
- 5xx → `ServerError`

The underlying `RequestsHttpClient` configures automatic retries for transient HTTP status codes (429, 502, 503, 504) using urllib3 Retry.

Traceability:

- nexla_sdk/client.py:146
- nexla_sdk/http_client.py:73

