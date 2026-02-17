import { describe, expect, it } from "vitest";
import { NexlaClient } from "../src/client/nexla-client.js";

const createMockFetch = () => {
  const calls: Request[] = [];
  const fetchFn: typeof fetch = async (input, init) => {
    const request = input instanceof Request ? input : new Request(input, init);
    calls.push(request);
    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { "content-type": "application/json" }
    });
  };
  return { fetchFn, calls };
};

describe("NexlaClient auth bypass header", () => {
  it("skips auth when x-nexla-skip-auth is set", async () => {
    const { fetchFn, calls } = createMockFetch();
    const client = new NexlaClient({
      accessToken: "access-token",
      baseUrl: "https://example.com",
      fetch: fetchFn
    });

    await client.request("get", "/flows", { headers: { "x-nexla-skip-auth": "true" } });

    const request = calls[0];
    if (!request) throw new Error("No request captured");
    expect(request.headers.get("Authorization")).toBeNull();
  });
});
