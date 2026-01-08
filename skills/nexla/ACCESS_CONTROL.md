# Access Control Reference

## Table of Contents
- [Mental Model](#mental-model)
- [Accessor Types](#accessor-types)
- [Access Roles](#access-roles)
- [API Reference](#api-reference)
- [Common Patterns](#common-patterns)
- [Audit Trail](#audit-trail)
- [Troubleshooting](#troubleshooting)

---

## Mental Model

**Access control in Nexla:**
- Every resource (source, nexset, destination, flow) has accessors
- Accessors are users, teams, or organizations with specific roles
- Operations: add (additive), replace (overwrite all), delete (remove specific)

**Inheritance:**
- Child resources do NOT inherit parent access automatically
- Grant access explicitly to each resource in a pipeline

---

## Accessor Types

| Type | Identifier | Description |
|------|------------|-------------|
| `USER` | `email` or `id` | Individual user access |
| `TEAM` | `id` or `name` | Team-based access |
| `ORG` | `id` or `email_domain` | Cross-organization sharing |

### User accessor
```python
{"type": "USER", "email": "analyst@company.com", "access_roles": ["collaborator"]}
# or
{"type": "USER", "id": 123, "access_roles": ["operator"]}
```

### Team accessor
```python
{"type": "TEAM", "id": 456, "access_roles": ["operator"]}
# or
{"type": "TEAM", "name": "data-engineering", "access_roles": ["admin"]}
```

### Organization accessor (cross-org)
```python
{"type": "ORG", "id": 789, "access_roles": ["collaborator"]}
# or
{"type": "ORG", "email_domain": "partner.com", "access_roles": ["collaborator"]}
```

---

## Access Roles

| Role | Permissions |
|------|-------------|
| `owner` | Full control: delete, transfer ownership, manage all settings |
| `admin` | Manage settings, accessors, activate/pause, but cannot delete |
| `operator` | Activate, pause, monitor, view logs, run samples |
| `collaborator` | View-only: read settings, view data samples, no modifications |

### Role hierarchy
```
owner > admin > operator > collaborator
```

---

## API Reference

All resources inherit these methods from BaseResource:

### get_accessors(resource_id)

Returns list of current accessors:

```python
accessors = client.sources.get_accessors(source_id)
for acc in accessors:
    print(f"{acc.type}: {getattr(acc, 'email', None) or acc.id} - {acc.access_roles}")
```

### add_accessors(resource_id, accessors)

**Additive** - adds to existing accessors:

```python
client.sources.add_accessors(source_id, [
    {"type": "USER", "email": "new-user@company.com", "access_roles": ["collaborator"]}
])
```

### replace_accessors(resource_id, accessors)

**Replaces all** accessors (use with caution):

```python
client.sources.replace_accessors(source_id, [
    {"type": "USER", "email": "admin@company.com", "access_roles": ["owner"]},
    {"type": "TEAM", "id": team_id, "access_roles": ["operator"]}
])
```

### delete_accessors(resource_id, accessors)

Removes specific accessors:

```python
client.sources.delete_accessors(source_id, [
    {"type": "USER", "email": "old-user@company.com"}
])
```

---

## Common Patterns

### Pattern 1: Grant user access to a resource

```python
from nexla_sdk import NexlaClient

client = NexlaClient()

# Grant collaborator access to a source
client.sources.add_accessors(source_id, [
    {"type": "USER", "email": "analyst@company.com", "access_roles": ["collaborator"]}
])

# Verify access was granted
accessors = client.sources.get_accessors(source_id)
print(f"Current accessors: {len(accessors)}")
```

### Pattern 2: Grant team access to entire pipeline

```python
def grant_pipeline_access(client, team_id, source_id, role="operator"):
    """Grant team access to source → nexsets → destinations."""
    accessor = {"type": "TEAM", "id": team_id, "access_roles": [role]}
    results = {"sources": [], "nexsets": [], "destinations": []}

    # Grant to source
    client.sources.add_accessors(source_id, [accessor])
    results["sources"].append(source_id)

    # Find and grant to connected nexsets
    source = client.sources.get(source_id, expand=True)
    for ds in getattr(source, 'data_sets', []):
        nexset_id = ds.id if hasattr(ds, 'id') else ds
        client.nexsets.add_accessors(nexset_id, [accessor])
        results["nexsets"].append(nexset_id)

        # Find and grant to connected destinations
        nexset = client.nexsets.get(nexset_id)
        for sink in getattr(nexset, 'data_sinks', []):
            sink_id = sink.id if hasattr(sink, 'id') else sink
            client.destinations.add_accessors(sink_id, [accessor])
            results["destinations"].append(sink_id)

    return results

# Usage
result = grant_pipeline_access(client, team_id=123, source_id=456, role="operator")
print(f"Granted access to {sum(len(v) for v in result.values())} resources")
```

### Pattern 3: Bulk grant access to project resources

```python
def grant_team_to_project(client, project_id, team_id, role="collaborator"):
    """Grant team access to all resources in a project."""
    accessor = {"type": "TEAM", "id": team_id, "access_roles": [role]}
    granted = 0

    for source in client.sources.list(project_id=project_id):
        client.sources.add_accessors(source.id, [accessor])
        granted += 1

    for nexset in client.nexsets.list(project_id=project_id):
        client.nexsets.add_accessors(nexset.id, [accessor])
        granted += 1

    for dest in client.destinations.list(project_id=project_id):
        client.destinations.add_accessors(dest.id, [accessor])
        granted += 1

    return granted

# Usage
count = grant_team_to_project(client, project_id=789, team_id=123)
print(f"Granted access to {count} resources")
```

### Pattern 4: Revoke user access from all resources

```python
def revoke_user_access(client, email, resource_ids):
    """Revoke user access from multiple resources."""
    accessor = {"type": "USER", "email": email}
    results = {"success": [], "failed": []}

    for resource_type, ids in resource_ids.items():
        api = getattr(client, resource_type)
        for resource_id in ids:
            try:
                api.delete_accessors(resource_id, [accessor])
                results["success"].append(f"{resource_type}/{resource_id}")
            except Exception as e:
                results["failed"].append({"id": resource_id, "error": str(e)})

    return results

# Usage
result = revoke_user_access(client, "departed-user@company.com", {
    "sources": [123, 456],
    "nexsets": [789],
    "destinations": [101]
})
```

### Pattern 5: List all users with access to critical resources

```python
def audit_resource_access(client, resource_type, resource_id):
    """Get detailed access information for a resource."""
    api = getattr(client, resource_type)
    accessors = api.get_accessors(resource_id)

    return [
        {
            "type": acc.type.value if hasattr(acc.type, 'value') else acc.type,
            "identifier": getattr(acc, 'email', None) or getattr(acc, 'name', None) or acc.id,
            "roles": [r.value if hasattr(r, 'value') else r for r in acc.access_roles]
        }
        for acc in accessors
    ]

# Audit critical production source
access_list = audit_resource_access(client, "sources", production_source_id)
for accessor in access_list:
    print(f"{accessor['type']}: {accessor['identifier']} - {accessor['roles']}")
```

---

## Audit Trail

Track access changes using the audit log:

```python
def get_access_changes(client, resource_type, resource_id, days=30):
    """Get access-related changes from audit log."""
    api = getattr(client, resource_type)
    logs = api.get_audit_log(resource_id)

    access_keywords = ["accessor", "access", "permission", "share", "role"]
    changes = []

    for log in logs:
        action = log.get("action", "").lower()
        if any(kw in action for kw in access_keywords):
            changes.append({
                "action": log.get("action"),
                "user": log.get("user", {}).get("email"),
                "timestamp": log.get("created_at"),
                "details": log.get("details", {})
            })

    return sorted(changes, key=lambda x: x.get("timestamp", ""), reverse=True)

# Check access changes in last week
changes = get_access_changes(client, "sources", source_id, days=7)
print(f"Access changes: {len(changes)}")
for change in changes[:5]:
    print(f"  [{change['timestamp']}] {change['action']} by {change['user']}")
```

---

## Troubleshooting

### Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Forbidden` | Insufficient permissions | Verify you have admin/owner role |
| `404 Not Found` | Resource doesn't exist | Check resource_id |
| `400 Validation Error` | Invalid accessor format | Check accessor type and required fields |
| `409 Conflict` | Accessor already exists | Use replace_accessors or skip |

### Verify your access level

```python
# Check your access to a resource
resource = client.sources.get(source_id)
my_roles = resource.access_roles
print(f"My roles: {my_roles}")
```

### Debug accessor operations

```python
# Before operation
before = client.sources.get_accessors(source_id)
print(f"Before: {len(before)} accessors")

# Perform operation
client.sources.add_accessors(source_id, [new_accessor])

# After operation
after = client.sources.get_accessors(source_id)
print(f"After: {len(after)} accessors")
```

### Common mistakes

1. **Forgetting child resources**: Granting source access doesn't grant nexset access
2. **Using replace instead of add**: Replace removes all existing accessors
3. **Wrong identifier**: Use email for users, id for teams
4. **Role case sensitivity**: Use lowercase (`"operator"` not `"OPERATOR"`)
