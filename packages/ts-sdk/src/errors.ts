export type ErrorDetails = Record<string, unknown>;

export class NexlaError extends Error {
  readonly details: ErrorDetails;
  readonly operation: string | undefined;
  readonly resourceType: string | undefined;
  readonly resourceId: string | undefined;
  readonly step: string | undefined;
  readonly context: ErrorDetails;
  readonly originalError: Error | undefined;
  readonly statusCode: number | undefined;
  readonly response: unknown | undefined;

  constructor(
    message: string,
    options: {
      details?: ErrorDetails;
      operation?: string;
      resourceType?: string;
      resourceId?: string;
      step?: string;
      context?: ErrorDetails;
      originalError?: Error;
      statusCode?: number;
      response?: unknown;
    } = {}
  ) {
    super(message);
    this.name = "NexlaError";
    this.details = options.details ?? {};
    this.operation = options.operation;
    this.resourceType = options.resourceType;
    this.resourceId = options.resourceId;
    this.step = options.step;
    this.context = options.context ?? {};
    this.originalError = options.originalError;
    this.statusCode = options.statusCode;
    this.response = options.response;
  }

  getErrorSummary(): Record<string, unknown> {
    return {
      message: this.message,
      step: this.step,
      operation: this.operation,
      resource_type: this.resourceType,
      resource_id: this.resourceId,
      details: this.details,
      context: this.context,
      status_code: this.statusCode,
      response: this.response,
      original_error: this.originalError?.message
    };
  }
}

export class AuthenticationError extends NexlaError {
  constructor(message = "Authentication failed", options: ConstructorParameters<typeof NexlaError>[1] = {}) {
    super(message, { operation: "authentication", ...options });
    this.name = "AuthenticationError";
  }
}

export class AuthorizationError extends NexlaError {
  constructor(message = "Authorization failed", options: ConstructorParameters<typeof NexlaError>[1] = {}) {
    super(message, options);
    this.name = "AuthorizationError";
  }
}

export class NotFoundError extends NexlaError {
  constructor(message = "Resource not found", options: ConstructorParameters<typeof NexlaError>[1] = {}) {
    super(message, options);
    this.name = "NotFoundError";
  }
}

export class ValidationError extends NexlaError {
  constructor(message = "Validation failed", options: ConstructorParameters<typeof NexlaError>[1] = {}) {
    super(message, options);
    this.name = "ValidationError";
  }
}

export class RateLimitError extends NexlaError {
  readonly retryAfter: number | undefined;

  constructor(
    message = "Rate limit exceeded",
    options: ConstructorParameters<typeof NexlaError>[1] & { retryAfter?: number } = {}
  ) {
    super(message, options);
    this.name = "RateLimitError";
    this.retryAfter = options.retryAfter;
  }
}

export class ServerError extends NexlaError {
  constructor(message = "Server error", options: ConstructorParameters<typeof NexlaError>[1] = {}) {
    super(message, options);
    this.name = "ServerError";
  }
}

export class ResourceConflictError extends NexlaError {
  constructor(message = "Resource conflict", options: ConstructorParameters<typeof NexlaError>[1] = {}) {
    super(message, options);
    this.name = "ResourceConflictError";
  }
}

export const isRecord = (value: unknown): value is Record<string, unknown> => {
  return typeof value === "object" && value !== null;
};
