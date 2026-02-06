import { describe, expect, it } from "vitest";
import { ServiceKeyAuthProvider } from "../src/auth/service-key.js";
import { AuthenticationError } from "../src/errors.js";

const createMockFetch = (responses: Array<{ status: number; body?: unknown }>) => {
  const calls: Request[] = [];
  const fetchFn: typeof fetch = async (input, init) => {
    const request = input instanceof Request ? input : new Request(input, init);
    calls.push(request);

    const next = responses.shift() ?? { status: 200, body: {} };
    const body = JSON.stringify(next.body ?? {});
    return new Response(body, {
      status: next.status,
      headers: { "content-type": "application/json" }
    });
  };
  return { fetchFn, calls };
};

describe("ServiceKeyAuthProvider", () => {
  it("obtains and caches access tokens", async () => {
    const { fetchFn, calls } = createMockFetch([
      { status: 200, body: { access_token: "token-1", expires_in: 7200 } }
    ]);

    const provider = new ServiceKeyAuthProvider({
      serviceKey: "svc-key",
      baseUrl: "https://example.com",
      apiVersion: "v1",
      tokenRefreshMargin: 60,
      fetchFn
    });

    const token1 = await provider.getAccessToken();
    const token2 = await provider.getAccessToken();

    expect(token1).toBe("token-1");
    expect(token2).toBe("token-1");
    expect(calls.length).toBe(1);
  });

  it("refreshes token when near expiry", async () => {
    const { fetchFn, calls } = createMockFetch([
      { status: 200, body: { access_token: "token-1", expires_in: 1 } },
      { status: 200, body: { access_token: "token-2", expires_in: 7200 } }
    ]);

    const provider = new ServiceKeyAuthProvider({
      serviceKey: "svc-key",
      baseUrl: "https://example.com",
      apiVersion: "v1",
      tokenRefreshMargin: 3600,
      fetchFn
    });

    const token1 = await provider.getAccessToken();
    const token2 = await provider.getAccessToken();

    expect(token1).toBe("token-1");
    expect(token2).toBe("token-2");
    expect(calls.length).toBe(2);
  });

  it("throws AuthenticationError on 401", async () => {
    const { fetchFn } = createMockFetch([
      { status: 401, body: { message: "Invalid service key" } }
    ]);

    const provider = new ServiceKeyAuthProvider({
      serviceKey: "svc-key",
      baseUrl: "https://example.com",
      apiVersion: "v1",
      tokenRefreshMargin: 60,
      fetchFn
    });

    await expect(provider.getAccessToken()).rejects.toBeInstanceOf(AuthenticationError);
  });
});
