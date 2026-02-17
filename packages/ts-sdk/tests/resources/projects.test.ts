/**
 * Unit tests for Projects resource operations.
 */

import { describe, expect, it, beforeEach } from "vitest";
import { createMockFetch } from "../utils/mock-fetch.js";
import { createProject, createProjectList, resetIdCounter } from "../utils/factories/index.js";
import { NexlaClient } from "../../src/client/nexla-client.js";

describe("ProjectsResource", () => {
  beforeEach(() => {
    resetIdCounter();
  });

  describe("list operations", () => {
    it("fetches all projects", async () => {
      const projects = createProjectList(3);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: projects },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.projects.list();

      expect(result).toEqual(projects);
      expect(calls.length).toBe(2);
      expect(calls[1]?.url).toContain("/projects");
    });

    it("passes query parameters correctly", async () => {
      const projects = createProjectList(2);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: projects },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.projects.list({ params: { query: { page: 2, per_page: 10 } } });

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

      const result = await client.projects.list();

      expect(result).toEqual([]);
    });
  });

  describe("get operations", () => {
    it("fetches project by ID", async () => {
      const project = createProject({ id: 123 });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: project },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.projects.get({ params: { path: { project_id: 123 } } });

      expect(result).toEqual(project);
      expect(calls[1]?.url).toContain("/projects/123");
    });

    it("handles project not found (404)", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 404, body: { message: "Project not found" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.projects.get({ params: { path: { project_id: 99999 } } })
      ).rejects.toThrow();
    });
  });

  describe("create operations", () => {
    it("creates a new project", async () => {
      const newProject = createProject({ name: "My New Project" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 201, body: newProject },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.projects.create({
        body: { name: "My New Project" },
      });

      expect(result).toEqual(newProject);
      expect(calls[1]?.method).toBe("POST");
      expect(calls[1]?.url).toContain("/projects");
    });

    it("creates a project with description", async () => {
      const newProject = createProject({
        name: "Project with Description",
        description: "A detailed project description"
      });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 201, body: newProject },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.projects.create({
        body: { name: "Project with Description", description: "A detailed project description" },
      });

      expect(result).toEqual(newProject);
      expect(calls[1]?.method).toBe("POST");
    });
  });

  describe("update operations", () => {
    it("updates existing project", async () => {
      const updatedProject = createProject({ id: 123, name: "Updated Project" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: updatedProject },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.projects.update({
        params: { path: { project_id: 123 } },
        body: { name: "Updated Project" },
      });

      expect(result).toEqual(updatedProject);
      expect(calls[1]?.method).toBe("PUT");
      expect(calls[1]?.url).toContain("/projects/123");
    });

    it("updates project description", async () => {
      const updatedProject = createProject({
        id: 123,
        description: "New description"
      });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: updatedProject },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.projects.update({
        params: { path: { project_id: 123 } },
        body: { description: "New description" },
      });

      expect(result).toEqual(updatedProject);
      expect(calls[1]?.method).toBe("PUT");
    });
  });

  describe("delete operations", () => {
    it("deletes project by ID", async () => {
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: { status: "deleted" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.projects.delete({ params: { path: { project_id: 123 } } });

      expect(calls[1]?.method).toBe("DELETE");
      expect(calls[1]?.url).toContain("/projects/123");
    });

    it("handles delete of non-existent project", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 404, body: { message: "Project not found" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.projects.delete({ params: { path: { project_id: 99999 } } })
      ).rejects.toThrow();
    });
  });

  describe("flow operations", () => {
    it("gets project flows", async () => {
      const flows = [{ id: 1, name: "Flow 1" }, { id: 2, name: "Flow 2" }];
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: flows },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.projects.get_project_flows({
        params: { path: { project_id: 123 } },
      });

      expect(result).toEqual(flows);
      expect(calls[1]?.url).toContain("/projects/123/flows");
      expect(calls[1]?.method).toBe("GET");
    });

    it("adds flows to project", async () => {
      const updatedProject = createProject({ id: 123 });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: updatedProject },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.projects.add_project_flows({
        params: { path: { project_id: 123 } },
        body: { flow_ids: [1, 2, 3] },
      });

      expect(result).toEqual(updatedProject);
      expect(calls[1]?.url).toContain("/projects/123/flows");
      expect(calls[1]?.method).toBe("PUT");
    });

    it("removes flows from project", async () => {
      const updatedProject = createProject({ id: 123 });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: updatedProject },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.projects.remove_project_flows({
        params: { path: { project_id: 123 } },
        body: { flow_ids: [1, 2] },
      });

      expect(result).toEqual(updatedProject);
      expect(calls[1]?.url).toContain("/projects/123/flows");
      expect(calls[1]?.method).toBe("DELETE");
    });

    it("replaces project flows list", async () => {
      const updatedProject = createProject({ id: 123 });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: updatedProject },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.projects.replace_project_flows({
        params: { path: { project_id: 123 } },
        body: { flow_ids: [4, 5, 6] },
      });

      expect(result).toEqual(updatedProject);
      expect(calls[1]?.url).toContain("/projects/123/flows");
      expect(calls[1]?.method).toBe("POST");
    });
  });
});
