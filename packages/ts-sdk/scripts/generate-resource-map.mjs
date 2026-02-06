import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import YAML from "yaml";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const repoRoot = path.resolve(__dirname, "..", "..", "..");
const specPath = path.join(repoRoot, "plugin-redoc-0.yaml");
const generatedDir = path.join(__dirname, "..", "src", "generated");
const resourcesDir = path.join(__dirname, "..", "src", "resources", "generated");

const basePaths = {
  api_keys: "/api_keys",
  approval_requests: "/approval_requests",
  async_tasks: "/async_tasks",
  attribute_transforms: "/attribute_transforms",
  auth_parameters: "/auth_parameters",
  auth_templates: "/auth_templates",
  catalog_configs: "/catalog_configs",
  cluster_endpoints: "/cluster_endpoints",
  clusters: "/clusters",
  code_containers: "/code_containers",
  connectors: "/connectors",
  credentials: "/data_credentials",
  cubejs: "/cubejs",
  custom_data_flows: "/custom_data_flows",
  dashboard_transforms: "/dashboard_transforms",
  data_credentials_groups: "/data_credentials_groups",
  data_flows: "/data_flows",
  data_schemas: "/data_schemas",
  destinations: "/data_sinks",
  doc_containers: "/doc_containers",
  flow_nodes: "/flow_nodes",
  flow_triggers: "/flow_triggers",
  flows: "/flows",
  lookups: "/data_maps",
  marketplace: "/marketplace",
  mcp_sessions: "/mcp_sessions",
  nexsets: "/data_sets",
  notification_channel_settings: "/notification_channel_settings",
  notification_settings: "/notification_settings",
  notification_types: "/notification_types",
  notifications: "/notifications",
  org_auth_configs: "/api_auth_configs",
  org_tiers: "/org_tiers",
  organizations: "/orgs",
  projects: "/projects",
  quarantine_settings: "/quarantine_settings",
  resource_parameters: "/resource_parameters",
  runtimes: "/runtimes",
  search_health: "/search_health",
  self_signup_blocked_domains: "/self_signup_blocked_domains",
  service_keys: "/service_keys",
  sources: "/data_sources",
  teams: "/teams",
  tool_sets: "/tool_sets",
  tools: "/tools",
  transforms: "/transforms",
  user_settings: "/user_settings",
  user_tiers: "/user_tiers",
  users: "/users",
  validators: "/validators",
  vendor_endpoints: "/vendor_endpoints",
  vendors: "/vendors"
};

const tagToResource = {
  "Session Management": "tokens",
  "Flows": "flows",
  "Sources": "sources",
  "Destinations (Data Sinks)": "destinations",
  "Nexsets (Data Sets)": "nexsets",
  "Custom Data Flows": "custom_data_flows",
  "Credentials": "credentials",
  "Lookups (Data Maps)": "lookups",
  "Data Maps": "lookups",
  "Organizations": "organizations",
  "Users": "users",
  "Teams": "teams",
  "Projects": "projects",
  "Transforms": "transforms",
  "Attribute Transforms": "attribute_transforms",
  "Code Containers": "code_containers",
  "Doc Containers": "doc_containers",
  "Notifications": "notifications",
  "Notification Settings": "notification_settings",
  "Notification Types": "notification_types",
  "Notification Channel Settings": "notification_channel_settings",
  "Metrics": "metrics",
  "Audit Logs": "audit_logs",
  "Access Control": "access_control",
  "Quarantine Settings": "quarantine_settings",
  "Gen AI Recommendations": "genai",
  "Approval Requests": "approval_requests",
  "Limits": "limits",
  "Env: Org Management": "env_org_management",
  "Env: Vendor Management": "env_vendor_management",
  "Env: General Settings": "env_general_settings",
  "Org authentication configs": "org_auth_configs",
  "Marketplace": "marketplace",
  "Self Sign-Up": "self_signup",
  "Self Sign-Up Admin": "self_signup_admin",
  "Async Tasks": "async_tasks",
  "Custom Runtimes": "runtimes",
  "GenAI Configurations": "genai",
  "GenAI Configs": "genai",
  "GenAI Configuration": "genai",
  "API Keys": "api_keys",
  "Tool Sets": "tool_sets",
  "Tools": "tools",
  "Service Keys": "service_keys",
  "User Settings": "user_settings",
  "User Tiers": "user_tiers",
  "Org Tiers": "org_tiers",
  "Catalog Configs": "catalog_configs",
  "Clusters": "clusters",
  "Cluster Endpoints": "cluster_endpoints",
  "Connectors": "connectors",
  "Data Schemas": "data_schemas",
  "Data Flows": "data_flows",
  "Data Credentials Groups": "data_credentials_groups",
  "Auth Templates": "auth_templates",
  "Auth Parameters": "auth_parameters",
  "Resource Parameters": "resource_parameters",
  "Search Health": "search_health",
  "MCP Sessions": "mcp_sessions",
  "Flow Nodes": "flow_nodes",
  "Flow Triggers": "flow_triggers",
  "Vendors": "vendors",
  "Vendor Endpoints": "vendor_endpoints",
  "Dashboard Transforms": "dashboard_transforms",
  "CubeJS": "cubejs"
};

