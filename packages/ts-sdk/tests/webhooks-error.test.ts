import { describe, expect, it } from "vitest";
import { WebhooksClient } from "../src/webhooks/index.js";
import { NexlaError } from "../src/errors.js";

const createMockFetch = (status: number, body?: unknown) => {
  const fetchFn: typeof fetch = async () => {
    return new Response(JSON.stringify(body ?? {}), {
      status,
      headers: { "content-type": "application/json" }
    });
  };
  return fetchFn;
};

describe("WebhooksClient errors", () => {
  it("throws NexlaError on non-200", async () => {
    const fetchFn = createMockFetch(500, { error: "boom" });
    const client = new WebhooksClient({ apiKey: "abc", fetch: fetchFn });

    await expect(
      client.sendOneRecord("https://example.com/webhook", { id: 1 })
    ).rejects.toBeInstanceOf(NexlaError);
  });
});
