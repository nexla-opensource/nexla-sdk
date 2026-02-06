/**
 * Flow test data factory.
 */

import { createOwner, createOrg, createTimestamp, generateId, type Owner, type Org } from "./common.js";

export interface FlowNode {
  id: number;
  node_type: "SOURCE" | "TRANSFORM" | "DESTINATION" | "NEXSET";
  resource_id: number;
  resource_type: string;
  status: "ACTIVE" | "PAUSED" | "ERROR" | "INIT";
  upstream_node_ids: number[];
  downstream_node_ids: number[];
}

export interface FlowResponse {
  id: number;
  name: string;
  description?: string;
  status: "ACTIVE" | "PAUSED" | "DRAFT" | "DELETED" | "ERROR" | "INIT";
  flow_type: "DATA_FLOW" | "INGESTION" | "TRANSFORMATION" | "DISTRIBUTION";
  owner: Owner;
  org: Org;
  nodes: FlowNode[];
  origin_node_id: number | null;
  data_sources: unknown[];
  data_sets: unknown[];
  data_sinks: unknown[];
  access_roles: string[];
  created_at: string;
  updated_at: string;
}

export interface FlowNodeFactoryOptions {
  id?: number;
  node_type?: FlowNode["node_type"];
  resource_id?: number;
  resource_type?: string;
  status?: FlowNode["status"];
  upstream_node_ids?: number[];
  downstream_node_ids?: number[];
}

export interface FlowFactoryOptions {
  id?: number;
  name?: string;
  description?: string;
  status?: FlowResponse["status"];
  flow_type?: FlowResponse["flow_type"];
  owner?: Partial<Owner>;
  org?: Partial<Org>;
  nodes?: FlowNode[];
  origin_node_id?: number | null;
  access_roles?: string[];
}

/**
 * Create a mock flow node.
 */
export function createFlowNode(options: FlowNodeFactoryOptions = {}): FlowNode {
  const id = options.id ?? generateId();
  return {
    id,
    node_type: options.node_type ?? "SOURCE",
    resource_id: options.resource_id ?? generateId(),
    resource_type: options.resource_type ?? "data_source",
    status: options.status ?? "ACTIVE",
    upstream_node_ids: options.upstream_node_ids ?? [],
    downstream_node_ids: options.downstream_node_ids ?? [],
  };
}

/**
 * Create a mock flow response.
 */
export function createFlow(options: FlowFactoryOptions = {}): FlowResponse {
  const id = options.id ?? generateId();
  const nodes = options.nodes ?? [createFlowNode()];
  return {
    id,
    name: options.name ?? `Test Flow ${id}`,
    description: options.description,
    status: options.status ?? "ACTIVE",
    flow_type: options.flow_type ?? "DATA_FLOW",
    owner: createOwner(options.owner),
    org: createOrg(options.org),
    nodes,
    origin_node_id: options.origin_node_id ?? (nodes.length > 0 ? nodes[0]!.id : null),
    data_sources: [],
    data_sets: [],
    data_sinks: [],
    access_roles: options.access_roles ?? ["owner"],
    created_at: createTimestamp(),
    updated_at: createTimestamp(),
  };
}

/**
 * Create a list of mock flows.
 */
export function createFlowList(count: number, options?: FlowFactoryOptions): FlowResponse[] {
  return Array.from({ length: count }, () => createFlow(options));
}
