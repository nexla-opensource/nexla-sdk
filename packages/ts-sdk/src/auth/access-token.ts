import { AuthenticationError } from "../errors.js";
import type { AuthProvider } from "./types.js";

export class AccessTokenAuthProvider implements AuthProvider {
  readonly isRefreshable = false;
  private readonly accessToken: string;

  constructor(accessToken: string) {
    if (!accessToken) {
      throw new AuthenticationError("Access token must be provided");
    }
    this.accessToken = accessToken;
  }

  async getAccessToken(): Promise<string> {
    return this.accessToken;
  }

  async refreshAccessToken(): Promise<void> {
    throw new AuthenticationError("Direct access tokens cannot be refreshed");
  }

  async logout(): Promise<void> {
    // No-op for direct tokens.
  }
}
