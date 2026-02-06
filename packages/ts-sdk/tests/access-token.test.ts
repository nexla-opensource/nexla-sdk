import { describe, expect, it } from "vitest";
import { AccessTokenAuthProvider } from "../src/auth/access-token.js";
import { AuthenticationError } from "../src/errors.js";

describe("AccessTokenAuthProvider", () => {
  it("returns the provided access token", async () => {
    const provider = new AccessTokenAuthProvider("token");
    await expect(provider.getAccessToken()).resolves.toBe("token");
  });

  it("throws on refresh attempts", async () => {
    const provider = new AccessTokenAuthProvider("token");
    await expect(provider.refreshAccessToken()).rejects.toBeInstanceOf(AuthenticationError);
  });
});
