/**
 * Test client setup utilities.
 */

import { NexlaClient } from "../../src/client/nexla-client.js";
import { createMockFetch, type MockFetchResult, type MockResponse } from "./mock-fetch.js";

export interface TestClientOptions {
  mockResponses?: MockResponse[];
  accessToken?: string;
  baseUrl?: string;
}

export interface TestClientResult {
  client: NexlaClient;
  mockFetch: MockFetchResult;
}

/**
 * Create a test client with mocked fetch.
 * Automatically includes a token response for service key auth.
 */
export function createTestClient(options: TestClientOptions = {}): TestClientResult {
  const {
    mockResponses = [],
    accessToken,
    baseUrl = "https://test.nexla.io/nexla-api",
  } = options;

  // If using service key auth, prepend token response
  const allResponses: MockResponse[] = accessToken
    ? [...mockResponses]
    : [
        { status: 200, body: { access_token: "test-token", expires_in: 7200 } },
        ...mockResponses,
      ];

  const mockFetch = createMockFetch(allResponses);

  const client = accessToken
    ? new NexlaClient({
        accessToken,
        baseUrl,
        fetch: mockFetch.fetchFn,
      })
    : new NexlaClient({
        serviceKey: "test-service-key",
        baseUrl,
        fetch: mockFetch.fetchFn,
      });

  return { client, mockFetch };
}

/**
 * Create a test client for direct token auth (no token refresh).
 */
export function createDirectTokenClient(
  mockResponses: MockResponse[] = []
): TestClientResult {
  return createTestClient({
    mockResponses,
    accessToken: "direct-test-token",
  });
}
