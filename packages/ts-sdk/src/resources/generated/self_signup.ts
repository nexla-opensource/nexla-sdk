import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class SelfSignupResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  /** Sign Up */
  async self_sign_up(init?: OperationInit<"self_sign_up">): Promise<OperationData<"self_sign_up">> {
    return this.client.requestOperation("self_sign_up", "post", "/signup", init);
  }

  /** Verify Email */
  async verify_email(init?: OperationInit<"verify_email">): Promise<OperationData<"verify_email">> {
    return this.client.requestOperation("verify_email", "get", "/signup/verify_email", init);
  }
}