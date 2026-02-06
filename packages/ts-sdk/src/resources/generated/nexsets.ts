import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class NexsetsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_nexsets">): Promise<OperationData<"get_nexsets">> {
    return this.client.requestOperation("get_nexsets", "get", "/data_sets", init);
  }

  async create(init?: OperationInit<"create_nexset">): Promise<OperationData<"create_nexset">> {
    return this.client.requestOperation("create_nexset", "post", "/data_sets", init);
  }

  async get(init?: OperationInit<"get_nexset">): Promise<OperationData<"get_nexset">> {
    return this.client.requestOperation("get_nexset", "get", "/data_sets/{set_id}", init);
  }

  async update(init?: OperationInit<"update_nexset">): Promise<OperationData<"update_nexset">> {
    return this.client.requestOperation("update_nexset", "put", "/data_sets/{set_id}", init);
  }

  async delete(init?: OperationInit<"delete_nexset">): Promise<OperationData<"delete_nexset">> {
    return this.client.requestOperation("delete_nexset", "delete", "/data_sets/{set_id}", init);
  }

  /** Activate Nexset */
  async activate_nexset(init?: OperationInit<"activate_nexset">): Promise<OperationData<"activate_nexset">> {
    return this.client.requestOperation("activate_nexset", "put", "/data_sets/{set_id}/activate", init);
  }

  /** Copy Nexset */
  async copy_nexset(init?: OperationInit<"copy_nexset">): Promise<OperationData<"copy_nexset">> {
    return this.client.requestOperation("copy_nexset", "post", "/data_sets/{set_id}/copy", init);
  }

  /** Create a Nexset */
  async create_nexset(init?: OperationInit<"create_nexset">): Promise<OperationData<"create_nexset">> {
    return this.client.requestOperation("create_nexset", "post", "/data_sets", init);
  }

  /** Generate an AI suggestion for Nexset documentation */
  async data_set_docs_recommendation(init?: OperationInit<"data_set_docs_recommendation">): Promise<OperationData<"data_set_docs_recommendation">> {
    return this.client.requestOperation("data_set_docs_recommendation", "post", "/data_sets/{data_set_id}/docs/recommendation", init);
  }

  /** Delete a Nexset */
  async delete_nexset(init?: OperationInit<"delete_nexset">): Promise<OperationData<"delete_nexset">> {
    return this.client.requestOperation("delete_nexset", "delete", "/data_sets/{set_id}", init);
  }

  /** Get a Nexset */
  async get_nexset(init?: OperationInit<"get_nexset">): Promise<OperationData<"get_nexset">> {
    return this.client.requestOperation("get_nexset", "get", "/data_sets/{set_id}", init);
  }

  /** Get Nexset Samples */
  async get_nexset_samples(init?: OperationInit<"get_nexset_samples">): Promise<OperationData<"get_nexset_samples">> {
    return this.client.requestOperation("get_nexset_samples", "get", "/data_sets/{set_id}/samples", init);
  }

  /** Get All Nexsets */
  async get_nexsets(init?: OperationInit<"get_nexsets">): Promise<OperationData<"get_nexsets">> {
    return this.client.requestOperation("get_nexsets", "get", "/data_sets", init);
  }

  /** Pause Nexset */
  async pause_nexset(init?: OperationInit<"pause_nexset">): Promise<OperationData<"pause_nexset">> {
    return this.client.requestOperation("pause_nexset", "put", "/data_sets/{set_id}/pause", init);
  }

  /** Update a Nexset */
  async update_nexset(init?: OperationInit<"update_nexset">): Promise<OperationData<"update_nexset">> {
    return this.client.requestOperation("update_nexset", "put", "/data_sets/{set_id}", init);
  }
}