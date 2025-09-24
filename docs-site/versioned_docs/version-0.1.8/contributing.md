---
id: contributing
title: Contributing to Docs
description: How to contribute and preview the documentation site.
slug: /contributing
---

Local development:

```bash
npm install
npm run start
```

Generate API docs (Python):

```bash
pip install -e ..
python3 scripts/gen_api_docs.py
```

Style:

- Markdownlint + Prettier (run `npm run lint`)

