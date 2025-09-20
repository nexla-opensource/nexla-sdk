---
id: faq
title: FAQ
description: Frequently asked questions about using the SDK.
slug: /faq
---

Q: How do I authenticate?
A: Prefer service keys using `NEXLA_SERVICE_KEY` or `NexlaClient(service_key=...)`.

Q: How do I enable tracing?
A: Set OTEL environment variables; the SDK auto-detects configuration.

Q: Where are the CLI commands?
A: This package ships as a Python library only—there is no bundled CLI. Use the Nexla web UI for interactive workflows or build small entry points with `NexlaClient` for automation. Reach out to support@nexla.com if you need access to the hosted Nexla CLI offering.
