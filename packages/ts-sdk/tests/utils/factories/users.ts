/**
 * User test data factory.
 */

import { createOrg, createTimestamp, generateId, type Org } from "./common.js";

export interface UserTeam {
  id: number;
  name: string;
}

export interface UserResponse {
  id: number;
  email: string;
  full_name: string;
  status: "ACTIVE" | "PENDING" | "INACTIVE" | "DELETED";
  org: Org;
  orgs: Org[];
  teams: UserTeam[];
  role: "admin" | "member" | "viewer";
  created_at: string;
  updated_at: string;
}

export interface UserFactoryOptions {
  id?: number;
  email?: string;
  full_name?: string;
  status?: UserResponse["status"];
  org?: Partial<Org>;
  orgs?: Partial<Org>[];
  teams?: Partial<UserTeam>[];
  role?: UserResponse["role"];
}

/**
 * Create a mock team object.
 */
function createTeam(overrides: Partial<UserTeam> = {}): UserTeam {
  const id = overrides.id ?? generateId();
  return {
    id,
    name: overrides.name ?? `Test Team ${id}`,
  };
}

/**
 * Create a mock user response.
 */
export function createUser(options: UserFactoryOptions = {}): UserResponse {
  const id = options.id ?? generateId();
  const org = createOrg(options.org);
  return {
    id,
    email: options.email ?? `user${id}@test.com`,
    full_name: options.full_name ?? `Test User ${id}`,
    status: options.status ?? "ACTIVE",
    org,
    orgs: options.orgs ? options.orgs.map((o) => createOrg(o)) : [org],
    teams: options.teams ? options.teams.map((t) => createTeam(t)) : [],
    role: options.role ?? "member",
    created_at: createTimestamp(),
    updated_at: createTimestamp(),
  };
}

/**
 * Create a list of mock users.
 */
export function createUserList(count: number, options?: UserFactoryOptions): UserResponse[] {
  return Array.from({ length: count }, () => createUser(options));
}
