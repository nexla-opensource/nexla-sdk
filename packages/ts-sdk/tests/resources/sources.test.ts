/**
 * Unit tests for Sources resource operations.
 */

import { describe, expect, it, beforeEach } from "vitest";
import { createMockFetch } from "../utils/mock-fetch.js";
import { createSource, createSourceList, resetIdCounter } from "../utils/factories/index.js";
import { NexlaClient } from "../../src/client/nexla-client.js";

describe("SourcesResource", () => {
  beforeEach(() => {
    resetIdCounter();
  });

  describe("list operations", () => {
    it("fetches all sources", async () => {
      const sources = createSourceList(3);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: sources },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.sources.list();

      expect(result).toEqual(sources);
      expect(calls.length).toBe(2);
      expect(calls[1]?.url).toContain("/data_sources");
    });

    it("passes query parameters correctly", async () => {
      const sources = createSourceList(2);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: sources },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.sources.list({ params: { query: { page: 2, per_page: 10 } } });

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

      const result = await client.sources.list();

      expect(result).toEqual([]);
    });
  });

  describe("get operations", () => {
    it("fetches source by ID", async () => {
      const source = createSource({ id: 123 });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: source },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.sources.get({ params: { path: { source_id: 123 } } });

      expect(result).toEqual(source);
      expect(calls[1]?.url).toContain("/data_sources/123");
    });

    it("handles source not found (404)", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 404, body: { message: "Source not found" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.sources.get({ params: { path: { source_id: 99999 } } })
      ).rejects.toThrow();
    });
  });

  describe("create operations", () => {
    it("creates a new source", async () => {
      const newSource = createSource({ name: "My New Source" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 201, body: newSource },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.sources.create({
        body: { name: "My New Source", connector_id: 1, data_credentials_id: 1 },
      });

      expect(result).toEqual(newSource);
      expect(calls[1]?.method).toBe("POST");
    });
  });

  describe("update operations", () => {
    it("updates existing source", async () => {
      const updatedSource = createSource({ id: 123, name: "Updated Source" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: updatedSource },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.sources.update({
        params: { path: { source_id: 123 } },
        body: { name: "Updated Source" },
      });

      expect(result).toEqual(updatedSource);
      expect(calls[1]?.method).toBe("PUT");
      expect(calls[1]?.url).toContain("/data_sources/123");
    });
  });

  describe("delete operations", () => {
    it("deletes source by ID", async () => {
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: { status: "deleted" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.sources.delete({ params: { path: { source_id: 123 } } });

      expect(calls[1]?.method).toBe("DELETE");
      expect(calls[1]?.url).toContain("/data_sources/123");
    });
  });

  describe("lifecycle operations", () => {
    it("activates a paused source", async () => {
      const activatedSource = createSource({ id: 123, status: "ACTIVE" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: activatedSource },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.sources.activate_source({
        params: { path: { source_id: 123 } },
      });

      expect(result).toEqual(activatedSource);
      expect(calls[1]?.url).toContain("/data_sources/123/activate");
    });

    it("pauses an active source", async () => {
      const pausedSource = createSource({ id: 123, status: "PAUSED" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: pausedSource },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.sources.pause_source({
        params: { path: { source_id: 123 } },
      });

      expect(result).toEqual(pausedSource);
      expect(calls[1]?.url).toContain("/data_sources/123/pause");
    });

    it("copies a source", async () => {
      const copiedSource = createSource({ id: 456, name: "Copy of Source" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: copiedSource },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.sources.copy_source({
        params: { path: { source_id: 123 } },
      });

      expect(result).toEqual(copiedSource);
      expect(calls[1]?.url).toContain("/data_sources/123/copy");
      expect(calls[1]?.method).toBe("POST");
    });
  });
});
