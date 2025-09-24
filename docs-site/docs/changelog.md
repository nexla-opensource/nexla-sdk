---
id: changelog
title: Changelog
description: Changes across releases based on Git tags.
slug: /changelog
---

The SDK follows semantic Git tags. Use `pip install nexla-sdk==<version>` to pin to a specific release. The highlights below pull from annotated commits; run `git log <old>..<new>` for full details.

## v0.1.8 — Webhook & Schema Enhancements
- Added schema template helpers in the schema client (create/get/delete `/data_schemas/templates`).
- Introduced webhook test, retry, and delivery history endpoints plus supporting models.
- Expanded integration coverage for `users.get_by_email`.
- Reference diff: `git diff v0.1.7..v0.1.8`.

## v0.1.7 — Token Lifecycle Improvements
- `TokenAuthHandler` refresh logic revamped; `NexlaClient.refresh_access_token()` exposed for manual refreshes.
- Better handling of expiring session tokens obtained from service keys.

## v0.1.6 — Client Refinements
- Client convenience methods tightened, addressing minor bugs identified during early adoption.

## v0.1.5 — Client Stability Fixes
- Additional adjustments to `NexlaClient` for pagination and serialization edge cases.

## v0.1.4 — Authentication Refactor
- Authentication flow reorganized, simplifying service-key handling and preparing for token reuse.

## v0.1.3 — Packaging & CI Updates
- Updated `pyproject.toml` metadata and publishing workflow.

## Git Shortlog

```text
### v0.1.3
- Update pyproject.toml for version management and enhance GitHub Actions workflow (d0c5b57)

### v0.1.4
- Refactor authentication handling in Nexla SDK (af418c2)

### v0.1.5
- Update client.py (ec130fc)

### v0.1.6
- Update client.py (ec130fc)

### v0.1.7
- Enhance token management in TokenAuthHandler and add refresh_access_token method in NexlaClient (57be7fe)

### v0.1.8
- Merge pull request #3 from golchakrish/add-get-user-by-email-nexla (9259aa1)
```
