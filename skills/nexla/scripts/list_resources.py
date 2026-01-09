#!/usr/bin/env python3
"""List and filter Nexla resources."""

import sys
import json
import argparse
from typing import Dict, List, Any, Optional

try:
    from nexla_sdk import NexlaClient
except ImportError:
    print("Error: nexla_sdk not installed. Run: pip install nexla-sdk", file=sys.stderr)
    sys.exit(1)


def _summarize_resource(resource: Any, resource_type: str) -> Dict[str, Any]:
    return {
        "id": getattr(resource, "id", None),
        "name": getattr(resource, "name", "N/A"),
        "type": resource_type,
        "updated_at": getattr(
            resource, "updated_at", getattr(resource, "updated_on", None)
        ),
    }


def _serialize_resource(resource: Any) -> Dict[str, Any]:
    if hasattr(resource, "model_dump"):
        return resource.model_dump(exclude_none=True)
    if hasattr(resource, "to_dict"):
        return resource.to_dict()
    if hasattr(resource, "__dict__"):
        return resource.__dict__
    return {"value": resource}


def _extract_run_nodes(flow_responses: List[Any]) -> List[Any]:
    nodes = []
    for flow_response in flow_responses:
        flows = getattr(flow_response, "flows", None)
        if flows:
            nodes.extend(flows)
    return nodes


def list_resources(
    client: NexlaClient,
    resource_type: str,
    name_pattern: Optional[str] = None,
    limit: int = 10,
    full_info: bool = False,
) -> List[Dict[str, Any]]:
    """
    List resources with optional filtering.

    Args:
        client: NexlaClient instance
        resource_type: Resource type (sources, destinations, nexsets, flows, etc.)
        name_pattern: Optional substring to match in resource name (case-insensitive)
        limit: Maximum number of items to return (capped at 500 items due to pagination limits)
        full_info: If True, return full resource dicts; else summary

    Returns:
        List of resource dicts or summaries

    Note:
        Pagination is limited to 10 pages of 50 items each (500 items max).
        For larger datasets, use the SDK paginator directly.
    """
    type_map = {
        "source": "sources",
        "sources": "sources",
        "destination": "destinations",
        "destinations": "destinations",
        "nexset": "nexsets",
        "nexsets": "nexsets",
        "flow": "flows",
        "flows": "flows",
        "credential": "credentials",
        "credentials": "credentials",
    }

    sdk_attr = type_map.get(resource_type.lower(), resource_type)
    if not hasattr(client, sdk_attr):
        raise ValueError(f"Unknown resource type: {resource_type}")

    api = getattr(client, sdk_attr)
    items: List[Any] = []

    if sdk_attr == "flows":
        flow_responses = api.list(flows_only=True)
        items = _extract_run_nodes(flow_responses)
    else:
        page = 1
        per_page = 50
        while len(items) < limit:
            batch = api.list(page=page, per_page=per_page)
            if not batch:
                break
            items.extend(batch)
            page += 1
            if page > 10:
                break

    results: List[Dict[str, Any]] = []
    for item in items:
        name = getattr(item, "name", "") or ""
        if name_pattern and name_pattern.lower() not in name.lower():
            continue
        if full_info:
            results.append(_serialize_resource(item))
        else:
            if sdk_attr == "flows":
                resource_id = (
                    getattr(item, "data_source_id", None)
                    or getattr(item, "data_set_id", None)
                    or getattr(item, "data_sink_id", None)
                )
                results.append(
                    {
                        "id": getattr(item, "id", None),
                        "name": getattr(item, "name", None),
                        "status": getattr(item, "status", None),
                        "flow_type": getattr(item, "flow_type", None),
                        "resource_id": resource_id,
                    }
                )
            else:
                results.append(_summarize_resource(item, sdk_attr))
        if len(results) >= limit:
            break

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="List and filter Nexla resources")
    parser.add_argument(
        "--type",
        required=True,
        help="Resource type (sources, destinations, nexsets, flows, credentials)",
    )
    parser.add_argument(
        "--name", help="Filter by name (substring match, case-insensitive)"
    )
    parser.add_argument(
        "--limit", type=int, default=10, help="Maximum number of results (default: 10, max: 500)"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Output full resource details instead of summary",
    )
    parser.add_argument("--output", help="Output file for JSON results")
    args = parser.parse_args()

    try:
        client = NexlaClient()
    except Exception as exc:
        print(f"Error initializing NexlaClient: {exc}", file=sys.stderr)
        print("Ensure NEXLA_SERVICE_KEY or NEXLA_ACCESS_TOKEN is set", file=sys.stderr)
        sys.exit(1)

    try:
        results = list_resources(
            client,
            args.type,
            name_pattern=args.name,
            limit=args.limit,
            full_info=args.full,
        )
        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2))
    except Exception as exc:
        print(f"Error listing resources: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
