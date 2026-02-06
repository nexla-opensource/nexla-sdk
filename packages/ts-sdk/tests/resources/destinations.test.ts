/**
 * Unit tests for Destinations resource operations.
 */

import { describe, expect, it, beforeEach } from "vitest";
import { createMockFetch } from "../utils/mock-fetch.js";
import { createDestination, createDestinationList, resetIdCounter } from "../utils/factories/index.js";
import { NexlaClient } from "../../src/client/nexla-client.js";

describe("DestinationsResource", () => {
  beforeEach(() => {
    resetIdCounter();
  });

  describe("list operations", () => {
    it("fetches all destinations", async () => {
      const destinations = createDestinationList(3);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: destinations },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.destinations.list();

      expect(result).toEqual(destinations);
      expect(calls.length).toBe(2);
      expect(calls[1]?.url).toContain("/data_sinks");
    });

    it("passes query parameters correctly", async () => {
      const destinations = createDestinationList(2);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: destinations },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.destinations.list({ params: { query: { page: 2, per_page: 10 } } });

      const requestUrl = calls[1]?.url ?? "";
      expect(requestUrl).toContain("page=2");
      expect(requestUrl).toContain("per_page=10");
    });

    it("handles empty results", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.destinations.list();

      expect(result).toEqual([]);
    });
  });

  describe("get operations", () => {
    it("fetches destination by ID", async () => {
      const destination = createDestination({ id: 123 });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: destination },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.destinations.get({ params: { path: { sink_id: 123 } } });

      expect(result).toEqual(destination);
      expect(calls[1]?.url).toContain("/data_sinks/123");
    });

    it("handles destination not found (404)", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 404, body: { message: "Destination not found" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.destinations.get({ params: { path: { sink_id: 99999 } } })
      ).rejects.toThrow();
    });
  });

  describe("create operations", () => {
    it("creates a new destination", async () => {
      const newDestination = createDestination({ name: "My New Destination" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 201, body: newDestination },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.destinations.create({
        body: { name: "My New Destination", connector_id: 1, data_credentials_id: 1 },
      });

      expect(result).toEqual(newDestination);
      expect(calls[1]?.method).toBe("POST");
    });
  });

  describe("update operations", () => {
    it("updates existing destination", async () => {
      const updatedDestination = createDestination({ id: 123, name: "Updated Destination" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: updatedDestination },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.destinations.update({
        params: { path: { sink_id: 123 } },
        body: { name: "Updated Destination" },
      });

      expect(result).toEqual(updatedDestination);
      expect(calls[1]?.method).toBe("PUT");
      expect(calls[1]?.url).toContain("/data_sinks/123");
    });
  });

  describe("delete operations", () => {
    it("deletes destination by ID", async () => {
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: { status: "deleted" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.destinations.delete({ params: { path: { sink_id: 123 } } });

      expect(calls[1]?.method).toBe("DELETE");
      expect(calls[1]?.url).toContain("/data_sinks/123");
    });
  });

  describe("lifecycle operations", () => {
    it("activates a paused destination", async () => {
      const activatedDestination = createDestination({ id: 123, status: "ACTIVE" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: activatedDestination },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.destinations.activate_data_sink({
        params: { path: { sink_id: 123 } },
      });

      expect(result).toEqual(activatedDestination);
      expect(calls[1]?.url).toContain("/data_sinks/123/activate");
    });

    it("pauses an active destination", async () => {
      const pausedDestination = createDestination({ id: 123, status: "PAUSED" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: pausedDestination },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.destinations.pause_data_sink({
        params: { path: { sink_id: 123 } },
      });

      expect(result).toEqual(pausedDestination);
      expect(calls[1]?.url).toContain("/data_sinks/123/pause");
    });

    it("copies a destination", async () => {
      const copiedDestination = createDestination({ id: 456, name: "Copy of Destination" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: copiedDestination },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.destinations.copy_data_sink_source({
        params: { path: { sink_id: 123 } },
      });

      expect(result).toEqual(copiedDestination);
      expect(calls[1]?.url).toContain("/data_sinks/123/copy");
      expect(calls[1]?.method).toBe("POST");
    });
  });
});
