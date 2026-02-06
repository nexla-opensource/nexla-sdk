# Nexla TypeScript SDK

TypeScript SDK for interacting with the Nexla API.

## Installation

```bash
npm install @nexla/sdk
```

## Authentication

### Service key (recommended)

```ts
import { NexlaClient } from "@nexla/sdk";

const client = new NexlaClient({ serviceKey: process.env.NEXLA_SERVICE_KEY });
```

### Access token

```ts
import { NexlaClient } from "@nexla/sdk";

const client = new NexlaClient({ accessToken: process.env.NEXLA_ACCESS_TOKEN });
```

Supported env vars:

- `NEXLA_SERVICE_KEY`
- `NEXLA_ACCESS_TOKEN`
- `NEXLA_API_URL`

## Quick Start

```ts
import { NexlaClient } from "@nexla/sdk";

const client = new NexlaClient({ serviceKey: process.env.NEXLA_SERVICE_KEY });

const flows = await client.flows.list();
const activated = await client.flows.flow_activate_with_flow_id({
  params: { path: { flow_id: 123 } }
});
```

## Raw OpenAPI Access

Use the raw client when you need direct path-level access:

```ts
const { data } = await client.raw.GET("/flows", {
  params: { query: { page: 1 } }
});
```

## Webhooks

```ts
import { WebhooksClient } from "@nexla/sdk";

const webhooks = new WebhooksClient({ apiKey: process.env.NEXLA_WEBHOOK_API_KEY });
await webhooks.sendOneRecord("https://api.nexla.com/webhook/abc", { id: 1 });
```

## SDK Configuration

```ts
const client = new NexlaClient({
  serviceKey: process.env.NEXLA_SERVICE_KEY,
  baseUrl: "https://dataops.nexla.io/nexla-api",
  apiVersion: "v1",
  retry: { maxRetries: 3 },
  userAgent: "my-app/1.2.3"
});
```

## Documentation Map

- [Architecture](../../docs/ts-sdk/architecture.md)
- [API coverage process](../../docs/ts-sdk/api-coverage.md)
- [Python to TS migration guide](../../docs/ts-sdk/migration-guide.md)
- [Generated parity matrix](../../docs/ts-sdk/parity-matrix.md)
- [Integration test policy (non-blocking)](../../docs/ts-sdk/integration-tests.md)

## Refreshing Generated Coverage Docs

From repository root:

```bash
pnpm -C packages/ts-sdk gen
node packages/ts-sdk/scripts/generate-parity-matrix.mjs
```

This regenerates TS OpenAPI artifacts and refreshes `docs/ts-sdk/parity-matrix.md`.

## License

MIT
