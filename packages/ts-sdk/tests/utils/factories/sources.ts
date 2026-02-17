/**
 * Source test data factory.
 */

import { createOwner, createOrg, createTimestamp, generateId, type Owner, type Org } from "./common.js";

export interface SourceResponse {
  id: number;
  name: string;
  description?: string;
  status: "ACTIVE" | "PAUSED" | "DRAFT" | "DELETED" | "ERROR" | "INIT";
  source_type: string;
  ingest_method: string;
  source_format: string;
  managed: boolean;
  auto_generated: boolean;
  owner: Owner;
  org: Org;
  access_roles: string[];
  data_sets: unknown[];
  data_credentials?: unknown;
  tags: string[];
  run_ids: unknown[];
  created_at: string;
  updated_at: string;
}

export interface SourceFactoryOptions {
  id?: number;
  name?: string;
  description?: string;
  status?: SourceResponse["status"];
  source_type?: string;
  ingest_method?: string;
  source_format?: string;
  managed?: boolean;
  auto_generated?: boolean;
  owner?: Partial<Owner>;
  org?: Partial<Org>;
  access_roles?: string[];
  tags?: string[];
}

/**
 * Create a mock source response.
 */
export function createSource(options: SourceFactoryOptions = {}): SourceResponse {
  const id = options.id ?? generateId();
  return {
    id,
    name: options.name ?? `Test Source ${id}`,
    description: options.description,
    status: options.status ?? "ACTIVE",
    source_type: options.source_type ?? "postgres",
    ingest_method: options.ingest_method ?? "POLL",
    source_format: options.source_format ?? "JSON",
    managed: options.managed ?? false,
    auto_generated: options.auto_generated ?? false,
    owner: createOwner(options.owner),
    org: createOrg(options.org),
    access_roles: options.access_roles ?? ["owner"],
    data_sets: [],
    data_credentials: undefined,
    tags: options.tags ?? [],
    run_ids: [],
    created_at: createTimestamp(),
    updated_at: createTimestamp(),
  };
}

/**
 * Create a list of mock sources.
 */
export function createSourceList(count: number, options?: SourceFactoryOptions): SourceResponse[] {
  return Array.from({ length: count }, () => createSource(options));
}
