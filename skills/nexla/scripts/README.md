# Nexla Production Scripts

Production-ready utilities for Nexla operations.

## Overview

This directory contains battle-tested scripts for deploying, monitoring, and managing Nexla data flows in production environments. All scripts support:

- Environment variables for authentication (`NEXLA_SERVICE_KEY`, `NEXLA_API_URL`)
- JSON configuration files for repeatable operations
- CLI arguments for customization
- Dry-run mode for testing (where applicable)
- Proper error handling and exit codes

## Scripts

### Validation

**`nexla_quickstart.py`** - Validate authentication and list resources

Quick validation script to verify your credentials and connectivity.

```bash
# Set environment variables first
export NEXLA_SERVICE_KEY="your-service-key"
export NEXLA_API_URL="https://dataops.nexla.io/nexla-api"

# Run validation
python scripts/nexla_quickstart.py
```

Expected output:
- Lists sources, nexsets, destinations, flows
- Prints counts and sample IDs
- Exits with 0 on success, 1 on failure

---

### Deployment

**`deploy_flow.py`** - Deploy flow with validation and rollback

Deploys a complete flow (credential → source → destination → activation) with automatic rollback on failure.

```bash
# Dry run first
python scripts/deploy_flow.py --config flow_config.json --dry-run

# Deploy
python scripts/deploy_flow.py --config flow_config.json

# Save results
python scripts/deploy_flow.py --config flow_config.json --output deployment_result.json
```

Config structure:
```json
{
  "credential_id": 123,
  "source": {
    "name": "production-data",
    "source_type": "s3",
    "data_credentials_id": 123,
    "source_config": {
      "path": "s3://bucket/data/",
      "file_format": "parquet"
    }
  },
  "destination": {
    "name": "warehouse-sink",
    "sink_type": "snowflake",
    "data_credentials_id": 456,
    "sink_config": {
      "database": "analytics",
      "schema": "raw",
      "table": "data"
    }
  }
}
```

Deployment steps:
1. Validate credential (probe)
2. Create source
3. Wait for nexset discovery
4. Create destination
5. Activate flow

On failure: Automatically rolls back (deletes created resources in reverse order)

---

**`batch_operations.py`** - Batch create/update/delete resources

Execute bulk operations on Nexla resources with idempotency checks.

```bash
# Batch create sources
python scripts/batch_operations.py \
  --operation create \
  --resource-type sources \
  --config sources_config.json

# Batch update destinations
python scripts/batch_operations.py \
  --operation update \
  --resource-type destinations \
  --config updates_config.json

# Batch delete resources
python scripts/batch_operations.py \
  --operation delete \
  --resource-type nexsets \
  --config delete_config.json \
  --output results.json
```

Config for CREATE:
```json
{
  "items": [
    {
      "name": "source-1",
      "source_type": "s3",
      "data_credentials_id": 123,
      "source_config": {"path": "s3://bucket/data1/"}
    },
    {
      "name": "source-2",
      "source_type": "s3",
      "data_credentials_id": 123,
      "source_config": {"path": "s3://bucket/data2/"}
    }
  ]
}
```

Config for UPDATE:
```json
{
  "items": [
    {"id": 456, "data": {"description": "Updated"}},
    {"id": 789, "data": {"tags": ["production"]}}
  ]
}
```

Config for DELETE:
```json
{
  "items": [123, 456, 789]
}
```

---

### Monitoring

**`health_check.py`** - Health check for flows with alerting

Monitor flow health and send alerts on issues.

```bash
# Run health check
python scripts/health_check.py --config monitoring_config.json

# With alerting
python scripts/health_check.py \
  --config monitoring_config.json \
  --alert-webhook https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Save results
python scripts/health_check.py \
  --config monitoring_config.json \
  --output health_results.json
```

Config structure:
```json
{
  "resources": [
    {"type": "data_sources", "id": 123},
    {"type": "data_sets", "id": 456},
    {"type": "data_sinks", "id": 789}
  ]
}
```

Health checks performed:
- Flow status (active/paused/failed)
- Last run timestamp (detects staleness)
- Error rate from last 10 runs
- Credential validity (for sources/destinations)

Exit codes:
- `0`: All resources healthy
- `1`: One or more unhealthy resources found

Schedule with cron:
```cron
# Run every 4 hours
0 */4 * * * python /path/to/scripts/health_check.py --config /path/to/monitoring_config.json --alert-webhook https://...
```

---

### Error Recovery Utilities

**`retry_helpers.py`** - Retry decorators and backoff utilities

Reusable retry patterns for handling transient failures.

**Decorators:**

1. **`exponential_backoff_retry`** - Exponential backoff with jitter
   ```python
   from scripts.retry_helpers import exponential_backoff_retry

   @exponential_backoff_retry(max_attempts=5, base_delay=1.0, max_delay=60.0)
   def create_source(client, config):
       return client.sources.create(config)
   ```

