#!/usr/bin/env python3
"""Health check script for Nexla flows with alerting."""

import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Any

try:
    from nexla_sdk import NexlaClient
except ImportError:
    print("Error: nexla_sdk not installed. Run: pip install nexla-sdk", file=sys.stderr)
    sys.exit(1)


def check_flow_health(
    client: NexlaClient, resource_type: str, resource_id: int, error_threshold: float = 0.2
) -> Dict[str, Any]:
    """
    Comprehensive health check for a flow.

    Args:
        client: NexlaClient instance
        resource_type: Resource type (e.g., "data_sources", "data_sets", "data_sinks")
        resource_id: Resource ID
        error_threshold: Error rate threshold for flagging issues (default: 0.2 = 20%)

    Returns:
        Health status dict with issues list
    """
    health = {
        "resource_id": resource_id,
        "resource_type": resource_type,
        "status": "unknown",
        "last_run": None,
        "error_rate": 0.0,
        "issues": [],
        "checked_at": datetime.utcnow().isoformat(),
    }

    try:
        # Get flow status
        flow = client.flows.get_by_resource(resource_type, resource_id)
        if not flow.flows:
            health["status"] = "no_flow"
            health["issues"].append("No flow found for resource")
            return health

        flow_node = flow.flows[0]
        health["status"] = flow_node.status

        # Check recent runs
        try:
            metrics = client.metrics.get_resource_metrics_by_run(
                resource_type=resource_type,
                resource_id=resource_id,
                orderby="runId",
                page=1,
                size=10,
            )

            if metrics.metrics:
                # Get last run timestamp
                last_run = metrics.metrics[0]
                health["last_run"] = last_run.get("lastWritten")

                # Calculate error rate from last 10 runs
                failed = sum(1 for r in metrics.metrics if r.get("status") == "FAILED")
                health["error_rate"] = failed / len(metrics.metrics)

                if health["error_rate"] > error_threshold:
                    health["issues"].append(
                        f"High error rate: {health['error_rate']:.1%}"
                    )

                # Check for staleness (no run in last 24 hours)
                if health["last_run"]:
                    from dateutil import parser

                    try:
                        last_run_time = parser.parse(health["last_run"])
                        age_hours = (
                            datetime.utcnow() - last_run_time.replace(tzinfo=None)
                        ).total_seconds() / 3600
                        if age_hours > 24:
                            health["issues"].append(
                                f"Stale data: no run in {age_hours:.1f} hours"
                            )
                    except Exception:
                        pass
            else:
                health["issues"].append("No run history found")

        except Exception as e:
            health["issues"].append(f"Metrics check failed: {e}")

    except Exception as e:
        health["status"] = "check_failed"
        health["issues"].append(f"Health check error: {e}")

    return health


def send_alert(webhook_url: str, unhealthy_resources: List[Dict[str, Any]]):
    """
    Send alert to webhook.

    Args:
        webhook_url: Webhook URL (e.g., Slack, generic webhook)
        unhealthy_resources: List of unhealthy resource health dicts
    """
    try:
        import requests
    except ImportError:
        print("Warning: requests not installed, skipping alert", file=sys.stderr)
        return

    alert_payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "alert_type": "nexla_health_check",
        "unhealthy_count": len(unhealthy_resources),
        "resources": unhealthy_resources,
    }

    try:
        response = requests.post(
            webhook_url,
            json=alert_payload,
            timeout=10,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        print(f"Alert sent to {webhook_url}")
    except Exception as e:
        print(f"Failed to send alert: {e}", file=sys.stderr)


def main():
    """Main entry point for health check script."""
    parser = argparse.ArgumentParser(
        description="Health check for Nexla flows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example config file (config.json):
{
  "resources": [
    {"type": "data_sources", "id": 123},
    {"type": "data_sets", "id": 456},
    {"type": "data_sinks", "id": 789}
  ]
}

Example usage:
  python health_check.py --config monitoring_config.json
  python health_check.py --config monitoring_config.json --alert-webhook https://hooks.slack.com/...
  python health_check.py --config monitoring_config.json --output results.json
        """,
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Configuration file (JSON) with resources to monitor",
    )
    parser.add_argument(
        "--alert-webhook", help="Webhook URL for alerts (Slack, generic webhook, etc.)"
    )
    parser.add_argument("--output", help="Output file for results (JSON)")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.2,
        help="Error rate threshold for alerting (default: 0.2 = 20%%)",
    )
    args = parser.parse_args()

    # Load configuration
    try:
        with open(args.config) as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate config structure
    if "resources" not in config or not isinstance(config["resources"], list):
        print("Error: config must have 'resources' list", file=sys.stderr)
        sys.exit(1)

    # Initialize client
    try:
        client = NexlaClient()
    except Exception as e:
        print(f"Error initializing NexlaClient: {e}", file=sys.stderr)
        print("Ensure NEXLA_SERVICE_KEY or NEXLA_ACCESS_TOKEN is set", file=sys.stderr)
        sys.exit(1)

    # Run health checks
    results = []
    unhealthy = []

    print(f"Checking health of {len(config['resources'])} resources...\n")

    for resource in config["resources"]:
        try:
            resource_type = resource["type"]
            resource_id = resource["id"]

            health = check_flow_health(client, resource_type, resource_id, args.threshold)
            results.append(health)

            if health["issues"]:
                unhealthy.append(health)
                print(f"❌ UNHEALTHY: {resource_type} {resource_id}")
                for issue in health["issues"]:
                    print(f"   - {issue}")
            else:
                print(f"✓ HEALTHY: {resource_type} {resource_id}")
                print(
                    f"   Status: {health['status']}, Error rate: {health['error_rate']:.1%}"
                )

        except Exception as e:
            print(f"❌ ERROR checking {resource.get('type')} {resource.get('id')}: {e}")
            results.append(
                {
                    "resource_type": resource.get("type"),
                    "resource_id": resource.get("id"),
                    "status": "check_error",
                    "issues": [str(e)],
                }
            )

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"Summary: {len(results)} checked, {len(unhealthy)} unhealthy")
    print(f"{'=' * 60}")

    # Send alert if needed
    if unhealthy and args.alert_webhook:
        print(f"\nSending alert for {len(unhealthy)} unhealthy resources...")
        send_alert(args.alert_webhook, unhealthy)

    # Save results
    if args.output:
        try:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {args.output}")
        except Exception as e:
            print(f"Error saving results: {e}", file=sys.stderr)

    # Exit with error code if unhealthy resources found
    sys.exit(1 if unhealthy else 0)


if __name__ == "__main__":
    main()
