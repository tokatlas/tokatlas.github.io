#!/usr/bin/env python3
"""Collect llama.cpp GitHub Discussions performance scoreboards.

Targets the official per-backend performance threads. Each post in those
threads is a primary-source benchmark report; the collector parses
llama-bench style tables from every post plus the chip name from the post
text. Cached fetches in .cache/.

Threads (discussion number: backend label):
  4167   Apple Silicon (Metal)
  15013  NVIDIA CUDA
  15021  AMD ROCm
  10879  Vulkan (all vendors)
  23313  Intel SYCL
"""
import hashlib
import html
import json
import os
import re
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
UA = "tokatlas/0.1 (+https://tokatlas.github.io)"
BASE = "https://github.com/ggml-org/llama.cpp/discussions"
RETRIEVED = "2026-09-26"

THREADS = {
    4167: "Apple Silicon",
    15013: "NVIDIA CUDA",
    15021: "AMD ROCm",
    10879: "Vulkan",
    23313: "Intel SYCL",
}

ANCHOR_RE = re.compile(r'id="discussioncomment-(\d+)"[^>]*data-url="([^"]+)"', re.S)
DATE_RE = re.compile(r'<relative-time[^>]*datetime="([^"]+)"')
TABLE_RE = re.compile(r"<table[^>]*>(.*?)</table>", re.S)
TR_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
TD_RE = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S)
NEXT_PAGE_RE = re.compile(r'action="(/ggml-org/llama\.cpp/discussions/\d+/pages\?after=[^"]+)"')
HEADING_RE = re.compile(r"<h[1-6][^>]*>(.*?)</h[1-6]>", re.S)

QUANT_TAIL_RE = re.compile(
    r"\s*((?:Q\d_K(?:_S|_M|_L)?|Q\d_[0-8]|F16|BF16|F32"
    r"|IQ\d(?:_XXS|_XS|_S|_NL|_M|_L)?|MTP)"
    r"(?:\s*-\s*(?:Medium|Small|Large|\d+(?:\.\d+)?\s*bpw))?)\s*$")

CHIP_PATTERNS = {
    "Apple Silicon": [
        r"M[1-5](?: Max| Pro| Ultra)?\s*\d+\s?GB",
        r"M[1-5](?: Max| Pro| Ultra)?\s*\d+\+\d+",
        r"M[1-5](?: Max| Pro| Ultra)?\b(?![0-9A-Za-z])",
    ],
    "NVIDIA CUDA": [
        r"(?:GeForce |Quadro |NVIDIA )?RTX\s?(?:[3-6]\d{3})(?:\s?(?:Super|Ti|Mobile|Max-Q|Blackwell))?",
        r"\b(?:RTX\s?PRO\s?\d{4}|A[1-9]\d{2}|T4|V100|P100|B[12]\d{2,3}|H100|H200|B200|B300|GB200|GB10)\b",
    ],
    "AMD ROCm": [
        r"Radeon\s?(?:RX\s?)?\d{3,4}\s?[A-Z]{0,3}",
        r"\bMI[123]\d{3}\b",
    ],
    "Vulkan": [
        r"RTX\s?\d{4}(?:\s?(?:Super|Ti|Mobile|Max-Q))?",
        r"Radeon\s?(?:RX\s?)?\d{3,4}\s?[A-Z]{0,3}",
        r"\bArc\s?[ABK]\d{3}\b",
        r"\bIris\s?Xe\b",
        r"M[1-5](?: Max| Pro| Ultra)?\s*\d+\s?GB",
        r"M[1-5](?: Max| Pro| Ultra)?\b(?![0-9A-Za-z])",
        r"\b(?:A[1-9]\d{2}|T4|V100|P100|B[12]\d{2,3}|H100|H200|B200|B300|GB200|GB10)\b",
    ],
    "Intel SYCL": [
        r"\bArc\s?[ABK]\d{3}\b",
        r"\bIris\s?Xe\b(?:\s?\d{1,3})?",
        r"\bUHD\s?\d{3}\b",
    ],
}

