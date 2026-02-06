import { NexlaError, isRecord } from "../errors.js";

export interface WebhookSendOptions {
  includeHeaders?: boolean;
  includeUrlParams?: boolean;
  forceSchemaDetection?: boolean;
  authMethod?: "query" | "header";
}

export interface WebhooksClientOptions {
  apiKey: string;
  fetch?: typeof fetch;
}

export class WebhooksClient {
  private readonly apiKey: string;
  private readonly fetchFn: typeof fetch;

  constructor(options: WebhooksClientOptions) {
    this.apiKey = options.apiKey;
    this.fetchFn = options.fetch ?? globalThis.fetch;
  }

  async sendOneRecord(
    webhookUrl: string,
    record: Record<string, unknown>,
    options?: WebhookSendOptions
  ): Promise<unknown> {
    return this.makeRequest(webhookUrl, record, options);
  }

  async sendManyRecords(
    webhookUrl: string,
    records: Record<string, unknown>[],
    options?: WebhookSendOptions
  ): Promise<unknown> {
    return this.makeRequest(webhookUrl, records, options);
  }

  private async makeRequest(
    webhookUrl: string,
    body: Record<string, unknown> | Record<string, unknown>[],
    options?: WebhookSendOptions
  ): Promise<unknown> {
    const authMethod = options?.authMethod ?? "query";
    const url = new URL(webhookUrl);

    if (authMethod === "query") {
      url.searchParams.set("api_key", this.apiKey);
    }
    if (options?.includeHeaders) url.searchParams.set("include_headers", "true");
    if (options?.includeUrlParams) url.searchParams.set("include_url_params", "true");
    if (options?.forceSchemaDetection) url.searchParams.set("force_schema_detection", "true");

    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (authMethod === "header") {
      headers["Authorization"] = `Basic ${Buffer.from(this.apiKey).toString("base64")}`;
    }

    const response = await this.fetchFn(url.toString(), {
      method: "POST",
      headers,
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      const errorBody = await safeParseJson(response);
      const message = extractErrorMessage(errorBody) ?? response.statusText ?? "Webhook request failed";
      throw new NexlaError(message, { statusCode: response.status, response: errorBody });
    }

    return safeParseJson(response);
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

const extractErrorMessage = (body: unknown): string | undefined => {
  if (isRecord(body)) {
    const message = body["message"];
    if (typeof message === "string") return message;
    const error = body["error"];
    if (typeof error === "string") return error;
  }
  return undefined;
};
