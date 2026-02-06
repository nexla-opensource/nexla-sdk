/**
 * Credential test data factory.
 */

import { createOwner, createOrg, createTimestamp, generateId, type Owner, type Org } from "./common.js";

export interface CredentialResponse {
  id: number;
  name: string;
  description?: string;
  credentials_type: string;
  credentials_version: string;
  verified_status: "VERIFIED" | "UNVERIFIED" | "FAILED";
  owner: Owner;
  org: Org;
  access_roles: string[];
  managed: boolean;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface CredentialFactoryOptions {
  id?: number;
  name?: string;
  description?: string;
  credentials_type?: string;
  credentials_version?: string;
  verified_status?: CredentialResponse["verified_status"];
  owner?: Partial<Owner>;
  org?: Partial<Org>;
  access_roles?: string[];
  managed?: boolean;
  tags?: string[];
}

/**
 * Create a mock credential response.
 */
export function createCredential(options: CredentialFactoryOptions = {}): CredentialResponse {
  const id = options.id ?? generateId();
  return {
    id,
    name: options.name ?? `Test Credential ${id}`,
    description: options.description,
    credentials_type: options.credentials_type ?? "postgres",
    credentials_version: options.credentials_version ?? "1",
    verified_status: options.verified_status ?? "VERIFIED",
    owner: createOwner(options.owner),
    org: createOrg(options.org),
    access_roles: options.access_roles ?? ["owner"],
    managed: options.managed ?? false,
    tags: options.tags ?? [],
    created_at: createTimestamp(),
    updated_at: createTimestamp(),
  };
}

/**
 * Create a list of mock credentials.
 */
export function createCredentialList(count: number, options?: CredentialFactoryOptions): CredentialResponse[] {
  return Array.from({ length: count }, () => createCredential(options));
}
