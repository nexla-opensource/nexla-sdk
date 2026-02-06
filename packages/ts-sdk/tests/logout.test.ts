import { describe, expect, it } from "vitest";
import { ServiceKeyAuthProvider } from "../src/auth/service-key.js";

const createMockFetch = () => {
  const calls: Request[] = [];
  const fetchFn: typeof fetch = async (input, init) => {
    const request = input instanceof Request ? input : new Request(input, init);
    calls.push(request);

    if (request.url.endsWith("/token")) {
      return new Response(JSON.stringify({ access_token: "token-1", expires_in: 1 }), {
        status: 200,
        headers: { "content-type": "application/json" }
      });
    }

    return new Response("", { status: 204 });
  };
  return { fetchFn, calls };
};

describe("ServiceKeyAuthProvider logout", () => {
  it("calls /token/logout and clears token", async () => {
    const { fetchFn, calls } = createMockFetch();

    const provider = new ServiceKeyAuthProvider({
      serviceKey: "svc-key",
      baseUrl: "https://example.com",
      apiVersion: "v1",
      tokenRefreshMargin: 1,
      fetchFn
    });

    await provider.getAccessToken();
    await provider.logout();

    const logoutCall = calls.find((req) => req.url.endsWith("/token/logout"));
    expect(logoutCall).toBeTruthy();
  });
});
