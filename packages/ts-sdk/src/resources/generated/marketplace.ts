import type { NexlaClient } from "../../client/nexla-client.js";
import type { OperationData, OperationInit } from "../../client/operation-types.js";
import { withSkipAuth } from "./utils.js";

export class MarketplaceResource {
  private readonly client: NexlaClient;

  constructor(client: NexlaClient) {
    this.client = client;
  }

  /** Add custodians to a marketplace domain. */
  async add_domain_custodians(init?: OperationInit<"add_domain_custodians">): Promise<OperationData<"add_domain_custodians">> {
    return this.client.requestOperation("add_domain_custodians", "post", "/marketplace/domains/{domain_id}/custodians", init);
  }

  /** Create a single marketplace domain. */
  async create_domain(init?: OperationInit<"create_domain">): Promise<OperationData<"create_domain">> {
    return this.client.requestOperation("create_domain", "post", "/marketplace/domains/{domain_id}", init);
  }

  /** Create a marketplace item for a domain. */
  async create_domain_item(init?: OperationInit<"create_domain_item">): Promise<OperationData<"create_domain_item">> {
    return this.client.requestOperation("create_domain_item", "post", "/marketplace/domains/{domain_id}/items", init);
  }

  /** Create marketplace domains. */
  async create_domains(init?: OperationInit<"create_domains">): Promise<OperationData<"create_domains">> {
    return this.client.requestOperation("create_domains", "post", "/marketplace/domains", init);
  }

  /** Delete a single marketplace domain. */
  async delete_domain(init?: OperationInit<"delete_domain">): Promise<OperationData<"delete_domain">> {
    return this.client.requestOperation("delete_domain", "delete", "/marketplace/domains/{domain_id}", init);
  }

  /** Get a single marketplace domain. */
  async get_domain(init?: OperationInit<"get_domain">): Promise<OperationData<"get_domain">> {
    return this.client.requestOperation("get_domain", "get", "/marketplace/domains/{domain_id}", init);
  }

  /** Get custodians for a marketplace domain. */
  async get_domain_custodians(init?: OperationInit<"get_domain_custodians">): Promise<OperationData<"get_domain_custodians">> {
    return this.client.requestOperation("get_domain_custodians", "get", "/marketplace/domains/{domain_id}/custodians", init);
  }

  /** Get marketplace items for a domain. */
  async get_domain_items(init?: OperationInit<"get_domain_items">): Promise<OperationData<"get_domain_items">> {
    return this.client.requestOperation("get_domain_items", "get", "/marketplace/domains/{domain_id}/items", init);
  }

  /** Get marketplace domains. */
  async get_domains(init?: OperationInit<"get_domains">): Promise<OperationData<"get_domains">> {
    return this.client.requestOperation("get_domains", "get", "/marketplace/domains", init);
  }

  /** Get marketplace domains for organization. */
  async get_domains_for_org(init?: OperationInit<"get_domains_for_org">): Promise<OperationData<"get_domains_for_org">> {
    return this.client.requestOperation("get_domains_for_org", "get", "/marketplace/domains/for_org", init);
  }

  /** Remove custodians from a marketplace domain. */
  async remove_domain_custodians(init?: OperationInit<"remove_domain_custodians">): Promise<OperationData<"remove_domain_custodians">> {
    return this.client.requestOperation("remove_domain_custodians", "delete", "/marketplace/domains/{domain_id}/custodians", init);
  }

  /** Update a single marketplace domain. */
  async update_domain(init?: OperationInit<"update_domain">): Promise<OperationData<"update_domain">> {
    return this.client.requestOperation("update_domain", "put", "/marketplace/domains/{domain_id}", init);
  }

  /** Update custodians for a marketplace domain. */
  async update_domain_custodians(init?: OperationInit<"update_domain_custodians">): Promise<OperationData<"update_domain_custodians">> {
    return this.client.requestOperation("update_domain_custodians", "put", "/marketplace/domains/{domain_id}/custodians", init);
  }
}