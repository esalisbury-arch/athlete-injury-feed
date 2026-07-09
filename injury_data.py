#!/usr/bin/env python3
"""Shared loader for injuries.json, used by generate_report.py and generate_opml.py."""
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "injuries.json"

REQUIRED_FIELDS = (
    "guid", "athlete", "org", "sport", "injury_context", "duration",
    "financial_impact", "team_impact", "date_reported", "source_title", "source_url",
)


def load_valid_records() -> tuple:
    """Returns (valid_records, total_record_count)."""
    all_records = json.loads(DATA_FILE.read_text())
    seen_guids = set()
    good = []
    for i, record in enumerate(all_records):
        missing = [f for f in REQUIRED_FIELDS if not record.get(f)]
        if missing:
            print(f"skipping record {i}: missing {missing}", file=sys.stderr)
            continue
        if record["guid"] in seen_guids:
            print(f"skipping record {i}: duplicate guid {record['guid']!r}", file=sys.stderr)
            continue
        seen_guids.add(record["guid"])
        good.append(record)
    return good, len(all_records)
