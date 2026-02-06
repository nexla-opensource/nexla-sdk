import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import YAML from "yaml";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const repoRoot = path.resolve(__dirname, "..", "..", "..");
const pythonClientPath = path.join(repoRoot, "nexla_sdk", "client.py");
const tsClientPath = path.join(repoRoot, "packages", "ts-sdk", "src", "client", "nexla-client.ts");
const tsGeneratedIndexPath = path.join(repoRoot, "packages", "ts-sdk", "src", "resources", "generated", "index.ts");
const tsGeneratedResourcesDir = path.join(repoRoot, "packages", "ts-sdk", "src", "resources", "generated");
const openApiPath = path.join(repoRoot, "plugin-redoc-0.yaml");
const outputPath = path.join(repoRoot, "docs", "ts-sdk", "parity-matrix.md");

const METHODS = ["get", "post", "put", "patch", "delete", "options", "head", "trace"];

const read = (filePath) => fs.readFileSync(filePath, "utf8");

const toPercent = (numerator, denominator) => {
  if (denominator === 0) return "0.0";
  return ((numerator / denominator) * 100).toFixed(1);
};

const extractPythonResources = (source) => {
  const set = new Set();
  const assignmentPattern = /self\.([a-z_]+)\s*=\s*[A-Za-z0-9_]+Resource\(self\)/g;

  let match = assignmentPattern.exec(source);
  while (match) {
    set.add(match[1]);
    match = assignmentPattern.exec(source);
  }

  if (/def\s+create_webhook_client\s*\(/.test(source)) {
    set.add("webhooks");
  }

  return [...set].sort();
};

const extractTsResources = (generatedIndexSource, tsClientSource) => {
  const set = new Set();
  const assignmentPattern = /^\s*([a-z_]+):\s*new\s+[A-Za-z0-9_]+\(client\),?\s*$/gm;

  let match = assignmentPattern.exec(generatedIndexSource);
  while (match) {
    set.add(match[1]);
    match = assignmentPattern.exec(generatedIndexSource);
  }

  if (
    /readonly\s+webhooks\?:\s+WebhooksClient;/.test(tsClientSource) ||
    /new\s+WebhooksClient\(/.test(tsClientSource)
  ) {
    set.add("webhooks");
  }

  return [...set].sort();
};

const extractSpecOperationIds = (rawSpec) => {
  const spec = YAML.parse(rawSpec);
  const paths = spec?.paths ?? {};

  const allOperationIds = new Set();
  const sessionOperationIds = new Set();
  const webhookOperationIds = new Set();

  for (const pathItem of Object.values(paths)) {
    for (const method of METHODS) {
      const operation = pathItem?.[method];
      if (!operation?.operationId) continue;

      const operationId = operation.operationId;
      allOperationIds.add(operationId);

      const firstTag = Array.isArray(operation.tags) && typeof operation.tags[0] === "string"
        ? operation.tags[0].trim()
        : "";

      if (firstTag === "Webhooks") {
        webhookOperationIds.add(operationId);
      } else {
        sessionOperationIds.add(operationId);
      }
    }
  }

  return { allOperationIds, sessionOperationIds, webhookOperationIds };
};

const extractTsOperationIds = (generatedResourcesDir) => {
  const set = new Set();
  const files = fs
    .readdirSync(generatedResourcesDir)
    .filter((fileName) => fileName.endsWith(".ts") && fileName !== "index.ts" && fileName !== "utils.ts");

  for (const fileName of files) {
    const filePath = path.join(generatedResourcesDir, fileName);
    const source = read(filePath);
    const operationPattern = /requestOperation\("([^"]+)"/g;

    let match = operationPattern.exec(source);
    while (match) {
      set.add(match[1]);
      match = operationPattern.exec(source);
    }
  }

  return set;
};

const formatCode = (value) => `\`${value}\``;

const buildResourceRows = (pythonResources, tsResources) => {
  const tsSet = new Set(tsResources);

  const aliasMap = {
    webhooks: "webhooks"
  };

  const notes = {
    webhooks:
      "Python uses create_webhook_client(); TS uses WebhooksClient directly or NexlaClient({ webhookApiKey })."
  };

  const rows = [];
  let coveredCount = 0;

  for (const pythonResource of pythonResources) {
    const alias = aliasMap[pythonResource] ?? pythonResource;
    const isCovered = tsSet.has(alias);

    if (isCovered) coveredCount += 1;

    const tsEquivalent = isCovered
      ? alias === "webhooks"
        ? "`WebhooksClient` / `client.webhooks`"
        : formatCode(`client.${alias}`)
      : "--";

    const status = isCovered ? "covered" : "missing";
    const note = notes[pythonResource]
      ? notes[pythonResource]
      : isCovered
        ? "Generated TS resource client available."
        : "Use `client.raw` for typed path-level access until this resource is generated.";

    rows.push(`| ${formatCode(pythonResource)} | ${tsEquivalent} | ${status} | ${note} |`);
  }

  return { rows, coveredCount };
};

const buildTsOnlyRows = (pythonResources, tsResources) => {
  const pythonSet = new Set(pythonResources);

  return tsResources
    .filter((resource) => !pythonSet.has(resource))
    .map((resource) => {
      const note = resource === "webhooks"
        ? "Webhook support exists in both SDKs but with different entry points."
        : "OpenAPI-generated TS resource. Python client does not expose this as a first-class resource property.";
      return `| ${formatCode(resource)} | ${note} |`;
    });
};

const renderMarkdown = ({
  pythonResources,
  tsResources,
  coveredCount,
  specOperationIds,
  specSessionOperationIds,
  specWebhookOperationIds,
  tsOperationIds,
  missingOperationIds,
  extraOperationIds,
  pythonRows,
  tsOnlyRows
}) => {
  const lines = [];
  const generatedAt = new Date().toISOString();

  lines.push("# TypeScript SDK Parity Matrix (Generated)");
  lines.push("");
  lines.push("> Auto-generated by `node packages/ts-sdk/scripts/generate-parity-matrix.mjs`. Do not edit this file manually.");
  lines.push("");
  lines.push(`Generated at: ${formatCode(generatedAt)}`);
  lines.push("");
  lines.push("## Summary");
  lines.push("");
  lines.push(`- Python resources discovered: **${pythonResources.length}**`);
  lines.push(`- TS resources discovered: **${tsResources.length}**`);
  lines.push(
    `- Python resource parity: **${coveredCount}/${pythonResources.length} (${toPercent(coveredCount, pythonResources.length)}%)**`
  );
  lines.push(`- OpenAPI operations in spec: **${specOperationIds.size}**`);
  lines.push(`- OpenAPI session operations in spec (excluding webhook-tagged operations): **${specSessionOperationIds.size}**`);
  lines.push(`- OpenAPI webhook-tagged operations in spec: **${specWebhookOperationIds.size}**`);
  lines.push(`- OperationIds implemented in generated TS resources: **${tsOperationIds.size}**`);
  lines.push(
    `- Session operationId coverage: **${specSessionOperationIds.size - missingOperationIds.length}/${specSessionOperationIds.size} (${toPercent(specSessionOperationIds.size - missingOperationIds.length, specSessionOperationIds.size)}%)**`
  );
  lines.push("");
  lines.push("## Python To TS Resource Parity");
  lines.push("");
  lines.push("| Python resource | TS equivalent | Status | Notes |");
  lines.push("| --- | --- | --- | --- |");
  lines.push(...pythonRows);

  if (tsOnlyRows.length > 0) {
    lines.push("");
    lines.push("## TS-Only Resource Surfaces");
    lines.push("");
    lines.push("| TS resource | Notes |");
    lines.push("| --- | --- |");
    lines.push(...tsOnlyRows);
  }

  lines.push("");
  lines.push("## Operation Coverage Details");
  lines.push("");
  lines.push(`- Missing session operationIds in generated TS resources: **${missingOperationIds.length}**`);
  lines.push(`- Extra operationIds in generated TS resources (not found in current spec session set): **${extraOperationIds.length}**`);

  if (missingOperationIds.length > 0) {
    lines.push("");
    lines.push("### Missing operationIds");
    lines.push("");
    for (const operationId of missingOperationIds) {
      lines.push(`- ${formatCode(operationId)}`);
    }
  }

  if (extraOperationIds.length > 0) {
    lines.push("");
    lines.push("### Extra operationIds");
    lines.push("");
    for (const operationId of extraOperationIds) {
      lines.push(`- ${formatCode(operationId)}`);
    }
  }

  lines.push("");
  return `${lines.join("\n")}`;
};

const main = () => {
  const pythonClientSource = read(pythonClientPath);
  const tsClientSource = read(tsClientPath);
  const tsGeneratedIndexSource = read(tsGeneratedIndexPath);
  const rawSpec = read(openApiPath);

  const pythonResources = extractPythonResources(pythonClientSource);
  const tsResources = extractTsResources(tsGeneratedIndexSource, tsClientSource);

  const { allOperationIds, sessionOperationIds, webhookOperationIds } = extractSpecOperationIds(rawSpec);
  const tsOperationIds = extractTsOperationIds(tsGeneratedResourcesDir);

  const missingOperationIds = [...sessionOperationIds]
    .filter((operationId) => !tsOperationIds.has(operationId))
    .sort();

  const extraOperationIds = [...tsOperationIds]
    .filter((operationId) => !sessionOperationIds.has(operationId))
    .sort();

  const { rows: pythonRows, coveredCount } = buildResourceRows(pythonResources, tsResources);
  const tsOnlyRows = buildTsOnlyRows(pythonResources, tsResources);

  const markdown = renderMarkdown({
    pythonResources,
    tsResources,
    coveredCount,
    specOperationIds: allOperationIds,
    specSessionOperationIds: sessionOperationIds,
    specWebhookOperationIds: webhookOperationIds,
    tsOperationIds,
    missingOperationIds,
    extraOperationIds,
    pythonRows,
    tsOnlyRows
  });

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, markdown, "utf8");

  process.stdout.write(`Wrote ${path.relative(repoRoot, outputPath)}\n`);
};

main();
