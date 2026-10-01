#!/usr/bin/env python3
"""Data checks for the Token Atlas dataset. Run before every push.

Validates data/records.csv: required fields, value sanity, uniqueness,
quote consistency (the exact quoted row must contain the recorded numbers),
and flag freshness (stored flags must match the deterministic recomputation
in scripts/flags.py). Exits non-zero on any failure.
"""
import csv
import datetime
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", str(s).lower())

REQUIRED = ["id", "model", "hardware", "backend", "quant", "source_url",
            "source_name", "retrieved", "quote"]
PROV_OK = {"sourced", "community", "estimated", "unknown"}
FLAG_OK = {"contradiction", "outlier"}


def fail(msg):
    print("FAIL: %s" % msg)
    sys.exit(1)


def flags_of(r):
    return [f for f in (r.get("flags") or "").split(",") if f]


def main():
    path = os.path.join(ROOT, "data", "records.csv")
    if not os.path.exists(path):
        fail("missing %s" % path)
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        fail("no records")

    errors = 0

    # flag freshness: stored flags must match the deterministic recomputation
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from flags import compute_flags
    jrows = [dict(r) for r in rows]
    expected = compute_flags(jrows)
    for i, r in enumerate(jrows):
        got = flags_of(r)
        want = expected.get(r["id"], [])
        if got != want:
            print("row %d (%s): flags %r != computed %r" % (i, r["id"], got, want))
            errors += 1

    today = datetime.date.today().isoformat()
    seen = set()
    for i, r in enumerate(rows):
        for k in REQUIRED:
            if not (r.get(k) or "").strip():
                print("row %d (%s): missing %s" % (i, r.get("id"), k))
                errors += 1
        if r["id"] in seen:
            print("row %d: duplicate id %s" % (i, r["id"]))
            errors += 1
        seen.add(r["id"])
        # speed: at least one of tps (decode) / pp_tps (prompt) must be > 0;
        # prefill-only reports carry pp_tps with tps left empty
        def _pos(key):
            v = (r.get(key) or "").strip()
            if not v:
                return True
            try:
                return float(v) > 0
            except ValueError:
                return False
        if not _pos("tps"):
            print("row %d (%s): bad tps %r" % (i, r.get("id"), r.get("tps")))
            errors += 1
        if not _pos("pp_tps"):
            print("row %d (%s): bad pp_tps %r" % (i, r.get("id"), r.get("pp_tps")))
            errors += 1
        if not (r.get("tps") or "").strip() and not (r.get("pp_tps") or "").strip():
            print("row %d (%s): needs tps or pp_tps > 0" % (i, r.get("id")))
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
        for fl in flags_of(r):
            if fl not in FLAG_OK:
                print("row %d (%s): bad flag %r" % (i, r["id"], fl))
                errors += 1
        # quote consistency: numbers must appear verbatim; identity fields must
        # appear as a normalized substring (hardware may be a mapped name)
        # thousands separators in the quote are ignored, as in check_quotes
        quote_nums = r["quote"].replace(",", "")
        for k in ("tps", "ttft_s"):
            v = (r.get(k) or "").strip()
            if v and v not in quote_nums:
                print("row %d (%s): %s=%r not in quote" % (i, r["id"], k, v))
                errors += 1
        for k in ("hardware", "model"):
            v = (r.get(k) or "").strip()
            if v and norm(v) not in norm(r["quote"]):
                print("row %d (%s): %s=%r not in quote" % (i, r["id"], k, v))
                errors += 1
        # each llama-bench run is its own record: a test appearing twice in one
        # quote means two runs were collapsed into one record
        tests = re.findall(r"\b(pp\d{1,4}|tg\d{1,4})\b", r["quote"])
        if len(tests) != len(set(tests)):
            print("row %d (%s): quote has duplicate test tokens %r" % (i, r["id"], tests))
            errors += 1
        for k in ("pp_tokens", "tg_tokens"):
            v = (r.get(k) or "").strip()
            if v and not (v.isdigit() and int(v) > 0):
                print("row %d (%s): bad %s %r" % (i, r["id"], k, v))
                errors += 1

    if errors:
        print("%d errors in %d records" % (errors, len(rows)))
        sys.exit(1)

    hw = len(set(r["hardware"] for r in rows))
    models = len(set(r["model"] for r in rows))
    backends = len(set(r["backend"] for r in rows))
    prov = {}
    flg = {}
    for r in rows:
        prov[r["provenance"]] = prov.get(r["provenance"], 0) + 1
        for fl in flags_of(r):
            flg[fl] = flg.get(fl, 0) + 1
    print("OK: %d records, %d hardware, %d models, %d backends; provenance %s; flags %s"
          % (len(rows), hw, models, backends, dict(sorted(prov.items())),
             dict(sorted(flg.items())) or "none"))


if __name__ == "__main__":
    main()
