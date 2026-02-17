import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class ApprovalRequestsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  /** Approve pending approval requests */
  async approve_approval_request(init?: OperationInit<"approve_approval_request">): Promise<OperationData<"approve_approval_request">> {
    return this.client.requestOperation("approve_approval_request", "put", "/approval_requests/{request_id}/approve", init);
  }

  /** Get all pending approval requests. */
  async get_pending_approval_requests(init?: OperationInit<"get_pending_approval_requests">): Promise<OperationData<"get_pending_approval_requests">> {
    return this.client.requestOperation("get_pending_approval_requests", "get", "/approval_requests/pending", init);
  }

  /** Get all requested approval requests by the user. */
  async get_requested_approval_requests(init?: OperationInit<"get_requested_approval_requests">): Promise<OperationData<"get_requested_approval_requests">> {
    return this.client.requestOperation("get_requested_approval_requests", "get", "/approval_requests/requested", init);
  }

  /** Reject pending approval requests */
  async reject_approval_request(init?: OperationInit<"reject_approval_request">): Promise<OperationData<"reject_approval_request">> {
    return this.client.requestOperation("reject_approval_request", "delete", "/approval_requests/{request_id}/reject", init);
  }
}