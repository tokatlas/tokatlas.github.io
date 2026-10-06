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
    tps = f"{r['tps']}" if r.get("tps") is not None else "–"
    pp = f"{r['pp_tps']}" if r.get("pp_tps") is not None else "–"
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
            f"<td class=\"num\">{esc(tps)}</td>"
            f"<td class=\"num\">{esc(pp)}</td>"
            f"<td class=\"num\">{esc(pw)}</td>"
            f"<td class=\"num\">{esc(ttft)}</td>"
            f"<td>{esc(ctx)}</td><td>{esc(date)}</td>"
            f"<td>{prov_badge(r.get('provenance'))}</td>"
            f"<td>{flag_badges(r.get('flags'))}</td>"
            f"<td><a href=\"{esc(r['source_url'])}\" rel=\"nofollow\">source</a></td></tr>")


TABLE_HEAD = ("<tr><th>hardware</th><th>model</th><th>quant</th><th>backend</th>"
              "<th>tok/s</th><th>pp tok/s</th><th>W</th><th>ttft s</th><th>ctx/tg</th>"
              "<th>date</th><th>class</th><th>flags</th><th>source</th></tr>")


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

    def ab_note(venue, issue, hw, model, rows, backend=""):
        if (venue, issue) == ("llama.cpp", "?"):
            if hw == "RTX 5080 (PCIe Gen 4) + Ryzen 3900X" and model == "Qwen3.6-35B-A3B":
                return ("Three-tier expert cache (VRAM + pinned RAM + io_uring disk "
                        "reads) vs stock --n-cpu-moe at matched VRAM, RTX 5080 + "
                        "Ryzen 3900X, 32 GB DDR4, slow SATA SSD. Qwen3.6-35B-A3B "
                        "UD-Q4_K_M at 256k ctx: "
                        f"{val(rows,'lc-lid-qwen36-ncmoe','tps')} tok/s stock vs "
                        f"{val(rows,'lc-lid-qwen36-cache','tps')} tok/s with the cache "
                        f"({pct(rows,'lc-lid-qwen36-ncmoe','lc-lid-qwen36-cache','tps'):+.0f}%, "
                        "published as approximate numbers). Unlike mfethe1's "
                        "matched-budget test on an RTX 5060 Ti, here the cache beats "
                        "residency: the fork keeps hot experts in pinned RAM instead of "
                        "re-reading them from the host over PCIe per miss, and the "
                        "LFU-with-aging policy keeps the VRAM tier's hit rate high "
                        "enough that the bookkeeping stays amortized. Shrinking the "
                        "budget to 16 GB RAM + 12 GB VRAM keeps the advantage: "
                        f"{val(rows,'lc-lid-qwen36-ncmoe-12gb','tps')} tok/s stock "
                        f"(--n-cpu-moe 30) vs {val(rows,'lc-lid-qwen36-cache-12gb','tps')} "
                        "tok/s with the cache at 70 VRAM + 186 pinned-RAM experts "
                        "(+65% published): the cache degrades gracefully as the VRAM "
                        "tier shrinks from 120 to 70 experts.")
            if hw == "RTX 5080 (PCIe Gen 4) + Ryzen 3900X" and model == "Qwen3-Coder-Next":
                return ("Same three-tier expert cache and machine as the Qwen3.6 "
                        "comparison: Qwen3-Coder-Next UD-IQ4_XS at 256k ctx, "
                        f"{val(rows,'lc-lid-codernext-ncmoe','tps')} tok/s with stock "
                        f"--n-cpu-moe 37 vs {val(rows,'lc-lid-codernext-cache','tps')} "
                        f"tok/s with the cache at 110 VRAM + 402 pinned-RAM experts "
                        f"({pct(rows,'lc-lid-codernext-ncmoe','lc-lid-codernext-cache','tps'):+.0f}%, "
                        "published as approximate numbers). The model needs 28.7 GB of "
                        "pinned RAM to reach that rate on a 16 GB card, and the author "
                        "notes disk reads on cache misses are the bottleneck on his "
                        "SATA SSD. At the 12 GB VRAM target the disk tier switches on "
                        "(55/402/55 experts VRAM/RAM/disk): "
                        f"{val(rows,'lc-lid-codernext-ncmoe-12gb','tps')} tok/s stock "
                        f"(--n-cpu-moe 41) vs {val(rows,'lc-lid-codernext-cache-12gb','tps')} "
                        "tok/s with the cache (+58% published) - the relative win "
                        "survives, but the absolute rate halves versus the 16 GB arm.")
        if (venue, issue) == ("llama.cpp", "29429"):
            if hw == "2x RTX 3090" and model == "GLM-5.3-Flash":
                return ("neurall/llama.cpp fork (VRAM-filling MoE expert cache, builds on "
                        "csantiago78 PR #27861) vs stock llama.cpp. GLM-5.3-Flash 3.0-bit "
                        "(106 GB) on 2x RTX 3090 (3700X, 125 GB DDR4), short chat, single "
                        "stream, temp 0, model in RAM. decode "
                        f"{val(rows,'lc-29429-2x3090-glm53-3.0bit-stock','tps')} -> "
                        f"{val(rows,'lc-29429-2x3090-glm53-3.0bit-fork','tps')} tok/s "
                        f"({pct(rows,'lc-29429-2x3090-glm53-3.0bit-stock','lc-29429-2x3090-glm53-3.0bit-fork','tps'):+.0f}%). "
                        "The model is ~2.2x the 48 GB VRAM, so stock leaves most expert work "
                        "on the CPU; the fork's live expert cache plus parallel CPU misses "
                        "recovers it.")
            if hw == "2x RTX 3090" and model == "MiMo-V2.6-Flash":
                return ("neurall/llama.cpp fork (MoE expert cache) vs stock. MiMo-V2.6-Flash "
                        "IQ3_XXS (132 GB, bigger than the 125 GB RAM) on 2x RTX 3090 (3700X), "
                        "short chat, single stream, temp 0. decode "
                        f"{val(rows,'lc-29429-2x3090-mimo26-iq3xxs-stock','tps')} -> "
                        f"{val(rows,'lc-29429-2x3090-mimo26-iq3xxs-fork','tps')} tok/s "
                        f"({pct(rows,'lc-29429-2x3090-mimo26-iq3xxs-stock','lc-29429-2x3090-mimo26-iq3xxs-fork','tps'):+.0f}%), "
                        "the largest gain in the table: the model is bigger than RAM, so "
                        "stock streams experts over the PCIe link and the fork's cache "
                        "turns the idle second GPU into live compute.")
            if hw == "2x RTX 3090" and model == "Qwen3.8-Flash-Next":
                return ("neurall/llama.cpp fork (MoE expert cache) vs stock. Qwen3.8-Flash-Next "
                        "UD-IQ4_XS (88 GB) on 2x RTX 3090 (3700X, 125 GB DDR4), short chat, "
                        "single stream, temp 0. decode "
                        f"{val(rows,'lc-29429-2x3090-qwen38next-udiq4xs-stock','tps')} -> "
                        f"{val(rows,'lc-29429-2x3090-qwen38next-udiq4xs-fork','tps')} tok/s "
                        f"({pct(rows,'lc-29429-2x3090-qwen38next-udiq4xs-stock','lc-29429-2x3090-qwen38next-udiq4xs-fork','tps'):+.0f}%).")
            if hw == "4x RTX 3090" and model == "GLM-5.3-Flash":
                return ("neurall/llama.cpp fork (MoE expert cache) vs stock, on a rented 4x "
                        "RTX 3090 box (EPYC 7B12, 256 GB DDR4; raw logs not kept). "
                        "GLM-5.3-Flash 3.0-bit (117.5 GB). 4 GPUs, warm run: decode "
                        f"{val(rows,'lc-29429-4x3090-glm53-4gpu-stock','tps')} -> "
                        f"{val(rows,'lc-29429-4x3090-glm53-4gpu-fork','tps')} tok/s "
                        f"({pct(rows,'lc-29429-4x3090-glm53-4gpu-stock','lc-29429-4x3090-glm53-4gpu-fork','tps'):+.0f}%); "
                        "3 of the 4 GPUs (best ratio): "
                        f"{val(rows,'lc-29429-4x3090-glm53-3of4-stock','tps')} -> "
                        f"{val(rows,'lc-29429-4x3090-glm53-3of4-fork','tps')} tok/s "
                        f"({pct(rows,'lc-29429-4x3090-glm53-3of4-stock','lc-29429-4x3090-glm53-3of4-fork','tps'):+.0f}%). "
                        "The 85%-in-VRAM 4-GPU box gains little on the first run; the "
                        "3-GPU (66% VRAM) placement is the best ratio.")
            return None
        if (venue, issue) == ("llama.cpp", "29935"):
            if hw == "2x RTX 3080 20GB" and model == "qwen3.5-arch 27B":
                return ("llama.cpp perf issue #29935 (CUDA fattn KV streaming on sm86, "
                        "context-decay report). qwen3.5-arch 27B NVFP4 on 2x RTX 3080 20GB, "
                        "-fa on (tensor split), MTP3 spec (verify batch 4), local build 836d571 "
                        "(b11379 + 2 commits, fattn identical), single request. Decode decays "
                        "with context; q8_0 KV decays faster than f16 KV because the VEC path is "
                        "gated to batch==1, so at the MTP3 verify batch 4 quantized KV takes the "
                        "MMA path plus a whole-cache f16 conversion. f16 KV "
                        f"{val(rows,'lc-29935-2x3080-qwen35arch27b-f16-30k','tps')} -> "
                        f"{val(rows,'lc-29935-2x3080-qwen35arch27b-f16-90k','tps')} tok/s "
                        f"({pct(rows,'lc-29935-2x3080-qwen35arch27b-f16-30k','lc-29935-2x3080-qwen35arch27b-f16-90k','tps'):+.0f}% from 30K to 90K); "
                        "q8_0 KV "
                        f"{val(rows,'lc-29935-2x3080-qwen35arch27b-q8-30k','tps')} -> "
                        f"{val(rows,'lc-29935-2x3080-qwen35arch27b-q8-90k','tps')} tok/s "
                        f"({pct(rows,'lc-29935-2x3080-qwen35arch27b-q8-30k','lc-29935-2x3080-qwen35arch27b-q8-90k','tps'):+.0f}%). "
                        "Step-time slopes ~0.075 (f16) vs ~0.081 ms/1K tok (q8_0); official "
                        "b11379 f16 48.2 @30K for reference.")
            return None
        if (venue, issue) == ("llama.cpp", "29936"):
            if hw == "B70 Arc Pro" and model == "gemma4 26B.A4B":
                return ("llama.cpp PR #29936 (Vulkan Intel prefill regression fix; a "
                        "git-bisect shows #29182 halved Intel MoE prefill by steering the "
                        "tile selector away from the tuned l_warptile config). B70 Arc Pro "
                        "(Windows), gemma4 26B.A4B Q4_K_M, pp8192 prefill. Without flash "
                        "attn (fa 0): b11017 "
                        f"{val(rows,'lc-29936-b70arc-b11017-fa0','pp_tps')} -> b11352 "
                        f"{val(rows,'lc-29936-b70arc-b11352-fa0','pp_tps')} t/s "
                        f"({pct(rows,'lc-29936-b70arc-b11017-fa0','lc-29936-b70arc-b11352-fa0','pp_tps'):+.0f}%); "
                        "with flash attn (fa 1): "
                        f"{val(rows,'lc-29936-b70arc-b11017-fa1','pp_tps')} -> "
                        f"{val(rows,'lc-29936-b70arc-b11352-fa1','pp_tps')} t/s "
                        f"({pct(rows,'lc-29936-b70arc-b11017-fa1','lc-29936-b70arc-b11352-fa1','pp_tps'):+.0f}%).")
            return None
        if (venue, issue) == ("llama.cpp", "29949"):
            if hw == "7900 XTX" and model == "Qwen3.8-Flash-Next":
                return ("llama.cpp issue #29949 (MoE expert cache with GPU-resident LRU; "
                        "feature request with working impl, commit 9d7cf288a). 7900 XTX 24GB, "
                        "Qwen3.8-Flash-Next. UD-IQ3_XXS, 48 layers pooled: no pool "
                        f"{val(rows,'lc-29949-7900xtx-iq3xxs-nopool','tps')} -> 160 slots "
                        f"{val(rows,'lc-29949-7900xtx-iq3xxs-160s','tps')} tok/s "
                        f"({pct(rows,'lc-29949-7900xtx-iq3xxs-nopool','lc-29949-7900xtx-iq3xxs-160s','tps'):+.0f}%); "
                        "MTP-Q8 on top: "
                        f"{val(rows,'lc-29949-7900xtx-iq3xxs-nopool-mtp','tps')} (no pool) and "
                        f"{val(rows,'lc-29949-7900xtx-iq3xxs-160s-mtp','tps')} (160 slots) tok/s. "
                        "UD-IQ4_XS reverse placement (8 native + 40 pooled): 72 slots "
                        f"{val(rows,'lc-29949-7900xtx-iq4xs-72s','tps')} tok/s (77.9% hit); "
                        "40 slots "
                        f"{val(rows,'lc-29949-7900xtx-iq4xs-40s','tps')} tok/s; "
                        "40 slots + MTP-Q4 "
                        f"{val(rows,'lc-29949-7900xtx-iq4xs-40s-mtp','tps')} tok/s.")
            if hw == "2x RTX 3090" and model == "Qwen3.8-Flash-Next":
                return ("llama.cpp issue #29949 (MoE expert cache with GPU-resident LRU). "
                        "2x RTX 3090 48GB, Qwen3.8-Flash-Next, UD-IQ4_XS, 48 layers pooled, "
                        "320 slots (34.7 GiB pool). EN plain "
                        f"{val(rows,'lc-29949-2x3090-iq4xs-plain','tps')} -> EN + MTP-Q8 "
                        f"{val(rows,'lc-29949-2x3090-iq4xs-mtp','tps')} tok/s "
                        f"({pct(rows,'lc-29949-2x3090-iq4xs-plain','lc-29949-2x3090-iq4xs-mtp','tps'):+.0f}%); "
                        "93.6% hit rate plain, 96.0% with MTP.")
            return None
        if (venue, issue) == ("llama.cpp", "30021"):
            if model == "Granite 3.0 3B":
                return ("Full GCN MMQ config re-tune (llama.cpp #30021) on an "
                        "A800M, Granite 3.0 3B pp2048 prefill, master vs PR by "
                        "ub: Q8_0 ub16 "
                        f"{val(rows,'lc30021-a800m-q8_0-ub16-master','pp_tps')} -> "
                        f"{val(rows,'lc30021-a800m-q8_0-ub16-pr','pp_tps')} tok/s "
                        f"({pct(rows,'lc30021-a800m-q8_0-ub16-master','lc30021-a800m-q8_0-ub16-pr','pp_tps'):+.0f}%); "
                        "IQ4_XS ub16 "
                        f"{val(rows,'lc30021-a800m-iq4_xs-ub16-master','pp_tps')} -> "
                        f"{val(rows,'lc30021-a800m-iq4_xs-ub16-pr','pp_tps')} "
                        f"({pct(rows,'lc30021-a800m-iq4_xs-ub16-master','lc30021-a800m-iq4_xs-ub16-pr','pp_tps'):+.0f}%) "
                        f"and ub48 {val(rows,'lc30021-a800m-iq4_xs-ub48-master','pp_tps')} -> "
                        f"{val(rows,'lc30021-a800m-iq4_xs-ub48-pr','pp_tps')} tok/s "
                        f"({pct(rows,'lc30021-a800m-iq4_xs-ub48-master','lc30021-a800m-iq4_xs-ub48-pr','pp_tps'):+.0f}%). "
                        "Every other ub point is within +-1%: the retune "
                        "targets the small-ub regime where the old configs "
                        "picked the wrong J.")
            if model == "Meta Llama 3 8B":
                return ("Same GCN MMQ re-tune (llama.cpp #30021), IQ4_NL "
                        "Meta Llama 3 8B pp2048 prefill by ub: ub16 "
                        f"{val(rows,'lc30021-a800m-iq4_nl-ub16-master','pp_tps')} -> "
                        f"{val(rows,'lc30021-a800m-iq4_nl-ub16-pr','pp_tps')} tok/s "
                        f"({pct(rows,'lc30021-a800m-iq4_nl-ub16-master','lc30021-a800m-iq4_nl-ub16-pr','pp_tps'):+.0f}%) "
                        f"and ub48 {val(rows,'lc30021-a800m-iq4_nl-ub48-master','pp_tps')} -> "
                        f"{val(rows,'lc30021-a800m-iq4_nl-ub48-pr','pp_tps')} tok/s "
                        f"({pct(rows,'lc30021-a800m-iq4_nl-ub48-master','lc30021-a800m-iq4_nl-ub48-pr','pp_tps'):+.0f}%); "
                        "flat within +-0.2% at every other ub.")
            return None
        if (venue, issue) == ("llama.cpp", "28894") and model == "Qwen3.8-27B":
            return ("KVMem keeps a 256K conversation mostly in system RAM and "
                    "loads only a 32-36K window per question on an RTX 5060 Ti "
                    "16GB (WSL2): first-pass prefill "
                    f"{val(rows,'lc-disc-28894-qwen3827b-iq3','pp_tps')} tok/s "
                    f"(IQ3_S) / {val(rows,'lc-disc-28894-qwen3827b-iq4','pp_tps')} "
                    f"(IQ4_XS), decode across 33 tool requests "
                    f"{val(rows,'lc-disc-28894-qwen3827b-iq3','tps')} / "
                    f"{val(rows,'lc-disc-28894-qwen3827b-iq4','tps')} tok/s at "
                    "262058/262144 tokens, peak VRAM 15.5-15.6 GB. Accuracy at a "
                    "32K GPU window is within noise of full 256K history (85.6 vs "
                    "86.6% LongMemEval-S).")
        if (venue, issue) == ("llama.cpp", "28512") and model == "Qwen3.8-Flash-Next":
            return ("Stack-level tuning of Flash-Next serving on a Bosgame M5 "
                    "(Strix Halo, 128 GB, Vulkan/RADV), replaying ten real agent "
                    "conversations: row-id hoisting for 512-expert models (+19% "
                    "prefill, #28501), always drafting 3 tokens (p-min 0, +13% "
                    "decode) and a trimmed-vocab FR-Spec draft head. File rewrite "
                    "@8k decode "
                    f"{val(rows,'lc-disc-28512-flashnext-filerewrite8k-before','tps')} -> "
                    f"{val(rows,'lc-disc-28512-flashnext-filerewrite8k-now','tps')} "
                    f"tok/s (63.2 at n-max 6), new code @8k "
                    f"{val(rows,'lc-disc-28512-flashnext-newcode8k-before','tps')} -> "
                    f"{val(rows,'lc-disc-28512-flashnext-newcode8k-now','tps')}; "
                    "prefill 340 -> 510 tok/s at 8k. Median over the replays: 25 -> "
                    "33 tok/s, TTFT on a fresh 18k prompt 67 -> 44 s.")
        if (venue, issue) == ("llama.cpp", "28514") and model == "Qwen3.8-27B":
            return ("NVFP4 prefill headroom on an RTX 5090 (sm_120a), pp16384: "
                    f"stock {val(rows,'lc-disc-28514-5090-nvfp4-stock','pp_tps')} -> "
                    f"{val(rows,'lc-disc-28514-5090-nvfp4-poc','pp_tps')} tok/s "
                    "(+44.7%) with chunked gated-delta-net prefill, GEMM fusions "
                    "and TMA-fed NVFP4 MMQ; hand-written W4A4 NInfer sits at 8,466. "
                    "draft-mtp costs 23% prefill on the patched build (8,499 -> "
                    "6,518 engine-reported) vs -9% on NInfer; keeping the MTP "
                    "hand-off on device recovers 7,065 -> 7,550 under the profiler.")
        if (venue, issue) == ("llama.cpp", "28363") and model == "Qwen3.8-Flash-Next":
            return ("Fixed GPU expert pool (CUDA-resident packed experts, misses "
                    "executed on CPU) at 16K context on an RTX 4080 Super 16 GiB: "
                    f"control {val(rows,'lc-disc-28363-flashnext-control','tps')} -> "
                    f"{val(rows,'lc-disc-28363-flashnext-pool4g','tps')} -> "
                    f"{val(rows,'lc-disc-28363-flashnext-pool6g','tps')} -> "
                    f"{val(rows,'lc-disc-28363-flashnext-pool8g','tps')} tok/s for "
                    "0/4/6/8 GiB pools (+23.9% at 8 GiB). CUDA Graphs are essential: "
                    f"graphs off drops the 8 GiB config to "
                    f"{val(rows,'lc-disc-28363-flashnext-pool8g-nograph','tps')} "
                    "tok/s. The gain shrinks to about +4.6% at 262K, where KV "
                    "dominates: 5.776 tok/s at q8-q4 KV + 4 GiB pool vs 5.649 at "
                    "q4-q4 + 6 GiB; crossing physical VRAM collapses the run to "
                    "0.71 tok/s via Windows shared-memory paging.")
        if (venue, issue) == ("llama.cpp", "28767") and model == "Qwen3.8-Flash-Next":
            return ("Same 4-GPU rig (5070 + 2x5060 + 4060, PCIe x8/x4/x1/x1, "
                    "DDR4-3200) on Windows vs Ubuntu: Q3_XXS full offload prefill "
                    f"{val(rows,'lc-disc-28767-flashnext-q3xxs-win','pp_tps')} -> "
                    f"{val(rows,'lc-disc-28767-flashnext-q3xxs-linux','pp_tps')} "
                    "tok/s and Q4_XS partial offload decode 10 -> "
                    f"{val(rows,'lc-disc-28767-flashnext-q4xs-linux','tps')} tok/s "
                    "moving to Linux; the author's WDDM multi-GPU finding (4th GPU "
                    "halves decode on Windows, unchanged on Ubuntu/WSL2) was "
                    "reproduced on a separate 27B Q6 model, not named, so those "
                    "rows are not recorded.")
        if (venue, issue) == ("llama.cpp", "29037"):
            pair = {"Qwen3-4B-Instruct": ("qwen34bi", "30"),
                    "SmolLM2-135M": ("smolm135", "240"),
                    "Midm-2.0-Mini": ("midm2mini", "40")}.get(model)
            if pair:
                slug, tgt = pair
                return ("FiTuna auto-tuner on an Apple M3 Pro: pick the lightest "
                        "quant (and minimum -ngl) that hits the "
                        f"{tgt} tok/s target within a 5% perplexity-loss budget. "
                        f"The Q8_0 default measured "
                        f"{val(rows,f'lc-disc-29037-{slug}-q80','tps')} tok/s and "
                        "failed; the passing config reached "
                        f"{val(rows,f'lc-disc-29037-{slug}-pass','tps')} tok/s. "
                        "Author notes run-to-run noise of about +-1.7 tok/s at a "
                        "30 tok/s baseline, so near-miss verdicts are marginal.")
            return None
        if (venue, issue) == ("llama.cpp", "29387") and model == "Ternary-Bonsai-2-27B":
            return ("DFlash2 speculative decoding (from #27816, cherry-picked onto "
                    "PrismML's fork) on one L4, greedy, drafter Q4_K_M: decode goes "
                    f"{val(rows,'lc-disc-29387-bonsai-gsm8k-plain','tps')} -> "
                    f"{val(rows,'lc-disc-29387-bonsai-gsm8k-dflash','tps')} tok/s on "
                    "GSM8K, 31.6 -> 68.4 on MBPP, 30.6 -> 67.8 on MATH-500 (2.15-2.22x) "
                    f"and {val(rows,'lc-disc-29387-bonsai-mtbench-plain','tps')} -> "
                    f"{val(rows,'lc-disc-29387-bonsai-mtbench-dflash','tps')} on "
                    "MT-Bench turn 1 (1.37x). ngram-mod on the same sets was "
                    "0.92-0.95x; draft-n-max 7 suits code/math, 3 suits open-ended "
                    "text. Accuracy moved by at most one problem per set.")
        if (venue, issue) == ("llama.cpp", "29253"):
            if model == "Qwen3 4B":
                return ("Per-UID RPC graph caching over 2.5G Ethernet between two "
                        "GMKtec K12 boxes (Ryzen H255): tg32 "
                        f"{val(rows,'lc-disc-29253-qwen34b-upstream','tps')} -> "
                        f"{val(rows,'lc-disc-29253-qwen34b-graphcache','tps')} tok/s "
                        f"(solo K12-1 baseline "
                        f"{val(rows,'lc-disc-29253-qwen34b-solo','tps')} tok/s), pp64 "
                        f"{val(rows,'lc-disc-29253-qwen34b-upstream','pp_tps')} -> "
                        f"{val(rows,'lc-disc-29253-qwen34b-graphcache','pp_tps')} "
                        "tok/s. Gemma-4-31B sees the bigger relative win: tg32 "
                        "1.64 -> 4.11 tok/s, close to its 4.49 tok/s solo rate.")
            if model == "Gemma-4-31B":
                return ("Per-UID RPC graph caching over 2.5G Ethernet between two "
                        "GMKtec K12 boxes (Ryzen H255), Gemma 4 31B Q4_0 (241 graphs "
                        "reused): tg32 "
                        f"{val(rows,'lc-disc-29253-gemma431b-upstream','tps')} -> "
                        f"{val(rows,'lc-disc-29253-gemma431b-graphcache','tps')} tok/s, "
                        f"vs {val(rows,'lc-disc-29253-gemma431b-solo','tps')} tok/s "
                        f"solo; pp64 {val(rows,'lc-disc-29253-gemma431b-upstream','pp_tps')} "
                        f"-> {val(rows,'lc-disc-29253-gemma431b-graphcache','pp_tps')} tok/s.")
            return None
        if (venue, issue) == ("llama.cpp", "29249") and model == "Qwen3-4B-Instruct-2507":
            return ("Sarge harness (in-process Rust rule checker linked into "
                    "llama-server) writing code with Qwen3-4B-Instruct-2507 Q4_K_M: "
                    f"{val(rows,'lc-disc-29249-4070lp-gpu','tps')} tok/s on the 4070 "
                    f"laptop card vs {val(rows,'lc-disc-29249-4070lp-cpu','tps')} "
                    "tok/s on 4 CPU cores at -ngl 0. A rule check on a 2,250-token "
                    "file costs about 70 s on CPU or a few seconds on the card.")
        if (venue, issue) == ("llama.cpp", "29072") and model == "Gemma 4 26B-A4B":
            return ("Conservative narrow-MoE MMVQ selector patch for RDNA3 UMA iGPUs "
                    "(gfx1103) on Vulkan, Gemma 4 26B-A4B QAT-Q4_0 on a 780M: tg "
                    f"{val(rows,'lc-disc-29072-780m-gemma26a4b-before','tps')} -> "
                    f"{val(rows,'lc-disc-29072-780m-gemma26a4b-after','tps')} t/s "
                    "(+12.2% published, single same-prompt speed test; a maintainer "
                    "asked for repeated runs and a selector-only ablation).")
        if (venue, issue) == ("llama.cpp", "30033"):
            if model == "Qwen3.8-Flash-Next":
                return ("Regression bisect on 2x Intel B70 (VM, 32 Ryzen 9 5950X "
                        "threads), UD-IQ3_XXS, -c 196608, llama-server via "
                        "llama-swap with -fa on -sm layer -ctxcp 3: tg "
                        f"{val(rows,'lc30033-b70x2-29612','tps')} -> "
                        f"{val(rows,'lc30033-b70x2-29622','tps')} tok/s and pp "
                        f"{val(rows,'lc30033-b70x2-29612','pp_tps')} -> "
                        f"{val(rows,'lc30033-b70x2-29622','pp_tps')} tok/s from PR "
                        "#29612 to #29622 (first bad commit 0bb496d, b11400); "
                        "the reporter observes the same regression through "
                        "#29971.")
            return None
        if (venue, issue) == ("llama.cpp", "29621"):
            if model == "Ternary-Bonsai-2-27B":
                return ("xyz-llama fork on RTX 4070 Ti SUPER 16 GB, PTQ1_0 "
                        "weights, ~161k context, lossless block-verified draft: "
                        "the stock build with the xyzkv2 2-bit rotated KV cache "
                        f"decodes {val(rows,'lc29621-4070tis-xyzkv2','tps')} tok/s "
                        "(2.82 tokens per round) and the optional CUDA speculative "
                        "runtime (XYZ_ENGINE=1) reaches "
                        f"{val(rows,'lc29621-4070tis-xyzengine','tps')} tok/s. "
                        "Later build on the same card (2.94 tokens per round): "
                        f"xyzkv2 {val(rows,'lc29621-4070tis-xyzkv2-r2','tps')} tok/s "
                        "at 7.5 GiB KV versus "
                        f"{val(rows,'lc29621-4070tis-q40-r2','tps')} tok/s at 9.0 GiB "
                        "with q4_0 KV - about 11% faster and 1.5 GiB smaller, "
                        "the gap is all cache reads.")
            return None
        if (venue, issue) == ("llama.cpp", "28766"):
            if model == "DeepSeek-V4.1-Flash":
                return ("DSV4.1 port (b10269) on one RTX 5090, 31.8 GiB VRAM + "
                        "125.7 GiB RAM, MXFP4 experts, 189 GiB of engram tables "
                        "on disk: new-content decode is disk-bound at "
                        f"{val(rows,'lc28766-5090-dsv41-new','tps')} tok/s (20% "
                        "compute / 26% PCIe / 54% NVMe per remap), "
                        f"{val(rows,'lc28766-5090-dsv41-cached','tps')} tok/s with "
                        "the expert cache resident (105 GiB working set). "
                        "Measured ceilings: "
                        f"{val(rows,'lc28766-5090-dsv41-ceil-nomiss','tps')} tok/s "
                        "with zero disk misses (oracle routing) and "
                        f"{val(rows,'lc28766-5090-dsv41-ceil-resident','tps')} tok/s "
                        "if everything were resident.")
            return None
        if (venue, issue) == ("llama.cpp", "29643"):
            if model == "Bonsai 2 27B":
                return ("Xe2 XMX kernels for ternary weights and q4_0 KV-cache "
                        "attention on Arc B580, 128K context: the branch reaches "
                        f"{val(rows,'lc-disc-29643-bonsai-branch','tps')} tok/s plain "
                        f"generation and {val(rows,'lc-disc-29643-bonsai-branch','pp_tps')} tok/s "
                        "prompt reading vs "
                        f"{val(rows,'lc-disc-29643-bonsai-fork','tps')} / "
                        f"{val(rows,'lc-disc-29643-bonsai-fork','pp_tps')} tok/s on "
                        "PrismML's fork SYCL support on the same card and flags. At "
                        "32K context the gap widens: "
                        f"{val(rows,'lc-disc-29643-bonsai-branch32k','tps')} vs "
                        f"{val(rows,'lc-disc-29643-bonsai-fork32k','tps')} tok/s. "
                        "MTP drafting lifts generation to 90 tok/s writing new code "
                        "and 250-370 tok/s on code edits; a 115K-token history costs "
                        f"almost nothing ({val(rows,'lc-disc-29643-bonsai-hist115k','tps')} tok/s with "
                        f"MTP, {val(rows,'lc-disc-29643-bonsai-plain115k','tps')} tok/s plain "
                        "decode on the same prompt).")
            if model == "Gemma 4 12B":
                return ("The same XMX q4_0 KV attention plus a q4_0 small-batch GEMM "
                        "generalise to Gemma 4 12B QAT with Google's assistant "
                        "drafter on Arc B580: "
                        f"{val(rows,'lc-disc-29643-gemma412b-old','tps')} -> "
                        f"{val(rows,'lc-disc-29643-gemma412b-new','tps')} tok/s "
                        "(published as about 40 to 100 t/s).")
            return None
        if (venue, issue) == ("llama.cpp", "29861"):
            if model == "Bonsai":
                return ("Cross-backend tensor+mode-split (GPU + ANE via IOSurface "
                        "buffer sharing) on a Mac Mini M4 16GB, bonsai-llama.cpp "
                        "fork, PQ2_0: prompt processing "
                        f"{val(rows,'lc-disc-29861-macmini-bonsai-before','pp_tps')} -> "
                        f"{val(rows,'lc-disc-29861-macmini-bonsai-after','pp_tps')} tok/s "
                        "with decode unchanged (mode-split keeps decode on the GPU).")
            if model == "Qwen3.8-Flash-Next":
                return ("Same cross-backend idea on a Ryzen 8845HS (Radeon iGPU + "
                        "XDNA NPU), Qwen3.8-Flash-Next UD-IQ1_S: prompt processing "
                        f"{val(rows,'lc-disc-29861-8845hs-qwen38-before','pp_tps')} -> "
                        f"{val(rows,'lc-disc-29861-8845hs-qwen38-after','pp_tps')} tok/s "
                        "with GPU/NPU tensor+mode-split, decode unchanged. A related "
                        "ROCm/Vulkan tensor-split PoC on the same chip recovered 80% "
                        "of the ROCm-over-Vulkan prefill advantage while keeping "
                        "Vulkan decode speed (relative figure only, not recorded).")
            return None
        if (venue, issue) == ("llama.cpp", "29531"):
            if model == "Qwen3.8-27B":
                return ("Declarative Attention (focus-llama): keeps the full 230K "
                        "context but attends only a 3-40K hot window, offloading the "
                        "rest of the KV cache and refilling on demand. Identical 1 "
                        "hour coding session on an RTX 5090, Q6_K: "
                        f"{val(rows,'lc-disc-29531-5090-qwen3827b-vanilla','tps')} -> "
                        f"{val(rows,'lc-disc-29531-5090-qwen3827b-focus','tps')} t/s "
                        "(+35% published). The sparse gather kernel supports f16 and "
                        "q4_0 KV caches; other KV quants fall back to the dense path.")
            return None
        if (venue, issue) == ("llama.cpp", "29964"):
            if model == "Qwen3.8":
                return ("Pipeline-parallelism patch for MoE weights in host RAM on "
                        "3x RTX PRO 4000 Blackwell (EPYC 9274F, 384 GB DDR5). Stock "
                        "master disables pipeline parallelism whenever any weights "
                        "sit in host RAM, serializing all expert uploads through "
                        "GPU0; the patch routes ops with host weights to each "
                        "layer's own GPU. 52421-token prompt, fit, c=262144: "
                        f"{val(rows,'lc-disc-29964-qwen38-master','pp_tps')} -> "
                        f"{val(rows,'lc-disc-29964-qwen38-patched','pp_tps')} tok/s "
                        "(1st request, 961 -> 1982 on the 2nd), decode 40.8 -> 41.6 "
                        "tok/s. With only 2 GPUs the gain is smaller (pp16384 "
                        f"{val(rows,'lc-disc-29964-qwen38-2gpu-master','pp_tps')} -> "
                        f"{val(rows,'lc-disc-29964-qwen38-2gpu-patched','pp_tps')}) "
                        "since there is less upload traffic to spread. The patch "
                        "depends on CUDA_SCALE_LAUNCH_QUEUES=4x: at pp8192 the same "
                        "patch drops to "
                        f"{val(rows,'lc-disc-29964-qwen38-qnone','pp_tps')} tok/s "
                        f"without it (vs {val(rows,'lc-disc-29964-qwen38-q4x','pp_tps')} "
                        "with 4x queues).")
            if model == "DeepSeek-V4-Flash":
                return ("Same pipeline-parallel patch, fit layout, 52421-token "
                        "prompt: "
                        f"{val(rows,'lc-disc-29964-dsv4f-master','pp_tps')} -> "
                        f"{val(rows,'lc-disc-29964-dsv4f-patched','pp_tps')} tok/s "
                        "prefill (1st request, 629 -> 1321 on the 2nd), decode "
                        "23.0 -> 23.1 tok/s. The patch's balanced fit layout also "
                        "slices layers evenly across GPUs instead of piling all "
                        "host weights on the last device.")
            if model == "MiMo-V2.6-Flash":
                return ("Same pipeline-parallel patch, fit, c=131072, 51341-token "
                        "prompt: "
                        f"{val(rows,'lc-disc-29964-mimo-master','pp_tps')} -> "
                        f"{val(rows,'lc-disc-29964-mimo-patched','pp_tps')} tok/s "
                        "prefill (1st request, 886 -> 1834 on the 2nd), decode "
                        "33.6 -> 33.3 tok/s. The author notes llama-bench pp2048 "
                        "shows -20% for this model as an artifact (per-test "
                        "contexts trigger the upload-all-experts path); on the "
                        "server it is at parity.")
            if model == "Qwen3.5 35B":
                return ("Topology regression bisect, model fully in VRAM, 52421-token "
                        "prompt, c=65536: #29184 broke the constant-graph assumption "
                        "for models with shared experts on CUDA, halving prefill "
                        f"from 7131 (parent 4ebdf2c74) to {val(rows,'lc-disc-29964-qwen3535b-master','pp_tps')} "
                        f"tok/s on master; the patch restores "
                        f"{val(rows,'lc-disc-29964-qwen3535b-patched','pp_tps')} tok/s. "
                        "Models without shared experts (gpt-oss) are unaffected.")
            if model == "Qwen3.5-35B-A3B":
                return ("All experts in host RAM (-ncmoe 999, no fit): the patch "
                        "overlaps expert uploads with compute across the three GPUs. "
                        f"pp8192: {val(rows,'lc-disc-29964-qwen3535ba3b-pp8192-master','pp_tps')} -> "
                        f"{val(rows,'lc-disc-29964-qwen3535ba3b-pp8192-patched','pp_tps')} tok/s; "
                        f"pp32768: {val(rows,'lc-disc-29964-qwen3535ba3b-pp32768-master','pp_tps')} -> "
                        f"{val(rows,'lc-disc-29964-qwen3535ba3b-pp32768-patched','pp_tps')} tok/s. "
                        "The author measured PCIe at 57.6 GB/s on one GPU and "
                        "106.8 GB/s (1.85x) with all three uploading at once; the "
                        "patch does not make uploads faster, it spreads them over "
                        "three links. Gain peaks at ubatch 2048 (+66%).")
            if model == "Gemma 4 26B-A4B":
                return ("Two-GPU -ncmoe 999 1:1 layer split on a 4500 + 3060 rig, "
                        "prompt processing: master runs it all on the 4500 at "
                        f"{val(rows,'lc-disc-29964-gemma426b-master','pp_tps')} tok/s "
                        "(3060 mostly idle), while PR #29963's pipeline parallelism "
                        f"halves it to {val(rows,'lc-disc-29964-gemma426b-pr29963','pp_tps')} "
                        "tok/s (3060 at ~3GiB/s RX). Hard-disabling pipeline_parallel "
                        "on the PR branch recovers full performance, so the penalty "
                        "is the pipeline itself; 4:1, 6:1 and 10:1 splits beat 1:1 "
                        "but stay ~14% below the 4500-alone run.")
            return None
        if (venue, issue) == ("llama.cpp", "29885"):
            if model == "Qwen3.6-35B-A3B":
                return ("MoE offload lesson on a GTX 1080 8GB (40K-token agentic "
                        "prompt, 92k ctx): keeping experts on GPU while the KV cache "
                        "follows the layers gives "
                        f"{val(rows,'lc-disc-29885-gtx1080-qwen36-pp-gpu','pp_tps')} tok/s "
                        "prefill (cold TTFT ~155s); pushing 20 MoE layers to CPU "
                        f"collapses prefill to {val(rows,'lc-disc-29885-gtx1080-qwen36-pp-cpu20','pp_tps')} "
                        "tok/s, an ~8.8x drop that no KV-cache persistence can fix. "
                        "The disk-restored KV prefix checkpoint itself reads back in "
                        "2.1s, cutting post-restart TTFT from ~155s to ~6s.")
            return None
        if (venue, issue) == ("llama.cpp", "30018"):
            if model == "Gemma 4 E4B":
                return ("Decode regression on Arc B580 (Vulkan) bisected to "
                        "0bb496db (#29622, embd+raw batch support), Gemma-4-E4B "
                        "Q4_0, llama-bench -p 512 -n 128: parent 2ca15f54 "
                        f"{val(rows,'lc30018-b580-gemma4-before','tps')} -> "
                        f"{val(rows,'lc30018-b580-gemma4-after','tps')} tok/s decode "
                        f"({pct(rows,'lc30018-b580-gemma4-before','lc30018-b580-gemma4-after','tps'):+.1f}%), "
                        f"prefill {val(rows,'lc30018-b580-gemma4-before','pp_tps')} -> "
                        f"{val(rows,'lc30018-b580-gemma4-after','pp_tps')} tok/s "
                        f"({pct(rows,'lc30018-b580-gemma4-before','lc30018-b580-gemma4-after','pp_tps'):+.1f}%). "
                        "Bisect points bf79dbb "
                        f"{val(rows,'lc30018-b580-gemma4-bf79dbb','tps')} and a7fb71f "
                        f"{val(rows,'lc30018-b580-gemma4-a7fb71f','tps')} tok/s isolate "
                        "the single regressing commit. Cause: gemma scales input "
                        "embeddings by sqrt(n_embd); #29622 turned that constant "
                        "into per-batch scale_rows work, which hurts b1 decode. "
                        "Qwen3-14B (no input scale) is unaffected.")
            if model == "Qwen3 14B":
                return ("Control arm for the #29622 regression on Arc B580: "
                        "Qwen3-14B decodes "
                        f"{val(rows,'lc30018-b580-qwen314b-before','tps')} tok/s on "
                        "both sides of the boundary (no input-embedding scale, "
                        "no regression).")
            return None
        if (venue, issue) == ("llama.cpp", "10879") and any("c18711544" in i for i in rows):
            fa0 = next(i for i in rows if i.endswith("fa0"))
            fa1 = next(i for i in rows if i.endswith("fa1"))
            be = rows[fa0].get("backend") or ""
            if hw == "Ryzen AI Max+ 395":
                return ("Strix Halo (Ryzen AI Max+ 395) CPU, 16 threads, "
                        "llama 7B Q4_0, llama-bench. fa=0 -> fa=1: prefill "
                        f"{val(rows,fa0,'pp_tps')} -> {val(rows,fa1,'pp_tps')} tok/s "
                        f"({pct(rows,fa0,fa1,'pp_tps'):+.1f}%), decode "
                        f"{val(rows,fa0,'tps')} -> {val(rows,fa1,'tps')} tok/s "
                        f"({pct(rows,fa0,fa1,'tps'):+.1f}%).")
            if "ROCm" in be:
                return ("Strix Halo Radeon 8060S iGPU, ROCm, ngl 100, "
                        "llama 7B Q4_0, llama-bench. fa=0 -> fa=1: prefill "
                        f"{val(rows,fa0,'pp_tps')} -> {val(rows,fa1,'pp_tps')} tok/s "
                        f"({pct(rows,fa0,fa1,'pp_tps'):+.1f}%), decode "
                        f"{val(rows,fa0,'tps')} -> {val(rows,fa1,'tps')} tok/s "
                        f"({pct(rows,fa0,fa1,'tps'):+.1f}%).")
            if "Vulkan" in be:
                return ("Strix Halo Radeon 8060S iGPU, Vulkan (RADV strix_halo), "
                        "ngl 100, llama 7B Q4_0, llama-bench. fa=0 -> fa=1: prefill "
                        f"{val(rows,fa0,'pp_tps')} -> {val(rows,fa1,'pp_tps')} tok/s "
                        f"({pct(rows,fa0,fa1,'pp_tps'):+.1f}%), decode "
                        f"{val(rows,fa0,'tps')} -> {val(rows,fa1,'tps')} tok/s "
                        f"({pct(rows,fa0,fa1,'tps'):+.1f}%). Reporter: Vulkan has "
                        "improved a lot on Strix Halo and is now ahead of ROCm on "
                        f"both axes at fa=1 (decode {val(rows,fa1,'tps')} vs 51.33 "
                        f"tok/s, prefill {val(rows,fa1,'pp_tps')} vs 1456.15 tok/s).")
            return None
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
        if (venue, issue) == ("vLLM", "60159"):
            if model == "Kimi-K3":
                return ("Native ROCm merge_attn_states kernel versus the Triton "
                        "fallback, Kimi-K3 on 8x MI355X TP=8, FP8 KV cache, "
                        "concurrency 16: at 60k-in / 600-out output "
                        f"{val(rows,'vllm-60159-mi355x8-triton-60k','tps')} -> "
                        f"{val(rows,'vllm-60159-mi355x8-native-60k','tps')} tok/s "
                        f"({pct(rows,'vllm-60159-mi355x8-triton-60k','vllm-60159-mi355x8-native-60k','tps'):+.1f}%), at 128k-in / "
                        f"1k-out {val(rows,'vllm-60159-mi355x8-triton-128k','tps')} -> "
                        f"{val(rows,'vllm-60159-mi355x8-native-128k','tps')} tok/s "
                        f"({pct(rows,'vllm-60159-mi355x8-triton-128k','vllm-60159-mi355x8-native-128k','tps'):+.1f}%): "
                        "the merge kernel itself is 4.1x / 4.3x faster, but it is "
                        "only 0.26% / 0.42% of total kernel time, so end-to-end "
                        "throughput and mean TTFT move within run-to-run noise. "
                        "Unit level: 2592 timed cases per GPU, median 2.39x "
                        "(MI325X gfx942) and 2.36x (MI355X gfx950), 0 slower.")
            return None
        if (venue, issue) == ("vLLM", "60158"):
            if model == "DiffusionGemma-26B-A4B":
                return ("FA4 hd512 Blackwell attention (d=dv=512, SM100/SM110) "
                        "versus the Triton fallback on one B300, BF16 TP1, "
                        "concurrency 1: block tok/s "
                        f"{val(rows,'vllm-60158-b300-diffgemma-triton','tps')} "
                        "-> "
                        f"{val(rows,'vllm-60158-b300-diffgemma-fa4','tps')}-1206 "
                        f"({pct(rows,'vllm-60158-b300-diffgemma-triton','vllm-60158-b300-diffgemma-fa4','tps'):+.0f}% "
                        "to the published range's low end), mean end-to-end "
                        "1.36 s -> 1.03-1.07 s, first block "
                        f"{val(rows,'vllm-60158-b300-diffgemma-triton','ttft_s')} s "
                        "-> 0.39-0.42 s. GSM8K 126/128 -> 125/128, a one-question "
                        "flip within noise. Kernel level: the hd512 attention "
                        "call is 80 us vs Triton's 658 us (k=8256, page 128).")
            return None
        if (venue, issue) == ("vLLM", "60153"):
            return ("Routing the gfx942 mHC seam through one fused PyISA kernel "
                    "instead of the delayed AITER seam, 4x MI325X TP4, "
                    "DeepSeek-V4.1-Flash, vllm bench serve c=2: at 262144-in / "
                    "1024-out output "
                    f"{val(rows,'vllm-60153-mi325x4-off-262k','tps')} -> "
                    f"{val(rows,'vllm-60153-mi325x4-on-262k','tps')} tok/s "
                    f"({pct(rows,'vllm-60153-mi325x4-off-262k','vllm-60153-mi325x4-on-262k','tps'):+.1f}%), "
                    "mean TTFT "
                    f"{val(rows,'vllm-60153-mi325x4-off-262k','ttft_s')} -> "
                    f"{val(rows,'vllm-60153-mi325x4-on-262k','ttft_s')} ms; at 8192-in "
                    "the gain is smaller, "
                    f"{val(rows,'vllm-60153-mi325x4-off-8k','tps')} -> "
                    f"{val(rows,'vllm-60153-mi325x4-on-8k','tps')} tok/s. "
                    "The fused seam is 468 us per call vs the three-kernel "
                    "319/291/174 us family it replaces.")
        if (venue, issue) == ("vLLM", "59916"):
            g = "vllm-59916-b300x4-glm53-tp1pcp4-gatherdcp4"
            k = "vllm-59916-b300x4-glm53-tp1pcp4-kvpp"
            rep = "vllm-59916-b300x4-glm53-tp1pcp4-replicated"
            t4g = "vllm-59916-b300x4-glm53-tp4-gatherdcp4"
            t4n = "vllm-59916-b300x4-glm53-tp4-nativedcp4"
            return (f"Gather-based DCP on 4x B300, GLM-5.3-NVFP4 prefix-pooled "
                    f"prefill (60K shared + 6K unique, OSL 1, concurrency 8): at "
                    f"TP1\u00d7PCP4 gather DCP4 does {val(rows,g,'pp_tps'):.1f}K tok/s, "
                    f"matching KVPP ({val(rows,k,'pp_tps'):.1f}K, "
                    f"{pct(rows,k,g,'pp_tps'):+.1f}%) and "
                    f"{val(rows,g,'pp_tps')/val(rows,rep,'pp_tps'):.1f}x replicated "
                    f"({val(rows,rep,'pp_tps'):.1f}K), holding 2.40M KV tokens vs KVPP "
                    f"2.18M; at TP4 gather DCP4 ({val(rows,t4g,'pp_tps'):.1f}K) is "
                    f"{val(rows,t4g,'pp_tps')/val(rows,t4n,'pp_tps'):.2f}x native DCP4 "
                    f"({val(rows,t4n,'pp_tps'):.1f}K).")
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
        if (venue, issue) == ("vLLM", "59846"):
            return ("DeepSeek-V4.1-Flash, TP4 on 4x RTX PRO 6000 Blackwell "
                    "(SM120), vLLM, FP8 model. KV-cache dtype A/B: the V4 record "
                    "(before this PR) vs nvfp4_ds_mla, which SM120 rejected before "
                    "and now accepts. Aggregate output tok/s, 8k in / 1k out, by "
                    "concurrency: at c64, V4 "
                    f"{val(rows,'vllm-59846-sm120-v4rec-c64','tps')} vs nvfp4 "
                    f"{val(rows,'vllm-59846-sm120-nvfp4-c64','tps')} tok/s. "
                    "Throughput is unchanged within 2% (no regression) at every "
                    "concurrency except c32 nvfp4 ("
                    f"{val(rows,'vllm-59846-sm120-nvfp4-c32','tps')} vs V4 "
                    f"{val(rows,'vllm-59846-sm120-v4rec-c32','tps')}, one run, "
                    "not claimed per the PR). The PR's real win is capacity: "
                    "nvfp4_ds_mla fits 305,319 KV tokens vs 214,991 for the V4 "
                    "record (+42%) at the same throughput. The source table is "
                    "malformed (an empty column plus a duplicated fp8_ds_mla "
                    "header); only the clearly-labeled V4-before and nvfp4 "
                    "columns are mined.")
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
                    f"Rust: {val(rows,'vllm-59489-rtx3070-rust','tps'):g}-1680, "
                    f"Python: {val(rows,'vllm-59489-rtx3070-python','tps'):g}-1673 "
                    "output tok/s over three runs, 200/200 requests each, "
                    "with TPOT/ITL within run noise. The point of the PR is "
                    "parity for the Responses API, not a speedup.")
        if (venue, issue) == ("vLLM", "59668"):
            pts = [("8k1k", "8192/1024", ["4", "8", "16", "32", "64",
                                          "128", "256"]),
                   ("60k600", "60000/600", ["4", "16", "64"]),
                   ("128k1k", "128000/1024", ["4", "16"])]
            segs = []
            for key, label, concs in pts:
                pairs = ", ".join(
                    f"c{c} "
                    f"{val(rows,f'vllm-59668-mi355x-{key}-c{c}-default','tps')} -> "
                    f"{val(rows,f'vllm-59668-mi355x-{key}-c{c}-fused','tps')}"
                    for c in concs)
                segs.append(f"{label}: {pairs}")
            return ("Single-launch DSA decode candidate mask on MI355X "
                    "(TP4 + EP, FP8): the flags kernel is folded into the "
                    "mask kernel and the int64 cast and zeros_like before it "
                    "are dropped. Output throughput tok/s, default -> fused, "
                    "by input/output length and concurrency. " + "; ".join(segs)
                    + ". Mean +0.44% throughput and -0.48% TPOT over the 12 "
                    "sweep points (no single point moves more than 1%); the "
                    "mask kernel alone is 1.06x to 2.50x faster on MI355X. "
                    "GSM8K unchanged within error.")
        if (venue, issue) == ("vLLM", "59878"):
            A = "vllm-59878-sm80-1k256-triton"
            B = "vllm-59878-sm80-1k256-flashinfer"
            return ("FlashInfer fa2 sink wrappers routed on SM8x for "
                    "gpt-oss-20b with a BF16 KV cache, so the sink model now "
                    "selects FLASHINFER instead of TRITON_ATTN by backend "
                    "priority: total tok/s at 1024 in / 256 out (200 prompts), "
                    "averaged over two sm_80 GPUs. "
                    f"TRITON_ATTN {val(rows,A,'tps'):g} vs FLASHINFER "
                    f"{val(rows,B,'tps'):g} ({pct(rows,A,B,'tps'):+.1f}%). "
                    "The batch-1 latency gap is in decode (FlashInfer decode "
                    "attention kernel 9.07 us/layer vs Triton 4.73); prefill "
                    "matches, and batch-32 latency is 2.76% lower.")
        if (venue, issue) == ("vLLM", "59894"):
            A8 = "vllm-59894-b200x4-8k1c16-main"
            B8 = "vllm-59894-b200x4-8k1c16-pr"
            A32 = "vllm-59894-b200x4-32k256c32-main"
            B32 = "vllm-59894-b200x4-32k256c32-pr"
            return ("Decoder SWA bounded replay (#58132) now splits the cut "
                    "layer (20 on DSV4.1-Flash) by default, so trimmed replay "
                    "rows only run the KV side. DSV4.1-Flash DEP4, B200 x4, "
                    "vllm bench serve, main -> PR. Total tok/s 8k in / 1 out "
                    f"C16: {val(rows,A8,'tps'):g} -> {val(rows,B8,'tps'):g} "
                    f"({pct(rows,A8,B8,'tps'):+.1f}%), TTFT "
                    f"{val(rows,A8,'ttft_s'):.0f} -> {val(rows,B8,'ttft_s'):.0f} ms. "
                    "Output tok/s 32k in / 256 out C32: "
                    f"{val(rows,A32,'tps'):g} -> {val(rows,B32,'tps'):g} "
                    f"({pct(rows,A32,B32,'tps'):+.1f}%), TPOT "
                    "25.4 -> 23.1 ms. "
                    "GSM8K 0.9629 -> 0.9651, within noise.")
        if (venue, issue) == ("vLLM", "59732"):
            segs = []
            for key, label, concs in (("8k1k", "8192/1024", ("4", "16", "64")),
                                      ("60k600", "60000/600", ("4",))):
                pairs = ", ".join(
                    f"c{c} "
                    f"{val(rows,f'vllm-59732-mi355x-{key}-c{c}-ctrl','tps')} -> "
                    f"{val(rows,f'vllm-59732-mi355x-{key}-c{c}-fused','tps')}"
                    for c in concs)
                segs.append(f"{label}: {pairs}")
            return ("QSA prepare launch on MI355X (TP2, MXFP4): the "
                    "main-attention QK-norm, RoPE, gate split and K/V cache "
                    "write are folded into the fused QSA prepare launch, as "
                    "already done for NVIDIA. Output throughput tok/s, "
                    "unfused -> fused, by input/output length and "
                    "concurrency. " + "; ".join(segs)
                    + ". Gain +0.9% to +2.9%, faster in all 8 measured cells. "
                    "GSM8K 0.9638 -> 0.9605, within run-to-run noise.")
        if (venue, issue) == ("vLLM", "59733"):
            return ("Kimi-K3 + DSpark draft on MI355X (TP8, MXFP4): #57652 "
                    "dropped the KV cache from 4 to 20 groups because the "
                    "DSpark draft spec omitted max_tp_shards, so the MLA "
                    "layers stopped merging. This PR declares "
                    "max_tp_shards=1 to restore the 4-group layout. Output "
                    "tok/s by build (c8, 8K/1K): pre-#57652 nightly "
                    f"{val(rows,'vllm-59733-mi355x-k3-36768d1','tps'):g}, "
                    f"current nightly with #57652 "
                    f"{val(rows,'vllm-59733-mi355x-k3-ac9126e','tps'):g}, full "
                    f"revert {val(rows,'vllm-59733-mi355x-k3-revert57652','tps'):g}, "
                    f"this PR {val(rows,'vllm-59733-mi355x-k3-59733','tps'):g}. "
                    "The fix restores pre-#57652 throughput (median TPOT "
                    "11.47 -> 11.09 ms).")
        if (venue, issue) == ("vLLM", "59778"):
            if hw == "GB10":
                return ("CuTe skinny-GEMM table for GB10 (sm_121) on "
                        "Qwen3.8-Flash-Next-NVFP4 (MTP, TP=1, ISL "
                        "2048/OSL 256): the table cuts aiperf TPOT "
                        "(ms/token, lower is better) hardest at low batch. "
                        "At bs=1, k=3 it drops "
                        f"{val(rows,'vllm-59778-gb10-b1k3-base','tps')} -> "
                        f"{val(rows,'vllm-59778-gb10-b1k3-tuned','tps')} "
                        f"({pct(rows,'vllm-59778-gb10-b1k3-base','vllm-59778-gb10-b1k3-tuned','tps'):.1f}%), "
                        "and the effect shrinks as batch grows toward the "
                        "kernel's M<=16 limit: bs=1 k=1 "
                        f"{val(rows,'vllm-59778-gb10-b1k1-base','tps')} -> "
                        f"{val(rows,'vllm-59778-gb10-b1k1-tuned','tps')}, "
                        "bs=2 k=3 "
                        f"{val(rows,'vllm-59778-gb10-b2k3-base','tps')} -> "
                        f"{val(rows,'vllm-59778-gb10-b2k3-tuned','tps')}, "
                        "bs=4 k=3 "
                        f"{val(rows,'vllm-59778-gb10-b4k3-base','tps')} -> "
                        f"{val(rows,'vllm-59778-gb10-b4k3-tuned','tps')}. "
                        "n=3 per arm (3.1 sigma at the headline point); "
                        "84% of the gain is the LM head.")
        if (venue, issue) == ("vLLM", "59779"):
            if hw == "B300":
                return ("Watermarking fix (stale draft prompt lengths under "
                        "CUDA graphs) on Qwen3-4B + EAGLE3, aggregate output "
                        "tok/s, main vs fix. A correctness change with no "
                        "measurable regression: the fix moves output "
                        f"c1 {val(rows,'vllm-59779-b300-c1-main','tps'):g} -> "
                        f"{val(rows,'vllm-59779-b300-c1-fix','tps'):g}, "
                        f"c8 {val(rows,'vllm-59779-b300-c8-main','tps'):g} -> "
                        f"{val(rows,'vllm-59779-b300-c8-fix','tps'):g}, "
                        f"c64 {val(rows,'vllm-59779-b300-c64-main','tps'):g} -> "
                        f"{val(rows,'vllm-59779-b300-c64-fix','tps'):g}; "
                        "every delta is within its 95% CI, which includes "
                        "zero, and mean TTFT rises 0.35-0.65 ms, inside the "
                        "A/A noise floor.")
        if (venue, issue) == ("vLLM", "59824"):
            if hw == "MI355X":
                return ("DSpark adaptive verification on Kimi-K3 FP4 TP8, "
                        "MI355X ROCm. enable_adaptive_verification trims each "
                        "verify request to 1..k+1 tokens on the device using the "
                        "DSpark confidence head; off is the static K=7 baseline. "
                        "Output tok/s, off -> on: "
                        f"c10 {val(rows,'vllm-59824-c10-off','tps'):g} -> "
                        f"{val(rows,'vllm-59824-c10-on','tps'):g} "
                        f"({pct(rows,'vllm-59824-c10-off','vllm-59824-c10-on','tps'):+.1f}%), "
                        f"c12 {val(rows,'vllm-59824-c12-off','tps'):g} -> "
                        f"{val(rows,'vllm-59824-c12-on','tps'):g} "
                        f"({pct(rows,'vllm-59824-c12-off','vllm-59824-c12-on','tps'):+.1f}%), "
                        f"c14 {val(rows,'vllm-59824-c14-off','tps'):g} -> "
                        f"{val(rows,'vllm-59824-c14-on','tps'):g} "
                        f"({pct(rows,'vllm-59824-c14-off','vllm-59824-c14-on','tps'):+.1f}%). "
                        "KV cache capacity drops ~9.8% (3.31M -> 2.99M tok); the "
                        "gains are against static K=7, not the best static K per "
                        "concurrency, and trimming only kicks in at conc >= 8.")
        if (venue, issue) == ("vLLM", "59653"):
            dec = ", ".join(
                f"c{c} {val(rows,f'vllm-59653-mi350x-dec-c{c}-off','tps'):g} -> "
                f"{val(rows,f'vllm-59653-mi350x-dec-c{c}-on','tps'):g}"
                for c in ("1", "2", "4", "8", "16"))
            srv = ", ".join(
                f"c{c} {val(rows,f'vllm-59653-mi350x-srv-c{c}-off','tps'):g} -> "
                f"{val(rows,f'vllm-59653-mi350x-srv-c{c}-on','tps'):g}"
                for c in ("2", "4", "8"))
            return ("Fused sparse-layer decode via AITER on 4x MI350X "
                    "(MiniMax-M3 MXFP4, TP4, FP8 KV): each of the 57 sparse "
                    "MoE layers runs as one kernel launch with both TP "
                    "all-reduces inside the kernel, on pure decode steps of "
                    "up to 16 tokens. Output tok/s, unfused -> fused. Decode "
                    f"8K/256: {dec} (1.95x at c1, TPOT 6.14 -> 3.15 ms). "
                    f"Serving 128K/1K: {srv} (+24% at c2). The gain shrinks "
                    "with concurrency because launches stop dominating. "
                    "GSM8K 0.948 both ways.")
        if (venue, issue) == ("vLLM", "59567"):
            pts = [("p1024", "1024/1024"), ("p256", "256/256"),
                   ("p256wide", "256/256 wide (50 ids/token)")]
            segs = []
            for pid, label in pts:
                segs.append(
                    f"{label}: no mask "
                    f"{val(rows,f'vllm-59567-gb300-{pid}-base','tps'):g}, stock "
                    f"{val(rows,f'vllm-59567-gb300-{pid}-stock','tps'):g}, "
                    f"branch "
                    f"{val(rows,f'vllm-59567-gb300-{pid}-branch','tps'):g}")
            return ("Sampling-mask transport cost A/B on one GB300 "
                    "(Qwen3-8B, c=256, median of 2 passes). The PR moves "
                    "mask work from per-request to per-step batches. Output "
                    "tok/s, no mask / stock mask path / this PR: "
                    + "; ".join(segs) + ". The stock mask path costs 4.9% "
                    "(narrow) to 17.6% (wide); the PR cuts that to 0.9% to "
                    "11.3%. Most of the removed cost was CPU-side: msgspec "
                    "encode/decode hooks, per-row CSR build, and pydantic "
                    "re-validation of the mask lists.")
        if (venue, issue) == ("vLLM", "59520"):
            return ("GDN decode kernel dispatch A/B on 2x H200 (Qwen3.5-9B "
                    "BF16, non-speculative decode, one sequential 2x2). The "
                    "default CUDA fused-norm wrapper only helps "
                    "speculative/MTP batches; for pure decode the Triton "
                    "path is faster. Output tok/s, CUDA default -> Triton: "
                    "sparse retention "
                    f"{val(rows,'vllm-59520-h200-sparse-cuda','tps')} -> "
                    f"{val(rows,'vllm-59520-h200-sparse-triton','tps')} "
                    "(+30.35%), dense retention "
                    f"{val(rows,'vllm-59520-h200-dense-cuda','tps')} -> "
                    f"{val(rows,'vllm-59520-h200-dense-triton','tps')} "
                    "(+34.68%). Measured on vLLM 0.29.0; the reporter did "
                    "not rerun current main, but the same dispatch is still "
                    "in the source.")
        if (venue, issue) == ("vLLM", "59548"):
            if hw == "A10":
                return ("Spec-decode boot-to-boot dispersion A/B, Qwen3-4B "
                        "with a DFlash-b16 drafter, concurrency 1, mean of "
                        "12 boots per arm, vLLM 0.29.0 on an A10. "
                        "CUDA-graph default vs --enforce-eager: "
                        f"{val(rows,'vllm-59548-a10-e-default','tps')} vs "
                        f"{val(rows,'vllm-59548-a10-e-eager','tps')} tok/s "
                        "(ratio 0.959, CV 2.08%). The same config on L4 "
                        "lost up to half its throughput to boot luck; the "
                        "A10 is nearly immune, and the reporter suspects "
                        "memory pressure (the L4's 22.03 GiB usable sits "
                        "right at this config's ceiling).")
            return ("Spec-decode boot-to-boot dispersion A/B, Qwen3-4B with "
                    "a DFlash-b16 drafter, concurrency 1, mean of 12 boots "
                    "per arm on one L4. CUDA-graph default vs "
                    "--enforce-eager, vLLM 0.29.0: session A "
                    f"{val(rows,'vllm-59548-l4-a-default','tps')} vs "
                    f"{val(rows,'vllm-59548-l4-a-eager','tps')} tok/s "
                    "(ratio 0.487, CV 13.92%), session B "
                    f"{val(rows,'vllm-59548-l4-b-default','tps')} vs "
                    f"{val(rows,'vllm-59548-l4-b-eager','tps')} (ratio "
                    "0.768, CV 3.73%). vLLM 0.30.0 reaches parity: session "
                    f"C {val(rows,'vllm-59548-l4-c-default','tps')} vs "
                    f"{val(rows,'vllm-59548-l4-c-eager','tps')} (1.014, CV "
                    f"0.99%), session D {val(rows,'vllm-59548-l4-d-default','tps')} "
                    f"vs {val(rows,'vllm-59548-l4-d-eager','tps')} (1.017, "
                    "CV 1.61%). The eager arm is stable everywhere, which "
                    "is what makes it usable as a control; acceptance length "
                    "is flat, so this is throughput, not acceptance. Same "
                    "config, same container, different boots: the "
                    "dispersion itself is not reproducible.")
        if (venue, issue) == ("vLLM", "59655"):
            return ("NVFP4 draft-expert quantization fix on DeepSeek V4.1 "
                    "Flash, GB300 TP4, DSpark k=5 speculative decoding, "
                    "MT-Bench output tok/s; every arm ran on the same three "
                    "nodes (node-to-node spread reaches ~25%). Unmodified "
                    "v0.30.0 mis-quantizes the MXFP4 mtp.* draft experts as "
                    "NVFP4: acceptance length collapses to 1.00 (0 of "
                    "604,200 draft tokens accepted) and speculation is pure "
                    "overhead. With the fix acceptance recovers to 2.80-2.87 "
                    "and node A goes "
                    f"{val(rows,'vllm-59655-gb300-a-c1-v030','tps'):g} -> "
                    f"{val(rows,'vllm-59655-gb300-a-c1-pr','tps'):g} tok/s at "
                    "concurrency 1 (2.19x; 2.39x and 2.45x on nodes B and "
                    "C) and "
                    f"{val(rows,'vllm-59655-gb300-a-c8-v030','tps'):g} -> "
                    f"{val(rows,'vllm-59655-gb300-a-c8-pr','tps'):g} at "
                    "concurrency 8 (1.90x; 1.95x and 2.08x elsewhere). The "
                    "native checkpoint arm lands within -13.1% to +0.4% of "
                    "the PR (the author's back-to-back rotated runs show "
                    "+2.5%, so the gap is node noise). Median TPOT at c1: "
                    "8.49 -> 3.28 ms, native 3.06 ms. GSM8K accuracy is "
                    "unchanged either way, which is exactly why only an "
                    "acceptance-length gate catches this bug.")
        if (venue, issue) == ("llama.cpp", "29772"):
            return ("Vulkan FWHT extended from width 512 up to 8192: wide "
                    "Hadamard blocks move from the dense f32 fallback to a "
                    "shared-memory FWHT shader. Radeon 860M (RDNA 3.5), "
                    "Bonsai 2 27B Q2_0: decode "
                    f"{val(rows,'lc-29772-radeon860m-fwht-master','tps')} -> "
                    f"{val(rows,'lc-29772-radeon860m-fwht-pr','tps')} tok/s "
                    f"({pct(rows,'lc-29772-radeon860m-fwht-master','lc-29772-radeon860m-fwht-pr','tps'):+.1f}%), "
                    "pp512 59.2 -> 66.4, pp2048 55.8 -> 62.2 (+12 to "
                    "13%), KLD unchanged. The underlying op at width 8192 "
                    "drops 76.4 ms -> 2.0 ms; widths 64-512 are untouched. "
                    "Same fix measured on Apple M5 Pro in the body "
                    "(kernel-level only).")
        if (venue, issue) == ("vLLM", "59600"):
            return ("ShortConv drafter state restore fix for the Mamba "
                    "hybrid LFM2.5 target on ROCm. Radeon 8060S "
                    "(gfx1151), TP1, BF16, GSM8K first 32 questions, "
                    "offline output tok/s: target only "
                    f"{val(rows,'vllm-59600-8060s-target-only','tps')} -> "
                    f"target + fixed LFM2.5-350M drafter K=3 "
                    f"{val(rows,'vllm-59600-8060s-drafter-k3','tps')} "
                    f"({pct(rows,'vllm-59600-8060s-target-only','vllm-59600-8060s-drafter-k3','tps'):+.1f}%). "
                    "Acceptance 71.83% (4,491/6,252 draft tokens); "
                    "accuracy identical at 16/32, single run each. Before "
                    "the fix the drafter's recurrent state was not "
                    "restored on rejected tails, which is why speculation "
                    "previously did not help.")
        if (venue, issue) == ("vLLM", "59606"):
            return ("MoE backend A/B on a DGX Spark (GB10, SM121) TP2, "
                    "CYBER-FROST-3.8-NVFP4 (512 experts, top-10) with MTP "
                    "k=3, vLLM 0.30.0. 8-stream aggregate decode: "
                    f"flashinfer_cutlass {val(rows,'vllm-59606-spark-decode-cutlass','tps')} "
                    "vs native b12x "
                    f"{val(rows,'vllm-59606-spark-decode-b12x','tps')} "
                    f"tok/s ({pct(rows,'vllm-59606-spark-decode-cutlass','vllm-59606-spark-decode-b12x','tps'):+.1f}% "
                    "for b12x), and at 1 stream 43 vs 48 ms per step. "
                    "b12x is also broken here beyond speed: illegal memory "
                    "access during CUDA-graph capture with padded batches, "
                    "and a worker kill on the first 6,941-token prefill "
                    "even with the padding workaround. NLL identical. "
                    "Reporter reverted to flashinfer_cutlass.")
        if (venue, issue) == ("vLLM", "59514"):
            return ("silu_and_mul_quant kernel fix (dead vector loop, fp32 "
                    "fast-math chain), H100, Llama 3.1 8B FP8, vllm bench "
                    "serve output tok/s, three interleaved rounds per arm "
                    "in one session: main kernel "
                    f"{val(rows,'vllm-59514-h100-main-kernel','tps')} -> PR "
                    f"{val(rows,'vllm-59514-h100-pr','tps')} "
                    f"({pct(rows,'vllm-59514-h100-main-kernel','vllm-59514-h100-pr','tps'):+.1f}%), "
                    "torch Inductor path "
                    f"{val(rows,'vllm-59514-h100-inductor','tps')} (PR vs "
                    "Inductor +0.6%, noise; outputs bit-identical). Every "
                    "main round is below every PR round. Fused op's GPU "
                    "time per profile iteration: 69.87 -> 27.63 ms; mean "
                    "TPOT 73.31 -> 70.66 ms. GSM8K differences are noise.")
        if (venue, issue) == ("vLLM", "59679"):
            slug = {"GLM-4-9B-Chat": "glm-4-9b-chat",
                    "AFM-4.5B-Base": "afm-4-5b-base",
                    "facebook/cwm": "cwm",
                    "Mellum2-12B-A2.5B-Base": "mellum2-12b-a2-5b"}[model]
            return ("Migration to the Transformers modeling backend, "
                    f"{model} on 1x B200, vllm bench throughput 1024/256 "
                    "x 1000 prompts, one run per cell: main "
                    f"{val(rows,f'vllm-59679-b200-{slug}-main','tps')} vs "
                    f"branch {val(rows,f'vllm-59679-b200-{slug}-branch','tps')} "
                    f"tok/s ({pct(rows,f'vllm-59679-b200-{slug}-main',f'vllm-59679-b200-{slug}-branch','tps'):+.1f}%). "
                    "The author states the +-1.5% spread is run-to-run "
                    "noise, not a speedup or regression, and gsm8k agrees "
                    "within noise: this is a parity check, recorded as "
                    "one.")
        if (venue, issue) == ("vLLM", "59701"):
            slug = {"pythia-12b": "pythia-12b", "phi-2": "phi-2",
                    "Seed-OSS-36B-Base": "seed-oss-36b-base",
                    "Jais-2-8B-Chat": "jais-2-8b-chat"}[model]
            return ("Migration to the Transformers modeling backend, "
                    f"{model} on 1x B200, vllm bench throughput 1024/256 "
                    "x 1000 prompts, one run per cell: main "
                    f"{val(rows,f'vllm-59701-b200-{slug}-main','tps')} vs "
                    f"branch {val(rows,f'vllm-59701-b200-{slug}-branch','tps')} "
                    f"tok/s ({pct(rows,f'vllm-59701-b200-{slug}-main',f'vllm-59701-b200-{slug}-branch','tps'):+.1f}%). "
                    "The author states the +-1% spread is run-to-run "
                    "noise, not a speedup or regression, and gsm8k agrees "
                    "within noise: this is a parity check, recorded as "
                    "one.")
        if (venue, issue) == ("vLLM", "59594"):
            return ("KV-cache layout fallback fix (BLNHC -> BLHNC when a "
                    "connector needs head-major pages), RTX PRO 6000 TP2, "
                    "Qwen3.8-Flash-Next, 8K in / 1K out. Throughput is "
                    "flat across all ten concurrency cells: MTP3 c4 "
                    f"{val(rows,'vllm-59594-pro6000-mtp-blnhc-c4','tps')} vs "
                    f"{val(rows,'vllm-59594-pro6000-mtp-blhnc-c4','tps')} "
                    "(-2%, worst cell), c32 "
                    f"{val(rows,'vllm-59594-pro6000-mtp-blnhc-c32','tps')} "
                    f"vs {val(rows,'vllm-59594-pro6000-mtp-blhnc-c32','tps')} "
                    "(+1%, best); no-spec cells all within +-1%; p50 TPOT "
                    "identical. The point is functional: under BLNHC every "
                    "TP1-prefill pull failed the Mooncake handshake "
                    "(local=39739392 vs remote=1605632), BLHNC fixes it "
                    "for free.")
        if (venue, issue) == ("llama.cpp", "29768"):
            return ("CUDA graph warmup fix: recapture a changed graph once "
                    "instead of resetting warmup at every padded-KV length "
                    "step. RTX 5090, qwen35 (the author's llama-bench name; "
                    "an earlier revision of this body named Qwen3.8-27B "
                    "Q4_K_M), unified 128K KV cache on top of #29510. "
                    "Decode tok/s by sequence count, without -> with: npl 8 "
                    f"{val(rows,'lc-29768-rtx5090-npl8-off','tps'):g} -> "
                    f"{val(rows,'lc-29768-rtx5090-npl8-on','tps'):g} (+1.28%, "
                    "95% CI +0.84% to +1.72%), npl 6 "
                    f"{val(rows,'lc-29768-rtx5090-npl6-off','tps'):g} -> "
                    f"{val(rows,'lc-29768-rtx5090-npl6-on','tps'):g} (+0.85%), "
                    "npl 4 "
                    f"{val(rows,'lc-29768-rtx5090-npl4-off','tps'):g} -> "
                    f"{val(rows,'lc-29768-rtx5090-npl4-on','tps'):g} (+0.93%), "
                    "npl 2 "
                    f"{val(rows,'lc-29768-rtx5090-npl2-off','tps'):g} -> "
                    f"{val(rows,'lc-29768-rtx5090-npl2-on','tps'):g} (+0.27%), "
                    "npl 1 "
                    f"{val(rows,'lc-29768-rtx5090-npl1-off','tps'):g} -> "
                    f"{val(rows,'lc-29768-rtx5090-npl1-on','tps'):g} "
                    "(-0.30%). The warmup-reset count drops to 0 at every "
                    "npl; llama-bench tg128 is about 0.4% slower (a one-off "
                    "graph captured then discarded after each memory "
                    "clear).")
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
            if model == "gpt-oss 20B":
                return ("SYCL MXFP4 MoE A/B on Intel Arc Pro B70 (Windows "
                        "11, oneAPI 2026.0, EPYC 7402P host). The patch "
                        "replaces table-based MXFP4 decoding with "
                        "bit-identical 32-bit arithmetic plus lazy "
                        "per-expert weight reordering. gpt-oss 20B decode "
                        "on one card: "
                        f"{val(rows,'lc-29809-b70-20b-dec-before','tps')} -> "
                        f"{val(rows,'lc-29809-b70-20b-dec-after','tps')} "
                        "tok/s (1.91x, mean of 5 repetitions). Perplexity "
                        "14.5148 -> 14.5129, within noise.")
            return ("SYCL MXFP4 MoE A/B on Intel Arc Pro B70 (Windows 11, "
                    "oneAPI 2026.0, EPYC 7402P host). The patch replaces "
                    "table-based MXFP4 decoding with bit-identical 32-bit "
                    "arithmetic plus lazy per-expert weight reordering. "
                    "gpt-oss 120B decode on two cards: "
                    f"{val(rows,'lc-29809-2xb70-120b-dec-before','tps')} -> "
                    f"{val(rows,'lc-29809-2xb70-120b-dec-after','tps')} tok/s "
                    "(2.02x, mean of 2 repetitions). Prompt processing "
                    "barely moves "
                    f"({val(rows,'lc-29809-2xb70-120b-pp-before','pp_tps')} -> "
                    f"{val(rows,'lc-29809-2xb70-120b-pp-after','pp_tps')} "
                    "tok/s): the win is in the decode-side expert matmuls. "
                    "Perplexity 14.5148 -> 14.5129, within noise.")
        if (venue, issue) == ("llama.cpp", "29807"):
            return ("CUDA copy removal after SSM_SCAN (recurrent state "
                    "snapshots are written straight into the cache by the "
                    "kernel). nemotron_h_moe 31B.A3.5B Q4_K_M on RTX PRO "
                    "6000 Blackwell, Windows. Without MTP the change is "
                    "flat: pp512 "
                    f"{val(rows,'lc-29807-pro6000b-pp512-master','pp_tps')} -> "
                    f"{val(rows,'lc-29807-pro6000b-pp512-pr','pp_tps')}, tg128 "
                    f"{val(rows,'lc-29807-pro6000b-tg128-master','tps')} -> "
                    f"{val(rows,'lc-29807-pro6000b-tg128-pr','tps')} (both "
                    "1.00x). With MTP drafting the removed copies matter: "
                    f"SPEED-Bench coding decode "
                    f"{val(rows,'lc-29807-pro6000b-mtp-master','tps')} -> "
                    f"{val(rows,'lc-29807-pro6000b-mtp-pr','tps')} t/s "
                    "(1.035x, faster on 80 of 80 prompts, acceptance 0.777 "
                    "identical on both builds).")
        if (venue, issue) == ("llama.cpp", "29836"):
            return ("Q8_0 matmul support added to the zDNN backend "
                    "(feat/zdnn-i8-upscale vs baseline build b11284) on the "
                    "IBM Z NNPA coprocessor. llama 1B Q8_0. The gain is "
                    "dramatic for prompt processing and modest for decode: "
                    "pp512 "
                    f"{val(rows,'lc-29836-nnpa-pp512-base','pp_tps'):g} -> "
                    f"{val(rows,'lc-29836-nnpa-pp512-pr','pp_tps'):g} tok/s "
                    "(9.67x), tg128 "
                    f"{val(rows,'lc-29836-nnpa-tg128-base','tps'):g} -> "
                    f"{val(rows,'lc-29836-nnpa-tg128-pr','tps'):g} tok/s "
                    "(1.39x). The multiplier shrinks as the @d context depth "
                    "grows: pp512 4.71x at d1024 to 2.39x at d4096, tg128 "
                    "1.17x at d1024 to 1.06x at d4096.")
        if (venue, issue) == ("llama.cpp", "29769"):
            return ("Unified decode masks built in one cache scan (sequence "
                    "membership bits, batches of 4+ tokens with one token "
                    "per sequence). RTX 5090, Qwen3.8-27B Q4_K_M, F16 KV. "
                    "The fast path (llama-batched-bench -c 131072 -npp 15872 "
                    "-ntg 512 -npl 8) medians "
                    f"{val(rows,'lc-29769-rtx5090-npl8-before','tps')} -> "
                    f"{val(rows,'lc-29769-rtx5090-npl8-after','tps')} tok/s, "
                    "+5.77% (95% CI +5.11% to +6.43%, mean of 10 paired "
                    "per-repetition changes). The sanity runs do not "
                    "trigger the fast path and move within noise: pp512 "
                    f"{val(rows,'lc-29769-rtx5090-pp512-before','pp_tps')} -> "
                    f"{val(rows,'lc-29769-rtx5090-pp512-after','pp_tps')} "
                    "(-0.33%), tg128 "
                    f"{val(rows,'lc-29769-rtx5090-tg128-before','tps')} -> "
                    f"{val(rows,'lc-29769-rtx5090-tg128-after','tps')} "
                    "(-0.23%); perplexity 6.1814 unchanged.")
        if (venue, issue) == ("llama.cpp", "29784"):
            return ("CPU thread default fix for Apple chips with Super and "
                    "Performance clusters: sum every hw.perflevelN."
                    "physicalcpu instead of reading only perflevel0. M5 Max "
                    "(6 Super + 12 Performance), muse-glimmer 30B Q4_K_XL, "
                    "llama-bench -ngl 0 -r 3 CPU-only, default threads 6 -> "
                    "18: pp512 "
                    f"{val(rows,'lc-29784-m5max-pp512-master','pp_tps')} -> "
                    f"{val(rows,'lc-29784-m5max-pp512-fix','pp_tps')} t/s "
                    "(2.18x), tg128 "
                    f"{val(rows,'lc-29784-m5max-tg128-master','tps')} -> "
                    f"{val(rows,'lc-29784-m5max-tg128-fix','tps')} (1.48x). "
                    "Prompt processing benefits most: it is the "
                    "thread-starved side of the old 6-core default.")
        if (venue, issue) == ("llama.cpp", "29824"):
            return ("qwen4exp attention-mask construction repeats rows "
                    "instead of 1-element seeds (the seed-repeat graph is "
                    "slow on Metal). M2 Ultra, Qwen3.8-Flash-Next GGUF, "
                    "llama-batched-bench B=1, npp=ctx, ntg=32. Prompt "
                    "processing S_PP t/s, master -> PR: 2048 "
                    f"{val(rows,'lc-29824-m2ultra-2048-master','pp_tps'):g} -> "
                    f"{val(rows,'lc-29824-m2ultra-2048-pr','pp_tps'):g}, 8192 "
                    f"{val(rows,'lc-29824-m2ultra-8192-master','pp_tps'):g} -> "
                    f"{val(rows,'lc-29824-m2ultra-8192-pr','pp_tps'):g}, 32768 "
                    f"{val(rows,'lc-29824-m2ultra-32768-master','pp_tps'):g} -> "
                    f"{val(rows,'lc-29824-m2ultra-32768-pr','pp_tps'):g}, 65536 "
                    f"{val(rows,'lc-29824-m2ultra-65536-master','pp_tps'):g} -> "
                    f"{val(rows,'lc-29824-m2ultra-65536-pr','pp_tps'):g}: the "
                    "PR recovers the long-context regression #29751 "
                    "introduced (pre-#29751 was 690.15 at 65536) and "
                    "surpasses it. Decode S_TG t/s roughly flat: 2048 "
                    f"{val(rows,'lc-29824-m2ultra-2048-master','tps'):g} -> "
                    f"{val(rows,'lc-29824-m2ultra-2048-pr','tps'):g}, 65536 "
                    f"{val(rows,'lc-29824-m2ultra-65536-master','tps'):g} -> "
                    f"{val(rows,'lc-29824-m2ultra-65536-pr','tps'):g}.")
        if (venue, issue) == ("llama.cpp", "29779"):
            if model == "Qwen3.5-2B":
                return ("3D ssm_out matmuls flattened to 2D so they run on "
                        "the Hexagon HMX instead of HVX (IQ-9075 NPU, "
                        "llama-batched-bench -c 4096 -npp 128 -ntg 32). "
                        "Qwen3.5-2B Q4_0: single sequence is flat (pp128 "
                        f"{val(rows,'lc-29779-qwen35-1pp-master','pp_tps'):g} "
                        f"-> {val(rows,'lc-29779-qwen35-1pp-patch','pp_tps'):g}"
                        ", tg32 "
                        f"{val(rows,'lc-29779-qwen35-1tg-master','tps'):g} -> "
                        f"{val(rows,'lc-29779-qwen35-1tg-patch','tps'):g}); "
                        "with 2 sequences pp128 x2 "
                        f"{val(rows,'lc-29779-qwen35-2pp-master','pp_tps'):g} "
                        f"-> {val(rows,'lc-29779-qwen35-2pp-patch','pp_tps'):g} "
                        "(+58.9%), tg32 x2 "
                        f"{val(rows,'lc-29779-qwen35-2tg-master','tps'):g} -> "
                        f"{val(rows,'lc-29779-qwen35-2tg-patch','tps'):g}; "
                        "with 4 sequences pp128 x4 "
                        f"{val(rows,'lc-29779-qwen35-4pp-master','pp_tps'):g} "
                        f"-> {val(rows,'lc-29779-qwen35-4pp-patch','pp_tps'):g} "
                        "(+57.8%), tg32 x4 "
                        f"{val(rows,'lc-29779-qwen35-4tg-master','tps'):g} -> "
                        f"{val(rows,'lc-29779-qwen35-4tg-patch','tps'):g}. "
                        "Per-call ssm_out MUL_MAT time drops 95.5% at npl 2.")
            return ("3D shortconv in/out_proj matmuls flattened to 2D so "
                    "they run on the Hexagon HMX instead of HVX (IQ-9075 "
                    "NPU, llama-batched-bench -c 4096 -npp 128 -ntg 32). "
                    "LFM2-2.6B Q4_0: single sequence is flat (pp128 "
                    f"{val(rows,'lc-29779-lfm2-1pp-master','pp_tps'):g} -> "
                    f"{val(rows,'lc-29779-lfm2-1pp-patch','pp_tps'):g}, tg32 "
                    f"{val(rows,'lc-29779-lfm2-1tg-master','tps'):g} -> "
                    f"{val(rows,'lc-29779-lfm2-1tg-patch','tps'):g}); with 2 "
                    "sequences pp128 x2 "
                    f"{val(rows,'lc-29779-lfm2-2pp-master','pp_tps'):g} -> "
                    f"{val(rows,'lc-29779-lfm2-2pp-patch','pp_tps'):g} "
                    "(+227.4%), tg32 x2 "
                    f"{val(rows,'lc-29779-lfm2-2tg-master','tps'):g} -> "
                    f"{val(rows,'lc-29779-lfm2-2tg-patch','tps'):g}; with 4 "
                    "sequences pp128 x4 "
                    f"{val(rows,'lc-29779-lfm2-4pp-master','pp_tps'):g} -> "
                    f"{val(rows,'lc-29779-lfm2-4pp-patch','pp_tps'):g} "
                    "(+224.7%), tg32 x4 "
                    f"{val(rows,'lc-29779-lfm2-4tg-master','tps'):g} -> "
                    f"{val(rows,'lc-29779-lfm2-4tg-patch','tps'):g}. The "
                    "single-sequence path keeps HVX; the gain is entirely "
                    "in multi-sequence batching.")
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
        if (venue, issue) == ("vLLM", "59973"):
            return ("Opt-in quantized draft lm_head for MTP spec-decode "
                    "(Qwen3.8-Flash-Next NVFP4, GB10, MTP k=3, "
                    "SPEED-Bench 4 users x 32 prompts, greedy, 256 output "
                    "tokens, full vocabulary). At c=4, the NVFP4 draft "
                    f"lm_head lifts decode from BF16 "
                    f"{val(rows,'vllm-59973-gb10-bf16-c4','tps')} -> "
                    f"{val(rows,'vllm-59973-gb10-nvfp4-c4','tps')} tok/s "
                    f"({pct(rows,'vllm-59973-gb10-bf16-c4','vllm-59973-gb10-nvfp4-c4','tps'):+.1f}%). "
                    f"At c=1 the BF16 baseline is "
                    f"{val(rows,'vllm-59973-gb10-bf16-c1','tps')} tok/s; "
                    "the PR reports the NVFP4 gain at c=1 only as a "
                    "relative +28.7%. The FP8 arm is measured against a "
                    "different stock node, so no absolute FP8 value is "
                    "recorded.")
        if (venue, issue) == ("vLLM", "60110"):
            return ("Kimi-K3 MLA decode on a 8x MI355X node (vLLM ROCm, "
                    "AITER, InferenceX agentic c14, 14 concurrent users). "
                    "Folding q_b_proj and W_UK into one GEMM lifts output "
                    f"throughput {val(rows,'vllm-60110-mi355x-kimik3-before','tps')} -> "
                    f"{val(rows,'vllm-60110-mi355x-kimik3-after','tps')} tok/s "
                    f"({pct(rows,'vllm-60110-mi355x-kimik3-before','vllm-60110-mi355x-kimik3-after','tps'):+.1f}%) "
                    "with gsm8k unchanged (0.9583 -> 0.9598 flexible-extract).")
        if (venue, issue) == ("vLLM", "60068"):
            return ("MRV2 opt-in confidence stop for autoregressive drafting "
                    "(Qwen3.8-Flash-Next NVFP4, GB10, MTP k=3, SPEED-Bench, "
                    "one run per arm). Stock uses 3 drafts with BF16 head; "
                    "fixed 6 and confidence stop use the NVFP4 head from "
                    f"#59973. At c=1: stock "
                    f"{val(rows,'vllm-60068-gb10-stock-c1','tps')} -> "
                    f"fixed 6 {val(rows,'vllm-60068-gb10-fixed6-c1','tps')} "
                    f"({pct(rows,'vllm-60068-gb10-stock-c1','vllm-60068-gb10-fixed6-c1','tps'):+.1f}%) -> "
                    f"stop {val(rows,'vllm-60068-gb10-stop-c1','tps')} "
                    f"({pct(rows,'vllm-60068-gb10-fixed6-c1','vllm-60068-gb10-stop-c1','tps'):+.1f}% vs fixed 6). "
                    f"At c=4: fixed 6 {val(rows,'vllm-60068-gb10-fixed6-c4','tps')} -> "
                    f"stop {val(rows,'vllm-60068-gb10-stop-c4','tps')} "
                    f"({pct(rows,'vllm-60068-gb10-fixed6-c4','vllm-60068-gb10-stop-c4','tps'):+.1f}%). "
                    "The stop gives up AL (fewer drafts) and wins on step "
                    "time; gain is largest where acceptance is low.")
        if (venue, issue) == ("vLLM", "60008"):
            return ("Hybrid Mamba prefix caching align mode vs off "
                    "(Nemotron-3.5-Lightning NVFP4, 4x GB200 DP4/EP4, "
                    "8K-in/1K-out, median of 6 paired rounds). Total "
                    "throughput: PC off "
                    f"{val(rows,'vllm-60008-4xgb200-pcoff-c1','tps')} (c=1), "
                    f"{val(rows,'vllm-60008-4xgb200-pcoff-c8','tps')} (c=8), "
                    f"{val(rows,'vllm-60008-4xgb200-pcoff-c32','tps')} (c=32), "
                    f"{val(rows,'vllm-60008-4xgb200-pcoff-c64','tps')} (c=64); "
                    "PC on "
                    f"{val(rows,'vllm-60008-4xgb200-pcon-c1','tps')} (c=1), "
                    f"{val(rows,'vllm-60008-4xgb200-pcon-c8','tps')} (c=8), "
                    f"{val(rows,'vllm-60008-4xgb200-pcon-c32','tps')} (c=32), "
                    f"{val(rows,'vllm-60008-4xgb200-pcon-c64','tps')} (c=64) "
                    "tok/s. Align mode costs 13-24% throughput but is "
                    "required for correct Mamba state alignment.")
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
        if (venue, issue) == ("llama.cpp", "10879"):
            if hw == "AMD Custom GPU 0932":
                ids = sorted(rows)
                off = next(i for i in ids if i.endswith("fa0"))
                on = next(i for i in ids if i.endswith("fa1"))
                return ("Flash-attention A/B on a Steam Deck iGPU (AMD "
                        "Custom GPU 0932, VANGOGH, 4 GiB shared memory), "
                        "llama-b10360, -ngl 100, llama-bench pp512/tg128. "
                        "fa=0 -> fa=1: decode "
                        f"{val(rows,off,'tps')} -> {val(rows,on,'tps')} "
                        f"tok/s ({pct(rows,off,on,'tps'):+.1f}%), prefill "
                        f"{val(rows,off,'pp_tps')} -> "
                        f"{val(rows,on,'pp_tps')} tok/s "
                        f"({pct(rows,off,on,'pp_tps'):+.1f}%). Across the "
                        "reporter's 12-model matrix fa is worth up to "
                        "+14% prefill and +7% decode, sometimes costs a "
                        "point or two, and is a wash on the 3B-31B "
                        "IQ2_XXS quants; the effect is model-dependent, "
                        "not free.")
            if model == "Qwen3.6-35B-A3B-APEX-MTP-I-Balanced":
                bare = next(i for i in rows if i.endswith("-bare"))
                mtp = next(i for i in rows if i.endswith("-mtp"))
                return ("Vulkan vs ROCm on the same Radeon 8060S Strix "
                        "Halo iGPU (llama.cpp master 2026-08, "
                        "single-request chat decode, tok/s). This arm is "
                        f"{'ROCm' if 'rocm' in bare else 'Vulkan'}: bare "
                        f"{val(rows,bare,'tps')} -> with MTP "
                        f"{val(rows,mtp,'tps')} "
                        f"({pct(rows,bare,mtp,'tps'):+.1f}%). Cross-backend: "
                        "bare ROCm 56.41 vs Vulkan 66.86 (+18.5% Vulkan); "
                        "with MTP ROCm 69.47 vs Vulkan 80.89 (+16.4%). The "
                        "sibling MoE entry (Hy-MT2-30B-A3B, Q6_K) shows the "
                        "widest bare gap: ROCm 59.19 vs Vulkan 74.28 "
                        "(+25.5%). Reporter's pick on this UMA iGPU "
                        "(~230 GB/s measured): Vulkan + MTP.")
            if model == "Qwopus3.6-27B-Coder-Compat-MTP":
                bare = next(i for i in rows if i.endswith("-bare"))
                mtp = next(i for i in rows if i.endswith("-mtp"))
                return ("Vulkan vs ROCm on the same Radeon 8060S Strix "
                        "Halo iGPU, dense 27B coder Q5_K_M, "
                        "single-request chat decode, tok/s. This arm is "
                        f"{'ROCm' if 'rocm' in bare else 'Vulkan'}: bare "
                        f"{val(rows,bare,'tps')} -> with MTP "
                        f"{val(rows,mtp,'tps')} "
                        f"({pct(rows,bare,mtp,'tps'):+.1f}%). Cross-backend: "
                        "bare ROCm 10.94 vs Vulkan 11.23 (+2.6%, near "
                        "parity); with MTP ROCm 19.38 vs Vulkan 22.38 "
                        "(+15.5%). MTP nearly doubles both backends; the "
                        "backend gap only shows up once speculation is on.")
            if hw == "RX 6800":
                off = next(i for i in rows if i.endswith("fa0"))
                on = next(i for i in rows if i.endswith("fa1"))
                return ("Flash-attention A/B on a desktop RX 6800 under "
                        "Vulkan (Mesa RADV 26.2.2 with RADV_PERFTEST=nogttspill, "
                        "build f1cee99, -ngl 100). fa=0 -> fa=1: decode "
                        f"{val(rows,off,'tps')} -> {val(rows,on,'tps')} tok/s "
                        f"({pct(rows,off,on,'tps'):+.1f}%), prefill "
                        f"{val(rows,off,'pp_tps')} -> "
                        f"{val(rows,on,'pp_tps')} tok/s "
                        f"({pct(rows,off,on,'pp_tps'):+.1f}%). Reporter: vs the "
                        "older scoreboard entry (build 4b385bf) tg128 is up 6% "
                        "(no FA) and 10% (FA) while pp512 is down 6-9%. On the "
                        "same card ROCm gets pp512 1510/1739 and tg128 "
                        "86.0/93.6 (no FA/FA): Vulkan generates ~18% faster on "
                        "RDNA2, ROCm only wins prefill with FA on.")
            if hw == "Radeon RX 9060 XT":
                off = next(i for i in rows if i.endswith("fa0"))
                on = next(i for i in rows if i.endswith("fa1"))
                return ("Flash-attention A/B on a Radeon RX 9060 XT "
                        "(16 GB, 128-bit, gfx1200) under Vulkan (Mesa RADV "
                        "26.2.2, RADV_PERFTEST=nogttspill, build f1cee99, "
                        "-ngl 100, Ryzen 5 7600X). fa=0 -> fa=1: decode "
                        f"{val(rows,off,'tps')} -> {val(rows,on,'tps')} "
                        f"tok/s ({pct(rows,off,on,'tps'):+.1f}%), prefill "
                        f"{val(rows,off,'pp_tps')} -> "
                        f"{val(rows,on,'pp_tps')} tok/s "
                        f"({pct(rows,off,on,'pp_tps'):+.1f}%). Same card on "
                        "ROCm 7.2.4 (same commit, -ngl 99): fa=0->fa=1 pp512 "
                        "2641.07->3014.51, tg128 67.27->70.18; Vulkan is still "
                        "ahead on RDNA4 for both (decode 74.01 vs 70.18, "
                        "prefill 3228.15 vs 3014.51). Larger models on the "
                        "same card (-ngl 99 -fa 1, pp512/tg128, Vulkan/HIP): "
                        "gpt-oss-20b MXFP4 3464/105.8 vs 3372/92.8, Qwen3.8-27B "
                        "UD-IQ4_XS 709/20.1 vs 738/19.5, Gemma 4 12B Q4_K_M "
                        "1509/39.0 vs 1467/37.6. Reporter notes the 128-bit "
                        "bus (not 256-bit) and a big build-over-build prefill "
                        "gain vs the older scoreboard entry (ed52f36).")
            if hw == "Arc(TM) B390":
                s0 = next(i for i in rows if i.endswith("fa0-short"))
                s1 = next(i for i in rows if i.endswith("fa1-short"))
                l0 = next(i for i in rows if i.endswith("fa0-long"))
                l1 = next(i for i in rows if i.endswith("fa1-long"))
                return ("Flash attention on an Arc B390 (Vulkan, coopmat, "
                        "build b10903). Short context: fa=0 -> fa=1 prefill "
                        f"{val(rows,s0,'pp_tps')} -> {val(rows,s1,'pp_tps')} "
                        f"tok/s ({pct(rows,s0,s1,'pp_tps'):+.1f}%), decode "
                        f"{val(rows,s0,'tps')} -> {val(rows,s1,'tps')} tok/s "
                        f"({pct(rows,s0,s1,'tps'):+.1f}%). Long context "
                        "(pp8192/tg2048): prefill "
                        f"{val(rows,l0,'pp_tps')} -> {val(rows,l1,'pp_tps')} "
                        f"tok/s ({pct(rows,l0,l1,'pp_tps'):+.1f}%), decode "
                        f"{val(rows,l0,'tps')} -> {val(rows,l1,'tps')} tok/s "
                        f"({pct(rows,l0,l1,'tps'):+.1f}%). FA costs little at "
                        "512 tokens but collapses prefill by more than half at "
                        "8192 on this chip; decode is flat either way.")
            if hw == "Arc(TM) 140V":
                off = next(i for i in rows if i.endswith("fa0"))
                on = next(i for i in rows if i.endswith("fa1"))
                return ("Flash-attention A/B on a Lunar Lake Arc 140V iGPU "
                        "(Vulkan, coopmat, build b10941, -ngl -1). fa=0 -> "
                        f"fa=1: prefill {val(rows,off,'pp_tps')} -> "
                        f"{val(rows,on,'pp_tps')} tok/s "
                        f"({pct(rows,off,on,'pp_tps'):+.1f}%), decode "
                        f"{val(rows,off,'tps')} -> {val(rows,on,'tps')} tok/s "
                        f"({pct(rows,off,on,'tps'):+.1f}%). FA is roughly "
                        "neutral here; the reporter notes the big xe2 prefill "
                        "jump came earlier, from coopmat matrix cores, not FA.")
            if model == "Qwen3.8-27B-AD":
                bare = next(i for i in rows if i.endswith("-bare"))
                mtp = next(i for i in rows if i.endswith("-mtp"))
                return ("Vulkan vs ROCm on the same Radeon 8060S Strix "
                        "Halo iGPU, dense 27B Q5_K_M, single-request chat "
                        "decode, tok/s. This arm is "
                        f"{'ROCm' if 'rocm' in bare else 'Vulkan'}: bare "
                        f"{val(rows,bare,'tps')} -> with MTP "
                        f"{val(rows,mtp,'tps')} "
                        f"({pct(rows,bare,mtp,'tps'):+.1f}%). Cross-backend: "
                        "bare ROCm 10.52 vs Vulkan 10.76 (+2.3%); with MTP "
                        "ROCm 14.09 vs Vulkan 16.98 (+20.5%). Same pattern "
                        "as the sibling 27B: bare backends at parity, MTP "
                        "widens the gap.")
        if (venue, issue) == ("llama.cpp", "15021"):
            if hw == "RX 6800":
                off = next(i for i in rows if i.endswith("fa0"))
                on = next(i for i in rows if i.endswith("fa1"))
                return ("Flash-attention A/B on a desktop RX 6800 under ROCm "
                        "7.2.4 (gfx1030, build f1cee99, -ngl 99). fa=0 -> "
                        f"fa=1: prefill {val(rows,off,'pp_tps')} -> "
                        f"{val(rows,on,'pp_tps')} tok/s "
                        f"({pct(rows,off,on,'pp_tps'):+.1f}%), decode "
                        f"{val(rows,off,'tps')} -> {val(rows,on,'tps')} tok/s "
                        f"({pct(rows,off,on,'tps'):+.1f}%). Cross-backend on "
                        "the same card and commit: Vulkan (RADV 26.2.2) gets "
                        "pp512 1594/1598 and tg128 101.5/106.5 (no FA/FA), so "
                        "Vulkan still leads generation on RDNA2 while ROCm "
                        "only wins prefill with FA on.")
            if hw == "Radeon RX 9060 XT":
                off = next(i for i in rows if i.endswith("fa0"))
                on = next(i for i in rows if i.endswith("fa1"))
                return ("Flash-attention A/B on a Radeon RX 9060 XT "
                        "(16 GB, 128-bit, gfx1200) under ROCm 7.2.4 (build "
                        "f1cee99, -DGGML_HIP=ON -DGPU_TARGETS=gfx1200, -ngl "
                        "99, Ryzen 5 7600X). fa=0 -> fa=1: prefill "
                        f"{val(rows,off,'pp_tps')} -> "
                        f"{val(rows,on,'pp_tps')} tok/s "
                        f"({pct(rows,off,on,'pp_tps'):+.1f}%), decode "
                        f"{val(rows,off,'tps')} -> {val(rows,on,'tps')} tok/s "
                        f"({pct(rows,off,on,'tps'):+.1f}%). Same card on Vulkan "
                        "(RADV 26.2.2, RADV_PERFTEST=nogttspill, -ngl 100): "
                        "fa=0->fa=1 pp512 2844.80->3228.15, tg128 71.07->74.01, "
                        "so Vulkan is still ahead on both for this RDNA4 card. "
                        "Reporter: vs the older scoreboard entry (a0e13dc) "
                        "pp512 is up 86% (no FA) and 104% (FA), tg128 level "
                        "(no FA) and up 7% (FA); the card has a 128-bit bus, "
                        "not 256-bit.")
            if hw == "Radeon AI PRO R9700":
                ids = list(rows)
                fa0 = next(i for i in ids if i.endswith("fa0"))
                fa1 = next(i for i in ids if i.endswith("fa1"))
                p8 = next(i for i in ids if i.endswith("pp8192"))
                is_rocm = "rocm" in fa0
                if is_rocm:
                    return ("ROCm (TheRock 10.1, gfx1201) on an R9700, "
                            f"llama.cpp 8ea2902. fa=0 -> fa=1: prefill "
                            f"{val(rows,fa0,'pp_tps')} -> "
                            f"{val(rows,fa1,'pp_tps')} tok/s "
                            f"({pct(rows,fa0,fa1,'pp_tps'):+.1f}%), decode "
                            f"{val(rows,fa0,'tps')} -> {val(rows,fa1,'tps')} "
                            f"tok/s ({pct(rows,fa0,fa1,'tps'):+.1f}%). ROCm "
                            "falls off hard with prompt length: pp512 "
                            f"{val(rows,fa1,'pp_tps')} -> pp8192 "
                            f"{val(rows,p8,'pp_tps')} tok/s "
                            f"({pct(rows,fa1,p8,'pp_tps'):+.1f}%). Reporter: "
                            "at pp512 the backends are 8% apart, by pp8192 "
                            "54% (Vulkan 4235.87 at pp8192).")
                return ("Vulkan (Mesa RADV 26.1.8) on an R9700, llama.cpp "
                        f"8ea2902. fa=0 -> fa=1: prefill "
                        f"{val(rows,fa0,'pp_tps'):g} -> "
                        f"{val(rows,fa1,'pp_tps'):g} tok/s "
                        f"({pct(rows,fa0,fa1,'pp_tps'):+.1f}%), decode "
                        f"{val(rows,fa0,'tps'):g} -> {val(rows,fa1,'tps'):g} tok/s "
                        f"({pct(rows,fa0,fa1,'tps'):+.1f}%). Vulkan is steady "
                        "with prompt length: pp512 "
                        f"{val(rows,fa1,'pp_tps')} -> pp8192 "
                        f"{val(rows,p8,'pp_tps')} tok/s "
                        f"({pct(rows,fa1,p8,'pp_tps'):+.1f}%), so at pp8192 "
                        "Vulkan is +54% over ROCm (2755.01) while at pp512 "
                        "they are within 8%. Decode also favors Vulkan "
                        "(~+8%). Reporter notes the ordering inverts on MoE "
                        "models (ROCm +8.5% at 57k ctx on a 35B-A3B).")
            if hw == "V620":
                off = next(i for i in rows if i.endswith("fa0"))
                on = next(i for i in rows if i.endswith("fa1"))
                return ("AMD Radeon Pro V620 (gfx1030, 32 GB) on ROCm v10, "
                        "llama.cpp 434ddbbc0 (10884), llama 7B Q4_0, single "
                        f"card. fa=0 -> fa=1: prefill {val(rows,off,'pp_tps'):g} -> "
                        f"{val(rows,on,'pp_tps'):g} tok/s "
                        f"({pct(rows,off,on,'pp_tps'):+.1f}%), decode "
                        f"{val(rows,off,'tps'):g} -> {val(rows,on,'tps'):g} tok/s "
                        f"({pct(rows,off,on,'tps'):+.1f}%). The second card is a "
                        "near-identical replicate (pp512 1819.51, tg128 "
                        "91.48/98.44). Cross-config: running both V620s in "
                        "parallel keeps prefill flat (2146.36 vs 2173.13, "
                        "-1.2%) but decode falls to 71.38 tok/s (-27.7%), so a "
                        "second 32 GB card costs rather than helps a 3.56 GiB "
                        "model that already fits on one.")
            if hw == "2x V620":
                off = next(i for i in rows if i.endswith("fa0"))
                on = next(i for i in rows if i.endswith("fa1"))
                return ("Two V620 (gfx1030) in parallel on ROCm v10, "
                        "llama.cpp 434ddbbc0 (10884), llama 7B Q4_0. fa=0 -> "
                        f"fa=1: prefill {val(rows,off,'pp_tps'):g} -> "
                        f"{val(rows,on,'pp_tps'):g} tok/s "
                        f"({pct(rows,off,on,'pp_tps'):+.1f}%), decode "
                        f"{val(rows,off,'tps'):g} -> {val(rows,on,'tps'):g} tok/s "
                        f"({pct(rows,off,on,'tps'):+.1f}%). Versus the single "
                        "card (2173.13 prefill / 98.78 decode at fa=1), the "
                        "dual setup holds prefill (-1.2%) but loses ~28% of "
                        "decode (71.38 vs 98.78): tensor-parallel sync over "
                        "PCIe, not extra bandwidth, is the bottleneck for a "
                        "model that fits on one card.")
        if (venue, issue) == ("llama.cpp", "15013"):
            off5 = "lc-disc-15013-c18693775-fa0"
            on5 = "lc-disc-15013-c18693775-fa1"
            off10 = "lc-disc-15013-c18695871-fa0"
            on10 = "lc-disc-15013-c18695871-fa1"
            return ("P102-100 mining card (Pascal GP104, no display) on "
                    "llama.cpp CUDA b11312, llama 7B Q4_0. fa=0 -> fa=1 on the "
                    "stock 5 GB BIOS: prefill "
                    f"{val(rows,off5,'pp_tps'):g} -> {val(rows,on5,'pp_tps'):g} tok/s "
                    f"({pct(rows,off5,on5,'pp_tps'):+.1f}%), decode "
                    f"{val(rows,off5,'tps'):g} -> {val(rows,on5,'tps'):g} tok/s "
                    f"({pct(rows,off5,on5,'tps'):+.1f}%). A BIOS mod doubles the "
                    "reported VRAM to 10 GB: prefill "
                    f"{val(rows,off10,'pp_tps'):g} -> {val(rows,on10,'pp_tps'):g}, "
                    "decode "
                    f"{val(rows,off10,'tps'):g} -> {val(rows,on10,'tps'):g} tok/s "
                    f"({pct(rows,off10,on10,'tps'):+.1f}%). Doubling VRAM barely "
                    "moves speed (within ~1%): the 3.56 GiB model fits in either.")
        if (venue, issue) == ("llama.cpp", "4167"):
            if hw == "M5 Ultra":
                f16 = next(i for i in rows if i.endswith("quant-f16"))
                q8 = next(i for i in rows if i.endswith("quant-q8_0"))
                q4 = next(i for i in rows if i.endswith("quant-q4_0"))
                return ("llama.cpp 0.3.0 Metal quant ladder on an M5 Ultra "
                        "(36 CPU / 80 GPU cores, 256 GB). Decode F16 -> Q8_0 -> "
                        f"Q4_0: {val(rows,f16,'tps')} -> {val(rows,q8,'tps')} "
                        f"-> {val(rows,q4,'tps')} tok/s "
                        f"({val(rows,q4,'tps')/val(rows,f16,'tps'):.1f}x F16), "
                        "while prefill barely moves: "
                        f"{val(rows,f16,'pp_tps')} -> {val(rows,q8,'pp_tps')} "
                        f"-> {val(rows,q4,'pp_tps')} tok/s. Decode is "
                        "bandwidth-bound (scales with bytes), prefill is "
                        "compute-bound on this chip.")
            if hw == "M6":
                f16 = next(i for i in rows if i.endswith("quant-f16"))
                q8 = next(i for i in rows if i.endswith("quant-q8_0"))
                q4 = next(i for i in rows if i.endswith("quant-q4_0"))
                return ("llama.cpp b11312 Metal quant ladder on a Mac mini M6 "
                        "(12-core GPU, 32 GB, reporter quotes ~170 GB/s). "
                        "Decode F16 -> Q8_0 -> Q4_0: "
                        f"{val(rows,f16,'tps')} -> {val(rows,q8,'tps')} -> "
                        f"{val(rows,q4,'tps')} tok/s "
                        f"({val(rows,q4,'tps')/val(rows,f16,'tps'):.1f}x F16); "
                        "prefill is flat across quants "
                        f"({val(rows,f16,'pp_tps')} -> "
                        f"{val(rows,q4,'pp_tps')} tok/s). Same "
                        "bandwidth-decode / compute-prefill split as the M5 "
                        "Ultra, at a much smaller absolute rate.")
            if model == "Qwen3.8-27B":
                mp = "lc-disc-4167-c18555918-"
                return ("Qwen3.8-27B dense IQ3_S on M2 Max (30 GPU, 32 GB) "
                        "Metal, llama.cpp. Plain bench: pp4096 "
                        f"{val(rows,mp+'q38-27b','pp_tps'):g} / tg128 "
                        f"{val(rows,mp+'q38-27b','tps'):g} tok/s. "
                        "DFlash2 speculative decoding (xsn/dflash2 branch, "
                        "--spec-draft-n-max 7) vs plain, 256-token "
                        "generations: code "
                        f"{val(rows,'lc-disc-4167-c18631101-code-off','tps')} "
                        "-> "
                        f"{val(rows,'lc-disc-4167-c18631101-code-dflash','tps')} "
                        f"tok/s "
                        f"({pct(rows,'lc-disc-4167-c18631101-code-off','lc-disc-4167-c18631101-code-dflash','tps'):+.1f}%); "
                        "math "
                        f"{val(rows,'lc-disc-4167-c18631101-math-off','tps')} -> "
                        f"{val(rows,'lc-disc-4167-c18631101-math-dflash','tps')} "
                        f"({pct(rows,'lc-disc-4167-c18631101-math-off','lc-disc-4167-c18631101-math-dflash','tps'):+.1f}%); "
                        "prose "
                        f"{val(rows,'lc-disc-4167-c18631101-prose-off','tps')} -> "
                        f"{val(rows,'lc-disc-4167-c18631101-prose-dflash','tps')} "
                        f"({pct(rows,'lc-disc-4167-c18631101-prose-off','lc-disc-4167-c18631101-prose-dflash','tps'):+.1f}%) "
                        "- spec decode loses on every prompt type despite 76% "
                        "acceptance. MTP (--spec-type draft-mtp, 32k window, "
                        "q8_0 KV, ollama) is also a net loss on this chip and "
                        "degrades monotonically with draft depth: no-draft "
                        f"{val(rows,mp+'mtp-nodraft','tps'):g} -> n=2 "
                        f"{val(rows,mp+'mtp-n2','tps'):g} -> n=4 "
                        f"{val(rows,mp+'mtp-n4','tps'):g} -> n=6 "
                        f"{val(rows,mp+'mtp-n6','tps'):g} -> n=8 "
                        f"{val(rows,mp+'mtp-n8','tps'):g} tok/s.")
            if model == "Qwen3.6-35B-A3B":
                return ("DFlash2 spec decode on the same M2 Max, MoE 35B-A3B "
                        "IQ3_S (only 3B active per token). Code: "
                        f"{val(rows,'lc-disc-4167-c18631101-code-off','tps')} "
                        "-> "
                        f"{val(rows,'lc-disc-4167-c18631101-code-dflash','tps')} "
                        f"tok/s "
                        f"({pct(rows,'lc-disc-4167-c18631101-code-off','lc-disc-4167-c18631101-code-dflash','tps'):+.1f}%); "
                        "math "
                        f"{val(rows,'lc-disc-4167-c18631101-math-off','tps')} -> "
                        f"{val(rows,'lc-disc-4167-c18631101-math-dflash','tps')} "
                        f"({pct(rows,'lc-disc-4167-c18631101-math-off','lc-disc-4167-c18631101-math-dflash','tps'):+.1f}%); "
                        "prose "
                        f"{val(rows,'lc-disc-4167-c18631101-prose-off','tps')} -> "
                        f"{val(rows,'lc-disc-4167-c18631101-prose-dflash','tps')} "
                        f"({pct(rows,'lc-disc-4167-c18631101-prose-off','lc-disc-4167-c18631101-prose-dflash','tps'):+.1f}%). "
                        "The MoE loses harder than the dense 27B: the target "
                        "step is cheap precisely because few params are "
                        "active, so a ~1B drafter eats a larger share of what "
                        "it saves (reporter's analysis).")
        if (venue, issue) == ("llama.cpp", "27593"):
            return ("SYCL tuning sweep on one Arc Pro B70 (BMG G31, 32 GB), "
                    "Qwen3.8-27B Q8_0, master 63b64a50a, oneAPI 2026.1. The "
                    f"headline is a build flag: -DGGML_SYCL_F16 OFF -> ON takes "
                    f"pp2048 {val(rows,'lc-disc-27593-f16-off','pp_tps'):g} -> "
                    f"{val(rows,'lc-disc-27593-f16-on','pp_tps'):g} tok/s (3.72x) "
                    "with tg128 flat (15.80 -> 15.79); the flag is OFF in the "
                    "CMake default. MTP sweep (--spec-type draft-mtp, the model's "
                    "own MTP layer): short 22-token answers 15.73 -> 50.92 tok/s "
                    "(3.2x at n-max 6), long 512-token answers peak at 33.53 "
                    "(n-max 3, 2.1x); draft acceptance falls 0.87 -> 0.40 across "
                    "the sweep, so the optimum draft length differs by answer "
                    "length. Micro-batch: -ub 512 -> 2048 is +34.8% prefill "
                    "(1074.8 -> 1448.7), -b makes no difference once >= -ub, "
                    "-ub 4096 adds ~+2% at pp8192. -fa 1 is +6% at 2048 / +9% "
                    "at 8192, generation flat. KV cache: f16 reaches 49152 "
                    "context at 1115.7 tok/s, q8_0 65536 at 1032.6, q4_0 the "
                    "full 131072 at 795.3; tg128 is 15.79/15.72/15.69 across "
                    "f16/q8_0/q4_0 at short context (deep-context decode not "
                    "measured here). Env vars: GGML_SYCL_ENABLE_OPT=0 costs 68% "
                    "of generation (15.79 -> 5.07) though it is the documented "
                    "corruption workaround for #21893; SYCL_UR_USE_LEVEL_ZERO_V2=0 "
                    "is +1.4% generation for free; GGML_SYCL_FA_ONEDNN=0 trades "
                    "-5% prefill for +3% generation (16.59 combined with L0 v2). "
                    "Repeated runs land within ~+-1% on prefill, so smaller "
                    "moves are noise. Separately, comment 18692471 (Qwen3.8-27B-"
                    "UD-Q4_K_XL, n_slots 4, ctx 262144, KV q8_0, MTP k=3) "
                    f"reports PP 1149.66 tok/s on the single card vs 855.54 "
                    "with the tensor split across two B70s over PCIe gen4 x16 "
                    "(-25.6%); both fall to ~668-870 by 64k tokens.")
        if (venue, issue) == ("llama.cpp", "23313") and hw == "Arc Pro B70":
            if model == "llama 7B":
                return ("llama 7B Q4_0, fa A/B, on an Arc Pro B70 passed "
                        "through to a Proxmox VM (Xeon E5-2699 v4, 64 GB "
                        "DDR4), SYCL F16 build. fa 0 -> 1: prefill "
                        f"{val(rows,'lc-disc-23313-c18467211-llama7b-fa0','pp_tps'):g} -> "
                        f"{val(rows,'lc-disc-23313-c18467211-llama7b-fa1','pp_tps'):g} "
                        "tok/s (2.47x), generation "
                        f"{val(rows,'lc-disc-23313-c18467211-llama7b-fa0','tps')} -> "
                        f"{val(rows,'lc-disc-23313-c18467211-llama7b-fa1','tps')} "
                        "(+3.8%). FA is worth more than 2x prefill on this "
                        "card at 512 tokens; the VM overhead is unmeasured "
                        "(no bare-metal numbers from the same post).")
            if model == "Qwen3.8-27B":
                return ("qwen35 27B Q6_K, latest SYCL, n_ubatch 1024. "
                        "Prompt-depth decay at fixed pp2048/tg256: "
                        f"{val(rows,'lc-disc-23313-c18629941-d0','pp_tps'):g} / "
                        f"{val(rows,'lc-disc-23313-c18629941-d0','tps')} at no "
                        "depth, "
                        f"{val(rows,'lc-disc-23313-c18629941-d8192','pp_tps'):g} / "
                        f"{val(rows,'lc-disc-23313-c18629941-d8192','tps')} at "
                        "d8192, "
                        f"{val(rows,'lc-disc-23313-c18629941-d16384','pp_tps'):g} / "
                        f"{val(rows,'lc-disc-23313-c18629941-d16384','tps')} at "
                        "d16384. The mtp-bench rows are multi-token-prediction "
                        "spec decode per prompt type: code_python 40.9 tok/s "
                        "(acceptance 0.936) down to long_code_review 28.0 "
                        "(0.653); throughput tracks acceptance, and even the "
                        "best cell is ~1.9x the 21.32 bare tg256.")
        if (venue, issue) == ("llama.cpp", "23313") and hw == "Arc A770":
            off = next(i for i in rows if i.endswith("fa0"))
            on = next(i for i in rows if i.endswith("fa1"))
            return ("Intel Arc A770, i7-13700K, Ubuntu 24.04, 64 GB DDR5, "
                    "llama.cpp 2cdae802e (10714), SYCL, llama 7B Q4_0, "
                    "-ctk f16 -ctv f16. fa=0 -> fa=1: prefill "
                    f"{val(rows,off,'pp_tps'):g} -> {val(rows,on,'pp_tps'):g} "
                    "tok/s "
                    f"({pct(rows,off,on,'pp_tps'):+.1f}%), decode "
                    f"{val(rows,off,'tps'):g} -> {val(rows,on,'tps'):g} tok/s "
                    f"({pct(rows,off,on,'tps'):+.1f}%). FA helps both, decode "
                    "more than prefill here (the opposite of the B70, where "
                    "FA was 2.47x on prefill).")
        if (venue, issue) == ("HF", "?") and hw == "M4 Pro" and model == "Ternary-Bonsai-2-27B":
            return ("DFlash2 drafter quants on Metal (PrismML fork, 32k window, "
                    "bench5.py): plain decode without a drafter is fastest at "
                    f"{val(rows,'hf-schiltmans-ft5-none','tps')} tok/s - the "
                    "fork's Metal DFlash2 path is slower than no drafter at all. "
                    "Among drafters, ft5 Q8_0 reaches "
                    f"{val(rows,'hf-schiltmans-ft5-ft5-q80','tps')} tok/s "
                    "(acceptance 0.432) vs "
                    f"{val(rows,'hf-schiltmans-ft5-stock-q80','tps')} tok/s for the "
                    "stock z-lab Q8_0 (0.395); ft5 Q4_K_M keeps nearly all of it at "
                    "56% of the size and Q2_K matches the stock acceptance at a "
                    "third. CUDA is the intended platform; the author has not "
                    "measured these GGUFs there.")
        if (venue, issue) == ("HF", "?") and model == "Qwen3.8-Flash-Next" and hw == "Radeon 8060S":
            return ("Sakura K352 expert-pruned Qwen3.8-Flash-Next variants on one "
                    "64 GB Strix Halo, 32k ctx, KV q8_0. With the shared MTP head "
                    "(danielhanchen qwen4exp/mtp fork) the ISTA-Darwin-R3 3-bit cut "
                    f"reaches {val(rows,'hf-webmp3-istadarwin3b-mtp','tps')} tok/s "
                    f"decode / {val(rows,'hf-webmp3-istadarwin3b-mtp','pp_tps')} "
                    "prefill, slightly under the Swift 1.5 cut's 34.5 tok/s; "
                    "without speculation on official b11259 the plain ISTA 3-bit "
                    "cut decodes at 22.7 tok/s. ROCm collapses on the 3-bit files "
                    "(~31 GiB resident > dedicated carve-out) but holds 21.6 tok/s "
                    "on the 2.5-bit cut. See the Sakura-Qwen3.8-Flash-Next-Swift "
                    "rows for the full MTP n-max and -b sweep.")
        if (venue, issue) == ("HF", "?"):
            if hw == "M4 Max (128 GB)" and model == "Qwen3.8-Flash-Next":
                return ("mlx-serve 26.8.11 on M4 Max 128 GB, ~75 GB resident, "
                        "mixed 4-bit experts / 8-bit rest pack: serial decode "
                        f"{val(rows,'hf-ddalcu-q38fn-mlx-serial','tps')} tok/s, "
                        "the native MTP head (lossless, opt-in) "
                        f"{val(rows,'hf-ddalcu-q38fn-mlx-mtp','tps')} tok/s "
                        f"({pct(rows,'hf-ddalcu-q38fn-mlx-serial','hf-ddalcu-q38fn-mlx-mtp','tps'):+.0f}%; "
                        "+41% on code, a few percent slower on prose), "
                        f"prefill ~{val(rows,'hf-ddalcu-q38fn-mlx-prefill','pp_tps')} tok/s; "
                        "a 24.8k-token needle stays recovered with sparse "
                        "attention. The card points to a re-quantized iQ-MLX "
                        "4.7 bpw successor pack, kept here as the measured "
                        "mixed 4/8-bit baseline.")
            if hw == "M4 Pro (48 GB)" and model == "Qwen3.6-27B-AEON-Ultimate-Uncensored":
                return ("AEON-7 Qwen3.6-27B merge on M4 Pro 48 GB, mlx-vlm: the "
                        "compact mxfp4 build decodes "
                        f"{val(rows,'hf-aeon7-fp4-text','tps')} tok/s at "
                        f"17 GB; the 8-bit max-fidelity build "
                        f"{val(rows,'hf-aeon7-8bit-text','tps')} tok/s at "
                        "29.85 GB. The native qwen3_5_mtp drafter (lossless, "
                        "verified) is the real win: block size 3 hits "
                        f"{val(rows,'hf-aeon7-fp4-mtp-bs3','tps')} tok/s (1.78x, "
                        "94.7% draft accept) versus "
                        f"{val(rows,'hf-aeon7-fp4-mtp-bs2','tps')} at bs=2 and "
                        f"{val(rows,'hf-aeon7-fp4-mtp-bs4','tps')} at bs=4 "
                        "(accept rate collapses to 86.9%). Per-category at bs=3: "
                        f"{val(rows,'hf-aeon7-fp4-mtp3-chat','tps')} tok/s on chat "
                        "(67.1% accept) to "
                        f"{val(rows,'hf-aeon7-fp4-mtp3-math','tps')} on math "
                        "(90.1%); the per-category baselines are flat 14.7-15.3 "
                        "tok/s, so decode is bandwidth bound, not compute bound.")
            if hw == "M5 Ultra" and model == "Swift 1.5 Qwen3.8-Flash-Next":
                return ("mlx-serve 26.10.1 with the calibrated 4.7 bpw "
                        "mixed-precision pack (4-bit experts, 8-bit spine, 32 GB "
                        "n-gram table memory-mapped, pooled n-gram prefetch) "
                        "versus the Swift llama.cpp IQ3_XXS build on the same "
                        "M5 Ultra 96 GB Mac Studio, ctx 179200: prefill 25k "
                        f"{val(rows,'hf-dankpaws-swift15-mlx-pp25k','pp_tps')} vs "
                        f"{val(rows,'hf-dankpaws-swift15-ic3-pp25k','pp_tps')} "
                        "tok/s, 95k "
                        f"{val(rows,'hf-dankpaws-swift15-mlx-pp95k','pp_tps')} vs "
                        f"{val(rows,'hf-dankpaws-swift15-ic3-pp95k','pp_tps')}; "
                        "decode after 4k "
                        f"{val(rows,'hf-dankpaws-swift15-mlx-d4k','tps')} vs "
                        f"{val(rows,'hf-dankpaws-swift15-ic3-d4k','tps')}, after "
                        "95k "
                        f"{val(rows,'hf-dankpaws-swift15-mlx-d95k','tps')} vs "
                        f"{val(rows,'hf-dankpaws-swift15-ic3-d95k','tps')} tok/s. "
                        "Top-1 agreement with Swift BF16 is 91.0% for the pack "
                        "versus 84.1% for IQ3_XXS.")
            if hw == "Radeon 8060S" and model == "Sakura-Qwen3.8-Flash-Next-Swift":
                return ("Expert-pruned Qwen3.8-Flash-Next cuts on one 64 GB Strix "
                        "Halo (webmp3 cards, 32k ctx, KV q8_0). The shared MTP "
                        "sidecar (fork build) lifts IQ3_XXS decode "
                        f"{val(rows,'hf-sakura-swift3-iq3xxs-official','tps')} -> "
                        f"{val(rows,'hf-sakura-swift3-iq3xxs-mtp2-b2048','tps')} tok/s "
                        f"({pct(rows,'hf-sakura-swift3-iq3xxs-official','hf-sakura-swift3-iq3xxs-mtp2-b2048','tps'):+.0f}%) "
                        "and IQ2_XS "
                        f"{val(rows,'hf-sakura-swift25-iq2xs-official','tps')} -> "
                        f"{val(rows,'hf-sakura-swift25-iq2xs-mtp2-b2048','tps')} tok/s "
                        f"({pct(rows,'hf-sakura-swift25-iq2xs-official','hf-sakura-swift25-iq2xs-mtp2-b2048','tps'):+.0f}%). "
                        "The 2.5-bit IQ2_XS cut decodes faster than IQ3_XXS with MTP "
                        f"({val(rows,'hf-sakura-swift25-iq2xs-mtp2-b2048','tps')} vs "
                        f"{val(rows,'hf-sakura-swift3-iq3xxs-mtp2-b2048','tps')} tok/s) "
                        "because its ~26 GiB of resident weights fit the dedicated "
                        "GPU carve-out; on ROCm the IQ3_XXS file collapses to about 5 "
                        "tok/s while IQ2_XS still does "
                        "21.6 tok/s decode / 322 tok/s prefill. "
                        "n-max 3 never beats n-max 2.")
            if hw == "Radeon 8060S" and model == "MiMo-V2.6-Flash-MOPD-P160":
                return ("MiMo SSD Streaming on a 64 GB Strix Halo: middle-layer "
                        "experts run from RAM (~20 GiB), NVMe backing. Context "
                        f"16k {val(rows,'hf-mimo-mopd160-iq2xs-ctx16k','tps')} (range "
                        "9-10.5), 24k "
                        f"{val(rows,'hf-mimo-mopd160-iq2xs-ctx24k','tps')} (range "
                        "6.6-7.4), 32k with expert lock "
                        f"{val(rows,'hf-mimo-mopd160-iq2xs-ctx32k-lock','tps')} tok/s "
                        "(range 5.6-7.7): KV and GPU buffers spill into shared RAM "
                        "and starve the CPU-side experts. The ubatch sweep is a "
                        "decode/prefill trade: ub512 "
                        f"{val(rows,'hf-mimo-mopd160-iq2xs-ub512','tps')} decode / "
                        f"{val(rows,'hf-mimo-mopd160-iq2xs-ub512','pp_tps')} prefill -> "
                        f"ub1024 {val(rows,'hf-mimo-mopd160-iq2xs-ub1024','tps')} / "
                        f"{val(rows,'hf-mimo-mopd160-iq2xs-ub1024','pp_tps')} tok/s "
                        f"({pct(rows,'hf-mimo-mopd160-iq2xs-ub512','hf-mimo-mopd160-iq2xs-ub1024','tps'):+.0f}% "
                        "decode for +76% prefill); ub4096 OOMs. The full 512-expert "
                        "model on the same machine pages from NVMe at 2.6 tok/s "
                        "(separate record).")
            if (hw == "Radeon AI PRO R9700" and model == "Qwen3.8-Flash-Next"
                    and backend == "ranma.cpp (ROCm)"):
                return ("ranma.cpp keeps routed experts in host RAM and streams them "
                        "over PCIe, so the RAM tier is a first-class variable. TG128 "
                        f"warm-cache decode: 3.05 bpw {val(rows,'hf-ranma-r9700-128gb-bench-305','tps')} "
                        f"(128 GB) vs {val(rows,'hf-ranma-r9700-64gb-bench-305','tps')} tok/s (64 GB); "
                        f"4.05 bpw {val(rows,'hf-ranma-r9700-128gb-bench-405','tps')} vs "
                        f"{val(rows,'hf-ranma-r9700-64gb-bench-405','tps')} tok/s: halving "
                        "the host RAM pool costs about 2 percent at 3.05 bpw and 4 "
                        "percent at 4.05 bpw; the VRAM expert "
                        "cache absorbs the difference. MTP smart decode beats plain "
                        f"decode on every arm: 3.05 bpw {val(rows,'hf-ranma-r9700-128gb-bench-305','tps')} -> "
                        f"{val(rows,'hf-ranma-r9700-128gb-mtp-305','tps')} tok/s "
                        f"({pct(rows,'hf-ranma-r9700-128gb-bench-305','hf-ranma-r9700-128gb-mtp-305','tps'):+.0f}% "
                        "at the low end of the published preset range). MTP narrows the "
                        "quant gap: at 4.05 bpw the MTP arms are within about 1 percent "
                        "of each other across RAM tiers.")
            if hw == "RX 9070 XT (emulated)" and model == "Qwen3.8-Flash-Next":
                return ("Not a real RX 9070 XT: the author emulates a 16 GiB card by "
                        "limiting the R9700's expert cache to its budget. TG128 warm "
                        f"decode {val(rows,'hf-ranma-9070xt-emul-64gb-bench-305','tps')} "
                        f"(3.05 bpw) / {val(rows,'hf-ranma-9070xt-emul-64gb-bench-405','tps')} tok/s "
                        "(4.05 bpw), about 18-22 percent below the real R9700 at the "
                        "same 64 GB tier. MTP "
                        f"still helps but less at 4.05 bpw: {val(rows,'hf-ranma-9070xt-emul-64gb-mtp-405','tps')} "
                        "tok/s low end (range 29.1-30.8), under the 3.05 bpw arm's "
                        f"{val(rows,'hf-ranma-9070xt-emul-64gb-mtp-305','tps')} - a "
                        "tight expert cache punishes the bigger quant's bandwidth "
                        "demand even with speculation.")
            if hw == "Radeon 8060S" and model == "Tiel-Coder":
                return ("Strix Halo (Ryzen AI Max+ 395, 96 GiB unified): the ROCmFPX "
                        "engine with a ROCmFP4 requant beats stock llama.cpp on the "
                        "same battery. Effective generation speed "
                        f"{val(rows,'hf-tielcoder-8060s-stock-dflash','tps')} tok/s "
                        f"(stock + DFlash, UD-Q4_K_XL) -> "
                        f"{val(rows,'hf-tielcoder-8060s-fpx-dflash','tps')} tok/s "
                        f"(ROCmFPX + DFlash n4, ROCmFP4), "
                        f"{pct(rows,'hf-tielcoder-8060s-stock-dflash','hf-tielcoder-8060s-fpx-dflash','tps'):+.0f}%; "
                        "the native MTP head is slower than DFlash on the same file "
                        f"({val(rows,'hf-tielcoder-8060s-fpx-mtp','tps')} tok/s) but "
                        "scored 17/17 vs 16/17 (author: battery noise is about 3 "
                        "tasks, so treat that as noise). Plain decode via llama-swap "
                        "is published as a range, 117-125 tok/s. The ROCmFPX fork is "
                        "required to read the file; stock llama.cpp cannot load it.")
            if hw == "48 GB GPU" and model == "Agens-Volundr-32B-Preview":
                return ("Context decay on an unnamed 48 GB card (Q4_K_M, -ngl 99, FA): "
                        f"decode {val(rows,'hf-volundr-48gb-ctx1k','tps')} (1K) -> "
                        f"{val(rows,'hf-volundr-48gb-ctx8k','tps')} (8K) -> "
                        f"{val(rows,'hf-volundr-48gb-ctx32k','tps')} tok/s (32K), "
                        f"{pct(rows,'hf-volundr-48gb-ctx1k','hf-volundr-48gb-ctx32k','tps'):+.0f}% "
                        "1K to 32K. Prefill decays much harder: 2218 tok/s at 1K vs "
                        "about 620 tok/s at 32K because the model selects blocks per "
                        "prompt token. Card model is not stated on the card.")
            if hw == "RTX 4090 Laptop GPU" and model == "FrogNano-4B-2609":
                return ("TensorFold 0.6.3 CUDA engine, 4-bit MLX affine (group 64), "
                        "one RTX 4090 Laptop GPU (16 GB), greedy, thinking on. "
                        "Single-stream decode is "
                        f"{val(rows,'capyctl-frognano-tf-single','tps')} tok/s; the "
                        "--parallel 8 sweep scales aggregate throughput "
                        f"{val(rows,'capyctl-frognano-tf-c1','tps')} to "
                        f"{val(rows,'capyctl-frognano-tf-c8','tps')} tok/s from 1 to 8 "
                        f"streams ({pct(rows,'capyctl-frognano-tf-c1','capyctl-frognano-tf-c8','tps'):+.0f}% "
                        "aggregate), while per-stream throughput declines 50.6 to 40.3 "
                        "tok/s as the streams share the card. Decode holds about 49-50 "
                        "tok/s single-stream from 0.5k to 32k context; the BF16 vLLM "
                        "baseline runs 59.9 single-stream.")
            if hw == "2\u00d7 Quadro RTX 4000" and model == "rune-26b-a4b-v3":
                return ("Prompt processing (prefill) on 2x Quadro RTX 4000 8 GB, "
                        "llama.cpp 8212c78, 2k-token prompt, IQ3_M 26B MoE + q8_0 "
                        "KV cache. The update/buffer batch size is the lever: "
                        f"-ub 512 gives {val(rows,'livesport-rune26b-rtx4000-ub512','pp_tps')} "
                        f"vs -ub 256 {val(rows,'livesport-rune26b-rtx4000-ub256','pp_tps')} tok/s "
                        f"({pct(rows,'livesport-rune26b-rtx4000-ub256','livesport-rune26b-rtx4000-ub512','pp_tps'):+.0f}%). "
                        "The card's latency table (per-question seconds, KV-cache "
                        "reuse) is decode-side and is not mined here as tok/s.")
            if hw == "8 threads" and model == "Qwen3.8-Flash-Next":
                return ("CPU field note: a separate MTP head (--spec-type "
                        "draft-mtp) is a clear win on CPU for this 176B MoE "
                        "(pruned 512 -> 256 experts). Serial decode is "
                        f"{val(rows,'davidmg-qwen38flash-mtp-nospec','tps')} tok/s; "
                        "the unsloth 512-expert head gives "
                        f"{val(rows,'davidmg-qwen38flash-mtp-h512','tps')} "
                        f"({pct(rows,'davidmg-qwen38flash-mtp-nospec','davidmg-qwen38flash-mtp-h512','tps'):+.0f}%, "
                        "81.7% draft acceptance) and the pruned 256-expert head "
                        f"{val(rows,'davidmg-qwen38flash-mtp-h256','tps')} "
                        f"({pct(rows,'davidmg-qwen38flash-mtp-nospec','davidmg-qwen38flash-mtp-h256','tps'):+.0f}%, "
                        "74.8% acceptance). The card's GPU setup (2x 20 GB) shows "
                        "only a small code gain and a prose loss, so the CPU rows "
                        "are the clean win.")
            if hw == "2\u00d7 20 GB" and model == "Qwen3.8-Flash-Next":
                return ("GPU field note (2x 20 GB CUDA, 3-slot llama-server, KV "
                        "q5_1, one run per cell): the same MTP head helps code but "
                        "not German prose, and the size of both effects is n-max-"
                        "sensitive. No-head baseline is "
                        f"{val(rows,'davidmg-qwen38flash-gpu-nospec','tps')} tok/s for "
                        "both workloads (its context is not stated). At 3x64K the "
                        "256-head n-max 2 arm lifts code to "
                        f"{val(rows,'davidmg-qwen38flash-gpu-nmax2-code','tps')} "
                        f"({pct(rows,'davidmg-qwen38flash-gpu-nospec','davidmg-qwen38flash-gpu-nmax2-code','tps'):+.0f}% vs baseline) "
                        f"but prose falls to {val(rows,'davidmg-qwen38flash-gpu-nmax2-prose','tps')} "
                        f"({pct(rows,'davidmg-qwen38flash-gpu-nospec','davidmg-qwen38flash-gpu-nmax2-prose','tps'):+.0f}%); "
                        "n-max 3 pushes code highest "
                        f"({val(rows,'davidmg-qwen38flash-gpu-nmax3-code','tps')}, "
                        f"{pct(rows,'davidmg-qwen38flash-gpu-nospec','davidmg-qwen38flash-gpu-nmax3-code','tps'):+.0f}%) "
                        "but is unstable (CUDA OOM under three parallel 54k prompts), "
                        "and p-min 0.6 at n-max 3 drops prose hardest "
                        f"({val(rows,'davidmg-qwen38flash-gpu-nmax3pmin-prose','tps')}, "
                        f"{pct(rows,'davidmg-qwen38flash-gpu-nospec','davidmg-qwen38flash-gpu-nmax3pmin-prose','tps'):+.0f}%). "
                        "Author flags every cell as a single-run indication, not a "
                        "benchmark; the CPU section of this card is the cleaner MTP "
                        "win.")
            if hw == "Radeon 8065S" and model == "GLM-5.3-Flash":
                return ("GLM-5.3-Flash (320.8B MoE) Q5K-IQ3S mix on a Gorgon Halo "
                        "(Radeon 8065S, 192 GB) with the ROCmFPX Vulkan build. "
                        "Context-depth decay at fixed pp2048: prefill "
                        f"{val(rows,'hf3-glm53flash-8065s-pp2048','pp_tps')} drops to "
                        f"{val(rows,'hf3-glm53flash-8065s-pp2048-d32k','pp_tps')} at "
                        "32K context, decode "
                        f"{val(rows,'hf3-glm53flash-8065s-tg','tps')} to "
                        f"{val(rows,'hf3-glm53flash-8065s-tg-d32k','tps')} tok/s. "
                        "Plain llama.cpp master runs the file at the same decode "
                        "speed but slower prefill.")
            if hw == "10\u00d7 MI100" and model == "GLM-5.3-Flash":
                return ("e-waste edition of GLM-5.3-Flash (321B/18B MoE, "
                        "glm5-next arch) on 10x MI100 (gfx908), llama.cpp fork, "
                        "ROCm, llama-bench -p 2048 -n 128, no spec decode, -fa off. "
                        "Quant-width comparison (not a before/after): Q4_K_XL "
                        f"{val(rows,'hf3-glm53flash-mi100-q4kxl','pp_tps')} prefill / "
                        f"{val(rows,'hf3-glm53flash-mi100-q4kxl','tps')} decode vs Q3_K_M "
                        f"{val(rows,'hf3-glm53flash-mi100-q3km','pp_tps')} / "
                        f"{val(rows,'hf3-glm53flash-mi100-q3km','tps')} t/s. "
                        "The card: 3-bit is not faster than 4-bit on this GPU class "
                        "because K-quant dequantization, not bandwidth, is the decode "
                        "bottleneck (why the e-waste editions drop i-quants).")
            if hw == "Radeon 8065S" and model == "MiMo-V2.6-Flash-RL":
                return ("MiMo-V2.6-Flash-RL-UNCENSORED (309.8B MoE) at "
                        "4.29 bpw (MXFP4 experts, Q5_K attention/dense/MTP) "
                        "on a Gorgon Halo (Radeon 8065S, 192 GB), ROCmFPX "
                        "main Vulkan build with the fused gate/up expert "
                        "tensors (from PR #33), full GPU offload. "
                        "Context-depth decay: prefill "
                        f"{val(rows,'hf3-mimov26flashrl-8065s-pp2048','pp_tps')} -> "
                        f"{val(rows,'hf3-mimov26flashrl-8065s-pp2048-d32k','pp_tps')} at "
                        "32K context, decode "
                        f"{val(rows,'hf3-mimov26flashrl-8065s-tg','tps')} -> "
                        f"{val(rows,'hf3-mimov26flashrl-8065s-tg-d32k','tps')} tok/s.")
            if hw == "RTX 3090" and model == "Qwen3.8-27B":
                return ("Three PAW editions of Qwen3.8-27B on one RTX 3090, "
                        "llama-paw CUDA fork, 262144-token context. "
                        "X3.1 (3.5 bpw): the DFlash2 drafter is the speed "
                        "story, coding "
                        f"{val(rows,'hf3-qwen3827b-paw-3090-coding-draft','tps')} vs "
                        f"{val(rows,'hf3-qwen3827b-paw-3090-nodraft','tps')} no-drafter "
                        f"({pct(rows,'hf3-qwen3827b-paw-3090-nodraft','hf3-qwen3827b-paw-3090-coding-draft','tps'):+.0f}%), "
                        f"new code {val(rows,'hf3-qwen3827b-paw-3090-newcode-draft','tps')}; "
                        "prompt "
                        f"{val(rows,'hf3-qwen3827b-paw-3090-pp-short','pp_tps')} short, "
                        f"{val(rows,'hf3-qwen3827b-paw-3090-pp-8k','pp_tps')} at 8k. "
                        "PAW-27B (~2.17 bpw): the MTP drafter lifts short-context "
                        f"decode to {val(rows,'hf3-qwen3827b-paw27b-mtpshort','tps')} from "
                        f"{val(rows,'hf3-qwen3827b-paw27b-nodraft','tps')} no-drafter "
                        f"({pct(rows,'hf3-qwen3827b-paw27b-nodraft','hf3-qwen3827b-paw27b-mtpshort','tps'):+.0f}%), "
                        f"falling to {val(rows,'hf3-qwen3827b-paw27b-mtp191k','tps')} at 191k. "
                        "X3 (3.5 bpw): prompt "
                        f"{val(rows,'hf3-qwen3827b-pawx3-pp512','pp_tps')} at 512, "
                        f"{val(rows,'hf3-qwen3827b-pawx3-pp8192','pp_tps')} at 8k, "
                        f"{val(rows,'hf3-qwen3827b-pawx3-pp211k','pp_tps')} at 211k; "
                        "decode "
                        f"{val(rows,'hf3-qwen3827b-pawx3-tg128','tps')} at tg128, "
                        f"{val(rows,'hf3-qwen3827b-pawx3-tg211k','tps')} at 211k depth; "
                        "verified spec decode "
                        f"{val(rows,'hf3-qwen3827b-pawx3-spec8k','tps')} at 8k code context.")
            if hw == "RTX 5090" and model == "Qwen3.8-27B":
                return ("akopytko Blackwell-native NVFP4 (no per-tensor scales, "
                        "quant-time MSE scale search) on one RTX 5090 (stock 575 W), "
                        "current llama.cpp, default flags -b 2048 -ub 512. "
                        f"tg128 decode {val(rows,'hf5-qwen3827b-nvfp4-5090-default','tps')} / "
                        f"pp2048 prefill {val(rows,'hf5-qwen3827b-nvfp4-5090-default','pp_tps')}; "
                        "the embedded MTP draft head (--spec-type draft-mtp, n-max 8, "
                        f"p-min 0.8) lifts decode to {val(rows,'hf5-qwen3827b-nvfp4-5090-mtp','tps')} "
                        f"tok/s ({pct(rows,'hf5-qwen3827b-nvfp4-5090-default','hf5-qwen3827b-nvfp4-5090-mtp','tps'):+.0f}% "
                        "at 0.75 draft acceptance). The card's unsloth NVFP4 reference "
                        "runs 87.69 tg128 / 6018.71 pp2048 on the same card, so the "
                        "edge over it is on prefill, not decode.")
            if hw == "H200 NVL" and model == "Qwen3.8-27B":
                return ("Qui-Linta13 IQ2_M fused MTP on H200 NVL, -ngl 99, "
                        "flash attention, F16 KV, 256 gen tokens, median of 3. "
                        f"Baseline (no spec-decode, prose) "
                        f"{val(rows,'hf6-qui-linta13-iq2m-baseline','tps')} tok/s. "
                        "MTP n_max 2 on code gives "
                        f"{val(rows,'hf6-qui-linta13-iq2m-mtp-n2','tps')} tok/s "
                        f"({pct(rows,'hf6-qui-linta13-iq2m-baseline','hf6-qui-linta13-iq2m-mtp-n2','tps'):+.0f}%). "
                        "Split noMTP-IQ2_M + draft-Q8_0 (n_max 2, prose) reaches "
                        f"{val(rows,'hf6-qui-linta13-iq2m-split-draft','tps')} tok/s "
                        f"({pct(rows,'hf6-qui-linta13-iq2m-baseline','hf6-qui-linta13-iq2m-split-draft','tps'):+.0f}%). "
                        "Spec-decode gain varies by prompt type (code > prose > chat).")
            if hw == "RTX 3090" and model == "Qwen3.6-35B-A3B":
                return ("PAW 1.54 bpw trellis of Qwen3.6-35B-A3B on a single "
                        "RTX 3090, llama.cpp CUDA. Decode by workload: mixed "
                        f"{val(rows,'hf3-qwen3635b-paw3090-mixed','tps')} tok/s, "
                        f"code {val(rows,'hf3-qwen3635b-paw3090-code','tps')} tok/s "
                        f"({pct(rows,'hf3-qwen3635b-paw3090-mixed','hf3-qwen3635b-paw3090-code','tps'):+.0f}%). "
                        "Not a before/after: two workloads on the same quant.")
            if hw == "Radeon AI PRO R9700" and model == "Qwen3.8-Flash-Next":
                return ("Gyro rotor quantization on one R9700 with the agentionai "
                        "llama.cpp Vulkan build: llama-bench batch 1, "
                        f"pp512 {val(rows,'hf3-qwen38flashnext-gyro-r9700-1x','pp_tps')} / "
                        f"tg128 {val(rows,'hf3-qwen38flashnext-gyro-r9700-1x','tps')} tok/s. "
                        "With the MTP draft (agentionai draft-mtp flags, n-max 6), "
                        "code generation reaches "
                        f"{val(rows,'hf3-qwen38flashnext-gyro-r9700-mtp-code-on','tps')} tok/s.")
            if hw == "Radeon AI PRO R9700" and model == "Swift 1.5":
                return ("MXFP4 GGUF of the Swift-1.5 fine-tune of Qwen3.8 27b "
                        "(MTP layer kept), base MXFP4 with 3 output-head "
                        "variants, llama.cpp b11214 ROCm on the R9700. MTP "
                        "(n-max 3) is a clear win over plain decode on every "
                        "variant, e.g. variant A "
                        f"{val(rows,'hf3-swift15-r9700-a-plain','tps')} -> "
                        f"{val(rows,'hf3-swift15-r9700-a-mtp','tps')} "
                        f"({pct(rows,'hf3-swift15-r9700-a-plain','hf3-swift15-r9700-a-mtp','tps'):+.0f}%); "
                        "2k prefill "
                        f"{val(rows,'hf3-swift15-r9700-a-plain','pp_tps')} tok/s. "
                        "The head variant matters little: the Q4_K-head build C "
                        "is fastest for both plain "
                        f"({val(rows,'hf3-swift15-r9700-c-plain','tps')}) and MTP "
                        f"({val(rows,'hf3-swift15-r9700-c-mtp','tps')}), the "
                        "Q8_0-head B slowest (plain "
                        f"{val(rows,'hf3-swift15-r9700-b-plain','tps')}, MTP "
                        f"{val(rows,'hf3-swift15-r9700-b-mtp','tps')} tok/s).")
            if hw == "Radeon AI PRO R9700" and model == "Ornith-1.5-35B-A3B":
                return ("MXFP4 GGUF of the Ornith-1.5-35B-A3B MoE (~35B total "
                        "/ ~3B active, MTP layer kept), llama.cpp b11214 ROCm "
                        "on the R9700. These are the llama.cpp baseline numbers "
                        "from a WHIRL-vs-llama.cpp comparison (the card's focus "
                        "is WHIRL, which leads 1.4-2.8x). llama.cpp plain "
                        "decode is ~107-120 tok/s by workload (CLI tg256 "
                        f"{val(rows,'hf3-ornith15-35b-r9700-cli256','tps')}, "
                        "800-token Chinese coding "
                        f"{val(rows,'hf3-ornith15-35b-r9700-zh800','tps')}, "
                        "after a 16k context "
                        f"{val(rows,'hf3-ornith15-35b-r9700-ctx16k','tps')}); "
                        "the file-editing workload is fastest with "
                        "draft-mtp,ngram-mod n-max 1 "
                        f"({val(rows,'hf3-ornith15-35b-r9700-fileedit','tps')} "
                        "tok/s); 4 concurrent requests aggregate to "
                        f"{val(rows,'hf3-ornith15-35b-r9700-conc4','tps')} "
                        f"tok/s. Prefill at 131k tokens (-ub 2048) is "
                        f"{val(rows,'hf3-ornith15-35b-r9700-pp131k','pp_tps')} "
                        "tok/s.")
            if hw == "RTX 5090" and model == "Qwen3.8-Flash-Next" and backend == "Strata":
                return ("Strata rc1 (all experts cached, greedy, MTP draft "
                        "always on) on RTX 5090. Gyro-S decode by content: "
                        f"prose {val(rows,'hf6-gyro-5090-strata-prose','tps')}, JSON "
                        f"{val(rows,'hf6-gyro-5090-strata-json','tps')}, code "
                        f"{val(rows,'hf6-gyro-5090-strata-code','tps')} tok/s; "
                        f"Gyro-M prose {val(rows,'hf6-gyro-5090-strata-gyrom-prose','tps')} tok/s. "
                        f"Prefill {val(rows,'hf6-gyro-5090-strata-prefill','pp_tps')} "
                        "tok/s on a 16k-token prompt. Strata is AgentionAI's "
                        "experimental runtime; MTP is always on, so these are "
                        "not directly comparable to the llama.cpp rows above.")
            if hw == "RTX 5090" and model == "Qwen3.8-Flash-Next":
                return ("Gyro-S on one RTX 5090 (Ryzen 9 9950X host) with the "
                        "agentionai CUDA kernels, llama.cpp fork main from "
                        "2026-10-04, decode tg128 or greedy content-type "
                        "prompts with the MTP draft. llama-bench batch 1: "
                        f"decode {val(rows,'hf6-gyro-5090-cuda-decode','tps')} "
                        f"(pp2048 ~{val(rows,'hf6-gyro-5090-cuda-decode','pp_tps')} "
                        "tok/s); with the MTP draft: JSON "
                        f"{val(rows,'hf6-gyro-5090-cuda-mtp-json','tps')}, "
                        f"code {val(rows,'hf6-gyro-5090-cuda-mtp-code','tps')}, "
                        f"copy {val(rows,'hf6-gyro-5090-cuda-mtp-copy','tps')} tok/s.")
            if hw == "RTX A6000" and model == "Qwen3.8-Flash-Next":
                return ("Gyro rotor quantization on RTX A6000 48 GB (CUDA, "
                        "agentionai/llama.cpp main). llama-bench batch 1: "
                        f"Gyro-S pp2048 {val(rows,'hf6-gyro-a6000-gyro-s','pp_tps')} / "
                        f"tg128 {val(rows,'hf6-gyro-a6000-gyro-s','tps')} tok/s; "
                        f"Gyro-M tg128 {val(rows,'hf6-gyro-a6000-gyro-m','tps')} tok/s. "
                        "Gyro-M trades a few percent decode for the smaller file.")
            if hw == "AMD Strix Halo" and model == "Qwen3.8-Flash-Next":
                return ("Gyro rotor quantization on AMD Strix Halo, agentionai "
                        "llama.cpp Vulkan build, batch 1 decode: Gyro-S "
                        f"{val(rows,'hf3-qwen38flashnext-gyro-8060s-gyros','tps')} tok/s, "
                        f"Gyro-M {val(rows,'hf3-qwen38flashnext-gyro-8060s-gyrom','tps')} tok/s. "
                        "With the MTP draft from the mtp- file: code "
                        f"{val(rows,'hf3-qwen38flashnext-gyro-8060s-mtp-code-on','tps')}, "
                        f"JSON {val(rows,'hf3-qwen38flashnext-gyro-8060s-mtp-json-on','tps')} "
                        "tok/s; drafting lifts both well above the no-draft "
                        "baseline.")
            if hw == "M4 Pro (48 GB)" and model == "Qwen3.8-27B":
                return ("AEON abliterated Qwen3.8-27B, 6-bit MLX (vision tower "
                        "preserved) on a Mac mini M4 Pro 48 GB (~273 GB/s), "
                        "mlx-vlm with the native MTP drafter. Serial decode "
                        f"{val(rows,'hf3-qwen3827b-aeon-mlx-serial','tps')} tok/s, "
                        f"~100% of the chip's streaming-bandwidth roofline. "
                        "MTP drafting raises it by workload: coding (block 4) "
                        f"{val(rows,'hf3-qwen3827b-aeon-mlx-coding','tps')}, "
                        f"document QA at 13k ctx (block 3) "
                        f"{val(rows,'hf3-qwen3827b-aeon-mlx-docqa','tps')}, "
                        f"creative prose (block 3) "
                        f"{val(rows,'hf3-qwen3827b-aeon-mlx-prose','tps')} tok/s; "
                        f"prefill ~{val(rows,'hf3-qwen3827b-aeon-mlx-prefill','pp_tps')}. "
                        "The card notes mlx-dspark with the DFlash2 drafter "
                        "decodes 15-19 tok/s at 24-27k context where the MTP "
                        "path measured 6-7.")
            if hw == "RTX PRO 6000 Blackwell Max-Q" and model == "Qwen3.8-27B-TURBO":
                return ("Concurrency sweep (scale_and_context.py, aggregate "
                        "tok/s) for Qwen3.8-27B TURBO NVFP4-W4A16 (modelopt FP4, "
                        "native MTP head n=1), vLLM 0.27.1 + GDN decode backport "
                        "(PR #41966), KV fp8, 262144 max ctx, single 96 GB Max-Q. "
                        "Throughput scales to a peak of "
                        f"{val(rows,'deluxetiky-qwen38turbo-vllm-c8','tps')} tok/s at "
                        "c8, then drops to "
                        f"{val(rows,'deluxetiky-qwen38turbo-vllm-c16','tps')} at c16 "
                        f"({pct(rows,'deluxetiky-qwen38turbo-vllm-c8','deluxetiky-qwen38turbo-vllm-c16','tps'):+.0f}%) "
                        "under the 160%-of-roofline over-subscription; c1 is "
                        f"{val(rows,'deluxetiky-qwen38turbo-vllm-c1','tps')} tok/s.")
            if hw == "RTX PRO 6000 Blackwell Max-Q" and model == "Agnes-3.0-Flash":
                return ("Concurrency sweep (scale_and_context.py, aggregate "
                        "tok/s) for Agnes-3.0-Flash BF16 (66.2 GB), SGLang 0.5.19 "
                        "+ checkpoint sglang_patch, NEXTN spec-decode (steps=3 "
                        "draft=4), KV fp8, 262144 max ctx, single 96 GB Max-Q. "
                        "Plateaus at "
                        f"{val(rows,'deluxetiky-agnes-sglang-c8','tps')} tok/s "
                        f"(c4 {val(rows,'deluxetiky-agnes-sglang-c4','tps')} to "
                        f"c8 {val(rows,'deluxetiky-agnes-sglang-c8','tps')}) and "
                        "collapses to "
                        f"{val(rows,'deluxetiky-agnes-sglang-c16','tps')} at c16 "
                        f"({pct(rows,'deluxetiky-agnes-sglang-c8','deluxetiky-agnes-sglang-c16','tps'):+.0f}%) "
                        "under over-subscription; c1 is "
                        f"{val(rows,'deluxetiky-agnes-sglang-c1','tps')} tok/s.")
            if hw == "M4 Max (64 GB)" and model == "ELYZA-Thinking-1.0-llm-jp-4-32b-a3b":
                return ("ELYZA-Thinking-1.0 (Japanese 4th-gen 32B MoE, 3B active), "
                        "4-bit MLX (group 64, 4.501 bpw), mlx-lm 0.32.0, Apple M4 "
                        "Max 64 GB, 4096 ctx, greedy. Two sample prompts, not a "
                        "sweep: the math prompt (reasoning_effort=medium) runs "
                        f"{val(rows,'rariruluis-elyza-m4max-medium','tps')} tok/s "
                        "and the code prompt (reasoning_effort=low) "
                        f"{val(rows,'rariruluis-elyza-m4max-low','tps')} tok/s "
                        f"({pct(rows,'rariruluis-elyza-m4max-medium','rariruluis-elyza-m4max-low','tps'):+.0f}%, "
                        "confounded by the different prompts); the author flags "
                        "both as small sanity checks, not a benchmark.")
            if hw == "MacBook Pro 128GB" and model == "Qwen3.8-27B":
                return ("MLX quant sweep of the MindMeld-AREX merge "
                        "(Qwen3.8-27B) on a 128 GB MacBook Pro (M-chip not "
                        "stated in the card). All five quantizations land "
                        "within a 4.4% band (204-213 tok/s): q8-hi tops it "
                        f"at {val(rows,'nightmedia-qwen38-27b-mac128-q8hi','tps')} tok/s, "
                        "the card's default mxfp8 runs "
                        f"{val(rows,'nightmedia-qwen38-27b-mac128-mxfp8','tps')} tok/s, "
                        "qx64-hi trails at "
                        f"{val(rows,'nightmedia-qwen38-27b-mac128-qx64hi','tps')} tok/s. "
                        "The real lever is memory: q8-hi needs 37.3 GB while "
                        "mxfp4 fits in 21.3 GB at "
                        f"{val(rows,'nightmedia-qwen38-27b-mac128-mxfp4','tps')} tok/s, "
                        "so the quant choice trades capacity for a sub-5% "
                        "speed difference.")
            if hw == "GB10" and model == "GLM-4.6":
                return ("GLM-4.6 (355B-A32B MoE) abliterated, IQ2_XXS+Q5_K mix "
                        "(2.26 bpw), llama.cpp CUDA on GB10 (DGX Spark, 128 GB). "
                        "MTP speculative decode vs no-spec at 32k ctx (q8_0 KV): "
                        f"no-spec {val(rows,'hf-promzeus-glm46-gb10-nospec','tps')} tok/s, "
                        "MTP n-max 2 "
                        f"{val(rows,'hf-promzeus-glm46-gb10-mtp2','tps')} "
                        f"({pct(rows,'hf-promzeus-glm46-gb10-nospec','hf-promzeus-glm46-gb10-mtp2','tps'):+.0f}%), "
                        "n-max 3 "
                        f"{val(rows,'hf-promzeus-glm46-gb10-mtp3','tps')} "
                        f"({pct(rows,'hf-promzeus-glm46-gb10-nospec','hf-promzeus-glm46-gb10-mtp3','tps'):+.0f}%). "
                        "N-max 1 at 113k ctx (q4_0 KV) hits "
                        f"{val(rows,'hf-promzeus-glm46-gb10-mtp1','tps')} tok/s "
                        "(80-94% draft acceptance). Depth decay: prefill "
                        f"{val(rows,'hf-promzeus-glm46-gb10-57k','pp_tps')} at 57.6k "
                        f"({val(rows,'hf-promzeus-glm46-gb10-57k','tps')} tok/s decode), "
                        f"{val(rows,'hf-promzeus-glm46-gb10-112k','pp_tps')} at 111.9k "
                        f"({val(rows,'hf-promzeus-glm46-gb10-112k','tps')} tok/s MTP decode).")
            if hw == "10× MI100" and model == "GLM-5.3-Flash":
                return ("Q3_K_M vs Q4_K_XL on 10x MI100 (ROCm, llama.cpp fork). "
                        "llama-bench pp2048/tg128, no spec decode, FA off. "
                        f"Q3_K_M: pp {val(rows,'hf-glm53-flash-10xmi100-q3km','pp_tps')}, "
                        f"tg {val(rows,'hf-glm53-flash-10xmi100-q3km','tps')} tok/s. "
                        f"Q4_K_XL: pp {val(rows,'hf-glm53-flash-10xmi100-q4kxl','pp_tps')}, "
                        f"tg {val(rows,'hf-glm53-flash-10xmi100-q4kxl','tps')} tok/s. "
                        "Q4_K_XL is slightly faster on both axes despite larger size.")
            if hw == "2× 20 GB" and model == "Qwen3.8-Flash-Next":
                return ("MTP draft-mtp speculative decoding sweep on 2x RTX 2080 Ti "
                        "(2x 20 GB, CUDA). No-spec baseline "
                        f"{val(rows,'hf-qwen38flashnext-2x20gb-nospec','tps')} tok/s. "
                        "Prose: n_max 1 "
                        f"{val(rows,'hf-qwen38flashnext-2x20gb-nmax1-prose','tps')}, "
                        f"n_max 2 {val(rows,'hf-qwen38flashnext-2x20gb-nmax2-prose','tps')}, "
                        f"n_max 3 {val(rows,'hf-qwen38flashnext-2x20gb-nmax3-prose','tps')}, "
                        f"n_max 3 + pmin {val(rows,'hf-qwen38flashnext-2x20gb-nmax3pmin-prose','tps')} tok/s. "
                        "Code: n_max 1 "
                        f"{val(rows,'hf-qwen38flashnext-2x20gb-nmax1-code','tps')}, "
                        f"n_max 2 {val(rows,'hf-qwen38flashnext-2x20gb-nmax2-code','tps')}, "
                        f"n_max 3 {val(rows,'hf-qwen38flashnext-2x20gb-nmax3-code','tps')}, "
                        f"n_max 3 + pmin {val(rows,'hf-qwen38flashnext-2x20gb-nmax3pmin-code','tps')} tok/s. "
                        "Code benefits more from MTP than prose; pmin hurts both.")
            if hw == "GB10" and model == "Ornith-1.5-397B-A17B":
                return ("ik_llama.cpp DFlash drafter n_max sweep on GB10 (DGX Spark). "
                        f"n_max 0 (no spec) {val(rows,'hf-ornith15-397b-gb10-dflash-nmax0','tps')} tok/s. "
                        f"n_max 2 {val(rows,'hf-ornith15-397b-gb10-dflash-nmax2','tps')}, "
                        f"n_max 3 {val(rows,'hf-ornith15-397b-gb10-dflash-nmax3','tps')}, "
                        f"n_max 4 {val(rows,'hf-ornith15-397b-gb10-dflash-nmax4','tps')}, "
                        f"n_max 5 {val(rows,'hf-ornith15-397b-gb10-dflash-nmax5','tps')} tok/s. "
                        "n_max 4 is the sweet spot (+32% over no-spec); n_max 5 "
                        "regresses due to draft overhead exceeding acceptance gains.")
            if hw == "M5 Pro" and model == "Swift 1.5":
                return ("Splash (Metal) with DFlash2 on 48 GB M5 Pro MacBook Pro "
                        "(20 GPU cores), Q4/Q6/Q8 mixed quant. "
                        f"Code {val(rows,'hf-swift15-m5pro-code','tps')}, "
                        f"median {val(rows,'hf-swift15-m5pro-median','tps')}, "
                        f"thinking {val(rows,'hf-swift15-m5pro-thinking','tps')}, "
                        f"weighted {val(rows,'hf-swift15-m5pro-weighted','tps')} tok/s. "
                        "Code is ~2x the median; thinking tasks are the slowest.")
            if hw == "RTX 5090" and model == "Qwen3.6-35B-A3B":
                return ("Quant comparison on RTX 5090 (CUDA), llama-bench "
                        "pp512/tg128, custom per-tensor requantization. "
                        f"Q4_K_M: pp {val(rows,'hf-qwen36-35b-5090-q4km','pp_tps')}, "
                        f"tg {val(rows,'hf-qwen36-35b-5090-q4km','tps')} tok/s (fastest decode). "
                        f"NVFP4: pp {val(rows,'hf-qwen36-35b-5090-nvfp4','pp_tps')}, "
                        f"tg {val(rows,'hf-qwen36-35b-5090-nvfp4','tps')} (fastest prefill). "
                        f"Q4_blend2: pp {val(rows,'hf-qwen36-35b-5090-q4blend2','pp_tps')}, "
                        f"tg {val(rows,'hf-qwen36-35b-5090-q4blend2','tps')}. "
                        f"Q4_blend4: pp {val(rows,'hf-qwen36-35b-5090-q4blend4','pp_tps')}, "
                        f"tg {val(rows,'hf-qwen36-35b-5090-q4blend4','tps')}. "
                        f"Q4_blend5: pp {val(rows,'hf-qwen36-35b-5090-q4blend5','pp_tps')}, "
                        f"tg {val(rows,'hf-qwen36-35b-5090-q4blend5','tps')} tok/s. "
                        "Q4_K_M wins decode; NVFP4 wins prefill; blends trade between.")
        if (venue, issue) == ("llama.cpp", "29869"):
            return ("Metal has no tensor API on M1-M4, so the 2-16 row mat-muls "
                    "that speculative decoding issues ran the mat-vec kernels "
                    "and slowed per draft row; on master DFlash2 was at or "
                    "below serial. The PR's few-row MMA kernels reverse it: "
                    "DFlash2 decode goes "
                    f"{val(rows,'lc-29869-m3u-dflash-code-master','tps')} to "
                    f"{val(rows,'lc-29869-m3u-dflash-code-pr','tps')} tok/s on "
                    "code "
                    f"({pct(rows,'lc-29869-m3u-dflash-code-master','lc-29869-m3u-dflash-code-pr','tps'):+.0f}%) "
                    f"and {val(rows,'lc-29869-m3u-dflash-prose-master','tps')} "
                    "to "
                    f"{val(rows,'lc-29869-m3u-dflash-prose-pr','tps')} on "
                    "prose "
                    f"({pct(rows,'lc-29869-m3u-dflash-prose-master','lc-29869-m3u-dflash-prose-pr','tps'):+.0f}%), "
                    "while serial decode is flat "
                    f"({val(rows,'lc-29869-m3u-serial-code-master','tps')} to "
                    f"{val(rows,'lc-29869-m3u-serial-code-pr','tps')} code, "
                    f"{val(rows,'lc-29869-m3u-serial-prose-master','tps')} to "
                    f"{val(rows,'lc-29869-m3u-serial-prose-pr','tps')} prose) "
                    "and the serial llama-bench path does not regress "
                    f"(pp512 {val(rows,'lc-29869-m3u-bench-master','pp_tps')} "
                    f"to {val(rows,'lc-29869-m3u-bench-pr','pp_tps')}, "
                    f"tg128 {val(rows,'lc-29869-m3u-bench-master','tps')} to "
                    f"{val(rows,'lc-29869-m3u-bench-pr','tps')}).")
        if (venue, issue) == ("llama.cpp", "29882"):
            ids = list(rows.keys())
            def arm(fa, after):
                cands = [i for i in ids if ("-fa%d-" % fa) in i]
                return (next(i for i in cands if not i.endswith("b11369"))
                        if after else next(i for i in cands if i.endswith("b11369")))
            fb, fa2 = arm(0, False), arm(0, True)
            pp_b, pp_a = val(rows, fb, "pp_tps"), val(rows, fa2, "pp_tps")
            tg_b, tg_a = val(rows, fb, "tps"), val(rows, fa2, "tps")
            s = ("Vulkan rms-norm subgroup-reduction opt, before (build 11369) vs "
                 "after; fa0/fa1 = flash-attention off/on; ngl -1, r 5, Windows. ")
            if pp_b is not None:
                s += "fa0 prefill %s to %s tok/s (%+.1f%%)" % (pp_b, pp_a, (pp_a - pp_b) / pp_b * 100)
                s += (", decode %s to %s tok/s (%+.1f%%)" % (tg_b, tg_a, (tg_a - tg_b) / tg_b * 100)
                      if tg_b is not None else ".")
            return s
        if (venue, issue) == ("llama.cpp", "29884"):
            if hw == "Dimensity 9400":
                fast = val(rows, "lc-29884-d9400-armv8.6_1", "pp_tps")
                sel = val(rows, "lc-29884-d9400-armv9.0_1", "pp_tps")
                return ("CPU backend variant sweep, Dimensity 9400 (MT6991), "
                        "Android 16, Qwen3-Embedding-0.6B Q8_0, llama-bench -p 512 "
                        "-r 3, each variant run in isolation. The aarch64 score "
                        f"function selects armv9.0_1 ({sel:g} tok/s) but armv8.6_1 "
                        f"({fast:g} tok/s) is the fastest, roughly 2x faster; "
                        "armv9.2_1/2 are not loaded (no SME). All five measured "
                        "variants are listed.")
        if (venue, issue) == ("llama.cpp", "29887"):
            h = "4090" if hw == "RTX 4090" else "5090"
            m = "lc-29887-%s-master" % h
            pc = "lc-29887-%s-fitcache" % h
            fc = "lc-29887-%s-cmoecache" % h
            s = ("MoE expert GPU cache (port of qvac-fabric): host experts run "
                 "on the GPU with an LRU cache and only misses are uploaded; "
                 "small batches (<=32 tokens), larger batches bypass the cache. "
                 "Three arms, the master --fit baseline (no cache), a 6.4 GB "
                 "partial cache (--fit --moe-cache-mib 6544), and the full -cmoe "
                 "cache. SPEED-Bench qualitative decode goes %s to %s tok/s "
                 "(%+.0f%%) with the full cache (partial %s)" % (val(rows, m, "tps"),
                  val(rows, fc, "tps"), pct(rows, m, fc, "tps"), val(rows, pc, "tps")))
            if hw == "RTX 4090":
                s += ("; prompt processing dips as whole layers move to the "
                      "cache (pp2048 %d to %d)" % (val(rows, m, "pp_tps"),
                                                   val(rows, fc, "pp_tps")))
            return s + "."
        if (venue, issue) == ("llama.cpp", "29892"):
            p1 = "lc-29892-ub1024-parent"
            m1 = "lc-29892-ub1024-master"
            p2 = "lc-29892-ub2048-parent"
            m2 = "lc-29892-ub2048-master"
            return ("#29182 (vulkan: MOE-aware mat_mul_id tile selection) regressed "
                    f"pp2048 @ d48000 on RDNA4 (RX 9070 XT, Qwen3.6-35B-A3B IQ3_S, 256 "
                    f"experts top-8). At -ub 1024 prefill drops {val(rows,p1,'pp_tps'):g} to "
                    f"{val(rows,m1,'pp_tps'):g} tok/s ({pct(rows,p1,m1,'pp_tps'):+.1f}%) "
                    f"parent vs master; at -ub 2048 it is flat "
                    f"({val(rows,p2,'pp_tps'):g} to {val(rows,m2,'pp_tps'):g}, inside the "
                    f"+/-94-124 noise floor). Token generation is unaffected (107.3 vs "
                    f"107.1 t/s all-VRAM per the report); reverting restores 2145.6.")
        if (venue, issue) == ("llama.cpp", "29901"):
            b = "lc-29901-prod6000-base"
            p = "lc-29901-prod6000-pr"
            return ("cuda: tile the lightning indexer over keys and tokens for the "
                    f"4-head case (qwen4exp, port of the Vulkan shader). Prefill at "
                    f"128k ctx on RTX PRO 6000 goes {val(rows,b,'pp_tps'):g} to "
                    f"{val(rows,p,'pp_tps'):g} tok/s ({pct(rows,b,p,'pp_tps'):+.1f}%), "
                    f"TG unchanged; the indexer kernel itself is 2.5x faster "
                    f"(6.4 vs 16.4 ms at kv 65536, nb 2048) and drops from 9.6% to "
                    f"4.0% of GPU time in nsys.")
        if (venue, issue) == ("llama.cpp", "29910"):
            if hw == "MI50":
                m64 = "lc-29910-mi50-ub64-master"
                o64 = "lc-29910-mi50-ub64-optimized"
                m512 = "lc-29910-mi50-ub512-master"
                o512 = "lc-29910-mi50-ub512-optimized"
                return ("Q2_K mmq VGPR-spill fix (gentler unroll, drop an unneeded "
                        "temporary loop), pp2048 -b 2048 -r 10 on MI50 (gfx906, DP4A). "
                        "The spill count drops 164 to 0 and prefill climbs across the "
                        f"-ub sweep: ub64 {val(rows,m64,'pp_tps'):g} to "
                        f"{val(rows,o64,'pp_tps'):g} tok/s "
                        f"({pct(rows,m64,o64,'pp_tps'):+.0f}%), ub512 "
                        f"{val(rows,m512,'pp_tps'):g} to {val(rows,o512,'pp_tps'):g} "
                        f"({pct(rows,m512,o512,'pp_tps'):+.0f}%). Prefill-only A/B; "
                        "the full -ub 16-512 sweep is listed.")
            if hw == "gfx1152":
                m16 = "lc-29910-gfx1152-ub16-master"
                o16 = "lc-29910-gfx1152-ub16-optimized"
                m512 = "lc-29910-gfx1152-ub512-master"
                o512 = "lc-29910-gfx1152-ub512-optimized"
                return ("Q2_K mmq VGPR-spill fix (gentler unroll, drop an unneeded "
                        "temporary loop), pp2048 -b 2048 -r 10 on gfx1152 (RDNA 3.5, "
                        "MMA). Spills drop 1387 to 0, but the prefill gain is only at "
                        f"low -ub (ub16 {val(rows,m16,'pp_tps'):g} to "
                        f"{val(rows,o16,'pp_tps'):g}, {pct(rows,m16,o16,'pp_tps'):+.0f}%"
                        f"); at -ub 512 master and optimized are within noise "
                        f"({val(rows,m512,'pp_tps'):g} vs {val(rows,o512,'pp_tps'):g}). "
                        "Prefill-only A/B; the full -ub 16-512 sweep is listed.")
        if (venue, issue) == ("llama.cpp", "29911"):
            b1 = "lc-29911-3060-before-r1"
            a1 = "lc-29911-3060-after-r1"
            b2 = "lc-29911-3060-before-r2"
            a2 = "lc-29911-3060-after-r2"
            return ("MUL_MAT_ID with GGML_PREC_F32 on quantized weights was rejected "
                    "by CUDA/Vulkan, offloading every ffn_down_exps mul_mat_id to the "
                    "CPU and copying the full expert matrix VRAM->host per token. "
                    f"Interleaved A/B swapping only libggml-cuda.so on Mistral Small 4 "
                    f"(119B, IQ4_XS): decode {val(rows,b1,'tps')} to {val(rows,a1,'tps')} "
                    f"tok/s (run 1) and {val(rows,b2,'tps')} to {val(rows,a2,'tps')} "
                    f"(run 2), ~3.6x faster; the 570 MB D2H transfers drop 232 to 0 "
                    "and the output is byte-identical.")
        if (venue, issue) == ("llama.cpp", "29924"):
            if model == "Llama 3.1 8B":
                return ("N-gram spec decode at temp>0: drafts were silently "
                        "rejected after context truncation, forcing a fallback "
                        "to the base model. Llama 3.1 8B, 8 seeds, median t/s: "
                        f"pre-PR {val(rows,'lc-29924-l318b-ngram-prePR','tps')}, "
                        f"with bug {val(rows,'lc-29924-l318b-ngram-tot','tps')}, "
                        f"with fix {val(rows,'lc-29924-l318b-ngram-fix','tps')} "
                        f"(recovers {pct(rows,'lc-29924-l318b-ngram-tot','lc-29924-l318b-ngram-fix','tps'):.0f}% "
                        "of the pre-PR gap).")
            if model == "Qwen3.6-35B-A3B":
                return ("N-gram spec decode at temp>0 with MTP drafts: "
                        "truncation rejected all n-gram drafts, dropping "
                        "throughput to the no-spec baseline. Qwen3.6-35B-A3B, "
                        "8 seeds, median t/s: n-gram "
                        f"{val(rows,'lc-29924-q36-ngram-tot','tps')} -> "
                        f"{val(rows,'lc-29924-q36-ngram-fix','tps')} "
                        f"(+{pct(rows,'lc-29924-q36-ngram-tot','lc-29924-q36-ngram-fix','tps'):.0f}%), "
                        "MTP-1 "
                        f"{val(rows,'lc-29924-q36-ngram-mtp1-tot','tps')} -> "
                        f"{val(rows,'lc-29924-q36-ngram-mtp1-fix','tps')}, "
                        "MTP-2 "
                        f"{val(rows,'lc-29924-q36-ngram-mtp2-tot','tps')} -> "
                        f"{val(rows,'lc-29924-q36-ngram-mtp2-fix','tps')}, "
                        "MTP-prob "
                        f"{val(rows,'lc-29924-q36-ngram-mtpprob-tot','tps')} -> "
                        f"{val(rows,'lc-29924-q36-ngram-mtpprob-fix','tps')}.")
        if (venue, issue) == ("llama.cpp", "29875"):
            if hw == "AMD Ryzen 7 7735HS" and model == "Qwen2.5 3B":
                return ("Speculative decoding on CPU (llama.cpp issue #29875). Qwen2.5 3B "
                        "Q8_0 on AMD Ryzen 7 7735HS, two evaluation tasks (code, riddle), "
                        "static baseline vs pmin06/entropy15 draft thresholds. code: "
                        f"{val(rows,'lc-29875-ryzen-code-static','tps')} -> "
                        f"{val(rows,'lc-29875-ryzen-code-entropy15','tps')} tok/s "
                        f"({pct(rows,'lc-29875-ryzen-code-static','lc-29875-ryzen-code-entropy15','tps'):+.0f}%); "
                        "riddle: "
                        f"{val(rows,'lc-29875-ryzen-riddle-static','tps')} -> "
                        f"{val(rows,'lc-29875-ryzen-riddle-entropy15','tps')} tok/s "
                        f"({pct(rows,'lc-29875-ryzen-riddle-static','lc-29875-ryzen-riddle-entropy15','tps'):+.0f}%). "
                        "The entropy15 threshold is the best on both tasks; the sparser "
                        "riddle task benefits more from spec-decode than the code task.")
        if (venue, issue) == ("?", "?"):
            if hw == "M1 Pro" and model == "Qwen2.5 3B":
                return ("TurboQuant KV-cache quantization on an M1 Pro 16 GB, "
                        "Qwen2.5-3B-Instruct 4-bit MLX at 16K context, effective rate "
                        "(generated tokens over total request time, prefill included): "
                        f"FP16 KV {val(rows,'tq-m1pro-mlx-fp16kv','tps')} tok/s in "
                        "39.9 s wall vs Hybrid K5/V4 quantized KV "
                        f"{val(rows,'tq-m1pro-mlx-hybrid-kv','tps')} tok/s in 71.4 s "
                        f"wall ({pct(rows,'tq-m1pro-mlx-fp16kv','tq-m1pro-mlx-hybrid-kv','tps'):+.0f}%). "
                        "The quantized cache stores 435.6 MB vs 563.4 MB for FP16 "
                        "(1.29x, not the 4x a packed-bits formula predicts, because "
                        "mlx-optiq 0.0.1 stores one byte per element) and peaks "
                        "*higher* than FP16 (3245.4 vs 3076.8 MB) since dequantized "
                        "K/V returns float32. Dequantizing the full cache every step "
                        "in unfused MLX ops costs more than the smaller cache saves. "
                        "For reference the same page measured Ollama Q4_K_M GGUF at "
                        "37.5 tok/s decode-only (49.3 s wall), a different metric.")
            if hw == "GB10" and model == "GLM-4.6":
                return ("HF card promzeus/gh0stx-glm46-gb10-GGUF (GLM-4.6 355B MoE on GB10). "
                        "MTP speculative decoding: no-spec "
                        f"{val(rows,'hf-promzeus-glm46-gb10-nospec','tps')}, MTP nmax1 "
                        f"{val(rows,'hf-promzeus-glm46-gb10-mtp1','tps')} "
                        f"({pct(rows,'hf-promzeus-glm46-gb10-nospec','hf-promzeus-glm46-gb10-mtp1','tps'):+.0f}%), "
                        "nmax2 "
                        f"{val(rows,'hf-promzeus-glm46-gb10-mtp2','tps')}, nmax3 "
                        f"{val(rows,'hf-promzeus-glm46-gb10-mtp3','tps')} tok/s (nmax1 is the "
                        "best; longer drafts do not help). Context depth: "
                        f"{val(rows,'hf-promzeus-glm46-gb10-57k','tps')} @57k, "
                        f"{val(rows,'hf-promzeus-glm46-gb10-112k','tps')} @112k tok/s (the "
                        "355B MoE decays as context grows).")
        if (venue, issue) == ("llama.cpp", "29973"):
            if hw == "Threadripper PRO 3975WX" and model == "Qwen3.8-Flash-Next":
                return ("CPU-only Zen 2 workstation (32C/64T, AVX2, DDR4-2667 at "
                        "about 46.6 GB/s), Qwen3.8-Flash-Next 177B UD-Q3_K_XL. "
                        "Build matters more than any runtime knob: the same source "
                        "tag built with MinGW gcc 16.2.0 decodes "
                        f"{val(rows,'lc29973-tr-mingw-znver2','tps')} tok/s vs "
                        f"{val(rows,'lc29973-tr-msvc-b11160','tps')} tok/s under MSVC "
                        f"({pct(rows,'lc29973-tr-msvc-b11160','lc29973-tr-mingw-znver2','tps'):+.0f}%), "
                        "and the collapse is ISA-independent (znver2 and haswell "
                        "multi-variant builds land within 0.01 tok/s of each other), "
                        "pointing at gcc codegen in the MoE expert-gather decode path. "
                        "Even the release builds differ: the CUDA build used CPU-only "
                        f"beats the Vulkan build used CPU-only "
                        f"{val(rows,'lc29973-tr-relcuda-cpu','tps')} vs "
                        f"{val(rows,'lc29973-tr-relvulkan-cpu','tps')} tok/s decode. "
                        "On the server side, -tb 24 lifts long-prompt prefill to "
                        f"{val(rows,'lc29973-tr-t20-tb24-long','pp_tps')} tok/s "
                        f"({val(rows,'lc29973-tr-t16-long','pp_tps')} at -t 16), and "
                        "tuned MTP (--spec-draft-p-min 0.30) beats the default "
                        f"{val(rows,'lc29973-tr-spec-pmin030','tps')} vs "
                        f"{val(rows,'lc29973-tr-spec-pmin0','tps')} tok/s; ngram-mod "
                        "hybrid is worse than tuned MTP "
                        f"({val(rows,'lc29973-tr-spec-mtp-ngram','tps')} tok/s). "
                        "Decode peaks at -t 20 (6.83), SMT siblings hurt: -t 32 "
                        f"{val(rows,'lc29973-tr-t32','tps')}, 16-thread no-SMT masks "
                        f"{val(rows,'lc29973-tr-mask-nosmt','tps')}, full 32-core mask "
                        f"{val(rows,'lc29973-tr-mask-full','tps')} tok/s.")
        if (venue, issue) == ("llama.cpp", "29930"):
            if hw == "RTX 5070 + Ryzen 5 5600GT" and model == "Qwen3.8-Flash-Next":
                return ("Expert streaming on a 12 GB card with 32 GB DDR4-2400 over "
                        "PCIe Gen3: the author's hashyy setup (fixed Windows I/O "
                        "queue depth, one file handle per worker, page-locked hot "
                        "expert tier) lifts decode from roughly "
                        f"{val(rows,'lc29930-5070-inherited','tps')} tok/s on the "
                        f"inherited setup to about {val(rows,'lc29930-5070-streaming-bench','tps')} "
                        f"tok/s ({pct(rows,'lc29930-5070-inherited','lc29930-5070-streaming-bench','tps'):+.0f}%) "
                        "on the published benchmark. Real-work runs: 10.15 tok/s over "
                        "4892 tokens on a long coding prompt, 10.41 tok/s over 10k "
                        "tokens in a video-verified run, 14-15 tok/s in normal "
                        "conversation (stored low end). The author notes Strata would "
                        "not work here: it targets 64 GB+ RAM builds.")
        if (venue, issue) == ("llama.cpp", "24528"):
            if hw == "2x RTX 3090" and model == "Qwen3.8-Flash-Next":
                return ("Expert-caching fork shootout on 2x RTX 3090 (x8+x8) + Ryzen "
                        "9950X, 192 GB DDR5-3600, every row with MTP and per-branch "
                        "tuned parameters. thecodacus (expert cache + async prefetch + "
                        "CUDA-pinned host RAM) wins every matchup: "
                        f"{val(rows,'lc24528-3090-qwen-iq4xs-q80-q51-thecodacus','tps')} vs "
                        f"{val(rows,'lc24528-3090-qwen-iq4xs-q80-q51-upstream','tps')} tok/s at "
                        "IQ4_XS with q8_0/q5_1 KV "
                        f"({pct(rows,'lc24528-3090-qwen-iq4xs-q80-q51-upstream','lc24528-3090-qwen-iq4xs-q80-q51-thecodacus','tps'):+.0f}%), "
                        "and the gap widens as the weights get heavier: UD-Q6_K_XL with "
                        f"f16 KV {val(rows,'lc24528-3090-qwen-ud-q6kxl-f16-f16-thecodacus','tps')} vs "
                        f"{val(rows,'lc24528-3090-qwen-ud-q6kxl-f16-f16-upstream','tps')} tok/s "
                        "(+84%). The other forks split: TheTom lands below upstream at "
                        f"IQ4_XS/q8_0-q5_1 ({val(rows,'lc24528-3090-qwen-iq4xs-q80-q51-thetom','tps')} vs "
                        f"{val(rows,'lc24528-3090-qwen-iq4xs-q80-q51-upstream','tps')} tok/s) "
                        "and GenerelSchwerz collapses to "
                        f"{val(rows,'lc24528-3090-qwen-iq4xs-q80-q51-generelschwerz','tps')} tok/s "
                        "(an MTP regression the author flags). KV quant choice moves the "
                        "baseline more than the fork gap at some quants: upstream IQ4_XS "
                        "runs 26.8 tok/s with both q8_0/q5_1 and f16 KV but 27.3 with "
                        "q8_0/q8_0. Two later branches beat thecodacus at IQ4_XS: "
                        f"csantiago78's PR reaches {val(rows,'lc24528-3090-csantiago-493','tps')} "
                        f"tok/s at 3500 tokens ({val(rows,'lc24528-3090-csantiago-combined','tps')} "
                        "with the author's combined patch set, MTP not yet integrated), and "
                        f"simlu's branch holds {val(rows,'lc24528-3090-simlu-qwen-tg1000','tps')} "
                        f"tok/s at tg1000 ({val(rows,'lc24528-3090-simlu-qwen-tg500','tps')} at "
                        "tg500) on IQ4_XS-PLEQ4 at 1M context.")
            if hw == "2x RTX 3090" and model == "DeepSeek-V4-Flash":
                return ("Same 2x RTX 3090 rig, DeepSeek V4 Flash UD-Q8_K_XL (161 GB "
                        "incl DSpark) with DSpark MTP and q8_0 KV: the expert-cache "
                        "forks roughly double upstream decode at 65k context, "
                        f"{val(rows,'lc24528-3090-dsv4-c65535-leloch','tps')} tok/s (leloch) and "
                        f"{val(rows,'lc24528-3090-dsv4-c65535-thetom','tps')} tok/s (TheTom) vs "
                        f"{val(rows,'lc24528-3090-dsv4-c65535-upstream','tps')} tok/s upstream "
                        f"({pct(rows,'lc24528-3090-dsv4-c65535-upstream','lc24528-3090-dsv4-c65535-leloch','tps'):+.0f}% "
                        "for leloch). The advantage shrinks with context: at 1M the "
                        f"leloch edge is {val(rows,'lc24528-3090-dsv4-c1048576-leloch','tps')} vs "
                        f"{val(rows,'lc24528-3090-dsv4-c1048576-upstream','tps')} tok/s (+46%) "
                        "and TheTom falls to +29%. Upstream itself gets slightly faster "
                        "with a bigger context window here (6.88 to 7.53 tok/s), so the "
                        "forks lose ground while upstream gains none of it. simlu's "
                        f"newer branch matches the leader: {val(rows,'lc24528-3090-simlu-dsv4-tg500','tps')} "
                        f"tok/s at tg500 and {val(rows,'lc24528-3090-simlu-dsv4-tg1000','tps')} at "
                        "tg1000 (256k ctx), about level with leloch's 13.57 at 65k.")
            if hw == "2x RTX 3090" and model == "GLM-5.3-Flash":
                return ("simlu expert-cache branch on the 2x RTX 3090 rig, GLM-5.3-Flash "
                        f"Q4_K_M at 256k context with q8_0 KV and no draft model: "
                        f"{val(rows,'lc24528-3090-simlu-glm-tg500','tps')} tok/s at tg500 and "
                        f"{val(rows,'lc24528-3090-simlu-glm-tg1000','tps')} tok/s at tg1000. "
                        "Decode is flat to slightly up with generation length here, so "
                        "the expert cache is not thrashing over a long run; the author "
                        "notes attention on one GPU and the draft on the other is the "
                        "layout that matters on two cards.")
            if hw == "2x RTX 3090 + EPYC 7663" and model == "Qwen3.8-Flash-Next":
                return ("Rented 2x RTX 3090 box (two NUMA nodes, no P2P, 2x EPYC 7663, "
                        "640 GB DDR4 ECC), Qwen3.8-Flash-Next UD-IQ4_XS with a shared "
                        "Q8_0 MTP draft. The csantiago78 reconstruction climbs with "
                        f"length: {val(rows,'lc24528-epyc-csantiago-partial','tps')} tok/s mid-run "
                        f"at 3493 tokens to {val(rows,'lc24528-epyc-csantiago-full','tps')} tok/s over "
                        "the full 8513-token generation as the expert cache warms. "
                        "GenerelSchwerz's own moe-cache branch beats it on the same "
                        f"machine: {val(rows,'lc24528-epyc-gs-mtp2','tps')} tok/s decode with "
                        f"{val(rows,'lc24528-epyc-gs-mtp2','pp_tps')} tok/s prefill at 256k "
                        f"capacity ({pct(rows,'lc24528-epyc-csantiago-full','lc24528-epyc-gs-mtp2','tps'):+.0f}% "
                        "vs the csantiago full-run number), with the draft layers pinned "
                        "to the second GPU to avoid a device crossing at the shared head. "
                        "An earlier 80k-capacity run on the same box with much larger "
                        f"cache budgets reached {val(rows,'lc24528-epyc-gs-mtp2-80k','tps')} "
                        "tok/s over 10,781 tokens (55.89% MTP2 acceptance), above the "
                        "256k run, though the author flags it as uncontrolled (bigger "
                        "budgets, draft device not pinned). Cache budget looks like the "
                        "dominant lever over context capacity here. "
                        "Cross-machine note: the same csantiago branch hit 49.3 tok/s on "
                        "a desktop 2x RTX 3090 (Ryzen 9950X) with a different patch set, "
                        "so these are not controlled A/Bs.")
            if hw == "M3 Pro 36GB" and model == "Qwen3 30B A3B":
                return ("Metal on-demand expert loading straight from disk, Qwen3-30B-A3B "
                        "Q6_K on an M3 Pro 36 GB: fully resident runs at "
                        f"{val(rows,'lc24528-m3pro-resident','tps')} tok/s; streaming experts "
                        "to free 11 GB costs "
                        f"{pct(rows,'lc24528-m3pro-resident','lc24528-m3pro-stream11','tps'):+.0f}% "
                        f"({val(rows,'lc24528-m3pro-stream11','tps')} tok/s) and freeing 16.6 GB "
                        f"costs {pct(rows,'lc24528-m3pro-resident','lc24528-m3pro-stream16','tps'):+.0f}% "
                        f"({val(rows,'lc24528-m3pro-stream16','tps')} tok/s). The same trick "
                        "gets the model onto an M1 Pro 16 GB at 13 tok/s. Disk-backed "
                        "expert streaming trades roughly 1 tok/s per GB freed in this "
                        "band.")
            if hw == "RTX 5060 Ti" and model == "Qwen3 30B A3B":
                return ("Matched-budget test: same ~12.5 GiB of VRAM on an RTX 5060 Ti, "
                        "spent either on the VRAM expert cache or on resident layers, "
                        "Qwen3-30B-A3B Q4_K_M, same binary both arms. Residency wins "
                        "outright: prefill "
                        f"{val(rows,'lc24528-5060ti-matched-resident','pp_tps')} vs "
                        f"{val(rows,'lc24528-5060ti-matched-cache','pp_tps')} tok/s and "
                        "decode "
                        f"{val(rows,'lc24528-5060ti-matched-resident','tps')} vs "
                        f"{val(rows,'lc24528-5060ti-matched-cache','tps')} tok/s "
                        f"({pct(rows,'lc24528-5060ti-matched-cache','lc24528-5060ti-matched-resident','tps'):+.0f}% "
                        "for resident). The cache arm hit 85.3% of expert lookups at "
                        "steady state with zero evictions and still lost: the misses "
                        "cost full CPU round-trips and the hits pay bookkeeping, while "
                        "resident weights serve every token at the same byte cost. "
                        "Prefill gains nothing from the cache (0/8 hits cold), so budget "
                        "spent on the cache is budget not spent on layers that would "
                        "accelerate every prompt token.")
            if hw == "GTX 1080 Ti" and model == "Qwen3.6-35B-A3B":
                return ("MoE-cache budget sweep on the leloch moe-cache-pr branch, "
                        "single GTX 1080 Ti 11 GB, Qwen3.6-35B-A3B UD-Q8_K_XL, experts "
                        "on CPU. Every cache budget regresses against the "
                        "hard-disabled path: "
                        f"{val(rows,'lc24528-1080ti-cache-off','tps')} tok/s with the cache "
                        "off, and the regression scales with budget size, down to "
                        f"{val(rows,'lc24528-1080ti-cache-4096','tps')} tok/s at 4096 MB "
                        f"({pct(rows,'lc24528-1080ti-cache-off','lc24528-1080ti-cache-4096','tps'):+.0f}%). "
                        "Even the smallest budgets stay below baseline (32 MB: "
                        f"{val(rows,'lc24528-1080ti-cache-32','tps')} tok/s, -3%). On an "
                        "old Pascal card with a slow host path, the pool's bookkeeping "
                        "and copy traffic cost more than the host-to-VRAM expert fetches "
                        "it replaces; the author's note is that this is outside the "
                        "hardware regime where the cache was expected to help.")
        if (venue, issue) == ("llama.cpp", "28248"):
            if hw == "RTX 5070 Ti 16 GB + RTX 4060 Ti 16 GB" and model == "DeepSeek-V4-Flash-Vision-Exp":
                return ("Persistent VRAM expert pool (-mec) across two unequal GPUs, "
                        "RTX 5070 Ti (PCIe 5.0 x16) + RTX 4060 Ti (PCIe 4.0 x4), all "
                        "experts on CPU at baseline. Pooling 48 experts per device "
                        "lifts decode from "
                        f"{val(rows,'lc28248-dualgpu-mec-0-baseline','tps')} to "
                        f"{val(rows,'lc28248-dualgpu-mec-48','tps')} tok/s "
                        f"({pct(rows,'lc28248-dualgpu-mec-0-baseline','lc28248-dualgpu-mec-48','tps'):+.0f}%) "
                        "at 85-93% window hit. The pool only pays where the PCIe rail "
                        "is fast: -mec 48,0 (pool on the 5070 Ti only) reaches just "
                        f"{val(rows,'lc28248-dualgpu-mec-48-0','tps')} tok/s, while "
                        "per-device sizing helps a little (48,56: "
                        f"{val(rows,'lc28248-dualgpu-mec-48-56','tps')}). The best arm "
                        "is auto-scaling: asking for 128 slots per device, the fork's "
                        "budget logic scales to ~47/~58 and lands at "
                        f"{val(rows,'lc28248-dualgpu-mec-128-128','tps')} tok/s decode / "
                        f"{val(rows,'lc28248-dualgpu-mec-128-128','pp_tps')} tok/s prefill, "
                        "about 14% over the hand-picked 48-slot config: over-requesting "
                        "degrades gracefully, while aggressive manual sizing caused a "
                        "shared-memory spill the author measured at ~5%.")
        if (venue, issue) == ("llama.cpp", "29965"):
            if hw == "Radeon 780M" and model == "GLM-4.7-Flash":
                return ("Vulkan flash-attention head grouping on a Radeon 780M APU "
                        "(gfx1103), GLM-4.7-Flash Q4_K_M at 32K context. The model's "
                        "20 query heads per KV head exceed the coopmat1 max_gqa of 16, "
                        "so upstream disables GQA mode and every head re-reads the "
                        "whole KV cache: "
                        f"{val(rows,'lc29965-780m-groups-off','tps')} tok/s. Grouping "
                        "heads to the largest divisor of the ratio that fits under the "
                        "limit lifts decode to "
                        f"{val(rows,'lc29965-780m-groups-on','tps')} tok/s "
                        f"({pct(rows,'lc29965-780m-groups-off','lc29965-780m-groups-on','tps'):+.0f}%), "
                        "with a further +15-19% at 8K and unchanged prefill. The "
                        "author's group floor of 4 heads matters: smaller groups push "
                        "split_k down to 1 and each workgroup ends up reading the "
                        "entire cache alone.")
        if (venue, issue) == ("llama.cpp", "30001"):
            if hw == "RTX 4090" and model == "Qwen2.5-7B":
                return ("Native q8_0-q4_0 FlashAttention kernel vs the default f16 "
                        "fallback, RTX 4090, Qwen2.5-7B Q4_0 with q8_0 KV, same commit "
                        "A/B. The win scales with KV depth: "
                        f"{val(rows,'lc30001-4090-kv4096-default','tps')} vs "
                        f"{val(rows,'lc30001-4090-kv4096-native','tps')} tok/s at 4k "
                        f"({pct(rows,'lc30001-4090-kv4096-default','lc30001-4090-kv4096-native','tps'):+.0f}%), "
                        f"{val(rows,'lc30001-4090-kv16384-default','tps')} vs "
                        f"{val(rows,'lc30001-4090-kv16384-native','tps')} at 16k, "
                        f"{val(rows,'lc30001-4090-kv32768-default','tps')} vs "
                        f"{val(rows,'lc30001-4090-kv32768-native','tps')} at 32k (+26%). "
                        "The fallback penalty grows because the K/V dequant work scales "
                        "with cache size while the decode matvec does not; the author "
                        "measured the binary cost at +0.47 MiB for the single quant pair "
                        "instead of the rejected ALL_QUANTS build.")
        if (venue, issue) == ("llama.cpp", "30006"):
            if hw == "Dimensity 9400" and model == "Qwen3.5-0.8B":
                return ("Mali-G925-Immortalis MC12 (Dimensity 9400, Android 16 Termux): "
                        "VK_KHR_cooperative_matrix is a prefill pessimization. "
                        f"pp512 coopmat on {val(rows,'lc-30006-d9400-coopmat-on','pp_tps')} "
                        f"-> coopmat off {val(rows,'lc-30006-d9400-coopmat-off','pp_tps')} "
                        f"tok/s ({pct(rows,'lc-30006-d9400-coopmat-on','lc-30006-d9400-coopmat-off','pp_tps'):+.0f}%), "
                        "decode unchanged. The author's hypothesis: the coopmat mul_mm "
                        "variant fails its shared-memory validation on this device "
                        "(32 KB shared memory) and prefill falls back to matvec speed; "
                        "the CPU arm (pp512 "
                        f"{val(rows,'lc-30006-d9400-cpu','pp_tps')} tok/s) matches the "
                        "coopmat-on GPU arm, consistent with that. Disabling f16 on top "
                        "of coopmat is slightly worse, and integer-dot or host-memory "
                        "toggles change nothing, so coopmat is the only lever.")
        if (venue, issue) == ("llama.cpp", "30000") and hw == "RTX 5060 Ti":
            if model in ("Qwen3-Embedding-8B", "Qwen3-Reranker-8B", "granite-4.2-8b"):
                pre = [r for r in rows.values() if r["id"].endswith("b6d9c82")]
                post = [r for r in rows.values() if r["id"].endswith("b91f6a6")]
                if pre and post:
                    a, b = pre[0]["id"], post[0]["id"]
                    return ("Bisected regression: #25773 (91f6a6cf3, spec constant for "
                            "matmul A-type) made Q8_0 Vulkan prefill slower on this "
                            f"NV_coopmat2 card: pp512 {val(rows,a,'pp_tps')} -> "
                            f"{val(rows,b,'pp_tps')} tok/s "
                            f"({pct(rows,a,b,'pp_tps'):+.0f}%). Still present at "
                            "b11425 (the author re-ran b10405 vs b11425: -17% to -19%). "
                            "Token generation is unchanged.")
        if (venue, issue) == ("llama.cpp", "20969"):
            if hw == "RTX 4090" and model == "Qwen3 30B A3B":
                return ("Baseline KV-cache sweep for a TurboQuant fork build (AmesianX "
                        "v1.2.0) on RTX 4090, Qwen3-30B-A3B Q4_K_M, llama-bench "
                        "pp512/tg128, mean of 3 reps. llama-bench rejects the tbq KV "
                        "types in this build, so only f16/q8_0/q4_0 KV caches have "
                        "throughput: "
                        f"f16 {val(rows,'lc20969-st-kv-f16','pp_tps')} pp / "
                        f"{val(rows,'lc20969-st-kv-f16','tps')} tg, q8_0 "
                        f"{val(rows,'lc20969-st-kv-q80','pp_tps')} / "
                        f"{val(rows,'lc20969-st-kv-q80','tps')}, q4_0 "
                        f"{val(rows,'lc20969-st-kv-q40','pp_tps')} / "
                        f"{val(rows,'lc20969-st-kv-q40','tps')} tok/s. KV quantization "
                        "costs about 4% decode from f16 to q4_0 on this model.")
            if hw == "RTX 4090" and model == "Llama 3.1 8B":
                return ("TurboQuant KV-cache matrix on RTX 4090 (i9-14900K), Llama 3.1 "
                        "8B Q4_K_M, two spiritbuun fork builds. Build flags first: "
                        "without -DGGML_CUDA_FA the fused FA kernels are missing and "
                        "prefill drops from "
                        f"{val(rows,'lc20969-wsf1-fa-f16','pp_tps')} to "
                        f"{val(rows,'lc20969-wsf1-nofa-f16','pp_tps')} pp512 (-7%). "
                        "With FA on, q8_0-K + turbo4-V is the best config: "
                        f"{val(rows,'lc20969-wsf1-q8-t4','pp_tps')} pp512 (+8.4% vs "
                        f"f16's {val(rows,'lc20969-wsf1-fa-f16','pp_tps')}) at "
                        f"{val(rows,'lc20969-wsf1-q8-t4','tps')} tg128 vs "
                        f"{val(rows,'lc20969-wsf1-fa-f16','tps')} (-6.2%). Symmetric "
                        "turbo is much slower: turbo3/turbo3 "
                        f"{val(rows,'lc20969-wsf1-t3-t3','tps')} tok/s, turbo4/turbo4 "
                        f"{val(rows,'lc20969-wsf1-t4-t4','tps')}. The v2 build "
                        "reproduces this (f16 "
                        f"{val(rows,'lc20969-wsf2-4090-off-f16','pp_tps')} / "
                        f"{val(rows,'lc20969-wsf2-4090-off-f16','tps')}, q8_0+turbo4 "
                        f"{val(rows,'lc20969-wsf2-4090-off-q8t4','pp_tps')} / "
                        f"{val(rows,'lc20969-wsf2-4090-off-q8t4','tps')}) and adds "
                        "layer-adaptive mode: LA=1 (first/last 4 layers at q8_0) "
                        "*raises* decode, q8_0+turbo4 goes "
                        f"{val(rows,'lc20969-wsf2-4090-off-q8t4','tps')} -> "
                        f"{val(rows,'lc20969-wsf2-4090-la1-q8t4','tps')} tok/s, "
                        "because the promoted layers use native int8 decode.")
            if hw == "RTX 5090" and model == "Llama 3.1 8B":
                return ("Same TurboQuant matrix on RTX 5090 (9950X3D, 64 GB DDR5), "
                        "Llama 3.1 8B Q4_K_M, CUDA 12.8 sm_120 (CUDA 13.2 sm_120a "
                        "identical within noise). Blackwell handles TurboQuant decode "
                        "far worse than Ada: f16 baseline "
                        f"{val(rows,'lc20969-wsf2-5090-off-f16','pp_tps')} pp512 / "
                        f"{val(rows,'lc20969-wsf2-5090-off-f16','tps')} tg128, but "
                        "q8_0-K + turbo4-V falls to "
                        f"{val(rows,'lc20969-wsf2-5090-off-q8t4','tps')} tok/s "
                        f"({pct(rows,'lc20969-wsf2-5090-off-f16','lc20969-wsf2-5090-off-q8t4','tps'):+.0f}%) "
                        "where the same config costs only about 6-9% on the RTX 4090. "
                        "Symmetric turbo3 loses "
                        f"{pct(rows,'lc20969-wsf2-5090-off-f16','lc20969-wsf2-5090-off-t3','tps'):+.0f}% "
                        "decode. The author attributes this to TurboQuant's dequant "
                        "path matching Ada int8 dp4a while Blackwell's tensor cores "
                        "are optimized for fp8/fp4. LA=1 again helps: q8_0+turbo4 "
                        f"{val(rows,'lc20969-wsf2-5090-off-q8t4','tps')} -> "
                        f"{val(rows,'lc20969-wsf2-5090-la1-q8t4','tps')} tok/s.")
            if hw == "RTX 5090" and model == "Qwen 3.5 27B":
                return ("Madreag's CUDA-optimized TurboQuant fork on RTX 5090, Qwen 3.5 "
                        "27B Q6_K, llama-bench tg128 measured at 32K context depth. "
                        "Against the q8_0 KV baseline at "
                        f"{val(rows,'lc20969-5090-md59-q8','tps')} tok/s, the optimized "
                        "turbo types match or beat it: turbo4 "
                        f"{val(rows,'lc20969-5090-md59-t4','tps')} (+2.0% at 3.8x "
                        "compression), turbo3 "
                        f"{val(rows,'lc20969-5090-md59-t3','tps')}, turbo2 "
                        f"{val(rows,'lc20969-5090-md59-t2','tps')} "
                        f"({pct(rows,'lc20969-5090-md59-q8','lc20969-5090-md59-t2','tps'):+.1f}% "
                        "at 7.5x compression, the 32K champion), turbo1.5 "
                        f"{val(rows,'lc20969-5090-md59-t15','tps')}. The same numbers with "
                        "the *base* fork were far slower: turbo4 "
                        f"{val(rows,'lc20969-5090-md59b-t4','tps')}, turbo3 "
                        f"{val(rows,'lc20969-5090-md59b-t3','tps')}, turbo2 "
                        f"{val(rows,'lc20969-5090-md59b-t2','tps')} tok/s, so the kernel "
                        "rewrite alone is worth +13 to +46% decode. Short-context "
                        "decode (63-65 tok/s) is identical across all types, weight-"
                        "loading bound; the differences only appear at 32K+ where KV "
                        "bandwidth dominates.")
            if hw == "RTX 3090" and model == "Qwen 3.5 9B":
                return ("Base-fork vs CUDA-optimized-fork A/B on RTX 3090, Qwen 3.5 9B "
                        "Q8_0, llama-bench tg128 at depth, back-to-back on the same "
                        "GPU. At 32K the optimization lifts turbo4 from "
                        f"{val(rows,'lc20969-3090-md39b-t4','tps')} to "
                        f"{val(rows,'lc20969-3090-md39-t4','tps')} tok/s "
                        f"({pct(rows,'lc20969-3090-md39b-t4','lc20969-3090-md39-t4','tps'):+.0f}%, "
                        "the largest gain in the study), turbo3 "
                        f"{val(rows,'lc20969-3090-md39b-t3','tps')} -> "
                        f"{val(rows,'lc20969-3090-md39-t3','tps')}, turbo2 "
                        f"{val(rows,'lc20969-3090-md39b-t2','tps')} -> "
                        f"{val(rows,'lc20969-3090-md39-t2','tps')}, and even q8_0 "
                        f"{val(rows,'lc20969-3090-md39b-q8','tps')} -> "
                        f"{val(rows,'lc20969-3090-md39-q8','tps')} from better KV reads. "
                        "At 64K: turbo3 "
                        f"{val(rows,'lc20969-3090-md39b-t3-64','tps')} -> "
                        f"{val(rows,'lc20969-3090-md39-t3-64','tps')}, turbo2 "
                        f"{val(rows,'lc20969-3090-md39b-t2-64','tps')} -> "
                        f"{val(rows,'lc20969-3090-md39-t2-64','tps')} tok/s. After optimization "
                        "turbo2 "
                        f"({val(rows,'lc20969-3090-md39-t2','tps')}) is the fastest 32K "
                        "config, above q8_0 "
                        f"({val(rows,'lc20969-3090-md39-q8','tps')}), while turbo4 "
                        f"({val(rows,'lc20969-3090-md39-t4','tps')}) closes to within 1%.")
            if hw == "RTX 4090M" and model == "Qwen 3.5 9B":
                return ("Same base-vs-optimized fork A/B on a RTX 4090M 16 GB (SM89), "
                        "Qwen 3.5 9B Q8_0, tg128 at 32K depth: turbo4 "
                        f"{val(rows,'lc20969-4090m-md4mb-t4','tps')} -> "
                        f"{val(rows,'lc20969-4090m-md4m-t4','tps')} tok/s "
                        f"({pct(rows,'lc20969-4090m-md4mb-t4','lc20969-4090m-md4m-t4','tps'):+.0f}%), "
                        "turbo3 "
                        f"{val(rows,'lc20969-4090m-md4mb-t3','tps')} -> "
                        f"{val(rows,'lc20969-4090m-md4m-t3','tps')}, turbo2 "
                        f"{val(rows,'lc20969-4090m-md4mb-t2','tps')} -> "
                        f"{val(rows,'lc20969-4090m-md4m-t2','tps')}, q8_0 "
                        f"{val(rows,'lc20969-4090m-md4mb-q8','tps')} -> "
                        f"{val(rows,'lc20969-4090m-md4m-q8','tps')}. After the rewrite all "
                        "types land within 1.5 tok/s of each other (49-53), the 16 GB "
                        "part also makes 32K the practical ceiling here.")
            if hw == "RTX 3090 Ti" and model == "Qwen 3.5 9B":
                return ("TurboQuant KV matrix on a memory-overclocked RTX 3090 Ti "
                        "(+2200 mem), Qwen 3.5 9B Q8_0, llama-bench tg128 at depth, "
                        "optimized fork. At 32K: q8_0 "
                        f"{val(rows,'lc20969-3090ti-mdti-q8','tps')} tok/s, turbo4 "
                        f"{val(rows,'lc20969-3090ti-mdti-t4','tps')}, turbo3 "
                        f"{val(rows,'lc20969-3090ti-mdti-t3','tps')}, turbo1.5 "
                        f"{val(rows,'lc20969-3090ti-mdti-t15','tps')}, and turbo2 "
                        f"{val(rows,'lc20969-3090ti-mdti-t2','tps')} "
                        f"({pct(rows,'lc20969-3090ti-mdti-q8','lc20969-3090ti-mdti-t2','tps'):+.1f}%, "
                        "again the depth winner at 7.5x compression). At 64K q8_0 and "
                        "turbo4 OOM on 24 GB while turbo2 reaches "
                        f"{val(rows,'lc20969-3090ti-mdti-t2-64','tps')}, turbo1.5 "
                        f"{val(rows,'lc20969-3090ti-mdti-t15-64','tps')} and turbo3 "
                        f"{val(rows,'lc20969-3090ti-mdti-t3-64','tps')} tok/s: the low-bit "
                        "caches buy context length that simply does not fit otherwise. "
                        "Short-context decode is 90-91 tok/s for every type.")
            if hw == "2x RTX 5060 Ti" and model == "Llama 3.1 8B":
                return ("animehacker TurboQuant fork on 2x RTX 5060 Ti (SM 120), "
                        "Llama 3.1 8B Q5_K_M, 8K context, 4 concurrent: stock f16 KV "
                        f"{val(rows,'lc20969-5060ti-df-l31-b','tps')} tok/s vs tq3_0 "
                        f"K+V {val(rows,'lc20969-5060ti-df-l31-t','tps')} tok/s, a "
                        f"{pct(rows,'lc20969-5060ti-df-l31-b','lc20969-5060ti-df-l31-t','tps'):+.0f}% "
                        "collapse. The animehacker kernels target Ampere; on Blackwell "
                        "SM 120 the author sees the same ~5x penalty on every model "
                        "tested and asks whether the spiritbuun or Madreag forks do "
                        "better on this hardware (they do: Madreag's optimized CUDA "
                        "path matches q8_0 at short context on SM 120).")
            if hw == "2x RTX 5060 Ti" and model == "Qwen 2.5 14B":
                return ("Same 2x RTX 5060 Ti animehacker-fork test, Qwen 2.5 14B "
                        "Q5_K_M at 8K context, 4 concurrent: "
                        f"{val(rows,'lc20969-5060ti-df-q14-b','tps')} tok/s with f16 KV "
                        f"vs {val(rows,'lc20969-5060ti-df-q14-t','tps')} with tq3_0, "
                        f"{pct(rows,'lc20969-5060ti-df-q14-b','lc20969-5060ti-df-q14-t','tps'):+.0f}%, "
                        "the same Ampere-kernels-on-Blackwell penalty as the other "
                        "models in the sweep.")
            if hw == "2x RTX 5060 Ti" and model == "Qwen 2.5 32B":
                return ("Same 2x RTX 5060 Ti animehacker-fork test, Qwen 2.5 32B "
                        "Q4_K_M at 8K context, 4 concurrent: "
                        f"{val(rows,'lc20969-5060ti-df-q32-b','tps')} tok/s with f16 KV "
                        f"vs {val(rows,'lc20969-5060ti-df-q32-t','tps')} with tq3_0, "
                        f"{pct(rows,'lc20969-5060ti-df-q32-b','lc20969-5060ti-df-q32-t','tps'):+.0f}%. "
                        "Defilan also measured a VRAM crossover on this hardware: tq3_0 "
                        "uses *more* VRAM below 32K context (16K: 22.8 vs 8.0 GB) and "
                        "less above (65K: 8.4 vs 14.3 GB).")
            if hw == "2x EVGA RTX 3080 Ti 12GB" and model == "Qwen3.5-9B":
                return ("seanrasch pushed Qwen3.5-9B Q4_K_M to its native 256K context "
                        "on dual RTX 3080 Ti 12 GB with turbo2 K+V cache: decode is "
                        f"flat at {val(rows,'lc20969-3080ti-sr-128k','tps')} / "
                        f"{val(rows,'lc20969-3080ti-sr-160k','tps')} / "
                        f"{val(rows,'lc20969-3080ti-sr-256k','tps')} tok/s at 128K / "
                        "160K / 256K while full-context prefill falls "
                        f"{val(rows,'lc20969-3080ti-sr-128k','pp_tps')} -> "
                        f"{val(rows,'lc20969-3080ti-sr-256k','pp_tps')} tok/s with "
                        "O(n^2) attention. 10 GB of VRAM stays free at 256K, so the "
                        "context limit is the model, not the hardware; a single 12 GB "
                        "card tops out at 96K with any turbo config.")
            if hw == "DGX Spark" and model == "Qwen3.5 35B":
                return ("AmesianX fork on DGX Spark (SM 121 GB10): the author reports "
                        "turbo KV *faster* than q8_0 on Blackwell decode, "
                        f"{val(rows,'lc20969-spark-ax-35b-q80','tps')} tok/s q8_0 vs "
                        f"{val(rows,'lc20969-spark-ax-35b-turbo','tps')} turbo "
                        f"({pct(rows,'lc20969-spark-ax-35b-q80','lc20969-spark-ax-35b-turbo','tps'):+.1f}%), "
                        "the opposite sign from WaveboSF's spiritbuun-fork numbers on "
                        "a desktop RTX 5090 (-25 to -46%): the fork's fused flash "
                        "attention path, not the architecture, decides whether turbo "
                        "KV helps on Blackwell.")
            if hw == "DGX Spark" and model == "Qwen3.5-27B":
                return ("Prompt processing with tbqp3-K/tbq3-V KV on DGX Spark (SM 121 "
                        "native build), Qwen3.5-27B heretic-v3 i1-Q3_K_M: "
                        f"{val(rows,'lc20969-spark-ax-27b-f16pp','pp_tps')} tok/s with "
                        f"f16 KV vs {val(rows,'lc20969-spark-ax-27b-tbqpp','pp_tps')} "
                        f"with turbo ({pct(rows,'lc20969-spark-ax-27b-f16pp','lc20969-spark-ax-27b-tbqpp','pp_tps'):+.0f}%). "
                        "The author stresses this is the SM 121 native build; the "
                        "v1.2 release binaries defaulted to SM 52 and lost 50-75% of "
                        "prompt processing to JIT emulation on other hardware.")
        if (venue, issue) == ("vLLM", "60091"):
            if hw == "MI350X" and model == "DeepSeek-V4.1-Flash":
                return ("vLLM PR #60091 passes output_size to the two "
                        "repeat_interleave calls in the ROCm "
                        "combine_topk_swa_indices, removing 160 host syncs per prefill "
                        "step (40 layers) on gfx950. MI350X TP=4 with expert "
                        "parallelism, DeepSeek-V4.1-Flash, mean of 3-5 reps, arms "
                        "interleaved in rotated order with disjoint ranges: prompt "
                        f"throughput {val(rows,'vllm-60091-mi350x-dsv41-main','pp_tps')} "
                        f"-> {val(rows,'vllm-60091-mi350x-dsv41-pr','pp_tps')} tok/s "
                        f"({pct(rows,'vllm-60091-mi350x-dsv41-main','vllm-60091-mi350x-dsv41-pr','pp_tps'):+.1f}%), "
                        "aggregate output at concurrency 64 "
                        f"{val(rows,'vllm-60091-mi350x-dsv41-main','tps')} -> "
                        f"{val(rows,'vllm-60091-mi350x-dsv41-pr','tps')} tok/s (+2.7%), "
                        "median TTFT at conc 1 340.7 -> 321.1 ms (-5.7%), median TPOT "
                        "33.34 -> 32.47 ms. About 20 ms saved per prefill step, roughly "
                        "120 microseconds per removed sync. Outputs bit-identical, "
                        "GSM8K 0.9014 vs 0.9083 (SE 0.008).")
        if (venue, issue) == ("vLLM", "60070"):
            if hw == "4x NVIDIA B200" and model == "GLM-5.2-NVFP4":
                return ("vLLM PR #60070 removes a per-decode-step FillFunctor launch "
                        "(3,900 launches in the baseline trace, 0 patched) by owning a "
                        "persistent FlashInfer multi-CTA-KV counter buffer. "
                        f"Output throughput {val(rows,'vllm-60070-4xb200-baseline','tps')} "
                        f"-> {val(rows,'vllm-60070-4xb200-patched','tps')} tok/s "
                        f"({pct(rows,'vllm-60070-4xb200-baseline','vllm-60070-4xb200-patched','tps'):+.1f}%) "
                        "at BS=1, ISL=4, OSL=2048; TPOT -4.5%. Both arms on the same "
                        "FlashInfer build (like-with-like).")
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
        note = ab_note(venue, issue, hw, model, by_id, backend)
        note_html = (f"<p><strong>Note:</strong> {note}</p>" if note else "")
        if issue.isdigit():
            link = f'<a href=\"{esc(url)}\" rel=\"nofollow\">#{esc(issue)}</a>'
        else:
            link = f'<a href=\"{esc(url)}\" rel=\"nofollow\">{esc(url)}</a>'
        ab_sections.append(f"""<h3>{esc(model)} on {esc(hw)} ({esc(backend)}) - {esc(venue)} {link}</h3>
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
