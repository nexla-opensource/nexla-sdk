# Transforms & Schemas Reference

## Table of Contents
- [Mental Model](#mental-model)
- [Record Transforms API](#record-transforms-api)
- [Attribute Transforms API](#attribute-transforms-api)
- [Transform Code Structure](#transform-code-structure)
- [Schema Management](#schema-management)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

---

## Mental Model

**Transform types:**
- **Record transforms** (`client.transforms`): Apply operations to entire records (filter, map, aggregate)
- **Attribute transforms** (`client.attribute_transforms`): Apply operations to individual fields (mask, convert, extract)

**Reusability:**
- Set `reusable=True` to share transforms across multiple nexsets
- Use `list_public()` to discover shared transforms in your organization

**Data flow:**
```
Source → Nexset (with transform_id) → Transformed output → Destination
```

---

## Record Transforms API

```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.transforms.requests import TransformCreate, TransformUpdate

client = NexlaClient()
```

### List transforms
```python
transforms = client.transforms.list(page=1, per_page=25)
```

### List public (shared) transforms
```python
public_transforms = client.transforms.list_public()
```

### Get transform by ID
```python
transform = client.transforms.get(transform_id)
```

### Create transform
```python
transform = client.transforms.create(TransformCreate(
    name="remove-pii",
    description="Remove PII fields before delivery",
    output_type="json",
    reusable=True,
    code_type="jolt",
    code_encoding="json",
    code=[
        {"operation": "remove", "spec": {"ssn": "", "dob": ""}}
    ]
))
```

### Update transform
```python
updated = client.transforms.update(transform_id, TransformUpdate(
    description="Updated description",
    code=[{"operation": "shift", "spec": {"*": "&"}}]
))
```

### Copy transform
```python
copied = client.transforms.copy(transform_id)
```

### Delete transform
```python
client.transforms.delete(transform_id)
```

---

## Attribute Transforms API

Attribute transforms apply operations to individual fields.

```python
from nexla_sdk.models.attribute_transforms.requests import (
    AttributeTransformCreate, AttributeTransformUpdate
)
```

### List attribute transforms
```python
attr_transforms = client.attribute_transforms.list()
```

### Create attribute transform
```python
attr_transform = client.attribute_transforms.create(AttributeTransformCreate(
    name="mask-email",
    description="Mask email addresses",
    output_type="string",
    reusable=True,
    code_type="python",
    code_encoding="text",
    code='lambda x: x.split("@")[0][:2] + "***@" + x.split("@")[1] if "@" in str(x) else x'
))
```

### List public attribute transforms
```python
public_attr = client.attribute_transforms.list_public()
```

---

## Transform Code Structure

### TransformCodeOp

Record transforms use a list of operations:

```python
code = [
    {"operation": "shift", "spec": {"old_field": "new_field"}},
    {"operation": "remove", "spec": {"sensitive_field": ""}},
    {"operation": "default", "spec": {"missing_field": "default_value"}}
]
```

### Code Types

| code_type | Description | Use Case |
|-----------|-------------|----------|
| `jolt` | JSON-to-JSON transformation | Schema mapping, field renaming |
| `python` | Python code | Complex logic, data enrichment |
| `sql` | SQL expressions | Filtering, aggregation |
| `javascript` | JavaScript code | Web-style transformations |

### Code Encodings

| code_encoding | Description |
|---------------|-------------|
| `json` | JSON-encoded operation list |
| `text` | Plain text (for Python/JS code) |
| `base64` | Base64-encoded content |

### Output Types

| output_type | Description |
|-------------|-------------|
| `json` | JSON output (default) |
| `csv` | CSV output |
| `xml` | XML output |
| `text` | Plain text |

---

## Schema Management

### Via Nexsets

Schemas are managed through nexset properties:

```python
from nexla_sdk.models.nexsets.requests import NexsetCreate, NexsetUpdate

# Create nexset with custom schema
nexset = client.nexsets.create(NexsetCreate(
    name="validated-customers",
    parent_data_set_id=parent_id,
    has_custom_schema=True,
    output_schema={
        "type": "object",
        "properties": {
            "customer_id": {"type": "integer"},
            "email": {"type": "string", "format": "email"},
            "created_at": {"type": "string", "format": "date-time"}
        },
        "required": ["customer_id", "email"]
    }
))
```

### Attach transform to nexset

```python
client.nexsets.update(nexset_id, NexsetUpdate(
    has_custom_transform=True,
    transform_id=transform.id
))
```

### Validate with samples

```python
samples = client.nexsets.get_samples(nexset_id, count=10, include_metadata=True)
for sample in samples:
    print(sample.raw_message)
```

---

## Common Patterns

### Pattern 1: Create reusable PII removal transform

```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.transforms.requests import TransformCreate
from nexla_sdk.models.nexsets.requests import NexsetUpdate

client = NexlaClient()

# Create transform
transform = client.transforms.create(TransformCreate(
    name="remove-pii-v1",
    description="Remove sensitive fields (SSN, DOB, phone)",
    output_type="json",
    reusable=True,
    code_type="jolt",
    code_encoding="json",
    code=[
        {"operation": "remove", "spec": {"ssn": "", "dob": "", "phone": ""}}
    ]
))

# Apply to nexset
client.nexsets.update(nexset_id, NexsetUpdate(
    has_custom_transform=True,
    transform_id=transform.id
))

# Validate output
samples = client.nexsets.get_samples(nexset_id, count=5)
for sample in samples:
    assert "ssn" not in sample.raw_message, "PII field not removed!"
print("Transform validated successfully")
```

### Pattern 2: Field masking with attribute transform

```python
# Mask credit card numbers
cc_mask = client.attribute_transforms.create(AttributeTransformCreate(
    name="mask-credit-card",
    output_type="string",
    reusable=True,
    code_type="python",
    code_encoding="text",
    code='lambda x: "****-****-****-" + str(x)[-4:] if x else x'
))
```

### Pattern 3: Schema validation function

```python
def validate_schema(client, nexset_id, required_fields, field_types=None):
    """Validate nexset data against expected schema."""
    samples = client.nexsets.get_samples(nexset_id, count=20, include_metadata=True)

    issues = []
    for i, sample in enumerate(samples):
        record = sample.raw_message

        # Check required fields
        for field in required_fields:
            if field not in record:
                issues.append(f"Sample {i}: missing '{field}'")

        # Check field types
        if field_types:
            for field, expected_type in field_types.items():
                if field in record and not isinstance(record[field], expected_type):
                    actual = type(record[field]).__name__
                    issues.append(f"Sample {i}: '{field}' is {actual}, expected {expected_type.__name__}")

    return {"valid": len(issues) == 0, "sample_count": len(samples), "issues": issues}

# Usage
result = validate_schema(
    client, nexset_id,
    required_fields=["customer_id", "email", "created_at"],
    field_types={"customer_id": int, "email": str}
)
print(f"Valid: {result['valid']}, Issues: {len(result['issues'])}")
```

### Pattern 4: Copy and modify transform

```python
# Copy existing transform for modification
original = client.transforms.get(original_id)
copied = client.transforms.copy(original_id)

# Modify the copy
client.transforms.update(copied.id, TransformUpdate(
    name=f"{original.name}-v2",
    description="Enhanced version with additional filtering"
))
```

---

## Troubleshooting

### Transform not applying

1. Verify transform is attached:
```python
nexset = client.nexsets.get(nexset_id)
print(f"has_custom_transform: {nexset.has_custom_transform}")
print(f"transform_id: {nexset.transform_id}")
```

2. Check transform exists and is valid:
```python
transform = client.transforms.get(nexset.transform_id)
print(f"code_type: {transform.code_type}")
print(f"code: {transform.code}")
```

### Empty or unexpected output

1. Fetch samples from parent nexset:
```python
parent_samples = client.nexsets.get_samples(parent_nexset_id, count=5)
```

2. Compare with transformed output:
```python
transformed_samples = client.nexsets.get_samples(nexset_id, count=5)
```

### Transform errors in logs

Check metrics for transform-related failures:
```python
from nexla_sdk.models.metrics.enums import ResourceType

metrics = client.metrics.get_resource_metrics_by_run(
    resource_type=ResourceType.DATA_SETS,
    resource_id=nexset_id,
    page=1, size=10
)

for run in metrics.metrics:
    if run.get("status") == "FAILED":
        print(f"Run {run['runId']}: {run.get('error_message', 'No message')}")
```

### Common transform issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Empty output | Transform filters all records | Review filter logic |
| Null fields | Field path incorrect in spec | Check field names match source schema |
| Type errors | Output doesn't match expected type | Verify output_type setting |
| Slow performance | Complex nested operations | Simplify transform, test on smaller dataset |
