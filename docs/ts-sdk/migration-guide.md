# Migration Guide: Python SDK to TypeScript SDK

This guide maps common Python SDK patterns to their TypeScript SDK equivalents.

## Initialization and Auth Mapping

| Python SDK | TypeScript SDK |
| --- | --- |
| `NexlaClient(service_key="...")` | `new NexlaClient({ serviceKey: "..." })` |
| `NexlaClient(access_token="...")` | `new NexlaClient({ accessToken: "..." })` |
| `base_url=` | `baseUrl:` |
| `api_version=` | `apiVersion:` |

Shared environment variables:

- `NEXLA_SERVICE_KEY`
- `NEXLA_ACCESS_TOKEN`
- `NEXLA_API_URL`

## Core Call-Pattern Mapping

| Python pattern | TS pattern |
| --- | --- |
| `client.<resource>.list()` | `await client.<resource>.list()` |
| `client.<resource>.get(id)` | `await client.<resource>.get({ params: { path: { <id_field>: id } } })` |
| `client.<resource>.create(payload)` | `await client.<resource>.create({ body: payload })` |
| `client.request("get", "/flows")` | `await client.request("get", "/flows")` |
| synchronous return values | Promise-based (`await`) |

For non-CRUD endpoints, TS exposes operationId methods:

```ts
const activated = await client.flows.flow_activate_with_flow_id({
  params: { path: { flow_id: 123 } }
});
```

## Python to TS Resource Mapping Guidance

### One-to-one common resources

- `flows` -> `client.flows`
- `sources` -> `client.sources`
- `destinations` -> `client.destinations`
- `credentials` -> `client.credentials`
- `nexsets` -> `client.nexsets`
- `users` -> `client.users`
- `teams` -> `client.teams`
- `projects` -> `client.projects`
- `organizations` -> `client.organizations`

### Webhooks mapping

Python:

```python
webhooks = client.create_webhook_client(api_key="...")
```

TypeScript:

```ts
import { NexlaClient, WebhooksClient } from "@nexla/sdk";

// Option 1: standalone
const webhooks = new WebhooksClient({ apiKey: "..." });

// Option 2: attached to NexlaClient
const client = new NexlaClient({ serviceKey: "...", webhookApiKey: "..." });
await client.webhooks?.sendOneRecord("https://api.nexla.com/webhook/abc", { id: 1 });
```

### Python resources not yet first-class in TS

For resources that are still missing in TS as dedicated `client.<resource>` clients, use typed raw access:

```ts
const result = await client.raw.GET("/clusters");
```

Use [parity-matrix.md](./parity-matrix.md) as the current source of Python-to-TS parity status.

## Type Mapping Guidance

Python models are Pydantic-based. TS uses generated OpenAPI types.

```ts
import type { operations } from "@nexla/sdk";

type GetFlowResponse = operations["get_flow_by_id"]["responses"][200]["content"]["application/json"];
```

## Error Mapping

| Python exception | TS exception |
| --- | --- |
| `AuthenticationError` | `AuthenticationError` |
| `NotFoundError` | `NotFoundError` |
| `ValidationError` | `ValidationError` |
| `RateLimitError` | `RateLimitError` |
| `ServerError` | `ServerError` |
| `NexlaError` | `NexlaError` |

TS usage example:

```ts
import { AuthenticationError } from "@nexla/sdk";

try {
  await client.flows.list();
} catch (error) {
  if (error instanceof AuthenticationError) {
    // re-authenticate or fail fast
  }
  throw error;
}
```

## Practical Migration Checklist

1. Convert constructor args (`service_key` -> `serviceKey`, `access_token` -> `accessToken`).
2. Convert synchronous calls to `await`-based calls.
3. Move positional path args into `params.path` objects.
4. Move payload arguments into `body`.
5. For uncovered resources, use `client.raw` and track parity updates in [parity-matrix.md](./parity-matrix.md).

## Related Docs

- [Architecture](./architecture.md)
- [Coverage process](./api-coverage.md)
- [Generated parity matrix](./parity-matrix.md)
