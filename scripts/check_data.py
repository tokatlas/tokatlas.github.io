#!/usr/bin/env python3
"""Data checks for the Token Atlas dataset. Run before every push.

Validates data/records.csv: required fields, value sanity, uniqueness,
and quote consistency (the exact quoted row must contain the recorded numbers).
Exits non-zero on any failure.
"""
import csv
import datetime
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED = ["id", "model", "hardware", "backend", "quant", "source_url",
            "source_name", "retrieved", "quote", "tps"]
PROV_OK = {"sourced", "community", "estimated", "unknown"}


def fail(msg):
    print("FAIL: %s" % msg)
    sys.exit(1)


def main():
    path = os.path.join(ROOT, "data", "records.csv")
    if not os.path.exists(path):
        fail("missing %s" % path)
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        fail("no records")

    today = datetime.date.today().isoformat()
    seen = set()
    errors = 0
    for i, r in enumerate(rows):
        for k in REQUIRED:
            if not (r.get(k) or "").strip():
                print("row %d (%s): missing %s" % (i, r.get("id"), k))
                errors += 1
        if r["id"] in seen:
            print("row %d: duplicate id %s" % (i, r["id"]))
            errors += 1
        seen.add(r["id"])
        try:
            tps = float(r["tps"])
            if tps <= 0:
                raise ValueError
        except ValueError:
            print("row %d (%s): bad tps %r" % (i, r["id"], r["tps"]))
            errors += 1
        if r["retrieved"] > today:
            print("row %d (%s): retrieved %s is in the future" % (i, r["id"], r["retrieved"]))
            errors += 1
        if not r["source_url"].startswith(("http://", "https://")):
            print("row %d (%s): bad source_url %r" % (i, r["id"], r["source_url"]))
            errors += 1
        if r["provenance"] not in PROV_OK:
            print("row %d (%s): bad provenance %r" % (i, r["id"], r["provenance"]))
            errors += 1
        # quote consistency: every recorded number must appear in the quoted row
        for k in ("tps", "ttft_s", "hardware", "model"):
            v = (r.get(k) or "").strip()
            if v and v not in r["quote"]:
                print("row %d (%s): %s=%r not in quote" % (i, r["id"], k, v))
                errors += 1

    if errors:
        print("%d errors in %d records" % (errors, len(rows)))
        sys.exit(1)

    hw = len(set(r["hardware"] for r in rows))
    models = len(set(r["model"] for r in rows))
    backends = len(set(r["backend"] for r in rows))
    prov = {}
    for r in rows:
        prov[r["provenance"]] = prov.get(r["provenance"], 0) + 1
    print("OK: %d records, %d hardware, %d models, %d backends; provenance %s"
          % (len(rows), hw, models, backends, dict(sorted(prov.items()))))


if __name__ == "__main__":
    main()
