/**
 * Common factory utilities and shared types.
 */

let idCounter = 1;

/**
 * Generate a unique ID for test data.
 */
export function generateId(): number {
  return idCounter++;
}

/**
 * Reset the ID counter (useful between test suites).
 */
export function resetIdCounter(): void {
  idCounter = 1;
}

/**
 * Create a mock owner object.
 */
export function createOwner(overrides: Partial<Owner> = {}): Owner {
  return {
    id: generateId(),
    full_name: `Test User ${idCounter}`,
    email: `user${idCounter}@test.com`,
    ...overrides,
  };
}

/**
 * Create a mock organization object.
 */
export function createOrg(overrides: Partial<Org> = {}): Org {
  return {
    id: generateId(),
    name: `Test Org ${idCounter}`,
    ...overrides,
  };
}

/**
 * Create a timestamp string.
 */
export function createTimestamp(): string {
  return new Date().toISOString();
}

// Type definitions
export interface Owner {
  id: number;
  full_name: string;
  email: string;
}

export interface Org {
  id: number;
  name: string;
}
