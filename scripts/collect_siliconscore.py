#!/usr/bin/env python3
"""Deterministic collector: Silicon Score benchmark audit.

Source: https://siliconscore.com/benchmarks.json (per-row source_url; license
not stated in the dataset, so rows are used with per-row attribution and
recorded as such). Writes data/raw/siliconscore.json.
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

DATASET_URL = "https://siliconscore.com/benchmarks.json"
SOURCE_NAME = "Silicon Score benchmark audit"


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
    rows = json.loads(body)
    retrieved = datetime.date.today().isoformat()

    out = []
    for r in rows:
        verified = bool(r.get("verified"))
        notes = "source label: %s; verified=%s" % (r.get("source"), verified)
        prov = "sourced" if r.get("source_url") else ("community" if verified else "unknown")
        out.append({
            "id": slug("siliconscore|%s|%s|%s|ctx%s" % (
                r["chip"], r["model"], r.get("quantization"), r.get("context_tokens"))),
            "model": r["model"],
            "params": None,
            "quant": r.get("quantization"),
            "hardware": r["chip"],
            "ram_gb": r.get("ram_required_gb"),
            "backend": r.get("runtime"),
            "ctx": r.get("context_tokens"),
            "batch": None,
            "tps": r.get("avg_tok_s"),
            "pp_tps": r.get("prompt_eval_tok_s"),
            "ttft_s": r.get("time_to_first_token_s"),
            "power_w": None,
            "date": None,
            "provenance": prov,
            "source_url": r.get("source_url") or DATASET_URL,
            "source_name": SOURCE_NAME,
            "retrieved": retrieved,
            "quote": ("%s,%s,%s,ctx %s,%s tok/s" % (
                r["chip"], r["model"], r.get("quantization"),
                r.get("context_tokens"), r.get("avg_tok_s"))
                + (("; ttft %ss" % r["time_to_first_token_s"])
                   if r.get("time_to_first_token_s") is not None else "")),
            "notes": notes,
        })

    os.makedirs(os.path.join(ROOT, "data", "raw"), exist_ok=True)
    doc = {
        "source": {
            "name": SOURCE_NAME,
            "url": DATASET_URL,
            "license": "not stated; used with per-row attribution (source_url on each row)",
            "retrieved": retrieved,
            "note": "Apple Silicon rows; runtime is llamafile/MLX/Ollama/llama.cpp/LM Studio; "
                    "rows carry prompt eval and TTFT where published.",
        },
        "records": out,
    }
    with open(os.path.join(ROOT, "data", "raw", "siliconscore.json"), "w") as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print("wrote %d siliconscore records (retrieved %s)" % (len(out), retrieved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
