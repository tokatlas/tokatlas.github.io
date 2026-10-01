#!/usr/bin/env python3
"""Generate the static site from data/records.json. Stdlib only.

Outputs (committed to the repo root, served by GitHub Pages):
  index.html, lookup.html, data.html, changelog.html,
  hardware/index.html + hardware/<slug>.html,
  models/index.html + models/<slug>.html,
  backends/index.html
"""
import datetime
import html
import json
import os
import re
import shutil
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

PAGE_TITLE = "Token Atlas"

CREDITS = [
    ("LocalScore", "https://www.localscore.ai",
     "Open benchmark and CLI on top of Llamafile; per-hardware LLM scores. "
     "Complementary: LocalScore focuses on standardized benchmark runs, we aggregate and cite public sources across backends."),
    ("LLMCheck", "https://llmcheck.net",
     "Apple Silicon LLM index and the source of our current dataset (CC BY 4.0)."),
    ("llmconfigurator benchmarks", "https://llmconfigurator.com/en/benchmarks",
     "GPU leaderboard of local LLM tokens/sec; one of our data sources (CC BY 4.0)."),
    ("Silicon Score", "https://siliconscore.com/bench/",
     "Apple Silicon benchmark audit with per-row sources; one of our data sources."),
    ("Localmaxxing", "https://www.localmaxxing.com",
     "Community local LLM inference speed tests, filterable by model/hardware/engine/quant."),
    ("Bench360", "https://arxiv.org/abs/2511.16682",
     "Academic benchmarking of local LLM inference (360 degrees)."),
    ("anubis-oss", "https://github.com/uncSoft/anubis-oss",
     "Apple Silicon community leaderboard."),
    ("r/LocalLLaMA", "https://www.reddit.com/r/LocalLLaMA/",
     "Community benchmark threads; llama-bench results posts."),
]


def slug(s: str) -> str:
    s = (s or "").lower().replace("+", " plus ")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "unknown"


def esc(v):
    return html.escape(str(v if v is not None else ""))


def page(title, body, extra=""):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}: Token Atlas</title>
<link rel="stylesheet" href="/assets/style.css">{extra}
</head><body>
<header><a class="logo" href="/">tokatlas</a><nav>
<a href="/">home</a><a href="/lookup.html">lookup</a><a href="/hardware/">hardware</a>
<a href="/models/">models</a><a href="/backends/">backends</a><a href="/data/">data</a>
<a href="/changelog.html">changelog</a></nav></header>
<main>
{body}
</main>
<footer>
<p><strong>Token Atlas</strong> is built and maintained by an autonomous AI agent
(<a href="https://github.com/tokatlas">tokatlas</a>) on a standing mandate. Every record links
to its public source. <a href="/#cite">Cite it</a>.</p>
<p class="gen">generated {now} from <a href="/data/records.json">data/records.json</a></p>
</footer>
</body></html>
"""


def prov_badge(p):
    cls = {"sourced": "b-src", "community": "b-com", "estimated": "b-est"}.get(p, "b-est")
    label = {"sourced": "sourced", "community": "community", "estimated": "estimated"}.get(p, p or "?")
    return f'<span class="badge {cls}">{label}</span>'


def flag_badges(flags):
    flags = flags or []
    if not flags:
        return "–"
    return " ".join(f'<span class="badge b-flag">{esc(f)}</span>' for f in flags)


def record_row(r):
    ttft = f"{r['ttft_s']}" if r.get("ttft_s") is not None else "–"
    pw = f"{r['power_w']}" if r.get("power_w") is not None else "–"
    # ctx is a real context depth; when it is null but the test shape is
    # known (llama-bench), show the decode length (tgNNN) instead
    ctx = r.get("ctx") or ("tg" + str(r["tg_tokens"]) if r.get("tg_tokens") else "–")
    date = r.get("date") or "–"
    return (f"<tr><td><a href=\"/hardware/{slug(r['hardware'])}/\">{esc(r['hardware'])}</a></td>"
            f"<td><a href=\"/models/{slug(r['model'])}/\">{esc(r['model'])}</a> "
            f"<span class=\"dim\">{esc(r.get('params'))}</span></td>"
            f"<td>{esc(r.get('quant'))}</td><td>{esc(r.get('backend'))}</td>"
            f"<td class=\"num\">{esc(r.get('tps'))}</td>"
            f"<td class=\"num\">{esc(pw)}</td>"
            f"<td class=\"num\">{esc(ttft)}</td>"
            f"<td>{esc(ctx)}</td><td>{esc(date)}</td>"
            f"<td>{prov_badge(r.get('provenance'))}</td>"
            f"<td>{flag_badges(r.get('flags'))}</td>"
            f"<td><a href=\"{esc(r['source_url'])}\" rel=\"nofollow\">source</a></td></tr>")


TABLE_HEAD = ("<tr><th>hardware</th><th>model</th><th>quant</th><th>backend</th>"
              "<th>tok/s</th><th>W</th><th>ttft s</th><th>ctx/tg</th><th>date</th>"
              "<th>class</th><th>flags</th><th>source</th></tr>")


def records_table(rows):
    rows = sorted(rows, key=lambda r: (str(r.get("model")).lower(),
                                       -float(r.get("tps") or 0)))
    body = "\n".join(record_row(r) for r in rows)
    return f"<table>{TABLE_HEAD}{body}</table>"


def main():
    with open(os.path.join(DATA, "records.json")) as f:
        ds = json.load(f)
    records = ds["records"]
    retrieved = ds.get("retrieved", "?")
    ref_path = os.path.join(DATA, "reference", "estimates.json")
    if os.path.exists(ref_path):
        with open(ref_path) as f:
            ref = json.load(f)
    else:
        ref = {"count": 0, "records": []}
    ref_records = ref["records"]
    clu_path = os.path.join(DATA, "reference", "cluster.json")
    if os.path.exists(clu_path):
        with open(clu_path) as f:
            clu = json.load(f)
    else:
        clu = {"count": 0, "records": []}

    def mkey(s):
        return re.sub(r"[^a-z0-9]+", "", str(s).lower())

    hw = defaultdict(list)
    models = defaultdict(list)
    backends = defaultdict(list)
    for r in records:
        hw[r["hardware"]].append(r)
        models[r["model"]].append(r)
        backends[(mkey(r["model"]), r["hardware"], r["quant"])].append(r)

    # Guard: one page per key at <prefix>/<slug>/, so two keys with the same
    # slug would overwrite each other and hide rows. Fail the build instead.
    for prefix, keys in (("hardware", hw), ("model", models)):
        seen = {}
        for k in keys:
            seen.setdefault(slug(k), []).append(k)
        coll = {s: ks for s, ks in seen.items() if len(ks) > 1}
        if coll:
            for s, ks in sorted(coll.items()):
                print(f"slug collision on {s}: {sorted(ks)}", file=sys.stderr)
            sys.exit(1)

    def write(path, content):
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(content)
        print("wrote", path)

    # --- index ---
    prov = defaultdict(int)
    for r in records:
        prov[r.get("provenance") or "?"] += 1
    stats = (f"<p class=\"stats\">{len(records)} records · "
             f"{len(models)} models · {len(hw)} hardware · "
             f"{len(set(r['backend'] for r in records))} backends · "
             f"data retrieved {esc(retrieved)}</p>")
    credits = "".join(f"<li><a href=\"{u}\">{esc(n)}</a>: {esc(d)}</li>" for n, u, d in CREDITS)
    prov_note = (" ".join(f"<span class=\"badge { {'sourced':'b-src','community':'b-com','estimated':'b-est'}[k]}\">{k}</span> {v}"
                          for k, v in sorted(prov.items())))
    index = f"""
<h1>Token Atlas</h1>
<p>A continuously updated, <strong>source-cited</strong> dataset and lookup for local LLM
inference performance: hardware, backend, build, model, quant, context, and measured
tokens per second. The place to check before buying hardware or choosing a quant or backend.</p>
{stats}
<h2>What speed will I get?</h2>
<p><a href="/lookup.html">Open the lookup →</a> pick your hardware and a model; get every
recorded tokens/sec figure with its source.</p>
<h2>Browse</h2>
<ul>
<li><a href="/hardware/">Per-hardware pages</a>: every recorded run on each chip</li>
<li><a href="/models/">Per-model pages</a>: every hardware/quant/backend for each model</li>
<li><a href="/backends/">Cross-backend notes</a>: same model + chip across backends</li>
<li><a href="/notes/build-ab.html">Build A/B notes</a>: regressions and improvements between builds of the same backend</li>
<li><a href="/notes/cross-source.html">Cross-source checks</a>: where an estimate meets a measurement</li>
<li><a href="/data/">The dataset</a>: CSV and JSON, with schema</li>
<li><a href="/changelog.html">Changelog</a>: what changed, when</li>
</ul>
<h2>Reading the data</h2>
<p>Provenance classes: {prov_note}.</p>
<p><strong>sourced</strong>: a public page we link to, containing the quoted number.
<strong>community</strong>: a community-measured run (e.g. llama-bench results) carried in the
source dataset. <strong>estimated</strong>: the source's own model-based estimate, kept in
the reference area, never mixed with measured rows.</p>
<p>Current coverage: {len(hw)} hardware strings: Apple Silicon (M1 to M6),
NVIDIA RTX 30/40/50, AMD (Radeon RX 7000/9000, Ryzen AI APUs), Intel Arc, and
datacenter GPUs (A100, H100, L40S, DGX Spark). Backends: MLX, Ollama, LM Studio,
llama.cpp, llamafile, plus the llama.cpp runtime behind the Hardware Corner GPU
context curves (4k to 262k). Q4_K_M plus other quants. Every record carries a
source URL and the exact quoted cells; the {ref['count']} reference estimates
(board-spec power, tok/W) live in
<a href="/data/reference/estimates.json">data/reference/estimates.json</a>,
excluded from record counts. Cluster and multi-node runs (e.g. 8-way or 24-way
datacenter boxes) are measured and source-cited but out of the local-inference
record set: they live in
<a href="/data/reference/cluster.json">data/reference/cluster.json</a> and are
shown only via the lookup toggle.</p>
<h2>Complementary projects</h2>
<p>Token Atlas is built to complement, not duplicate, existing efforts. We credit and link them:</p>
<ul>{credits}</ul>
<h2 id="about">About this project</h2>
<p>Token Atlas is <strong>built and maintained by an autonomous AI agent</strong>
(<a href="https://github.com/tokatlas">github.com/tokatlas</a>) working a standing mandate.
Deterministic scripts collect and cite the data; the agent curates, analyzes, and publishes.
Found an error or have a result to submit?
<a href="https://github.com/tokatlas/tokatlas.github.io/issues/new?template=correction.md">File a correction</a>
or <a href="https://github.com/tokatlas/tokatlas.github.io/issues/new?template=submit-data.md">submit data</a>
(via issue templates).</p>
<h2 id="cite">Cite</h2>
<p>Token Atlas (tokatlas.github.io), retrieved {esc(retrieved)}. Data: LLMCheck Apple Silicon
LLM Benchmark Database (CC BY 4.0) via <a href="https://llmcheck.net/data/">llmcheck.net/data</a>;
LLM Configurator measured benchmarks (CC BY 4.0) via
<a href="https://llmconfigurator.com/measured-benchmarks.json">measured-benchmarks.json</a> and
benchmark cells via <a href="https://llmconfigurator.com/benchmarks.json">benchmarks.json</a>;
Silicon Score benchmark audit via <a href="https://siliconscore.com/benchmarks.json">benchmarks.json</a>;
Hardware Corner GPU LLM benchmarks (per-row attribution) via
<a href="https://www.hardware-corner.net/gpu-llm-benchmarks/">hardware-corner.net</a>.
Per-row source links are in the dataset.</p>
"""
    write("index.html", page("Local LLM inference performance, source-cited", index))

    # remove per-chip / per-model directories from earlier builds whose
    # hardware or model no longer has measured records (v3 split)
    for prefix, keys in (("hardware", hw.keys()), ("models", models.keys())):
        base = os.path.join(ROOT, prefix)
        if os.path.isdir(base):
            wanted = {slug(k) for k in keys}
            for name in os.listdir(base):
                if name == "index.html" or name in wanted:
                    continue
                p = os.path.join(base, name)
                if os.path.isdir(p):
                    shutil.rmtree(p)

    # --- hardware pages ---
    hw_list = "".join(
        f"<li><a href=\"/hardware/{slug(h)}/\">{esc(h)}</a>: {len(rs)} records, "
        f"{len(set(r['model'] for r in rs))} models</li>"
        for h, rs in sorted(hw.items()))
    write("hardware/index.html", page("Hardware", f"""
<h1>By hardware</h1>
<p>Every recorded inference run on each chip, with source links. {len(hw)} chips covered.</p>
<ul>{hw_list}</ul>"""))
    for h, rs in hw.items():
        s = sorted(set(r.get("quant") or "?" for r in rs))
        write(f"hardware/{slug(h)}/index.html", page(h, f"""
<h1>{esc(h)}</h1>
<p>{len(rs)} records across {len(set(r['model'] for r in rs))} models
(quants: {esc(', '.join(s))}).</p>
{records_table(rs)}
<p class="dim">All rows cite their source. Provenance: {prov_note}</p>
<p><a href="/hardware/">← all hardware</a></p>"""))

    # --- model pages ---
    m_list = "".join(
        f"<li><a href=\"/models/{slug(m)}/\">{esc(m)}</a>: {len(rs)} records, "
        f"{len(set(r['hardware'] for r in rs))} hardware</li>"
        for m, rs in sorted(models.items()))
    write("models/index.html", page("Models", f"""
<h1>By model</h1>
<p>{len(models)} models covered. Each page lists every hardware/quant/backend recording,
with source links.</p>
<ul>{m_list}</ul>"""))
    for m, rs in models.items():
        write(f"models/{slug(m)}/index.html", page(m, f"""
<h1>{esc(m)}</h1>
<p>{len(rs)} records across {len(set(r['hardware'] for r in rs))} hardware.</p>
{records_table(rs)}
<p><a href="/models/">← all models</a></p>"""))

    # --- cross-backend notes (analysis) ---
    multi = {k: v for k, v in backends.items() if len({r["backend"] for r in v}) > 1}
    notes = []
    for (m, h, q), rs in sorted(multi.items()):
        best = max(rs, key=lambda r: float(r.get("tps") or 0))
        names = " / ".join(sorted({r["model"] for r in rs}))
        lines = []
        for r in sorted(rs, key=lambda r: -float(r.get("tps") or 0)):
            pct = (100.0 * float(r.get("tps") or 0) / float(best.get("tps") or 1))
            lines.append(f"<li><strong>{esc(r['backend'])}</strong>: "
                         f"{esc(r.get('tps'))} tok/s ({pct:.0f}%) "
                         f"{prov_badge(r.get('provenance'))} "
                         f"<a href=\"{esc(r['source_url'])}\" rel=\"nofollow\">source</a></li>")
        notes.append(f"""<h3>{esc(names)} on {esc(h)} ({esc(q)})</h3>
<ul>{''.join(lines)}</ul>
<p class="dim">Auto-generated comparison; relative % vs the fastest recorded backend.
Differences between backends on the same model+chip can reflect build/version,
sampling, and context differences, not just the backend itself.</p>""")
    if not notes:
        notes.append("<p>No cross-backend comparisons yet.</p>")
    write("backends/index.html", page("Cross-backend notes", f"""
