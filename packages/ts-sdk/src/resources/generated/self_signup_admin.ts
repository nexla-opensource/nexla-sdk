import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class SelfSignupAdminResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  /** Add self-sign-up blocked domain for admins. */
  async add_self_signup_blocked_domain(init?: OperationInit<"add_self_signup_blocked_domain">): Promise<OperationData<"add_self_signup_blocked_domain">> {
    return this.client.requestOperation("add_self_signup_blocked_domain", "post", "/self_signup_blocked_domains", init);
  }

  /** Approve Self Sign Up Request */
  async approve_self_sign_up_request(init?: OperationInit<"approve_self_sign_up_request">): Promise<OperationData<"approve_self_sign_up_request">> {
    return this.client.requestOperation("approve_self_sign_up_request", "put", "/self_signup_requests/{request_id}/approve", init);
  }

  /** Delete self-sign-up blocked domain for admins. */
  async delete_self_signup_blocked_domain(init?: OperationInit<"delete_self_signup_blocked_domain">): Promise<OperationData<"delete_self_signup_blocked_domain">> {
    return this.client.requestOperation("delete_self_signup_blocked_domain", "delete", "/self_signup_blocked_domains/{domain_id}", init);
  }

  /** List self-sign-up blocked domains for admins. */
  async get_self_signup_blocked_domains(init?: OperationInit<"get_self_signup_blocked_domains">): Promise<OperationData<"get_self_signup_blocked_domains">> {
    return this.client.requestOperation("get_self_signup_blocked_domains", "get", "/self_signup_blocked_domains", init);
  }

  /** List Self Sign Up Requests */
  async get_self_signup_requests(init?: OperationInit<"get_self_signup_requests">): Promise<OperationData<"get_self_signup_requests">> {
    return this.client.requestOperation("get_self_signup_requests", "get", "/self_signup_requests", init);
  }

  /** Update self-sign-up blocked domain for admins. */
  async update_self_signup_blocked_domain(init?: OperationInit<"update_self_signup_blocked_domain">): Promise<OperationData<"update_self_signup_blocked_domain">> {
    return this.client.requestOperation("update_self_signup_blocked_domain", "put", "/self_signup_blocked_domains/{domain_id}", init);
  }
}