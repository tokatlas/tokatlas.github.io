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
RETRIEVED = "2026-09-27"

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
        r"\b(?:RTX\s?PRO\s?\d{4}|A[1-9]\d{2,4}|T4|V100|P100|B[12]\d{2,3}|H100|H200|B200|B300|GB200|GB10)\b",
    ],
    "AMD ROCm": [
        r"Radeon\s?(?:RX\s?)?\d{3,4}\s?[A-Z]{0,3}",
        r"\bMI[123]\d{3}\b",
    ],
    "Vulkan": [
        r"RTX\s?\d{4}(?:\s?(?:Super|Ti|Mobile|Max-Q))?",
        r"Radeon\s?(?:RX\s?)?\d{3,4}\s?[A-Z]{0,3}",
        r"\bArc(?:\(tm\))?\s?(?:Pro\s?)?[ABK]\d{2,3}\b",
        r"\bIris\s?Xe\b",
        r"M[1-5](?: Max| Pro| Ultra)?\s*\d+\s?GB",
        r"M[1-5](?: Max| Pro| Ultra)?\b(?![0-9A-Za-z])",
        r"\b(?:A[1-9]\d{2,4}|T4|V100|P100|B[12]\d{2,3}|H100|H200|B200|B300|GB200|GB10)\b",
    ],
    "Intel SYCL": [
        r"\bArc(?:\(tm\))?\s?(?:Pro\s?)?[ABK]\d{2,3}\b",
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


def text_tables(fragment):
    """Markdown-style pipe tables pasted as plain text inside <pre>/<code>.

    Many posts paste llama-bench output verbatim; GitHub renders it as
    text, so TABLE_RE never sees it. We only accept blocks whose header
    line looks like a llama-bench header (test + t/s, or ppNNN/tgNNN
    columns) so random pipe text does not become a table.
    """
    out = []
    for m in re.finditer(r"<pre[^>]*>(.*?)</pre>|<code[^>]*>(.*?)</code>",
                         fragment, re.S):
        block = m.group(1) if m.group(1) is not None else m.group(2)
        block_abs = m.start(1) if m.group(1) is not None else m.start(2)
        txt = html.unescape(re.sub(r"<[^>]+>", " ", block))
        lines = txt.splitlines()
        # absolute offset of each line (tags are rare inside <pre>/<code>)
        line_off, o = [], 0
        for ln in txt.splitlines():
            i = txt.find(ln, o)
            line_off.append(block_abs + (i if i >= 0 else 0))
            o = i + len(ln) + 1
        runs = []  # (first_line_index, lines)
        cur, cur_start = [], None
        for i, ln in enumerate(lines):
            s = ln.strip()
            if s.startswith("|") and s.count("|") >= 6:
                if cur_start is None:
                    cur_start = i
                cur.append(s)
            else:
                if cur:
                    runs.append((cur_start, cur))
                    cur, cur_start = [], None
        if cur:
            runs.append((cur_start, cur))
        last_hdr = None
        for start_i, run in runs:
            cells_rows = []
            for s in run:
                cells = [c.strip() for c in s.strip("|").split("|")]
                if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
                    continue  # separator line
                cells_rows.append(cells)
            if not cells_rows:
                continue
            low0 = [c.lower() for c in cells_rows[0]]
            if "t/s" in low0 or "test" in low0:
                hdr, body = cells_rows[0], cells_rows[1:]
            elif last_hdr is not None and len(cells_rows[0]) == len(last_hdr):
                # continuation of the previous table (header not repeated)
                hdr, body = last_hdr, cells_rows
            else:
                continue
            if body:
                preceding = " ".join(l.strip() for l in lines[:start_i])
                out.append((line_off[start_i], [hdr] + body, preceding))
                last_hdr = hdr
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


def _clean(chip):
    chip = re.sub(r"\s*\(tm\)\s*", " ", chip, flags=re.I)
    return re.sub(r"\s+", " ", chip).strip()


def _match_chip(text, pat, m):
    chip = m.group(0)
    ext = re.match(r"\s+(Super|Blackwell|Mobile)\b", text[m.end():], re.I)
    if ext:
        chip += " " + ext.group(1).capitalize()
    return _clean(chip)


def chip_in(text, thread_label):
    for pat in CHIP_PATTERNS.get(thread_label, []):
        m = re.search(pat, text)
        if m:
            return _match_chip(text, pat, m)
    return None


def nearest_chip(text, thread_label):
    """Chip mentioned closest to the end of the text, i.e. the one
    describing the machine the table that follows was run on."""
    best_end, best = -1, None
    for pat in CHIP_PATTERNS.get(thread_label, []):
        for m in re.finditer(pat, text):
            if m.end() > best_end:
                best_end, best = m.end(), _match_chip(text, pat, m)
    return best


def backend_of(cell):
    up = cell.upper().strip()
    if not up or set(up) <= {"-"}:
        return "llama.cpp"
    for pat, name in BACKEND_MAP:
        if re.search(pat, up, re.I):
            return name
    return "llama.cpp"


def dev_backend(dev):
    """The dev column names the device a test ran on ('Vulkan0', 'CUDA0',
    'ROCm1', 'SYCL0/SYCL1'); it is authoritative over the backend cell,
    which only describes the build."""
    d = dev.upper()
    if "VULKAN" in d:
        return "llama.cpp (Vulkan)"
    if "CUDA" in d:
        return "llama.cpp (CUDA)"
    if "ROCM" in d or "HIP" in d:
        return "llama.cpp (ROCm)"
    if "SYCL" in d:
        return "llama.cpp (SYCL)"
    return None


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


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def power_entries(part):
    """Measured power reported in post prose, as (pos, label, kind, value, desc).

    kind is 'sys' (whole-system watts for the tg test), 'rate' (watts per
    t/s; multiply by the row's tps), or 'watts' (device watts).
    Positions are offsets into the raw part HTML so they line up with
    table positions; the text is matched on a tag-flattened copy.
    """
    flat_chars, pos_map = [], []
    for mm in re.finditer(r"<[^>]+>|.", part, re.S):
        s = mm.group(0)
        if s.startswith("<"):
            flat_chars.append(" ")
            pos_map.append(mm.end())
        else:
            flat_chars.append(s)
            pos_map.append(mm.start())
    t = "".join(flat_chars)

    def rawpos(m):
        return pos_map[m.start()]

    out = []
    for m in re.finditer(r"tg\d*\s*:\s*(\d+\.?\d*)\s*W\b", t, re.I):
        if "total system power" in t[max(0, m.start() - 160):m.start()].lower():
            out.append((rawpos(m), None, "sys", float(m.group(1)),
                        "measured total system power (hwmon), tg test"))
    for m in re.finditer(
            r"([^:|<]{2,40}?)\s*:\s*~?(\d+)-(\d+)\s*W\s*"
            r"\(\s*Watt per tg/s:\s*~?([\d.]+)", t, re.I):
        out.append((rawpos(m), m.group(1), "rate", float(m.group(4)),
                    "measured nvtop power, %s W per t/s (published range %s-%sW)"
                    % (m.group(4), m.group(2), m.group(3))))
    for m in re.finditer(r"Observed power\.draw:\s*Short runs:\s*~?(\d+)\s*W",
                         t, re.I):
        out.append((rawpos(m), None, "watts", float(m.group(1)),
                    "measured nvidia-smi power.draw, short runs (approximate)"))
    for m in re.finditer(r"Power-draw went up as well:\s*~?(\d+)\s*W",
                         t, re.I):
        out.append((rawpos(m), None, "watts", float(m.group(1)),
                    "measured power draw"))
    for m in re.finditer(r"peaked? at\s*~?(\d+\.?\d*)\s*W\b", t, re.I):
        out.append((rawpos(m), None, "watts", float(m.group(1)),
                    "measured GPU power, peaked at ~%s W during the run (approximate)"
                    % m.group(1)))
    for m in re.finditer(r"run at performance[^:.|<]{0,60}:\s*~?(\d+)-(\d+)\s*W\b",
                         t, re.I):
        lo, hi = float(m.group(1)), float(m.group(2))
        out.append((rawpos(m), None, "range", (lo + hi) / 2,
                    "measured GPU power %s-%s W during the run (midpoint %s W, approximate)"
                    % (m.group(1), m.group(2), (lo + hi) / 2)))
    return out


def attach_power(rows, part, table_pos):
    """Pair measured-power prose with the rows of the table it follows.

    An entry belongs to the table that starts just before it. If several
    entries belong to the same table (multi-GPU sections), pair by label
    when possible, then by row/entry order.
    """
    entries = power_entries(part)
    if not entries:
        return
    unused = set(id(e) for e in entries)

    def apply(r, e):
        w = round(e[3] * r["tps"]) if e[2] == "rate" else e[3]
        if e[2] == "rate" and w == 0:
            w = e[3]
        r["power_w"] = w
        r["notes"] = ((r["notes"] + "; " if r["notes"] else "")
                      + str(w) + " W " + e[4])

    for r in rows:
        hw = norm(r.get("hardware"))
        lab = [e for e in entries if id(e) in unused and e[1]
               and (norm(e[1]) in hw or hw in norm(e[1]))]
        if len(lab) == 1:
            apply(r, lab[0])
            unused.discard(id(lab[0]))
    tpos = sorted(set(p for p in table_pos.values() if p is not None))
    by_table = {}
    for e in entries:
        if id(e) in unused and tpos:
            t = min(tpos, key=lambda tp: abs(tp - e[0]))
            by_table.setdefault(t, []).append(e)
    for r in rows:
        if r.get("power_w"):
            continue
        es = [e for e in by_table.get(table_pos.get(id(r)), [])
              if id(e) in unused]
        if len(es) == 1:
            apply(r, es[0])
            unused.discard(id(es[0]))


def extract(frag, comment_url, thread_label, thread_num, comment_id):
    """Pull benchmark rows out of one post fragment."""
    rows = []
    frag = strip_templates(frag)
    parts = body_parts(frag)
    plain = re.sub(r"\s+", " ", " ".join(
        text_of(re.sub(r"<table.*?</table>", " ", p, flags=re.S)) for p in parts))
    part_starts = []
    for part in parts:
        part_starts.append(len(rows))
        context = [(m.start(), clean(m.group(1))) for m in HEADING_RE.finditer(part)]
        context += [(m.start(), clean(m.group(1))) for m in re.finditer(r"<p[^>]*>(.*?)</p>", part, re.S)]
        heads = [(m.start(), clean(m.group(1))) for m in HEADING_RE.finditer(part)]

        def context_before(pos):
            before = [t for p, t in context if p < pos]
            return before[-1] if before else ""

        def nearest_hw(pos):
            for hp, ht in reversed([x for x in xcontext if x[0] <= pos]):
                c = nearest_chip(ht, thread_label)
                if c:
                    return c
            return chip_in(plain, thread_label)

        def gpu_map(pos):
            """Numbered GPU list ('0: X 1: Y' or '0 = X 1 = Y') in the text
            preceding a table, as {index: (chip, snippet)}. The mention
            closest to the table wins.
            """
            m = {}
            for gp, gt in [x for x in xcontext if x[0] <= pos]:
                segs = re.split(r"\b(\d)\s*[:=]\s*", gt)
                if len(segs) < 4:
                    continue
                for k in range(1, len(segs) - 1, 2):
                    chip = chip_in(segs[k + 1][:120], thread_label)
                    if chip:
                        m[segs[k]] = (chip, segs[k + 1][:80].strip())
            return m

        all_tables = []
        for p2, t2 in table_rows(part):
            all_tables.append((p2, t2, ""))
        for p2, t2, pred in text_tables(part):
            all_tables.append((p2, t2, pred))
        all_tables.sort(key=lambda x: x[0])
        xcontext = context + [(p2, pred) for p2, t2, pred in all_tables
                              if pred]
        xcontext.sort(key=lambda x: x[0])
        for ti, (pos, tbl, pred) in enumerate(all_tables):
            hdr = [h.lower() for h in tbl[0]]
            if "test" in hdr and "t/s" in hdr:
                # old llama-bench: one row per test (pp*/tg*)
                idx = {c.lower(): i for i, c in enumerate(tbl[0])}
                model_i = idx.get("model", 0)
                mg_i = idx.get("main_gpu")
                # Repeated test cells for the same (model, quant, mg, dev,
                # backend, threads) are separate llama-bench runs (different
                # build/flags); split them instead of overwriting.
                runs_by_key = {}
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
                    mg = r[mg_i] if mg_i is not None and mg_i < len(r) else ""
                    dev = (r[idx["dev"]].strip().upper() if "dev" in idx
                           and idx["dev"] < len(r) else "")
                    key = (model, quant, mg, dev,
                           r[idx.get("backend", 0)] if "backend" in idx and idx["backend"] < len(r) else "",
                           r[idx.get("threads", idx.get("ngl", 0))] if ("threads" in idx or "ngl" in idx) and max(idx.get("threads", 0), idx.get("ngl", 0)) < len(r) else "")
                    runs = runs_by_key.setdefault(key, [])
                    target = None
                    for run in reversed(runs):
                        if test not in run["tests"]:
                            target = run
                            break
                    if target is None:
                        target = {"model": model, "quant": quant, "mg": key[2],
                                  "dev": dev, "backend": key[4], "threads": key[5],
                                  "tests": {}, "cells": []}
                        runs.append(target)
                    target["tests"][test] = (val, r[idx["t/s"]])
                    target["cells"].append((model_cell or key[0], test, r[idx["t/s"]]))
                for key, runs in runs_by_key.items():
                    for ri, ent in enumerate(runs):
                        tgk = [k for k in ent["tests"] if k.startswith("tg")]
                        ppk = [k for k in ent["tests"] if k.startswith("pp")]
                        if not tgk:
                            continue
                        tgv, tgs = ent["tests"][tgk[0]]
                        pp = ent["tests"].get(ppk[0], (None, "")) if ppk else (None, "")
                        note = "threads=%s" % ent["threads"] if ent["threads"] else None
                        if ri:
                            run_note = ("run %d of %d in this comment (separate "
                                        "llama-bench run; build/flags differ)"
                                        % (ri + 1, len(runs)))
                            note = (note + "; " + run_note) if note else run_note
                        quote = "; ".join("%s | %s | %s" % c for c in ent["cells"])
                        if ent["dev"]:
                            quote = "dev=%s; " % ent["dev"] + quote
                        hw, gsnip = None, None
                        if mg_i is not None and ent["mg"]:
                            gmap = gpu_map(pos)
                            if ent["mg"] in gmap:
                                hw, gsnip = gmap[ent["mg"]]
                        if not hw:
                            hw = nearest_hw(pos)
                        if hw:
                            if gsnip and norm(hw) not in norm(gsnip):
                                quote = hw + "; " + gsnip + "; " + quote
                            elif gsnip:
                                quote = gsnip + "; " + quote
                            else:
                                quote = hw + "; " + quote
                        rows.append({
                            "model": ent["model"], "quant": ent["quant"],
                            "backend": dev_backend(ent["dev"]) or backend_of(ent["backend"]),
                            "ctx": None, "tps": tgv,
                            "pp_tps": pp[0],
                            "pp_tokens": int(ppk[0][2:]) if ppk else None,
                            "tg_tokens": int(tgk[0][2:]),
                            "quote": quote, "notes": note,
                            "source_url": comment_url,
                            "hardware": hw,
                            "_tpos": pos,
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
                    tg_tokens = None
                    pp_tokens = None
                    for h in hdr[1:]:
                        if re.fullmatch(r"tg\d+", h):
                            v, raw = value_of(r[idx[h]]), r[idx[h]]
                            if tps is None and v is not None:
                                tps = v
                                tg_tokens = int(h[2:])
                            quote = quote + "; " + h + ": " + raw
                        elif re.fullmatch(r"pp\d+", h):
                            v, raw = value_of(r[idx[h]]), r[idx[h]]
                            if v is not None and pp is None:
                                pp = v
                                pp_tokens = int(h[2:])
                            quote = quote + "; " + h + ": " + raw
                    if tps is None:
                        continue
                    dev = (r[idx["dev"]].strip().upper() if "dev" in idx
                           and idx["dev"] < len(r) else "")
                    if dev:
                        quote = "dev=%s; " % dev + quote
                    hw = nearest_hw(pos)
                    if hw:
                        quote = hw + "; " + quote
                    rows.append({
                        "model": model, "quant": quant or "as-published",
                        "backend": dev_backend(dev) or backend_of(r[idx["backend"]]),
                        "ctx": None, "tps": tps, "pp_tps": pp,
                        "pp_tokens": pp_tokens, "tg_tokens": tg_tokens,
                        "quote": quote, "notes": None, "source_url": comment_url,
                        "hardware": hw,
                        "_tpos": pos,
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
                            "source_url": comment_url, "_tpos": pos})
    # measured power reported in the post prose, paired to rows per part
    off = 0
    for i, part in enumerate(parts):
        nxt = part_starts[i + 1] if i + 1 < len(part_starts) else len(rows)
        seg = rows[off:nxt]
        table_pos = {id(r): r.pop("_tpos", None) for r in seg}
        attach_power(seg, part, table_pos)
        off = nxt
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
                    "pp_tokens": row.get("pp_tokens"),
                    "tg_tokens": row.get("tg_tokens"),
                    "ttft_s": None,
                    "power_w": row.get("power_w"),
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