BACKEND_MAP = [
    (r"MTL|METAL", "llama.cpp (Metal)"),
    (r"CUDA", "llama.cpp (CUDA)"),
    (r"VULKAN", "llama.cpp (Vulkan)"),
    (r"ROCm|HIP", "llama.cpp (ROCm)"),
    (r"SYCL|ONEAPI|oneDNN", "llama.cpp (SYCL)"),
    (r"OPENVINO", "llama.cpp (OpenVINO)"),
    (r"OPENCL", "llama.cpp (OpenCL)"),
    (r"RPC", "llama.cpp (RPC)"),
    (r"^CPU|BLAS", "llama.cpp (CPU)"),
]


def fetch(url):
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha256(url.encode()).hexdigest()
    path = os.path.join(CACHE, key)
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
        tmp = path + ".tmp"
        with open(tmp, "wb") as f:
            f.write(body)
        os.replace(tmp, path)
        time.sleep(1.5)
    with open(path, "rb") as f:
        return f.read().decode("utf-8", "replace")


def clean(cell):
    return html.unescape(re.sub(r"<[^>]+>", " ", cell)).strip()


def strip_templates(fragment):
    while True:
        m = re.search(r"<template[^>]*>.*?</template>", fragment, re.S)
        if not m:
            return fragment
        fragment = fragment[:m.start()] + " " + fragment[m.end():]


def text_of(fragment):
    t = re.sub(r"<[^>]+>", " ", fragment)
    return html.unescape(t)


def table_rows(fragment):
    out = []
    for m in TABLE_RE.finditer(fragment):
        tbl = m.group(1)
        rows = []
        for tr in TR_RE.finditer(tbl):
            cells = [clean(c) for c in TD_RE.findall(tr.group(1))]
            if any(cells):
                rows.append(cells)
        if rows:
            out.append((m.start(), rows))
    return out


def discussion_items(num):
    """Yield (author, date, comment_url, fragment) for every post in the thread."""
    urls = [BASE + "/" + str(num)]
    seen = set()
    while urls:
        url = urls.pop(0)
        if url in seen:
            continue
        seen.add(url)
        h = fetch(url)
        anchors = list(ANCHOR_RE.finditer(h))
        if url == BASE + "/" + str(num):
            # original post: timeline content before the first comment anchor
            op_frag = h[:anchors[0].start()] if anchors else h
            dm = DATE_RE.search(strip_templates(op_frag))
            op_date = dm.group(1)[:10] if dm else None
            if op_date and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", op_date):
                op_date = None
            yield ("op", op_date, "%s/%d" % (BASE, num), op_frag)
        for i, m in enumerate(anchors):
            end = anchors[i + 1].start() if i + 1 < len(anchors) else len(h)
            frag = h[m.end():end]
            cid = m.group(1)
            # comment date: the permalink in the item header (exact per comment);
            # template dialogs contain a literal {{datetime}} placeholder, so a
            # blind first-match on relative-time is not safe
            dm = re.search(
                r'id="discussioncomment-%s-permalink".*?'
                r'<relative-time[^>]*datetime="([^"]+)"' % cid, frag, re.S)
            if not dm:
                dm = DATE_RE.search(strip_templates(frag))
            date = dm.group(1)[:10] if dm else None
            if date and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                date = None
            am = re.search(r'<span class="Truncate-text text-bold">([^<]+)</span>', frag)
            if not am:
                am = re.search(r'class="author[^"]*">([^<]+)</a>', frag)
            url = "%s/%d#discussioncomment-%s" % (BASE, num, cid)
            yield (am.group(1).strip() if am else None,
                   date,
                   url,
                   frag)
        pm = NEXT_PAGE_RE.search(h)
        if pm:
            urls.append("https://github.com" + html.unescape(pm.group(1)))
        if len(seen) > 80:
            break


def split_model_quant(model_cell):
    m = QUANT_TAIL_RE.search(model_cell)
    if m and m.start() > 0:
        return model_cell[:m.start()].rstrip(), re.sub(r"\s+", " ", m.group(1)).strip()
    return model_cell, None


