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
<title>{esc(title)} — Token Atlas</title>
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
        return "—"
    return " ".join(f'<span class="badge b-flag">{esc(f)}</span>' for f in flags)


def record_row(r):
    ttft = f"{r['ttft_s']}" if r.get("ttft_s") is not None else "—"
    ctx = r.get("ctx") or "—"
    date = r.get("date") or "—"
    return (f"<tr><td><a href=\"/{slug(r['hardware'])}/\">{esc(r['hardware'])}</a></td>"
            f"<td><a href=\"/{slug(r['model'])}/\">{esc(r['model'])}</a> "
            f"<span class=\"dim\">{esc(r.get('params'))}</span></td>"
            f"<td>{esc(r.get('quant'))}</td><td>{esc(r.get('backend'))}</td>"
            f"<td class=\"num\">{esc(r.get('tps'))}</td><td class=\"num\">{esc(ttft)}</td>"
            f"<td>{esc(ctx)}</td><td>{esc(date)}</td>"
            f"<td>{prov_badge(r.get('provenance'))}</td>"
            f"<td>{flag_badges(r.get('flags'))}</td>"
            f"<td><a href=\"{esc(r['source_url'])}\" rel=\"nofollow\">source</a></td></tr>")


TABLE_HEAD = ("<tr><th>hardware</th><th>model</th><th>quant</th><th>backend</th>"
              "<th>tok/s</th><th>ttft s</th><th>ctx</th><th>date</th><th>class</th><th>flags</th><th>source</th></tr>")


def records_table(rows):
    rows = sorted(rows, key=lambda r: (str(r.get("model")).lower(),
                                       -(r.get("tps") or 0)))
    body = "\n".join(record_row(r) for r in rows)
    return f"<table>{TABLE_HEAD}{body}</table>"


def main():
    with open(os.path.join(DATA, "records.json")) as f:
        ds = json.load(f)
    records = ds["records"]
    retrieved = ds.get("retrieved", "?")

    hw = defaultdict(list)
    models = defaultdict(list)
    backends = defaultdict(list)
    for r in records:
        hw[r["hardware"]].append(r)
        models[r["model"]].append(r)
        backends[(r["model"], r["hardware"], r["quant"])].append(r)

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
    credits = "".join(f"<li><a href=\"{u}\">{esc(n)}</a> — {esc(d)}</li>" for n, u, d in CREDITS)
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
<li><a href="/hardware/">Per-hardware pages</a> — every recorded run on each chip</li>
<li><a href="/models/">Per-model pages</a> — every hardware/quant/backend for each model</li>
<li><a href="/backends/">Cross-backend notes</a> — same model + chip across backends</li>
<li><a href="/data/">The dataset</a> — CSV and JSON, with schema</li>
<li><a href="/changelog.html">Changelog</a> — what changed, when</li>
</ul>
<h2>Reading the data</h2>
<p>Provenance classes: {prov_note}.</p>
<p><strong>sourced</strong> — a public page we link to, containing the quoted number.
<strong>community</strong> — a community-measured run (e.g. llama-bench results) carried in the
source dataset. <strong>estimated</strong> — the source's own model-based estimate; always shown
as such, never mixed with measured rows.</p>
<p>Current coverage: Apple Silicon (M1–M6) and x86 GPUs (RTX 3090/4090); backends
MLX / Ollama / LM Studio / llama.cpp / llamafile; multiple quantizations and context
lengths (4k–131k where published). vLLM, ExLlama, and more x86 hardware are next —
see the <a href="/changelog.html">changelog</a>.</p>
<h2>Complementary projects</h2>
<p>Token Atlas is built to complement, not duplicate, existing efforts — we credit and link them:</p>
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
<a href="https://llmconfigurator.com/measured-benchmarks.json">measured-benchmarks.json</a>;
Silicon Score benchmark audit via <a href="https://siliconscore.com/benchmarks.json">benchmarks.json</a>.
Per-row source links are in the dataset.</p>
"""
    write("index.html", page("Local LLM inference performance, source-cited", index))

    # --- hardware pages ---
    hw_list = "".join(
        f"<li><a href=\"hardware/{slug(h)}/\">{esc(h)}</a> — {len(rs)} records, "
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
        f"<li><a href=\"models/{slug(m)}/\">{esc(m)}</a> — {len(rs)} records, "
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
    multi = {k: v for k, v in sorted(backends.items()) if len({r["backend"] for r in v}) > 1}
    notes = []
    for (m, h, q), rs in multi.items():
        best = max(rs, key=lambda r: r.get("tps") or 0)
        lines = []
        for r in sorted(rs, key=lambda r: -(r.get("tps") or 0)):
            pct = (100.0 * (r.get("tps") or 0) / (best.get("tps") or 1))
            lines.append(f"<li><strong>{esc(r['backend'])}</strong>: "
                         f"{esc(r.get('tps'))} tok/s ({pct:.0f}%) "
                         f"{prov_badge(r.get('provenance'))} "
                         f"<a href=\"{esc(r['source_url'])}\" rel=\"nofollow\">source</a></li>")
        notes.append(f"""<h3>{esc(m)} on {esc(h)} ({esc(q)})</h3>
