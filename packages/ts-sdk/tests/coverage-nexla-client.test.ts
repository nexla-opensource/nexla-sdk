import { describe, expect, it } from "vitest";
import { NexlaClient } from "../src/client/nexla-client.js";
import { AuthenticationError, RateLimitError, ServerError } from "../src/errors.js";

const createFetchSequence = (responses: Array<{ status: number; body?: unknown; headers?: Record<string, string> }>) => {
  const calls: Request[] = [];
  const fetchFn: typeof fetch = async (input, init) => {
    const request = input instanceof Request ? input : new Request(input, init);
    calls.push(request);

    const url = request.url;
    if (url.endsWith("/token")) {
      const body = JSON.stringify({ access_token: "token-1", expires_in: 3600 });
      return new Response(body, { status: 200, headers: { "content-type": "application/json" } });
    }

    const next = responses.shift() ?? { status: 200, body: {} };
    return new Response(JSON.stringify(next.body ?? {}), {
      status: next.status,
      headers: { "content-type": "application/json", ...(next.headers ?? {}) }
    });
  };
  return { fetchFn, calls };
};

describe("NexlaClient internal flows", () => {
  it("refreshes auth on 401 for service key", async () => {
    const { fetchFn, calls } = createFetchSequence([
      { status: 401, body: { message: "expired" } },
      { status: 200, body: [{ id: 1 }] }
    ]);

    const client = new NexlaClient({
      serviceKey: "svc",
      baseUrl: "https://example.com",
      fetch: fetchFn
    });

    const data = await client.request("get", "/flows");
    expect(Array.isArray(data)).toBe(true);
    expect(calls.length).toBeGreaterThanOrEqual(2);
  });

  it("maps rate limit errors with retry-after", async () => {
    const { fetchFn } = createFetchSequence([
      { status: 429, body: { message: "slow down" }, headers: { "retry-after": "5" } }
    ]);

    const client = new NexlaClient({
      serviceKey: "svc",
      baseUrl: "https://example.com",
      fetch: fetchFn,
      retry: { maxRetries: 0 }
    });

    await expect(client.request("get", "/flows")).rejects.toBeInstanceOf(RateLimitError);
  });

  it("maps 500 errors to ServerError", async () => {
    const { fetchFn } = createFetchSequence([
      { status: 500, body: { error: "boom" } }
    ]);

    const client = new NexlaClient({
      serviceKey: "svc",
      baseUrl: "https://example.com",
      fetch: fetchFn
    });

    await expect(client.request("get", "/flows")).rejects.toBeInstanceOf(ServerError);
  });

  it("throws AuthenticationError when using expired access token", async () => {
    const { fetchFn } = createFetchSequence([{ status: 401, body: { message: "invalid" } }]);

    const client = new NexlaClient({
      accessToken: "access",
      baseUrl: "https://example.com",
      fetch: fetchFn
    });

    await expect(client.request("get", "/flows")).rejects.toBeInstanceOf(AuthenticationError);
  });
});
