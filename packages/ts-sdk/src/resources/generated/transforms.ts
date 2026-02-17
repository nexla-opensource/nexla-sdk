import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class TransformsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_reusable_record_transforms">): Promise<OperationData<"get_reusable_record_transforms">> {
    return this.client.requestOperation("get_reusable_record_transforms", "get", "/transforms", init);
  }

  async create(init?: OperationInit<"create_reusable_record_transform">): Promise<OperationData<"create_reusable_record_transform">> {
    return this.client.requestOperation("create_reusable_record_transform", "post", "/transforms", init);
  }

  async get(init?: OperationInit<"get_reusable_record_transform">): Promise<OperationData<"get_reusable_record_transform">> {
    return this.client.requestOperation("get_reusable_record_transform", "get", "/transforms/{transform_id}", init);
  }

  async update(init?: OperationInit<"update_reusable_record_transform">): Promise<OperationData<"update_reusable_record_transform">> {
    return this.client.requestOperation("update_reusable_record_transform", "put", "/transforms/{transform_id}", init);
  }

  async delete(init?: OperationInit<"delete_reusable_record_transform">): Promise<OperationData<"delete_reusable_record_transform">> {
    return this.client.requestOperation("delete_reusable_record_transform", "delete", "/transforms/{transform_id}", init);
  }

  /** Copy a Reusable Record Transform */
  async copy_transform(init?: OperationInit<"copy_transform">): Promise<OperationData<"copy_transform">> {
    return this.client.requestOperation("copy_transform", "post", "/transforms/{transform_id}/copy", init);
  }

  /** Create an Attribute Transform */
  async create_attribute_transform(init?: OperationInit<"create_attribute_transform">): Promise<OperationData<"create_attribute_transform">> {
    return this.client.requestOperation("create_attribute_transform", "post", "/attribute_transforms", init);
  }

  /** Create a Reusable Record Transform */
  async create_reusable_record_transform(init?: OperationInit<"create_reusable_record_transform">): Promise<OperationData<"create_reusable_record_transform">> {
    return this.client.requestOperation("create_reusable_record_transform", "post", "/transforms", init);
  }

  /** Delete an Attribute Transform */
  async delete_attribute_transform(init?: OperationInit<"delete_attribute_transform">): Promise<OperationData<"delete_attribute_transform">> {
    return this.client.requestOperation("delete_attribute_transform", "delete", "/attribute_transforms/{attribute_transform_id}", init);
  }

  /** Delete a Reusable Record Transform */
  async delete_reusable_record_transform(init?: OperationInit<"delete_reusable_record_transform">): Promise<OperationData<"delete_reusable_record_transform">> {
    return this.client.requestOperation("delete_reusable_record_transform", "delete", "/transforms/{transform_id}", init);
  }

  /** Get Attribute Transform by ID */
  async get_attribute_transform(init?: OperationInit<"get_attribute_transform">): Promise<OperationData<"get_attribute_transform">> {
    return this.client.requestOperation("get_attribute_transform", "get", "/attribute_transforms/{attribute_transform_id}", init);
  }

  /** Get all Attribute Transforms */
  async get_attribute_transforms(init?: OperationInit<"get_attribute_transforms">): Promise<OperationData<"get_attribute_transforms">> {
    return this.client.requestOperation("get_attribute_transforms", "get", "/attribute_transforms", init);
  }

  /** Get all Public Attribute Transforms */
  async get_public_attribute_transforms(init?: OperationInit<"get_public_attribute_transforms">): Promise<OperationData<"get_public_attribute_transforms">> {
    return this.client.requestOperation("get_public_attribute_transforms", "get", "/attribute_transforms/public", init);
  }

  /** Get all Public Reusable Record Transforms */
  async get_public_reusable_record_transforms(init?: OperationInit<"get_public_reusable_record_transforms">): Promise<OperationData<"get_public_reusable_record_transforms">> {
    return this.client.requestOperation("get_public_reusable_record_transforms", "get", "/transforms/public", init);
  }

  /** Get A Reusable Record Transform */
  async get_reusable_record_transform(init?: OperationInit<"get_reusable_record_transform">): Promise<OperationData<"get_reusable_record_transform">> {
    return this.client.requestOperation("get_reusable_record_transform", "get", "/transforms/{transform_id}", init);
  }

  /** Get all Reusable Record Transforms */
  async get_reusable_record_transforms(init?: OperationInit<"get_reusable_record_transforms">): Promise<OperationData<"get_reusable_record_transforms">> {
    return this.client.requestOperation("get_reusable_record_transforms", "get", "/transforms", init);
  }

  /** Update Attribute Transform */
  async update_attribute_transform(init?: OperationInit<"update_attribute_transform">): Promise<OperationData<"update_attribute_transform">> {
    return this.client.requestOperation("update_attribute_transform", "put", "/attribute_transforms/{attribute_transform_id}", init);
  }

  /** Update Reusable Record Transform */
  async update_reusable_record_transform(init?: OperationInit<"update_reusable_record_transform">): Promise<OperationData<"update_reusable_record_transform">> {
    return this.client.requestOperation("update_reusable_record_transform", "put", "/transforms/{transform_id}", init);
  }
}