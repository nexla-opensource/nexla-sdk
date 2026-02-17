import { describe, expect, it } from "vitest";
import { NexlaClient } from "../src/client/nexla-client.js";

const createMockFetch = () => {
  const calls: Request[] = [];
  const fetchFn: typeof fetch = async (input, init) => {
    const request = input instanceof Request ? input : new Request(input, init);
    calls.push(request);

    const body = JSON.stringify([{ id: 1, name: "flow-1" }]);
    return new Response(body, {
      status: 200,
      headers: { "content-type": "application/json" }
    });
  };
  return { fetchFn, calls };
};

describe("NexlaClient", () => {
  it("injects authorization and accept headers", async () => {
    const { fetchFn, calls } = createMockFetch();

    const client = new NexlaClient({
      accessToken: "access-token",
      baseUrl: "https://example.com",
      fetch: fetchFn,
      userAgent: "nexla-sdk-test"
    });

    await client.request("get", "/flows");

    expect(calls.length).toBe(1);
    const request = calls[0];
    if (!request) throw new Error("No request captured");
    expect(request.headers.get("Authorization")).toBe("Bearer access-token");
    expect(request.headers.get("Accept")).toBe("application/vnd.nexla.api.v1+json");
    expect(request.headers.get("User-Agent")).toBe("nexla-sdk-test");
  });
});
