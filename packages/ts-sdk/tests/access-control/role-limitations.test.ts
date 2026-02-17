/**
 * Unit tests for access role limitations.
 * Based on admin-api spec/access_control/role_limitations_spec.rb
 */

import { describe, expect, it, beforeEach } from "vitest";
import { createMockFetch } from "../utils/mock-fetch.js";
import { createAccessor, resetIdCounter } from "../utils/factories/index.js";
import { NexlaClient } from "../../src/client/nexla-client.js";

describe("AccessRoleLimitations", () => {
  beforeEach(() => {
    resetIdCounter();
  });

  describe("collaborator role", () => {
    it("is supported for sources", async () => {
      const accessor = createAccessor({ access_roles: ["collaborator"] });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [accessor] },
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

      expect(result[0].access_roles).toContain("collaborator");
    });

    it("is supported for credentials", async () => {
      const accessor = createAccessor({ access_roles: ["collaborator"] });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [accessor] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.add_data_credential_accessors({
        params: { path: { data_credential_id: 123 } },
        body: { accessors: [{ id: 456, type: "user", access_role: "collaborator" }] },
      });

      expect(result[0].access_roles).toContain("collaborator");
    });

    it("is supported for nexsets", async () => {
      const accessor = createAccessor({ access_roles: ["collaborator"] });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [accessor] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.add_nexset_accessors({
        params: { path: { data_set_id: 123 } },
        body: { accessors: [{ id: 456, type: "user", access_role: "collaborator" }] },
      });

      expect(result[0].access_roles).toContain("collaborator");
    });
  });

  describe("admin role", () => {
    it("is supported for sources", async () => {
      const accessor = createAccessor({ access_roles: ["admin"] });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [accessor] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.add_data_source_accessors({
        params: { path: { data_source_id: 123 } },
        body: { accessors: [{ id: 456, type: "user", access_role: "admin" }] },
      });

      expect(result[0].access_roles).toContain("admin");
    });

    it("is supported for teams", async () => {
      const accessor = createAccessor({ access_roles: ["admin"] });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [accessor] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.add_team_accessors({
        params: { path: { team_id: 123 } },
        body: { accessors: [{ id: 456, type: "user", access_role: "admin" }] },
      });

      expect(result[0].access_roles).toContain("admin");
    });
  });

  describe("operator role", () => {
    it("is supported for sources", async () => {
      const accessor = createAccessor({ access_roles: ["operator"] });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [accessor] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.add_data_source_accessors({
        params: { path: { data_source_id: 123 } },
        body: { accessors: [{ id: 456, type: "user", access_role: "operator" }] },
      });

      expect(result[0].access_roles).toContain("operator");
    });

    it("is supported for nexsets", async () => {
      const accessor = createAccessor({ access_roles: ["operator"] });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [accessor] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.add_nexset_accessors({
        params: { path: { data_set_id: 123 } },
        body: { accessors: [{ id: 456, type: "user", access_role: "operator" }] },
      });

      expect(result[0].access_roles).toContain("operator");
    });
  });

  describe("sharer role", () => {
    it("is supported for nexsets (data_sets)", async () => {
      const accessor = createAccessor({ access_roles: ["sharer"] });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [accessor] },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.access_control.add_nexset_accessors({
        params: { path: { data_set_id: 123 } },
        body: { accessors: [{ id: 456, type: "user", access_role: "sharer" }] },
      });

      expect(result[0].access_roles).toContain("sharer");
    });

    it("returns error for sources (sharer not allowed)", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 400, body: { message: "Invalid access role 'sharer' for data_source" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.access_control.add_data_source_accessors({
          params: { path: { data_source_id: 123 } },
          body: { accessors: [{ id: 456, type: "user", access_role: "sharer" }] },
        })
      ).rejects.toThrow();
    });

    it("returns error for teams (sharer not allowed)", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 400, body: { message: "Invalid access role 'sharer' for team" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.access_control.add_team_accessors({
          params: { path: { team_id: 123 } },
          body: { accessors: [{ id: 456, type: "user", access_role: "sharer" }] },
        })
      ).rejects.toThrow();
    });
  });

  describe("invalid role", () => {
    it("returns bad request for unknown role", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 400, body: { message: "Invalid access role 'unknown_role'" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.access_control.add_data_source_accessors({
          params: { path: { data_source_id: 123 } },
          body: { accessors: [{ id: 456, type: "user", access_role: "unknown_role" }] },
        })
      ).rejects.toThrow();
    });
  });

  describe("accessor type", () => {
    it("supports USER type", async () => {
      const accessor = createAccessor({ type: "USER" });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [accessor] },
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

      expect(result[0].type).toBe("USER");
    });

    it("supports TEAM type", async () => {
      const accessor = createAccessor({ type: "TEAM" });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: [accessor] },
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

      expect(result[0].type).toBe("TEAM");
    });
  });
});
