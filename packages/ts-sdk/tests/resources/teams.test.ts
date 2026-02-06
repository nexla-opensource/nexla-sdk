/**
 * Unit tests for Teams resource operations.
 */

import { describe, expect, it, beforeEach } from "vitest";
import { createMockFetch } from "../utils/mock-fetch.js";
import { createTeam, createTeamList, createTeamMember, resetIdCounter } from "../utils/factories/index.js";
import { NexlaClient } from "../../src/client/nexla-client.js";

describe("TeamsResource", () => {
  beforeEach(() => {
    resetIdCounter();
  });

  describe("list operations", () => {
    it("fetches all teams", async () => {
      const teams = createTeamList(3);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: teams },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.teams.list();

      expect(result).toEqual(teams);
      expect(calls.length).toBe(2);
      expect(calls[1]?.url).toContain("/teams");
    });

    it("passes query parameters correctly", async () => {
      const teams = createTeamList(2);
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: teams },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.teams.list({ params: { query: { page: 2, per_page: 10 } } });

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

      const result = await client.teams.list();

      expect(result).toEqual([]);
    });
  });

  describe("get operations", () => {
    it("fetches team by ID", async () => {
      const team = createTeam({ id: 123 });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: team },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.teams.get({ params: { path: { team_id: 123 } } });

      expect(result).toEqual(team);
      expect(calls[1]?.url).toContain("/teams/123");
    });

    it("handles team not found (404)", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 404, body: { message: "Team not found" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.teams.get({ params: { path: { team_id: 99999 } } })
      ).rejects.toThrow();
    });
  });

  describe("create operations", () => {
    it("creates a new team with name", async () => {
      const newTeam = createTeam({ name: "My New Team" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 201, body: newTeam },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.teams.create({
        body: { name: "My New Team" },
      });

      expect(result).toEqual(newTeam);
      expect(calls[1]?.method).toBe("POST");
      expect(calls[1]?.url).toContain("/teams");
    });

    it("creates a team with members", async () => {
      const members = [
        createTeamMember({ email: "member1@test.com", admin: false }),
        createTeamMember({ email: "member2@test.com", admin: true }),
      ];
      const newTeam = createTeam({ name: "Team with Members", members });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 201, body: newTeam },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.teams.create({
        body: {
          name: "Team with Members",
          members: [
            { email: "member1@test.com", admin: false },
            { email: "member2@test.com", admin: true },
          ],
        },
      });

      expect(result).toEqual(newTeam);
      expect(calls[1]?.method).toBe("POST");
    });
  });

  describe("update operations", () => {
    it("updates existing team", async () => {
      const updatedTeam = createTeam({ id: 123, name: "Updated Team" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: updatedTeam },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.teams.update({
        params: { path: { team_id: 123 } },
        body: { name: "Updated Team" },
      });

      expect(result).toEqual(updatedTeam);
      expect(calls[1]?.method).toBe("PUT");
      expect(calls[1]?.url).toContain("/teams/123");
    });

    it("updates team description", async () => {
      const updatedTeam = createTeam({ id: 456, description: "New description" });
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: updatedTeam },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      const result = await client.teams.update({
        params: { path: { team_id: 456 } },
        body: { description: "New description" },
      });

      expect(result).toEqual(updatedTeam);
      expect(calls[1]?.method).toBe("PUT");
      expect(calls[1]?.url).toContain("/teams/456");
    });
  });

  describe("delete operations", () => {
    it("deletes team by ID", async () => {
      const { fetchFn, calls } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 200, body: { status: "deleted" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await client.teams.delete({ params: { path: { team_id: 123 } } });

      expect(calls[1]?.method).toBe("DELETE");
      expect(calls[1]?.url).toContain("/teams/123");
    });

    it("handles delete of non-existent team", async () => {
      const { fetchFn } = createMockFetch([
        { status: 200, body: { access_token: "token", expires_in: 7200 } },
        { status: 404, body: { message: "Team not found" } },
      ]);

      const client = new NexlaClient({
        serviceKey: "test-key",
        baseUrl: "https://test.nexla.io/nexla-api",
        fetch: fetchFn,
      });

      await expect(
        client.teams.delete({ params: { path: { team_id: 99999 } } })
      ).rejects.toThrow();
    });
  });
});
