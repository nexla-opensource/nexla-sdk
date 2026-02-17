/**
 * Team test data factory.
 */

import { createOwner, createOrg, createTimestamp, generateId, type Owner, type Org } from "./common.js";

export interface TeamMember {
  id: number;
  email: string;
  full_name: string;
  admin: boolean;
}

export interface TeamResponse {
  id: number;
  name: string;
  description?: string;
  owner: Owner;
  org: Org;
  members: TeamMember[];
  member: boolean;
  access_roles: string[];
  created_at: string;
  updated_at: string;
}

export interface TeamMemberFactoryOptions {
  id?: number;
  email?: string;
  full_name?: string;
  admin?: boolean;
}

export interface TeamFactoryOptions {
  id?: number;
  name?: string;
  description?: string;
  owner?: Partial<Owner>;
  org?: Partial<Org>;
  members?: TeamMember[];
  member?: boolean;
  access_roles?: string[];
}

/**
 * Create a mock team member.
 */
export function createTeamMember(options: TeamMemberFactoryOptions = {}): TeamMember {
  const id = options.id ?? generateId();
  return {
    id,
    email: options.email ?? `member${id}@test.com`,
    full_name: options.full_name ?? `Test Member ${id}`,
    admin: options.admin ?? false,
  };
}

/**
 * Create a mock team response.
 */
export function createTeam(options: TeamFactoryOptions = {}): TeamResponse {
  const id = options.id ?? generateId();
  return {
    id,
    name: options.name ?? `Test Team ${id}`,
    description: options.description,
    owner: createOwner(options.owner),
    org: createOrg(options.org),
    members: options.members ?? [],
    member: options.member ?? true,
    access_roles: options.access_roles ?? ["owner"],
    created_at: createTimestamp(),
    updated_at: createTimestamp(),
  };
}

/**
 * Create a list of mock teams.
 */
export function createTeamList(count: number, options?: TeamFactoryOptions): TeamResponse[] {
  return Array.from({ length: count }, () => createTeam(options));
}
