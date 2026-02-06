import type { HttpMethod, PathsWithMethod } from "openapi-typescript-helpers";
import type { paths } from "../generated/schema.js";
import { resourceMap } from "../generated/resource-map.js";
import type { NexlaClient } from "../client/nexla-client.js";
import { NexlaError } from "../errors.js";
import type { RequestOptions } from "../client/types.js";

export type ResourceKey = keyof typeof resourceMap;

type ResourceEntry = {
  path: string;
  method: string;
};

type ResourceAction = "list" | "get" | "create" | "update" | "delete";

export class ResourceClient {
  private readonly client: NexlaClient;
  private readonly key: ResourceKey;

  constructor(client: NexlaClient, key: ResourceKey) {
    this.client = client;
    this.key = key;
  }

  async list(init?: Record<string, unknown>): Promise<unknown> {
    return this.call("list", init);
  }

  async get(init?: Record<string, unknown>): Promise<unknown> {
    return this.call("get", init);
  }

  async create(init?: Record<string, unknown>): Promise<unknown> {
    return this.call("create", init);
  }

  async update(init?: Record<string, unknown>): Promise<unknown> {
    return this.call("update", init);
  }

  async delete(init?: Record<string, unknown>): Promise<unknown> {
    return this.call("delete", init);
  }

  private async call(action: ResourceAction, init?: Record<string, unknown>): Promise<unknown> {
    const entry = (resourceMap[this.key] as Record<string, ResourceEntry | undefined>)[action];

    if (!entry) {
      throw new NexlaError(`Action '${action}' is not available for resource '${this.key}'.`);
    }

    const method = entry.method.toLowerCase() as HttpMethod;
    const path = entry.path as PathsWithMethod<paths, HttpMethod>;

    return this.client.request(method, path, init as RequestOptions);
  }
}
