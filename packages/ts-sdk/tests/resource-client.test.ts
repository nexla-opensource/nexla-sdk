import { describe, expect, it } from "vitest";
import { NexlaClient } from "../src/client/nexla-client.js";

const createMockFetch = () => {
  const calls: Request[] = [];
  const fetchFn: typeof fetch = async (input, init) => {
    const request = input instanceof Request ? input : new Request(input, init);
    calls.push(request);

    const body = JSON.stringify([{ id: 1 }]);
    return new Response(body, {
      status: 200,
      headers: { "content-type": "application/json" }
    });
  };
  return { fetchFn, calls };
};

describe("ResourceClient", () => {
  it("calls list on flows resource", async () => {
    const { fetchFn, calls } = createMockFetch();

    const client = new NexlaClient({
      accessToken: "access-token",
      baseUrl: "https://example.com",
      fetch: fetchFn
    });

    await client.flows.list({ params: { query: { page: 1 } } });

    const request = calls[0];
    if (!request) throw new Error("No request captured");
    expect(request.url).toContain("/flows");
  });

  it("calls operationId method on flows resource", async () => {
    const { fetchFn, calls } = createMockFetch();

    const client = new NexlaClient({
      accessToken: "access-token",
      baseUrl: "https://example.com",
      fetch: fetchFn
    });

    await client.flows.flow_activate_with_flow_id({
      params: { path: { flow_id: 123, all: 1 } }
    });

    const request = calls[0];
    if (!request) throw new Error("No request captured");
    expect(request.url).toContain("/flows/123/activate");
    expect(request.method).toBe("PUT");
  });
});
