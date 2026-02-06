import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class AsyncTasksResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  async list(init?: OperationInit<"get_async_tasks">): Promise<OperationData<"get_async_tasks">> {
    return this.client.requestOperation("get_async_tasks", "get", "/async_tasks", init);
  }

  async create(init?: OperationInit<"create_async_task">): Promise<OperationData<"create_async_task">> {
    return this.client.requestOperation("create_async_task", "post", "/async_tasks", init);
  }

  async get(init?: OperationInit<"get_async_task">): Promise<OperationData<"get_async_task">> {
    return this.client.requestOperation("get_async_task", "get", "/async_tasks/{task_id}", init);
  }

  async delete(init?: OperationInit<"delete_async_task">): Promise<OperationData<"delete_async_task">> {
    return this.client.requestOperation("delete_async_task", "delete", "/async_tasks/{task_id}", init);
  }

  /** Acknowledge async operation */
  async acknowledge_async_task(init?: OperationInit<"acknowledge_async_task">): Promise<OperationData<"acknowledge_async_task">> {
    return this.client.requestOperation("acknowledge_async_task", "post", "/async_tasks/{task_id}/acknowledge", init);
  }

  /** Create an async operation. */
  async create_async_task(init?: OperationInit<"create_async_task">): Promise<OperationData<"create_async_task">> {
    return this.client.requestOperation("create_async_task", "post", "/async_tasks", init);
  }

  /** Delete async operation by ID */
  async delete_async_task(init?: OperationInit<"delete_async_task">): Promise<OperationData<"delete_async_task">> {
    return this.client.requestOperation("delete_async_task", "delete", "/async_tasks/{task_id}", init);
  }

  /** Get async operation by ID */
  async get_async_task(init?: OperationInit<"get_async_task">): Promise<OperationData<"get_async_task">> {
    return this.client.requestOperation("get_async_task", "get", "/async_tasks/{task_id}", init);
  }

  /** Get download link for async operation result */
  async get_async_task_download_link(init?: OperationInit<"get_async_task_download_link">): Promise<OperationData<"get_async_task_download_link">> {
    return this.client.requestOperation("get_async_task_download_link", "get", "/async_tasks/{task_id}/download_link", init);
  }

  /** Get async operation result */
  async get_async_task_result(init?: OperationInit<"get_async_task_result">): Promise<OperationData<"get_async_task_result">> {
    return this.client.requestOperation("get_async_task_result", "get", "/async_tasks/{task_id}/result", init);
  }

  /** Get async operation types */
  async get_async_task_types(init?: OperationInit<"get_async_task_types">): Promise<OperationData<"get_async_task_types">> {
    return this.client.requestOperation("get_async_task_types", "get", "/async_tasks/types", init);
  }

  /** Get async operations list for current user. */
  async get_async_tasks(init?: OperationInit<"get_async_tasks">): Promise<OperationData<"get_async_tasks">> {
    return this.client.requestOperation("get_async_tasks", "get", "/async_tasks", init);
  }

  /** Get async operations list for current user by status */
  async get_async_tasks_by_status(init?: OperationInit<"get_async_tasks_by_status">): Promise<OperationData<"get_async_tasks_by_status">> {
    return this.client.requestOperation("get_async_tasks_by_status", "get", "/async_tasks/by_status/{status}", init);
  }

  /** Get async operation arguments for a specific type with descriptions */
  async get_async_tasks_explain_arguments(init?: OperationInit<"get_async_tasks_explain_arguments">): Promise<OperationData<"get_async_tasks_explain_arguments">> {
    return this.client.requestOperation("get_async_tasks_explain_arguments", "get", "/async_tasks/explain_arguments/{task_type}", init);
  }

  /** Get async operations list for current user of a specific type. */
  async get_async_tasks_of_type(init?: OperationInit<"get_async_tasks_of_type">): Promise<OperationData<"get_async_tasks_of_type">> {
    return this.client.requestOperation("get_async_tasks_of_type", "get", "/async_tasks/of_type/{task_type}", init);
  }

  /** Rerun async operation */
  async rerun_async_task(init?: OperationInit<"rerun_async_task">): Promise<OperationData<"rerun_async_task">> {
    return this.client.requestOperation("rerun_async_task", "post", "/async_tasks/{task_id}/rerun", init);
  }
}