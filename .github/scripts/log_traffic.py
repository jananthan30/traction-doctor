#!/usr/bin/env python3
"""Merge the last 14 days of GitHub traffic into a CSV (one row per day).

Usage: log_traffic.py OWNER/REPO metrics/traffic.csv
Reads the token from GH_TOKEN (needs push access / "Administration: read").
Re-running is safe: rows are keyed by date and newer API values win.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import urllib.request
from pathlib import Path

FIELDS = ["date", "clones", "unique_cloners", "views", "unique_visitors"]


def fetch(repo: str, kind: str) -> list[dict]:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/traffic/{kind}?per=day",
        headers={"Authorization": f"Bearer {os.environ['GH_TOKEN']}",
                 "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)[kind]


def main(repo: str, out: str) -> int:
    path = Path(out)
    rows: dict[str, dict] = {}
    if path.exists():
        with path.open(newline="") as fh:
            rows = {r["date"]: r for r in csv.DictReader(fh)}
    for kind, count_key, unique_key in (("clones", "clones", "unique_cloners"),
                                        ("views", "views", "unique_visitors")):
        for day in fetch(repo, kind):
            date = day["timestamp"][:10]
            row = rows.setdefault(date, {f: "0" for f in FIELDS} | {"date": date})
            row[count_key], row[unique_key] = str(day["count"]), str(day["uniques"])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows[d] for d in sorted(rows))
    print(f"{path}: {len(rows)} days")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
