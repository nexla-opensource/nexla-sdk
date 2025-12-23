# Reference: Nexla Data Flows

## Mental model (Nexla objects)
- Credentials: stored auth/config used by connectors to access external systems.
- Sources: connect to upstream systems and produce datasets (Nexla "nexsets").
- Nexsets (data sets): data products that can apply transforms and schemas.
- Destinations (data sinks): deliver data out to target systems.
- Flows: the orchestration graph connecting sources → nexsets → destinations.

See:
- https://docs.nexla.com/dev-guides/data-flows
- https://docs.nexla.com/
- https://nexla.com/

## REST vs SDK (decision guide)
- REST: language-agnostic automation, quick diagnostics, or when you must integrate with non-Python systems.
- Python SDK: repeatable workflows with typed models and convenience helpers; safer updates.

## Authentication & base URL
- The API supports token-based auth. Use either a service key (to obtain a session token) or a user access token. Verify the correct login/session endpoint in the API docs for your instance.
- Set Accept header to `application/vnd.nexla.v1+json` when calling the API.
- For the SDK, prefer env vars:
  - `NEXLA_SERVICE_KEY` (recommended) or `NEXLA_ACCESS_TOKEN`
  - `NEXLA_API_URL` to override base URL for a custom instance
  - You can also pass `base_url` to `NexlaClient(...)` directly.

## Core API pointers (verify connector-specific payloads)
Use the API reference for exact endpoints, required fields, and payload shapes:
- Sources: list/get/create/update data sources
- Nexsets (data_sets): list/get/create/update data sets and transforms
- Destinations (data_sinks): list/get/create/update data sinks
- Credentials (data_credentials): list/get/create/update credentials

Flow endpoints (documented):
- List flows: `GET /flows`
- Get flow by ID: `GET /flows/{flow_id}`
- Get flow by resource: `GET /{resource_type}/{resource_id}/flow`
- Activate/pause flow: `PUT /flows/{flow_id}/activate` or `PUT /flows/{flow_id}/pause`
- Delete flow by resource: `DELETE /{resource_type}/{resource_id}/flow`

Metrics endpoints (documented):
- Daily metrics: `GET /{resource_type}/{resource_id}/metrics?from=YYYY-MM-DD&aggregate=1`
- Metrics by run: `GET /{resource_type}/{resource_id}/metrics/run_summary`

Transforms endpoints (documented):
- List transforms: `GET /transforms`
- Create/update transforms: use the transforms API (verify payload in docs)

## Reliability guardrails
- Idempotency: search by name/tag before create; prefer update or copy when re-running.
- Safe re-runs: pause flows before structural changes; re-activate after validation.
- Change isolation: update a derived nexset (child) instead of editing the base dataset.
- Pagination: use `page`/`per_page` consistently for list endpoints; stop when empty.
- Retries: use exponential backoff for 429/5xx; respect `Retry-After` if present.

## Error handling deep dive

### Exception hierarchy
```
NexlaError (base)
├── AuthenticationError (401, token expired/invalid)
├── AuthorizationError (403, insufficient permissions)
├── NotFoundError (404, resource doesn't exist)
├── ValidationError (400, invalid request payload)
├── RateLimitError (429, quota exceeded, has retry_after)
├── ServerError (5xx, transient server issues)
├── ResourceConflictError (409, duplicate/state conflict)
├── CredentialError (credential validation failed)
├── FlowError (flow operation failed, has flow_step)
└── TransformError (transform execution failed)
```

### Retry strategies

**1. Automatic retries (built into SDK)**
- HTTP client retries: 3 attempts, 0.5s backoff factor
- Retryable status codes: 429, 502, 503, 504
- All HTTP methods supported (GET, POST, PUT, DELETE, PATCH)

**2. Application-level retries (implement in your code)**
```python
from nexla_sdk import RateLimitError, ServerError
import time
import random

def exponential_backoff_retry(func, max_attempts=5, base_delay=1, max_delay=60):
    """Retry with exponential backoff + jitter."""
    for attempt in range(max_attempts):
        try:
            return func()
        except RateLimitError as e:
            if attempt == max_attempts - 1:
                raise
            # Respect retry_after if available
            delay = e.retry_after if e.retry_after else base_delay * (2 ** attempt)
            delay = min(delay, max_delay)
            # Add jitter to prevent thundering herd
            jitter = random.uniform(0, delay * 0.1)
            time.sleep(delay + jitter)
        except ServerError as e:
            if attempt == max_attempts - 1:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, delay * 0.1)
            time.sleep(delay + jitter)
```

