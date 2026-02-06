import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class DestinationsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_data_sinks">): Promise<OperationData<"get_data_sinks">> {
    return this.client.requestOperation("get_data_sinks", "get", "/data_sinks", init);
  }

  async create(init?: OperationInit<"create_data_sink">): Promise<OperationData<"create_data_sink">> {
    return this.client.requestOperation("create_data_sink", "post", "/data_sinks", init);
  }

  async get(init?: OperationInit<"get_data_sink">): Promise<OperationData<"get_data_sink">> {
    return this.client.requestOperation("get_data_sink", "get", "/data_sinks/{sink_id}", init);
  }

  async update(init?: OperationInit<"update_data_sink">): Promise<OperationData<"update_data_sink">> {
    return this.client.requestOperation("update_data_sink", "put", "/data_sinks/{sink_id}", init);
  }

  async delete(init?: OperationInit<"delete_data_sink">): Promise<OperationData<"delete_data_sink">> {
    return this.client.requestOperation("delete_data_sink", "delete", "/data_sinks/{sink_id}", init);
  }

  /** Activate a Sink */
  async activate_data_sink(init?: OperationInit<"activate_data_sink">): Promise<OperationData<"activate_data_sink">> {
    return this.client.requestOperation("activate_data_sink", "put", "/data_sinks/{sink_id}/activate", init);
  }

  /** Copy a Sink */
  async copy_data_sink_source(init?: OperationInit<"copy_data_sink_source">): Promise<OperationData<"copy_data_sink_source">> {
    return this.client.requestOperation("copy_data_sink_source", "post", "/data_sinks/{sink_id}/copy", init);
  }

  /** Create a Sink */
  async create_data_sink(init?: OperationInit<"create_data_sink">): Promise<OperationData<"create_data_sink">> {
    return this.client.requestOperation("create_data_sink", "post", "/data_sinks", init);
  }

  /** Delete a Sink */
  async delete_data_sink(init?: OperationInit<"delete_data_sink">): Promise<OperationData<"delete_data_sink">> {
    return this.client.requestOperation("delete_data_sink", "delete", "/data_sinks/{sink_id}", init);
  }

  /** Get Sink by ID */
  async get_data_sink(init?: OperationInit<"get_data_sink">): Promise<OperationData<"get_data_sink">> {
    return this.client.requestOperation("get_data_sink", "get", "/data_sinks/{sink_id}", init);
  }

  /** Get Sink by ID with Expanded References */
  async get_data_sink_expanded(init?: OperationInit<"get_data_sink_expanded">): Promise<OperationData<"get_data_sink_expanded">> {
    return this.client.requestOperation("get_data_sink_expanded", "get", "/data_sinks/{sink_id}?expand=1", init);
  }

  /** Get All Sinks */
  async get_data_sinks(init?: OperationInit<"get_data_sinks">): Promise<OperationData<"get_data_sinks">> {
    return this.client.requestOperation("get_data_sinks", "get", "/data_sinks", init);
  }

  /** Pause a Sink */
  async pause_data_sink(init?: OperationInit<"pause_data_sink">): Promise<OperationData<"pause_data_sink">> {
    return this.client.requestOperation("pause_data_sink", "put", "/data_sinks/{sink_id}/pause", init);
  }

  /** Update Sink */
  async update_data_sink(init?: OperationInit<"update_data_sink">): Promise<OperationData<"update_data_sink">> {
    return this.client.requestOperation("update_data_sink", "put", "/data_sinks/{sink_id}", init);
  }
}