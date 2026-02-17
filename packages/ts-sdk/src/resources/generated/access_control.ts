import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class AccessControlResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  /** Add Access Rules on Code Container */
  async add_code_container_accessors(init?: OperationInit<"add_code_container_accessors">): Promise<OperationData<"add_code_container_accessors">> {
    return this.client.requestOperation("add_code_container_accessors", "put", "/code_containers/{code_container_id}/accessors", init);
  }

  /** Add Access Rules on Data Credential */
  async add_data_credential_accessors(init?: OperationInit<"add_data_credential_accessors">): Promise<OperationData<"add_data_credential_accessors">> {
    return this.client.requestOperation("add_data_credential_accessors", "put", "/data_credentials/{data_credential_id}/accessors", init);
  }

  /** Add Access Rules on Data Map */
  async add_data_map_accessors(init?: OperationInit<"add_data_map_accessors">): Promise<OperationData<"add_data_map_accessors">> {
    return this.client.requestOperation("add_data_map_accessors", "put", "/data_maps/{data_map_id}/accessors", init);
  }

  /** Add Access Rules on Data Schema */
  async add_data_schema_accessors(init?: OperationInit<"add_data_schema_accessors">): Promise<OperationData<"add_data_schema_accessors">> {
    return this.client.requestOperation("add_data_schema_accessors", "put", "/data_schemas/{data_schema_id}/accessors", init);
  }

  /** Add Access Rules on Data Sink */
  async add_data_sink_accessors(init?: OperationInit<"add_data_sink_accessors">): Promise<OperationData<"add_data_sink_accessors">> {
    return this.client.requestOperation("add_data_sink_accessors", "put", "/data_sinks/{data_sink_id}/accessors", init);
  }

  /** Add Access Rules on Data Source */
  async add_data_source_accessors(init?: OperationInit<"add_data_source_accessors">): Promise<OperationData<"add_data_source_accessors">> {
    return this.client.requestOperation("add_data_source_accessors", "put", "/data_sources/{data_source_id}/accessors", init);
  }

  /** Add Access Rules on Document */
  async add_doc_container_accessors(init?: OperationInit<"add_doc_container_accessors">): Promise<OperationData<"add_doc_container_accessors">> {
    return this.client.requestOperation("add_doc_container_accessors", "put", "/doc_containers/{doc_container_id}/accessors", init);
  }

  /** Add Access Rules on Flow */
  async add_flow_accessors(init?: OperationInit<"add_flow_accessors">): Promise<OperationData<"add_flow_accessors">> {
    return this.client.requestOperation("add_flow_accessors", "put", "/flows/{flow_id}/accessors", init);
  }

  /** Add Access Rules on Flow (Deprecated) */
  async ["add_flow_accessors_(deprecated)"](init?: OperationInit<"add_flow_accessors_(deprecated)">): Promise<OperationData<"add_flow_accessors_(deprecated)">> {
    return this.client.requestOperation("add_flow_accessors_(deprecated)", "put", "/data_flows/{data_flow_id}/accessors", init);
  }

  /** Add Access Rules on Nexset */
  async add_nexset_accessors(init?: OperationInit<"add_nexset_accessors">): Promise<OperationData<"add_nexset_accessors">> {
    return this.client.requestOperation("add_nexset_accessors", "put", "/data_sets/{data_set_id}/accessors", init);
  }

  /** Add Project Accessors */
  async add_project_accessors(init?: OperationInit<"add_project_accessors">): Promise<OperationData<"add_project_accessors">> {
    return this.client.requestOperation("add_project_accessors", "put", "/projects/{project_id}/accessors", init);
  }

  /** Add Team Accessors */
  async add_team_accessors(init?: OperationInit<"add_team_accessors">): Promise<OperationData<"add_team_accessors">> {
    return this.client.requestOperation("add_team_accessors", "put", "/teams/{team_id}/accessors", init);
  }

  /** Delete Access Rules on Code Container */
  async delete_code_container_accessors(init?: OperationInit<"delete_code_container_accessors">): Promise<OperationData<"delete_code_container_accessors">> {
    return this.client.requestOperation("delete_code_container_accessors", "delete", "/code_containers/{code_container_id}/accessors", init);
  }

  /** Delete Access Rules on Data Credential */
  async delete_data_credential_accessors(init?: OperationInit<"delete_data_credential_accessors">): Promise<OperationData<"delete_data_credential_accessors">> {
    return this.client.requestOperation("delete_data_credential_accessors", "delete", "/data_credentials/{data_credential_id}/accessors", init);
  }

  /** Delete Access Rules on Data Map */
  async delete_data_map_accessors(init?: OperationInit<"delete_data_map_accessors">): Promise<OperationData<"delete_data_map_accessors">> {
    return this.client.requestOperation("delete_data_map_accessors", "delete", "/data_maps/{data_map_id}/accessors", init);
  }

  /** Delete Access Rules on Data Schema */
  async delete_data_schema_accessors(init?: OperationInit<"delete_data_schema_accessors">): Promise<OperationData<"delete_data_schema_accessors">> {
    return this.client.requestOperation("delete_data_schema_accessors", "delete", "/data_schemas/{data_schema_id}/accessors", init);
  }

  /** Delete Access Rules on Data Sink */
  async delete_data_sink_accessors(init?: OperationInit<"delete_data_sink_accessors">): Promise<OperationData<"delete_data_sink_accessors">> {
    return this.client.requestOperation("delete_data_sink_accessors", "delete", "/data_sinks/{data_sink_id}/accessors", init);
  }

  /** Delete Access Rules on Data Source */
  async delete_data_source_accessors(init?: OperationInit<"delete_data_source_accessors">): Promise<OperationData<"delete_data_source_accessors">> {
    return this.client.requestOperation("delete_data_source_accessors", "delete", "/data_sources/{data_source_id}/accessors", init);
  }

  /** Delete Access Rules on Document */
  async delete_doc_container_accessors(init?: OperationInit<"delete_doc_container_accessors">): Promise<OperationData<"delete_doc_container_accessors">> {
    return this.client.requestOperation("delete_doc_container_accessors", "delete", "/doc_containers/{doc_container_id}/accessors", init);
  }

  /** Delete Access Rules on Flow */
  async delete_flow_accessors(init?: OperationInit<"delete_flow_accessors">): Promise<OperationData<"delete_flow_accessors">> {
    return this.client.requestOperation("delete_flow_accessors", "delete", "/flows/{flow_id}/accessors", init);
  }

  /** Delete Access Rules on Flow (Deprecated) */
  async ["delete_flow_accessors_(deprecated)"](init?: OperationInit<"delete_flow_accessors_(deprecated)">): Promise<OperationData<"delete_flow_accessors_(deprecated)">> {
    return this.client.requestOperation("delete_flow_accessors_(deprecated)", "delete", "/data_flows/{data_flow_id}/accessors", init);
  }

  /** Delete Access Rules on Nexset */
  async delete_nexset_accessors(init?: OperationInit<"delete_nexset_accessors">): Promise<OperationData<"delete_nexset_accessors">> {
    return this.client.requestOperation("delete_nexset_accessors", "delete", "/data_sets/{data_set_id}/accessors", init);
  }

  /** Delete Project Accessors */
  async delete_project_accessors(init?: OperationInit<"delete_project_accessors">): Promise<OperationData<"delete_project_accessors">> {
    return this.client.requestOperation("delete_project_accessors", "delete", "/projects/{project_id}/accessors", init);
  }

  /** Delete Team Accessors */
  async delete_team_accessors(init?: OperationInit<"delete_team_accessors">): Promise<OperationData<"delete_team_accessors">> {
    return this.client.requestOperation("delete_team_accessors", "delete", "/teams/{team_id}/accessors", init);
  }

  /** Get Access Rules on Code Container */
  async get_code_container_accessors(init?: OperationInit<"get_code_container_accessors">): Promise<OperationData<"get_code_container_accessors">> {
    return this.client.requestOperation("get_code_container_accessors", "get", "/code_containers/{code_container_id}/accessors", init);
  }

  /** Get Access Rules on Data Credential */
  async get_data_credential_accessors(init?: OperationInit<"get_data_credential_accessors">): Promise<OperationData<"get_data_credential_accessors">> {
    return this.client.requestOperation("get_data_credential_accessors", "get", "/data_credentials/{data_credential_id}/accessors", init);
  }

  /** Get Access Rules on Data Map */
  async get_data_map_accessors(init?: OperationInit<"get_data_map_accessors">): Promise<OperationData<"get_data_map_accessors">> {
    return this.client.requestOperation("get_data_map_accessors", "get", "/data_maps/{data_map_id}/accessors", init);
  }

  /** Get Access Rules on Data Schema */
  async get_data_schema_accessors(init?: OperationInit<"get_data_schema_accessors">): Promise<OperationData<"get_data_schema_accessors">> {
    return this.client.requestOperation("get_data_schema_accessors", "get", "/data_schemas/{data_schema_id}/accessors", init);
  }

  /** Get Access Rules on Data Sink */
  async get_data_sink_accessors(init?: OperationInit<"get_data_sink_accessors">): Promise<OperationData<"get_data_sink_accessors">> {
    return this.client.requestOperation("get_data_sink_accessors", "get", "/data_sinks/{data_sink_id}/accessors", init);
  }

  /** Get Access Rules on Data Source */
  async get_data_source_accessors(init?: OperationInit<"get_data_source_accessors">): Promise<OperationData<"get_data_source_accessors">> {
    return this.client.requestOperation("get_data_source_accessors", "get", "/data_sources/{data_source_id}/accessors", init);
  }

  /** Get Access Rules on Document */
  async get_doc_container_accessors(init?: OperationInit<"get_doc_container_accessors">): Promise<OperationData<"get_doc_container_accessors">> {
    return this.client.requestOperation("get_doc_container_accessors", "get", "/doc_containers/{doc_container_id}/accessors", init);
  }

  /** Get Access Rules on Flow */
  async get_flow_accessors(init?: OperationInit<"get_flow_accessors">): Promise<OperationData<"get_flow_accessors">> {
    return this.client.requestOperation("get_flow_accessors", "get", "/flows/{flow_id}/accessors", init);
  }

  /** Get Access Rules on Flow (Deprecated) */
  async ["get_flow_accessors_(deprecated)"](init?: OperationInit<"get_flow_accessors_(deprecated)">): Promise<OperationData<"get_flow_accessors_(deprecated)">> {
    return this.client.requestOperation("get_flow_accessors_(deprecated)", "get", "/data_flows/{data_flow_id}/accessors", init);
  }

  /** Get Access Rules on Nexset */
  async get_nexset_accessors(init?: OperationInit<"get_nexset_accessors">): Promise<OperationData<"get_nexset_accessors">> {
    return this.client.requestOperation("get_nexset_accessors", "get", "/data_sets/{data_set_id}/accessors", init);
  }

  /** Get Project Accessors */
  async get_project_accessors(init?: OperationInit<"get_project_accessors">): Promise<OperationData<"get_project_accessors">> {
    return this.client.requestOperation("get_project_accessors", "get", "/projects/{project_id}/accessors", init);
  }

  /** Get Team Accessors */
  async get_team_accessors(init?: OperationInit<"get_team_accessors">): Promise<OperationData<"get_team_accessors">> {
    return this.client.requestOperation("get_team_accessors", "get", "/teams/{team_id}/accessors", init);
  }

  /** Replace Access Rules on Code Container */
  async replace_code_container_accessors(init?: OperationInit<"replace_code_container_accessors">): Promise<OperationData<"replace_code_container_accessors">> {
    return this.client.requestOperation("replace_code_container_accessors", "post", "/code_containers/{code_container_id}/accessors", init);
  }

  /** Replace Access Rules on Data Credential */
  async replace_data_credential_accessors(init?: OperationInit<"replace_data_credential_accessors">): Promise<OperationData<"replace_data_credential_accessors">> {
    return this.client.requestOperation("replace_data_credential_accessors", "post", "/data_credentials/{data_credential_id}/accessors", init);
  }

  /** Replace Access Rules on Data Map */
  async replace_data_map_accessors(init?: OperationInit<"replace_data_map_accessors">): Promise<OperationData<"replace_data_map_accessors">> {
    return this.client.requestOperation("replace_data_map_accessors", "post", "/data_maps/{data_map_id}/accessors", init);
  }

  /** Replace Access Rules on Data Schema */
  async replace_data_schema_accessors(init?: OperationInit<"replace_data_schema_accessors">): Promise<OperationData<"replace_data_schema_accessors">> {
    return this.client.requestOperation("replace_data_schema_accessors", "post", "/data_schemas/{data_schema_id}/accessors", init);
  }

  /** Replace Access Rules on Data Sink */
  async replace_data_sink_accessors(init?: OperationInit<"replace_data_sink_accessors">): Promise<OperationData<"replace_data_sink_accessors">> {
    return this.client.requestOperation("replace_data_sink_accessors", "post", "/data_sinks/{data_sink_id}/accessors", init);
  }

  /** Replace Access Rules on Data Source */
  async replace_data_source_accessors(init?: OperationInit<"replace_data_source_accessors">): Promise<OperationData<"replace_data_source_accessors">> {
    return this.client.requestOperation("replace_data_source_accessors", "post", "/data_sources/{data_source_id}/accessors", init);
  }

  /** Replace Access Rules on Document */
  async replace_doc_container_accessors(init?: OperationInit<"replace_doc_container_accessors">): Promise<OperationData<"replace_doc_container_accessors">> {
    return this.client.requestOperation("replace_doc_container_accessors", "post", "/doc_containers/{doc_container_id}/accessors", init);
  }

  /** Replace Access Rules on Flow */
  async replace_flow_accessors(init?: OperationInit<"replace_flow_accessors">): Promise<OperationData<"replace_flow_accessors">> {
    return this.client.requestOperation("replace_flow_accessors", "post", "/flows/{flow_id}/accessors", init);
  }

  /** Replace Access Rules on Flow (Deprecated) */
  async ["replace_flow_accessors_(deprecated)"](init?: OperationInit<"replace_flow_accessors_(deprecated)">): Promise<OperationData<"replace_flow_accessors_(deprecated)">> {
    return this.client.requestOperation("replace_flow_accessors_(deprecated)", "post", "/data_flows/{data_flow_id}/accessors", init);
  }

  /** Replace Access Rules on Nexset */
  async replace_nexset_accessors(init?: OperationInit<"replace_nexset_accessors">): Promise<OperationData<"replace_nexset_accessors">> {
    return this.client.requestOperation("replace_nexset_accessors", "post", "/data_sets/{data_set_id}/accessors", init);
  }

  /** Replace Access Rules on Project */
  async replace_project_accessors(init?: OperationInit<"replace_project_accessors">): Promise<OperationData<"replace_project_accessors">> {
    return this.client.requestOperation("replace_project_accessors", "post", "/projects/{project_id}/accessors", init);
  }

  /** Replace Team Accessors List */
  async replace_team_accessors(init?: OperationInit<"replace_team_accessors">): Promise<OperationData<"replace_team_accessors">> {
    return this.client.requestOperation("replace_team_accessors", "post", "/teams/{team_id}/accessors", init);
  }
}