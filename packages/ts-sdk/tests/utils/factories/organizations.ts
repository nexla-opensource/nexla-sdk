/**
 * Organization test data factory.
 */

import { createOwner, createTimestamp, generateId, type Owner } from "./common.js";

export interface OrganizationMember {
  id: number;
  email: string;
  full_name: string;
  role: "owner" | "admin" | "member";
}

export interface OrganizationResponse {
  id: number;
  name: string;
  description?: string;
  email_domain?: string;
  owner: Owner;
  members: OrganizationMember[];
  custodians: OrganizationMember[];
  status: "ACTIVE" | "INACTIVE" | "SUSPENDED";
  created_at: string;
  updated_at: string;
}

export interface OrganizationMemberOptions {
  id?: number;
  email?: string;
  full_name?: string;
  role?: OrganizationMember["role"];
}

export interface OrganizationFactoryOptions {
  id?: number;
  name?: string;
  description?: string;
  email_domain?: string;
  owner?: Partial<Owner>;
  members?: OrganizationMemberOptions[];
  custodians?: OrganizationMemberOptions[];
  status?: OrganizationResponse["status"];
}

/**
 * Create a mock organization member.
 */
export function createOrganizationMember(options: OrganizationMemberOptions = {}): OrganizationMember {
  const id = options.id ?? generateId();
  return {
    id,
    email: options.email ?? `member${id}@test.com`,
    full_name: options.full_name ?? `Test Member ${id}`,
    role: options.role ?? "member",
  };
}

/**
 * Create a mock organization response.
 */
export function createOrganization(options: OrganizationFactoryOptions = {}): OrganizationResponse {
  const id = options.id ?? generateId();
  return {
    id,
    name: options.name ?? `Test Organization ${id}`,
    description: options.description,
    email_domain: options.email_domain,
    owner: createOwner(options.owner),
    members: options.members?.map(createOrganizationMember) ?? [],
    custodians: options.custodians?.map(createOrganizationMember) ?? [],
    status: options.status ?? "ACTIVE",
    created_at: createTimestamp(),
    updated_at: createTimestamp(),
  };
}

/**
 * Create a list of mock organizations.
 */
export function createOrganizationList(count: number, options?: OrganizationFactoryOptions): OrganizationResponse[] {
  return Array.from({ length: count }, () => createOrganization(options));
}
