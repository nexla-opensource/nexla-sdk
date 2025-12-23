# Examples & Recipes

## Templates

### .env template (do not commit secrets)
```
NEXLA_SERVICE_KEY=your-service-key-here
# Or use an access token instead:
# NEXLA_ACCESS_TOKEN=your-access-token-here

# Optional: override for custom Nexla instances
NEXLA_API_URL=https://your-nexla-host/nexla-api
```

### Minimal Python (auth + list resources)
```python
from nexla_sdk import NexlaClient

client = NexlaClient()

sources = client.sources.list(page=1, per_page=20)
nexsets = client.nexsets.list(page=1, per_page=20)
destinations = client.destinations.list(page=1, per_page=20)
flows = client.flows.list(flows_only=True)

print(f"sources={len(sources)} nexsets={len(nexsets)} destinations={len(destinations)} flows={len(flows)}")
```

### Script quick commands
```bash
# List resources by type/name
python scripts/list_resources.py --type sources --name "orders" --limit 5

# Print deploy_flow config schema
python scripts/deploy_flow.py --print-schema

# Fetch logs for latest run
python scripts/get_resource_logs.py --resource-type data_sets --resource-id 123
```

### Create flow skeleton (destination → flow activation)
```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.destinations.requests import DestinationCreate

client = NexlaClient()

sink = client.destinations.create(
    DestinationCreate(
        name="my-destination",
        sink_type="<sink_type>",
        data_credentials_id=<data_credentials_id>,
        data_set_id=<nexset_id>,
        sink_config={"<connector_field>": "<value>"},
    )
)

flow = client.flows.get_by_resource("data_sinks", sink.id, flows_only=True)
flow_id = next((n.id for n in flow.flows if n.data_sink_id == sink.id), None)
if flow_id is None:
    raise RuntimeError("No flow node found for sink; verify flow creation in Nexla UI or API")

client.flows.activate(flow_id)
```

## Error Handling Pattern

**Apply this pattern to all recipes for production resilience:**

```python
from nexla_sdk import RateLimitError, ServerError, NexlaError
import time
import random

def with_retry(func, max_attempts=3):
    """Wrapper to add exponential backoff retry to any operation."""
    for attempt in range(max_attempts):
        try:
            return func()
        except (RateLimitError, ServerError) as e:
            if attempt == max_attempts - 1:
                raise
            # Exponential backoff with jitter
            delay = min(2 ** attempt, 60)
            jitter = random.uniform(0, delay * 0.1)
            print(f"Retry {attempt + 1}/{max_attempts} after {delay + jitter:.1f}s...")
            time.sleep(delay + jitter)
        except NexlaError as e:
            print(f"Nexla error: {e.get_error_summary()}")
            raise

# Usage example:
result = with_retry(lambda: client.sources.create(config))
```

Or use the retry helpers from `scripts/retry_helpers.py`:

```python
from scripts.retry_helpers import exponential_backoff_retry

@exponential_backoff_retry(max_attempts=5)
def create_source_safe(client, config):
    return client.sources.create(config)

source = create_source_safe(client, source_config)
```

## Recipe 1: List and inspect existing resources

**Preconditions**
- `NEXLA_SERVICE_KEY` or `NEXLA_ACCESS_TOKEN` set.
- `NEXLA_API_URL` set if using a non-default instance.

**Steps**
1) List sources, nexsets, and destinations with pagination.
2) List flows in lightweight mode (flows_only).
3) Inspect a specific resource by ID if needed.

**Example commands (Python SDK)**
```python
from nexla_sdk import NexlaClient

client = NexlaClient()

sources = client.sources.list(page=1, per_page=50)
nexsets = client.nexsets.list(page=1, per_page=50)
destinations = client.destinations.list(page=1, per_page=50)
flows = client.flows.list(flows_only=True)

print([s.id for s in sources][:5])
print([n.id for n in nexsets][:5])
print([d.id for d in destinations][:5])
print([f.id for f in flows[0].flows][:5] if flows else [])
```

**Example commands (cURL)**
```bash
curl -sS \
  -H "Authorization: Bearer $NEXLA_ACCESS_TOKEN" \
  -H "Accept: application/vnd.nexla.v1+json" \
  "$NEXLA_API_URL/flows?flows_only=1"
```