**3. Circuit breaker pattern**
```python
class CircuitBreaker:
    """Prevent cascading failures by failing fast after threshold."""
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.opened_at = None
        self.state = 'closed'  # closed, open, half-open

    def call(self, func):
        if self.state == 'open':
            if time.time() - self.opened_at > self.timeout:
                self.state = 'half-open'
            else:
                raise Exception("Circuit breaker open")

        try:
            result = func()
            if self.state == 'half-open':
                self.state = 'closed'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = 'open'
                self.opened_at = time.time()
            raise
```

### Timeout strategies
- **API calls**: Default 10s timeout (configurable via RequestsHttpClient)
- **Long-running operations**: Use async tasks API, poll for completion
- **Batch operations**: Implement checkpointing to resume from failure
- **Flow activation**: Poll flow status, timeout after N seconds

### Error context extraction
All NexlaError exceptions provide:
```python
try:
    client.sources.create(invalid_data)
except NexlaError as e:
    print(e.get_error_summary())  # Returns structured dict:
    # {
    #   "message": "...",
    #   "step": "create_source",
    #   "operation": "create_resource",
    #   "resource_type": "sources",
    #   "resource_id": "123",
    #   "details": {...},
    #   "context": {...},
    #   "status_code": 400,
    #   "response": {...},
    #   "original_error": "..."
    # }
```

## Advanced workflows

### Credential rotation
```python
def rotate_credential(client, old_cred_id, new_cred_config):
    """Safely rotate a credential across all dependent resources."""
    # 1. Create new credential
    new_cred = client.credentials.create(new_cred_config)

    # 2. Probe to validate
    probe_result = client.credentials.probe(new_cred.id)
    if probe_result.get('status') != 'success':
        client.credentials.delete(new_cred.id)
        raise CredentialError("New credential probe failed")

    # 3. Find all resources using old credential
    sources = [s for s in client.sources.list() if s.data_credentials_id == old_cred_id]
    destinations = [d for d in client.destinations.list() if d.data_credentials_id == old_cred_id]

    # 4. Pause affected flows
    flow_ids = []
    for source in sources:
        flow = client.flows.get_by_resource("data_sources", source.id)
        for node in flow.flows:
            client.flows.pause(node.id)
            flow_ids.append(node.id)

    # 5. Update resources (sources and destinations)
    for source in sources:
        client.sources.update(source.id, {"data_credentials_id": new_cred.id})
    for dest in destinations:
        client.destinations.update(dest.id, {"data_credentials_id": new_cred.id})

    # 6. Reactivate flows
    for flow_id in flow_ids:
        client.flows.activate(flow_id)

    # 7. Monitor first run with new credential
    time.sleep(60)  # Wait for first run
    # Check metrics to ensure success

    # 8. Delete old credential
    client.credentials.delete(old_cred_id)
```

### Schema migration
```python
def migrate_schema(client, nexset_id, new_schema):
    """Migrate nexset to new schema with zero downtime."""
    # 1. Get current nexset
    current = client.nexsets.get(nexset_id)

    # 2. Create child nexset with new schema
    child = client.nexsets.create({
        "name": f"{current.name}_v2",
        "parent_data_set_id": current.id,
        "has_custom_schema": True,
        "schema": new_schema
    })

    # 3. Test on samples
    samples = client.nexsets.get_samples(child.id, count=100)
    # Validate samples match expected schema

    # 4. Find all destinations using old nexset
    destinations = [d for d in client.destinations.list() if d.data_set_id == nexset_id]

    # 5. Create parallel destinations for new nexset
    new_destinations = []
    for dest in destinations:
        new_dest = client.destinations.create({
            "name": f"{dest.name}_v2",
            "sink_type": dest.sink_type,
            "data_set_id": child.id,
            "data_credentials_id": dest.data_credentials_id,
            "sink_config": dest.sink_config
        })
        new_destinations.append(new_dest)

    # 6. Activate new flows
    for dest in new_destinations:
        client.destinations.activate(dest.id)

    # 7. Monitor both versions in parallel
    # Compare metrics, validate data quality

    # 8. After validation period, deactivate old flows
    for dest in destinations:
        client.destinations.pause(dest.id)
```

