# TypeScript SDK API Coverage Process

## Coverage Dimensions

The TS SDK tracks coverage in two dimensions:

- **OpenAPI operation coverage:** whether every API `operationId` is available through generated TS resource methods.
- **Python-to-TS surface parity:** whether Python `client.<resource>` surfaces exist as first-class TS resource clients.

Operation coverage can be high while resource parity is still incomplete; these are tracked separately by design.

## Source of Truth

- OpenAPI spec: `plugin-redoc-0.yaml`
- Generated TS schema: `packages/ts-sdk/src/generated/schema.ts`
- Generated TS resources: `packages/ts-sdk/src/resources/generated/*.ts`
- Python resource surface: `nexla_sdk/client.py`
- Generated parity report: `docs/ts-sdk/parity-matrix.md`

## Refresh Workflow

Run this from repository root whenever API surface changes:

```bash
pnpm -C packages/ts-sdk gen
node packages/ts-sdk/scripts/generate-parity-matrix.mjs
pnpm -C packages/ts-sdk lint
pnpm -C packages/ts-sdk typecheck
pnpm -C packages/ts-sdk coverage
```

What this does:

1. Regenerates all TS OpenAPI artifacts.
2. Recomputes Python->TS parity and operation coverage matrix.
3. Verifies SDK quality gates still pass.

## CI Expectations

`ci-ts.yml` already enforces generated artifact consistency (`pnpm -C packages/ts-sdk gen` + clean git diff) and blocks merges if generated files are stale.

The parity matrix file is documentation output and should be refreshed in the same PR when parity or coverage changes.

## Interpreting `parity-matrix.md`

- **Python resource parity %**: how many Python resource surfaces currently have first-class TS resource clients.
- **Session operationId coverage %**: how many spec operationIds are generated into TS resource clients.
- **TS-only resources**: TS resource clients that do not yet exist as Python first-class resource properties.

## Gap Handling Policy

If a Python resource is not yet available as a generated TS resource client:

- Use `client.raw` as a typed fallback for path-level access.
- Keep migration docs updated with guidance for that resource.
- Track progress by refreshing `docs/ts-sdk/parity-matrix.md`.

## PR Checklist (Coverage-Sensitive Changes)

1. Regenerate TS artifacts (`pnpm -C packages/ts-sdk gen`).
2. Refresh parity matrix (`node packages/ts-sdk/scripts/generate-parity-matrix.mjs`).
3. Run lint/typecheck/tests for TS SDK.
4. Update `docs/ts-sdk/migration-guide.md` if Python->TS mapping changed.
5. Include generated doc diffs (`docs/ts-sdk/parity-matrix.md`) in the PR.

## Related Docs

- [Architecture](./architecture.md)
- [Migration guide](./migration-guide.md)
- [Integration testing (non-blocking guidance)](./integration-tests.md)