**Verification**
- You see non-empty lists or expected empty lists (e.g., new org).
- Flow nodes include the expected `data_source_id`, `data_set_id`, or `data_sink_id`.

**Common failure modes + fixes**
- 401/403: invalid token or missing role → re-auth or request access.
- 404 on base URL: wrong `NEXLA_API_URL` → verify instance URL.
- Empty lists when you expect data → check org/project scope and access roles.

## Recipe 2: Create a new source and discover nexsets

**Preconditions**
- You have connector-specific credential details.
- Know the `source_type` for the connector.

**Steps**
1) Create a credential (if needed).
2) Create a source using that credential.
3) Poll the source and check `data_sets` for discovered nexsets.

**Example commands (Python SDK)**
```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.credentials.requests import CredentialCreate
from nexla_sdk.models.sources.requests import SourceCreate

client = NexlaClient()

cred = client.credentials.create(
    CredentialCreate(
        name="my-connector-cred",
        credentials_type="<credentials_type>",
        credentials={"<connector_field>": "<value>"},
    )
)

source = client.sources.create(
    SourceCreate(
        name="my-source",
        source_type="<source_type>",
        data_credentials_id=cred.id,
        source_config={"<connector_field>": "<value>"},
    )
)

# Discovery can be async; re-fetch until data_sets is populated
source = client.sources.get(source.id, expand=True)
print(source.data_sets)
```

**Verification**
- `source.data_sets` contains at least one entry.
- The discovered nexset IDs appear in `client.nexsets.list()`.

**Common failure modes + fixes**
- Credential errors → re-check connector fields and re-run probe (if supported).
- No datasets discovered → verify connector path/config and wait for discovery to finish.
- Validation errors → check required fields for the connector in docs.

## Recipe 3: Create/modify a nexset transform pipeline

**Preconditions**
- You have a base nexset ID (parent data set).
- You have or plan to create a reusable transform.

**Steps**
1) List existing transforms to reuse (optional).
2) Create a child nexset with a transform, or update an existing nexset.
3) Validate output with samples before activation.

**Example commands (Python SDK)**
```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.nexsets.requests import NexsetCreate, NexsetUpdate

client = NexlaClient()

# Option A: attach an existing transform by ID
child = client.nexsets.create(
    NexsetCreate(
        name="my-transformed-nexset",
        parent_data_set_id=<parent_nexset_id>,
        has_custom_transform=True,
        transform_id=<transform_id>,
        description="Derived with reusable transform",
    )
)

# Option B: update an existing nexset to point to a transform
updated = client.nexsets.update(
    <nexset_id>,
    NexsetUpdate(
        has_custom_transform=True,
        transform_id=<transform_id>,
    )
)

samples = client.nexsets.get_samples(child.id, count=5, include_metadata=True)
print(samples)
```

**Verification**
- Samples return expected fields and data types.
- Nexset status is ACTIVE after activation (if required by your org settings).

**Common failure modes + fixes**
- Transform errors → verify transform code/schema in docs and test on samples.
- Schema mismatch → update transform or enable schema validation carefully.
- Parent dataset missing → confirm `parent_data_set_id` and access rights.

## Recipe 4: Create a destination and wire it to a nexset

**Preconditions**
- You have destination connector details and a valid credential.
- You know the target nexset ID.

**Steps**
1) Create the destination with `data_set_id` set to the target nexset.
2) Retrieve the flow for the destination resource.
3) Activate the flow node.

**Example commands (Python SDK)**
```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.destinations.requests import DestinationCreate

client = NexlaClient()

sink = client.destinations.create(
    DestinationCreate(
        name="my-destination",
        sink_type="<sink_type>",
        data_credentials_id=<data_credentials_id>,
        data_set_id=<nexset_id>,
        sink_config={"<connector_field>": "<value>"},
    )
)

flow = client.flows.get_by_resource("data_sinks", sink.id, flows_only=True)
flow_id = next((n.id for n in flow.flows if n.data_sink_id == sink.id), None)
if flow_id:
    client.flows.activate(flow_id)
```

**Example commands (cURL)**
```bash
curl -sS \
  -H "Authorization: Bearer $NEXLA_ACCESS_TOKEN" \
  -H "Accept: application/vnd.nexla.v1+json" \
  "$NEXLA_API_URL/data_sinks/<sink_id>/flow"
```