<h1>Cross-backend notes</h1>
<p>Where the same model and chip were recorded on more than one backend, we show them
side by side. {len(multi)} comparable cases so far. For regressions and improvements
between builds of the same backend, see the
<a href="/notes/build-ab.html">build A/B notes</a>.</p>
{''.join(notes)}"""))

    # --- build A/B notes (analysis) ---
    # Rows tagged with a config= token in notes form A/B groups: same model +
    # chip + backend, different builds or configurations of the same engine.
    # Every number in a rendered table or note comes from the record at build
    # time, so the page can never drift from records.json silently.
    def issue_ref(r):
        m = re.search(r"#(\d+)", r.get("source_name") or "")
        if m:
            return m.group(1)
        m = re.search(r"/(\d+)", r.get("source_url") or "")
        return m.group(1) if m else "?"

    def venue_of(r):
        name = r.get("source_name") or ""
        url = r.get("source_url") or ""
        if "llama.cpp" in name:
            return "llama.cpp"
        if "vLLM" in name:
            return "vLLM"
        if "ExLlamaV2" in name:
            return "ExLlamaV2"
        if "HF" in name:
            return "HF"
        if "vllm-project" in url:
            return "vLLM"
        if "llama.cpp" in url:
            return "llama.cpp"
        if "exllamav2" in url:
            return "ExLlamaV2"
        return "?"

    def cfg_token(r):
        m = re.search(r"config=([^\s;]+)", r.get("notes") or "")
        return m.group(1) if m else "?"

    ab_groups = defaultdict(list)
    for r in records:
        if re.search(r"config=", r.get("notes") or ""):
            ab_groups[(venue_of(r), issue_ref(r), r["hardware"],
                       r["model"], r.get("backend") or "?")].append(r)

    def ab_row(r):
        url = r.get("source_url") or ""
        tps = r.get("tps") if r.get("tps") is not None else "\u2013"
        pp = r.get("pp_tps") if r.get("pp_tps") is not None else "\u2013"
        batch = r.get("batch") if r.get("batch") is not None else "\u2013"
        return (f"<tr><td><code>{esc(cfg_token(r))}</code></td>"
                f"<td class=\"num\">{esc(tps)}</td>"
                f"<td class=\"num\">{esc(pp)}</td>"
                f"<td class=\"num\">{esc(batch)}</td>"
                f"<td><code>{esc(r['id'])}</code></td>"
                f"<td><a href=\"{esc(url)}\" rel=\"nofollow\">source</a></td></tr>")

    def val(rows, rid, field):
        r = rows.get(rid)
        return float(r[field]) if r and r.get(field) is not None else None

    def pct(rows, a, b, field):
        x, y = val(rows, a, field), val(rows, b, field)
        if x is None or y is None or not x:
            return None
        return (y - x) / x * 100

    def ab_note(venue, issue, hw, model, rows):
        if (venue, issue) == ("llama.cpp", "27137"):
            return ("Between tags 9006 and 10433, flash attention under Vulkan is "
                    f"auto-selected onto the slow path in this configuration: generation "
                    f"{val(rows,'lc-27137-b9006','tps')} to {val(rows,'lc-27137-b10433','tps')} tok/s "
                    f"({pct(rows,'lc-27137-b9006','lc-27137-b10433','tps'):.1f}%), prefill unchanged "
                    f"({val(rows,'lc-27137-b10433','pp_tps')} vs {val(rows,'lc-27137-b9006','pp_tps')} tok/s). "
                    "The issue argues the capability detection should not pick FA here.")
        if (venue, issue) == ("llama.cpp", "27171"):
            return ("Bisected: b10284 (commit 9a688e51e) is the first bad build for "
                    f"--fit-target 1024. tg256 {val(rows,'lc-27171-b10283','tps')} to "
                    f"{val(rows,'lc-27171-b10284','tps')} tok/s "
                    f"({pct(rows,'lc-27171-b10283','lc-27171-b10284','tps'):.1f}%), "
                    f"pp2048 {val(rows,'lc-27171-b10283','pp_tps')} to "
                    f"{val(rows,'lc-27171-b10284','pp_tps')} tok/s "
                    f"({pct(rows,'lc-27171-b10283','lc-27171-b10284','pp_tps'):.1f}%).")
        if (venue, issue) == ("llama.cpp", "27181"):
            return ("Identical-weights quant sweep: all three rows were "
                    "requantized from a single UD-Q6_K_XL source file, so this "
                    "is prefill throughput vs quant width, not a model "
                    "comparison. pp512 goes "
                    f"{val(rows,'lc-27181-r9700-mmq-q2_k','pp_tps')} tok/s "
                    "(Q2_K) to "
                    f"{val(rows,'lc-27181-r9700-mmq-q8_0','pp_tps')} tok/s "
                    f"(Q8_0), {pct(rows,'lc-27181-r9700-mmq-q2_k','lc-27181-r9700-mmq-q8_0','pp_tps'):+.0f}%, "
                    "with Q4_K at "
                    f"{val(rows,'lc-27181-r9700-mmq-q4_k','pp_tps')} tok/s.")
        if (venue, issue) == ("llama.cpp", "27464"):
            hwtag = "gb10" if hw == "GB10" else "pro6000"
            if model == "mamba2-2.7b":
                q = "Q8_0" if hwtag == "gb10" else "BF16"
                c = f"lc-27464-{hwtag}-mamba227b-q{q}-cur"
                p2 = f"lc-27464-{hwtag}-mamba227b-q{q}-pat"
                return ("The mamba-base.cpp reshape sent decode down a GEMV path; keeping "
                        f"the state tensor flat in 2D restores GEMM dispatch: "
                        f"{val(rows,c,'tps')} to {val(rows,p2,'tps')} tok/s "
                        f"({pct(rows,c,p2,'tps'):.0f}%).")
            if model.startswith("Nemotron"):
                c = f"lc-27464-{hwtag}-nemo-npl256-cur"
                p2 = f"lc-27464-{hwtag}-nemo-npl256-pat"
                return ("The fix targets decode at high concurrency, which is where the "
                        f"issue was filed: npl 256 goes {val(rows,c,'tps')} to "
                        f"{val(rows,p2,'tps')} tok/s ({pct(rows,c,p2,'tps'):.0f}%). "
                        f"Batch 1 barely moves (see the npl 1 rows).")
            if model.startswith("Falcon-H1") or model.startswith("granite"):
                tag = "falconh17b" if model.startswith("Falcon-H1") else "granite40htiny"
                qs = ["BF16", "Q4_K_M"]
                if tag == "falconh17b" and hwtag == "pro6000":
                    qs.insert(1, "Q8_0")
                parts = []
                for q in qs:
                    c = f"lc-27464-{hwtag}-{tag}-q{q}-cur"
                    p2 = f"lc-27464-{hwtag}-{tag}-q{q}-pat"
                    parts.append(f"{q} {val(rows,c,'tps')} to {val(rows,p2,'tps')} "
                                 f"({pct(rows,c,p2,'tps'):.0f}%)")
                return ("Same mamba2 flat-2D fix, npl 32: " + ", ".join(parts) + " tok/s.")
            return None
        if (venue, issue) == ("llama.cpp", "27623"):
            return ("Position sweep, q8 KV, no flash attention, WSL2 llama-server: "
                    f"decode holds {val(rows,'lc-27623-p45574','tps')} / "
                    f"{val(rows,'lc-27623-p60309','tps')} / {val(rows,'lc-27623-p68642','tps')} tok/s "
                    "at KV positions 45574 / 60309 / 68642, then collapses to "
                    f"{val(rows,'lc-27623-p91077','tps')} tok/s at 91077 (the source's "
                    "last row, published as '1.4 or timeout').")
        if (venue, issue) == ("llama.cpp", "27734"):
            return ("Wall-clock 1200-token single-stream completion: decode holds "
                    f"{val(rows,'lc-27734-r98304','tps')} tok/s at 98304, but at 131072 "
                    "the default KV suballocator hits a fragmentation cliff ("
                    f"{val(rows,'lc-27734-r131072','tps')} tok/s). A 4 GiB suballocator "
                    f"restores {val(rows,'lc-27734-r131072-4gib','tps')} tok/s at the "
                    "same depth.")
        if (venue, issue) == ("llama.cpp", "28135"):
            return ("Fix-verification A/B on the same machine: fastpath-off "
                    "ran with the hybrid-KV f16-scratch fast path disabled, "
                    "fastpath-on with it enabled. Prefill goes "
                    f"{val(rows,'lc-28135-rx9070-f16-scratch-off','pp_tps')} "
                    f"to "
                    f"{val(rows,'lc-28135-rx9070-f16-scratch-on','pp_tps')} "
                    "tok/s "
                    f"({pct(rows,'lc-28135-rx9070-f16-scratch-off','lc-28135-rx9070-f16-scratch-on','pp_tps'):+.0f}%); "
                    "decode was published as unchanged, so this group is the "
                    "prefill-only delta.")
        if (venue, issue) == ("llama.cpp", "28219"):
            return ("The local MSVC build collapses on both spec paths: MTP "
                    f"{val(rows,'lc-28219-msvc-mtp','tps')} and DFlash2 "
                    f"{val(rows,'lc-28219-msvc-dflash','tps')} tok/s, with an exact "
                    "500 ms stepping in the per-3s log lines. The same MSVC build "
                    f"without spec is {val(rows,'lc-28219-msvc-nospec','tps')} tok/s; "
                    "the official b10734 MTP baseline is "
                    f"{val(rows,'lc-28219-b10734-baseline','tps')} tok/s. The DFlash2 "
                    "result is identical to MTP, so the cliff is not MTP-specific.")
        if (venue, issue) == ("llama.cpp", "28761"):
            if hw == "2× TU106":
                return ("Tile-variant comparison on sm_75 (head_dim=256): "
                        "tile32 is the stock Q-tile cap, tile64 is a forced "
                        "build that register-spills at this head dimension, "
                        "and dynamic picks per FA call. All rows are "
                        "prompt_per_second (prefill) with FA on, KV q4_0, "
                        "ubatch 2048, MTP. At 8 K tile32 leads "
                        f"({val(rows,'lc-28761-tu106-qwen-tile32-8k','pp_tps')} "
                        f"vs {val(rows,'lc-28761-tu106-qwen-tile64-8k','pp_tps')} "
                        "tok/s); by 32 K tile64 leads "
                        f"({val(rows,'lc-28761-tu106-qwen-tile32-32k','pp_tps')} "
                        f"vs {val(rows,'lc-28761-tu106-qwen-tile64-32k','pp_tps')} "
                        "tok/s), and at 230 K "
                        f"({val(rows,'lc-28761-tu106-qwen-tile32-230k','pp_tps')} "
                        f"vs {val(rows,'lc-28761-tu106-qwen-tile64-230k','pp_tps')} "
                        "tok/s). The concurrent row is the 230 K slot at its "
                        f"solo speed ({val(rows,'lc-28761-tu106-qwen-dynamic-230k-concurrent','pp_tps')} "
                        "tok/s) while an 8 K slot runs alongside.")
            return ("Same tile-variant comparison at head_dim=128 on a single "
                    "TU106 (KV 8 K, prefill-only): no register spill at "
                    "either tile size, and tile64 is faster even here "
                    f"({val(rows,'lc-28761-tu106-llama-tile32-8k','pp_tps')} "
                    f"vs {val(rows,'lc-28761-tu106-llama-tile64-8k','pp_tps')} "
                    "tok/s), so the 32-token cap costs the most common "
                    "open-weight models on Turing.")
        if (venue, issue) == ("llama.cpp", "28790"):
            return ("On a self-built MSVC + CUDA 12.8 build, MTP makes prefill about 57x "
                    f"slower ({val(rows,'lc-28790-msvc-mtp','pp_tps')} vs "
                    f"{val(rows,'lc-28790-msvc-nomtp','pp_tps')} tok/s without MTP); the "
                    f"official Clang build b10917 keeps MTP prefill at "
                    f"{val(rows,'lc-28790-b10917-mtp','pp_tps')} tok/s. Between the official "
                    f"builds, MTP decode goes {val(rows,'lc-28790-b10889-mtp','tps')} to "
                    f"{val(rows,'lc-28790-b10917-mtp','tps')} tok/s and prefill "
                    f"{val(rows,'lc-28790-b10889-mtp','pp_tps')} to "
                    f"{val(rows,'lc-28790-b10917-mtp','pp_tps')} tok/s.")
        if (venue, issue) == ("llama.cpp", "28828"):
            return ("Cliff reproduction, not a version regression: both "
                    "IQ4_XS builds collapse, at slightly different prompt "
                    "lengths (b10727 between 32 K and 33 K, b10909 between 31 "
                    "K and 32 K), while the Q3_K_XL control stays flat across "
                    f"the same range ({val(rows,'lc-28828-7800xt-b10909-q3kxl-28672','pp_tps')}-"
                    f"{val(rows,'lc-28828-7800xt-b10909-q3kxl-33792','pp_tps')} "
                    "tok/s), so the cliff is IQ4_XS-specific on this RDNA3 "
                    "card. The MTP rows are the server-side (llama-server, MTP "
                    "spec decode) view of the same collapse: "
                    f"{val(rows,'lc-28828-7800xt-b10909-mtp-32100','pp_tps')} "
                    "tok/s prefill with a "
                    f"{val(rows,'lc-28828-7800xt-b10909-mtp-32100','ttft_s')} s "
                    "TTFT at the 32 100-token prompt, vs "
                    f"{val(rows,'lc-28828-7800xt-b10909-mtp-q3kxl-32100','pp_tps')} "
                    "tok/s for Q3_K_XL under identical conditions. The 8 192 "
                    "b10909 row is the single low sample the source flags as a "
                    "likely measurement artifact.")
        if (venue, issue) == ("llama.cpp", "28867"):
            return ("Bisected to #28102 (16378d93f), which admitted head-256 batches "
                    "to the AMD WMMA flash-attention path with a batch threshold of "
                    f"16: speculative decode drops from {val(rows,'lc-28867-pre','tps')} "
                    f"tok/s on 9113cc188 to {val(rows,'lc-28867-master','tps')} tok/s on "
                    f"master ({pct(rows,'lc-28867-pre','lc-28867-master','tps'):.0f}%). "
                    "Raising the WMMA threshold to 64 restores "
                    f"{val(rows,'lc-28867-t64','tps')} tok/s; prefill was insensitive "
                    "to the threshold at every width tested.")
        if (venue, issue) == ("llama.cpp", "29168") and "26B" in model:
            return ("Draft acceptance dropped 0.82 to 0.48 after the MoE weighted-reduction "
                    "fusion (bisected to b10751). MTP went from a "
                    f"{pct(rows,'lc-29168-b10750-plain','lc-29168-b10750-mtp','tps'):+.0f}% gain "
                    f"on b10750 ({val(rows,'lc-29168-b10750-mtp','tps')} vs "
                    f"{val(rows,'lc-29168-b10750-plain','tps')} tok/s plain) to a net loss "
                    f"on b10964 ({val(rows,'lc-29168-b10964-mtp','tps')} vs "
                    f"{val(rows,'lc-29168-b10964-plain','tps')}) and b11057 "
                    f"({val(rows,'lc-29168-b11057-mtp','tps')} vs "
                    f"{val(rows,'lc-29168-b11057-plain','tps')}).")
        if (venue, issue) == ("llama.cpp", "29172"):
            return ("Ternary PTQ1_0 weights, ngl 99, flash attention on: at KV depth "
                    f"154855 decode collapses to {val(rows,'lc-29172-d154855','tps')} "
                    f"tok/s from {val(rows,'lc-29172-d0','tps')} at depth 0, and the "
                    "source reports an ~21x prefill collapse at the same depth.")
        if (venue, issue) == ("llama.cpp", "29410") and "Qwopus" in model:
            return ("146 commits apart (not bisected): decode "
                    f"{val(rows,'lc-29410-b1','tps')} to {val(rows,'lc-29410-b2','tps')} tok/s "
                    f"({pct(rows,'lc-29410-b1','lc-29410-b2','tps'):.1f}%), MTP "
                    f"{val(rows,'lc-29410-b3','tps')} to {val(rows,'lc-29410-b5','tps')}/"
                    f"{val(rows,'lc-29410-b6','tps')} tok/s; pp512 did not regress "
                    f"({val(rows,'lc-29410-b1','pp_tps')} to {val(rows,'lc-29410-b2','pp_tps')} tok/s). "
                    "The issue suspects #27952 (RDNA3 q4_K MMQ retarget) for decode; the "
                    "MTP drop is attributed to an unknown commit in the same range.")
        if (venue, issue) == ("llama.cpp", "29419"):
            return ("Not a build A/B: two timing samples from the same SYCL run (n_gen "
                    f"103 at {val(rows,'lc-29419-1','tps')} and n_gen 159 at "
                    f"{val(rows,'lc-29419-2','tps')} tok/s), immediately followed by a "
                    "SIGABRT in ggml_sycl_flash_attn_ext. The gap between the samples "
                    "is the in-run trend into the crash, not a between-build difference.")
        if (venue, issue) == ("llama.cpp", "29536"):
            return ("Same R9700 under stock LLVM 23, before and after the "
                    "MMQ VGPR-spill fix: prefill "
                    f"{val(rows,'lc-29536-r9700-stock','pp_tps')} to "
                    f"{val(rows,'lc-29536-r9700-nospill','pp_tps')} tok/s "
                    f"({pct(rows,'lc-29536-r9700-stock','lc-29536-r9700-nospill','pp_tps'):+.0f}%) "
                    "on Qwen3.8-27B Q4_K_M, matching the result under AMD's "
                    "compiler. Prefill-only A/B.")
        if (venue, issue) == ("vLLM", "24728"):
            if "4B" in model:
                im_inf = "vllm-24728-a100-iv4-img-inf"
                vi_inf = "vllm-24728-a100-iv4-vid-inf"
                return (f"Burst mode (request-rate inf) only for this model: image "
                        f"{val(rows,im_inf,'tps')} vs video {val(rows,vi_inf,'tps')} tok/s "
                        "aggregate output, 50-prompt ShareGPT4Video sweep.")
            pfx = "qwen" if "Qwen" in model else ("minicpm" if "MiniCPM" in model else "iv2")
            im_c1, im_c50 = f"vllm-24728-a100-{pfx}-img-c1", f"vllm-24728-a100-{pfx}-img-c50"
            vi_c1, vi_c50 = f"vllm-24728-a100-{pfx}-vid-c1", f"vllm-24728-a100-{pfx}-vid-c50"
            vi_inf = f"vllm-24728-a100-{pfx}-vid-inf"
            if "Qwen" in model:
                im_inf = "vllm-24728-a100-qwen-img-inf"
                return (f"Aggregate output tok/s, 50-prompt ShareGPT4Video sweep: video "
                        f"c1 {val(rows,vi_c1,'tps')} to c50 {val(rows,vi_c50,'tps')} "
                        f"({pct(rows,vi_c1,vi_c50,'tps'):+.0f}%), image burst "
                        f"(request-rate inf) {val(rows,im_inf,'tps')} vs c50 "
                        f"{val(rows,im_c50,'tps')} tok/s; burst video "
                        f"{val(rows,vi_inf,'tps')} tok/s. The issue's finding is that "
                        "video prefill is CPU-bound (frame decoding plus ViT extraction "
                        "at ~100% CPU, ~20% GPU).")
            return (f"Aggregate output tok/s, 50-prompt ShareGPT4Video sweep: video c1 "
                    f"{val(rows,vi_c1,'tps')} to c50 {val(rows,vi_c50,'tps')} "
                    f"({pct(rows,vi_c1,vi_c50,'tps'):+.0f}%), image c1 "
                    f"{val(rows,im_c1,'tps')} to c50 {val(rows,im_c50,'tps')}; the burst "
                    f"(request-rate inf) video figure is {val(rows,vi_inf,'tps')} tok/s. "
                    "The issue's finding is that video prefill is CPU-bound (frame "
                    "decoding plus ViT extraction at ~100% CPU, ~20% GPU).")
        if (venue, issue) == ("vLLM", "29662"):
            if "FP4" in model:
                c, p2 = "vllm-29662-b200-dsr1-0528-fp4-async", "vllm-29662-b200-dsr1-0528-fp4-sync"
            else:
                c, p2 = "vllm-29662-b200-dsr1-0528-fp8-async", "vllm-29662-b200-dsr1-0528-fp8-sync"
            return (f"Same 8x B200 TP8 MTP setup (con 256, 1280 prompts): "
                    f"{val(rows,c,'tps')} with --async-scheduling vs "
                    f"{val(rows,p2,'tps')} tok/s without "
                    f"({pct(rows,c,p2,'tps'):+.1f}%), so synchronous scheduling wins on "
                    "this workload regardless of FP8 vs FP4 weights.")
        if (venue, issue) == ("vLLM", "36629"):
            c, p2 = ("vllm-36629-4090d-qwen25-14b-fp8-eagle3",
                     "vllm-36629-4090d-qwen25-14b-w4a16-eagle3")
            return (f"batch16: FP8 + EAGLE3 {val(rows,c,'tps')} vs W4A16 + EAGLE3 "
                    f"{val(rows,p2,'tps')} tok/s ({pct(rows,c,p2,'tps'):+.1f}%); the issue "
                    "reports W4A16 leading at low concurrency, and its W4A16 run shows "
                    "worse tail ITL (P95 73.98 ms vs 56.24 ms).")
        if (venue, issue) == ("vLLM", "48518"):
            c, p2 = ("vllm-48518-h100-qwen3-8b-fp8-l2persist",
                     "vllm-48518-h100-qwen3-8b-fp8-l2cleared")
            return (f"Run right after server start, high-priority L2 data from startup "
                    f"still persisting: {val(rows,c,'tps')} tok/s (TPOT 4.83 ms) vs "
                    f"{val(rows,p2,'tps')} tok/s (TPOT 4.66 ms) after a one-shot L2 clear "
                    f"({pct(rows,c,p2,'tps'):+.1f}%).")
        if (venue, issue) == ("vLLM", "49370"):
            c, p2 = "vllm-49370-b300-dsv4-flash-fp4-base", "vllm-49370-b300-dsv4-flash-fp4-nobreak"
            return (f"VLLM_USE_BREAKABLE_CUDAGRAPH=0 moves capture to the normal "
                    f"FULL_AND_PIECEWISE path: {val(rows,c,'tps')} to {val(rows,p2,'tps')} "
                    f"tok/s ({pct(rows,c,p2,'tps'):+.0f}%) on the same B300 offline batch, "
                    "the default startup with breakable cudagraph auto-enabled being "
                    "the slow arm.")
        if (venue, issue) == ("vLLM", "58578"):
            if "Qwen3.8" in model:
                c, p2 = "vllm-58578-b70-qwen38-dvfull", "vllm-58578-b70-qwen38-dvred"
            else:
                c, p2 = "vllm-58578-b70-qwen36-dvfull", "vllm-58578-b70-qwen36-dvred"
            return (f"Reduced draft vocabulary: {val(rows,c,'tps')} to {val(rows,p2,'tps')} "
                    f"tok/s ({pct(rows,c,p2,'tps'):+.1f}%) one-stream decode at unchanged "
                    "acceptance (2.99-3.04 vs 2.96-3.00 tokens per step); the stock "
                    "drafter reads the shared 248,320 x 5120 lm_head for every draft "
                    "token, which is most of the per-draft cost on this bandwidth-bound "
                    "card.")
        if (venue, issue) == ("ExLlamaV2", "10"):
            v1 = "exldisc-10-a6000-freewilly2-70b-v1-1"
            v2 = "exldisc-10-a6000-freewilly2-70b-v2-1"
            v1e = "exldisc-10-a6000-freewilly2-70b-v1-9"
            v2e = "exldisc-10-a6000-freewilly2-70b-v2-9"
            return ("v1 is the GPTQ runtime, v2 the v2.0 EXL2 format, same 4bit 70b "
                    f"weights on the A6000. The comparable first long run (3156 tokens, "
                    f"ctx 941) goes {val(rows,v1,'tps')} to {val(rows,v2,'tps')} tok/s "
                    f"({pct(rows,v1,v2,'tps'):+.1f}%), and the gap holds at the deepest "
                    f"context ({val(rows,v1e,'tps')} to {val(rows,v2e,'tps')} tok/s, "
                    f"{pct(rows,v1e,v2e,'tps'):+.1f}%); the author's verdict: \"It's "
                    "definitely faster. I applaud this work.\"")
        if (venue, issue) == ("ExLlamaV2", "572"):
            a7 = "exldisc-572-4xa10g-llama3ft-env017-ctx0"
            a8 = "exldisc-572-4xa10g-llama3ft-env018-ctx0"
            b7 = "exldisc-572-4xa10g-llama3ft-env017-ctx12500"
            b8 = "exldisc-572-4xa10g-llama3ft-env018-ctx12500"
            return ("environment A/B, not code: the 0.1.7 and 0.1.8 venvs differ in "
                    f"torch (2.3 vs 2.4) and CUDA libraries. At ctx 0, request 1 is flat "
                    f"({val(rows,a7,'tps')} vs {val(rows,a8,'tps')} tok/s); at ctx 12,500 "
                    f"the 0.1.8 env falls to {val(rows,b8,'tps')} from {val(rows,b7,'tps')} "
                    f"tok/s ({pct(rows,b7,b8,'tps'):+.1f}%) and degrades another ~0.05 t/s "
                    "per 100 output tokens; the author's profile blames the "
                    "gemm_half_q_half call in the newer torch.")
        if (venue, issue) == ("ExLlamaV2", "450"):
            c, p2 = ("githubissues-rtx2080ti-llama3-exl2-b8-batched",
                     "githubissues-rtx2080ti-llama3-exl2-b8-caches")
            c1 = "githubissues-rtx2080ti-llama3-exl2-b1-batched"
            c1m = "githubissues-rtx2080ti-llama3-exl2-b1-caches"
            return (f"batched_inference.py scales to {val(rows,c,'tps')} tok/s at batch 8 "
                    f"({pct(rows,c1,c,'tps'):+.0f}% over its batch 1 of {val(rows,c1,'tps')}), "
                    f"while the multiple_caches.py inflight path only reaches "
                    f"{val(rows,p2,'tps')} tok/s (1.48x from its own batch 1 of "
                    f"{val(rows,c1m,'tps')}): the issue's 2x-worse scaling complaint. "
                    "EXL2 4 bpw, 2080 Ti, 16 prompts; the issue body says llama3 while "
                    "the linked gist script loads mistral-7b-exl2.")
        if (venue, issue) == ("vLLM", "27021"):
            return ("Reproduction of PR #25337 on A100 PCIe: before vs after is "
                    f"{val(rows,'vllm-27021-a100-pcie-qwen3vl30b-fp8-pre','tps')} to "
                    f"{val(rows,'vllm-27021-a100-pcie-qwen3vl30b-fp8-post','tps')} tok/s "
                    f"({pct(rows,'vllm-27021-a100-pcie-qwen3vl30b-fp8-pre','vllm-27021-a100-pcie-qwen3vl30b-fp8-post','tps'):+.1f}%), "
                    "far below the PR's own numbers, which were measured on SXM hardware. "
                    "The issue asks whether the model and hardware difference explains "
                    "the gap.")
        if (venue, issue) == ("vLLM", "37441"):
            return ("vLLM 0.16.0 (Triton 3.5): "
                    f"{val(rows,'vllm-37441-h200-gptoss120b-v0160-triton35','tps')} tok/s. "
                    "On 0.17.1, Triton 3.6's _reduce MoE kernel runs about 6.4x longer, "
                    f"dropping to {val(rows,'vllm-37441-h200-gptoss120b-v0171-triton36','tps')} tok/s "
                    f"({pct(rows,'vllm-37441-h200-gptoss120b-v0160-triton35','vllm-37441-h200-gptoss120b-v0171-triton36','tps'):.1f}%); "
                    "forcing the legacy Triton 3.5 kernels on 0.17.1 recovers the "
                    f"original {val(rows,'vllm-37441-h200-gptoss120b-v0171-legacy-triton35','tps')} tok/s.")
        if (venue, issue) == ("vLLM", "56564"):
            return ("The 0.6.17 to 0.6.18 bump flipped this GLM-5.3-Flash TP8 setup from the "
                    "forced FlashAttention sparse path to the auto-selected FlashInfer sparse "
                    f"path. Sonnet 300/256: {val(rows,'vllm-56564-h100fa-c1','tps')} to "
                    f"{val(rows,'vllm-56564-h100fi-c1','tps')} tok/s at c1 "
                    f"({pct(rows,'vllm-56564-h100fa-c1','vllm-56564-h100fi-c1','tps'):.1f}%) and "
                    f"{val(rows,'vllm-56564-h100fa-c8','tps')} to "
                    f"{val(rows,'vllm-56564-h100fi-c8','tps')} at c8 "
                    f"({pct(rows,'vllm-56564-h100fa-c8','vllm-56564-h100fi-c8','tps'):.1f}%); random "
                    f"worst case c1 {val(rows,'vllm-56564-h100fa-c1-random','tps')} to "
                    f"{val(rows,'vllm-56564-h100fi-c1-random','tps')} tok/s. MTP draft "
                    "acceptance is identical across arms, so the gap is the per-step "
                    "attention kernel.")
        if (venue, issue) == ("vLLM", "57680"):
            return ("Decode throughput drops about 3.3x between vLLM 0.26.0 and 0.29.0 in a "
                    "Confidential Computing VM: c12 "
                    f"{val(rows,'vllm-57680-h100nvl-qwen36-35b-v0260-c12','tps')} to "
                    f"{val(rows,'vllm-57680-h100nvl-qwen36-35b-v0290-c12','tps')} tok/s "
                    f"({pct(rows,'vllm-57680-h100nvl-qwen36-35b-v0260-c12','vllm-57680-h100nvl-qwen36-35b-v0290-c12','tps'):.1f}%), "
                    f"c1 {val(rows,'vllm-57680-h100nvl-qwen36-35b-v0260-c1','tps')} to "
                    f"{val(rows,'vllm-57680-h100nvl-qwen36-35b-v0290-c1','tps')} tok/s. "
                    f"0.24.0 is {val(rows,'vllm-57680-h100nvl-qwen36-35b-v0240-c12','tps')} at c12, "
                    "so 0.26.0 is slightly faster than 0.24.0 and the loss is not a "
                    "gradual drift.")
        if (venue, issue) == ("vLLM", "58920"):
            return ("KV connector overhead on Model Runner V2 with pipeline "
                    "parallelism: with a no-op connector (empty metadata, "
                    "no loads or stores) aggregate decode throughput drops "
                    f"from {val(rows,'vllm-58920-2nodes-h100-none-c8','tps')} to "
                    f"{val(rows,'vllm-58920-2nodes-h100-noop-c8','tps')} tok/s "
                    f"({pct(rows,'vllm-58920-2nodes-h100-none-c8','vllm-58920-2nodes-h100-noop-c8','tps'):.0f}%) "
                    "at 8 running requests, decode TPOT 32.1 to 60.0 ms, while "
                    "the V1 model runner shows no overhead. All 16 PP x TP "
                    "ranks reply to every RPC once a KV aggregator exists "
                    "(output_rank becomes None) and the reply-ring writer "
                    "spins holding the GIL, starving prepare_inputs on the "
                    "worker main thread.")
        if (venue, issue) == ("vLLM", "58804"):
            return ("Tiered KV offloading (24 GB CPU tier plus NVMe FS tier), "
                    "gpt-oss-120b TP2, Guidellm 5-turn concurrency-64 replay: "
                    "aggregate total tokens/s goes "
                    f"{val(rows,'vllm-58804-h100-fs-tiering-ab35354','tps')} to "
                    f"{val(rows,'vllm-58804-h100-fs-tiering-f12fe1','tps')} "
                    f"({pct(rows,'vllm-58804-h100-fs-tiering-ab35354','vllm-58804-h100-fs-tiering-f12fe1','tps'):+.0f}%) "
                    "when commit f12fe1, which lands PR #51787, replaces its "
                    "parent ab35354; the reporter's git bisect lands on that "
                    "commit, and a CPU-only replay of the access pattern found "
                    "no eviction-order regression, so the loss is in the fs "
                    "transfer or GPU-side timing the replay cannot capture.")
        if (venue, issue) == ("vLLM", "17221"):
            if hw == "2 A10" and model == "Qwen2.5-7B" and backend == "SGLang":
                return ("DP vs TP on the same pair of A10s with the same "
                        "model. SGLang --dp (a full model copy per GPU) "
                        f"varied {val(rows,'qsl17221-2a10-qwen257b-awq-sglang-dp-c30-r1','tps')} "
                        f"to {val(rows,'qsl17221-2a10-qwen257b-awq-sglang-dp-c30-r2','tps')} tok/s "
                        "between same-day runs; on advice from SGLang issue "
                        "#5808 the author switched to --tp, which returned "
                        "to single-GPU-level consistency "
                        f"({val(rows,'qsl17221-2a10-qwen257b-awq-sglang-tp-c30-r1','tps')} / "
                        f"{val(rows,'qsl17221-2a10-qwen257b-awq-sglang-tp-c30-r2','tps')} "
                        "tok/s), about "
                        f"{pct(rows,'qsl17221-2a10-qwen257b-awq-sglang-dp-c30-r2','qsl17221-2a10-qwen257b-awq-sglang-tp-c30-r1','tps'):+.0f}% "
                        "over the weaker same-day DP run.")
            if hw == "2 A10" and model == "Qwen2.5-7B" and backend == "vLLM":
                return ("vLLM v0.8.4 --tensor-parallel-size 2 on the same "
                        "box and model: two same-day c30 runs at "
                        f"{val(rows,'qsl17221-2a10-qwen257b-awq-vllm-c30-r1','tps')} / "
                        f"{val(rows,'qsl17221-2a10-qwen257b-awq-vllm-c30-r2','tps')} tok/s. "
                        "The project's 2-GPU comparison table puts SGLang "
                        "tensor parallelism ahead (1151-1158 vs 1074 tok/s); "
                        "the next-day retake of this box (the Qwen7B-awq "
                        "groups) shows SGLang TP2 ahead again at c50.")
            if hw == "2 A10" and model == "Qwen7B-awq" and backend == "SGLang":
                return ("Next-day (4.29) retake on the same pair of A10s, "
                        "SGLang --tp 2: "
                        f"{val(rows,'qsl17221-2a10-qwen7bawq-sglang-c5','tps')} at c5, "
                        f"{val(rows,'qsl17221-2a10-qwen7bawq-sglang-c30-r1','tps')} / "
                        f"{val(rows,'qsl17221-2a10-qwen7bawq-sglang-c30-r2','tps')} at c30, "
                        f"{val(rows,'qsl17221-2a10-qwen7bawq-sglang-c50-r1','tps')} / "
                        f"{val(rows,'qsl17221-2a10-qwen7bawq-sglang-c50-r2','tps')} at c50; "
                        "repeat runs agree within about 1%. This file names "
                        "the model only by its local path /home/vllm/llm/"
                        "Qwen7B-awq, which the README identifies as the "
                        "Qwen2.5-7B-AWQ download.")
            if hw == "2 A10" and model == "Qwen7B-awq" and backend == "vLLM":
                return ("Next-day retake, vLLM --tensor-parallel-size 2: "
                        f"c30 {val(rows,'qsl17221-2a10-qwen7bawq-vllm-c30-r1','tps')} / "
                        f"{val(rows,'qsl17221-2a10-qwen7bawq-vllm-c30-r2','tps')}, c50 "
                        f"{val(rows,'qsl17221-2a10-qwen7bawq-vllm-c50-r1','tps')} / "
                        f"{val(rows,'qsl17221-2a10-qwen7bawq-vllm-c50-r2','tps')}, c100 "
                        f"{val(rows,'qsl17221-2a10-qwen7bawq-vllm-c100-r1','tps')} / "
                        f"{val(rows,'qsl17221-2a10-qwen7bawq-vllm-c100-r2','tps')} "
                        "tok/s. vLLM leads the same-day SGLang TP2 runs at "
                        f"c30 ({val(rows,'qsl17221-2a10-qwen7bawq-vllm-c30-r2','tps')} vs "
                        f"{val(all_by_id,'qsl17221-2a10-qwen7bawq-sglang-c30-r1','tps')} best run), "
                        "but SGLang reclaims the lead at c50 "
                        f"({val(all_by_id,'qsl17221-2a10-qwen7bawq-sglang-c50-r1','tps')} vs "
                        f"{val(rows,'qsl17221-2a10-qwen7bawq-vllm-c50-r1','tps')}, about "
                        f"{pct(all_by_id,'qsl17221-2a10-qwen7bawq-vllm-c50-r1','qsl17221-2a10-qwen7bawq-sglang-c50-r1','tps'):+.0f}%), "
                        "and the SGLang sweep stops at c50.")
            if hw == "4 A10" and model == "Qwen7B-awq" and backend == "SGLang":
                return ("SGLang TP4 on the full box: three c30 runs across "
                        "two days "
                        f"({val(rows,'qsl17221-4a10-qwen7bawq-sglang-c30-r1','tps')} / "
                        f"{val(rows,'qsl17221-4a10-qwen7bawq-sglang-c30-r2','tps')} "
                        f"on 4.27-28, {val(rows,'qsl17221-4a10-qwen7bawq-sglang-c30-r3','tps')} "
                        "on 4.29) and three c50 runs "
                        f"({val(rows,'qsl17221-4a10-qwen7bawq-sglang-c50-r1','tps')} / "
                        f"{val(rows,'qsl17221-4a10-qwen7bawq-sglang-c50-r2','tps')} / "
                        f"{val(rows,'qsl17221-4a10-qwen7bawq-sglang-c50-r3','tps')}), "
                        "all within about 2% of each other. At c50 SGLang "
                        "TP4 leads vLLM TP4 on the same box by about "
                        f"{pct(all_by_id,'qsl17221-4a10-qwen7bawq-vllm-c50-r1','qsl17221-4a10-qwen7bawq-sglang-c50-r1','tps'):+.0f}%.")
            if hw == "4 A10" and model == "Qwen7B-awq" and backend == "vLLM":
                return ("vLLM TP4 on the full box: c30 "
                        f"{val(rows,'qsl17221-4a10-qwen7bawq-vllm-c30-r1','tps')} / "
                        f"{val(rows,'qsl17221-4a10-qwen7bawq-vllm-c30-r2','tps')}, c50 "
                        f"{val(rows,'qsl17221-4a10-qwen7bawq-vllm-c50-r1','tps')} / "
                        f"{val(rows,'qsl17221-4a10-qwen7bawq-vllm-c50-r2','tps')}, c100 "
                        f"{val(rows,'qsl17221-4a10-qwen7bawq-vllm-c100-r1','tps')} / "
                        f"{val(rows,'qsl17221-4a10-qwen7bawq-vllm-c100-r2','tps')} "
                        "tok/s. The project's summary calls vLLM's 2 to 4 "
                        "GPU gains modest (its analysis: 15-20% improvement "
                        "in most scenarios); the stored c100 pair is within "
                        "about 10% of the 2 A10 TP2 c100 rate in the "
                        "matching group, and the c50 rate stays far behind "
                        "SGLang TP4 "
                        f"({val(rows,'qsl17221-4a10-qwen7bawq-vllm-c50-r1','tps')} vs "
                        f"{val(all_by_id,'qsl17221-4a10-qwen7bawq-sglang-c50-r1','tps')} at c50).")
        if (venue, issue) == ("llama.cpp", "27050"):
            if "lc-27050-vllm-1s" in rows:
                return ("Reference arm from the same run: vLLM BF16 at "
                        f"{val(rows,'lc-27050-vllm-1s','tps')} tok/s single-slot "
                        f"and {val(rows,'lc-27050-vllm-32s','tps')} tok/s at 32 "
                        "slots. llama.cpp beats vLLM single-slot; at 32 slots "
                        "vLLM stays ahead of the -bs llama.cpp build (TPOT "
                        "17.68 vs 25.39 ms). The source treats this as a "
                        "concurrency-scaling difference, not a quality "
                        "verdict.")
            return ("Closed-loop llama-server on a 2016 Xeon: the default path "
                    f"saturates at {val(rows,'lc-27050-b9660-32s','tps')} / "
                    f"{val(rows,'lc-27050-b10423-32s','tps')} tok/s (32 slots, "
                    "b9660 vs b10423); backend sampling (-bs) lifts it to "
                    f"{val(rows,'lc-27050-b10423bs-32s','tps')} tok/s "
                    f"({pct(rows,'lc-27050-b10423-32s','lc-27050-b10423bs-32s','tps'):+.0f}%) "
                    f"with single slot unchanged at about 100 tok/s. Nsight "
                    "attributes the default-path cost to the full logits matrix "
                    "(16.2 MB at batch 32) being copied to host on every decode "
                    "step; -bs transfers only the sampled token id. The vLLM "
                    "reference rows from the same run are in the vLLM section "
                    "of this issue.")
        if (venue, issue) == ("llama.cpp", "27327"):
            return ("Three consecutive runs of the same server (build 10154, after the "
                    "Gated DeltaNet fused-op fix): "
                    f"{val(rows,'lc-27327-t1','tps')} / "
                    f"{val(rows,'lc-27327-t285','tps')} / "
                    f"{val(rows,'lc-27327-t556','tps')} tok/s, prompt processing "
                    f"{val(rows,'lc-27327-t1','pp_tps')} / "
                    f"{val(rows,'lc-27327-t285','pp_tps')} tok/s; the model sits "
                    "partially outside the 16 GB of VRAM.")
        if (venue, issue) == ("llama.cpp", "27572"):
            return ("Single-stream MTP decode (np 4, the racing build before the "
                    "sched-sync workaround): tg rises "
                    f"{val(rows,'lc-27572-d620','tps')} / "
                    f"{val(rows,'lc-27572-d4603','tps')} / "
                    f"{val(rows,'lc-27572-d9154','tps')} / "
                    f"{val(rows,'lc-27572-d18256','tps')} tok/s as the prompt grows "
                    "620 to 18256 tokens and plateaus, with MTP acceptance growing "
                    f"with context; prefill {val(rows,'lc-27572-d620','pp_tps')} to "
                    f"{val(rows,'lc-27572-d9154','pp_tps')} tok/s over the same sweep.")
        if (venue, issue) == ("llama.cpp", "27980"):
            return ("Four memory-placement configurations (mmap with embeddings on "
                    f"CPU, no-load with embeddings on CPU, all-VRAM, forced MMQ) hold "
                    f"decode within {val(rows,'lc-27980-r1','tps')} to "
                    f"{val(rows,'lc-27980-r3','tps')} tok/s on the 4x Tesla P40 rig; "
                    "placement barely matters here, and the issue's reference run of "
                    "a 10B-active MoE on the same GPUs and build reaches 29.5 tok/s.")
        if (venue, issue) == ("llama.cpp", "28484"):
            return ("Draft-MTP depth 2 over an RPC tensor split to a second 10 GB GPU: "
                    f"{val(rows,'lc-28484-mtp-depth2','tps')} vs "
                    f"{val(rows,'lc-28484-dense','tps')} tok/s raw dense decode on the "
                    f"same split ({pct(rows,'lc-28484-dense','lc-28484-mtp-depth2','tps'):+.1f}%); "
                    "the commit regressed MTP from 27-32 tok/s at bb4caa7, while the "
                    "issue's 31B Glimmer control row (no speculation, same split) "
                    "sits at 17.66 tok/s on both commits.")
        if (venue, issue) == ("llama.cpp", "29418"):
            return ("Not a build A/B: two timing samples from the same 2x B580 Vulkan "
                    f"run (n_gen 103 at {val(rows,'lc-29418-1','tps')} and n_gen 156 at "
                    f"{val(rows,'lc-29418-2','tps')} tok/s), immediately followed by the "
                    "GGML_ASSERT(neq0 == HSK) crash.")
        if (venue, issue) == ("llama.cpp", "29473"):
            if "Llama" in model:
                return ("The CPU runs 34.4 tok/s; the default Hexagon HMX path is broken "
                        "(garbled output, MUL_MAT inf for n >= 5) at "
                        f"{val(rows,'lc-29473-2','tps')} tok/s, and the HVX-only "
                        f"workaround that restores correct output gives "
                        f"{val(rows,'lc-29473-3','tps')} tok/s.")
            return ("Same pattern at 4B: the CPU runs 9.1 tok/s and the Adreno 722 "
                    "OpenCL path 7.5, while the broken HMX path gives "
                    f"{val(rows,'lc-29473-6','tps')} (garbled output) and the HVX-only "
                    f"workaround {val(rows,'lc-29473-7','tps')} tok/s.")
        if (venue, issue) == ("llama.cpp", "29510"):
            if "gemma" in model.lower():
                c, p2 = "lc-29510-gemma-master", "lc-29510-gemma-pr"
            else:
                c, p2 = "lc-29510-qwen-master", "lc-29510-qwen-pr"
            return ("The PR's flash_attn_ext_rows replaces the unified-KV penalty at "
                    f"ctx 400000: tg {val(rows,c,'tps')} to {val(rows,p2,'tps')} tok/s "
                    f"({pct(rows,c,p2,'tps'):+.1f}%), prefill "
                    f"{val(rows,c,'pp_tps')} to {val(rows,p2,'pp_tps')} tok/s "
                    f"({pct(rows,c,p2,'pp_tps'):+.0f}%).")
        if (venue, issue) == ("llama.cpp", "29523"):
            c, p2 = "lc-29523-2x3090-released", "lc-29523-2x3090-mtp-lag"
            return ("With the MTP catch-up lag fix: prefill "
                    f"{val(rows,c,'pp_tps')} to {val(rows,p2,'pp_tps')} tok/s "
                    f"({pct(rows,c,p2,'pp_tps'):+.0f}%), tg "
                    f"{val(rows,c,'tps')} to {val(rows,p2,'tps')} tok/s "
                    f"({pct(rows,c,p2,'tps'):+.1f}%); draft-mtp at 71.4% acceptance, "
                    "layer split 0.525/0.475.")
        if (venue, issue) == ("llama.cpp", "27420"):
            return ("The 2x2 matrix isolates the failure: only ubatch 256 + f16 "
                    f"KV + MTP at ctx 50000 collapses ({val(rows,'lc-27420-ub256-f16','tps')} "
                    f"tg / {val(rows,'lc-27420-ub256-f16','pp_tps')} pp tok/s); "
                    f"ub1024 + f16 is {val(rows,'lc-27420-ub1024-f16','tps')} tg, "
                    f"ub256 + q8 is {val(rows,'lc-27420-ub256-q8','tps')} tg, "
                    f"ub1024 + q8 is {val(rows,'lc-27420-ub1024-q8','tps')} tg. "
                    "The same ub256/f16 configuration is fine at ctx 16384 "
                    "(about 64 tg) and at 50k without MTP (about 660 tg), so the "
                    "three conditions are conjunctive; ub1024 or q8_0 KV is a "
                    "workaround. The source pins a deterministic boundary near "
                    "the 47.6k context mark.")
        if (venue, issue) == ("llama.cpp", "28218"):
            return ("Original report of the 500 ms stepping cliff: the official "
                    "b10734 drops to "
                    f"{val(rows,'lc-28218-m2','tps')} tok/s when an explicit "
                    f"tensor split 1 is added ({val(rows,'lc-28218-m1','tps')} "
                    "tok/s without it), and a local MSVC build of the same "
                    "commit reproduces the cliff on both spec paths (MTP "
                    f"{val(rows,'lc-28218-m3','tps')}, DFlash2 "
                    f"{val(rows,'lc-28218-m4','tps')} tok/s) while the same "
                    f"build runs {val(rows,'lc-28218-m5','tps')} tok/s without "
                    "speculation. Draft acceptance stayed about 81%, so the "
                    "cliff is a fixed wait per verification step, not compute. "
                    "#28219 is the companion report on the same build.")
        if (venue, issue) == ("llama.cpp", "28721"):
            if "lc-28721-d1k-sycl" in rows:
                return ("The SYCL arm degrades only 2.4x across the same "
                        f"range ({val(rows,'lc-28721-d1k-sycl','tps')} at 1k to "
                        f"{val(rows,'lc-28721-d64k-sycl','tps')} at 64k), and "
                        f"the no-draft control degrades at a similar rate "
                        f"({val(rows,'lc-28721-d1k-sycl-nomtp','tps')} at 1k, "
                        f"{val(rows,'lc-28721-d32k-sycl-nomtp','tps')} at "
                        "32k), so SYCL deep-context behavior is gradual KV "
                        "growth, not a cliff. SYCL draft acceptance is lower "
                        "at depth yet it still decodes faster than Vulkan at "
                        "every depth (see the Vulkan section). Prefill holds "
                        "around 510-635 tok/s across the range, and short "
                        "context decode is within about 8% of Vulkan.")
            return ("Vulkan decode on Arc Pro B70 (Xe2) collapses about 8x as "
                    f"context grows ({val(rows,'lc-28721-d1k-vk','tps')} at 1k "
                    f"to {val(rows,'lc-28721-d64k-vk','tps')} at 64k), and the "
                    "f16 KV control collapses in the same shape ("
                    f"{val(rows,'lc-28721-d1k-vkf16','tps')} to "
                    f"{val(rows,'lc-28721-d64k-vkf16','tps')}), so this is "
                    "not a KV-quantization effect. The MTP gain vanishes with "
                    "depth (no-draft control "
                    f"{val(rows,'lc-28721-d1k-vk-nomtp','tps')} at 1k, "
                    f"{val(rows,'lc-28721-d32k-vk-nomtp','tps')} at 32k) and "
                    "prefill degrades on Vulkan only (329 s TTFT for a 33k "
                    "prompt vs about 65 s on SYCL). The collapse is absent on "
                    "RDNA3 (RX 7900 XTX), and at 1k both backends sit at the "
                    "bandwidth ceiling (about 37 tok/s theoretical at 608 GB/s).")
        if (venue, issue) == ("llama.cpp", "28734"):
            return ("Single-stream decode decays roughly linearly with context "
                    "on master (shallow control "
                    f"{val(rows,'lc-28734-master-shallow','tps')} tok/s; "
                    f"{val(rows,'lc-28734-master-42k','tps')} at 42k, "
                    f"{val(rows,'lc-28734-master-111k','tps')} at 111k, "
                    f"{val(rows,'lc-28734-master-250k','tps')} at 250k) "
                    "because the QSA top-k path was running as a dense scan "
                    "over all n_kv (nsys profiled). A 2k-line, 7-patch lever "
                    "branch restores "
                    f"{val(rows,'lc-28734-patch-42k','tps')} / "
                    f"{val(rows,'lc-28734-patch-111k','tps')} / "
                    f"{val(rows,'lc-28734-patch-250k','tps')} tok/s "
                    f"({pct(rows,'lc-28734-master-42k','lc-28734-patch-42k','tps'):+.0f}% / "
                    f"{pct(rows,'lc-28734-master-111k','lc-28734-patch-111k','tps'):+.0f}% / "
                    f"{pct(rows,'lc-28734-master-250k','lc-28734-patch-250k','tps'):+.0f}%) "
                    "with a prefill side effect of 609 to 716 tok/s at 111k. "
                    "f16 KV is mandatory (quantized KV cannot reach the sparse "
                    "MMA kernel at batch 1 on Ampere); the reporter frames it "
                    "as an improvement, not a fix.")
        if (venue, issue) == ("llama.cpp", "29235"):
            return ("Same card, same model, different device enumeration: "
                    f"indexed GPU.1 is {val(rows,'lc-29235-gpu1-d128','tps')} "
                    f"vs {val(rows,'lc-29235-gpu-d128','tps')} tok/s at depth "
                    f"128, and {val(rows,'lc-29235-gpu1-d4096','tps')} vs "
                    f"{val(rows,'lc-29235-gpu-d4096','tps')} at depth 4096 "
                    f"({pct(rows,'lc-29235-gpu-d4096','lc-29235-gpu1-d4096','tps'):.0f}%). "
                    "The OpenVINO backend compares the device name against "
                    "'GPU', so indexed names keep the KV cache on the host and "
                    "never use the fast GQN attention. Prefill drops from "
                    f"{val(rows,'lc-29235-gpu-d4096','pp_tps')} to "
                    f"{val(rows,'lc-29235-gpu1-d4096','pp_tps')} tok/s "
                    f"({pct(rows,'lc-29235-gpu-d4096','lc-29235-gpu1-d4096','pp_tps'):.0f}%) "
                    "at 4096, the same mechanism on the prompt side.")
        if (venue, issue) == ("llama.cpp", "29513"):
            if "lc-29513-vulkan-first" in rows:
                return ("The Vulkan arm of the same report: first chat "
                        f"completion {val(rows,'lc-29513-vulkan-first','tps')} "
                        f"tok/s (prompt eval {val(rows,'lc-29513-vulkan-first','pp_tps')} "
                        f"tok/s), then {val(rows,'lc-29513-vulkan-warm','tps')} "
                        "tok/s from the third request on. Same build, same "
                        "model, same warm-up shape as the CUDA section; the "
                        "Vulkan first-request value is still about 5x the CUDA "
                        "first-request value.")
            return ("Not a build A/B: two states of the same b11206 build with "
                    "ngl=99 on a 2016 Xeon box. The first chat completion "
                    "right after load is "
                    f"{val(rows,'lc-29513-cuda-first','tps')} tok/s (Gated "
                    "DeltaNet warm-up at startup; /health was already ok "
                    f"before it), then from the third request on the same "
                    f"model runs {val(rows,'lc-29513-cuda-warm','tps')} tok/s. "
                    "The Vulkan arm on the same box follows the same shape "
                    "(see the adjacent section); warm prompt eval is in the "
                    "117-131 tok/s range as published.")
        if (venue, issue) == ("vLLM", "55139"):
            return ("Same 4x A100 PCIe layout (-pp 2 -tp 2), same sonnet "
                    "4096/1024 workload at max concurrency 18: MRV1 "
                    f"{val(rows,'vllm-55139-a100-gptoss20b-mrv1','tps')} vs "
                    f"MRV2 {val(rows,'vllm-55139-a100-gptoss20b-mrv2','tps')} "
                    "tok/s. The reporter bisected the drop to PR #42187 "
                    "(microbatch enable on V2 to avoid the pipeline bubble), "
                    "which may introduce collectives that this PP/TP layout "
                    "cannot hide.")
        if (venue, issue) == ("vLLM", "58639"):
            return ("The side-stream default roughly doubles the R9700 decode "
                    "forward (last PP rank, gfx1201): "
                    f"{val(rows,'vllm-58639-r9700-pp3-step-sidestreams','tps')} "
                    "tok/s at about 17 ms forward vs "
                    f"{val(rows,'vllm-58639-r9700-pp3-step-mainstream','tps')} "
                    "tok/s at about 7.2 ms after moving the last-rank sends "
                    "and the async output copy onto the main stream. The V620 "
                    "control ranks were unaffected. Serving reproduces it "
                    f"({val(rows,'vllm-58639-r9700-pp3-serve-sidestreams','tps')} to "
                    f"{val(rows,'vllm-58639-r9700-pp3-serve-mainstream','tps')} "
                    "tok/s median), and GPU_MAX_HW_QUEUES=2 (arms B and C) "
                    "removes the microbench penalty but does not match the "
                    "main-stream option end to end.")
        if (venue, issue) == ("vLLM", "40124"):
            return ("Patched results, not stock vLLM: the 13 Ampere-specific "
                    "monkey patches fix Hopper+ kernel selection (Triton FP8, "
                    "TurboQuant hybrid-MoE geometry). CUDA graphs are load-"
                    "bearing: enforce-eager drops "
                    f"{val(rows,'vllm-40124-a5000x2-qwen3-35b-decode','tps')} to "
                    f"{val(rows,'vllm-40124-a5000x2-qwen3-35b-eager','tps')} tok/s "
                    f"({pct(rows,'vllm-40124-a5000x2-qwen3-35b-decode','vllm-40124-a5000x2-qwen3-35b-eager','tps'):.0f}%), "
                    f"and TurboQuant k8v4 fits 160k context into 2x24 GB at "
                    f"{val(rows,'vllm-40124-a5000x2-qwen3-35b-160k','tps')} tok/s. "
                    "The source reports 10/10 stability runs, sigma 0.11 tok/s.")
        if (venue, issue) == ("vLLM", "58638"):
            return ("Every KV cache group rebuilds attention metadata per step, "
                    "and the GDN builders are expensive. The one-layer drafter "
                    "bucket forces one group per layer (46 groups), so the RFC's "
                    "worst-case-padding group sizing (gs=3, 17 groups) lifts "
                    f"c=1 from {val(rows,'vllm-58638-b300-qwen36-g46','tps')} to "
                    f"{val(rows,'vllm-58638-b300-qwen36-g17','tps')} tok/s "
                    f"({pct(rows,'vllm-58638-b300-qwen36-g46','vllm-58638-b300-qwen36-g17','tps'):+.0f}%); "
                    "the price is KV capacity, 7.42M down to 5.19M tokens.")
        if (venue, issue) == ("vLLM", "58845"):
            return ("Skips the qlnorm compute for MHA, which saves 78 kernel "
                    "calls per forward, with MTP on (8k prefill cannot be "
                    "cuda-graphed). Throughput holds at c4: "
                    f"{val(rows,'vllm-58845-glm53-main-c4','tps')} to "
                    f"{val(rows,'vllm-58845-glm53-skip-c4','tps')} tok/s "
                    f"({pct(rows,'vllm-58845-glm53-main-c4','vllm-58845-glm53-skip-c4','tps'):+.0f}%), "
                    "and the PR reports TTFT 360.5 to 332.9 ms (-7.7%) at c1 "
                    "and gsm8k 0.9212 vs 0.9151; at c16 the same change is "
                    f"{val(rows,'vllm-58845-glm53-main-c16','tps')} to "
                    f"{val(rows,'vllm-58845-glm53-skip-c16','tps')} tok/s "
                    f"({pct(rows,'vllm-58845-glm53-main-c16','vllm-58845-glm53-skip-c16','tps'):+.0f}%).")
        if (venue, issue) == ("vLLM", "58872"):
            return ("The split activates only at 2048+ token batches, so the "
                    "1K rows run the same kernels as main: c1 "
                    f"{val(rows,'vllm-58872-h20-main-1k-c1','tps')} to "
                    f"{val(rows,'vllm-58872-h20-split-1k-c1','tps')} tok/s "
                    f"({pct(rows,'vllm-58872-h20-main-1k-c1','vllm-58872-h20-split-1k-c1','tps'):+.0f}%), "
                    "which the PR attributes to server spread: the two PR "
                    "servers differ by 1.2% there, more than the gap between "
                    "the arms. The 8K rows take it: "
                    f"c16 {val(rows,'vllm-58872-h20-main-8k-c16','tps')} to "
                    f"{val(rows,'vllm-58872-h20-split-8k-c16','tps')} "
                    f"({pct(rows,'vllm-58872-h20-main-8k-c16','vllm-58872-h20-split-8k-c16','tps'):+.0f}%), "
                    f"c64 {val(rows,'vllm-58872-h20-main-8k-c64','tps')} to "
                    f"{val(rows,'vllm-58872-h20-split-8k-c64','tps')} "
                    f"({pct(rows,'vllm-58872-h20-main-8k-c64','vllm-58872-h20-split-8k-c64','tps'):+.0f}%), "
                    "with the PR estimating about 58 ms saved per 8K prefill "
                    "chunk and measuring TTFT -4.2% at 8K prompt.")
        if (venue, issue) == ("vLLM", "58880"):
            return ("Fuses MiniMax2-style routing into the monolithic TRT-LLM "
                    "MoE kernel, removing a separate topk_sigmoid launch per "
                    "MoE layer (1.3-2 microseconds per layer, 91-115 us per "
                    "decode step at TP4 for 32 tokens or fewer). "
                    f"c1 {val(rows,'vllm-58880-gb300-main-c1','tps')} to "
                    f"{val(rows,'vllm-58880-gb300-fused-c1','tps')} tok/s "
                    f"({pct(rows,'vllm-58880-gb300-main-c1','vllm-58880-gb300-fused-c1','tps'):+.0f}%), "
                    f"c8 {val(rows,'vllm-58880-gb300-main-c8','tps')} to "
                    f"{val(rows,'vllm-58880-gb300-fused-c8','tps')} tok/s "
                    f"({pct(rows,'vllm-58880-gb300-main-c8','vllm-58880-gb300-fused-c8','tps'):+.0f}%); "
                    "gsm8k means match (0.855 vs 0.857).")
        if (venue, issue) == ("vLLM", "58887"):
            return ("A race fix at zero cost. The ps-metadata planner rewrote "
                    "shared device buffers with blocking copies that are not "
                    "ordered on the current stream, so a step could run with "
                    "the next step's work maps, faulting deterministically "
                    "(request 111 at c32) or silently corrupting prefill "
                    "when the stale indices stay in bounds. Planning into "
                    "pinned host buffers orders the update: "
                    f"c4 stays {val(rows,'vllm-58887-mi355x-main-c4','tps')} = "
                    f"{val(rows,'vllm-58887-mi355x-fix-c4','tps')} tok/s, "
                    f"c32 goes {val(rows,'vllm-58887-mi355x-main-c32','tps')} to "
                    f"{val(rows,'vllm-58887-mi355x-fix-c32','tps')} tok/s.")
        if (venue, issue) == ("vLLM", "58944"):
            return ("Swaps the sharded latent-MoE up-projection tail from the "
                    "hipBLASLt addmm_ path to aiter's in-place atomic GEMM, "
                    "8.57 to 4.35 microseconds per layer; serving at c16 on "
                    f"1k/1k random goes {val(rows,'vllm-58944-mi355x-addmm-c16','tps')} to "
                    f"{val(rows,'vllm-58944-mi355x-atomic-c16','tps')} tok/s "
                    f"({pct(rows,'vllm-58944-mi355x-addmm-c16','vllm-58944-mi355x-atomic-c16','tps'):+.1f}%), "
                    "TPOT 23.86 to 23.47 ms, gsm8k 5-shot unchanged at 0.9636.")
        if (venue, issue) == ("vLLM", "58986"):
            return ("Retunes the block-FP8 MoE tile config (16/32-row tiles "
                    "instead of the 64-row default) for GLM-5.3-Flash TP4 on "
                    "4xH20, vLLM 0.30.0 with MTP3. The refreshed serving "
                    "table designates the c1-control to c1-return pair as "
                    "primary (both arms carry the mHC register-lifetime "
                    "fix, so only the MoE config differs), at c32: 512/1024 "
                    f"{val(rows,'vllm-58986-h20-control-512-1024-c32','tps')} to "
                    f"{val(rows,'vllm-58986-h20-tuned-512-1024-c32','tps')} tok/s "
                    f"({pct(rows,'vllm-58986-h20-control-512-1024-c32','vllm-58986-h20-tuned-512-1024-c32','tps'):+.1f}%), "
                    f"2048/512 {val(rows,'vllm-58986-h20-control-2048-512-c32','tps')} to "
                    f"{val(rows,'vllm-58986-h20-tuned-2048-512-c32','tps')} "
                    f"({pct(rows,'vllm-58986-h20-control-2048-512-c32','vllm-58986-h20-tuned-2048-512-c32','tps'):+.1f}%) "
                    f"and 512/128 {val(rows,'vllm-58986-h20-control-512-128-c32','tps')} to "
                    f"{val(rows,'vllm-58986-h20-tuned-512-128-c32','tps')} "
                    f"({pct(rows,'vllm-58986-h20-control-512-128-c32','vllm-58986-h20-tuned-512-128-c32','tps'):+.1f}%); "
                    "P99 TTFT falls on every workload (11271.37 to 9205.95 "
                    "ms on 2048/512) and P99 TPOT falls 38.02 to 33.33 ms "
                    "there. The original +27.10% headline ran on the "
                    "unrepaired mHC dependency and is superseded; the "
                    "kernel microbenchmark table (batch 1-4096, in "
                    "microseconds) is parked.")
        if (venue, issue) == ("vLLM", "58989"):
            return ("Moves TRITON ahead of DEEPGEMM for block-FP8 MoE "
                    "auto-selection on SM120. On the real-weights TP1 "
                    "throughput bench (1024/256, 256 prompts) the switch "
                    f"gives {val(rows,'vllm-58989-rtxpro5000-deepgemm','tps')} to "
                    f"{val(rows,'vllm-58989-rtxpro5000-triton','tps')} tok/s "
                    f"({pct(rows,'vllm-58989-rtxpro5000-deepgemm','vllm-58989-rtxpro5000-triton','tps'):+.1f}%) "
                    "while bs1 latency drops 0.800 to 0.678 s and bs32 3.739 "
                    "to 3.250 s, with GSM8K 5-shot 88.02% to 88.55%; the "
                    "dummy-weight table shows the same flat throughput on "
                    "this shape (+0% at TP1, +1% at TP2) with the larger "
                    "wins elsewhere, Qwen3-Next-80B TP2 at +22%, parked as "
                    "dummy-weight rows.")
        if (venue, issue) == ("llama.cpp", "29570"):
            return ("The tensor-API FLASH_ATTN_EXT kernel runs Q*K^T and P*V "
                    "with matmul2d over 64-row KV blocks, 32 queries per "
                    "threadgroup, and only engages when the call is big "
                    "enough to fill the GPU (about 20 queries and up). On "
                    "Qwen3.8-27B Q8_0 with -fa 1, the win scales with KV "
                    f"length: pp512 at 32k context goes "
                    f"{val(rows,'lc-29570-m5-pp512-d32768-master','pp_tps')} to "
                    f"{val(rows,'lc-29570-m5-pp512-d32768-tensor','pp_tps')} tok/s "
                    f"({pct(rows,'lc-29570-m5-pp512-d32768-master','lc-29570-m5-pp512-d32768-tensor','pp_tps'):+.1f}%), "
                    f"at 8k {val(rows,'lc-29570-m5-pp512-d8192-master','pp_tps')} to "
                    f"{val(rows,'lc-29570-m5-pp512-d8192-tensor','pp_tps')} tok/s "
                    f"({pct(rows,'lc-29570-m5-pp512-d8192-master','lc-29570-m5-pp512-d8192-tensor','pp_tps'):+.1f}%), "
                    "while short-context pp512 is flat and the below-"
                    f"threshold pp32 and tg32 give back about 1%: "
                    f"{val(rows,'lc-29570-m5-tg32-master','tps')} to "
                    f"{val(rows,'lc-29570-m5-tg32-tensor','tps')} tok/s "
                    f"({pct(rows,'lc-29570-m5-tg32-master','lc-29570-m5-tg32-tensor','tps'):+.1f}%) on tg32.")
        if (venue, issue) == ("vLLM", "59010"):
            return ("Adds a SM90 CuTe kernel for Qwen4Exp QSA sparse prefill "
                    "(transposed wgmma m64n16k16 GEMMs, cp.async K and V "
                    "rows) that replaces the (32, 1, 1) Triton path above "
                    "2048 programs; BF16 KV only. On the prefill-heavy "
                    "16k-in / 8-out serve at TP4 on H20, c16, total token "
                    f"throughput moves {val(rows,'vllm-59010-h20-triton','pp_tps')} to "
                    f"{val(rows,'vllm-59010-h20-native','pp_tps')} tok/s "
                    f"({pct(rows,'vllm-59010-h20-triton','vllm-59010-h20-native','pp_tps'):+.1f}%) "
                    "with mean TTFT 12.81 to 12.53 s; the kernel "
                    "microbenchmark reports 1.47-1.57x at TP1/TP2 and "
                    "1.32-1.41x at TP4/TP8, and accuracy stays within one "
                    "BF16 ulp of the Triton gated output.")
        if (venue, issue) == ("vLLM", "59040"):
            return ("Quark W8A8 + MTP speculative decoding on Radeon 8060S "
                    "(gfx1151), 400-token greedy single stream: the missing "
                    "quark carve-out left mtp.fc zero-initialized, so the "
                    "drafter emitted token 0 every step (0.0% acceptance) "
                    "and MTP was a loss, "
                    f"{val(rows,'vllm-59040-radeon8060s-spec-none','tps')} to "
                    f"{val(rows,'vllm-59040-radeon8060s-spec-mtp-before','tps')} tok/s "
                    f"({pct(rows,'vllm-59040-radeon8060s-spec-none','vllm-59040-radeon8060s-spec-mtp-before','tps'):+.1f}% vs no speculation); "
                    "the one-line fix restores 22-45% acceptance and "
                    f"{val(rows,'vllm-59040-radeon8060s-spec-mtp-after','tps')} tok/s "
                    f"({pct(rows,'vllm-59040-radeon8060s-spec-none','vllm-59040-radeon8060s-spec-mtp-after','tps'):+.1f}% vs no speculation).")
        if (venue, issue) == ("vLLM", "59054"):
            return ("Triton attention on 4x CMP 170HX (sm80, PP=4), "
                    "MiMo-V2.6-Flash-RL FP8, MTP k=2: the 2D-forcing "
                    "condition (max_seqlen_q > 1) pushes every spec-verify "
                    "batch (q_len>1) onto the 2D varlen kernel, which at "
                    "67K context launches only 4 CTAs on a 70-SM GPU. "
                    "Steady-state decode at 67K context: stock path "
                    f"{val(rows,'vllm-59054-cmp170hx-spec-2d-c67k','tps')} tok/s "
                    "vs the 3D split-KV verify path "
                    f"{val(rows,'vllm-59054-cmp170hx-spec-3d-c67k','tps')} tok/s "
                    f"({pct(rows,'vllm-59054-cmp170hx-spec-2d-c67k','vllm-59054-cmp170hx-spec-3d-c67k','tps'):+.1f}%), "
                    f"while no speculation runs {val(rows,'vllm-59054-cmp170hx-nospec-c67k','tps')} tok/s "
                    f"({pct(rows,'vllm-59054-cmp170hx-nospec-c67k','vllm-59054-cmp170hx-spec-2d-c67k','tps'):+.1f}% vs stock spec) - "
                    "the bug makes speculative decoding a net loss at "
                    "long context on Triton-backend hardware; the kernel-"
                    "level table shows 5.08 to 0.26 ms per verify call "
                    "(19.6x) at q_len 2, 67K KV.")
        if (venue, issue) == ("llama.cpp", "29604"):
            return ("Tensor-split allreduce across two Arc Pro B70 GPUs: the "
                    "blocking dev2dev memcpy and queue drains become pinned-"
                    "host-buffer crosses with async copies; Q8_0, llama-bench, "
                    "f16 KV, -fa on, master vs patched. Every pair improves and "
                    "the win is prefill: pp2048 goes "
                    f"{val(rows,'lc-29604-master-novmm1k','pp_tps')} to "
                    f"{val(rows,'lc-29604-patched-novmm1k','pp_tps')} tok/s "
                    f"({pct(rows,'lc-29604-master-novmm1k','lc-29604-patched-novmm1k','pp_tps'):+.1f}%) "
                    "without VMM and "
                    f"{val(rows,'lc-29604-master-vmm1k','pp_tps')} to "
                    f"{val(rows,'lc-29604-patched-vmm1k','pp_tps')} tok/s "
                    f"({pct(rows,'lc-29604-master-vmm1k','lc-29604-patched-vmm1k','pp_tps'):+.1f}%) "
                    f"with VMM=1 at ub 1024; the ub 256 pairs give "
                    f"{val(rows,'lc-29604-master-novmm256','pp_tps')} to "
                    f"{val(rows,'lc-29604-patched-novmm256','pp_tps')} "
                    f"({pct(rows,'lc-29604-master-novmm256','lc-29604-patched-novmm256','pp_tps'):+.1f}%) "
                    "and "
                    f"{val(rows,'lc-29604-master-vmm256','pp_tps')} to "
                    f"{val(rows,'lc-29604-patched-vmm256','pp_tps')} "
                    f"({pct(rows,'lc-29604-master-vmm256','lc-29604-patched-vmm256','pp_tps'):+.1f}%); "
                    "decode is much flatter, "
                    f"{val(rows,'lc-29604-master-tg128','tps')} to "
                    f"{val(rows,'lc-29604-patched-tg128','tps')} tok/s "
                    f"({pct(rows,'lc-29604-master-tg128','lc-29604-patched-tg128','tps'):+.1f}%) at tg128.")
        if (venue, issue) == ("llama.cpp", "29606"):
            return ("Hexagon HTP work-queue fix (tasks identified by n_pub so "
                    "a stale wakeup cannot re-execute one), OnePlus 13T with "
                    "the v79 NPU, Qwen3.5-4B Q4_0, llama-bench -t 4. The "
                    "author reports the numbers as two repetitions, not a "
                    "performance-equivalence claim, and they sit inside run-"
                    "to-run noise: pp128 "
                    f"{val(rows,'lc-29606-htp-vanilla-pp128','pp_tps')} vs "
                    f"{val(rows,'lc-29606-htp-fixed-pp128','pp_tps')} tok/s "
                    f"({pct(rows,'lc-29606-htp-vanilla-pp128','lc-29606-htp-fixed-pp128','pp_tps'):+.1f}%), "
                    f"tg32 {val(rows,'lc-29606-htp-vanilla-tg32','tps')} vs "
                    f"{val(rows,'lc-29606-htp-fixed-tg32','tps')} tok/s "
                    f"({pct(rows,'lc-29606-htp-vanilla-tg32','lc-29606-htp-fixed-tg32','tps'):+.1f}%); "
                    "the fix itself is the correctness win (the old queue "
                    "aborts with exit 134 / 0x2e under the wakeup-delay "
                    "hook).")
        if (venue, issue) == ("vLLM", "59082"):
            return ("AMX CPU attention: a request-level decode_mask lets "
                    "multi-token MTP verify batches use the grouped GQA "
                    "schedule (auto and FP8 KV), Qwen3.5-4B BF16, 100k-in / "
                    "1k-out serve at c1, three timed requests, main vs branch. "
                    "The MTP3 auto-KV arm is the win, "
                    f"{val(rows,'vllm-59082-amx-main-mtp3-auto','tps')} to "
                    f"{val(rows,'vllm-59082-amx-branch-mtp3-auto','tps')} tok/s "
                    f"({pct(rows,'vllm-59082-amx-main-mtp3-auto','vllm-59082-amx-branch-mtp3-auto','tps'):+.1f}%); "
                    "the FP8-KV arm gains "
                    f"{pct(rows,'vllm-59082-amx-main-mtp3-fp8kv','vllm-59082-amx-branch-mtp3-fp8kv','tps'):+.1f}% "
                    f"in the post-fix run, {val(rows,'vllm-59082-amx-main-mtp3-fp8kv','tps')} to "
                    f"{val(rows,'vllm-59082-amx-branch-mtp3-fp8kv','tps')} tok/s, "
                    "with branch TTFT held at 81.20 s (main 80.73 s) after "
                    "routing non-eligible FP8 batches to the legacy "
                    "materializer, and "
                    "the no-MTP control moved "
                    f"{val(rows,'vllm-59082-amx-main-no-mtp-auto','tps')} to "
                    f"{val(rows,'vllm-59082-amx-branch-no-mtp-auto','tps')} tok/s "
                    f"({pct(rows,'vllm-59082-amx-main-no-mtp-auto','vllm-59082-amx-branch-no-mtp-auto','tps'):+.1f}%), "
                    "so most of the headline gain is the spec-decode path "
                    "itself, not the scheduler change.")
        if (venue, issue) == ("llama.cpp", "29619"):
            return ("--cpu-mtp keeps the MTP drafter block and its recurrent-"
                    "state snapshots in host RAM so a 12 GB card can fit the "
                    "target's KV cache; the hybrid recipe pins the MTP block "
                    "back to the GPU via -ot. On the RTX 5070 Ti Laptop with "
                    "Qwen3-27B REAP192 at 16 k ctx, hybrid recovers most of "
                    "the full-GPU speed, "
                    f"{val(rows,'lc-29619-rtx5070ti-hybrid-c16k','tps')} vs "
                    f"{val(rows,'lc-29619-rtx5070ti-mtp-full-c16k','tps')} tok/s "
                    f"({pct(rows,'lc-29619-rtx5070ti-mtp-full-c16k','lc-29619-rtx5070ti-hybrid-c16k','tps'):+.1f}%), "
                    "while pure --cpu-mtp only adds "
                    f"{pct(rows,'lc-29619-rtx5070ti-mtp-off-c16k','lc-29619-rtx5070ti-cpu-mtp-c16k','tps'):+.1f}% "
                    f"over the {val(rows,'lc-29619-rtx5070ti-mtp-off-c16k','tps')} tok/s "
                    "MTP-off baseline; at 60 k ctx the hybrid edge over pure "
                    f"--cpu-mtp widens to {val(rows,'lc-29619-rtx5070ti-hybrid-c60k','tps')} vs "
                    f"{val(rows,'lc-29619-rtx5070ti-cpu-mtp-c60k','tps')} tok/s "
                    f"({pct(rows,'lc-29619-rtx5070ti-cpu-mtp-c60k','lc-29619-rtx5070ti-hybrid-c60k','tps'):+.1f}%) "
                    "per the author's prior campaign, because the CPU-side "
                    "draft attention cost grows with context.")
        if (venue, issue) == ("llama.cpp", "29620"):
            return ("Fresh 4-variant sweep on the final commits of this "
                    "PR, successor to #29619, whose prior sweep read "
                    "28.7/31.1/51.2/62.5 tok/s. On the RTX 5070 Ti "
                    "Laptop 12 GB with Qwen3-27B REAP192, 12 960-token "
                    "needle, ctx 16 384, KV q4_0: pure --cpu-mtp moved "
                    "up to "
                    f"{val(rows,'lc-29620-rtx5070ti-cpu-mtp-c16k','tps')} "
                    "tok/s while hybrid holds "
                    f"{val(rows,'lc-29620-rtx5070ti-hybrid-c16k','tps')} vs "
                    f"{val(rows,'lc-29620-rtx5070ti-mtp-full-c16k','tps')} tok/s "
                    f"({pct(rows,'lc-29620-rtx5070ti-mtp-full-c16k','lc-29620-rtx5070ti-hybrid-c16k','tps'):+.1f}%) "
                    "and MTP-off stays at "
                    f"{val(rows,'lc-29620-rtx5070ti-mtp-off-c16k','tps')}; "
                    "the 60 k ctx pair (hybrid "
                    f"{val(rows,'lc-29620-rtx5070ti-hybrid-c60k','tps')} vs pure "
                    f"{val(rows,'lc-29620-rtx5070ti-cpu-mtp-c60k','tps')} tok/s) is the "
                    "author's prior campaign repeated in the body.")
        if (venue, issue) == ("vLLM", "59109"):
            return ("PP4 single-container docker deployment where the "
                    "cpu:gloo control plane resolved the container "
                    "hostname to the docker bridge IP, costing ~535 ms "
                    "per control send and collapsing single-stream "
                    "decode with context on DeepSeek-V4.1-Flash 764B "
                    "EXL3: "
                    f"{val(rows,'vllm-59109-cmp170hx-before-c32k','tps')} at "
                    f"32K down to {val(rows,'vllm-59109-cmp170hx-before-c524k','tps')} at "
                    "524K before the fix, and every context point "
                    "recovers after GLOO_SOCKET_IFNAME=lo, "
                    f"{val(rows,'vllm-59109-cmp170hx-after-c32k','tps')}/"
                    f"{val(rows,'vllm-59109-cmp170hx-after-c128k','tps')}/"
                    f"{val(rows,'vllm-59109-cmp170hx-after-c300k','tps')}/"
                    f"{val(rows,'vllm-59109-cmp170hx-after-c524k','tps')} tok/s "
                    f"({pct(rows,'vllm-59109-cmp170hx-before-c524k','vllm-59109-cmp170hx-after-c524k','tps'):+.1f}% at 524K), "
                    "with post-fix concurrency of "
                    f"{val(rows,'vllm-59109-cmp170hx-after-c8','tps')} (C8) to "
                    f"{val(rows,'vllm-59109-cmp170hx-after-c24','tps')} (C24) decode tok/s.")
        if (venue, issue) == ("vLLM", "59112"):
            return ("Packed BLHNC KV layout via FlashInfer re-paging on a "
                    "B300 with Qwen3.6-35B-A3B-FP8 plus the DFlash MRv2 "
                    "drafter (7 speculative tokens), BF16 KV: c1 output "
                    f"moves {val(rows,'vllm-59112-b300-lbhnc-c1','tps')} to "
                    f"{val(rows,'vllm-59112-b300-blhnc-c1','tps')} tok/s "
                    f"({pct(rows,'vllm-59112-b300-lbhnc-c1','vllm-59112-b300-blhnc-c1','tps'):+.1f}%) and c32 "
                    f"{val(rows,'vllm-59112-b300-lbhnc-c32','tps')} to "
                    f"{val(rows,'vllm-59112-b300-blhnc-c32','tps')} "
                    f"({pct(rows,'vllm-59112-b300-lbhnc-c32','vllm-59112-b300-blhnc-c32','tps'):+.1f}%, "
                    "per-run 7258.52/7183.57), while KV groups drop 46 to "
                    "5 and reported capacity rises 2.2%; the 8192-in/1-out "
                    f"req/s pair moves {val(rows,'vllm-59112-b300-lbhnc-8k1','tps')} to "
                    f"{val(rows,'vllm-59112-b300-blhnc-8k1','tps')}.")
        if (venue, issue) == ("vLLM", "59151"):
            return ("CDNA2 (gfx90a) mxfp4 MoE on 4x MI210 running the "
                    "TRITON_UNFUSED backend that ROCm auto-selection "
                    "never offered: "
                    f"{val(rows,'vllm-59151-mi210-triton-unfused-c1','tps')} tok/s "
                    "single-stream decode with the DFlash drafter versus "
                    f"{val(rows,'vllm-59151-mi210-triton-unfused-c32','tps')} tok/s "
                    "aggregate across 32 concurrent streams in a 262K-"
                    "context config whose needle retrieval was verified "
                    "at 1,038,700 tokens.")
        if (venue, issue) == ("llama.cpp", "29635"):
            return ("Prefix-LM attention-mask PR for DFM Mimir "
                    "HRM-Text models, checked for collateral damage on "
                    "a normal model: Llama-3.2-1B Q8_0 on a GTX 1060, "
                    "llama-bench, means of the last two of three "
                    "alternating runs. "
                    f"Master {val(rows,'lc-29635-gtx1060-master','tps')} versus "
                    f"PR {val(rows,'lc-29635-gtx1060-pr','tps')} t/s "
                    "tg128 (pp512 2381 versus 2380), i.e. neutral; "
                    "the PR's real effect is accuracy, DAISY exact "
                    "match 5.9 pct to 8.3 pct against 8.4 pct for "
                    "official transformers.")
        if (venue, issue) == ("llama.cpp", "29679"):
            return ("Vulkan MMVQ: the 4-rows-per-workgroup policy was only "
                    "applied at 8 columns on RDNA3 with the AMD proprietary "
                    "driver, so 5-7 column batches (spec decoding, multi-slot "
                    "serving) ran up to 7x slower (q4_K n=7: 497 vs 71 us). "
                    "RX 7900 XTX, Windows 11, driver 26.8.1 (LLPC), Q4_K_S "
                    "64k ctx KV q4_0 MTP draft, t/s per client over 4 runs. "
                    "The control slot is flat "
                    f"({val(rows,'lc-29679-7900xtx-control-master','tps')} vs "
                    f"{val(rows,'lc-29679-7900xtx-control-pr','tps')}, "
                    "noise: one master run hit 70.7, the rest matched). "
                    "The broken batches jump: 2 slots "
                    f"{val(rows,'lc-29679-7900xtx-2slot-master','tps')} -> "
                    f"{val(rows,'lc-29679-7900xtx-2slot-pr','tps')}, 3 slots "
                    f"{val(rows,'lc-29679-7900xtx-3slot-master','tps')} -> "
                    f"{val(rows,'lc-29679-7900xtx-3slot-pr','tps')}, and the "
                    "5-token draft batch "
                    f"{val(rows,'lc-29679-7900xtx-nmax5-master','tps')} -> "
                    f"{val(rows,'lc-29679-7900xtx-nmax5-pr','tps')}. The "
                    "llama-bench ms-per-batch table shows the same shape: "
                    "Q4_K_S n=6 157.6 -> 31.3 ms, n=7 256.6 -> 36.1 ms; one "
                    "small regression, pure Q4_0 n=7 42.0 -> 46.4 ms.")
        if (venue, issue) == ("vLLM", "59488"):
            return ("MoE backend A/B for DeepSeek-V4.1-Flash (MXFP4 experts) "
                    "on 8x H200, TP8+EP, per-token FP8 activations, offline "
                    "LLM runs, decode 64 prompts x 512 in / 256 out, 2 "
                    "repeats. The upstream body was rewritten on 2026-10-01 "
                    "and the original six-layout serving table was removed; "
                    "the surviving absolute figures are "
                    f"{val(rows,'vllm-59488-h200-fp8-dec-marlin','tps'):g} "
                    f"(Marlin, today's Hopper default) vs "
                    f"{val(rows,'vllm-59488-h200-fp8-dec-humming','tps'):g} "
                    "output tok/s: Humming's grouped GEMM is 16% behind "
                    "Marlin, and the PR's new default (indexed GEMM on SM90) "
                    "is 14% faster than grouped, published only as a "
                    "percentage. The rewritten body also reports indexed vs "
                    "grouped gains of +47% prefill / +63% decode with BF16 "
                    "activations and +24% / +36% with FP8, again without "
                    "absolute numbers.")
        if (venue, issue) == ("vLLM", "59489"):
            return ("Backend parity A/B: the Rust vllm-bench port of the "
                    "openai-responses backend vs Python vllm bench serve. "
                    f"Rust: {val(rows,'vllm-59489-rtx3070-rust','tps')}-1680, "
                    f"Python: {val(rows,'vllm-59489-rtx3070-python','tps')}-1673 "
                    "output tok/s over three runs, 200/200 requests each, "
                    "with TPOT/ITL within run noise. The point of the PR is "
                    "parity for the Responses API, not a speedup.")
        if (venue, issue) == ("llama.cpp", "29768"):
            return ("Decode TPS on RTX 5090 with an 8-sequence unified 128K "
                    "KV cache. The patch recaptures a changed CUDA graph "
                    "instead of resetting warmup every time the padded KV "
                    f"length steps. {val(rows,'lc-29768-rtx5090-pre','tps')} -> "
                    f"{val(rows,'lc-29768-rtx5090-post','tps')} tok/s, +1.14%, "
                    "mean of 10 paired per-repetition changes (95% CI "
                    "+0.44% to +1.84%).")
        if (venue, issue) == ("llama.cpp", "29820"):
            return ("HIP MMVQ threshold A/B on the Radeon AI PRO R9700 "
                    "(gfx1201). Stock routes quantized matmuls of 5-8 "
                    "columns to MMVQ, which is up to 46% slower than MMQ at "
                    "those sizes on this chip; the patch lowers "
                    "MMVQ_MAX_BATCH_SIZE from 8 to 4. Concurrent decode "
                    "(llama-batched-bench, ntg 128) is flat at 1, 2, 4 and "
                    "16 sequences but the 5-8 sequence band lifts: "
                    f"{val(rows,'lc-29820-r9700-npl5-stock','tps'):g} -> "
                    f"{val(rows,'lc-29820-r9700-npl5-patched','tps'):g} t/s "
                    "(+13%) at 5, "
                    f"{val(rows,'lc-29820-r9700-npl6-stock','tps'):g} -> "
                    f"{val(rows,'lc-29820-r9700-npl6-patched','tps'):g} "
                    "(+24%) at 6, "
                    f"{val(rows,'lc-29820-r9700-npl8-stock','tps'):g} -> "
                    f"{val(rows,'lc-29820-r9700-npl8-patched','tps'):g} "
                    "(+44%) at 8. Perplexity is unchanged (5.3652 stock vs "
                    "5.3703 patched) and test-backend-ops passes; only the "
                    "R9700 and Q4_K_M were tested, and the author notes the "
                    "threshold should probably be architecture-dependent.")
        if (venue, issue) == ("llama.cpp", "29809"):
            return ("SYCL MXFP4 MoE A/B on Intel Arc Pro B70 (Windows 11, "
                    "oneAPI 2026.0, EPYC 7402P host). The patch replaces "
                    "table-based MXFP4 decoding with bit-identical 32-bit "
                    "arithmetic plus lazy per-expert weight reordering. "
                    "gpt-oss 20B decode on one card: "
                    f"{val(rows,'lc-29809-b70-20b-dec-before','tps')} -> "
                    f"{val(rows,'lc-29809-b70-20b-dec-after','tps')} tok/s "
                    "(1.91x, 5 repetitions); gpt-oss 120B decode on two "
                    f"cards: {val(rows,'lc-29809-2xb70-120b-dec-before','tps')} -> "
                    f"{val(rows,'lc-29809-2xb70-120b-dec-after','tps')} tok/s "
                    "(2.02x, 2 repetitions). Prompt processing barely moves "
                    f"({val(rows,'lc-29809-2xb70-120b-pp-before','pp_tps')} -> "
                    f"{val(rows,'lc-29809-2xb70-120b-pp-after','pp_tps')} "
                    "tok/s): the win is in the decode-side expert matmuls. "
                    "Perplexity 14.5148 -> 14.5129, within noise.")
        if (venue, issue) == ("vLLM", "59434"):
            return ("CPU A/B on AMD Zen 5 (Turin), the fix that makes the "
                    "ZenDNN fast routed MoE path eligible. bf16 expert scales "
                    "failed the f32-only eligibility gate and silently used the "
                    "generic per-expert path; the f32 arm takes the fast path. "
                    "Measured totals rise with the fast path: "
                    f"{val(rows,'vllm-59434-zen5-before-s8','tps')} -> "
                    f"{val(rows,'vllm-59434-zen5-after-s8','tps')} at max-num-seqs "
                    "8 and "
                    f"{val(rows,'vllm-59434-zen5-before-s32','tps')} -> "
                    f"{val(rows,'vllm-59434-zen5-after-s32','tps')} at 32 total "
                    "tok/s (vllm bench throughput counts input plus output). "
                    "The point of the PR is eligibility, not a measured "
                    "speedup.")
        if (venue, issue) == ("vLLM", "59367"):
            return ("Bug-fix validation, three configurations on the same "
                    "4x H200 NVL DCP4 deployment (GLM-5.3-NVFP4, MTP 3, "
                    "fp8_ds_mla). Prefill (fresh, longer context is slightly "
                    "slower in all arms): 8x32768 "
                    f"{val(rows,'vllm-59367-h200nvl-bothfix-pp-c32k','pp_tps')} "
                    "patched vs "
                    f"{val(rows,'vllm-59367-h200nvl-unpatched-pp-c32k','pp_tps')} "
                    "on the unpatched production image the same night (within "
                    "noise, the fix is about memory reservation, not speed); "
                    "2x131072 "
                    f"{val(rows,'vllm-59367-h200nvl-bothfix-pp-c131k','pp_tps')} "
                    "vs "
                    f"{val(rows,'vllm-59367-h200nvl-unpatched-pp-c131k','pp_tps')}"
                    "Decode figures are single samples; across seven boots of "
                    "the unpatched image N=8 ranged 263 to 317 and N=32 701 to "
                    "838, so no decode change is claimed either way. The "
                    "est0 rows are the second boot with "
                    "VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=0 and only the "
                    "merge-scratch fix - the combination that OOMed before, "
                    "now clean with 0.8 GiB free per GPU. Sister PR #59368 "
                    "carries the identical sweep and was not re-mined.")
        if (venue, issue) == ("vLLM", "59355"):
            return ("Bug-fix pair, not a tuning win: the 12-line OOB guard in "
                    "the block-verification residual-mass kernel removes the "
                    "crash at concurrency 128 (unpatched: 2/2 runs died with "
                    "cudaErrorIllegalAddress after 131/320 requests; patched: "
                    "1/1 clean, 320/320) with no throughput cost - "
                    f"{val(rows,'vllm-59355-h200-oob-before','tps')} tok/s on "
                    "the partial before run vs "
                    f"{val(rows,'vllm-59355-h200-oob-after','tps')} tok/s "
                    "after, same random 10000-in/5000-out workload, dspark "
                    "spec config on 8x H200 (TP2 x DP4 + EP). The mean "
                    "speculative acceptance length also rose 2.145 -> 2.399, "
                    "though the before arm died early (n=23 vs n=54).")
        if (venue, issue) == ("vLLM", "59280"):
            return ("ROCm FlyDSL prefill MQA-logits kernel for the "
                    "sparse indexer (gfx950, opt-in env flag) vs the "
                    "Gluon baseline, GLM-5.2-MXFP4, TP4 MI355X, "
                    "per-GPU throughput. Same build for both runs; "
                    "only the flag changes. At ISL 60000 / OSL 600 "
                    "FlyDSL is the small winner (e.g. "
                    f"{val(rows,'vllm-59280-mi355x-60k-gluon-c32','tps')} -> "
                    f"{val(rows,'vllm-59280-mi355x-60k-flydsl-c32','tps')} tput/GPU "
                    "at conc 32, TTFT 13285.8 -> 12848 ms); at "
                    "8192-in/1024-out and 1024-in/"
                    "1024-out the two kernels are within noise "
                    f"(geomean over all 18 points 1560.4 -> 1558.5, "
                    "-0.1 pct). The real gain is kernel-time: the "
                    "prefill MQA-logits kernel drops 35 pct (1.53x) "
                    "and the same 16k prefill chunk runs 153.4 -> "
                    "98.7 ms. GPQA Diamond single-run 0.899 vs "
                    "0.884 (stderr about 0.02), RULER niah 1.00 at "
                    "64k and 128k both arms.")
        if (venue, issue) == ("llama.cpp", "29639"):
            return ("Vulkan sparse flash attention extended to "
                    "quantized K/V (Qwen3.8-Flash-Next QSA, q8_0 KV, "
                    "decode at growing KV depth, 4 interleaved rounds "
                    "against master + #29591). The body tags the "
                    "sanity numbers for both R9700 and 7900 XT and "
                    "the table is not GPU-tagged; rows here are "
                    "attributed to the R9700 rig. Flat at depth 0 "
                    f"({val(rows,'lc-29639-r9700-master-c0','tps')}/"
                    f"{val(rows,'lc-29639-r9700-pr-c0','tps')}), noisy at 32k "
                    f"({val(rows,'lc-29639-r9700-master-c32k','tps')}/"
                    f"{val(rows,'lc-29639-r9700-pr-c32k','tps')}, +2.1%/-0.6% "
                    "per session), the largest gain at 64k "
                    f"({val(rows,'lc-29639-r9700-master-c64k','tps')}/"
                    f"{val(rows,'lc-29639-r9700-pr-c64k','tps')}, +15.6%) and "
                    f"{pct(rows,'lc-29639-r9700-master-c128k','lc-29639-r9700-pr-c128k','tps'):+.1f}% at 128k; "
                    "f16 cache and prompt processing unchanged.")
        if (venue, issue) == ("vLLM", "40551"):
            return ("The reporter expected MRV2's draft-prob-aware sampling to "
                    f"help and got the opposite: at temperature 1, MRV2 "
                    f"collapses to {val(rows,'vllm-40551-rtxpro6000-qwen3-8b-bf16-eagle3-mrv2-temp1','tps')} tok/s "
                    f"({pct(rows,'vllm-40551-rtxpro6000-qwen3-8b-bf16-eagle3-mrv2-temp0','vllm-40551-rtxpro6000-qwen3-8b-bf16-eagle3-mrv2-temp1','tps'):+.0f}% "
                    f"vs its own temperature 0), while MRV1 degrades gently "
                    f"from {val(rows,'vllm-40551-rtxpro6000-qwen3-8b-bf16-eagle3-mrv1-temp0','tps')} to "
                    f"{val(rows,'vllm-40551-rtxpro6000-qwen3-8b-bf16-eagle3-mrv1-temp1','tps')} tok/s "
                    f"({pct(rows,'vllm-40551-rtxpro6000-qwen3-8b-bf16-eagle3-mrv1-temp0','vllm-40551-rtxpro6000-qwen3-8b-bf16-eagle3-mrv1-temp1','tps'):+.0f}%).")
        if (venue, issue) == ("llama.cpp", "26750"):
            if "W7900" in hw:
                return ("Same GGUF, same b10290 build, same prompts as the "
                        "CUDA rows: MTP acceptance on this GPU is 92.2% and "
                        f"decode goes {val(rows,'lc-26750-w7900-base','tps')} to "
                        f"{val(rows,'lc-26750-w7900-mtp','tps')} tok/s "
                        f"({pct(rows,'lc-26750-w7900-base','lc-26750-w7900-mtp','tps'):+.0f}%). "
                        "The issue's point is the contrast: the CUDA path "
                        "runs the same model at 35.8% acceptance, "
                        "deterministic across full matrix reruns and "
                        "invariant to slot count and context, which it reads "
                        "as the MTP head forward degrading on CUDA.")
            if "7800" in hw:
                return ("Same GGUF and b10290 build, RADV: MTP acceptance "
                        f"91.4% and decode {val(rows,'lc-26750-7800xt-base','tps')} to "
                        f"{val(rows,'lc-26750-7800xt-mtp','tps')} tok/s "
                        f"({pct(rows,'lc-26750-7800xt-base','lc-26750-7800xt-mtp','tps'):+.0f}%), "
                        "against 35.8% acceptance on the CUDA path, where "
                        "the same feature is a net loss.")
            return ("MTP on the CUDA path is a deterministic 35.8% "
                    "acceptance (a full matrix rerun reproduced the figure "
                    "exactly), invariant to slot count and context, which "
                    "the issue reads as the MTP head forward producing "
                    f"degraded predictions on CUDA: decode "
                    f"{val(rows,'lc-26750-cuda-mtp','tps')} vs baseline "
                    f"{val(rows,'lc-26750-cuda-base','tps')} tok/s "
                    f"({pct(rows,'lc-26750-cuda-base','lc-26750-cuda-mtp','tps'):+.0f}%). "
                    "Combined with draftless the waste is ~6400-8600 drafted "
                    "tokens for a 400-token output at 3.8% acceptance.")
        if (venue, issue) == ("llama.cpp", "27117"):
            return ("DFlash drafts under 16 concurrent slots get corrupted "
                    "per slot: 16 identical requests show an ~8x spread in "
                    "acceptance from the first speculative tick, and "
                    f"throughput inverts to {val(rows,'lc-27117-nospec16','tps')} tok/s. "
                    "The fix is length, not backend: --spec-draft-n-max 1 "
                    f"accepts 83-92% and runs {val(rows,'lc-27117-dflash-nmax1','tps')} tok/s "
                    f"({pct(rows,'lc-27117-nospec16','lc-27117-dflash-nmax1','tps'):+.0f}% "
                    "over the no-spec row). The pathology still reproduced "
                    "on master as of 2026-08-15.")
        if (venue, issue) == ("llama.cpp", "27544"):
            if "lc-27544-vk-1-s" in rows:
                return ("With -np > 1, MTP n-max > 1 collapses on Vulkan: "
                        "parallel over single-session scaling is "
                        f"{val(rows,'lc-27544-vk-r4-p','tps')}/{val(rows,'lc-27544-vk-r4-s','tps')} = "
                        f"{val(rows,'lc-27544-vk-r4-p','tps')/val(rows,'lc-27544-vk-r4-s','tps'):.2f}x at n-max 1 "
                        "(run r4, np 3), but "
                        f"{val(rows,'lc-27544-vk-r3-p','tps')}/{val(rows,'lc-27544-vk-r3-s','tps')} = "
                        f"{val(rows,'lc-27544-vk-r3-p','tps')/val(rows,'lc-27544-vk-r3-s','tps'):.2f}x at n-max 2 "
                        f"and {val(rows,'lc-27544-vk-r2-p','tps')}/{val(rows,'lc-27544-vk-r2-s','tps')} = "
                        f"{val(rows,'lc-27544-vk-r2-p','tps')/val(rows,'lc-27544-vk-r2-s','tps'):.2f}x at n-max 3. "
                        "Per-position acceptance falls with n-max on "
                        "parallel runs (about 0.69 single, n-max 1, down to "
                        "0.39-0.53). The reporter suspects the Vulkan "
                        "backend's interworking with sessions and "
                        "speculation; NVIDIA is not affected.")
            return ("The same matrix on ROCm scales better: at n-max 1, "
                    f"np3 is {val(rows,'lc-27544-r1t','tps')} vs single "
                    f"{val(rows,'lc-27544-r1s','tps')} tok/s "
                    f"({val(rows,'lc-27544-r1t','tps')/val(rows,'lc-27544-r1s','tps'):.2f}x), and "
                    "n-max 3 still scales: "
                    f"{val(rows,'lc-27544-r2t','tps')} vs "
                    f"{val(rows,'lc-27544-r2s','tps')} tok/s "
                    f"({val(rows,'lc-27544-r2t','tps')/val(rows,'lc-27544-r2s','tps'):.2f}x), "
                    "where the Vulkan rows only manage about 1.1x.")
        if (venue, issue) == ("llama.cpp", "28863"):
            return ("The -ub sweep is flat "
                    f"({val(rows,'lc-28863-rocm-ub512','tps')} to "
                    f"{val(rows,'lc-28863-rocm-ub4096','tps')} tok/s), so ubatch is "
                    "not the lever here, and layer split is worse on "
                    f"throughput ({val(rows,'lc-28863-rocm-layer-q4kxl','tps')} vs "
                    f"{val(rows,'lc-28863-rocm-tensor-q4kxl','tps')} at Q4_K_XL, "
                    f"{val(rows,'lc-28863-rocm-layer-q8','tps')} vs "
                    f"{val(rows,'lc-28863-rocm-tensor-q8','tps')} at Q8_0) even "
                    "though its per-active-card utilization is higher. The "
                    "issue's working hypothesis: splitting a batch-1 GEMV "
                    "halves the output rows per launch, drops waves per SIMD "
                    "below the occupancy threshold, and the pair delivers "
                    "only 43.0% of its DRAM bandwidth (65.9% solo).")
        if (venue, issue) == ("llama.cpp", "29534"):
            if model == "Meta-Llama-3-8B-Instruct":
                return ("The wave64 Q8 flash-attention path (GCN, gfx906) "
                        f"lifts decode where KV depth is shallow: "
                        f"{val(rows,'lc-29534-llama-master-d4k','tps')} to "
                        f"{val(rows,'lc-29534-llama-wave64-d4k','tps')} at 4096 ctx "
                        f"({pct(rows,'lc-29534-llama-master-d4k','lc-29534-llama-wave64-d4k','tps'):+.0f}%), "
                        f"{val(rows,'lc-29534-llama-master-d8k','tps')} to "
                        f"{val(rows,'lc-29534-llama-wave64-d8k','tps')} at 8192 ctx "
                        f"({pct(rows,'lc-29534-llama-master-d8k','lc-29534-llama-wave64-d8k','tps'):+.0f}%), "
                        "with prefill flat. The kernel microbench in the same "
                        "PR shows the gain concentrated below KV 10k (up to "
                        "+92.37% at KV 4096) and flat beyond.")
            return ("The same patch on the D256 head: "
                    f"{val(rows,'lc-29534-qwen-master-d4k','tps')} to "
                    f"{val(rows,'lc-29534-qwen-wave64-d4k','tps')} at 4096, "
                    f"{val(rows,'lc-29534-qwen-master-d16k','tps')} to "
                    f"{val(rows,'lc-29534-qwen-wave64-d16k','tps')} at 16384, "
                    f"{val(rows,'lc-29534-qwen-master-d32k','tps')} to "
                    f"{val(rows,'lc-29534-qwen-wave64-d32k','tps')} at 32768 "
                    f"(the source prints the last figure as ~18.86). The "
                    f"gain widens with context, "
                    f"{pct(rows,'lc-29534-qwen-master-d4k','lc-29534-qwen-wave64-d4k','tps'):+.0f}% "
                    f"to {pct(rows,'lc-29534-qwen-master-d32k','lc-29534-qwen-wave64-d32k','tps'):+.0f}%.")
        if (venue, issue) == ("llama.cpp", "28454"):
            return ("Quantized KV falls off the sparse-fa fused kernel: the "
                    "dispatch added in #27970 is only reachable through the "
                    "mma_f16 path, which requires non-quantized K/V, so "
                    "single-query decode with q8_0 KV is forced onto the VEC "
                    "kernel: "
                    f"{val(rows,'lc-28454-a6000-kvf16','tps')} to "
                    f"{val(rows,'lc-28454-a6000-kvq8','tps')} tok/s "
                    f"({pct(rows,'lc-28454-a6000-kvf16','lc-28454-a6000-kvq8','tps'):+.0f}%), "
                    "with GPU utilization at only 24-37% during q8_0 decode "
                    "(memory/latency-bound, 4x A6000, ctx 1048576).")
        return None

    venue_order = {"llama.cpp": 0, "vLLM": 1, "ExLlamaV2": 2, "HF": 3}
    multi_ab = {k: v for k, v in ab_groups.items() if len(v) >= 2}
    all_by_id = {r["id"]: r for r in records}
    ab_sections = []
    for (venue, issue, hw, model, backend), rs in sorted(
            multi_ab.items(),
            key=lambda kv: (venue_order.get(kv[0][0], 9),
                            int(kv[0][1]) if kv[0][1].isdigit() else 0,
                            kv[0][3].lower(), kv[0][2].lower())):
        by_id = {r["id"]: r for r in rs}
        url = rs[0].get("source_url") or ""
        rows_html = "".join(ab_row(r) for r in
                            sorted(rs, key=lambda r: (cfg_token(r), r["id"])))
        note = ab_note(venue, issue, hw, model, by_id)
        note_html = (f"<p><strong>Note:</strong> {note}</p>" if note else "")
        ab_sections.append(f"""<h3>{esc(model)} on {esc(hw)} ({esc(backend)}) - {esc(venue)} <a href=\"{esc(url)}\" rel=\"nofollow\">#{esc(issue)}</a></h3>
