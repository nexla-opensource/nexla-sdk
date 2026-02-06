/**
 * Unit tests for accessor management operations.
 */

import { describe, expect, it, beforeEach } from "vitest";
import { createMockFetch } from "../utils/mock-fetch.js";
import { createAccessor, createAccessorList, resetIdCounter } from "../utils/factories/index.js";
import { NexlaClient } from "../../src/client/nexla-client.js";

describe("AccessorManagement", () => {
  beforeEach(() => {
    resetIdCounter();
  });

  describe("get accessors", () => {
    it("fetches accessors for a source", async () => {
      const accessors = createAccessorList(3);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: accessors },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.get_data_source_accessors({
        params: { path: { data_source_id: 123 } },
      });

      expect(result).toEqual(accessors);
      expect(calls[1]?.url).toContain("/data_sources/123/accessors");
    });

    it("fetches accessors for a credential", async () => {
      const accessors = createAccessorList(2);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: accessors },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.get_data_credential_accessors({
        params: { path: { data_credential_id: 456 } },
      });

      expect(result).toEqual(accessors);
      expect(calls[1]?.url).toContain("/data_credentials/456/accessors");
    });

    it("returns empty list when no accessors", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.get_data_source_accessors({
        params: { path: { data_source_id: 123 } },
      });

      expect(result).toEqual([]);
    });
  });

  describe("add accessors", () => {
    it("adds user accessor with collaborator role", async () => {
      const newAccessor = createAccessor({ type: "USER", access_roles: ["collaborator"] });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [newAccessor] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.add_data_source_accessors({
        params: { path: { data_source_id: 123 } },
        body: { accessors: [{ id: 456, type: "user", access_role: "collaborator" }] },
      });

      expect(result).toEqual([newAccessor]);
      expect(calls[1]?.method).toBe("PUT");
      expect(calls[1]?.url).toContain("/data_sources/123/accessors");
    });

    it("adds team accessor", async () => {
      const teamAccessor = createAccessor({ type: "TEAM", access_roles: ["collaborator"] });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [teamAccessor] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.add_data_source_accessors({
        params: { path: { data_source_id: 123 } },
        body: { accessors: [{ id: 789, type: "team", access_role: "collaborator" }] },
      });

      expect(result).toEqual([teamAccessor]);
    });

    it("adds multiple accessors at once", async () => {
      const accessors = createAccessorList(3);
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: accessors },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.add_data_source_accessors({
        params: { path: { data_source_id: 123 } },
        body: {
          accessors: [
            { id: 1, type: "user", access_role: "collaborator" },
            { id: 2, type: "team", access_role: "admin" },
            { id: 3, type: "user", access_role: "operator" },
          ],
        },
      });

      expect(result.length).toBe(3);
    });
  });

  describe("replace accessors", () => {
    it("replaces entire accessor list", async () => {
      const newAccessors = [createAccessor({ type: "USER", access_roles: ["owner"] })];
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: newAccessors },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.replace_data_source_accessors({
        params: { path: { data_source_id: 123 } },
        body: { accessors: [{ id: 456, type: "user", access_role: "owner" }] },
      });

      expect(result).toEqual(newAccessors);
      expect(calls[1]?.method).toBe("POST");
    });
  });

  describe("delete accessors", () => {
    it("removes specific accessors", async () => {
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.delete_data_source_accessors({
        params: { path: { data_source_id: 123 } },
        body: { accessors: [{ id: 456, type: "user" }] },
      });

      expect(result).toEqual([]);
      expect(calls[1]?.method).toBe("DELETE");
    });
  });

  describe("error handling", () => {
    it("handles 404 for non-existent resource", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 404, body: { message: "Resource not found" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.access_control.get_data_source_accessors({
          params: { path: { data_source_id: 99999 } },
        })
      ).rejects.toThrow();
    });

    it("handles 403 for insufficient permissions", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 403, body: { message: "Forbidden" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.access_control.add_data_source_accessors({
          params: { path: { data_source_id: 123 } },
          body: { accessors: [{ id: 456, type: "user", access_role: "admin" }] },
        })
      ).rejects.toThrow();
    });
  });
});
