# Changelog

## 2026-09-26: Hardware Corner context curves, 308 measured GPU rows; estimates move to the reference area

- New source collected: Hardware Corner GPU LLM benchmark hub pages (21 NVIDIA
  GPUs, llama.cpp runtime). Each hub page publishes per-model, per-context
  (4k to 262k) prompt-processing and token-generation tok/s tables. The
  collector records one row per (model, quant, context) with the exact quoted
  cells: 308 measured rows covering Qwen3/Qwen3.5, Gemma 4, gpt-oss, and
  Llama 3.3 70B across RTX 3060 to RTX Pro 6000 Blackwell.
- Estimates are now reference values, not records. They live in
  `data/reference/estimates.json` (549 rows), excluded from
  `records.csv`/`records.json`, record counts, and the site's default views;
  the lookup has an explicit toggle to show them.
- Dataset: 752 measured records, 131 hardware strings, 72 models, 9 backends.
- Cross-source checks page rebuilt on the reference file: 4 strict overlaps
  plus 26 Q4-K family reference rows from the new hub tables.
- Style gate in CI: no em dashes in authored or generated files
  (`scripts/check_style.py`).

## 2026-09-26 - v0.3.0: 993 records, 70-accelerator estimate cells, power column

- New endpoint collected: LLM Configurator benchmark cells
  (/benchmarks.json, CC BY 4.0) - bandwidth-model estimates for 5 reference
  models x 70 accelerators at Q4_K_M / 4096 ctx, each row carrying the
  per-architecture calibration state (fitted run count, MAPE), board-spec
  power in watts, tok/W, and VRAM fit. Hardware names normalized by stripping
  the leading vendor token so cells join existing per-chip pages
  (e.g. "RTX 4090", "M3 Max").
- Dataset: 688 -> 993 records, 120 -> 174 hardware strings. First coverage of
  AMD APUs (Ryzen AI 9 HX 370, Ryzen AI Max+ 395), Intel Arc, Radeon RX
  7000/9000, and datacenter GPUs (A100/H100/L40S/DGX Spark/GB10). Power
  (board-spec, labeled) now populated for 305 rows.
- Estimates stay badged as estimates; measured rows are never mixed into
  flag computation with estimates.


## 2026-09-26: v0.2.0, x86 GPUs, 3 sources, contradiction/outlier flags

- Added 2 sources: LLM Configurator measured benchmarks (CC BY 4.0: RTX 3090/
  4090, llama.cpp, context lengths 4k-131k, per-row publisher + source URL) and
  Silicon Score benchmark audit (416 Apple Silicon rows with per-row source URLs,
  prompt-processing and TTFT figures).
- Dataset is now multi-source: 3 sources merged by `scripts/merge_data.py` from
  `data/raw/*.json`; collector-per-source, deterministic, cached.
- New `flags` column with deterministic rules: `contradiction` (same
  model+hardware+quant+backend+ctx differing >10%) and `outlier` (>3x group
  median among measured rows); verified fresh by `scripts/check_data.py` on
  every push. Flags are badged in every table.
- Site: lookup and tables show flags; coverage, credits, and citation updated.

## 2026-09-26: v0.1.0, first dataset, first site

- Initial dataset: 258 records from the LLMCheck Apple Silicon LLM Benchmark
  Database (CC BY 4.0): 64 models, 16 chips (M1 to M6), backends MLX, Ollama,
  LM Studio, llama.cpp; Q4_K_M plus 9 other quants. Every row carries source
  URL, retrieval date, and the exact quoted values; provenance classes
  (sourced / community / estimated) are badged on the site.
- Site: home, "what speed will I get" lookup (client-side filter over the
  committed JSON), per-hardware pages, per-model pages, cross-backend notes,
  data page with schema, changelog.
- Deterministic collectors and checks: `scripts/collect_llmcheck.py`,
  `scripts/check_data.py`, `scripts/build_site.py` (stdlib only, cached fetches).
- CI: data checks on every push; weekly release tagging workflow.
- Issue templates: data submission and corrections.
- Survey of existing projects completed (LocalScore, LLMCheck, llmconfigurator,
  Localmaxxing, Bench360, anubis-oss, r/LocalLLaMA threads); positioning
  documented on the home page with credits and links.
