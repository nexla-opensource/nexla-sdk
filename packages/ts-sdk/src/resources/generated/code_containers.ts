import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class CodeContainersResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_code_containers">): Promise<OperationData<"get_code_containers">> {
    return this.client.requestOperation("get_code_containers", "get", "/code_containers", init);
  }

  async create(init?: OperationInit<"create_code_container">): Promise<OperationData<"create_code_container">> {
    return this.client.requestOperation("create_code_container", "post", "/code_containers", init);
  }

  async get(init?: OperationInit<"get_code_container">): Promise<OperationData<"get_code_container">> {
    return this.client.requestOperation("get_code_container", "get", "/code_containers/{code_container_id}", init);
  }

  async update(init?: OperationInit<"update_code_container">): Promise<OperationData<"update_code_container">> {
    return this.client.requestOperation("update_code_container", "put", "/code_containers/{code_container_id}", init);
  }

  async delete(init?: OperationInit<"delete_code_container">): Promise<OperationData<"delete_code_container">> {
    return this.client.requestOperation("delete_code_container", "delete", "/code_containers/{code_container_id}", init);
  }

  /** Copy a Code Container */
  async copy_code_container(init?: OperationInit<"copy_code_container">): Promise<OperationData<"copy_code_container">> {
    return this.client.requestOperation("copy_code_container", "post", "/code_containers/{code_container_id}/copy", init);
  }

  /** Create a Code Container */
  async create_code_container(init?: OperationInit<"create_code_container">): Promise<OperationData<"create_code_container">> {
    return this.client.requestOperation("create_code_container", "post", "/code_containers", init);
  }

  /** Delete a Code Container */
  async delete_code_container(init?: OperationInit<"delete_code_container">): Promise<OperationData<"delete_code_container">> {
    return this.client.requestOperation("delete_code_container", "delete", "/code_containers/{code_container_id}", init);
  }

  /** Get Code Container by ID */
  async get_code_container(init?: OperationInit<"get_code_container">): Promise<OperationData<"get_code_container">> {
    return this.client.requestOperation("get_code_container", "get", "/code_containers/{code_container_id}", init);
  }

  /** Get all Code Containers */
  async get_code_containers(init?: OperationInit<"get_code_containers">): Promise<OperationData<"get_code_containers">> {
    return this.client.requestOperation("get_code_containers", "get", "/code_containers", init);
  }

  /** Get all Public Code Containers */
  async get_public_code_containers(init?: OperationInit<"get_public_code_containers">): Promise<OperationData<"get_public_code_containers">> {
    return this.client.requestOperation("get_public_code_containers", "get", "/code_containers/public", init);
  }

  /** Update a Code Container */
  async update_code_container(init?: OperationInit<"update_code_container">): Promise<OperationData<"update_code_container">> {
    return this.client.requestOperation("update_code_container", "put", "/code_containers/{code_container_id}", init);
  }
}