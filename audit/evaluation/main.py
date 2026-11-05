"""Archived grading harness for OBS-RADAR-Q3-26 (snapshot 2026-08-30, first 30 recordings).

This is the historical audit artifact. The snapshot was produced from a partial read of the
playlist and is known to be stale for the tail recordings.
"""
from argparse import ArgumentParser
import json
import os

# Partial expected entries captured from the first 30 recordings.
REQUIRED = {
    "Datadog": {
        "ring": "Trial",
        "mention_count": 2,
        "primary": "e7_C9Q1yf48"
    },
    "Model Context Protocol (MCP)": {
        "ring": "Trial",
        "mention_count": 2,
        "primary": "SIg81hkHZXQ"
    },
    "OpenSearch": {
        "ring": "Assess",
        "mention_count": 1,
        "primary": "LuKaV3WeNlk"
    },
    "OpenTelemetry": {
        "ring": "Trial",
        "mention_count": 3,
        "primary": "kSWfRsnghaE"
    },
    "Prometheus": {
        "ring": "Assess",
        "mention_count": 1,
        "primary": "1YQwMTGIjks"
    },
    "eBPF": {
        "ring": "Assess",
        "mention_count": 1,
        "primary": "GQBbUniJltg"
    }
}


def main():
    parser = ArgumentParser()
    parser.add_argument("--agent_workspace", required=True)
    args = parser.parse_args()
    path = os.path.join(args.agent_workspace, "observability_radar.json")
    if not os.path.exists(path):
        print("missing observability_radar.json")
        raise SystemExit(1)
    data = json.load(open(path, encoding="utf-8"))
    entries = {e.get("technology"): e for e in data.get("entries", [])}
    found = 0
    for tech, expected in REQUIRED.items():
        entry = entries.get(tech)
        if not entry:
            continue
        if str(entry.get("ring")) == expected["ring"]:
            found += 1
    print(f"Archived snapshot check: {found}/{len(REQUIRED)} archived entries matched")
    if found < 4:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
