#!/usr/bin/env python3
"""Parse MongoDB security advisory RSS/XML into structured JSON.

Deterministic extraction only — no judgment calls. Reads either a local
XML file (an already-fetched copy of https://www.mongodb.com/alerts/rss)
or a URL, and emits one JSON object per <item> with title, link (this feed
publishes the upstream MongoDB Jira ticket URL here, e.g.
jira.mongodb.org/browse/SERVER-XXXXX), pubDate, guid, a tag-stripped
summary, and any CVE IDs found in the title/summary.

The feed itself is NOT in chronological order (verified against the live
feed — items jump around by months/years) so this script always sorts by
the parsed pubDate, newest first, before any --index/--limit/--cve filter
is applied. Never assume feed order means recency.

Usage:
    parse_advisory.py --file feed.xml
    parse_advisory.py --url https://www.mongodb.com/alerts/rss
    parse_advisory.py --file feed.xml --cve CVE-2025-12345
    parse_advisory.py --file feed.xml --index 0      # newest item after sorting
    parse_advisory.py --file feed.xml --limit 5       # 5 most recent items
"""

import argparse
import datetime
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")


def strip_html(text):
    if not text:
        return ""
    text = TAG_RE.sub(" ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def find_cves(*parts):
    found = []
    for part in parts:
        for match in CVE_RE.findall(part or ""):
            cve = match.upper()
            if cve not in found:
                found.append(cve)
    return found


def parse_pub_date(raw):
    """Parse an RFC 2822 pubDate into an aware UTC datetime, or None if unparseable."""
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)


def parse_items(xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        guid = (item.findtext("guid") or "").strip()
        raw_desc = item.findtext("description") or ""
        summary = strip_html(raw_desc)
        dt = parse_pub_date(pub_date)
        items.append(
            {
                "title": title,
                "link": link,
                "guid": guid,
                "pub_date": pub_date,
                "pub_date_iso": dt.isoformat() if dt else None,
                "summary": summary,
                "cve_ids": find_cves(title, summary),
            }
        )
    return items


def sort_by_pub_date_desc(items):
    """Newest first. Items with an unparseable/missing pubDate sort last and
    are reported on stderr rather than silently dropped or mis-ordered."""
    undated = [i for i in items if i["pub_date_iso"] is None]
    if undated:
        print(
            f"warning: {len(undated)} item(s) had an unparseable pubDate and were "
            "sorted last: "
            + ", ".join(i["title"][:60] for i in undated),
            file=sys.stderr,
        )
    return sorted(
        items,
        key=lambda i: i["pub_date_iso"] or "",
        reverse=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="Path to a local RSS/XML file")
    src.add_argument("--url", help="URL to fetch the RSS/XML feed from")
    parser.add_argument("--cve", help="Filter to items mentioning this CVE ID")
    parser.add_argument(
        "--index", type=int, help="Return only the Nth item (0-based) after sorting"
    )
    parser.add_argument("--limit", type=int, help="Return at most N items after sorting")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "rb") as f:
            xml_bytes = f.read()
    else:
        with urllib.request.urlopen(args.url, timeout=30) as resp:
            xml_bytes = resp.read()

    items = parse_items(xml_bytes)
    items = sort_by_pub_date_desc(items)

    if args.cve:
        needle = args.cve.upper()
        items = [i for i in items if needle in i["cve_ids"]]

    if args.index is not None:
        items = items[args.index : args.index + 1]

    if args.limit is not None:
        items = items[: args.limit]

    json.dump(items, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
