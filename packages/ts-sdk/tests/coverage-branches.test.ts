import { describe, expect, it } from "vitest";
import { createFetchWithRetry } from "../src/client/http.js";
import { ServiceKeyAuthProvider } from "../src/auth/service-key.js";
import { NexlaClient } from "../src/client/nexla-client.js";

const createResponse = (status: number, contentType = "application/json") =>
  new Response("{}", { status, headers: { "content-type": contentType } });

describe("branch coverage extras", () => {
  it("does not retry on non-retryable status", async () => {
    let calls = 0;
    const baseFetch: typeof fetch = async () => {
      calls += 1;
      return createResponse(400);
    };

    const fetchWithRetry = createFetchWithRetry(baseFetch, { maxRetries: 2, backoffMs: 1, maxBackoffMs: 5 });
    const response = await fetchWithRetry(new Request("https://example.com"));

    expect(response.status).toBe(400);
    expect(calls).toBe(1);
  });

  it("handles non-json responses in service key auth", async () => {
    const fetchFn: typeof fetch = async (input, init) => {
      const request = input instanceof Request ? input : new Request(input, init);
      if (request.url.endsWith("/token")) {
        return createResponse(200, "text/plain");
      }
      return createResponse(200);
    };

    const provider = new ServiceKeyAuthProvider({
      serviceKey: "svc",
      baseUrl: "https://example.com",
      apiVersion: "v1",
      tokenRefreshMargin: 1,
      fetchFn
    });

    await expect(provider.getAccessToken()).rejects.toThrow();
  });

  it("defaults error message when response body is not JSON", async () => {
    const fetchFn: typeof fetch = async () => {
      return new Response("no-json", { status: 500, headers: { "content-type": "text/plain" } });
    };

    const client = new NexlaClient({
      accessToken: "access-token",
      baseUrl: "https://example.com",
      fetch: fetchFn
    });

    await expect(client.request("get", "/flows")).rejects.toThrow();
  });
});
