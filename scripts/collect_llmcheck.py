#!/usr/bin/env python3
"""Deterministic collector: LLMCheck Apple Silicon LLM Benchmark Database.

Source: https://llmcheck.net/data/ (CC BY 4.0, machine-readable CSV+JSON).
Fetches the JSON, normalizes every row into Token Atlas canonical records
with full provenance (source URL, retrieval date, exact quoted values),
and writes data/records.csv + data/records.json.

Stdlib only. Responses are cached in .cache/.
"""
import csv
import hashlib
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
DATA = os.path.join(ROOT, "data")

DATASET_URL = "https://llmcheck.net/data/benchmarks.json"
SOURCE_NAME = "LLMCheck Apple Silicon LLM Benchmark Database (CC BY 4.0)"

FIELDNAMES = [
    "id", "model", "params", "quant", "hardware", "ram_gb", "backend",
    "ctx", "batch", "tps", "pp_tps", "ttft_s", "power_w", "date",
    "provenance", "source_url", "source_name", "retrieved", "quote", "notes",
]


def fetch(url: str, timeout: int = 30) -> bytes:
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, hashlib.sha256(url.encode()).hexdigest()[:24] + ".json")
    if os.path.exists(path):
        return open(path, "rb").read()
    req = urllib.request.Request(url, headers={"User-Agent": "tokatlas/0.1 (+https://tokatlas.github.io)"})
    body = urllib.request.urlopen(req, timeout=timeout).read()
    with open(path, "wb") as f:
        f.write(body)
    return body


def slug(s: str) -> str:
    s = s.lower().replace("+", " plus ")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "unknown"


def num(v):
    if v in (None, "", "null", "None"):
        return None
    try:
        f = float(v)
        return int(f) if f == int(f) else f
    except (TypeError, ValueError):
        return None


def main() -> None:
    body = fetch(DATASET_URL)
    src = json.loads(body)
    today = src.get("version") or "unknown"  # dataset version, used for freshness
    # retrieval date: prefer the local UTC date
    import datetime
    retrieved = datetime.date.today().isoformat()

    out = []
    for r in src["benchmarks"]:
        quote = ",".join(str(r[k]) for k in
                         ["model", "params", "quant", "chip", "ram", "engine", "tps", "ttft", "date"])
        row = {
            "id": slug("%s|%s|%s|%s|%s" % (
                "llmcheck", r["model"], r["chip"], r["quant"], r["engine"])),
            "model": r["model"],
            "params": r.get("params"),
            "quant": r.get("quant"),
            "hardware": r["chip"],
            "ram_gb": num(r.get("ram")),
            "backend": r["engine"],
            "ctx": None,
            "batch": None,
            "tps": num(r.get("tps")),
            "pp_tps": None,
            "ttft_s": num(r.get("ttft")),
            "power_w": None,
            "date": r.get("date"),
            "provenance": r.get("provenance", "unknown"),
            "source_url": r.get("source") or DATASET_URL,
            "source_name": SOURCE_NAME,
            "retrieved": retrieved,
            "quote": quote,
            "notes": ("LLMCheck model-based estimate (bandwidth model)"
                      if r.get("provenance") == "estimated" else None),
        }
        out.append(row)

    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "records.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        for row in out:
            w.writerow({k: ("" if row[k] is None else row[k]) for k in FIELDNAMES})
    with open(os.path.join(DATA, "records.json"), "w") as f:
        json.dump({"count": len(out), "retrieved": retrieved,
                   "dataset_version": today,
                   "source": DATASET_URL, "records": out}, f, indent=1, sort_keys=True)
    with open(os.path.join(DATA, "sources.json"), "w") as f:
        json.dump({"llmcheck": {"url": DATASET_URL, "license": "CC BY 4.0",
                                "retrieved": retrieved, "rows": len(out),
                                "dataset_version": today}}, f, indent=1, sort_keys=True)
    print("wrote %d records (retrieved %s, dataset version %s)" % (len(out), retrieved, today))


if __name__ == "__main__":
    sys.exit(main())
