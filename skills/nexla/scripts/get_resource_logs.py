#!/usr/bin/env python3
"""Fetch flow logs for a Nexla resource run."""

import sys
import json
import argparse
from typing import Any, Dict, List, Optional

try:
    from nexla_sdk import NexlaClient
except ImportError:
    print("Error: nexla_sdk not installed. Run: pip install nexla-sdk", file=sys.stderr)
    sys.exit(1)


def _extract_runs(metrics_response: Any) -> List[Dict[str, Any]]:
    metrics = getattr(metrics_response, "metrics", None)
    if isinstance(metrics, dict):
        data = metrics.get("data")
        return data if isinstance(data, list) else []
    if isinstance(metrics, list):
        return metrics
    return []


def _resolve_run_context(
    client: NexlaClient,
    resource_type: str,
    resource_id: int,
    run_id: Optional[int],
    from_ts: Optional[int],
    to_ts: Optional[int],
) -> Dict[str, Optional[int]]:
    if run_id is not None and from_ts is not None:
        return {"run_id": run_id, "from_ts": from_ts, "to_ts": to_ts}

    metrics = client.metrics.get_resource_metrics_by_run(
        resource_type=resource_type,
        resource_id=resource_id,
        orderby="runId",
        page=1,
        size=10,
    )
    runs = _extract_runs(metrics)
    if not runs:
        raise ValueError("No run history found; provide --run-id and --from-ts")

    run = runs[0]
    if run_id is not None:
        run_id_str = str(run_id)
        for candidate in runs:
            candidate_id = candidate.get("runId") or candidate.get("run_id")
            if candidate_id is None:
                continue
            if str(candidate_id) == run_id_str:
                run = candidate
                break
        else:
            raise ValueError("Run ID not found in recent history; provide --from-ts")
    resolved_run_id = run_id or run.get("runId") or run.get("run_id")
    resolved_from_ts = (
        from_ts
        or run.get("startTime")
        or run.get("start_time")
        or run.get("lastWritten")
    )
    resolved_to_ts = to_ts or run.get("endTime") or run.get("end_time")

    if resolved_run_id is None or resolved_from_ts is None:
        raise ValueError(
            "Unable to infer run_id/from_ts; provide --run-id and --from-ts"
        )

    return {
        "run_id": int(resolved_run_id),
        "from_ts": int(resolved_from_ts),
        "to_ts": int(resolved_to_ts) if resolved_to_ts is not None else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch flow logs for a Nexla resource run"
    )
    parser.add_argument(
        "--resource-type",
        required=True,
        help="Resource type (data_sources, data_sets, data_sinks)",
    )
    parser.add_argument("--resource-id", type=int, required=True, help="Resource ID")
    parser.add_argument(
        "--run-id", type=int, help="Run ID (optional, inferred if omitted)"
    )
    parser.add_argument(
        "--from-ts", type=int, help="Start timestamp (required if run is not inferable)"
    )
    parser.add_argument("--to-ts", type=int, help="End timestamp (optional)")
    parser.add_argument("--page", type=int, help="Page number")
    parser.add_argument("--per-page", type=int, help="Results per page")
    parser.add_argument("--output", help="Output file for JSON results")
    args = parser.parse_args()

    try:
        client = NexlaClient()
    except Exception as exc:
        print(f"Error initializing NexlaClient: {exc}", file=sys.stderr)
        print("Ensure NEXLA_SERVICE_KEY or NEXLA_ACCESS_TOKEN is set", file=sys.stderr)
        sys.exit(1)

    try:
        context = _resolve_run_context(
            client,
            args.resource_type,
            args.resource_id,
            args.run_id,
            args.from_ts,
            args.to_ts,
        )
        logs = client.metrics.get_flow_logs(
            resource_type=args.resource_type,
            resource_id=args.resource_id,
            run_id=context["run_id"],
            from_ts=context["from_ts"],
            to_ts=context["to_ts"],
            page=args.page,
            per_page=args.per_page,
        )

        if args.output:
            with open(args.output, "w") as f:
                json.dump(logs, f, indent=2)
            print(f"Logs saved to {args.output}")
        else:
            print(json.dumps(logs, indent=2))
    except Exception as exc:
        print(f"Error fetching logs: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
