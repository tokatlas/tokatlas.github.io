#!/usr/bin/env python3
"""Merge data/raw/*.json source files into data/records.csv + records.json.

Also computes contradiction/outlier flags (scripts/flags.py) so every record
carries them. Stdlib only.
"""
import csv
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIELDNAMES = [
    "id", "model", "params", "quant", "hardware", "ram_gb", "backend",
    "ctx", "batch", "tps", "pp_tps", "ttft_s", "power_w", "date",
    "provenance", "source_url", "source_name", "retrieved", "quote", "notes",
    "flags",
]


def main() -> int:
    files = sorted(glob.glob(os.path.join(ROOT, "data", "raw", "*.json")))
    if not files:
        print("no raw source files; run the collectors first")
        return 1

    records, sources = [], {}
    for path in files:
        doc = json.load(open(path))
        recs = doc.get("records", [])
        records.extend(recs)
        sources[os.path.splitext(os.path.basename(path))[0]] = doc.get("source", {})

    # dedupe by id (keep first occurrence; sources are processed in sorted order)
    seen, deduped = set(), []
    for r in records:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        deduped.append(r)

    # flags
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from flags import compute_flags
    fl = compute_flags(deduped)
    for r in deduped:
        r["flags"] = fl.get(r["id"], [])

    retrieved = max((r["retrieved"] for r in deduped), default="?")
    with open(os.path.join(ROOT, "data", "records.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        for r in deduped:
            w.writerow({k: (",".join(r[k]) if isinstance(r.get(k), list)
                            else ("" if r.get(k) is None else r[k]))
                        for k in FIELDNAMES})
    with open(os.path.join(ROOT, "data", "records.json"), "w") as f:
        json.dump({"count": len(deduped), "retrieved": retrieved, "records": deduped},
                  f, indent=1, sort_keys=True)
    with open(os.path.join(ROOT, "data", "sources.json"), "w") as f:
        json.dump(sources, f, indent=1, sort_keys=True)

    print("merged %d records from %d sources (retrieved %s)" % (len(deduped), len(files), retrieved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
