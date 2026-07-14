#!/usr/bin/env python3
"""Builds injuries.csv from injuries.json."""
import csv
import os

from injury_data import BASE_DIR, load_valid_records

CSV_FILE = BASE_DIR / "injuries.csv"

COLUMNS = [
    ("Athlete", "athlete"),
    ("Organization", "org"),
    ("Sport", "sport"),
    ("Location", "location"),
    ("League", "league"),
    ("Injury", "injury_context"),
    ("Expected duration", "duration"),
    ("Financial impact", "financial_impact"),
    ("Team/game impact", "team_impact"),
    ("Date reported", "date_reported"),
    ("Source", "source_title"),
    ("Source URL", "source_url"),
]


def main() -> None:
    records, total = load_valid_records()
    records.sort(key=lambda r: r["date_reported"], reverse=True)

    tmp_file = CSV_FILE.with_suffix(".csv.tmp")
    with tmp_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header for header, _ in COLUMNS)
        for record in records:
            writer.writerow(record[key] for _, key in COLUMNS)
    os.replace(tmp_file, CSV_FILE)
    print(f"Wrote {len(records)} of {total} rows to {CSV_FILE}")


if __name__ == "__main__":
    main()
