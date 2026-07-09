#!/usr/bin/env python3
"""Builds feed.xml (RSS 2.0) from injuries.json."""
import os
from datetime import datetime, timezone
from xml.sax.saxutils import escape

from injury_data import BASE_DIR, load_valid_records

RSS_FILE = BASE_DIR / "feed.xml"

CHANNEL_TITLE = "High-Profile Athlete Injury Report"
CHANNEL_LINK = "https://esalisbury-arch.github.io/athlete-injury-feed/"
CHANNEL_DESCRIPTION = (
    "Daily-updated feed of high-profile athlete injuries across NFL, NBA, WNBA, MLB, NHL, "
    "top soccer leagues, tennis, golf, F1, boxing/UFC, cricket, Olympic sports, and NCAA D1."
)


def rfc822(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")


def item_xml(record: dict) -> str:
    description = (
        f"{record['athlete']} ({record['org']}) — {record['injury_context']}. "
        f"Expected duration: {record['duration']}. "
        f"Financial impact: {record['financial_impact']}. "
        f"Team impact: {record['team_impact']}."
    )
    return (
        "  <item>\n"
        f"    <title>{escape(record['athlete'])} ({escape(record['sport'])}) — {escape(record['injury_context'])}</title>\n"
        f"    <link>{escape(record['source_url'])}</link>\n"
        f"    <guid isPermaLink=\"false\">{escape(record['guid'])}</guid>\n"
        f"    <pubDate>{rfc822(record['date_reported'])}</pubDate>\n"
        f"    <category>{escape(record['sport'])}</category>\n"
        f"    <description>{escape(description)}</description>\n"
        "  </item>"
    )


def main() -> None:
    records, total = load_valid_records()
    records.sort(key=lambda r: r["date_reported"], reverse=True)

    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")
    items = "\n".join(item_xml(r) for r in records)

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>{escape(CHANNEL_TITLE)}</title>
  <link>{escape(CHANNEL_LINK)}</link>
  <description>{escape(CHANNEL_DESCRIPTION)}</description>
  <language>en-us</language>
  <lastBuildDate>{now}</lastBuildDate>
{items}
</channel>
</rss>
"""

    tmp_file = RSS_FILE.with_suffix(".xml.tmp")
    tmp_file.write_text(xml, encoding="utf-8")
    os.replace(tmp_file, RSS_FILE)
    print(f"Wrote {len(records)} of {total} items to {RSS_FILE}")


if __name__ == "__main__":
    main()
