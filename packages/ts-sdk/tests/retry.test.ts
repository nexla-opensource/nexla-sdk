import { describe, expect, it } from "vitest";
import { createFetchWithRetry } from "../src/client/http.js";

const createResponse = (status: number) =>
  new Response("{}", { status, headers: { "content-type": "application/json" } });

describe("createFetchWithRetry", () => {
  it("retries on retryable status codes", async () => {
    let calls = 0;
    const baseFetch: typeof fetch = async () => {
      calls += 1;
      if (calls < 3) return createResponse(503);
      return createResponse(200);
    };

    const fetchWithRetry = createFetchWithRetry(baseFetch, { maxRetries: 3, backoffMs: 1, maxBackoffMs: 5 });
    const response = await fetchWithRetry(new Request("https://example.com"));

    expect(response.status).toBe(200);
    expect(calls).toBe(3);
  });
});
