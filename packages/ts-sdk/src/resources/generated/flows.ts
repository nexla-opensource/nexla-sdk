import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class FlowsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_flows">): Promise<OperationData<"get_flows">> {
    return this.client.requestOperation("get_flows", "get", "/flows", init);
  }

  async get(init?: OperationInit<"get_flow_by_id">): Promise<OperationData<"get_flow_by_id">> {
    return this.client.requestOperation("get_flow_by_id", "get", "/flows/{flow_id}", init);
  }

  async delete(init?: OperationInit<"delete_flow">): Promise<OperationData<"delete_flow">> {
    return this.client.requestOperation("delete_flow", "delete", "/flows/{flow_id}", init);
  }

  /** Delete a Flow */
  async delete_flow(init?: OperationInit<"delete_flow">): Promise<OperationData<"delete_flow">> {
    return this.client.requestOperation("delete_flow", "delete", "/flows/{flow_id}", init);
  }

  /** Delete a Flow (by Resource ID) */
  async delete_flow_by_resource_id(init?: OperationInit<"delete_flow_by_resource_id">): Promise<OperationData<"delete_flow_by_resource_id">> {
    return this.client.requestOperation("delete_flow_by_resource_id", "delete", "/{resource_type}/{resource_id}/flow", init);
  }

  /** Activate a Flow */
  async flow_activate_with_flow_id(init?: OperationInit<"flow_activate_with_flow_id">): Promise<OperationData<"flow_activate_with_flow_id">> {
    return this.client.requestOperation("flow_activate_with_flow_id", "put", "/flows/{flow_id}/activate", init);
  }

  /** Activate a Flow (with Resource ID) */
  async flow_activate_with_resource_id(init?: OperationInit<"flow_activate_with_resource_id">): Promise<OperationData<"flow_activate_with_resource_id">> {
    return this.client.requestOperation("flow_activate_with_resource_id", "put", "/{resource_type}/{resource_id}/activate", init);
  }

  /** Copy a Flow */
  async flow_copy_with_flow_id(init?: OperationInit<"flow_copy_with_flow_id">): Promise<OperationData<"flow_copy_with_flow_id">> {
    return this.client.requestOperation("flow_copy_with_flow_id", "post", "/flows/{flow_id}/copy", init);
  }

  /** Generate an AI suggestion for flow documentation */
  async flow_docs_recommendation(init?: OperationInit<"flow_docs_recommendation">): Promise<OperationData<"flow_docs_recommendation">> {
    return this.client.requestOperation("flow_docs_recommendation", "post", "/flows/{flow_id}/docs/recommendation", init);
  }

  /** Pause a Flow */
  async flow_pause_with_flow_id(init?: OperationInit<"flow_pause_with_flow_id">): Promise<OperationData<"flow_pause_with_flow_id">> {
    return this.client.requestOperation("flow_pause_with_flow_id", "put", "/flows/{flow_id}/pause", init);
  }

  /** Pause a Flow (with Resource ID) */
  async flow_pause_with_resource_id(init?: OperationInit<"flow_pause_with_resource_id">): Promise<OperationData<"flow_pause_with_resource_id">> {
    return this.client.requestOperation("flow_pause_with_resource_id", "put", "/{resource_type}/{resource_id}/pause", init);
  }

  /** Get Flow by ID */
  async get_flow_by_id(init?: OperationInit<"get_flow_by_id">): Promise<OperationData<"get_flow_by_id">> {
    return this.client.requestOperation("get_flow_by_id", "get", "/flows/{flow_id}", init);
  }

  /** Get Flow (by Resource ID) */
  async get_flow_by_resource_id(init?: OperationInit<"get_flow_by_resource_id">): Promise<OperationData<"get_flow_by_resource_id">> {
    return this.client.requestOperation("get_flow_by_resource_id", "get", "/{resource_type}/{resource_id}/flow", init);
  }

  /** Get All Flows */
  async get_flows(init?: OperationInit<"get_flows">): Promise<OperationData<"get_flows">> {
    return this.client.requestOperation("get_flows", "get", "/flows", init);
  }
}