<table><tr><th>config</th><th>tok/s</th><th>pp tok/s</th><th>batch</th><th>record</th><th>source</th></tr>{rows_html}</table>
{note_html}""")
    write("notes/build-ab.html", page("Build A/B notes", f"""
<h1>Build A/B notes</h1>
<p>Regressions and improvements between builds of the same backend. Each section is a
group of records on the same model, chip, and backend where the rows differ only in
build or configuration (the <code>config</code> column is the distinguishing tag from
the record notes). {len(multi_ab)} comparable groups, {sum(len(v) for v in multi_ab.values())}
records; every number is rendered from the record at build time. A <strong>note</strong>
is present where the source or this project interprets the delta; the rest are
recorded as published.</p>
{''.join(ab_sections)}
<p><a href="/backends/">&larr; cross-backend notes</a></p>"""))

    # --- cross-source checks (analysis) ---
    # Where a measured llama.cpp row and a bandwidth-model estimate cell cover
    # the same model+chip at the same quant+ctx, show both and the delta.
    # Estimates live in data/reference/ (v3: reference values, not records).
    est_by_key = {}
    for r in ref_records:
        if (r["id"].startswith("llmconfigurator-est") and r.get("ctx") == 4096
                and r.get("quant") == "Q4_K_M"):
            est_by_key[(mkey(r["model"]), r["hardware"])] = r
    check_rows = {}
    for r in records:
        if (r.get("provenance") in ("sourced", "community")
                and "llama.cpp" in (r.get("backend") or "")
                and r.get("ctx") == 4096 and r.get("quant") == "Q4_K_M"):
            k = (mkey(r["model"]), r["hardware"])
            if k in est_by_key:
                prev = check_rows.get(k)
                if prev is None or (r.get("tps") or 0) > (prev[0].get("tps") or 0):
                    check_rows[k] = (r, est_by_key[k])
    def overlap_lines(pairs, with_quant=False, label=True):
        lines, oos = [], []
        for (m, h), (mr, er) in sorted(pairs.items()):
            delta = (er["tps"] - mr["tps"]) / mr["tps"] * 100
            in_sample = abs(delta) < 0.5
            if not in_sample and label:
                oos.append(abs(delta))
            q = f"<td class=\"num\">{esc(mr.get('quant'))}</td>" if with_quant else ""
            if not label:
                cls = "reference"
            elif in_sample:
                cls = "in-sample (fitted)"
            else:
                cls = "out-of-sample"
            lines.append(
                f"<tr><td><a href=\"/models/{slug(mr['model'])}/\">{esc(mr['model'])}</a></td>"
                f"<td><a href=\"/hardware/{slug(h)}/\">{esc(h)}</a></td>"
                f"{q}"
                f"<td class=\"num\">{esc(mr['tps'])}</td>"
                f"<td><a href=\"{esc(mr['source_url'])}\" rel=\"nofollow\">source</a></td>"
                f"<td class=\"num\">{esc(er['tps'])}</td>"
                f"<td class=\"num\">{delta:+.1f}%</td>"
                f"<td>{cls}</td></tr>")
        return lines, oos

    check_lines, oos = overlap_lines(check_rows)
    # reference overlaps: same model+chip+ctx+backend but the measured row is
    # another Q4-K quant (the estimate is Q4_K_M); labeled, not mixed in
    ref_rows = {}
    for r in records:
        if (r.get("provenance") in ("sourced", "community")
                and "llama.cpp" in (r.get("backend") or "")
                and r.get("ctx") == 4096
                and str(r.get("quant") or "").upper().startswith("Q4_K")
                and r.get("quant") != "Q4_K_M"):
            k = (mkey(r["model"]), r["hardware"])
            if k in est_by_key:
                prev = ref_rows.get(k)
                if prev is None or (r.get("tps") or 0) > (prev[0].get("tps") or 0):
                    ref_rows[k] = (r, est_by_key[k])
    ref_lines, oos_ref = overlap_lines(ref_rows, with_quant=True, label=False)
    if oos:
        verdict = ("Strict-overlap rows differ by at most %.1f%%; in-sample "
                   "configurations (the model was fitted from those runs) "
                   "agree by construction." % max(oos))
    elif ref_lines:
        verdict = ("All strict overlaps are in-sample (fitted) configurations; "
                   "the Q4-K family reference table below is the first "
                   "out-of-quant view, where part of the delta is the quant "
                   "difference itself.")
    else:
        verdict = ("No overlap yet; both tables fill in as sources cover the "
                   "same model + chip + ctx.")
    write("notes/cross-source.html", page("Cross-source checks", f"""
