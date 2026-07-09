#!/usr/bin/env python3
"""Builds injuries.opml, a standalone outline of injuries.json grouped by sport."""
import os
from collections import defaultdict
from xml.sax.saxutils import escape

from injury_data import BASE_DIR, load_valid_records

OPML_FILE = BASE_DIR / "injuries.opml"
OUTLINE_TITLE = "High-Profile Athlete Injury Report"


def injury_outline(record: dict) -> str:
    text = f"{record['athlete']} — {record['injury_context']} ({record['date_reported']})"
    return (
        f'    <outline text="{escape(text)}" type="link" '
        f'url="{escape(record["source_url"])}" '
        f'description="{escape(record["team_impact"])}"/>'
    )


def main() -> None:
    records, total = load_valid_records()
    records.sort(key=lambda r: r["date_reported"], reverse=True)

    by_sport = defaultdict(list)
    for record in records:
        by_sport[record["sport"]].append(record)

    sport_blocks = []
    for sport in sorted(by_sport):
        items = "\n".join(injury_outline(r) for r in by_sport[sport])
        sport_blocks.append(
            f'  <outline text="{escape(sport)}">\n{items}\n  </outline>'
        )

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
<head>
  <title>{escape(OUTLINE_TITLE)}</title>
</head>
<body>
{chr(10).join(sport_blocks)}
</body>
</opml>
"""

    tmp_file = OPML_FILE.with_suffix(".opml.tmp")
    tmp_file.write_text(xml, encoding="utf-8")
    os.replace(tmp_file, OPML_FILE)
    print(f"Wrote {len(records)} of {total} items to {OPML_FILE}")


if __name__ == "__main__":
    main()