### Access control patterns
```python
# Grant team access to resource
client.sources.add_accessors(source_id, [
    {"type": "TEAM", "team_id": 123, "access_roles": ["collaborator"]},
    {"type": "USER", "email": "user@example.com", "access_roles": ["operator"]}
])

# Replace all accessors (reset to owner-only + new list)
client.sources.replace_accessors(source_id, [
    {"type": "USER", "email": "admin@example.com", "access_roles": ["owner"]}
])

# Remove specific accessor
client.sources.delete_accessors(source_id, [
    {"type": "USER", "email": "old-user@example.com"}
])

# Batch update accessors across multiple resources
def grant_team_access_to_project(client, project_id, team_id):
    """Grant team access to all resources in a project."""
    resources = {
        'sources': client.sources.list(project_id=project_id),
        'nexsets': client.nexsets.list(project_id=project_id),
        'destinations': client.destinations.list(project_id=project_id)
    }

    accessor = {"type": "TEAM", "team_id": team_id, "access_roles": ["collaborator"]}

    for resource_type, items in resources.items():
        for item in items:
            getattr(client, resource_type).add_accessors(item.id, [accessor])
```

### Async task polling pattern
```python
def poll_async_task(client, task_id, max_wait=300, poll_interval=5):
    """Poll async task until completion or timeout."""
    start_time = time.time()
    while True:
        task = client.async_tasks.get(task_id)

        if task.status in ['completed', 'success']:
            return client.async_tasks.result(task_id)
        elif task.status in ['failed', 'error']:
            raise NexlaError(f"Task failed: {task.error_message}")

        if time.time() - start_time > max_wait:
            raise TimeoutError(f"Task {task_id} did not complete in {max_wait}s")

        time.sleep(poll_interval)
```

## Monitoring & observability

### Health check patterns
```python
def check_flow_health(client, resource_type, resource_id):
    """Comprehensive health check for a flow."""
    health = {
        "resource_id": resource_id,
        "resource_type": resource_type,
        "status": "unknown",
        "last_run": None,
        "error_rate": 0.0,
        "issues": []
    }

    # 1. Get flow status
    flow = client.flows.get_by_resource(resource_type, resource_id)
    if not flow.flows:
        health["status"] = "no_flow"
        health["issues"].append("No flow found for resource")
        return health

    flow_node = flow.flows[0]
    health["status"] = flow_node.status

    # 2. Check last run timestamp
    metrics = client.metrics.get_resource_metrics_by_run(
        resource_type=resource_type,
        resource_id=resource_id,
        orderby="runId",
        page=1,
        size=1
    )

    if metrics.metrics:
        last_run = metrics.metrics[0]
        health["last_run"] = last_run.get("lastWritten")

        # Check if stale (no run in last 24h)
        if last_run.get("lastWritten"):
            from dateutil import parser
            last_run_time = parser.parse(last_run["lastWritten"])
            age_hours = (datetime.utcnow() - last_run_time.replace(tzinfo=None)).total_seconds() / 3600
            if age_hours > 24:
                health["issues"].append("No run in last 24 hours")

    # 3. Calculate error rate (last 10 runs)
    recent_runs = client.metrics.get_resource_metrics_by_run(
        resource_type=resource_type,
        resource_id=resource_id,
        orderby="runId",
        page=1,
        size=10
    )

    if recent_runs.metrics:
        failed = sum(1 for r in recent_runs.metrics if r.get("status") == "FAILED")
        health["error_rate"] = failed / len(recent_runs.metrics)

        if health["error_rate"] > 0.2:  # > 20% failure rate
            health["issues"].append(f"High error rate: {health['error_rate']:.1%}")

    # 4. Check credential validity (if applicable)
    if resource_type == "data_sources":
        source = client.sources.get(resource_id)
        if source.data_credentials_id:
            try:
                probe = client.credentials.probe(source.data_credentials_id)
                if probe.get("status") != "success":
                    health["issues"].append("Credential probe failed")
            except Exception as e:
                health["issues"].append(f"Credential check error: {e}")

    return health
```

### Metrics interpretation
- **Daily metrics**: `get_resource_daily_metrics()` → aggregate records/errors per day
- **Run metrics**: `get_resource_metrics_by_run()` → per-run details (runId, records, errors, duration)
- **Flow logs**: `get_flow_logs()` → detailed execution logs for debugging

### SLA tracking
```python
def track_sla(client, resource_id, sla_config):
    """Track SLA compliance for a resource."""
    # sla_config: {"max_latency_s": 300, "min_success_rate": 0.95, "max_age_hours": 24}

    metrics = client.metrics.get_resource_metrics_by_run(
        resource_type="data_sets",
        resource_id=resource_id,
        orderby="runId",
        page=1,
        size=100
    )

    violations = []

    for run in metrics.metrics:
        # Check latency
        if run.get("duration_s", 0) > sla_config["max_latency_s"]:
            violations.append(f"Run {run['runId']}: latency {run['duration_s']}s exceeds SLA")

        # Check success rate
        if run.get("status") != "SUCCESS":
            violations.append(f"Run {run['runId']}: failed")

    success_rate = sum(1 for r in metrics.metrics if r.get("status") == "SUCCESS") / len(metrics.metrics)
    if success_rate < sla_config["min_success_rate"]:
        violations.append(f"Success rate {success_rate:.1%} below SLA {sla_config['min_success_rate']:.1%}")

    return violations
```

