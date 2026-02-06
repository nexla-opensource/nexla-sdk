/**
 * Project test data factory.
 */

import { createOwner, createOrg, createTimestamp, generateId, type Owner, type Org } from "./common.js";

export interface FlowReference {
  id: number;
  name: string;
}

export interface ProjectResponse {
  id: number;
  name: string;
  description?: string;
  owner: Owner;
  org: Org;
  flows: FlowReference[];
  data_flows: FlowReference[];
  access_roles: string[];
  copied_from_id?: number;
  created_at: string;
  updated_at: string;
}

export interface ProjectFactoryOptions {
  id?: number;
  name?: string;
  description?: string;
  owner?: Partial<Owner>;
  org?: Partial<Org>;
  flows?: FlowReference[];
  data_flows?: FlowReference[];
  access_roles?: string[];
  copied_from_id?: number;
}

/**
 * Create a mock flow reference.
 */
export function createFlowReference(overrides: Partial<FlowReference> = {}): FlowReference {
  const id = overrides.id ?? generateId();
  return {
    id,
    name: overrides.name ?? `Test Flow ${id}`,
  };
}

/**
 * Create a mock project response.
 */
export function createProject(options: ProjectFactoryOptions = {}): ProjectResponse {
  const id = options.id ?? generateId();
  return {
    id,
    name: options.name ?? `Test Project ${id}`,
    description: options.description,
    owner: createOwner(options.owner),
    org: createOrg(options.org),
    flows: options.flows ?? [],
    data_flows: options.data_flows ?? [],
    access_roles: options.access_roles ?? ["owner"],
    copied_from_id: options.copied_from_id,
    created_at: createTimestamp(),
    updated_at: createTimestamp(),
  };
}

/**
 * Create a list of mock projects.
 */
export function createProjectList(count: number, options?: ProjectFactoryOptions): ProjectResponse[] {
  return Array.from({ length: count }, () => createProject(options));
}
