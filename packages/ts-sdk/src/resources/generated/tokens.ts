import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class TokensResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  /** Get info on current user */
  async get_current_user(init?: OperationInit<"get_current_user">): Promise<OperationData<"get_current_user">> {
    return this.client.requestOperation("get_current_user", "get", "/users/current", init);
  }

  /** Login with Basic Authentication */
  async login_with_basic_auth(init?: OperationInit<"login_with_basic_auth">): Promise<OperationData<"login_with_basic_auth">> {
    return this.client.requestOperation("login_with_basic_auth", "post", "/token", withSkipAuth(init));
  }

  /** Logout */
  async logout(init?: OperationInit<"logout">): Promise<OperationData<"logout">> {
    return this.client.requestOperation("logout", "post", "/token/logout", init);
  }
}