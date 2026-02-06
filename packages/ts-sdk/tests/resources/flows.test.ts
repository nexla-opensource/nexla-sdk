/**
 * Unit tests for Flows resource operations.
 */

import { describe, expect, it, beforeEach } from "vitest";
import { createMockFetch } from "../utils/mock-fetch.js";
import { createFlow, createFlowList, resetIdCounter } from "../utils/factories/index.js";
import { NexlaClient } from "../../src/client/nexla-client.js";

describe("FlowsResource", () => {
  beforeEach(() => {
    resetIdCounter();
  });

  describe("list operations", () => {
    it("fetches all flows", async () => {
      const flows = createFlowList(3);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: flows },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.flows.list();

      expect(result).toEqual(flows);
      expect(calls.length).toBe(2);
      expect(calls[1]?.url).toContain("/flows");
    });

    it("passes query parameters correctly", async () => {
      const flows = createFlowList(2);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: flows },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.flows.list({ params: { query: { page: 2, per_page: 10 } } });

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

      const result = await client.flows.list();

      expect(result).toEqual([]);
    });
  });

  describe("get operations", () => {
    it("fetches flow by ID", async () => {
      const flow = createFlow({ id: 123 });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: flow },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.flows.get_flow_by_id({ params: { path: { flow_id: 123 } } });

      expect(result).toEqual(flow);
      expect(calls[1]?.url).toContain("/flows/123");
    });

    it("fetches flow using get alias", async () => {
      const flow = createFlow({ id: 456 });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: flow },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.flows.get({ params: { path: { flow_id: 456 } } });

      expect(result).toEqual(flow);
      expect(calls[1]?.url).toContain("/flows/456");
    });

    it("handles flow not found (404)", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 404, body: { message: "Flow not found" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.flows.get_flow_by_id({ params: { path: { flow_id: 99999 } } })
      ).rejects.toThrow();
    });
  });

  describe("delete operations", () => {
    it("deletes flow by ID", async () => {
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: { status: "deleted" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.flows.delete_flow({ params: { path: { flow_id: 123 } } });

      expect(calls[1]?.method).toBe("DELETE");
      expect(calls[1]?.url).toContain("/flows/123");
    });

    it("deletes flow using delete alias", async () => {
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: { status: "deleted" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.flows.delete({ params: { path: { flow_id: 456 } } });

      expect(calls[1]?.method).toBe("DELETE");
      expect(calls[1]?.url).toContain("/flows/456");
    });
  });

  describe("lifecycle operations", () => {
    it("activates a paused flow", async () => {
      const activatedFlow = createFlow({ id: 123, status: "ACTIVE" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: activatedFlow },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.flows.flow_activate_with_flow_id({
        params: { path: { flow_id: 123 } },
      });

      expect(result).toEqual(activatedFlow);
      expect(calls[1]?.url).toContain("/flows/123/activate");
      expect(calls[1]?.method).toBe("PUT");
    });

    it("pauses an active flow", async () => {
      const pausedFlow = createFlow({ id: 123, status: "PAUSED" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: pausedFlow },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.flows.flow_pause_with_flow_id({
        params: { path: { flow_id: 123 } },
      });

      expect(result).toEqual(pausedFlow);
      expect(calls[1]?.url).toContain("/flows/123/pause");
      expect(calls[1]?.method).toBe("PUT");
    });

    it("copies a flow", async () => {
      const copiedFlow = createFlow({ id: 456, name: "Copy of Flow" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: copiedFlow },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.flows.flow_copy_with_flow_id({
        params: { path: { flow_id: 123 } },
      });

      expect(result).toEqual(copiedFlow);
      expect(calls[1]?.url).toContain("/flows/123/copy");
      expect(calls[1]?.method).toBe("POST");
    });
  });
});
