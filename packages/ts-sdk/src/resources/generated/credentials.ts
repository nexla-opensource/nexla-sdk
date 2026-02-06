import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class CredentialsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_data_credentials">): Promise<OperationData<"get_data_credentials">> {
    return this.client.requestOperation("get_data_credentials", "get", "/data_credentials", init);
  }

  async create(init?: OperationInit<"create_data_credential">): Promise<OperationData<"create_data_credential">> {
    return this.client.requestOperation("create_data_credential", "post", "/data_credentials", init);
  }

  async get(init?: OperationInit<"get_data_credential">): Promise<OperationData<"get_data_credential">> {
    return this.client.requestOperation("get_data_credential", "get", "/data_credentials/{credential_id}", init);
  }

  async update(init?: OperationInit<"update_data_credential">): Promise<OperationData<"update_data_credential">> {
    return this.client.requestOperation("update_data_credential", "put", "/data_credentials/{credential_id}", init);
  }

  async delete(init?: OperationInit<"delete_data_credential">): Promise<OperationData<"delete_data_credential">> {
    return this.client.requestOperation("delete_data_credential", "delete", "/data_credentials/{credential_id}", init);
  }

  /** Create a Credential */
  async create_data_credential(init?: OperationInit<"create_data_credential">): Promise<OperationData<"create_data_credential">> {
    return this.client.requestOperation("create_data_credential", "post", "/data_credentials", init);
  }

  /** Test credential validity */
  async data_credential_probe(init?: OperationInit<"data_credential_probe">): Promise<OperationData<"data_credential_probe">> {
    return this.client.requestOperation("data_credential_probe", "get", "/data_credentials/{credential_id}/probe", init);
  }

  /** Delete a Credential */
  async delete_data_credential(init?: OperationInit<"delete_data_credential">): Promise<OperationData<"delete_data_credential">> {
    return this.client.requestOperation("delete_data_credential", "delete", "/data_credentials/{credential_id}", init);
  }

  /** Get Credential by ID */
  async get_data_credential(init?: OperationInit<"get_data_credential">): Promise<OperationData<"get_data_credential">> {
    return this.client.requestOperation("get_data_credential", "get", "/data_credentials/{credential_id}", init);
  }

  /** Get Credential by ID with expanded references */
  async get_data_credential_expanded(init?: OperationInit<"get_data_credential_expanded">): Promise<OperationData<"get_data_credential_expanded">> {
    return this.client.requestOperation("get_data_credential_expanded", "get", "/data_credentials/{credential_id}?expand=1", init);
  }

  /** Get All Credentials */
  async get_data_credentials(init?: OperationInit<"get_data_credentials">): Promise<OperationData<"get_data_credentials">> {
    return this.client.requestOperation("get_data_credentials", "get", "/data_credentials", init);
  }

  /** Preview Connector Content */
  async preview_connector_content(init?: OperationInit<"preview_connector_content">): Promise<OperationData<"preview_connector_content">> {
    return this.client.requestOperation("preview_connector_content", "post", "/data_credentials/{credential_id}/probe/sample", init);
  }

  /** Preview Storage Structure */
  async preview_storage_structure(init?: OperationInit<"preview_storage_structure">): Promise<OperationData<"preview_storage_structure">> {
    return this.client.requestOperation("preview_storage_structure", "post", "/data_credentials/{credential_id}/probe/tree", init);
  }

  /** Update Credential */
  async update_data_credential(init?: OperationInit<"update_data_credential">): Promise<OperationData<"update_data_credential">> {
    return this.client.requestOperation("update_data_credential", "put", "/data_credentials/{credential_id}", init);
  }
}