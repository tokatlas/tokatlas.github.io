# Changelog

## 2026-09-27: llama.cpp issue mining, second pass: 133 new rows across 15 issues

- **MTP6 vs baseline on three datacenter cards (llama.cpp #26750, 6 rows).** Qwen3.5-9B, b10290 official image, median of 108 runs per cell: draft-mtp n-max 6 vs no speculation - the W7900 goes 96 to 218 t/s and the RX 7800 XT 70 to 124, while the RTX PRO 4000 Blackwell drops 90 to 61.
- **RTX 5090 closed-loop server sweep (llama.cpp #27050, 8 rows).** Qwen2.5-7B-Instruct F16, 512+128 tokens per request at 1 and 32 concurrent: llama.cpp CUDA b9660 99.8/700.9, b10423 100.1/705.9, b10423 with the batching fix 101.4/1045.8, and vLLM BF16 92.9/1404.7.
- **DFlash on Strix Halo (llama.cpp #27117, 2 rows).** muse-glimmer 30B Q4_K on Radeon 8060S, 16 concurrent aggregate: 37 t/s with no speculation vs 80 with draft-dflash n-max 1 (0.83-0.92 acceptance, 2.2x the baseline).
- **Gated DeltaNet fused-op fix (llama.cpp #27327, 3 rows).** KAT-Coder-V2.5 on RTX 5080, three server-log runs after the fix (build 10154): 71.63/70.29/69.93 t/s.
- **ubatch and KV-quant interaction on R9700 (llama.cpp #27420, 4 rows).** qwen35 dense 27B at ctx 50000 with MTP3: ub256 f16 9.5, ub1024 f16 50, ub256 q8 53, ub1024 q8 60 t/s - the ubatch floor matters more than the KV quant.
- **Mamba2 flat-2d GEMM dispatch (llama.cpp #27464, 40 rows).** GB10 and RTX PRO 6000 Blackwell: Nemotron 3 Nano 30B-A3B NVFP4 across parallel-sequence lengths 1/8/32/256, current master vs the flat-2d fix (67.5 vs 67.7 at npl 1, 292.5 vs 660.8 at npl 256 on GB10; 1959.8 vs 3159.1 on the PRO 6000), plus Mamba2 2.7B, Falcon-H1 7B, and Granite 4.0 H Tiny at npl 32 in three quants each.
- **Vulkan vs ROCm MTP sweep on 2xR9700 (llama.cpp #27544, 20 rows).** Qwen3.8-27B UD-Q4_K_XL, n-max 1/2/3 across single, 2, and 3 parallel sessions: single-session TG 32-38 t/s on both backends; the 3-session aggregate peaks at 55.58 (Vulkan, n-max 1) and 71.42 (ROCm, n-max 3).
- **Draft-MTP race on Strix Halo (llama.cpp #27572, 4 rows).** Qwen3.8-27B on Radeon 8060S, the racing pre-workaround build: single-stream tg 16.3 to 25.3 t/s across 620 to 18256-token prompts.
- **Position sweep on RTX 4080 SUPER (llama.cpp #27623, 4 rows).** Qwen3.8-27B decode at KV positions 45574 to 91077: 35.6 to 33.1 t/s, then a cliff to 1.4 at position 91077 (q8 KV, no flash attention).
- **4x Tesla P40 decode (llama.cpp #27980, 5 rows).** Qwen3.8-Flash-Next: about 18 t/s at 150 tokens regardless of mmap, all-VRAM, or force-mmq; the 10B-active MoE reference on the same GPUs and build does 29.5.
- **500 ms stepping cliff on RTX 5060 Ti (llama.cpp #28218, 5 rows).** Qwen3.8-27B UD-IQ3_S with MTP: 38.8 t/s baseline, then 1.67 to 2.01 with tensor split 1 (official b10734 and a local MSVC build, dflash too), no-spec control 26.55.
- **CUDA vs Vulkan on RTX 5080 (llama.cpp #28274, 2 rows).** Qwen3.8-27B IQ4_XS on the b10766 builds: CUDA around 16 t/s, Vulkan settling at 35.59 (started at 40).
- **Arc Pro B70 deep-context MTP scan (llama.cpp #28721, 18 rows).** Qwen3.8-27B Q4_K_M, MTP3 draft at depth 1k/15k/32k/64k on Vulkan with q8 or f16 KV against SYCL, plus no-MTP controls: Vulkan drops to 4.3 at 64k depth while SYCL holds 15.8; MTP3 leads at 1k (35.6 vs 21.4 no-draft).
- **Flash-attention dispatch threshold on R9700 (llama.cpp #28867, 6 rows).** Qwen3.8-27B UD-Q4_K_XL with MTP3: 41.37 t/s on master, 51.62 at threshold 64 (51.70 on the pre-#28102 commit).
- **MTP exactness across builds (llama.cpp #29168, 6 rows).** RTX 2070 Super, gemma-4-26B-A4B-it QAT, partial offload ngl 31 + 21 CPU MoE: MTP 46.35 (b10750, byte-identical greedy output) vs 35.36 (b10964, the v0.4.1 build) vs 36.73 (b11057); plain 37.0 to 38.3.
- Also inspected and parked: #27256 (MTP acceptance-rate regression report, no clean tok/s value to quote) and #28828 (IQ4_XS prefill collapse on RX 7800 XT: 93.7 t/s prefill and 342.7 s TTFT only, no generation figure, so outside the row schema).
- New hardware pages: 2xR9700, 4x Tesla P40, Radeon AI PRO R9700, Radeon PRO W7900. New model pages include Nemotron 3 Nano 30B-A3B, Mamba2 2.7B, Falcon-H1 7B, Granite 4.0 H Tiny.
- Dataset: 2,794 measured records, 300 hardware strings, 146 models, 19 backends, plus 549 reference estimates and 11 cluster runs. Provenance: 746 sourced, 2,048 community. Flags unchanged: 521 contradiction, 34 outlier.

## 2026-09-27: llama.cpp issue mining pass: 24 new rows across eight issues

- **Deep-context RX 7900 XTX decode (llama.cpp #27734, 4 rows).** Qwen3.8-27B UD-Q4_K_XL, llama-server wall-clock decode: 40.4/40.8 t/s at ctx 65536/98304, a 8.9 t/s cliff at 131072 with the default KV-cache allocation, and 40.3 t/s at 131072 with a 4 GiB sub-allocated cache. First wall-clock (not llama-bench) rows; context depth is the row's independent variable.
- **Qwopus3.6-35B-A3B-Coder-MTP build comparison (llama.cpp #29410, 6 rows).** RX 7800 XT, Q4_K_M, two builds (c77ae695c, 84e76d8a2) across three test shapes: empty-context tg32+pp512, then MTP tg128 at 48k and 130k context. The MTP rows are flagged `spec` in notes.
- **Build regression on RTX 5070 Ti (llama.cpp #27171, 2 rows).** Qwen3.6-35B-A3B Q4_K_M, fit-target 1024: 101.00 t/s on build b10283 vs 87.92 on b10284 (pp512 1265.61 vs 923.45), 8 threads.
- **ROCm vs Vulkan on RX 6700 XT (llama.cpp #26702, 2 rows).** gemma-4-12b-it IQ4_NL, average of three runs: Vulkan 40.92 vs ROCm 34.6 t/s (pp512 354.4 vs 653.9) - the first entry on the new cross-backend notes page.
- **RTX 5060 Ti ceiling tests (llama.cpp #26674, 2 rows).** gemma-4-31B-it Q6_K at 0.62 t/s (pp512 41.84) and Qwen3.6-35B-A3B UD-Q6_K at 5.49 t/s (pp512 108.23) - models that fit with barely any headroom.
- **OpenVINO device naming (llama.cpp #29235, 4 rows).** Qwen2.5-7B-Instruct Q4_K_M on Arc Pro B70: the unmasked device (44.1 t/s at depth 128, 9.6 at 4096) vs the GPU.1 alias (59.7 / 41.1), with device identity kept as a `config=` token.
- **Ternary PTQ depth test (llama.cpp #29172, 2 rows).** Ternary-Bonsai-2-27B PTQ1_0 on RTX 5060 Ti: 44.68 t/s at depth 0 vs 8.10 at depth 154855 (pp 464.81 vs 21.87).
- **Dual-GPU split (llama.cpp #27137, 2 rows).** Qwen3.6-27B Q4_K_M across RTX 3060 + Intel Arc A770: build 9006 at 7.88 t/s vs build 10433 at 2.93, with the split ratio in notes.
- New conventions fixed by this pass: Unsloth Dynamic quant names (UD-Q4_K_XL, UD-Q6_K), ternary PTQ1_0, IQ4_NL in gguf form, and verbatim multi-GPU hardware strings from the issue body.
- Also inspected and skipped: #27181 (prompt-processing speeds only, no token-generation figure), #29341, #29323, #27097, #27682, #27366, #27373, #29154, #24437 (no complete hardware+model+t/s triple or values too thin to quote cleanly).
- Also fixed a latent bug in build_site.py: the cross-backend notes sort used the raw string tps, which crashes the moment that section has content to render.
- Dataset: 2,661 measured records, 295 hardware strings, 134 models, 19 backends, plus 549 reference estimates and 11 cluster runs. Provenance: 746 sourced, 1,915 community. Flags unchanged: 521 contradiction, 34 outlier.

## 2026-09-27: ExLlamaV2 issue pass: first row from the issue archive

- **Tesla P40 CodeLlama-34B (ExLlamaV2 #40, 1 row).** A 2023 report of 1.19 t/s (EXL2 4.0bpw H6, test_inference at length 1024, all seven positions between 1.17 and 1.19 t/s) with the card idling at 80 W under load; the same issue's 3090 driver-comparison figures (36/39 t/s) are not a row because the model is unnamed.
- Also inspected and skipped: #571 (no numbers), #734 (prompt-processing speeds only, no token-generation figure, so outside the row schema), #630 (an 11-16 t/s range with no named hardware), #499 (Q-Cache speeds, no hardware named).
- Dataset: 2,637 measured records, 294 hardware strings, 129 models, 19 backends, plus 549 reference estimates and 11 cluster runs. Provenance: 746 sourced, 1,891 community. Flags unchanged: 521 contradiction, 34 outlier.

## 2026-09-27: vLLM issue mining pass, second batch: 10 new rows across five issues

- **Qwen3.5-35B-A3B at concurrency 100 (vLLM #35625, 2 rows).** RTX PRO 6000 Blackwell Max-Q Workstation Edition (3341.89 tok/s) and DGX Spark (431.42 tok/s), both with Qwen3-Next MTP k=2 speculative decoding; the poster's TTFT tail-latency report, kept as measured rows with the TTFT numbers in notes.
- **EAGLE3 on Qwen3-8B (vLLM #40551, 4 rows).** RTX PRO 6000 Blackwell Workstation Edition, MT-Bench with 80 concurrent requests, EAGLE3 RedHatAI speculator k=7, across the MRV1/MRV2 model-runner tables at temperature 0 and 1 (2021.33 to 3936.20 tok/s); each table is a separate `config=` variant.
- **CPU whisper (vLLM #38586, 1 row).** whisper-medium on a dual-socket Xeon 6767P (torch CPU build, TP2), 9.08 output tok/s at 2.67x real-time on LibriSpeech ASR; first CPU row from the vLLM source.
- **Qwen3-VL-30B position-computation PR (vLLM #27021, 2 rows).** A100 PCIe, FP8 VLM, request-rate 10 RPS, before and after PR #25337 (681.42 vs 689.02 tok/s).
- **4x B300 Qwen3.5-397B-A17B NVFP4 (vLLM #40350, 1 cluster row).** TP4+EP4 with MTP3 at concurrency 512: 12921.2 tok/s aggregate in the engine log at Running 493, from the crash-report bench (the last request then hangs at 0.0 tok/s); added to the cluster reference area (now 11 runs).
- Skipped from the same search pass: #51799 (KV-cache concurrency headroom, no tok/s), #56868 (qualitative degeneration report), #44705 (latency table, no tok/s), #50880 (hang report, 0.0 tok/s only), #55394 (TTFT/kernel-ms table, no tok/s), #37666 (no model name in body).
- Dataset: 2,636 measured records, 293 hardware strings, 128 models, 19 backends, plus 549 reference estimates and 11 cluster runs. Provenance: 746 sourced, 1,890 community. Flags unchanged: 521 contradiction, 34 outlier.

## 2026-09-27: vLLM issue mining pass: 36 new rows across six issues

- **A100 multimodal benchmarks (vLLM #24728, 25 rows).** Four VLMs (Qwen2.5-VL-7B, MiniCPM-V-4, InternVL3.5-4B, InternVL3.5-2B) on a single A100 40 GB, image and video inputs, at the published concurrency levels (1, 10, 50 and the unlimited-rate max-QPS test). Modality is a machine-readable `config=` token, so image and video rows flag separately.
- **B200 DeepSeek-R1-0528 (vLLM #29662, 4 rows).** 8x B200 TP8 with MTP speculative decoding at concurrency 256, FP8 and FP4, with and without `--async-scheduling` (1994/2421/2375/2895 tok/s).
- **H100 Qwen3-8B FP8 (vLLM #48518, 2 rows).** Concurrency 4; the two runs differ only in L2 cache state persisting from server startup (809.40 vs 839.75 tok/s), kept as separate `config=` variants.
- **4090D Qwen2.5-14B (vLLM #36629, 2 rows).** FP8+EAGLE3 vs W4A16+EAGLE3 at batch 16 (1131.19 vs 1079.15 tok/s).
- **GPT OSS 120B kernel regression (vLLM #37441, 3 rows).** 8x H200 node, TP2, concurrency 1, eagle speculative decoding: vLLM 0.16.0/Triton 3.5 (275.84), vLLM 0.17.1/Triton 3.6 (231.22), and 0.17.1 with the reverted legacy kernels (275.84 recovered).
- **4x H200 DeepSeek-V4-Flash-FP8 (vLLM #43648, 1 cluster row).** DP4 + expert parallel crash-report run (1118.18 tok/s, 135 of 600 requests completed) added to the cluster reference area.
- Dataset: 2,627 measured records, 288 hardware strings, 126 models, 19 backends, plus 549 reference estimates and 10 cluster runs. Provenance: 746 sourced, 1,881 community. Flags unchanged: 521 contradiction, 34 outlier.

## 2026-09-27: Daily refresh: llama.cpp discussions re-retrieved, derived power values verified against published ranges

- Re-fetched every llama.cpp discussion page (all five performance threads, including all paginated windows) on 2026-09-27. No new rows: still 1,805 discussion records.
- `check_quotes` now accepts a stored power value when it falls inside a watt range the source publishes (for example "~220-230 W"). The collector derives per-row watts from the published W-per-t/s rate times the row's t/s, so the derived value is verified against the exact range it was derived from, instead of requiring the derived figure itself to appear as a point value on the page.
- The 4070 Ti Vulkan row consequently keeps the deterministic collector value (221 W at 110.53 t/s from the published ~2 W/tg/s rate), verified against the published 220-230 W nvtop range.

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
