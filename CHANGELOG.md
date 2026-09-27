# Changelog

## 2026-09-26: Data quality fixes: ctx semantics, multi-run splitting, settings-aware flags, cluster scope, quote verification

- **ctx semantics fixed.** `pp512`/`tg128` are prompt-processing and token-generation test lengths, not context windows. Added `pp_tokens`/`tg_tokens` fields; `ctx` is now null on llama-bench rows (all 1,805 llama.cpp discussion rows).
- **Multi-run splitting.** Repeated test cells within one post (separate runs on the same setup) are now separate record rows, marked in notes as "run 2 of 2" and so on. llama.cpp discussion rows went from 885 to 1,805.
- **Settings-aware contradiction flag.** The flag key now includes batch, threads/ngl/config, pp/tg test lengths, and run number, so different runs and different setups of the same chip+model+quant pair no longer flag each other. Flags: contradiction 616 to 521, outlier 40 to 34.
- **Cluster scope.** Nine multi-GPU node rows (24x GB200 DSV4-Pro FP4 runs, 8x H200-NVL Gemma-4-31B, 4x GB200 GLM-5.3-Flash FP8 at three concurrency levels, 1x H20 DSV3.2) moved from the record set to `data/reference/cluster.json` (`scope: cluster`); the site lists them in a separate reference table so they do not mix with single-node rows.
- **Quote verification in CI.** New `scripts/check_quotes.py` re-fetches (from cache) every cited source page and verifies that every stored value, every pp/tg test token, and every quote fragment appears in the source. For SiliconScore, LLMCheck, and LLM Configurator the machine-readable dataset JSON is checked, since the stored numbers come from the dataset, not the per-row attribution page. Citations are now machine-checked, not just written.
- **22 new GitHub issue rows.** ExLlamaV2 #450 (2080 Ti, EXL2 4.0bpw, batched_inference and multi-cache scaling, 8 rows); vLLM #48071 (8x H200-NVL, Gemma-4-31B ITL by concurrency, 6 rows including the TRT-LLM row); #55139 (A100, GPT-OSS-20B, MRV1/MRV2); #49369/#49370 (B300, DeepSeek-V4-Flash FP4, base/no-break/dspark); #58031 (GB300, DeepSeek-V4.1-Flash MXFP4); #39323 (H100, Qwen3.5-35B-A3B FP8 with FlashAttention-3); #30832 (H20, DeepSeek-V3.2, cluster scope).
- All quotes re-verified verbatim against cached source pages; github_issues quotes are checked fragment by fragment, discussion quotes are checked against the paginated comment pages where the cited content actually renders.
- Dataset: 2,591 measured records, 287 hardware strings, 117 models, 19 backends, plus 549 reference estimates and 9 cluster runs. Provenance: 746 sourced, 1,845 community. Flags: 521 contradiction, 34 outlier.

## 2026-09-26: llama.cpp performance discussions collected (885 measured rows, 5 threads)

- New source `data/raw/llamacpp_discussions.json`: 885 measured community rows
  from the official llama.cpp performance threads (GitHub Discussions
  #4167 Apple Silicon, #15013 CUDA, #15021 ROCm, #10879 Vulkan, #23313
  SYCL). The collector (scripts/collect_llamacpp_discussions.py) parses
  primary-source llama-bench tables from every post, including the paginated
  "hidden items" windows and the curated M-series scoreboard in #4167.
- Hardware is attributed from post text and section headings (chip patterns
  per thread); rows without a detectable chip are skipped. Accelerator is
  taken from the benchmark's backend column, so backends are now qualified
  (llama.cpp (Metal), (CUDA), (Vulkan), (ROCm), (SYCL), (CPU), (RPC),
  (OpenCL), (OpenVINO)) for cross-backend comparison.
- Dataset: 1644 measured records, 265 hardware strings, 102 models, 19
  backends. Provenance: 746 sourced, 898 community. Flags: 310
  contradiction, 38 outlier (community threads publish repeated runs on the
  same setups, which is exactly what the contradiction flag is for).

## 2026-09-26: GitHub issue reports added (GB10, dual 5090; first vLLM and ExLlamaV2 rows); site link fix

- New source `data/raw/github_issues.json`: 7 hand-curated community rows quoted
  verbatim from GitHub issues (llama.cpp #28196 and #23010, ExLlamaV2 #806,
  vLLM #49548). Adds GB10 / DGX Spark and dual RTX 5090 coverage plus the
  first ExLlamaV2 row (RTX 5090 laptop, TinyLlama 1.1B EXL2) and the first
  vLLM measured row (GB10, Qwen3.5-122B-A10B INT4, MTP k=2).
- Dataset: 759 measured records, 134 hardware strings, 74 models, 11 backends.
- Fixed broken link prefixes in generated record tables: rows linked hardware
  to `/<slug>/` instead of `/hardware/<slug>/` and models to `/<slug>/` instead
  of `/models/<slug>/`; the hardware/model index lists used relative hrefs that
  doubled the directory prefix.
- CI now verifies every internal link in the built site
  (`scripts/check_links.py`, 4,800+ links across 210 pages).

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
