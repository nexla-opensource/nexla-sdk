import { describe, expect, it } from "vitest";
import { NexlaClient } from "../src/client/nexla-client.js";
import { NotFoundError } from "../src/errors.js";

const createMockFetch = (status: number, body: unknown) => {
  const fetchFn: typeof fetch = async () => {
    return new Response(JSON.stringify(body), {
      status,
      headers: { "content-type": "application/json" }
    });
  };
  return fetchFn;
};

describe("NexlaClient error mapping", () => {
  it("maps 404 to NotFoundError", async () => {
    const fetchFn = createMockFetch(404, { message: "not found" });
    const client = new NexlaClient({
      accessToken: "access-token",
      baseUrl: "https://example.com",
      fetch: fetchFn
    });

    await expect(client.request("get", "/flows")).rejects.toBeInstanceOf(NotFoundError);
  });
});
