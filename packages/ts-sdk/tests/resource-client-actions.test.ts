import { describe, expect, it } from "vitest";
import { ResourceClient } from "../src/resources/resource-client.js";
import type { NexlaClient } from "../src/client/nexla-client.js";

class FakeClient {
  public calls: Array<{ method: string; path: string }> = [];

  async request(method: string, path: string): Promise<unknown> {
    this.calls.push({ method, path });
    return { ok: true };
  }
}

describe("ResourceClient actions", () => {
  it("calls create on async_tasks", async () => {
    const fake = new FakeClient();
    const resource = new ResourceClient(fake as unknown as NexlaClient, "async_tasks");

    await resource.create({});

    expect(fake.calls[0]).toEqual({ method: "post", path: "/async_tasks" });
  });
});
