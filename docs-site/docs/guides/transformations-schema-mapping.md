---
title: Transformations & Schema Mapping
description: Concepts and patterns for transforming data in flows.
slug: /guides/transformations
---

Flows embed transform nodes between source nexsets and downstream destinations. Use `NexsetCreate.transform` (or a reusable `transform_id`) to describe how records should be reshaped, then attach the resulting nexset to sinks or additional transforms.

```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.nexsets.requests import NexsetCreate

client = NexlaClient(service_key="<SERVICE_KEY>")

transformed = client.nexsets.create(NexsetCreate(
    name="Orders Flattened",
    parent_data_set_id=456789,  # Nexset emitted by a source
    has_custom_transform=True,
    transform={
        "version": 2,
        "operations": [
            {"operation": "flatten", "path": "line_items", "alias": "item"},
            {
                "operation": "rename",
                "fields": {
                    "item.productId": "product_id",
                    "item.quantity": "qty"
                }
            },
            {
                "operation": "compute",
                "expression": "qty * item.unitPrice",
                "as": "line_total"
            },
            {"operation": "filter", "condition": "status != 'CANCELLED'"}
        ]
    }
))
```

Common operations supported by the public API include:
- `flatten`: explode nested arrays or objects into distinct rows.
- `rename` / `map`: align field names with downstream schemas.
- `compute`: create derived values using Nexla's expression engine.
- `filter`: drop records that do not satisfy business rules.
- `typecast`: coerce data to expected types before validation.

When a transform is reusable across flows, store it as a template and set `transform_id` instead of duplicating the JSON payload. Copying a flow with `FlowCopyOptions(copy_entire_tree=True)` replicates the source → nexset → destination path and preserves the transform configuration.