## Troubleshooting runbook

### Step-by-step debugging process

**Step 1: Identify failure point**
```bash
# Check flow status
curl -H "Authorization: Bearer $TOKEN" \
     "$API_URL/flows/{flow_id}"

# Or with SDK
flow = client.flows.get(flow_id)
print(f"Status: {flow.flows[0].status}")
```

**Step 2: Get recent run metrics**
```python
metrics = client.metrics.get_resource_metrics_by_run(
    resource_type="data_sets",
    resource_id=nexset_id,
    orderby="runId",
    page=1,
    size=10
)

# Find failed runs
failed_runs = [r for r in metrics.metrics if r.get("status") == "FAILED"]
if failed_runs:
    print(f"Failed runs: {[r['runId'] for r in failed_runs]}")
```

**Step 3: Analyze logs for failed run**
```python
if failed_runs:
    run_id = failed_runs[0]["runId"]
    from_ts = failed_runs[0]["startTime"]
    to_ts = failed_runs[0]["endTime"]

    logs = client.metrics.get_flow_logs(
        resource_type="data_sets",
        resource_id=nexset_id,
        run_id=run_id,
        from_ts=from_ts,
        to_ts=to_ts
    )

    # Search for error patterns
    for log in logs:
        if "error" in log.get("message", "").lower():
            print(f"[{log['timestamp']}] {log['message']}")
```

**Step 4: Compare with successful run**
```python
successful_runs = [r for r in metrics.metrics if r.get("status") == "SUCCESS"]
if successful_runs and failed_runs:
    success = successful_runs[0]
    failure = failed_runs[0]

    print("Differences:")
    print(f"  Records: {success.get('records')} vs {failure.get('records')}")
    print(f"  Duration: {success.get('duration_s')}s vs {failure.get('duration_s')}s")
    print(f"  Error count: {success.get('errors', 0)} vs {failure.get('errors', 0)}")
```

**Step 5: Check dependencies**
```python
# For a nexset, check parent source
nexset = client.nexsets.get(nexset_id)
if nexset.data_source_id:
    source = client.sources.get(nexset.data_source_id)
    print(f"Source status: {source.status}")

    # Check source credential
    if source.data_credentials_id:
        try:
            probe = client.credentials.probe(source.data_credentials_id)
            print(f"Credential probe: {probe.get('status')}")
        except CredentialError as e:
            print(f"Credential issue: {e}")
```

**Step 6: Validate resource configuration**
```python
# Check for common misconfigurations
if nexset.has_custom_transform and nexset.transform_id:
    transform = client.transforms.get(nexset.transform_id)
    print(f"Transform: {transform.name}, status: {transform.status}")

    # Test transform on samples
    samples = client.nexsets.get_samples(nexset.parent_data_set_id, count=5)
    # Validate transform logic against samples
```

**Step 7: Implement fix and verify**
```python
# Pause flow
client.flows.pause(flow_id)

# Apply fix (e.g., update transform, rotate credential, fix config)
# ...

# Reactivate flow
client.flows.activate(flow_id)

# Monitor next run
time.sleep(300)  # Wait for next scheduled run
new_metrics = client.metrics.get_resource_metrics_by_run(
    resource_type="data_sets",
    resource_id=nexset_id,
    orderby="runId",
    page=1,
    size=1
)

if new_metrics.metrics and new_metrics.metrics[0].get("status") == "SUCCESS":
    print("Fix verified!")
else:
    print("Issue persists, escalate or investigate further")
```

### Common issues and solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Credential expired** | 401/403 errors, probe fails | Rotate credential using rotation workflow |
| **Transform error** | Failed runs, errors in logs | Test transform on samples, fix logic, update |
| **Schema mismatch** | Validation errors, parse failures | Migrate schema using schema migration workflow |
| **Rate limiting** | 429 errors, throttled requests | Implement exponential backoff, reduce request rate |
| **Network timeouts** | Connection errors, partial data | Increase timeout, check network connectivity |
| **Resource conflict** | 409 errors, duplicate names | Search before create, use unique names/tags |
| **Flow not running** | No recent runs, stale data | Check source schedule, activate flow, verify upstream |
| **High error rate** | >20% failed runs | Check logs, validate inputs, test incrementally |
| **Stale data** | No updates in 24h+ | Check source polling, upstream availability |
| **Permission denied** | 403 on operations | Verify access roles, request permissions |
