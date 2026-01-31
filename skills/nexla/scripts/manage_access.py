#!/usr/bin/env python3
"""Manage access control for Nexla resources.

Usage:
    # List accessors for a resource
    python manage_access.py --operation list --resource-type sources --resource-id 123

    # Grant user access
    python manage_access.py --operation grant --resource-type sources --resource-id 123 \
        --accessor-type USER --email user@example.com --role collaborator

    # Grant team access to multiple resources
    python manage_access.py --operation grant --resource-type nexsets --resource-ids 123,456,789 \
        --accessor-type TEAM --accessor-id 42 --role operator

    # Revoke user access
    python manage_access.py --operation revoke --resource-type sources --resource-id 123 \
        --accessor-type USER --email old-user@example.com

Environment:
    NEXLA_SERVICE_KEY or NEXLA_ACCESS_TOKEN must be set.
    NEXLA_API_URL can override the default API endpoint.
"""

import argparse
import json
import sys
from typing import Any, Dict, List

try:
    from nexla_sdk import NexlaClient
except ImportError:
    print("Error: nexla_sdk not installed. Run: pip install nexla-sdk", file=sys.stderr)
    sys.exit(1)


def list_accessors(client, resource_type: str, resource_id: int) -> List[Dict]:
    """List accessors for a resource."""
    resource_api = getattr(client, resource_type)
    accessors = resource_api.get_accessors(resource_id)

    return [
        {
            "type": acc.type.value if hasattr(acc.type, "value") else acc.type,
            "id": getattr(acc, "id", None),
            "email": getattr(acc, "email", None),
            "name": getattr(acc, "name", None),
            "access_roles": [
                r.value if hasattr(r, "value") else r for r in acc.access_roles
            ],
        }
        for acc in accessors
    ]


def grant_access(
    client, resource_type: str, resource_ids: List[int], accessor: Dict
) -> Dict[str, Any]:
    """Grant access to multiple resources."""
    resource_api = getattr(client, resource_type)
    results = {"success": [], "failed": []}

    for resource_id in resource_ids:
        try:
            resource_api.add_accessors(resource_id, [accessor])
            results["success"].append(resource_id)
            print(f"✓ Granted access to {resource_type}/{resource_id}")
        except Exception as e:
            results["failed"].append({"id": resource_id, "error": str(e)})
            print(f"✗ Failed {resource_type}/{resource_id}: {e}", file=sys.stderr)

    return results


def revoke_access(
    client, resource_type: str, resource_ids: List[int], accessor: Dict
) -> Dict[str, Any]:
    """Revoke access from multiple resources."""
    resource_api = getattr(client, resource_type)
    results = {"success": [], "failed": []}

    for resource_id in resource_ids:
        try:
            resource_api.delete_accessors(resource_id, [accessor])
            results["success"].append(resource_id)
            print(f"✓ Revoked access from {resource_type}/{resource_id}")
        except Exception as e:
            results["failed"].append({"id": resource_id, "error": str(e)})
            print(f"✗ Failed {resource_type}/{resource_id}: {e}", file=sys.stderr)

    return results


def build_accessor(args) -> Dict[str, Any]:
    """Build accessor dict from CLI arguments."""
    accessor = {
        "type": args.accessor_type,
        "access_roles": [args.role] if args.role else ["collaborator"],
    }

    if args.accessor_id:
        accessor["id"] = args.accessor_id
    if args.email:
        accessor["email"] = args.email

    return accessor


def main():
    parser = argparse.ArgumentParser(
        description="Manage Nexla resource access control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--operation",
        "-o",
        choices=["list", "grant", "revoke"],
        required=True,
        help="Operation to perform",
    )
    parser.add_argument(
        "--resource-type",
        "-t",
        required=True,
        help="Resource type: sources, nexsets, destinations, flows, credentials, etc.",
    )
    parser.add_argument("--resource-id", "-r", type=int, help="Single resource ID")
    parser.add_argument(
        "--resource-ids", help="Comma-separated resource IDs for batch operations"
    )
    parser.add_argument(
        "--accessor-type", choices=["USER", "TEAM", "ORG"], help="Type of accessor"
    )
    parser.add_argument("--accessor-id", type=int, help="Accessor ID (for TEAM or ORG)")
    parser.add_argument("--email", help="Email address (for USER accessor)")
    parser.add_argument(
        "--role",
        choices=["owner", "admin", "operator", "collaborator"],
        default="collaborator",
        help="Access role (default: collaborator)",
    )
    parser.add_argument("--output", "-O", help="Output file for results (JSON)")

    args = parser.parse_args()

    # Validate arguments
    if args.operation == "list" and not args.resource_id:
        parser.error("--resource-id is required for list operation")

    if args.operation in ["grant", "revoke"]:
        if not args.accessor_type:
            parser.error("--accessor-type is required for grant/revoke operations")
        if args.accessor_type == "USER" and not args.email and not args.accessor_id:
            parser.error("--email or --accessor-id is required for USER accessor")
        if args.accessor_type in ["TEAM", "ORG"] and not args.accessor_id:
            parser.error("--accessor-id is required for TEAM/ORG accessor")

    # Initialize client
    try:
        client = NexlaClient()
    except Exception as e:
        print(f"Error: Failed to initialize client: {e}", file=sys.stderr)
        print("Ensure NEXLA_SERVICE_KEY or NEXLA_ACCESS_TOKEN is set.", file=sys.stderr)
        sys.exit(1)

    # Determine resource IDs
    if args.resource_id:
        resource_ids = [args.resource_id]
    elif args.resource_ids:
        resource_ids = [int(x.strip()) for x in args.resource_ids.split(",")]
    else:
        parser.error("--resource-id or --resource-ids is required")

    # Execute operation
    try:
        if args.operation == "list":
            result = list_accessors(client, args.resource_type, resource_ids[0])
            print(json.dumps(result, indent=2))
        else:
            accessor = build_accessor(args)

            if args.operation == "grant":
                result = grant_access(
                    client, args.resource_type, resource_ids, accessor
                )
            else:
                result = revoke_access(
                    client, args.resource_type, resource_ids, accessor
                )

            # Summary
            print(
                f"\nSummary: {len(result['success'])} succeeded, {len(result['failed'])} failed"
            )

            if args.output:
                with open(args.output, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"Results saved to {args.output}")

        sys.exit(0 if not result.get("failed") else 1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
