import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class ProjectsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_projects">): Promise<OperationData<"get_projects">> {
    return this.client.requestOperation("get_projects", "get", "/projects", init);
  }

  async create(init?: OperationInit<"create_project">): Promise<OperationData<"create_project">> {
    return this.client.requestOperation("create_project", "post", "/projects", init);
  }

  async get(init?: OperationInit<"get_project">): Promise<OperationData<"get_project">> {
    return this.client.requestOperation("get_project", "get", "/projects/{project_id}", init);
  }

  async update(init?: OperationInit<"update_project">): Promise<OperationData<"update_project">> {
    return this.client.requestOperation("update_project", "put", "/projects/{project_id}", init);
  }

  async delete(init?: OperationInit<"delete_project">): Promise<OperationData<"delete_project">> {
    return this.client.requestOperation("delete_project", "delete", "/projects/{project_id}", init);
  }

  /** Add Flows to Project */
  async add_project_flows(init?: OperationInit<"add_project_flows">): Promise<OperationData<"add_project_flows">> {
    return this.client.requestOperation("add_project_flows", "put", "/projects/{project_id}/flows", init);
  }

  /** Add Flows to Project (Deprecated) */
  async ["add_project_flows_(deprecated)"](init?: OperationInit<"add_project_flows_(deprecated)">): Promise<OperationData<"add_project_flows_(deprecated)">> {
    return this.client.requestOperation("add_project_flows_(deprecated)", "put", "/projects/{project_id}/data_flows", init);
  }

  /** Create a project */
  async create_project(init?: OperationInit<"create_project">): Promise<OperationData<"create_project">> {
    return this.client.requestOperation("create_project", "post", "/projects", init);
  }

  /** Delete Project by ID */
  async delete_project(init?: OperationInit<"delete_project">): Promise<OperationData<"delete_project">> {
    return this.client.requestOperation("delete_project", "delete", "/projects/{project_id}", init);
  }

  /** Get Project by ID */
  async get_project(init?: OperationInit<"get_project">): Promise<OperationData<"get_project">> {
    return this.client.requestOperation("get_project", "get", "/projects/{project_id}", init);
  }

  /** Get Project Flows */
  async get_project_flows(init?: OperationInit<"get_project_flows">): Promise<OperationData<"get_project_flows">> {
    return this.client.requestOperation("get_project_flows", "get", "/projects/{project_id}/flows", init);
  }

  /** Get Project Flows (Deprecated) */
  async ["get_project_flows_(deprecated)"](init?: OperationInit<"get_project_flows_(deprecated)">): Promise<OperationData<"get_project_flows_(deprecated)">> {
    return this.client.requestOperation("get_project_flows_(deprecated)", "get", "/projects/{project_id}/data_flows", init);
  }

  /** Get all Projects */
  async get_projects(init?: OperationInit<"get_projects">): Promise<OperationData<"get_projects">> {
    return this.client.requestOperation("get_projects", "get", "/projects", init);
  }

  /** Remove Flows From A Project */
  async remove_project_flows(init?: OperationInit<"remove_project_flows">): Promise<OperationData<"remove_project_flows">> {
    return this.client.requestOperation("remove_project_flows", "delete", "/projects/{project_id}/flows", init);
  }

  /** Remove Flows From A Project (Deprecated) */
  async ["remove_project_flows_(deprecated)"](init?: OperationInit<"remove_project_flows_(deprecated)">): Promise<OperationData<"remove_project_flows_(deprecated)">> {
    return this.client.requestOperation("remove_project_flows_(deprecated)", "delete", "/projects/{project_id}/data_flows", init);
  }

  /** Replace Project Flows List */
  async replace_project_flows(init?: OperationInit<"replace_project_flows">): Promise<OperationData<"replace_project_flows">> {
    return this.client.requestOperation("replace_project_flows", "post", "/projects/{project_id}/flows", init);
  }

  /** Replace Project Flows List (Deprecated) */
  async ["replace_project_flows_(deprecated)"](init?: OperationInit<"replace_project_flows_(deprecated)">): Promise<OperationData<"replace_project_flows_(deprecated)">> {
    return this.client.requestOperation("replace_project_flows_(deprecated)", "post", "/projects/{project_id}/data_flows", init);
  }

  /** Modify a Project */
  async update_project(init?: OperationInit<"update_project">): Promise<OperationData<"update_project">> {
    return this.client.requestOperation("update_project", "put", "/projects/{project_id}", init);
  }
}