<ul>{''.join(lines)}</ul>
<p class="dim">Auto-generated comparison; relative % vs the fastest recorded backend.
Differences between backends on the same model+chip can reflect build/version,
sampling, and context differences, not just the backend itself.</p>""")
    if not notes:
        notes.append("<p>No cross-backend comparisons yet.</p>")
    write("backends/index.html", page("Cross-backend notes", f"""
<h1>Cross-backend notes</h1>
<p>Where the same model and chip were recorded on more than one backend, we show them
side by side. {len(multi)} comparable cases so far. These are the seeds of the
regression/improvement tracking the project will run between backend builds.</p>
{''.join(notes)}"""))

    # --- data page ---
    schema_fields = [
        ("id", "stable unique slug for the record"),
        ("model", "model name as published by the source"),
        ("params", "parameter size, as published (e.g. 8B, 3.8B)"),
        ("quant", "quantization (e.g. Q4_K_M)"),
        ("hardware", "chip/hardware identifier (e.g. M5 Max, RTX 4090)"),
        ("ram_gb", "memory, GB (when the source states it)"),
        ("backend", "inference backend/engine (llama.cpp, MLX, Ollama, vLLM, …)"),
        ("ctx", "context length (when stated)"),
        ("batch", "batch size (when stated)"),
        ("tps", "generation tokens/second"),
        ("pp_tps", "prompt-processing tokens/second (when reported)"),
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
<p>{len(records)} records, retrieved {esc(retrieved)}. Download and diff — the data is the
product, not the site.</p>
<ul>
<li><a href="/data/records.csv">records.csv</a></li>
<li><a href="/data/records.json">records.json</a></li>
<li><a href="/data/sources.json">sources.json</a> (source registry)</li>
</ul>
<h2>Schema</h2>
<table><tr><th>field</th><th>meaning</th></tr>{schema_rows}</table>
<h2>No record without provenance</h2>
<p>Every row carries <code>source_url</code>, <code>retrieved</code>, and <code>quote</code>
(the exact values as published). <code>estimated</code> rows are the source's own estimates
and are never mixed with measured rows in presentation.</p>
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
<p>Pick hardware and (optionally) a model, quant, or backend. Every row links to its source;
estimates are badged, never hidden.</p>
<div class="filters">
<label>hardware <select id="f-hw"></select></label>
<label>model <select id="f-model"></select></label>
<label>quant <select id="f-quant"></select></label>
<label>backend <select id="f-be"></select></label>
</div>
<p id="lcount" class="dim"></p>
<div id="ltable"></div>
<script>
fetch('/data/records.json').then(r => r.json()).then(ds => {
  const recs = ds.records;
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
    const rows = recs.filter(r =>
      (!f.hw || r.hardware === f.hw) && (!f.model || r.model === f.model) &&
      (!f.quant || r.quant === f.quant) && (!f.be || r.backend === f.be));
    rows.sort((a, b) => (a.model < b.model ? -1 : a.model > b.model ? 1 : (b.tps||0)-(a.tps||0)));
    sel('f-hw').value = f.hw; sel('f-model').value = f.model;
    sel('f-quant').value = f.quant; sel('f-be').value = f.be;
    document.getElementById('lcount').textContent =
      rows.length + ' of ' + recs.length + ' records';
    document.getElementById('ltable').innerHTML =
      '<table><tr><th>hardware</th><th>model</th><th>quant</th><th>backend</th>' +
      '<th>tok/s</th><th>ttft s</th><th>ctx</th><th>date</th><th>class</th><th>flags</th><th>source</th></tr>' +
      rows.map(r => '<tr><td>' + esc(r.hardware) + '</td><td>' + esc(r.model) +
        ' <span class="dim">' + esc(r.params) + '</span></td><td>' + esc(r.quant) +
        '</td><td>' + esc(r.backend) + '</td><td class="num">' + esc(r.tps) +
        '</td><td class="num">' + esc(r.ttft_s ?? '') + '</td><td>' + esc(r.ctx ?? '—') +
        '</td><td>' + esc(r.date ?? '—') + '</td><td>' + badge(r.provenance) +
        '</td><td>' + ((r.flags||[]).map(f => '<span class="badge b-flag">' + esc(f) + '</span>').join(' ') || '—') +
        '</td><td><a href="' + esc(r.source_url) + '" rel="nofollow">source</a></td></tr>'
      ).join('') + '</table>';
  }
  ['f-hw','f-model','f-quant','f-be'].forEach(id => sel(id).addEventListener('change', render));
  render();
});
</script>"""
    write("lookup.html", page("Lookup", lookup_body))

    print("done: %d records -> %d hardware pages, %d model pages, %d backend notes"
          % (len(records), len(hw), len(models), len(multi)))


if __name__ == "__main__":
    sys.exit(main())
