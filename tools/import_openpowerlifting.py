#!/usr/bin/env python3
"""Convert an official OpenPowerlifting bulk ZIP into a compact Kveldúlfur ranking JSON.

Usage:
  python tools/import_openpowerlifting.py openpowerlifting-latest.zip
  python tools/import_openpowerlifting.py openpowerlifting-latest.zip --limit 250

Only positive successful results are ranked. Each athlete has one best performance
per feat, sex and equipment group. This is a prototype, not a canonical OPL ranking.
"""
import argparse
import csv
import io
import json
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

FEATS = {
    "squat": ("Best3SquatKg", "Squat"),
    "bench": ("Best3BenchKg", "Bench press"),
    "deadlift": ("Best3DeadliftKg", "Deadlift"),
    "total": ("TotalKg", "Total"),
}
OUTPUT = Path(__file__).resolve().parents[1] / "logs" / "data" / "openpowerlifting.json"


def source_rows(path):
    with zipfile.ZipFile(path) as archive:
        names = [n for n in archive.namelist() if n.lower().endswith(".csv") and not n.startswith("__MACOSX")]
        if not names:
            raise ValueError("No CSV found in ZIP")
        # Bulk archive has a single principal CSV. Prefer the largest if there are extras.
        name = max(names, key=lambda n: archive.getinfo(n).file_size)
        with archive.open(name) as binary:
            with io.TextIOWrapper(binary, encoding="utf-8-sig", newline="") as text:
                yield from csv.DictReader(text)


def build(path, limit):
    best = {}
    count = 0
    for row in source_rows(path):
        count += 1
        athlete = (row.get("Name") or "").strip()
        sex = (row.get("Sex") or "").strip()
        equipment = (row.get("Equipment") or "").strip()
        if not athlete or not sex or not equipment:
            continue
        if row.get("Place") in ("DQ", "DD", "NS"):
            continue
        for feat, (column, _) in FEATS.items():
            try:
                value = float(row.get(column) or 0)
            except ValueError:
                continue
            if not 0 < value < 2000:
                continue
            key = (feat, sex, equipment, athlete)
            existing = best.get(key)
            if existing is None or value > existing["value"]:
                best[key] = {
                    "name": athlete, "sex": sex, "equipment": equipment,
                    "feat": feat, "value": value,
                    "bodyweight": row.get("BodyweightKg") or None,
                    "federation": row.get("Federation") or "",
                    "meet": row.get("MeetName") or "",
                    "date": row.get("Date") or "",
                    "country": row.get("Country") or "",
                    "source": "OpenPowerlifting",
                }
    groups = defaultdict(list)
    for record in best.values():
        groups[(record["feat"], record["sex"], record["equipment"])].append(record)
    rankings = []
    for (feat, sex, equipment), records in sorted(groups.items()):
        records.sort(key=lambda r: (-r["value"], r["name"]))
        for rank, record in enumerate(records[:limit], start=1):
            rankings.append({"rank": rank, **record})
    return {
        "source": "OpenPowerlifting",
        "source_url": "https://data.openpowerlifting.org",
        "license": "Public Domain (see OpenPowerlifting data license)",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_rows_processed": count,
        "note": "Top records per feat, sex, equipment. One best per athlete in each group. No population parses inferred.",
        "feats": [{"id": k, "name": label, "unit": "kg"} for k, (_, label) in FEATS.items()],
        "rankings": rankings,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zipfile", type=Path)
    parser.add_argument("--limit", type=int, default=100, help="Top athletes per feat/sex/equipment")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 10000:
        parser.error("--limit must be between 1 and 10000")
    result = build(args.zipfile, args.limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Processed {result['source_rows_processed']:,} entries; exported {len(result['rankings']):,} ranked performances to {args.output}")


if __name__ == "__main__":
    main()
