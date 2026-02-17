/**
 * Accessor test data factory.
 */

import { generateId } from "./common.js";

export interface AccessorResponse {
  id: number;
  type: "USER" | "TEAM";
  access_roles: string[];
  org_id: number;
  email?: string;
  full_name?: string;
  user_id?: number;
  name?: string;
  team_id?: number;
}

export interface AccessorFactoryOptions {
  id?: number;
  type?: AccessorResponse["type"];
  access_roles?: string[];
  org_id?: number;
  email?: string;
  full_name?: string;
  user_id?: number;
  name?: string;
  team_id?: number;
}

/**
 * Create a mock accessor response.
 */
export function createAccessor(options: AccessorFactoryOptions = {}): AccessorResponse {
  const id = options.id ?? generateId();
  const type = options.type ?? "USER";

  const base: AccessorResponse = {
    id,
    type,
    access_roles: options.access_roles ?? ["collaborator"],
    org_id: options.org_id ?? 1,
  };

  if (type === "USER") {
    base.email = options.email ?? `user${id}@test.com`;
    base.full_name = options.full_name ?? `Test User ${id}`;
    base.user_id = options.user_id ?? id;
  } else {
    base.name = options.name ?? `Test Team ${id}`;
    base.team_id = options.team_id ?? id;
  }

  return base;
}

/**
 * Create a list of mock accessors.
 */
export function createAccessorList(count: number, options?: AccessorFactoryOptions): AccessorResponse[] {
  return Array.from({ length: count }, (_, i) => {
    // Alternate between USER and TEAM types
    const type = i % 2 === 0 ? "USER" : "TEAM";
    return createAccessor({ ...options, type: options?.type ?? type });
  });
}

/**
 * Create accessor request payload for adding/updating accessors.
 */
export function createAccessorRequest(options: {
  id: number;
  type: "USER" | "TEAM";
  access_roles?: string[];
}): { id: number; type: string; access_roles: string[] } {
  return {
    id: options.id,
    type: options.type,
    access_roles: options.access_roles ?? ["collaborator"],
  };
}
