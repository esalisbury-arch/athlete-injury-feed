#!/usr/bin/env python3
"""Shared loader for injuries.json, used by generate_report.py and generate_opml.py."""
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "injuries.json"

REQUIRED_FIELDS = (
    "guid", "athlete", "org", "sport", "location", "league", "injury_context", "duration",
    "financial_impact_calculation", "team_impact", "date_reported", "source_title", "source_url",
)

# Nullable numeric field — legitimately None/0 for records with no confirmed dollar figure
# (e.g. "Not disclosed", "Not applicable"), so it's excluded from the truthiness check above.
OPTIONAL_NULLABLE_FIELDS = ("financial_impact_amount",)


def load_valid_records() -> tuple:
    """Returns (valid_records, total_record_count)."""
    all_records = json.loads(DATA_FILE.read_text())
    seen_guids = set()
    good = []
    for i, record in enumerate(all_records):
        missing = [f for f in REQUIRED_FIELDS if not record.get(f)]
        missing += [f for f in OPTIONAL_NULLABLE_FIELDS if f not in record]
        if missing:
            print(f"skipping record {i}: missing {missing}", file=sys.stderr)
            continue
        if record["guid"] in seen_guids:
            print(f"skipping record {i}: duplicate guid {record['guid']!r}", file=sys.stderr)
            continue
        seen_guids.add(record["guid"])
        good.append(record)
    return good, len(all_records)
