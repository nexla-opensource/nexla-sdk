/**
 * Nexset test data factory.
 */

import { createOwner, createOrg, createTimestamp, generateId, type Owner, type Org } from "./common.js";

export interface NexsetResponse {
  id: number;
  name: string;
  description?: string;
  status: "ACTIVE" | "PAUSED" | "DRAFT" | "DELETED" | "ERROR" | "INIT";
  data_format: string;
  managed: boolean;
  auto_generated: boolean;
  owner: Owner;
  org: Org;
  access_roles: string[];
  data_source_id?: number;
  tags: string[];
  input_schema?: unknown;
  output_schema?: unknown;
  created_at: string;
  updated_at: string;
}

export interface NexsetFactoryOptions {
  id?: number;
  name?: string;
  description?: string;
  status?: NexsetResponse["status"];
  data_format?: string;
  managed?: boolean;
  auto_generated?: boolean;
  owner?: Partial<Owner>;
  org?: Partial<Org>;
  access_roles?: string[];
  data_source_id?: number;
  tags?: string[];
  input_schema?: unknown;
  output_schema?: unknown;
}

/**
 * Create a mock nexset response.
 */
export function createNexset(options: NexsetFactoryOptions = {}): NexsetResponse {
  const id = options.id ?? generateId();
  return {
    id,
    name: options.name ?? `Test Nexset ${id}`,
    description: options.description,
    status: options.status ?? "ACTIVE",
    data_format: options.data_format ?? "JSON",
    managed: options.managed ?? false,
    auto_generated: options.auto_generated ?? false,
    owner: createOwner(options.owner),
    org: createOrg(options.org),
    access_roles: options.access_roles ?? ["owner"],
    data_source_id: options.data_source_id,
    tags: options.tags ?? [],
    input_schema: options.input_schema,
    output_schema: options.output_schema,
    created_at: createTimestamp(),
    updated_at: createTimestamp(),
  };
}

/**
 * Create a list of mock nexsets.
 */
export function createNexsetList(count: number, options?: NexsetFactoryOptions): NexsetResponse[] {
  return Array.from({ length: count }, () => createNexset(options));
}