def chip_in(text, thread_label):
    for pat in CHIP_PATTERNS.get(thread_label, []):
        m = re.search(pat, text)
        if m:
            return m.group(0).strip()
    return None


def backend_of(cell):
    up = cell.upper().strip()
    if not up or set(up) <= {"-"}:
        return "llama.cpp"
    for pat, name in BACKEND_MAP:
        if re.search(pat, up):
            return name
    return "llama.cpp"


def value_of(cell):
    m = re.match(r"([\d.]+)", cell.replace(",", ""))
    if m:
        return float(m.group(1))
    return None


def body_parts(fragment):
    """Comment bodies sit in <td class=...comment-body...> wrappers; return their HTML."""
    parts = []
    for m in re.finditer(r"<td[^>]*comment-body[^>]*>", fragment):
        depth = 1
        i = m.end()
        while i < len(fragment):
            nxt_open = fragment.find("<td", i)
            nxt_close = fragment.find("</td>", i)
            if nxt_close == -1:
                break
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                i = nxt_open + 3
            else:
                depth -= 1
                if depth == 0:
                    parts.append(fragment[m.end():nxt_close])
                    break
                i = nxt_close + 5
    return parts


def extract(frag, comment_url, thread_label, thread_num, comment_id):
    """Pull benchmark rows out of one post fragment."""
    rows = []
    frag = strip_templates(frag)
    parts = body_parts(frag)
    plain = re.sub(r"\s+", " ", " ".join(
        text_of(re.sub(r"<table.*?</table>", " ", p, flags=re.S)) for p in parts))
    for part in parts:
        context = [(m.start(), clean(m.group(1))) for m in HEADING_RE.finditer(part)]
        context += [(m.start(), clean(m.group(1))) for m in re.finditer(r"<p[^>]*>(.*?)</p>", part, re.S)]
        heads = [(m.start(), clean(m.group(1))) for m in HEADING_RE.finditer(part)]

        def context_before(pos):
            before = [t for p, t in context if p < pos]
            return before[-1] if before else ""

        def nearest_hw(pos):
            for hp, ht in reversed([x for x in heads if x[0] < pos]):
                c = chip_in(ht, thread_label)
                if c:
                    return c
            return chip_in(plain, thread_label)

        for pos, tbl in table_rows(part):
            hdr = [h.lower() for h in tbl[0]]
            if "test" in hdr and "t/s" in hdr:
                # old llama-bench: one row per test (pp*/tg*)
                idx = {c.lower(): i for i, c in enumerate(tbl[0])}
                model_i = idx.get("model", 0)
                merged = {}
                for r in tbl[1:]:
                    if len(r) < len(tbl[0]):
                        continue
                    model_cell = r[model_i] if model_i < len(r) else ""
                    if not model_cell or re.fullmatch(r"\d+", model_cell.strip()):
                        continue
                    test_raw = r[idx["test"]]
                    tm = re.fullmatch(r"(pp|tg)\s*(\d+)", test_raw)
                    val = value_of(r[idx["t/s"]])
                    if val is None or not tm:
                        continue
                    test = tm.group(1) + tm.group(2)
                    model, quant = split_model_quant(model_cell)
                    key = (model, quant, r[idx.get("backend", 0)] if "backend" in idx and idx["backend"] < len(r) else "",
                           r[idx.get("threads", idx.get("ngl", 0))] if ("threads" in idx or "ngl" in idx) and max(idx.get("threads", 0), idx.get("ngl", 0)) < len(r) else "")
                    ent = merged.setdefault(key, {"model": model, "quant": quant,
                                                  "backend": key[2], "threads": key[3], "cells": []})
                    ent[test] = (val, r[idx["t/s"]])
                    ent["cells"].append((model_cell or key[0], test, r[idx["t/s"]]))
                for key, ent in merged.items():
                    if "tg128" not in ent and "tg256" not in ent and "tg64" not in ent:
                        continue
                    tgk = [k for k in ent if k.startswith("tg")]
                    ppk = [k for k in ent if k.startswith("pp")]
                    if not tgk:
                        continue
                    tgv, tgs = ent[tgk[0]]
                    pp = ent.get(ppk[0], (None, "")) if ppk else (None, "")
                    quote = "; ".join("%s | %s | %s" % c for c in ent["cells"])
                    hw = nearest_hw(pos)
                    if hw:
                        quote = hw + "; " + quote
                    rows.append({
                        "model": ent["model"], "quant": ent["quant"],
                        "backend": backend_of(ent["backend"]),
                        "ctx": int(tgk[0][2:]), "tps": tgv,
                        "pp_tps": pp[0],
                        "quote": quote,
                        "notes": "threads=%s" % ent["threads"] if ent["threads"] else None,
                        "source_url": comment_url,
                        "hardware": hw,
                    })
            elif any(re.fullmatch(r"pp\d+", h) for h in hdr) and any(re.fullmatch(r"tg\d+", h) for h in hdr):
                # new llama-bench: pp/tg in one row
                if "model" not in hdr or "backend" not in hdr:
                    continue
                idx = {c.lower(): i for i, c in enumerate(tbl[0])}
                type_i = idx.get("type")
                for r in tbl[1:]:
                    if len(r) < len(tbl[0]):
                        continue
                    model_cell = r[idx["model"]]
                    if not model_cell or re.fullmatch(r"\d+", model_cell.strip()):
                        continue
                    model, q1 = split_model_quant(model_cell)
                    quant = None
                    if type_i is not None and type_i < len(r):
                        quant = re.sub(r"\[.*\]", "", r[type_i]).strip() or q1
                        quant = quant or q1
                    tps = None
                    pp = None
                    quote = model_cell
                    for h in hdr[1:]:
                        if re.fullmatch(r"tg\d+", h):
                            v, raw = value_of(r[idx[h]]), r[idx[h]]
                            if tps is None and v is not None:
                                tps = v
                            quote = quote + "; " + h + ": " + raw
                            ctx = int(h[2:])
                        elif re.fullmatch(r"pp\d+", h):
                            v, raw = value_of(r[idx[h]]), r[idx[h]]
                            if v is not None:
                                pp = v
                                quote = quote + "; " + h + ": " + raw
                    if tps is None:
                        continue
                    hw = nearest_hw(pos)
                    if hw:
                        quote = hw + "; " + quote
                    rows.append({
                        "model": model, "quant": quant or "as-published",
                        "backend": backend_of(r[idx["backend"]]),
                        "ctx": ctx, "tps": tps, "pp_tps": pp,
                        "quote": quote, "notes": None, "source_url": comment_url,
                        "hardware": hw,
                    })
            else:
                # curated summary: hardware row labels, per-quant PP/TG columns
                hdr_orig = tbl[0]
                if not any(re.search(r"\bBW\b|\[GB/s\]", c) for c in hdr_orig):
                    continue
                heading = context_before(pos)
                model = heading if (re.fullmatch(r"[A-Za-z0-9 .\-/()]{2,40}", heading)
                                    and any(c.isdigit() for c in heading)) else "as-published"
                cores_i = None
                for i, h2 in enumerate(hdr_orig):
                    if re.fullmatch(r"GPU\s+Cores", h2.strip()):
                        cores_i = i
                        break
                for r in tbl[1:]:
                    hw = r[0].strip()
                    hw = re.sub(r"^[^\w]+\s*", "", hw)  # status emoji / markers
                    hw = re.sub(r"\s+[0-9a-f]{7,}\b.*$", "", hw)  # trailing commit
                    hw = re.sub(r"\s+\d$", "", hw)  # trailing footnote digit
                    hw = re.sub(r"\s+", " ", hw).strip()
                    if not hw:
                        continue
                    if cores_i is not None and cores_i < len(r) \
                            and re.fullmatch(r"\d+", r[cores_i].strip()):
                        hw = "%s (%s GPU)" % (hw, r[cores_i].strip())
                    # collect (PP, TG) pairs per quant across the row
                    for i, h in enumerate(hdr_orig):
                        mh = re.match(r"([A-Z0-9_]+)\s*(PP|TG)\s*\[t/s\]", h)
                        if not mh or i >= len(r):
                            continue
                        quant, kind = mh.group(1), mh.group(2)
                        if kind == "PP":
                            continue
                        tg_val, tg_raw = value_of(r[i]), r[i]
                        if tg_val is None:
                            continue
                        pp_val, pp_raw, pp_hdr = None, None, None
                        for j, h2 in enumerate(hdr_orig):
                            m2 = re.match(r"([A-Z0-9_]+)\s*PP\s*\[t/s\]", h2)
                            if m2 and m2.group(1) == quant and j < len(r):
                                pp_val, pp_raw, pp_hdr = value_of(r[j]), r[j], h2
                                break
                        if pp_val is not None:
                            quote = "%s, %s, %s: %s; %s: %s" % (
                                hw, model, pp_hdr, pp_raw, h, tg_raw)
                            tps_out, pp_out = tg_val, pp_val
                        else:
                            quote = "%s, %s, %s: %s" % (hw, model, h, tg_raw)
                            tps_out, pp_out = tg_val, None
                        rows.append({
                            "model": model, "quant": quant,
                            "backend": "llama.cpp (Metal)" if thread_label == "Apple Silicon" else "llama.cpp",
                            "ctx": None, "tps": tps_out, "pp_tps": pp_out,
                            "hardware": hw, "quote": quote, "notes": None,
                            "source_url": comment_url})
    # attach hardware from post text (curated rows already carry their row label)
    for row in rows:
        if row.get("hardware"):
            continue
        hw = chip_in(plain, thread_label)
        if hw:
            row["hardware"] = hw
            row["quote"] = hw + "; " + row["quote"]
    return rows


