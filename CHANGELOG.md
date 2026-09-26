# Changelog

## 2026-09-26 — v0.2.0: x86 GPUs, 3 sources, contradiction/outlier flags

- Added 2 sources: LLM Configurator measured benchmarks (CC BY 4.0 — RTX 3090/
  4090, llama.cpp, context lengths 4k-131k, per-row publisher + source URL) and
  Silicon Score benchmark audit (432 Apple Silicon rows with per-row source URLs,
  prompt-processing and TTFT figures).
- Dataset is now multi-source: 3 sources merged by `scripts/merge_data.py` from
  `data/raw/*.json`; collector-per-source, deterministic, cached.
- New `flags` column with deterministic rules: `contradiction` (same
  model+hardware+quant+backend+ctx differing >10%) and `outlier` (>3x group
  median among measured rows); verified fresh by `scripts/check_data.py` on
  every push. Flags are badged in every table.
- Site: lookup and tables show flags; coverage, credits, and citation updated.

## 2026-09-26 — v0.1.0: first dataset, first site

- Initial dataset: 258 records from the LLMCheck Apple Silicon LLM Benchmark
  Database (CC BY 4.0) — 64 models, 16 chips (M1–M6), backends MLX, Ollama,
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
