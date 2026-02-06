import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class MetricsResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  /** Get Flow Execution Logs for Run ID of a Flow */
  async get_flow_logs_for_run_id(init?: OperationInit<"get_flow_logs_for_run_id">): Promise<OperationData<"get_flow_logs_for_run_id">> {
    return this.client.requestOperation("get_flow_logs_for_run_id", "get", "/data_flows/{resource_type}/{resource_id}/logs", init);
  }

  /** Get Metrics for a Flow */
  async get_flow_metrics(init?: OperationInit<"get_flow_metrics">): Promise<OperationData<"get_flow_metrics">> {
    return this.client.requestOperation("get_flow_metrics", "get", "/data_flows/{resource_type}/{resource_id}/metrics", init);
  }

  /** Get Metrics By Run ID for a Resource of a Flow */
  async get_resource_metrics_by_run(init?: OperationInit<"get_resource_metrics_by_run">): Promise<OperationData<"get_resource_metrics_by_run">> {
    return this.client.requestOperation("get_resource_metrics_by_run", "get", "/{resource_type}/{resource_id}/metrics/run_summary", init);
  }

  /** Get Daily Metrics for a Resource of a Flow */
  async get_resource_metrics_daily(init?: OperationInit<"get_resource_metrics_daily">): Promise<OperationData<"get_resource_metrics_daily">> {
    return this.client.requestOperation("get_resource_metrics_daily", "get", "/{resource_type}/{resource_id}/metrics", init);
  }

  /** Get Total Account Metrics for An Organization */
  async org_account_metrics_total(init?: OperationInit<"org_account_metrics_total">): Promise<OperationData<"org_account_metrics_total">> {
    return this.client.requestOperation("org_account_metrics_total", "get", "/orgs/{org_id}/flows/account_metrics", init);
  }

  /** Get 24 Hour Flow Stats for a User */
  async user_24_hour_flow_stats(init?: OperationInit<"user_24_hour_flow_stats">): Promise<OperationData<"user_24_hour_flow_stats">> {
    return this.client.requestOperation("user_24_hour_flow_stats", "get", "/users/{user_id}/flows/dashboard", init);
  }

  /** Get Total Account Metrics for a User */
  async user_account_metrics_total(init?: OperationInit<"user_account_metrics_total">): Promise<OperationData<"user_account_metrics_total">> {
    return this.client.requestOperation("user_account_metrics_total", "get", "/users/{user_id}/flows/account_metrics", init);
  }

  /** Get Daily Data Processing Metrics for a User */
  async user_metrics_daily(init?: OperationInit<"user_metrics_daily">): Promise<OperationData<"user_metrics_daily">> {
    return this.client.requestOperation("user_metrics_daily", "get", "/users/{user_id}/metrics", init);
  }
}