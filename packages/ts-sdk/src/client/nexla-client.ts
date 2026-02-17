import createClient, { type Client } from "openapi-fetch";
import type { HttpMethod, PathsWithMethod } from "openapi-typescript-helpers";
import type { paths } from "../generated/schema.js";
import { AuthenticationError, AuthorizationError, NexlaError, NotFoundError, RateLimitError, ResourceConflictError, ServerError, ValidationError, isRecord } from "../errors.js";
import { AccessTokenAuthProvider } from "../auth/access-token.js";
import { ServiceKeyAuthProvider } from "../auth/service-key.js";
import type { AuthProvider } from "../auth/types.js";
import { createFetchWithRetry, type RetryOptions } from "./http.js";
import type { RequestOptions } from "./types.js";
import type { OperationData, OperationId, OperationInit } from "./operation-types.js";
import { createGeneratedResources, type GeneratedResourceClients } from "../resources/generated/index.js";
import { WebhooksClient } from "../webhooks/index.js";

export interface NexlaClientOptions {
  serviceKey?: string;
  accessToken?: string;
  baseUrl?: string;
  apiVersion?: string;
  tokenRefreshMargin?: number;
  retry?: RetryOptions;
  fetch?: typeof fetch;
  userAgent?: string;
  webhookApiKey?: string;
}

export class NexlaClient {
  readonly raw: Client<paths>;
  readonly baseUrl: string;
  readonly apiVersion: string;
  readonly acceptHeader: string;
  readonly authProvider: AuthProvider;
  readonly webhooks?: WebhooksClient;


  constructor(options: NexlaClientOptions = {}) {
    const serviceKey = options.serviceKey ?? process.env.NEXLA_SERVICE_KEY;
    const accessToken = options.accessToken ?? process.env.NEXLA_ACCESS_TOKEN;

    if (!serviceKey && !accessToken) {
      throw new NexlaError(
        "Either serviceKey or accessToken must be provided (or set NEXLA_SERVICE_KEY/NEXLA_ACCESS_TOKEN)."
      );
    }
    if (serviceKey && accessToken) {
      throw new NexlaError("Cannot provide both serviceKey and accessToken.");
    }

    this.baseUrl = (options.baseUrl ?? process.env.NEXLA_API_URL ?? "https://dataops.nexla.io/nexla-api").replace(/\/$/, "");
    this.apiVersion = options.apiVersion ?? "v1";
    this.acceptHeader = `application/vnd.nexla.api.${this.apiVersion}+json`;

    const fetchImpl = options.fetch ?? globalThis.fetch;
    const fetchWithRetry = createFetchWithRetry(fetchImpl, options.retry);

    if (serviceKey) {
      const authOptions = {
        serviceKey,
        baseUrl: this.baseUrl,
        apiVersion: this.apiVersion,
        tokenRefreshMargin: options.tokenRefreshMargin ?? 3600,
        fetchFn: fetchImpl
      } as const;
      const provider = new ServiceKeyAuthProvider(
        options.userAgent ? { ...authOptions, userAgent: options.userAgent } : authOptions
      );
      this.authProvider = provider;
    } else {
      this.authProvider = new AccessTokenAuthProvider(accessToken ?? "");
    }

    this.raw = createClient<paths>({ baseUrl: this.baseUrl, fetch: fetchWithRetry });

    this.raw.use({
      onRequest: async ({ request }) => {
        const headers = new Headers(request.headers);
        const skipAuth = headers.get("x-nexla-skip-auth") === "true";
        headers.delete("x-nexla-skip-auth");

        if (!headers.has("Accept")) headers.set("Accept", this.acceptHeader);
        if (!headers.has("Content-Type") && request.method !== "GET" && request.method !== "HEAD") {
          headers.set("Content-Type", "application/json");
        }
        if (options.userAgent) {
          headers.set("User-Agent", options.userAgent);
        }
        if (!skipAuth) {
          const token = await this.authProvider.getAccessToken();
          headers.set("Authorization", `Bearer ${token}`);
        }

        return new Request(request, { headers });
      }
    });

    if (options.webhookApiKey) {
      this.webhooks = new WebhooksClient({ apiKey: options.webhookApiKey, fetch: fetchImpl });
    }

    Object.assign(this, createGeneratedResources(this));
  }

  async request<Method extends HttpMethod, Path extends PathsWithMethod<paths, Method>>(
    method: Method,
    path: Path,
    init?: RequestOptions
  ): Promise<unknown> {
    const execute = async (): Promise<unknown> => {
      const result = await this.invoke(method, path, init);
      const response = result as { data?: unknown; error?: unknown; response?: Response };
      if (response.error) {
        throw this.mapError(response.error, response.response ?? new Response(null, { status: 500 }), method, path as string);
      }
      return response.data as unknown;
    };

    try {
      return await execute();
    } catch (error) {
      if (error instanceof AuthenticationError && this.authProvider.isRefreshable) {
        await this.authProvider.refreshAccessToken();
        return await execute();
      }
      throw error;
    }
  }

  async requestOperation<OpId extends OperationId>(
    _operationId: OpId,
    method: HttpMethod,
    path: string,
    init?: OperationInit<OpId>
  ): Promise<OperationData<OpId>> {
    const data = await this.request(method, path as PathsWithMethod<paths, HttpMethod>, init as RequestOptions);
    return data as OperationData<OpId>;
  }

  async logout(): Promise<void> {
    await this.authProvider.logout();
  }

  private invoke<Method extends HttpMethod, Path extends PathsWithMethod<paths, Method>>(
    method: Method,
    path: Path,
    init?: RequestOptions
  ) {
    switch (method) {
      case "get":
        return this.raw.GET(path as never, init as never);
      case "post":
        return this.raw.POST(path as never, init as never);
      case "put":
        return this.raw.PUT(path as never, init as never);
      case "patch":
        return this.raw.PATCH(path as never, init as never);
      case "delete":
        return this.raw.DELETE(path as never, init as never);
      case "options":
        return this.raw.OPTIONS(path as never, init as never);
      case "head":
        return this.raw.HEAD(path as never, init as never);
      case "trace":
        return this.raw.TRACE(path as never, init as never);
      default:
        throw new NexlaError(`Unsupported HTTP method: ${method}`);
    }
  }

  private mapError(errorBody: unknown, response: Response, method?: string, path?: string): NexlaError {
    const message = extractErrorMessage(errorBody, response) ?? `Request failed with status ${response.status}`;
    const context: Record<string, unknown> = {
      method: method?.toUpperCase(),
      path,
      url: response.url,
      status_code: response.status,
    };
    const options = { statusCode: response.status, response: errorBody, context };

    if (response.status === 401) {
      return new AuthenticationError(message, options);
    }
    if (response.status === 403) {
      return new AuthorizationError(message, options);
    }
    if (response.status === 404) {
      return new NotFoundError(message, options);
    }
    if (response.status === 409) {
      return new ResourceConflictError(message, options);
    }
    if (response.status === 422 || response.status === 400) {
      return new ValidationError(message, options);
    }
    if (response.status === 429) {
      const retryAfter = parseRetryAfter(response.headers.get("retry-after"));
      return new RateLimitError(message, retryAfter === undefined ? options : { ...options, retryAfter });
    }
    if (response.status >= 500) {
      return new ServerError(message, options);
    }

    return new NexlaError(message, options);
  }
}

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

const parseRetryAfter = (value: string | null): number | undefined => {
  if (!value) return undefined;
  const parsed = Number(value);
  return Number.isNaN(parsed) ? undefined : parsed;
};

export interface NexlaClient extends GeneratedResourceClients {}
