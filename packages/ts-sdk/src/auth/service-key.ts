import { AuthenticationError, NexlaError, isRecord } from "../errors.js";
import type { AuthProvider } from "./types.js";

export interface ServiceKeyAuthOptions {
  serviceKey: string;
  baseUrl: string;
  apiVersion: string;
  tokenRefreshMargin: number;
  fetchFn: typeof fetch;
  userAgent?: string;
}

export class ServiceKeyAuthProvider implements AuthProvider {
  readonly isRefreshable = true;

  private readonly serviceKey: string;
  private readonly baseUrl: string;
  private readonly apiVersion: string;
  private readonly tokenRefreshMargin: number;
  private readonly fetchFn: typeof fetch;
  private readonly userAgent: string | undefined;

  private accessToken: string | undefined;
  private tokenExpiry = 0;

  constructor(options: ServiceKeyAuthOptions) {
    this.serviceKey = options.serviceKey;
    this.baseUrl = options.baseUrl.replace(/\/$/, "");
    this.apiVersion = options.apiVersion;
    this.tokenRefreshMargin = options.tokenRefreshMargin;
    this.fetchFn = options.fetchFn;
    this.userAgent = options.userAgent;
  }

  async getAccessToken(): Promise<string> {
    if (!this.accessToken) {
      await this.obtainSessionToken();
    } else if (this.isTokenNearExpiry()) {
      await this.obtainSessionToken();
    }

    if (!this.accessToken) {
      throw new AuthenticationError("No access token available after authentication");
    }

    return this.accessToken;
  }

  async refreshAccessToken(): Promise<void> {
    await this.obtainSessionToken();
  }

  async logout(): Promise<void> {
    if (!this.accessToken) return;

    const headers: Record<string, string> = {
      Accept: `application/vnd.nexla.api.${this.apiVersion}+json`,
      Authorization: `Bearer ${this.accessToken}`
    };
    if (this.userAgent) headers["User-Agent"] = this.userAgent;

    try {
      await this.fetchFn(`${this.baseUrl}/token/logout`, {
        method: "POST",
        headers
      });
    } catch {
      // Best-effort logout; ignore errors.
    } finally {
      this.accessToken = undefined;
      this.tokenExpiry = 0;
    }
  }

  private isTokenNearExpiry(): boolean {
    if (!this.tokenExpiry) return true;
    const now = Date.now() / 1000;
    return this.tokenExpiry - now < this.tokenRefreshMargin;
  }

  private async obtainSessionToken(): Promise<void> {
    const headers: Record<string, string> = {
      Authorization: `Basic ${this.serviceKey}`,
      Accept: `application/vnd.nexla.api.${this.apiVersion}+json`,
      "Content-Length": "0"
    };
    if (this.userAgent) headers["User-Agent"] = this.userAgent;

    const response = await this.fetchFn(`${this.baseUrl}/token`, {
      method: "POST",
      headers
    });

    if (!response.ok) {
      const errorBody = await safeParseJson(response);
      const message = extractErrorMessage(errorBody, response) ?? "Authentication failed";

      if (response.status === 401) {
        throw new AuthenticationError(message, { statusCode: response.status, response: errorBody });
      }

      throw new NexlaError(message, { statusCode: response.status, response: errorBody });
    }

    const data = await safeParseJson(response);
    if (!isRecord(data)) {
      throw new NexlaError("Invalid token response format", { response: data });
    }

    const accessToken = data["access_token"];
    const expiresIn = data["expires_in"];

    if (typeof accessToken !== "string") {
      throw new NexlaError("Missing access token in response", { response: data });
    }

    const expiresInSeconds = typeof expiresIn === "number" ? expiresIn : 86400;
    this.accessToken = accessToken;
    this.tokenExpiry = Date.now() / 1000 + expiresInSeconds;
  }
}

const safeParseJson = async (response: Response): Promise<unknown> => {
  const contentType = response.headers.get("content-type")?.toLowerCase() ?? "";
  if (!contentType.includes("application/json")) {
    return undefined;
  }
  try {
    return await response.json();
  } catch {
    return undefined;
  }
};

const extractErrorMessage = (body: unknown, response: Response): string | undefined => {
  if (isRecord(body)) {
    const message = body["message"];
    if (typeof message === "string") return message;
    const error = body["error"];
    if (typeof error === "string") return error;
  }
  if (response.statusText) return response.statusText;
  return undefined;
};