2. **`simple_retry`** - Fixed delay retry
   ```python
   from scripts.retry_helpers import simple_retry

   @simple_retry(max_attempts=3, delay=2.0)
   def get_source(client, source_id):
       return client.sources.get(source_id)
   ```

Features:
- Respects `retry_after` from `RateLimitError`
- Adds jitter to prevent thundering herd
- Handles `RateLimitError` and `ServerError` by default
- Customizable exception types

---

**`circuit_breaker.py`** - Circuit breaker implementation

Prevent cascading failures by failing fast after threshold.

**Usage:**

1. **CircuitBreaker class**
   ```python
   from scripts.circuit_breaker import CircuitBreaker

   breaker = CircuitBreaker(failure_threshold=5, timeout=60)

   def risky_operation():
       return client.sources.list()

   try:
       result = breaker.call(risky_operation)
   except Exception as e:
       print(f"Circuit breaker prevented call: {e}")
   ```

2. **Decorator pattern**
   ```python
   from scripts.circuit_breaker import circuit_breaker

   @circuit_breaker(failure_threshold=3, timeout=30)
   def get_metrics(client, resource_id):
       return client.metrics.get_resource_daily_metrics("data_sets", resource_id)
   ```

States:
- **CLOSED**: Normal operation
- **OPEN**: Failing fast (not executing calls)
- **HALF_OPEN**: Testing if service recovered

---

## Configuration Best Practices

### Environment Variables

Always set these before running scripts:

```bash
# Required: Authentication
export NEXLA_SERVICE_KEY="your-service-key-here"
# OR
export NEXLA_ACCESS_TOKEN="your-access-token-here"

# Optional: Custom Nexla instance
export NEXLA_API_URL="https://your-nexla-host/nexla-api"
```

### JSON Configuration Files

- Store in version control (excluding secrets)
- Use descriptive names: `prod_flow_config.json`, `staging_sources.json`
- Validate with `--dry-run` before executing

### Secrets Management

**DO NOT commit secrets:**
- Never commit credentials in config files
- Use credential IDs (integers) instead of raw credentials
- Store service keys in secure vaults (1Password, AWS Secrets Manager, etc.)
- Use environment variables or secure file paths

---

## Error Handling

All scripts implement:

1. **Exponential backoff retry** for transient failures (429, 5xx)
2. **Detailed error logging** with context
3. **Checkpointing** for long-running operations
4. **Rollback** on failure (where applicable)
5. **Exit codes**: 0 = success, 1 = failure

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy Nexla Flow

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install nexla-sdk

      - name: Deploy flow
        env:
          NEXLA_SERVICE_KEY: ${{ secrets.NEXLA_SERVICE_KEY }}
        run: |
          python scripts/deploy_flow.py \
            --config config/production_flow.json \
            --output deployment_result.json

      - name: Health check
        env:
          NEXLA_SERVICE_KEY: ${{ secrets.NEXLA_SERVICE_KEY }}
        run: |
          python scripts/health_check.py \
            --config config/monitoring.json \
            --alert-webhook ${{ secrets.SLACK_WEBHOOK }}
```

### Scheduled Monitoring (cron)

```bash
# Add to crontab (crontab -e)

# Health check every 4 hours
0 */4 * * * cd /path/to/nexla-sdk && python scripts/health_check.py --config config/monitoring.json --alert-webhook https://... >> /var/log/nexla_health.log 2>&1

# Daily validation
0 0 * * * cd /path/to/nexla-sdk && python scripts/nexla_quickstart.py >> /var/log/nexla_validation.log 2>&1
```

---

## Troubleshooting

### Common Issues

**Import Error: nexla_sdk not found**
```bash
pip install nexla-sdk
# or
pip install -e ".[dev]"  # if in SDK repository
```

**Authentication Error**
```bash
# Verify environment variables
echo $NEXLA_SERVICE_KEY
echo $NEXLA_API_URL

# Test with quickstart
python scripts/nexla_quickstart.py
```

**JSON Validation Error**
```bash
# Validate JSON syntax
python -m json.tool config/your_config.json

# Test with dry-run
python scripts/deploy_flow.py --config config/your_config.json --dry-run
```

**Permission Denied**
- Verify service key has necessary permissions
- Check resource access roles in Nexla UI
- Confirm organization/project scope

---

## Development

### Running Tests

```bash
# Syntax check
python -m py_compile scripts/*.py

# Run with test data
python scripts/deploy_flow.py --config test_config.json --dry-run
```

### Adding New Scripts

Follow these patterns:
1. Use argparse for CLI arguments
2. Support `--help` flag with examples
3. Implement error handling with try/except
4. Use proper exit codes (0 = success, 1 = failure)
5. Add logging/printing for progress
6. Document in this README

---

## Support

For issues or questions:
- Nexla SDK: https://github.com/nexla/nexla-sdk
- Nexla Docs: https://docs.nexla.com/
- Nexla Support: support@nexla.com
