#!/usr/bin/env python3
"""Deterministic collector: LLMCheck Apple Silicon LLM Benchmark Database.

Source: https://llmcheck.net/data/ (CC BY 4.0, machine-readable CSV+JSON).
Writes data/raw/llmcheck.json (canonical records + source metadata).
Run merge_data.py afterwards to combine sources into data/records.*.

Stdlib only. Responses are cached in .cache/.
"""
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")

DATASET_URL = "https://llmcheck.net/data/benchmarks.json"
SOURCE_NAME = "LLMCheck Apple Silicon LLM Benchmark Database (CC BY 4.0)"


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


def main() -> int:
    body = fetch(DATASET_URL)
    src = json.loads(body)
    retrieved = datetime.date.today().isoformat()

    out = []
    for r in src["benchmarks"]:
        quote = ",".join(str(r[k]) for k in
                         ["model", "params", "quant", "chip", "ram", "engine", "tps", "ttft", "date"])
        out.append({
            "id": slug("llmcheck|%s|%s|%s|%s" % (r["model"], r["chip"], r["quant"], r["engine"])),
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
        })

    os.makedirs(os.path.join(ROOT, "data", "raw"), exist_ok=True)
    doc = {
        "source": {
            "name": SOURCE_NAME,
            "url": DATASET_URL,
            "license": "CC BY 4.0",
            "retrieved": retrieved,
            "dataset_version": src.get("version"),
            "note": "Rows are estimates (244), sourced (9), or community (5) per the source's own provenance field.",
        },
        "records": out,
    }
    with open(os.path.join(ROOT, "data", "raw", "llmcheck.json"), "w") as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print("wrote %d llmcheck records (retrieved %s)" % (len(out), retrieved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
