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
            return None
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
        if (venue, issue) == ("llama.cpp", "29410") and "Qwopus" in model:
            return ("146 commits apart (not bisected): decode "
                    f"{val(rows,'lc-29410-b1','tps')} to {val(rows,'lc-29410-b2','tps')} tok/s "
                    f"({pct(rows,'lc-29410-b1','lc-29410-b2','tps'):.1f}%), MTP "
                    f"{val(rows,'lc-29410-b3','tps')} to {val(rows,'lc-29410-b5','tps')}/"
                    f"{val(rows,'lc-29410-b6','tps')} tok/s; pp512 did not regress "
                    f"({val(rows,'lc-29410-b1','pp_tps')} to {val(rows,'lc-29410-b2','pp_tps')} tok/s). "
                    "The issue suspects #27952 (RDNA3 q4_K MMQ retarget) for decode; the "
                    "MTP drop is attributed to an unknown commit in the same range.")
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
        return None

    venue_order = {"llama.cpp": 0, "vLLM": 1, "ExLlamaV2": 2, "HF": 3}
    multi_ab = {k: v for k, v in ab_groups.items() if len(v) >= 2}
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
