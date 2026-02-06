import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class UserSettingsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_user_settings">): Promise<OperationData<"get_user_settings">> {
    return this.client.requestOperation("get_user_settings", "get", "/user_settings", init);
  }

  /** Get the current user's settings */
  async get_user_settings(init?: OperationInit<"get_user_settings">): Promise<OperationData<"get_user_settings">> {
    return this.client.requestOperation("get_user_settings", "get", "/user_settings", init);
  }
}