**Verification**
- Flow lookup returns a node for the destination.
- Flow node status becomes ACTIVE after activation.

**Common failure modes + fixes**
- Destination config invalid → verify connector-specific fields.
- Flow not found → check whether destination creation completed; verify access.
- Activation fails → confirm upstream source/nexset are active and reachable.

## Recipe 5: Operate & monitor (activate, status, metrics)

**Preconditions**
- Flow exists and you have the relevant resource ID (source/nexset/destination).

**Steps**
1) Activate or pause a flow node.
2) Fetch daily metrics and run-level summaries.
3) Apply backoff and retries on transient errors.

**Example commands (Python SDK)**
```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.metrics.enums import ResourceType

client = NexlaClient()

client.flows.pause(<flow_id>)
client.flows.activate(<flow_id>)

metrics = client.metrics.get_resource_daily_metrics(
    resource_type=ResourceType.DATA_SETS,
    resource_id=<nexset_id>,
    from_date="2025-12-01",
)

run_summary = client.metrics.get_resource_metrics_by_run(
    resource_type=ResourceType.DATA_SETS,
    resource_id=<nexset_id>,
    groupby="runId",
    orderby="runId",
    page=1,
    size=20,
)
```

**Example commands (cURL)**
```bash
curl -sS \
  -H "Authorization: Bearer $NEXLA_ACCESS_TOKEN" \
  -H "Accept: application/vnd.nexla.v1+json" \
  "$NEXLA_API_URL/data_sets/<nexset_id>/metrics?from=2025-12-01&aggregate=1"
```

**Verification**
- Metrics show new runs and non-zero records after activation.
- Errors are visible in run summaries if a failure occurred.

**Common failure modes + fixes**
- 429 rate limit → implement exponential backoff and respect `Retry-After`.
- 5xx server errors → retry with jitter; check Nexla status.
- No recent runs → verify schedule/polling on the source and flow activation.

## Recipe 6: Batch create sources from configuration

**Preconditions**
- JSON configuration file with multiple source definitions.
- Credentials already created.

**Steps**
1) Load configuration from JSON file.
2) For each source, check if it already exists (idempotency).
3) Create sources with error handling.
4) Return results summary (created, skipped, failed).

**Example commands (Python SDK)**
```python
from nexla_sdk import NexlaClient
from nexla_sdk.models.sources.requests import SourceCreate
import json

def batch_create_sources(client, config_file):
    """Create multiple sources from JSON config with error handling."""
    with open(config_file) as f:
        configs = json.load(f)

    results = {"created": [], "skipped": [], "failed": []}

    for cfg in configs["sources"]:
        try:
            # Idempotency: check if source already exists
            existing = [s for s in client.sources.list() if s.name == cfg["name"]]
            if existing:
                print(f"Source {cfg['name']} already exists, skipping")
                results["skipped"].append(existing[0].id)
                continue

            # Create source
            source = client.sources.create(SourceCreate(**cfg))
            results["created"].append(source.id)
            print(f"Created source {cfg['name']} (ID: {source.id})")

        except Exception as e:
            results["failed"].append({"name": cfg["name"], "error": str(e)})
            print(f"Failed to create {cfg['name']}: {e}")

    return results

# Example config file structure
config = {
    "sources": [
        {
            "name": "orders-prod",
            "source_type": "s3",
            "data_credentials_id": 123,
            "source_config": {"path": "orders/", "file_format": "json"}
        },
        {
            "name": "customers-prod",
            "source_type": "s3",
            "data_credentials_id": 123,
            "source_config": {"path": "customers/", "file_format": "parquet"}
        }
    ]
}

client = NexlaClient()
results = batch_create_sources(client, "sources.json")
print(f"Created: {len(results['created'])}, Failed: {len(results['failed'])}")
```

**Verification**
- Check that created sources appear in `client.sources.list()`.
- Verify skipped sources were not duplicated.
- Review failed entries for errors.

**Common failure modes + fixes**
- Duplicate names → idempotency check prevents duplicates.
- Invalid credentials → validate credential_id before batch operation.
- Partial failures → results dict tracks successes and failures independently.

## Recipe 7: CI/CD deployment with validation and rollback

