import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class LookupsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_data_maps">): Promise<OperationData<"get_data_maps">> {
    return this.client.requestOperation("get_data_maps", "get", "/data_maps", init);
  }

  async create(init?: OperationInit<"create_static_data_map">): Promise<OperationData<"create_static_data_map">> {
    return this.client.requestOperation("create_static_data_map", "post", "/data_maps", init);
  }

  async get(init?: OperationInit<"get_data_map">): Promise<OperationData<"get_data_map">> {
    return this.client.requestOperation("get_data_map", "get", "/data_maps/{data_map_id}", init);
  }

  async update(init?: OperationInit<"update_data_map_metadata">): Promise<OperationData<"update_data_map_metadata">> {
    return this.client.requestOperation("update_data_map_metadata", "put", "/data_maps/{data_map_id}", init);
  }

  async delete(init?: OperationInit<"delete_data_map">): Promise<OperationData<"delete_data_map">> {
    return this.client.requestOperation("delete_data_map", "delete", "/data_maps/{data_map_id}", init);
  }

  /** Check Data Map Entries */
  async check_data_map_entries(init?: OperationInit<"check_data_map_entries">): Promise<OperationData<"check_data_map_entries">> {
    return this.client.requestOperation("check_data_map_entries", "get", "/data_maps/{data_map_id}/entries/{entry_keys}", init);
  }

  /** Create a Static Data Map */
  async create_static_data_map(init?: OperationInit<"create_static_data_map">): Promise<OperationData<"create_static_data_map">> {
    return this.client.requestOperation("create_static_data_map", "post", "/data_maps", init);
  }

  /** Delete a Data Map */
  async delete_data_map(init?: OperationInit<"delete_data_map">): Promise<OperationData<"delete_data_map">> {
    return this.client.requestOperation("delete_data_map", "delete", "/data_maps/{data_map_id}", init);
  }

  /** Delete Data Map Entries */
  async delete_data_map_entries(init?: OperationInit<"delete_data_map_entries">): Promise<OperationData<"delete_data_map_entries">> {
    return this.client.requestOperation("delete_data_map_entries", "delete", "/data_maps/{data_map_id}/entries/{entry_keys}", init);
  }

  /** Get Data Map by ID */
  async get_data_map(init?: OperationInit<"get_data_map">): Promise<OperationData<"get_data_map">> {
    return this.client.requestOperation("get_data_map", "get", "/data_maps/{data_map_id}", init);
  }

  /** Get all Data Maps */
  async get_data_maps(init?: OperationInit<"get_data_maps">): Promise<OperationData<"get_data_maps">> {
    return this.client.requestOperation("get_data_maps", "get", "/data_maps", init);
  }

  /** Update Data Map Metadata */
  async update_data_map_metadata(init?: OperationInit<"update_data_map_metadata">): Promise<OperationData<"update_data_map_metadata">> {
    return this.client.requestOperation("update_data_map_metadata", "put", "/data_maps/{data_map_id}", init);
  }

  /** Upsert Static Data Map Entries */
  async upsert_data_map_entries(init?: OperationInit<"upsert_data_map_entries">): Promise<OperationData<"upsert_data_map_entries">> {
    return this.client.requestOperation("upsert_data_map_entries", "put", "/data_maps/{data_map_id}/entries", init);
  }
}