import { describe, expect, it } from "vitest";
import { NexlaClient } from "../src/client/nexla-client.js";

const createMockFetch = () => {
  const fetchFn: typeof fetch = async () => {
    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { "content-type": "application/json" }
    });
  };
  return fetchFn;
};

describe("ResourceClient errors", () => {
  it("skips resources without OpenAPI operations", () => {
    const fetchFn = createMockFetch();
    const client = new NexlaClient({
      accessToken: "access-token",
      baseUrl: "https://example.com",
      fetch: fetchFn
    });

    const apiKeys = (client as { api_keys?: unknown }).api_keys;
    expect(apiKeys).toBeUndefined();
  });
});