**Preconditions**
- Flow configuration JSON file.
- Credentials validated.

**Steps**
1) Validate credential (probe).
2) Create source.
3) Create destination.
4) Activate flow.
5) Verify first run.
6) Rollback on failure (delete created resources in reverse order).

**Example commands (Python SDK)**
```python
def deploy_flow(client, config, dry_run=False):
    """Deploy flow with validation and rollback on failure."""
    steps = []
    rollback_ids = []

    try:
        # Step 1: Validate credential
        print("[1/5] Validating credential...")
        probe = client.credentials.probe(config["credential_id"])
        if probe.get("status") != "success":
            raise CredentialError("Credential probe failed")
        steps.append("credential_validated")

        if dry_run:
            print("DRY RUN: Would create source/destination/flow")
            return {"status": "dry_run_success", "steps": steps}

        # Step 2: Create source
        print("[2/5] Creating source...")
        source = client.sources.create(config["source"])
        rollback_ids.append(("source", source.id))
        steps.append(f"source_created:{source.id}")

        # Step 3: Create destination
        print("[3/5] Creating destination...")
        destination = client.destinations.create(config["destination"])
        rollback_ids.append(("destination", destination.id))
        steps.append(f"destination_created:{destination.id}")

        # Step 4: Activate flow
        print("[4/5] Activating flow...")
        flow = client.flows.get_by_resource("data_sinks", destination.id)
        client.flows.activate(flow.flows[0].id)
        steps.append("flow_activated")

        # Step 5: Verify first run
        print("[5/5] Verifying deployment...")
        time.sleep(60)
        metrics = client.metrics.get_resource_metrics_by_run(
            resource_type="data_sinks",
            resource_id=destination.id,
            page=1,
            size=1
        )
        if metrics.metrics and metrics.metrics[0].get("status") == "SUCCESS":
            steps.append("verified")
            print("Deployment successful!")
            return {"status": "success", "steps": steps}
        else:
            raise FlowError("First run verification failed")

    except Exception as e:
        print(f"Deployment failed: {e}")
        print("Rolling back...")

        # Rollback in reverse order
        for resource_type, resource_id in reversed(rollback_ids):
            try:
                if resource_type == "source":
                    client.sources.delete(resource_id)
                elif resource_type == "destination":
                    client.destinations.delete(resource_id)
                print(f"Deleted {resource_type} {resource_id}")
            except Exception as rollback_error:
                print(f"Rollback error: {rollback_error}")

        return {"status": "failed", "error": str(e), "steps": steps}

# Usage
result = deploy_flow(client, flow_config, dry_run=True)  # Test first
result = deploy_flow(client, flow_config)  # Deploy
```

**Verification**
- Dry-run completes successfully.
- All steps complete without errors.
- First run succeeds with expected data.

**Common failure modes + fixes**
- Credential validation fails → fix credential before deployment.
- Discovery timeout → increase wait time or check source configuration.
- Rollback fails → manual cleanup may be required.

## Recipe 8: Scheduled health check with alerting

**Preconditions**
- Monitoring configuration with resource list.
- Alert webhook URL (Slack, email, etc.).

**Steps**
1) Load resources to monitor from configuration.
2) Run health check on each resource.
3) Collect unhealthy resources.
4) Send alert if issues found.

**Example commands (Python SDK)**
```python
def scheduled_health_check(client, resources_to_monitor, alert_webhook=None):
    """Run health check on multiple resources and send alerts."""
    unhealthy = []

    for resource in resources_to_monitor:
        health = check_flow_health(client, resource["type"], resource["id"])

        if health["issues"]:
            unhealthy.append({
                "resource_id": resource["id"],
                "resource_type": resource["type"],
                "issues": health["issues"],
                "status": health["status"]
            })

    # Send alert if issues found
    if unhealthy and alert_webhook:
        import requests
        alert_message = {
            "text": f"Nexla Health Alert: {len(unhealthy)} resources unhealthy",
            "unhealthy_resources": unhealthy
        }
        requests.post(alert_webhook, json=alert_message)

    return unhealthy

# Schedule with cron or systemd timer
# 0 */4 * * * python health_check.py
```

**Verification**
- All healthy resources pass checks.
- Unhealthy resources trigger alerts.
- Alert webhook receives notifications.

