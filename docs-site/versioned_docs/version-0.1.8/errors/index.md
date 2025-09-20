---
title: Errors & Troubleshooting
description: Error catalog and common fixes.
slug: /errors
---

Common exceptions:

- `AuthenticationError`: Invalid or expired credentials. Fix: verify service key.
- `AuthorizationError`: Lacking permissions. Fix: adjust roles/scopes.
- `NotFoundError`: Resource not found. Fix: check IDs.
- `ValidationError`: Input validation failed. Fix: correct payloads.
- `RateLimitError`: Too many requests. Fix: backoff using `retry_after`.
- `ServerError`: Unexpected API errors. Fix: retry and contact support.

Traceability:

- nexla_sdk/exceptions.py:1
