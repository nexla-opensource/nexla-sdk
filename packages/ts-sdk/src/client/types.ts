import type { paths } from "../generated/schema.js";

export type HttpMethod = "get" | "post" | "put" | "patch" | "delete" | "options" | "head" | "trace";

export interface RequestOptions {
  params?: {
    query?: Record<string, unknown>;
    path?: Record<string, unknown>;
  };
  headers?: Record<string, string>;
  body?: unknown;
}

export type NexlaPaths = paths;
