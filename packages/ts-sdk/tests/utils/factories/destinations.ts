/**
 * Destination test data factory.
 */

import { createOwner, createOrg, createTimestamp, generateId, type Owner, type Org } from "./common.js";

export interface DestinationResponse {
  id: number;
  name: string;
  description?: string;
  status: "ACTIVE" | "PAUSED" | "DRAFT" | "DELETED" | "ERROR" | "INIT";
  sink_type: string;
  managed: boolean;
  auto_generated: boolean;
  in_memory: boolean;
  owner: Owner;
  org: Org;
  access_roles: string[];
  data_set_id?: number;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface DestinationFactoryOptions {
  id?: number;
  name?: string;
  description?: string;
  status?: DestinationResponse["status"];
  sink_type?: string;
  managed?: boolean;
  auto_generated?: boolean;
  in_memory?: boolean;
  owner?: Partial<Owner>;
  org?: Partial<Org>;
  access_roles?: string[];
  data_set_id?: number;
  tags?: string[];
}

/**
 * Create a mock destination response.
 */
export function createDestination(options: DestinationFactoryOptions = {}): DestinationResponse {
  const id = options.id ?? generateId();
  return {
    id,
    name: options.name ?? `Test Destination ${id}`,
    description: options.description,
    status: options.status ?? "ACTIVE",
    sink_type: options.sink_type ?? "postgres",
    managed: options.managed ?? false,
    auto_generated: options.auto_generated ?? false,
    in_memory: options.in_memory ?? false,
    owner: createOwner(options.owner),
    org: createOrg(options.org),
    access_roles: options.access_roles ?? ["owner"],
    data_set_id: options.data_set_id,
    tags: options.tags ?? [],
    created_at: createTimestamp(),
    updated_at: createTimestamp(),
  };
}

/**
 * Create a list of mock destinations.
 */
export function createDestinationList(count: number, options?: DestinationFactoryOptions): DestinationResponse[] {
  return Array.from({ length: count }, () => createDestination(options));
}
