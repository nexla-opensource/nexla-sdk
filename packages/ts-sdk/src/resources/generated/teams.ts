import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class TeamsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_teams">): Promise<OperationData<"get_teams">> {
    return this.client.requestOperation("get_teams", "get", "/teams", init);
  }

  async create(init?: OperationInit<"create_team">): Promise<OperationData<"create_team">> {
    return this.client.requestOperation("create_team", "post", "/teams", init);
  }

  async get(init?: OperationInit<"get_team">): Promise<OperationData<"get_team">> {
    return this.client.requestOperation("get_team", "get", "/teams/{team_id}", init);
  }

  async update(init?: OperationInit<"update_team">): Promise<OperationData<"update_team">> {
    return this.client.requestOperation("update_team", "put", "/teams/{team_id}", init);
  }

  async delete(init?: OperationInit<"delete_team">): Promise<OperationData<"delete_team">> {
    return this.client.requestOperation("delete_team", "delete", "/teams/{team_id}", init);
  }

  /** Add Members to A Team */
  async add_team_members(init?: OperationInit<"add_team_members">): Promise<OperationData<"add_team_members">> {
    return this.client.requestOperation("add_team_members", "put", "/teams/{team_id}/members", init);
  }

  /** Create a team */
  async create_team(init?: OperationInit<"create_team">): Promise<OperationData<"create_team">> {
    return this.client.requestOperation("create_team", "post", "/teams", init);
  }

  /** Delete Team by ID */
  async delete_team(init?: OperationInit<"delete_team">): Promise<OperationData<"delete_team">> {
    return this.client.requestOperation("delete_team", "delete", "/teams/{team_id}", init);
  }

  /** Remove Team Members */
  async delete_team_members(init?: OperationInit<"delete_team_members">): Promise<OperationData<"delete_team_members">> {
    return this.client.requestOperation("delete_team_members", "delete", "/teams/{team_id}/members", init);
  }

  /** Get Team by ID */
  async get_team(init?: OperationInit<"get_team">): Promise<OperationData<"get_team">> {
    return this.client.requestOperation("get_team", "get", "/teams/{team_id}", init);
  }

  /** Get Team Members */
  async get_team_members(init?: OperationInit<"get_team_members">): Promise<OperationData<"get_team_members">> {
    return this.client.requestOperation("get_team_members", "get", "/teams/{team_id}/members", init);
  }

  /** Get all Teams */
  async get_teams(init?: OperationInit<"get_teams">): Promise<OperationData<"get_teams">> {
    return this.client.requestOperation("get_teams", "get", "/teams", init);
  }

  /** Replace Team Members List */
  async replace_team_members(init?: OperationInit<"replace_team_members">): Promise<OperationData<"replace_team_members">> {
    return this.client.requestOperation("replace_team_members", "post", "/teams/{team_id}/members", init);
  }

  /** Modify a Team */
  async update_team(init?: OperationInit<"update_team">): Promise<OperationData<"update_team">> {
    return this.client.requestOperation("update_team", "put", "/teams/{team_id}", init);
  }
}