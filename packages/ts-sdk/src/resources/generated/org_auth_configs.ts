import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class OrgAuthConfigsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_api_auth_configs">): Promise<OperationData<"get_api_auth_configs">> {
    return this.client.requestOperation("get_api_auth_configs", "get", "/api_auth_configs", init);
  }

  async create(init?: OperationInit<"create_api_auth_config">): Promise<OperationData<"create_api_auth_config">> {
    return this.client.requestOperation("create_api_auth_config", "post", "/api_auth_configs", init);
  }

  async get(init?: OperationInit<"get_api_auth_configs">): Promise<OperationData<"get_api_auth_configs">> {
    return this.client.requestOperation("get_api_auth_configs", "get", "/api_auth_configs/{auth_config_id}", init);
  }

  async update(init?: OperationInit<"update_api_auth_config">): Promise<OperationData<"update_api_auth_config">> {
    return this.client.requestOperation("update_api_auth_config", "put", "/api_auth_configs/{auth_config_id}", init);
  }

  async delete(init?: OperationInit<"delete_api_auth_config">): Promise<OperationData<"delete_api_auth_config">> {
    return this.client.requestOperation("delete_api_auth_config", "delete", "/api_auth_configs/{auth_config_id}", init);
  }

  /** Create auth config. */
  async create_api_auth_config(init?: OperationInit<"create_api_auth_config">): Promise<OperationData<"create_api_auth_config">> {
    return this.client.requestOperation("create_api_auth_config", "post", "/api_auth_configs", init);
  }

  /** Delete auth config. */
  async delete_api_auth_config(init?: OperationInit<"delete_api_auth_config">): Promise<OperationData<"delete_api_auth_config">> {
    return this.client.requestOperation("delete_api_auth_config", "delete", "/api_auth_configs/{auth_config_id}", init);
  }

  /** Get all auth configs. */
  async get_all_api_auth_configs(init?: OperationInit<"get_all_api_auth_configs">): Promise<OperationData<"get_all_api_auth_configs">> {
    return this.client.requestOperation("get_all_api_auth_configs", "get", "/api_auth_configs/all", init);
  }

  /** Get auth configs. */
  async get_api_auth_configs(init?: OperationInit<"get_api_auth_configs">): Promise<OperationData<"get_api_auth_configs">> {
    return this.client.requestOperation("get_api_auth_configs", "get", "/api_auth_configs", init);
  }

  /** Get auth settings for org. */
  async get_api_auth_settings(init?: OperationInit<"get_api_auth_settings">): Promise<OperationData<"get_api_auth_settings">> {
    return this.client.requestOperation("get_api_auth_settings", "get", "/orgs/{org_id}/auth_settings", init);
  }

  /** Update auth config. */
  async update_api_auth_config(init?: OperationInit<"update_api_auth_config">): Promise<OperationData<"update_api_auth_config">> {
    return this.client.requestOperation("update_api_auth_config", "put", "/api_auth_configs/{auth_config_id}", init);
  }
}