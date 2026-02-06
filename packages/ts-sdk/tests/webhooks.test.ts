import { describe, expect, it } from "vitest";
import { WebhooksClient } from "../src/webhooks/index.js";

const createMockFetch = (status: number, body?: unknown) => {
  const calls: Request[] = [];
  const fetchFn: typeof fetch = async (input, init) => {
    const request = input instanceof Request ? input : new Request(input, init);
    calls.push(request);

    return new Response(JSON.stringify(body ?? {}), {
      status,
      headers: { "content-type": "application/json" }
    });
  };
  return { fetchFn, calls };
};

describe("WebhooksClient", () => {
  it("sends record with api_key query param", async () => {
    const { fetchFn, calls } = createMockFetch(200, { ok: true });
    const client = new WebhooksClient({ apiKey: "abc", fetch: fetchFn });

    await client.sendOneRecord("https://example.com/webhook", { id: 1 });

    const request = calls[0];
    if (!request) throw new Error("No request captured");
    const url = new URL(request.url);
    expect(url.searchParams.get("api_key")).toBe("abc");
  });

  it("sends record with basic auth header when authMethod=header", async () => {
    const { fetchFn, calls } = createMockFetch(200, { ok: true });
    const client = new WebhooksClient({ apiKey: "abc", fetch: fetchFn });

    await client.sendOneRecord("https://example.com/webhook", { id: 1 }, { authMethod: "header" });

    const request = calls[0];
    if (!request) throw new Error("No request captured");
    expect(request.headers.get("Authorization")).toBe(`Basic ${Buffer.from("abc").toString("base64")}`);
  });
});
