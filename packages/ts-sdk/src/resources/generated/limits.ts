import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class LimitsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  /** Get current rate limit and usage */
  async limits(init?: OperationInit<"limits">): Promise<OperationData<"limits">> {
    return this.client.requestOperation("limits", "get", "/limits", init);
  }
}