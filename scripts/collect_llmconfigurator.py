#!/usr/bin/env python3
"""Deterministic collector: LLM Configurator measured benchmarks.

Source: https://llmconfigurator.com/measured-benchmarks.json
(CC BY 4.0, self-declared in file). Curated-public rows compile third-party
published benchmarks (each row keeps publisher + sourceUrl); community rows
carry reviewedAt. Writes data/raw/llmconfigurator.json.
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

DATASET_URL = "https://llmconfigurator.com/measured-benchmarks.json"
SOURCE_NAME = "LLM Configurator measured benchmarks (CC BY 4.0)"

GPU_NAMES = {
    "rtx-4090": "RTX 4090",
    "rtx-3090": "RTX 3090",
    "rtx-3060": "RTX 3060",
    "rtx-4070": "RTX 4070",
    "rtx-4080": "RTX 4080",
    "rtx-4060": "RTX 4060",
    "apple-m3-max": "M3 Max",
    "apple-m4-max": "M4 Max",
}


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


def main() -> int:
    body = fetch(DATASET_URL)
    src = json.loads(body)
    retrieved = datetime.date.today().isoformat()

    out = []
    for e in src["entries"]:
        prov = "sourced" if e.get("provenance") == "curated-public" else "community"
        notes = "publisher: %s" % e["publisher"] if e.get("publisher") else None
        out.append({
            "id": slug("llmconfigurator|%s|%s|%s|ctx%s" % (
                e["gpuId"], e["variantId"], e.get("quant"), e.get("contextLength"))),
            "model": e["variantId"],
            "params": None,
            "quant": e.get("quant"),
            "hardware": GPU_NAMES.get(e["gpuId"], e["gpuId"]),
            "ram_gb": None,
            "backend": e.get("runtime") or "llama.cpp",
            "ctx": e.get("contextLength"),
            "batch": e.get("batchSize"),
            "tps": e.get("tokS"),
            "pp_tps": e.get("promptTokS"),
            "ttft_s": None,
            "power_w": e.get("measuredWatts"),
            "date": e.get("date"),
            "provenance": prov,
            "source_url": e.get("sourceUrl") or DATASET_URL,
            "source_name": SOURCE_NAME,
            "retrieved": retrieved,
            "quote": "%s,%s,%s,ctx %s,%s tok/s" % (
                e["gpuId"], e["variantId"], e.get("quant"),
                e.get("contextLength"), e.get("tokS")),
            "notes": notes,
        })

    os.makedirs(os.path.join(ROOT, "data", "raw"), exist_ok=True)
    doc = {
        "source": {
            "name": SOURCE_NAME,
            "url": DATASET_URL,
            "license": "CC BY 4.0 (self-declared in file)",
            "retrieved": retrieved,
            "generated_at": src.get("generatedAt"),
            "note": "curated-public rows are compiled from third-party published benchmarks (publisher + sourceUrl per row); community-submitted rows carry reviewedAt.",
        },
        "records": out,
    }
    with open(os.path.join(ROOT, "data", "raw", "llmconfigurator.json"), "w") as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print("wrote %d llmconfigurator records (retrieved %s)" % (len(out), retrieved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