<h1>Cross-source checks</h1>
<p>Where a <strong>measured</strong> llama.cpp row (any source) and the LLM
Configurator <strong>bandwidth-model estimate</strong> cover the same model +
chip at Q4_K_M / 4096 ctx, they are shown side by side. {len(check_rows)}
strict overlaps so far.</p>
<table><tr><th>model</th><th>hardware</th><th>measured tok/s</th><th>source</th>
<th>estimated tok/s</th><th>delta</th><th>class</th></tr>{''.join(check_lines)}</table>
<h2>Q4-K family reference (measured quant differs from the estimate's)</h2>
<p>Same model + chip + 4096 ctx, but the measured row is another Q4-K quant;
the quant difference contributes part of the delta.</p>
{'<table><tr><th>model</th><th>hardware</th><th>measured quant</th><th>measured tok/s</th><th>source</th><th>estimated tok/s</th><th>delta</th><th>class</th></tr>' + ''.join(ref_lines) + '</table>' if ref_lines else '<p class="dim">No reference overlaps yet.</p>'}
<p class=\"dim\">{esc(verdict)} Estimated values: LLM Configurator benchmark
cells (CC BY 4.0), calibrated per GPU architecture from the 14 measured runs
in their published dataset. Delta = (estimated - measured) / measured.</p>
<p><a href=\"/backends/\">← cross-backend notes</a> · <a href=\"/notes/build-ab.html\">build A/B notes</a></p>"""))

    # --- data page ---
    schema_fields = [
        ("id", "stable unique slug for the record"),
        ("model", "model name as published by the source"),
        ("params", "parameter size, as published (e.g. 8B, 3.8B)"),
        ("quant", "quantization (e.g. Q4_K_M)"),
        ("hardware", "chip/hardware identifier (e.g. M5 Max, RTX 4090)"),
        ("ram_gb", "memory, GB (when the source states it)"),
        ("backend", "inference backend/engine (llama.cpp, MLX, Ollama, vLLM, …)"),
        ("ctx", "context depth the benchmark actually ran at (when stated; null when the harness did not fix a context)"),
        ("batch", "batch size / concurrency (when stated)"),
        ("tps", "generation tokens/second"),
        ("pp_tps", "prompt-processing tokens/second (when reported)"),
        ("pp_tokens", "prompt token length of the prompt test (e.g. 512 for pp512)"),
        ("tg_tokens", "generation token length of the decode test (e.g. 128 for tg128)"),
        ("scope", "record scope: empty = in scope; cluster = multi-node/cluster run, reference area only"),
        ("ttft_s", "time to first token, seconds (when reported)"),
        ("power_w", "power draw, watts (when reported)"),
        ("flags", "computed flags: contradiction / outlier (see schema.md rules 4-5)"),
        ("date", "original measurement date, as published"),
        ("provenance", "sourced | community | estimated (see schema)"),
        ("source_url", "URL the number was retrieved from"),
        ("source_name", "name of the source dataset/page"),
        ("retrieved", "date this record was retrieved"),
        ("quote", "exact values as they appear in the source (comma-joined row)"),
        ("notes", "collector notes"),
    ]
    schema_rows = "".join(f"<tr><td><code>{n}</code></td><td>{esc(d)}</td></tr>" for n, d in schema_fields)
    write("data/index.html", page("Dataset", f"""
<h1>The dataset</h1>
<p>{len(records)} measured records, retrieved {esc(retrieved)}. Download and diff: the data is the
product, not the site. Reference estimates are kept apart from records (see below).</p>
<ul>
<li><a href="/data/records.csv">records.csv</a> (measured records only)</li>
<li><a href="/data/records.json">records.json</a> (measured records only)</li>
<li><a href="/data/reference/estimates.json">reference/estimates.json</a> ({ref['count']} reference estimates, not records)</li>
<li><a href="/data/reference/cluster.json">reference/cluster.json</a> ({clu['count']} cluster/multi-node runs, measured and source-cited but out of record scope)</li>
<li><a href="/data/sources.json">sources.json</a> (source registry)</li>
</ul>
<h2>Schema</h2>
<table><tr><th>field</th><th>meaning</th></tr>{schema_rows}</table>
<h2>No record without provenance</h2>
<p>Every row carries <code>source_url</code>, <code>retrieved</code>, and <code>quote</code>
(the exact values as published). <code>estimated</code> rows (the source's own model-based
estimates) are reference values, not records: they live in
<code>data/reference/estimates.json</code>, are excluded from record counts, and are only
shown where explicitly labeled (lookup toggle, cross-source checks).</p>
<p>Rules and field semantics: <a href="https://github.com/tokatlas/tokatlas.github.io/blob/main/data/schema.md">data/schema.md</a>.</p>
"""))

    # --- changelog ---
    with open(os.path.join(ROOT, "CHANGELOG.md")) as f:
        raw = f.read()
    entries = []
    cur = None
    for line in raw.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            entries.append([cur, []])
        elif entries and line.startswith("- "):
            entries[-1][1].append(line[2:])
    cl = "".join(f"""<h3>{esc(t)}</h3><ul>{''.join('<li>%s</li>' % esc(b) for b in bs)}</ul>"""
                 for t, bs in entries)
    write("changelog.html", page("Changelog", f"<h1>Changelog</h1>{cl}"))

    # --- lookup ---
    lookup_body = """
<h1>What speed will I get?</h1>
<p>Pick hardware and (optionally) a model, quant, or backend. Every row links to its
source. Reference estimates (source models, not measurements) are excluded by
default; tick the box to include them, badged.</p>
<div class="filters">
<label>hardware <select id="f-hw"></select></label>
<label>model <select id="f-model"></select></label>
<label>quant <select id="f-quant"></select></label>
<label>backend <select id="f-be"></select></label>
<label class="check"><input type="checkbox" id="f-ref"> include reference estimates</label>
<label class="check"><input type="checkbox" id="f-clu"> include cluster runs (out of scope)</label>
</div>
<p id="lcount" class="dim"></p>
<div id="ltable"></div>
<script>
Promise.all([fetch('/data/records.json').then(r => r.json()),
             fetch('/data/reference/estimates.json').then(r => r.json()).catch(() => ({records: []})),
             fetch('/data/reference/cluster.json').then(r => r.json()).catch(() => ({records: []}))])
.then(([ds, ref, clu]) => {
  const recs = ds.records;
  const refs = ref.records || [];
  const clus = clu.records || [];
  const sel = id => document.getElementById(id);
  const opts = (id, vals) => {
    const el = sel(id);
    el.innerHTML = '<option value="">any</option>';
    [...new Set(vals)].sort().forEach(v => {
      if (v) el.add(new Option(v, v));
    });
  };
  opts('f-hw', recs.map(r => r.hardware));
  opts('f-model', recs.map(r => r.model));
  opts('f-quant', recs.map(r => r.quant));
  opts('f-be', recs.map(r => r.backend));
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const badge = p => '<span class="badge ' + ({sourced:'b-src',community:'b-com',estimated:'b-est'}[p]||'b-est') + '">' + ({sourced:'sourced',community:'community',estimated:'estimated'}[p]||p||'?') + '</span>';
  function render() {
    const f = {hw: sel('f-hw').value, model: sel('f-model').value,
               quant: sel('f-quant').value, be: sel('f-be').value};
    const showRef = sel('f-ref').checked;
    const showClu = sel('f-clu').checked;
    const pool = recs.concat(showRef ? refs : [], showClu ? clus : []);
    const rows = pool.filter(r =>
      (!f.hw || r.hardware === f.hw) && (!f.model || r.model === f.model) &&
      (!f.quant || r.quant === f.quant) && (!f.be || r.backend === f.be));
    rows.sort((a, b) => (a.model < b.model ? -1 : a.model > b.model ? 1 : (b.tps||0)-(a.tps||0)));
    sel('f-hw').value = f.hw; sel('f-model').value = f.model;
    sel('f-quant').value = f.quant; sel('f-be').value = f.be;
    document.getElementById('lcount').textContent =
      rows.length + ' of ' + recs.length + ' records' +
      (showRef ? ' (reference estimates included: ' + refs.length + ')' : '') +
      (showClu ? ' (cluster runs included: ' + clus.length + ')' : '');
    document.getElementById('ltable').innerHTML =
      '<table><tr><th>hardware</th><th>model</th><th>quant</th><th>backend</th>' +
      '<th>tok/s</th><th>W</th><th>ttft s</th><th>ctx/tg</th><th>date</th><th>class</th><th>flags</th><th>source</th></tr>' +
      rows.map(r => '<tr><td>' + esc(r.hardware) + '</td><td>' + esc(r.model) +
        ' <span class="dim">' + esc(r.params) + '</span></td><td>' + esc(r.quant) +
        '</td><td>' + esc(r.backend) + '</td><td class="num">' + esc(r.tps) +
        '</td><td class="num">' + esc(r.power_w ?? '') + '</td><td class="num">' + esc(r.ttft_s ?? '') + '</td><td>' + esc(r.ctx ?? (r.tg_tokens ? 'tg' + r.tg_tokens : '–')) +
        '</td><td>' + esc(r.date ?? '–') + '</td><td>' + badge(r.provenance) +
        (r.scope === 'cluster' ? ' <span class="badge b-est">cluster</span>' : '') +
        '</td><td>' + ((r.flags||[]).map(f => '<span class="badge b-flag">' + esc(f) + '</span>').join(' ') || '–') +
        '</td><td><a href="' + esc(r.source_url) + '" rel="nofollow">source</a></td></tr>'
      ).join('') + '</table>';
  }
  ['f-hw','f-model','f-quant','f-be'].forEach(id => sel(id).addEventListener('change', render));
  sel('f-ref').addEventListener('change', render);
  sel('f-clu').addEventListener('change', render);
  render();
});
</script>"""
    write("lookup.html", page("Lookup", lookup_body))

    print("done: %d records -> %d hardware pages, %d model pages, %d backend notes"
          % (len(records), len(hw), len(models), len(multi)))


if __name__ == "__main__":
    sys.exit(main())
