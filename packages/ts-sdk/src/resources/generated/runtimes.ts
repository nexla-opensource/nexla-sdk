import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class RuntimesResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_runtimes">): Promise<OperationData<"get_runtimes">> {
    return this.client.requestOperation("get_runtimes", "get", "/runtimes", init);
  }

  async create(init?: OperationInit<"create_runtime">): Promise<OperationData<"create_runtime">> {
    return this.client.requestOperation("create_runtime", "post", "/runtimes", init);
  }

  async get(init?: OperationInit<"get_runtime">): Promise<OperationData<"get_runtime">> {
    return this.client.requestOperation("get_runtime", "get", "/runtimes/{runtime_id}", init);
  }

  async update(init?: OperationInit<"update_runtime">): Promise<OperationData<"update_runtime">> {
    return this.client.requestOperation("update_runtime", "put", "/runtimes/{runtime_id}", init);
  }

  async delete(init?: OperationInit<"delete_runtime">): Promise<OperationData<"delete_runtime">> {
    return this.client.requestOperation("delete_runtime", "delete", "/runtimes/{runtime_id}", init);
  }

  /** Activate a Custom Runtime */
  async activate_runtime(init?: OperationInit<"activate_runtime">): Promise<OperationData<"activate_runtime">> {
    return this.client.requestOperation("activate_runtime", "put", "/runtimes/{runtime_id}/activate", init);
  }

  /** Create a Custom Runtime */
  async create_runtime(init?: OperationInit<"create_runtime">): Promise<OperationData<"create_runtime">> {
    return this.client.requestOperation("create_runtime", "post", "/runtimes", init);
  }

  /** Delete a Custom Runtime */
  async delete_runtime(init?: OperationInit<"delete_runtime">): Promise<OperationData<"delete_runtime">> {
    return this.client.requestOperation("delete_runtime", "delete", "/runtimes/{runtime_id}", init);
  }

  /** Get a custom runtime by ID */
  async get_runtime(init?: OperationInit<"get_runtime">): Promise<OperationData<"get_runtime">> {
    return this.client.requestOperation("get_runtime", "get", "/runtimes/{runtime_id}", init);
  }

  /** Get all Custom Runtimes */
  async get_runtimes(init?: OperationInit<"get_runtimes">): Promise<OperationData<"get_runtimes">> {
    return this.client.requestOperation("get_runtimes", "get", "/runtimes", init);
  }

  /** Pause a Custom Runtime */
  async pause_runtime(init?: OperationInit<"pause_runtime">): Promise<OperationData<"pause_runtime">> {
    return this.client.requestOperation("pause_runtime", "put", "/runtimes/{runtime_id}/pause", init);
  }

  /** Update a Custom Runtime */
  async update_runtime(init?: OperationInit<"update_runtime">): Promise<OperationData<"update_runtime">> {
    return this.client.requestOperation("update_runtime", "put", "/runtimes/{runtime_id}", init);
  }
}