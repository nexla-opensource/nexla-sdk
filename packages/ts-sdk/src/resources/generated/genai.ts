import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class GenaiResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  /** Create a GenAI config */
  async create_gen_ai_config(init?: OperationInit<"create_gen_ai_config">): Promise<OperationData<"create_gen_ai_config">> {
    return this.client.requestOperation("create_gen_ai_config", "post", "/gen_ai_integration_configs", init);
  }

  /** Create a binding of GenAI config for the org for specific usage. */
  async create_gen_ai_org_setting(init?: OperationInit<"create_gen_ai_org_setting">): Promise<OperationData<"create_gen_ai_org_setting">> {
    return this.client.requestOperation("create_gen_ai_org_setting", "post", "/gen_ai_org_settings", init);
  }

  /** Delete GenAI Integration Config */
  async delete_gen_ai_integration_config(init?: OperationInit<"delete_gen_ai_integration_config">): Promise<OperationData<"delete_gen_ai_integration_config">> {
    return this.client.requestOperation("delete_gen_ai_integration_config", "delete", "/gen_ai_integration_configs/{gen_ai_config_id}", init);
  }

  /** Delete GenAI Config binding for org. */
  async delete_gen_ai_org_setting(init?: OperationInit<"delete_gen_ai_org_setting">): Promise<OperationData<"delete_gen_ai_org_setting">> {
    return this.client.requestOperation("delete_gen_ai_org_setting", "delete", "/gen_ai_org_settings/{gen_ai_org_setting_id}", init);
  }

  /** Shows active GenAI Configuration for specific usage */
  async gen_ai_org_settings_show_active(init?: OperationInit<"gen_ai_org_settings_show_active">): Promise<OperationData<"gen_ai_org_settings_show_active">> {
    return this.client.requestOperation("gen_ai_org_settings_show_active", "get", "/gen_ai_org_settings/active_config", init);
  }

  /** Get all GenAI configs in org */
  async get_gen_ai_configs(init?: OperationInit<"get_gen_ai_configs">): Promise<OperationData<"get_gen_ai_configs">> {
    return this.client.requestOperation("get_gen_ai_configs", "get", "/gen_ai_integration_configs", init);
  }

  /** Get GenAI Integration Config */
  async get_gen_ai_integration_config(init?: OperationInit<"get_gen_ai_integration_config">): Promise<OperationData<"get_gen_ai_integration_config">> {
    return this.client.requestOperation("get_gen_ai_integration_config", "get", "/gen_ai_integration_configs/{gen_ai_config_id}", init);
  }

  /** Get Org GenAI binding */
  async get_gen_ai_org_setting(init?: OperationInit<"get_gen_ai_org_setting">): Promise<OperationData<"get_gen_ai_org_setting">> {
    return this.client.requestOperation("get_gen_ai_org_setting", "get", "/gen_ai_org_settings/{gen_ai_org_setting_id}", init);
  }

  /** Get all bindings of GenAI configs of the org for specified usages. */
  async get_gen_ai_org_settings(init?: OperationInit<"get_gen_ai_org_settings">): Promise<OperationData<"get_gen_ai_org_settings">> {
    return this.client.requestOperation("get_gen_ai_org_settings", "get", "/gen_ai_org_settings", init);
  }

  /** Update GenAI Integration Config */
  async update_gen_ai_integration_config(init?: OperationInit<"update_gen_ai_integration_config">): Promise<OperationData<"update_gen_ai_integration_config">> {
    return this.client.requestOperation("update_gen_ai_integration_config", "put", "/gen_ai_integration_configs/{gen_ai_config_id}", init);
  }
}