**Common failure modes + fixes**
- False positives → adjust staleness/error rate thresholds.
- Webhook failures → verify webhook URL and network connectivity.
- Missing metrics → ensure flows have run at least once.

## Recipe 9: Credential rotation across environment

**Preconditions**
- Resources tagged by environment (dev/staging/prod).
- New credential configurations.

**Steps**
1) Discover resources by environment tag.
2) Build rotation plan.
3) Execute rotation with checkpointing.
4) Resume from checkpoint on failure.

**Example commands (Python SDK)**
```python
def rotate_credentials_for_environment(client, environment, new_creds_config):
    """Rotate all credentials for an environment (dev/staging/prod)."""
    # Tag-based resource discovery
    resources = {
        "sources": client.sources.list(),
        "destinations": client.destinations.list()
    }

    # Filter by environment tag
    env_resources = {
        "sources": [s for s in resources["sources"] if environment in s.tags],
        "destinations": [d for d in resources["destinations"] if environment in d.tags]
    }

    rotation_plan = []
    for source in env_resources["sources"]:
        rotation_plan.append({
            "type": "source",
            "id": source.id,
            "old_cred": source.data_credentials_id,
            "new_cred": new_creds_config[source.source_type]
        })

    # Execute rotation with checkpointing
    checkpoint_file = f"rotation_checkpoint_{environment}.json"
    completed = []

    for item in rotation_plan:
        try:
            rotate_credential(client, item["old_cred"], item["new_cred"])
            completed.append(item["id"])

            # Save checkpoint
            with open(checkpoint_file, 'w') as f:
                json.dump(completed, f)

        except Exception as e:
            print(f"Rotation failed for {item['type']} {item['id']}: {e}")
            print(f"Resume from checkpoint: {checkpoint_file}")
            raise
```

**Verification**
- All resources updated with new credentials.
- Flows continue running with new credentials.
- Checkpoint file created for resumability.

**Common failure modes + fixes**
- Partial completion → resume from checkpoint file.
- Invalid new credentials → validate with probe before rotation.
- Flow downtime → acceptable brief pause during rotation.

## Recipe 10: Compare environments (dev vs prod)

**Preconditions**
- Resources tagged by environment.
- Access to both environments.

**Steps**
1) Get snapshots of both environments.
2) Compare resources by name.
3) Find differences in configuration.
4) Generate drift report.

**Example commands (Python SDK)**
```python
def compare_environments(client, env1_tag, env2_tag):
    """Compare resource configurations between two environments."""
    def get_env_snapshot(tag):
        return {
            "sources": [s for s in client.sources.list() if tag in s.tags],
            "destinations": [d for d in client.destinations.list() if tag in d.tags],
            "flows": client.flows.list()
        }

    env1 = get_env_snapshot(env1_tag)
    env2 = get_env_snapshot(env2_tag)

    diff = {
        "sources": {
            "only_in_env1": [],
            "only_in_env2": [],
            "config_differences": []
        },
        "destinations": {
            "only_in_env1": [],
            "only_in_env2": [],
            "config_differences": []
        }
    }

    # Compare sources by name
    env1_source_names = {s.name for s in env1["sources"]}
    env2_source_names = {s.name for s in env2["sources"]}

    diff["sources"]["only_in_env1"] = list(env1_source_names - env2_source_names)
    diff["sources"]["only_in_env2"] = list(env2_source_names - env1_source_names)

    # Find config differences for common sources
    common_sources = env1_source_names & env2_source_names
    for name in common_sources:
        s1 = next(s for s in env1["sources"] if s.name == name)
        s2 = next(s for s in env2["sources"] if s.name == name)

        if s1.source_config != s2.source_config:
            diff["sources"]["config_differences"].append({
                "name": name,
                "env1_config": s1.source_config,
                "env2_config": s2.source_config
            })

    return diff

# Usage
drift = compare_environments(client, "dev", "prod")
print(json.dumps(drift, indent=2))
```

**Verification**
- Drift report shows expected differences.
- No unexpected configuration drift.
- Common resources have similar configurations.

**Common failure modes + fixes**
- Tag inconsistencies → standardize tagging strategy.
- Config format differences → normalize before comparison.
- Missing resources → verify environment completeness.
