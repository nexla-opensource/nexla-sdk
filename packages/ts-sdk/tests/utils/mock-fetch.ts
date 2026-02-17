/**
 * Mock fetch utilities for testing.
 * Replaces duplicated createMockFetch patterns across test files.
 */

export interface MockResponse {
  status: number;
  body?: unknown;
  headers?: Record<string, string>;
}

export interface MockFetchResult {
  fetchFn: typeof fetch;
  calls: Request[];
  getCall(index: number): Request | undefined;
  getLastCall(): Request | undefined;
  clearCalls(): void;
  getRequestBody(index: number): Promise<unknown>;
}

/**
 * Create a mock fetch function that returns responses in order.
 * Each call consumes the next response from the queue.
 */
export function createMockFetch(responses: MockResponse[]): MockFetchResult {
  const calls: Request[] = [];
  const responseQueue = [...responses];

  const fetchFn: typeof fetch = async (input, init) => {
    const request = input instanceof Request ? input : new Request(input, init);
    calls.push(request);

    const next = responseQueue.shift() ?? { status: 200, body: {} };
    const body = JSON.stringify(next.body ?? {});
    const headers: Record<string, string> = {
      "content-type": "application/json",
      ...(next.headers ?? {}),
    };

    return new Response(body, {
      status: next.status,
      headers,
    });
  };

  return {
    fetchFn,
    calls,
    getCall(index: number): Request | undefined {
      return calls[index];
    },
    getLastCall(): Request | undefined {
      return calls[calls.length - 1];
    },
    clearCalls(): void {
      calls.length = 0;
    },
    async getRequestBody(index: number): Promise<unknown> {
      const request = calls[index];
      if (!request) return undefined;
      try {
        const cloned = request.clone();
        return await cloned.json();
      } catch {
        return undefined;
      }
    },
  };
}

/**
 * Create a mock fetch that uses a handler function for dynamic responses.
 */
export function createDynamicMockFetch(
  handler: (request: Request) => MockResponse | Promise<MockResponse>
): MockFetchResult {
  const calls: Request[] = [];

  const fetchFn: typeof fetch = async (input, init) => {
    const request = input instanceof Request ? input : new Request(input, init);
    calls.push(request);

    const response = await handler(request);
    const body = JSON.stringify(response.body ?? {});
    const headers: Record<string, string> = {
      "content-type": "application/json",
      ...(response.headers ?? {}),
    };

    return new Response(body, {
      status: response.status,
      headers,
    });
  };

  return {
    fetchFn,
    calls,
    getCall(index: number): Request | undefined {
      return calls[index];
    },
    getLastCall(): Request | undefined {
      return calls[calls.length - 1];
    },
    clearCalls(): void {
      calls.length = 0;
    },
    async getRequestBody(index: number): Promise<unknown> {
      const request = calls[index];
      if (!request) return undefined;
      try {
        const cloned = request.clone();
        return await cloned.json();
      } catch {
        return undefined;
      }
    },
  };
}

/**
 * Create pagination response headers.
 */
export function paginationHeaders(options: {
  pageCount?: number;
  totalPageCount?: number;
  currentPage?: number;
}): Record<string, string> {
  const headers: Record<string, string> = {};
  if (options.pageCount !== undefined) {
    headers["X-Page-Count"] = String(options.pageCount);
  }
  if (options.totalPageCount !== undefined) {
    headers["X-Total-Page-Count"] = String(options.totalPageCount);
  }
  if (options.currentPage !== undefined) {
    headers["X-Current-Page"] = String(options.currentPage);
  }
  return headers;
}
