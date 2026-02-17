/**
 * Unit tests for Nexsets resource operations.
 */

import { describe, expect, it, beforeEach } from "vitest";
import { createMockFetch } from "../utils/mock-fetch.js";
import { createNexset, createNexsetList, resetIdCounter } from "../utils/factories/index.js";
import { NexlaClient } from "../../src/client/nexla-client.js";

describe("NexsetsResource", () => {
  beforeEach(() => {
    resetIdCounter();
  });

  describe("list operations", () => {
    it("fetches all nexsets", async () => {
      const nexsets = createNexsetList(3);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: nexsets },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.nexsets.list();

      expect(result).toEqual(nexsets);
      expect(calls.length).toBe(2);
      expect(calls[1]?.url).toContain("/data_sets");
    });

    it("passes query parameters correctly", async () => {
      const nexsets = createNexsetList(2);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: nexsets },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.nexsets.list({ params: { query: { page: 2, per_page: 10 } } });

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

      const result = await client.nexsets.list();

      expect(result).toEqual([]);
    });
  });

  describe("get operations", () => {
    it("fetches nexset by ID", async () => {
      const nexset = createNexset({ id: 123 });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: nexset },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.nexsets.get({ params: { path: { set_id: 123 } } });

      expect(result).toEqual(nexset);
      expect(calls[1]?.url).toContain("/data_sets/123");
    });

    it("handles nexset not found (404)", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 404, body: { message: "Nexset not found" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.nexsets.get({ params: { path: { set_id: 99999 } } })
      ).rejects.toThrow();
    });
  });

  describe("create operations", () => {
    it("creates a new nexset", async () => {
      const newNexset = createNexset({ name: "My New Nexset" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 201, body: newNexset },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.nexsets.create({
        body: { name: "My New Nexset", data_source_id: 1 },
      });

      expect(result).toEqual(newNexset);
      expect(calls[1]?.method).toBe("POST");
    });
  });

  describe("update operations", () => {
    it("updates existing nexset", async () => {
      const updatedNexset = createNexset({ id: 123, name: "Updated Nexset" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: updatedNexset },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.nexsets.update({
        params: { path: { set_id: 123 } },
        body: { name: "Updated Nexset" },
      });

      expect(result).toEqual(updatedNexset);
      expect(calls[1]?.method).toBe("PUT");
      expect(calls[1]?.url).toContain("/data_sets/123");
    });
  });

  describe("delete operations", () => {
    it("deletes nexset by ID", async () => {
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: { status: "deleted" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.nexsets.delete({ params: { path: { set_id: 123 } } });

      expect(calls[1]?.method).toBe("DELETE");
      expect(calls[1]?.url).toContain("/data_sets/123");
    });
  });

  describe("lifecycle operations", () => {
    it("activates a paused nexset", async () => {
      const activatedNexset = createNexset({ id: 123, status: "ACTIVE" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: activatedNexset },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.nexsets.activate_nexset({
        params: { path: { set_id: 123 } },
      });

      expect(result).toEqual(activatedNexset);
      expect(calls[1]?.url).toContain("/data_sets/123/activate");
    });

    it("pauses an active nexset", async () => {
      const pausedNexset = createNexset({ id: 123, status: "PAUSED" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: pausedNexset },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.nexsets.pause_nexset({
        params: { path: { set_id: 123 } },
      });

      expect(result).toEqual(pausedNexset);
      expect(calls[1]?.url).toContain("/data_sets/123/pause");
    });

    it("copies a nexset", async () => {
      const copiedNexset = createNexset({ id: 456, name: "Copy of Nexset" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: copiedNexset },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.nexsets.copy_nexset({
        params: { path: { set_id: 123 } },
      });

      expect(result).toEqual(copiedNexset);
      expect(calls[1]?.url).toContain("/data_sets/123/copy");
      expect(calls[1]?.method).toBe("POST");
    });
  });
});
