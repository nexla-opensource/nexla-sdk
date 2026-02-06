import { describe, expect, it } from "vitest";
import { NexlaClient } from "../../src/client/nexla-client.js";

const serviceKey = process.env.NEXLA_SERVICE_KEY;
const accessToken = process.env.NEXLA_ACCESS_TOKEN;
const hasAuth = Boolean(serviceKey || accessToken);

const describeIf = hasAuth ? describe : describe.skip;

const createClient = (): NexlaClient => {
  const options: {
    serviceKey?: string;
    accessToken?: string;
    baseUrl?: string;
  } = {};

  if (serviceKey) {
    options.serviceKey = serviceKey;
  } else if (accessToken) {
    options.accessToken = accessToken;
  }

  if (process.env.NEXLA_API_URL) {
    options.baseUrl = process.env.NEXLA_API_URL;
  }

  return new NexlaClient(options);
};

describeIf("Live API integration", () => {
  it("can list flows with real credentials", async () => {
    const client = createClient();
    const result = await client.flows.list();

    expect(result).toBeDefined();
  });

  it("can perform typed raw GET calls", async () => {
    const client = createClient();
    const { data } = await client.raw.GET("/flows");

    expect(data).toBeDefined();
  });
});