const rawSpec = fs.readFileSync(specPath, "utf8");
const spec = YAML.parse(rawSpec);
const paths = spec?.paths ?? {};

const METHODS = ["get", "post", "put", "patch", "delete", "options", "head", "trace"];

const normalizeTag = (value) => value.replace(/\s+/g, " ").trim();

const slugify = (value) =>
  value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .replace(/_+/g, "_");

const toPascalCase = (value) =>
  value
    .split("_")
    .filter(Boolean)
    .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
    .join("");

const isValidIdentifier = (value) => /^[A-Za-z_$][A-Za-z0-9_$]*$/.test(value);

const resolveResourceKey = (tags, apiPath) => {
  const tag = typeof tags?.[0] === "string" ? normalizeTag(tags[0]) : undefined;
  if (tag) {
    if (tag === "Webhooks") return null;
    return tagToResource[tag] ?? slugify(tag);
  }

  for (const [resourceKey, basePath] of Object.entries(basePaths)) {
    if (apiPath === basePath || apiPath.startsWith(`${basePath}/`)) {
      return resourceKey;
    }
  }

  return "misc";
};

const requiresSessionToken = (security) => {
  if (!security) return true;
  if (!Array.isArray(security) || security.length === 0) return false;
  return security.some((entry) => Object.prototype.hasOwnProperty.call(entry, "NexlaSessionToken"));
};

const operationsByResource = new Map();
const operationIndex = new Map();

for (const [apiPath, pathItem] of Object.entries(paths)) {
  for (const method of METHODS) {
    const operation = pathItem?.[method];
    if (!operation || !operation.operationId) continue;

    const operationId = operation.operationId;
    const resourceKey = resolveResourceKey(operation.tags, apiPath);
    if (!resourceKey) continue;

    const entry = {
      operationId,
      method,
      path: apiPath,
      summary: operation.summary ?? "",
      skipAuth: !requiresSessionToken(operation.security)
    };

    if (!operationsByResource.has(resourceKey)) {
      operationsByResource.set(resourceKey, []);
    }
    operationsByResource.get(resourceKey).push(entry);
    operationIndex.set(operationId, entry);
  }
}

const resourceMap = {};

for (const [resourceKey, basePath] of Object.entries(basePaths)) {
  const entry = {};
  const baseOps = paths[basePath] ?? {};

  if (baseOps.get) entry.list = { path: basePath, method: "get" };
  if (baseOps.post) entry.create = { path: basePath, method: "post" };

  const itemPath = Object.keys(paths).find((p) => {
    if (!p.startsWith(`${basePath}/`)) return false;
    const tail = p.slice(basePath.length + 1);
    return /^\{[^/]+\}$/.test(tail);
  });

  if (itemPath) {
    const itemOps = paths[itemPath] ?? {};
    if (itemOps.get) entry.get = { path: itemPath, method: "get" };
    if (itemOps.put) entry.update = { path: itemPath, method: "put" };
    else if (itemOps.patch) entry.update = { path: itemPath, method: "patch" };
    if (itemOps.delete) entry.delete = { path: itemPath, method: "delete" };
  }

  resourceMap[resourceKey] = entry;
}

