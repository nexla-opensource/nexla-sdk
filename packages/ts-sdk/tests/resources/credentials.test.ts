/**
 * Unit tests for Credentials resource operations.
 */

import { describe, expect, it, beforeEach } from "vitest";
import { createMockFetch } from "../utils/mock-fetch.js";
import { createCredential, createCredentialList, resetIdCounter } from "../utils/factories/index.js";
import { NexlaClient } from "../../src/client/nexla-client.js";

describe("CredentialsResource", () => {
  beforeEach(() => {
    resetIdCounter();
  });

  describe("list operations", () => {
    it("fetches all credentials", async () => {
      const credentials = createCredentialList(3);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: credentials },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.credentials.list();

      expect(result).toEqual(credentials);
      expect(calls.length).toBe(2);
      expect(calls[1]?.url).toContain("/data_credentials");
    });

    it("filters by credentials_type", async () => {
      const credentials = createCredentialList(2, { credentials_type: "s3" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: credentials },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.credentials.list({ params: { query: { credentials_type: "s3" } } });

      const requestUrl = calls[1]?.url ?? "";
      expect(requestUrl).toContain("credentials_type=s3");
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

      const result = await client.credentials.list();

      expect(result).toEqual([]);
    });
  });

  describe("get operations", () => {
    it("fetches credential by ID", async () => {
      const credential = createCredential({ id: 123 });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: credential },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.credentials.get({
        params: { path: { credential_id: 123 } },
      });

      expect(result).toEqual(credential);
      expect(calls[1]?.url).toContain("/data_credentials/123");
    });

    it("handles credential not found (404)", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 404, body: { message: "Credential not found" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.credentials.get({ params: { path: { credential_id: 99999 } } })
      ).rejects.toThrow();
    });
  });

  describe("create operations", () => {
    it("creates a new credential", async () => {
      const newCredential = createCredential({ name: "My New Credential" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 201, body: newCredential },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.credentials.create({
        body: {
          name: "My New Credential",
          credentials_type: "postgres",
          config: { host: "localhost" },
        },
      });

      expect(result).toEqual(newCredential);
      expect(calls[1]?.method).toBe("POST");
    });
  });

  describe("update operations", () => {
    it("updates existing credential", async () => {
      const updatedCredential = createCredential({ id: 123, name: "Updated Credential" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: updatedCredential },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.credentials.update({
        params: { path: { credential_id: 123 } },
        body: { name: "Updated Credential" },
      });

      expect(result).toEqual(updatedCredential);
      expect(calls[1]?.method).toBe("PUT");
      expect(calls[1]?.url).toContain("/data_credentials/123");
    });
  });

  describe("delete operations", () => {
    it("deletes credential by ID", async () => {
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: { status: "deleted" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.credentials.delete({ params: { path: { credential_id: 123 } } });

      expect(calls[1]?.method).toBe("DELETE");
      expect(calls[1]?.url).toContain("/data_credentials/123");
    });
  });

  describe("probe operations", () => {
    it("probes credential validity", async () => {
      const probeResult = { status: "ok", connection_verified: true };
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: probeResult },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.credentials.data_credential_probe({
        params: { path: { credential_id: 123 } },
      });

      expect(result).toEqual(probeResult);
      expect(calls[1]?.url).toContain("/data_credentials/123/probe");
    });

    it("returns tree structure", async () => {
      const treeResult = {
        status: "ok",
        object: { tree: [{ name: "folder1", type: "folder" }] },
      };
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: treeResult },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.credentials.preview_storage_structure({
        params: { path: { credential_id: 123 } },
      });

      expect(result).toEqual(treeResult);
      expect(calls[1]?.url).toContain("/data_credentials/123/probe/tree");
    });
  });

  describe("verification status", () => {
    it("returns VERIFIED status", async () => {
      const credential = createCredential({ verified_status: "VERIFIED" });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: credential },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.credentials.get({
        params: { path: { credential_id: 123 } },
      });

      expect(result.verified_status).toBe("VERIFIED");
    });

    it("returns FAILED status", async () => {
      const credential = createCredential({ verified_status: "FAILED" });
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: credential },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.credentials.get({
        params: { path: { credential_id: 123 } },
      });

      expect(result.verified_status).toBe("FAILED");
    });
  });
});
