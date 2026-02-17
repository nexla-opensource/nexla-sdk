# TypeScript SDK Integration Testing (Non-Blocking)

This document defines how to add and run TS integration tests without turning them into a release blocker.

## Policy

- Integration tests are **non-blocking** relative to TypeScript release/publish gates.
- Unit/lint/typecheck/build remain the blocking CI checks.
- Integration runs are for confidence, signal, and early regression detection.
- Existing workflow: `.github/workflows/ci-ts-integration.yml` (scheduled + manual + PR path-based).

## When to Add Integration Tests

Add integration tests for:

- auth/token lifecycle behavior against a live environment
- critical write/read flows that cannot be fully validated with mocked HTTP
- regressions reported from real API interactions

## Test Placement and Naming

- Directory: `packages/ts-sdk/tests/integration/`
- File pattern: `*.test.ts`
- Keep tests idempotent and cleanup-aware.
- Avoid assumptions about globally shared account state.

## Required Environment Variables

- `NEXLA_SERVICE_KEY` (preferred)
- or `NEXLA_ACCESS_TOKEN`
- optional `NEXLA_API_URL`

Never commit credentials or test fixtures containing secrets.

## Local Run Commands

```bash
NEXLA_SERVICE_KEY=... pnpm -C packages/ts-sdk test -- --passWithNoTests tests/integration
```

For iterative runs:

```bash
NEXLA_SERVICE_KEY=... pnpm -C packages/ts-sdk test:watch -- tests/integration
```

## Suggested CI Shape (Non-Blocking)

If a CI workflow is added for TS integration tests, keep it isolated from release gating. Recommended options:

- separate workflow (`workflow_dispatch` and/or scheduled)
- `continue-on-error: true` on the integration job
- avoid `needs` dependencies from release jobs

Example job policy snippet:

```yaml
continue-on-error: true
if: ${{ secrets.NEXLA_SERVICE_KEY != '' || secrets.NEXLA_ACCESS_TOKEN != '' }}
```

## Reporting Expectations

- Integration test failures should create a clear signal in CI logs.
- Failing integration runs should not block package release automation by default.
- Use failures to prioritize reliability work and test hardening.
