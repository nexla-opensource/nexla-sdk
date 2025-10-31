---
id: authentication-credentials
title: Authentication & Credentials
description: Service Key (recommended) or Access Token authentication.
slug: /auth
---

The SDK supports two authentication methods via `nexla_sdk.client.NexlaClient`.

- Service Key (recommended): long-lived credential; SDK obtains session tokens on demand.
- Access Token: pre-obtained token; SDK does not refresh it.

Environment variables:

- `NEXLA_SERVICE_KEY` — service key in Basic format
- `NEXLA_ACCESS_TOKEN` — direct access token
- `NEXLA_API_URL` — API base URL (defaults to `https://dataops.nexla.io/nexla-api`)

Examples:

```python
from nexla_sdk import NexlaClient

# 1) Service key (preferred)
client = NexlaClient(service_key="REDACTED")

# 2) Access token
client = NexlaClient(access_token="REDACTED")

# Auto from env
client = NexlaClient()
```

Token and session management:

- `client.get_access_token()` — returns a valid token (obtains one if needed in service-key mode)
- `client.refresh_access_token()` — forces obtaining a fresh token (service-key mode)
- `client.logout()` — ends the current session and invalidates token

Errors:

- `AuthenticationError` on invalid credentials or expired direct tokens.
- `NexlaError` for other failures during token obtain/refresh.

Notes:

- Only one auth method should be provided — either service key or access token.
- When using direct access tokens, the SDK cannot refresh them.
