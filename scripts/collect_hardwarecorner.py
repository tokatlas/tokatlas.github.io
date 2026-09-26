#!/usr/bin/env python3
"""Deterministic collector: Hardware Corner GPU LLM benchmarks (hub pages).

https://www.hardware-corner.net/gpu-llm-benchmarks/ indexes one hub page per
GPU (e.g. /gpu-llm-benchmarks/rtx-4090/). Each hub page has two tables under
"Local LLM Benchmarks", labeled by adjacent spans:
- "Prompt Processing" (t/s per context column)
- "Token Generation" (t/s per context column)
Row labels carry model + quant, e.g. "Qwen3 8B (Q4_K)", "gpt-oss 20B (MXFP4)".
Context columns are "4k Ctx" ... "256k Ctx" (k = 1024).

One record per (model, quant, context): tps from the generation table,
pp_tps from the prompt table (joined on the row label). Dash cells are not
recorded (the site marks unmeasured context columns with a dash). License is not stated on the site; rows carry per-row source URLs
and the exact quoted cell values. Runtime is llama.cpp per the site's
benchmark methodology (their benchmark articles document llama-bench).
-> data/raw/hardwarecorner.json
"""
import datetime
import hashlib
import html as htmlmod
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
INDEX_URL = "https://www.hardware-corner.net/gpu-llm-benchmarks/"
SOURCE_NAME = "Hardware Corner GPU LLM benchmarks (per-row attribution)"


def fetch(url: str, timeout: int = 30) -> bytes:
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, hashlib.sha256(url.encode()).hexdigest()[:24] + ".html")
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


def clean(cell: str) -> str:
    cell = re.sub(r"<[^>]+>", "", cell)
    return htmlmod.unescape(cell).strip()


def labeled_tables(page: str):
    """Yield (label, rows) for the two benchmark tables, by the span label
    in the markup immediately preceding each table."""
    out = []
    for m in re.finditer(r"<table.*?</table>", page, re.S):
        before = page[max(0, m.start() - 3000):m.start()]
        best = None
        for cand in ("Prompt Processing", "Token Generation"):
            idx = before.rfind(cand)
            if idx != -1 and (best is None or idx > best[0]):
                best = (idx, cand)
        label = best[1] if best else None
        rows = []
        for tr in re.findall(r"<tr.*?</tr>", m.group(0), re.S):
            cells = [clean(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, re.S)]
            if cells:
                rows.append(cells)
        if label and rows:
            out.append((label, rows))
    return out


def ctx_value(header: str):
    m = re.fullmatch(r"(\d+)k Ctx", header.strip())
    if not m:
        return None
    return int(m.group(1)) * 1024


def num(cell: str):
    v = cell.replace(",", "").strip()
    try:
        return float(v)
    except ValueError:
        return None


def split_label(label: str):
    m = re.fullmatch(r"(.*?)\s*\((\w+)\)\s*", label)
    if m:
        return m.group(1).strip(), m.group(2)
    return label.strip(), None


def main() -> int:
    retrieved = datetime.date.today().isoformat()
    index = fetch(INDEX_URL).decode("utf-8", "replace")

    table = re.search(r"<table.*?</table>", index, re.S)
    if not table:
        print("no table on index page; layout may have changed")
        return 1
    rows = []
    hrefs = re.findall(r'<a[^>]*href="([^"]+)"', table.group(0))
    for tr in re.findall(r"<tr.*?</tr>", table.group(0), re.S):
        cells = [clean(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, re.S)]
        if cells and cells[0] != "GPU" and len(cells) >= 3:
            rows.append(cells)
    if not rows:
        print("no GPU rows on index page; layout may have changed")
        return 1

    records = []
    for i, r in enumerate(rows):
        gpu, vram_s = r[0], r[1]
        url = hrefs[i] if i < len(hrefs) else None
        if not url:
            continue
        if not url.startswith("http"):
            url = "https://www.hardware-corner.net" + (url if url.startswith("/") else "/" + url)
        vram = None
        m = re.search(r"([\d.]+)", vram_s)
        if m:
            vram = float(m.group(1))
        page = fetch(url).decode("utf-8", "replace")

        pp_tbl = gen_tbl = None
        for label, tbl in labeled_tables(page):
            if label == "Prompt Processing":
                pp_tbl = tbl
            elif label == "Token Generation":
                gen_tbl = tbl
        if gen_tbl is None:
            print("skip %s: no labeled tables" % gpu)
            continue

        ctxs = [ctx_value(h) for h in gen_tbl[0][1:]]
        pp_by_label = {}
        if pp_tbl is not None:
            for row in pp_tbl[1:]:
                pp_by_label[row[0]] = row[1:]
        for row in gen_tbl[1:]:
            row_label, quant = split_label(row[0])
            if not quant:
                continue
            model = row_label
            params_m = re.search(r"([\d.]+B)\b", model)
            params = params_m.group(1) if params_m else None
            gen_vals = row[1:]
            pp_vals = pp_by_label.get(row[0])
            for j, ctx in enumerate(ctxs):
                if ctx is None or j >= len(gen_vals):
                    continue
                gcell = gen_vals[j].strip()
                if gcell in ("", "\u2014", "-"):
                    continue
                pcell = pp_vals[j].strip() if pp_vals is not None and j < len(pp_vals) else ""
                pnum = num(pcell)
                quote = "%s, %s, %s: generation %s t/s" % (gpu, row[0], gen_tbl[0][1 + j], gcell)
                if pnum is not None:
                    quote += ", prompt processing %s t/s" % pcell
                notes = "Hardware Corner %s hub page; llama.cpp runtime per the site's benchmark methodology" % gpu
                records.append({
                    "id": slug("hardwarecorner|%s|%s|ctx%s" % (gpu, row[0], ctx)),
                    "model": model,
                    "params": params,
                    "quant": quant,
                    "hardware": gpu,
                    "ram_gb": vram,
                    "backend": "llama.cpp",
                    "ctx": ctx,
                    "batch": None,
                    "tps": num(gcell),
                    "pp_tps": pnum,
                    "ttft_s": None,
                    "power_w": None,
                    "date": None,
                    "provenance": "sourced",
                    "source_url": url,
                    "source_name": SOURCE_NAME,
                    "retrieved": retrieved,
                    "quote": quote,
                    "notes": notes,
                })

    os.makedirs(os.path.join(ROOT, "data", "raw"), exist_ok=True)
    doc = {
        "source": {
            "name": SOURCE_NAME,
            "url": INDEX_URL,
            "license": "not stated; used with per-row attribution (source_url on each row)",
            "retrieved": retrieved,
            "note": "hub pages: prompt processing and token generation t/s per context column (4k-256k, k=1024); model + quant as labeled in the row; runtime llama.cpp per the site's benchmark methodology; dashes in the source are not records",
        },
        "records": records,
    }
    with open(os.path.join(ROOT, "data", "raw", "hardwarecorner.json"), "w") as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print("wrote %d hardwarecorner records from %d GPUs (retrieved %s)"
          % (len(records), len(rows), retrieved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
