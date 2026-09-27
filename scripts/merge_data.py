#!/usr/bin/env python3
"""Merge data/raw/*.json source files into data/records.csv + records.json.

Also splits reference estimates (data/reference/estimates.json) and computes
contradiction/outlier flags (scripts/flags.py) on measured rows, so every
record carries them. Stdlib only.
"""
import csv
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIELDNAMES = [
    "id", "model", "params", "quant", "hardware", "ram_gb", "backend",
    "ctx", "batch", "tps", "pp_tps", "pp_tokens", "tg_tokens",
    "ttft_s", "power_w", "date", "provenance", "source_url",
    "source_name", "retrieved", "quote", "notes", "flags",
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

    # v3: estimates are reference values, not records. They live in
    # data/reference/ and are excluded from record counts, flags, and the
    # default site views. v3.1: cluster / multi-node runs (scope=cluster) are
    # out of the local-inference record set too; they stay in the reference
    # area, measured and source-cited but excluded from counts and flags.
    measured = [r for r in deduped if r.get("provenance") != "estimated"
                and r.get("scope") != "cluster"]
    estimated = [r for r in deduped if r.get("provenance") == "estimated"]
    cluster = [r for r in deduped if r.get("provenance") != "estimated"
               and r.get("scope") == "cluster"]

    # flags (measured rows only; cluster rows are out of record scope)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from flags import compute_flags
    fl = compute_flags(measured)
    for r in measured:
        r["flags"] = fl.get(r["id"], [])
    for r in cluster:
        r["flags"] = []

    retrieved = max((r["retrieved"] for r in measured), default="?")
    with open(os.path.join(ROOT, "data", "records.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        for r in measured:
            w.writerow({k: (",".join(r[k]) if isinstance(r.get(k), list)
                            else ("" if r.get(k) is None else r[k]))
                        for k in FIELDNAMES})
    with open(os.path.join(ROOT, "data", "records.json"), "w") as f:
        json.dump({"count": len(measured), "retrieved": retrieved, "records": measured},
                  f, indent=1, sort_keys=True)
    os.makedirs(os.path.join(ROOT, "data", "reference"), exist_ok=True)
    with open(os.path.join(ROOT, "data", "reference", "estimates.json"), "w") as f:
        json.dump({"count": len(estimated), "retrieved": retrieved,
                   "note": "reference estimates only (source models, not measurements); excluded from record counts",
                   "records": estimated}, f, indent=1, sort_keys=True)
    with open(os.path.join(ROOT, "data", "reference", "cluster.json"), "w") as f:
        json.dump({"count": len(cluster), "retrieved": retrieved,
                   "note": "cluster and multi-node runs (measured, source-cited) out of record scope: local inference means single-machine hardware",
                   "records": cluster}, f, indent=1, sort_keys=True)
    with open(os.path.join(ROOT, "data", "sources.json"), "w") as f:
        json.dump(sources, f, indent=1, sort_keys=True)

    print("merged %d records + %d reference estimates + %d cluster runs from %d sources (retrieved %s)"
          % (len(measured), len(estimated), len(cluster), len(files), retrieved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
