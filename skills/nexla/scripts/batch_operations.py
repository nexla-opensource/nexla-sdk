#!/usr/bin/env python3
"""Batch operations for Nexla resources."""

import sys
import json
import argparse
from typing import Dict, List, Any

try:
    from nexla_sdk import NexlaClient
except ImportError:
    print("Error: nexla_sdk not installed. Run: pip install nexla-sdk", file=sys.stderr)
    sys.exit(1)


def batch_create(
    client: NexlaClient, resource_type: str, configs: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create multiple resources with idempotency and checkpointing.

    Args:
        client: NexlaClient instance
        resource_type: Resource type (sources, destinations, nexsets, etc.)
        configs: List of resource configurations

    Returns:
        Results dict with created, skipped, and failed lists
    """
    resource_api = getattr(client, resource_type)
    results = {"created": [], "skipped": [], "failed": []}

    for i, cfg in enumerate(configs, 1):
        try:
            print(f"[{i}/{len(configs)}] Processing {cfg.get('name', 'unnamed')}...")

            # Idempotency check: search by name
            existing = [r for r in resource_api.list() if r.name == cfg["name"]]
            if existing:
                print(
                    f"  ⚠ Resource '{cfg['name']}' already exists (ID: {existing[0].id}), skipping"
                )
                results["skipped"].append({"name": cfg["name"], "id": existing[0].id})
                continue

            # Create resource
            resource = resource_api.create(cfg)
            results["created"].append({"name": cfg["name"], "id": resource.id})
            print(f"  ✓ Created '{cfg['name']}' (ID: {resource.id})")

        except Exception as e:
            results["failed"].append(
                {"name": cfg.get("name", "unnamed"), "error": str(e)}
            )
            print(f"  ❌ Failed to create '{cfg.get('name', 'unnamed')}': {e}")

    return results


def batch_update(
    client: NexlaClient, resource_type: str, updates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Update multiple resources.

    Args:
        client: NexlaClient instance
        resource_type: Resource type (sources, destinations, nexsets, etc.)
        updates: List of update dicts with 'id' and 'data' keys

    Returns:
        Results dict with updated and failed lists
    """
    resource_api = getattr(client, resource_type)
    results = {"updated": [], "failed": []}

    for i, upd in enumerate(updates, 1):
        try:
            resource_id = upd["id"]
            update_data = upd["data"]

            print(f"[{i}/{len(updates)}] Updating resource ID {resource_id}...")

            resource = resource_api.update(resource_id, update_data)
            results["updated"].append(
                {"id": resource_id, "name": getattr(resource, "name", None)}
            )
            print(f"  ✓ Updated resource {resource_id}")

        except Exception as e:
            results["failed"].append({"id": upd.get("id"), "error": str(e)})
            print(f"  ❌ Failed to update {upd.get('id')}: {e}")

    return results


def batch_delete(
    client: NexlaClient, resource_type: str, resource_ids: List[int]
) -> Dict[str, Any]:
    """
    Delete multiple resources.

    Args:
        client: NexlaClient instance
        resource_type: Resource type (sources, destinations, nexsets, etc.)
        resource_ids: List of resource IDs to delete

    Returns:
        Results dict with deleted and failed lists
    """
    resource_api = getattr(client, resource_type)
    results = {"deleted": [], "failed": []}

    for i, resource_id in enumerate(resource_ids, 1):
        try:
            print(f"[{i}/{len(resource_ids)}] Deleting resource ID {resource_id}...")

            resource_api.delete(resource_id)
            results["deleted"].append(resource_id)
            print(f"  ✓ Deleted resource {resource_id}")

        except Exception as e:
            results["failed"].append({"id": resource_id, "error": str(e)})
            print(f"  ❌ Failed to delete {resource_id}: {e}")

    return results


def main():
    """Main entry point for batch operations script."""
    parser = argparse.ArgumentParser(
        description="Batch operations for Nexla resources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example config file for CREATE (sources_config.json):
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

Example config file for UPDATE (updates_config.json):
{
  "items": [
    {
      "id": 456,
      "data": {"description": "Updated description"}
    },
    {
      "id": 789,
      "data": {"tags": ["production", "critical"]}
    }
  ]
}

Example config file for DELETE (delete_config.json):
{
  "items": [123, 456, 789]
}

Example usage:
  # Create multiple sources
  python batch_operations.py --operation create --resource-type sources --config sources_config.json

  # Update multiple resources
  python batch_operations.py --operation update --resource-type destinations --config updates_config.json

  # Delete multiple resources
  python batch_operations.py --operation delete --resource-type nexsets --config delete_config.json

  # Save results
  python batch_operations.py --operation create --resource-type sources --config sources_config.json --output results.json
        """,
    )
    parser.add_argument(
        "--operation",
        choices=["create", "update", "delete"],
        required=True,
        help="Batch operation type",
    )
    parser.add_argument(
        "--resource-type",
        required=True,
        help="Resource type (sources, destinations, nexsets, credentials, etc.)",
    )
    parser.add_argument("--config", required=True, help="Configuration file (JSON)")
    parser.add_argument("--output", help="Output results to file (JSON)")
    args = parser.parse_args()

    # Load configuration
    try:
        with open(args.config) as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate config structure
    if "items" not in config:
        print("Error: config must have 'items' key", file=sys.stderr)
        sys.exit(1)

    # Initialize client
    try:
        client = NexlaClient()
    except Exception as e:
        print(f"Error initializing NexlaClient: {e}", file=sys.stderr)
        print("Ensure NEXLA_SERVICE_KEY or NEXLA_ACCESS_TOKEN is set", file=sys.stderr)
        sys.exit(1)

    # Execute batch operation
    print(f"\nExecuting batch {args.operation} on {args.resource_type}...")
    print(f"{'=' * 60}\n")

    try:
        if args.operation == "create":
            results = batch_create(client, args.resource_type, config["items"])
        elif args.operation == "update":
            results = batch_update(client, args.resource_type, config["items"])
        elif args.operation == "delete":
            results = batch_delete(client, args.resource_type, config["items"])
        else:
            print(f"Unknown operation: {args.operation}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"\nFatal error during batch operation: {e}", file=sys.stderr)
        sys.exit(1)

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"Batch {args.operation} summary:")
    print(f"{'=' * 60}")
    for key, value in results.items():
        print(f"{key.capitalize()}: {len(value)}")
    print(f"{'=' * 60}")

    # Save results
    if args.output:
        try:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {args.output}")
        except Exception as e:
            print(f"Error saving results: {e}", file=sys.stderr)

    # Print full results
    print("\nDetailed results:")
    print(json.dumps(results, indent=2))

    # Exit with error code if any failures
    sys.exit(0 if not results.get("failed") else 1)


if __name__ == "__main__":
    main()