const resourceMapContents = `/**\n * Auto-generated resource map from OpenAPI.\n * Do not edit manually.\n */\n\nexport const resourceMap = ${JSON.stringify(resourceMap, null, 2)} as const;\n\nexport type ResourceMap = typeof resourceMap;\n`;

fs.mkdirSync(generatedDir, { recursive: true });
fs.writeFileSync(path.join(generatedDir, "resource-map.ts"), resourceMapContents, "utf8");

const withSkipAuthContents = `/**\n * Auto-generated helpers for resource clients.\n * Do not edit manually.\n */\n\nimport type { HeadersOptions } from \"openapi-fetch\";\n\ntype HeaderCarrier = { headers?: HeadersOptions };\n\nconst normalizeHeaders = (headers?: HeadersOptions): Record<string, string> => {\n  if (!headers) return {};\n  if (headers instanceof Headers) {\n    const record: Record<string, string> = {};\n    headers.forEach((value, key) => {\n      record[key] = value;\n    });\n    return record;\n  }\n  if (Array.isArray(headers)) {\n    return Object.fromEntries(headers);\n  }\n  const record: Record<string, string> = {};\n  for (const [key, value] of Object.entries(headers)) {\n    if (value === null || value === undefined) continue;\n    if (Array.isArray(value)) {\n      record[key] = value.map((item) => String(item)).join(\", \");\n    } else {\n      record[key] = String(value);\n    }\n  }\n  return record;\n};\n\nexport const withSkipAuth = <T extends HeaderCarrier | undefined>(init?: T): T => {\n  if (!init) {\n    return { headers: { \"x-nexla-skip-auth\": \"true\" } } as unknown as T;\n  }\n  const headers = { ...normalizeHeaders(init.headers), \"x-nexla-skip-auth\": \"true\" };\n  return { ...(init as HeaderCarrier), headers } as unknown as T;\n};\n`;

if (fs.existsSync(resourcesDir)) {
  fs.rmSync(resourcesDir, { recursive: true, force: true });
}
fs.mkdirSync(resourcesDir, { recursive: true });
fs.writeFileSync(path.join(resourcesDir, "utils.ts"), withSkipAuthContents, "utf8");

const resourceKeys = Array.from(operationsByResource.keys()).sort();

const exportLines = [];
const interfaceLines = [];
const factoryLines = [];

