import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const packageRoot = path.resolve(__dirname, "..");
const repoRoot = path.resolve(packageRoot, "..", "..");

const specPath = path.join(repoRoot, "plugin-redoc-0.yaml");
const outputPath = path.join(packageRoot, "src", "generated", "spec-metadata.ts");

const SPEC_SOURCE = "../../plugin-redoc-0.yaml";
const SPEC_HASH_ALGORITHM = "sha256";

const specBytes = fs.readFileSync(specPath);
const specHash = crypto.createHash(SPEC_HASH_ALGORITHM).update(specBytes).digest("hex");

const output = `/**
 * Auto-generated spec metadata from ${SPEC_SOURCE}.
 * Do not edit manually.
 */

export const SPEC_SOURCE = "${SPEC_SOURCE}";
export const SPEC_HASH_ALGORITHM = "${SPEC_HASH_ALGORITHM}";
export const SPEC_HASH = "${specHash}";
`;

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, output, "utf8");

console.log(`Generated spec metadata at ${outputPath}`);