def main():
    records = []
    for num, label in sorted(THREADS.items()):
        n_posts = 0
        for author, date, url, frag in discussion_items(num):
            n_posts += 1
            rows = extract(frag, url, label, num, None)
            for row in rows:
                if not row.get("hardware"):
                    continue
                cid = url.split("#discussioncomment-")[-1]
                slug_src = "lc-disc-%d-c%s" % (num, cid)
                base = "%s-%s-%s" % (slug_src, re.sub(r"[^a-z0-9]+", "", row["model"].lower()).strip("-")[:24],
                                     row.get("quant") or "unknown")
                rec_id = base
                n = 2
                while any(r["id"] == rec_id for r in records):
                    rec_id = "%s-%d" % (base, n)
                    n += 1
                records.append({
                    "id": rec_id,
                    "model": row["model"],
                    "params": None,
                    "quant": row.get("quant") or "as-published",
                    "hardware": row["hardware"],
                    "ram_gb": None,
                    "backend": row["backend"],
                    "ctx": row.get("ctx"),
                    "batch": None,
                    "tps": row["tps"],
                    "pp_tps": row.get("pp_tps"),
                    "ttft_s": None,
                    "power_w": None,
                    "date": date,
                    "provenance": "community",
                    "source_url": row["source_url"],
                    "source_name": "llama.cpp discussions #%d (performance thread, %s)" % (num, label),
                    "retrieved": RETRIEVED,
                    "quote": row["quote"],
                    "notes": row.get("notes"),
                })
        print("thread %d (%s): %d posts, %d candidate rows so far" % (num, label, n_posts, len(records)), flush=True)
    out = {
        "source": {
            "name": "llama.cpp GitHub Discussions performance threads",
            "note": "Primary-source llama-bench posts from the official per-backend performance threads (#4167 Apple Silicon, #15013 CUDA, #15021 ROCm, #10879 Vulkan, #23313 SYCL). Hardware is taken from the post text; rows without a detectable chip are skipped.",
            "retrieved": RETRIEVED,
            "url": BASE,
        },
        "records": records,
    }
    path = os.path.join(ROOT, "data", "raw", "llamacpp_discussions.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print("wrote %s with %d records" % (path, len(records)))


if __name__ == "__main__":
    main()
