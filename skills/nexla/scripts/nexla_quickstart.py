#!/usr/bin/env python3
"""Quick sanity check for Nexla auth and basic listings."""

from typing import List

from nexla_sdk import NexlaClient, NexlaError


def _summarize(label: str, items: List[object]) -> str:
    return f"{label}={len(items)}"


def main() -> int:
    try:
        client = NexlaClient()

        sources = client.sources.list(page=1, per_page=10)
        nexsets = client.nexsets.list(page=1, per_page=10)
        destinations = client.destinations.list(page=1, per_page=10)
        flows = client.flows.list(flows_only=True)

        print(
            ", ".join(
                [
                    _summarize("sources", sources),
                    _summarize("nexsets", nexsets),
                    _summarize("destinations", destinations),
                    _summarize("flows", flows),
                ]
            )
        )

        if sources:
            print(f"sample source id: {sources[0].id}")
        if nexsets:
            print(f"sample nexset id: {nexsets[0].id}")
        if destinations:
            print(f"sample destination id: {destinations[0].id}")
        if flows and flows[0].flows:
            print(f"sample flow node id: {flows[0].flows[0].id}")

        return 0
    except NexlaError as exc:
        print(f"Nexla error: {exc}")
        return 1
    except Exception as exc:  # pragma: no cover - defensive
        print(f"Unexpected error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
