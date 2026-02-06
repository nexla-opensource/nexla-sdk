import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class SourcesResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_data_sources">): Promise<OperationData<"get_data_sources">> {
    return this.client.requestOperation("get_data_sources", "get", "/data_sources", init);
  }

  async create(init?: OperationInit<"create_data_source">): Promise<OperationData<"create_data_source">> {
    return this.client.requestOperation("create_data_source", "post", "/data_sources", init);
  }

  async get(init?: OperationInit<"get_data_source">): Promise<OperationData<"get_data_source">> {
    return this.client.requestOperation("get_data_source", "get", "/data_sources/{source_id}", init);
  }

  async update(init?: OperationInit<"update_data_source">): Promise<OperationData<"update_data_source">> {
    return this.client.requestOperation("update_data_source", "put", "/data_sources/{source_id}", init);
  }

  async delete(init?: OperationInit<"delete_data_source">): Promise<OperationData<"delete_data_source">> {
    return this.client.requestOperation("delete_data_source", "delete", "/data_sources/{source_id}", init);
  }

  /** Activate a Source */
  async activate_source(init?: OperationInit<"activate_source">): Promise<OperationData<"activate_source">> {
    return this.client.requestOperation("activate_source", "put", "/data_sources/{source_id}/activate", init);
  }

  /** Copy a Source */
  async copy_source(init?: OperationInit<"copy_source">): Promise<OperationData<"copy_source">> {
    return this.client.requestOperation("copy_source", "post", "/data_sources/{source_id}/copy", init);
  }

  /** Create a Source */
  async create_data_source(init?: OperationInit<"create_data_source">): Promise<OperationData<"create_data_source">> {
    return this.client.requestOperation("create_data_source", "post", "/data_sources", init);
  }

  /** Delete a Source */
  async delete_data_source(init?: OperationInit<"delete_data_source">): Promise<OperationData<"delete_data_source">> {
    return this.client.requestOperation("delete_data_source", "delete", "/data_sources/{source_id}", init);
  }

  /** Get Source by ID */
  async get_data_source(init?: OperationInit<"get_data_source">): Promise<OperationData<"get_data_source">> {
    return this.client.requestOperation("get_data_source", "get", "/data_sources/{source_id}", init);
  }

  /** Get Source by ID with Expanded References */
  async get_data_source_expanded(init?: OperationInit<"get_data_source_expanded">): Promise<OperationData<"get_data_source_expanded">> {
    return this.client.requestOperation("get_data_source_expanded", "get", "/data_sources/{source_id}?expand=1", init);
  }

  /** Get All Sources */
  async get_data_sources(init?: OperationInit<"get_data_sources">): Promise<OperationData<"get_data_sources">> {
    return this.client.requestOperation("get_data_sources", "get", "/data_sources", init);
  }

  /** Pause a Source */
  async pause_source(init?: OperationInit<"pause_source">): Promise<OperationData<"pause_source">> {
    return this.client.requestOperation("pause_source", "put", "/data_sources/{source_id}/pause", init);
  }

  /** Update a Source */
  async update_data_source(init?: OperationInit<"update_data_source">): Promise<OperationData<"update_data_source">> {
    return this.client.requestOperation("update_data_source", "put", "/data_sources/{source_id}", init);
  }
}