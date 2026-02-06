/**
 * Auto-generated helpers for resource clients.
 * Do not edit manually.
 */

import type { HeadersOptions } from "openapi-fetch";

type HeaderCarrier = { headers?: HeadersOptions };

const normalizeHeaders = (headers?: HeadersOptions): Record<string, string> => {
  if (!headers) return {};
  if (headers instanceof Headers) {
    const record: Record<string, string> = {};
    headers.forEach((value, key) => {
      record[key] = value;
    });
    return record;
  }
  if (Array.isArray(headers)) {
    return Object.fromEntries(headers);
  }
  const record: Record<string, string> = {};
  for (const [key, value] of Object.entries(headers)) {
    if (value === null || value === undefined) continue;
    if (Array.isArray(value)) {
      record[key] = value.map((item) => String(item)).join(", ");
    } else {
      record[key] = String(value);
    }
  }
  return record;
};

export const withSkipAuth = <T extends HeaderCarrier | undefined>(init?: T): T => {
  if (!init) {
    return { headers: { "x-nexla-skip-auth": "true" } } as unknown as T;
  }
  const headers = { ...normalizeHeaders(init.headers), "x-nexla-skip-auth": "true" };
  return { ...(init as HeaderCarrier), headers } as unknown as T;
};
