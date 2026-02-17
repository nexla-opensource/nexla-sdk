import { describe, expect, it } from "vitest";
import { createFetchWithRetry } from "../src/client/http.js";

const createResponse = (status: number, retryAfter?: string) =>
  new Response("{}", {
    status,
    headers: {
      "content-type": "application/json",
      ...(retryAfter ? { "retry-after": retryAfter } : {})
    }
  });

describe("createFetchWithRetry", () => {
  it("respects retry-after header", async () => {
    let calls = 0;
    const baseFetch: typeof fetch = async () => {
      calls += 1;
      if (calls === 1) return createResponse(429, "0");
      return createResponse(200);
    };

    const fetchWithRetry = createFetchWithRetry(baseFetch, { maxRetries: 2, backoffMs: 1, maxBackoffMs: 5 });
    const response = await fetchWithRetry(new Request("https://example.com"));

    expect(response.status).toBe(200);
    expect(calls).toBe(2);
  });
});
