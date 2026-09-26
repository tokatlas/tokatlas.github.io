#!/usr/bin/env python3
"""Deterministic flagging for contradictions and outliers (schema rules 4-5).

Flags are computed from the merged record set and stored on each record in the
`flags` field, so check_data.py can verify they are up to date.

Rules (conservative, documented in data/schema.md):
- contradiction: >=2 records with the same (model, hardware, quant, backend,
  ctx) whose tps differ by more than 10% relative to the group max.
- outlier: within a (model, hardware, quant, ctx) group of >=3 measured rows
  (provenance != 'estimated'), a row whose tps is >3x or <1/3 of the group
  median.

tps may arrive as number (JSON) or string (CSV); both are handled.
"""
import re
from collections import defaultdict


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", str(s).lower())


def tps_of(r):
    try:
        v = float(r.get("tps"))
        return v if v > 0 else None
    except (TypeError, ValueError):
        return None


def _grp(rows, key):
    g = defaultdict(list)
    for r in rows:
        g[key(r)].append(r)
    return g


def compute_flags(rows):
    flags = defaultdict(set)
    for r in rows:
        flags[r["id"]]  # touch so every id exists

    # contradictions
    for grp in _grp(rows, lambda r: (
            norm(r.get("model")), norm(r.get("hardware")), norm(r.get("quant")),
            norm(r.get("backend")), str(r.get("ctx") or ""))).values():
        vals = [tps_of(r) for r in grp]
        vals = [v for v in vals if v is not None]
        if len(vals) < 2:
            continue
        hi = max(vals)
        if hi <= 0:
            continue
        for r in grp:
            v = tps_of(r)
            if v is not None and hi - v > 0.10 * hi:
                flags[r["id"]].add("contradiction")

    # outliers (measured rows only)
    for grp in _grp(rows, lambda r: (
            norm(r.get("model")), norm(r.get("hardware")), norm(r.get("quant")),
            str(r.get("ctx") or ""))).values():
        measured = [r for r in grp
                    if tps_of(r) is not None and r.get("provenance") != "estimated"]
        if len(measured) < 3:
            continue
        vals = sorted(tps_of(r) for r in measured)
        med = vals[len(vals) // 2]
        if med <= 0:
            continue
        for r in measured:
            v = tps_of(r)
            if v > 3 * med or v < med / 3:
                flags[r["id"]].add("outlier")

    return {rid: sorted(v) for rid, v in flags.items()}


if __name__ == "__main__":
    import json
    import os
    data = json.load(open(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "data", "records.json")))
    fl = compute_flags(data["records"])
    n = sum(len(v) for v in fl.values())
    print("%d records, %d flags" % (len(fl), n))
    for rid, v in sorted(fl.items()):
        if v:
            print(" ", rid, v)