for (const resourceKey of resourceKeys) {
  const operations = operationsByResource.get(resourceKey) ?? [];
  operations.sort((a, b) => a.operationId.localeCompare(b.operationId));

  const className = `${toPascalCase(resourceKey)}Resource`;
  exportLines.push(`export { ${className} } from \"./${resourceKey}.js\";`);
  interfaceLines.push(`  ${resourceKey}: ${className};`);
  factoryLines.push(`    ${resourceKey}: new ${className}(client)`);

  const methodNames = new Set();

  const aliasEntries = [];
  const resourceMapEntry = resourceMap[resourceKey];
  if (resourceMapEntry?.list) {
    const listOp = operations.find((op) => op.path === resourceMapEntry.list.path && op.method === resourceMapEntry.list.method);
    if (listOp) aliasEntries.push({ name: "list", op: listOp });
  }
  if (resourceMapEntry?.create) {
    const createOp = operations.find((op) => op.path === resourceMapEntry.create.path && op.method === resourceMapEntry.create.method);
    if (createOp) aliasEntries.push({ name: "create", op: createOp });
  }
  if (resourceMapEntry?.get) {
    const getOp = operations.find((op) => op.path === resourceMapEntry.get.path && op.method === resourceMapEntry.get.method);
    if (getOp) aliasEntries.push({ name: "get", op: getOp });
  }
  if (resourceMapEntry?.update) {
    const updateOp = operations.find((op) => op.path === resourceMapEntry.update.path && op.method === resourceMapEntry.update.method);
    if (updateOp) aliasEntries.push({ name: "update", op: updateOp });
  }
  if (resourceMapEntry?.delete) {
    const deleteOp = operations.find((op) => op.path === resourceMapEntry.delete.path && op.method === resourceMapEntry.delete.method);
    if (deleteOp) aliasEntries.push({ name: "delete", op: deleteOp });
  }

  const lines = [];
  lines.push("import type { NexlaClient } from \"../../client/nexla-client.js\";");
  lines.push("import type { OperationData, OperationInit } from \"../../client/operation-types.js\";");
  lines.push("import { withSkipAuth } from \"./utils.js\";");
  lines.push("");
  lines.push(`export class ${className} {`);
  lines.push("  private readonly client: NexlaClient;");
  lines.push("");
  lines.push("  constructor(client: NexlaClient) {");
  lines.push("    this.client = client;");
  lines.push("  }");

  for (const alias of aliasEntries) {
    if (methodNames.has(alias.name)) continue;
    methodNames.add(alias.name);
    lines.push("");
    const methodName = isValidIdentifier(alias.name) ? alias.name : `[\"${alias.name}\"]`;
    const maybeSkip = alias.op.skipAuth;
    const initVar = maybeSkip ? "withSkipAuth(init)" : "init";
    lines.push(`  async ${methodName}(init?: OperationInit<\"${alias.op.operationId}\">): Promise<OperationData<\"${alias.op.operationId}\">> {`);
    lines.push(`    return this.client.requestOperation(\"${alias.op.operationId}\", \"${alias.op.method}\", \"${alias.op.path}\", ${initVar});`);
    lines.push("  }");
  }

  for (const op of operations) {
    const opId = op.operationId;
    if (methodNames.has(opId)) continue;
    methodNames.add(opId);
    lines.push("");
    if (op.summary) {
      lines.push(`  /** ${op.summary.replace(/\*/g, "").trim()} */`);
    }
    const methodName = isValidIdentifier(opId) ? opId : `[\"${opId.replace(/\\/g, "\\\\").replace(/\"/g, "\\\"")}\"]`;
    const initVar = op.skipAuth ? "withSkipAuth(init)" : "init";
    lines.push(`  async ${methodName}(init?: OperationInit<\"${opId}\">): Promise<OperationData<\"${opId}\">> {`);
    lines.push(`    return this.client.requestOperation(\"${opId}\", \"${op.method}\", \"${op.path}\", ${initVar});`);
    lines.push("  }");
  }

  lines.push("}");

  fs.writeFileSync(path.join(resourcesDir, `${resourceKey}.ts`), lines.join("\n"), "utf8");
}

const indexLines = [];
indexLines.push("import type { NexlaClient } from \"../../client/nexla-client.js\";");
for (const resourceKey of resourceKeys) {
  const className = `${toPascalCase(resourceKey)}Resource`;
  indexLines.push(`import { ${className} } from \"./${resourceKey}.js\";`);
}
indexLines.push("");
for (const resourceKey of resourceKeys) {
  const className = `${toPascalCase(resourceKey)}Resource`;
  indexLines.push(`export { ${className} };`);
}
indexLines.push("");
indexLines.push("export interface GeneratedResourceClients {");
for (const line of interfaceLines) {
  indexLines.push(line);
}
indexLines.push("}");
indexLines.push("");
indexLines.push("export const createGeneratedResources = (client: NexlaClient): GeneratedResourceClients => ({");
for (const line of factoryLines) {
  indexLines.push(line + ",");
}
indexLines.push("});");

fs.writeFileSync(path.join(resourcesDir, "index.ts"), indexLines.join("\n"), "utf8");

console.log(`Generated resource map at ${path.join(generatedDir, "resource-map.ts")}`);
console.log(`Generated resources at ${resourcesDir}`);
