import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class AuditLogsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  /** Get Audit Log for a Code Container */
  async get_code_container_audit_log(init?: OperationInit<"get_code_container_audit_log">): Promise<OperationData<"get_code_container_audit_log">> {
    return this.client.requestOperation("get_code_container_audit_log", "get", "/code_containers/{code_container_id}/audit_log", init);
  }

  /** Get Audit Log for a Data Credential */
  async get_data_credential_audit_log(init?: OperationInit<"get_data_credential_audit_log">): Promise<OperationData<"get_data_credential_audit_log">> {
    return this.client.requestOperation("get_data_credential_audit_log", "get", "/data_credentials/{credential_id}/audit_log", init);
  }

  /** Get Audit Log for a Data Map */
  async get_data_map_audit_log(init?: OperationInit<"get_data_map_audit_log">): Promise<OperationData<"get_data_map_audit_log">> {
    return this.client.requestOperation("get_data_map_audit_log", "get", "/data_maps/{data_map_id}/audit_log", init);
  }

  /** Get Audit Log for a Data Schema */
  async get_data_schema_audit_log(init?: OperationInit<"get_data_schema_audit_log">): Promise<OperationData<"get_data_schema_audit_log">> {
    return this.client.requestOperation("get_data_schema_audit_log", "get", "/data_schemas/{schema_id}/audit_log", init);
  }

  /** Get Audit Log for a Data Sink */
  async get_data_sink_audit_log(init?: OperationInit<"get_data_sink_audit_log">): Promise<OperationData<"get_data_sink_audit_log">> {
    return this.client.requestOperation("get_data_sink_audit_log", "get", "/data_sinks/{sink_id}/audit_log", init);
  }

  /** Get Audit Log for a Data Source */
  async get_data_source_audit_log(init?: OperationInit<"get_data_source_audit_log">): Promise<OperationData<"get_data_source_audit_log">> {
    return this.client.requestOperation("get_data_source_audit_log", "get", "/data_sources/{source_id}/audit_log", init);
  }

  /** Get Audit Log for a Document */
  async get_doc_container_audit_log(init?: OperationInit<"get_doc_container_audit_log">): Promise<OperationData<"get_doc_container_audit_log">> {
    return this.client.requestOperation("get_doc_container_audit_log", "get", "/doc_containers/{doc_container_id}/audit_log", init);
  }

  /** Get Audit Log for a Nexset */
  async get_nexset_audit_log(init?: OperationInit<"get_nexset_audit_log">): Promise<OperationData<"get_nexset_audit_log">> {
    return this.client.requestOperation("get_nexset_audit_log", "get", "/data_sets/{set_id}/audit_log", init);
  }

  /** Get Audit Log for an Organization */
  async get_org_audit_log(init?: OperationInit<"get_org_audit_log">): Promise<OperationData<"get_org_audit_log">> {
    return this.client.requestOperation("get_org_audit_log", "get", "/orgs/{org_id}/audit_log", init);
  }

  /** Get Audit Log for a Project */
  async get_project_audit_log(init?: OperationInit<"get_project_audit_log">): Promise<OperationData<"get_project_audit_log">> {
    return this.client.requestOperation("get_project_audit_log", "get", "/projects/{project_id}/audit_log", init);
  }

  /** Get Audit Log for a Team */
  async get_team_audit_log(init?: OperationInit<"get_team_audit_log">): Promise<OperationData<"get_team_audit_log">> {
    return this.client.requestOperation("get_team_audit_log", "get", "/teams/{team_id}/audit_log", init);
  }

  /** Get Audit Log for a User */
  async get_user_audit_log(init?: OperationInit<"get_user_audit_log">): Promise<OperationData<"get_user_audit_log">> {
    return this.client.requestOperation("get_user_audit_log", "get", "/users/{user_id}/audit_log", init);
  }
}