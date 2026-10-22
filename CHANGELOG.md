# Changelog

## 2026-10-22: oMLX batch 682 (+52 rows)

- scan666 sweep (45 new traces), mined 52 records, +1 new model LFM2.5-24B-A2B-Uncensored-Heretic (4bit MLX); MAPs also for Huihui-Qwen3.8-27B-abliterated 6bit MLX, LFM2.5-24B-A2B MLX Serve mixed-4-8bit, and Qwen3.6-35B-A3B oQ3e MTP.
- Dataset 40190 -> 40242, community 39105 -> 39157. check_quotes green (40894 verified).

## 2026-10-22: oMLX batch 681 (+51 rows)

- scan665 sweep (45 new traces), mined 51 records, no new models; MAPs for Jundot Qwen3.8-Flash-Next oQ2.7e MTP (to the distinct Jundot:Qwen3.8-Flash-Next model), Qwen3.5-0.8B MTP, and Qwen3.8-27B-Uncensored oQ5e fp16 MLX MTP.
- Dataset 40139 -> 40190, community 39054 -> 39105. check_quotes green (40842 verified).

## 2026-10-22: oMLX batch 680 (+54 rows)

- scan664 sweep (45 new traces), mined 54 records, no new models (incl. Qwen3.8-27B-Abliterated bf16 MTP variant with a malformed page label).
- Dataset 40085 -> 40139, community 39000 -> 39054. check_quotes green (40791 verified).

## 2026-10-22: oMLX batch 679 (+50 rows)

- scan663 sweep (45 new traces), mined 50 records, +2 new models Huihui-GLM-4.7-Flash-abliterated (4bit MLX) and Qwen3.6-28B-REAP (oQ4); MAPs also for DeepSeek-V4.1-Flash 1017 build and Qwen3.8-27B-Abliterated bf16 MLX MTP.
- Dataset 40035 -> 40085, community 38950 -> 39000. check_quotes green (40737 verified).

## 2026-10-22: oMLX batch 678 (+49 rows)

- scan662 sweep (45 new traces), mined 49 records, no new models.
- Dataset 39986 -> 40035, community 38901 -> 38950. check_quotes green (40687 verified).

## 2026-10-22: oMLX batch 677 (+48 rows)

- scan661 sweep (45 new traces), mined 48 records, +1 new model Occamy-1.0-6bit-XL-mlx (6bit; XL size variant, kept as the full page-label form per the Devstral-4bit-mlx precedent since the page interleaves the quant token).
- Dataset 39938 -> 39986, community 38853 -> 38901. check_quotes green (40638 verified).

## 2026-10-22: oMLX batch 676 (+48 rows)

- scan660 sweep (45 new traces), mined 48 records, +1 new model BigBang-v1 (oQ6e MTP); MAPs for BigBang-v1, Qwen3.8-Flash-Next oct11 build, and lowercase glm-5.3-flash-uncensored oQ4e MTP.
- Dataset 39890 -> 39938, community 38805 -> 38853. check_quotes green (40590 verified).

## 2026-10-22: oMLX batch 675 (+50 rows)

- scan659 sweep (45 new traces), mined 50 records, +1 new model Phi-4-reasoning-plus (4bit MLX); MAPs for GLM-5.3 4bit, Phi-4-reasoning-plus 4bit MLX, and Qwen3.8-27B 4bit MLX (p4ik conversion).
- Dataset 39840 -> 39890, community 38755 -> 38805. check_quotes green (40542 verified).

## 2026-10-22: llama.cpp #30923 (LFM2.5-24B-A2B on Ryzen 7 8845H)

- llama.cpp PR #30923 (CPU softmax parallelism across head/batch dims): LFM2.5-24B-A2B Q4_K_M, CPU-only on AMD Ryzen 7 8845H (8 threads), 32K context, Q8_0 K-cache, F16 V-cache, flash-attn off. Mined 2 records (master 15.156, this PR 17.640 decode tok/s). New hardware AMD Ryzen 7 8845H.
- Dataset 39838 -> 39840, sourced 1083 -> 1085. check_quotes green (40492 verified).

## 2026-10-22: oMLX batch 674 (+42 rows)

- scan658 sweep (39 new traces), mined 42 records, +1 new model DeepSeek-R1-Distill-Qwen-14B (4bit); MAPs for DeepSeek-R1-Distill-Qwen-14B 4bit and GLM-5.3-Flash-UNCENSORED oQ5e.
- Dataset 39796 -> 39838, community 38713 -> 38755. check_quotes green (40490 verified).

## 2026-10-22: vLLM #63101 (GLM-5.3-MXFP4 on B300)

- vLLM PR #63101 (MXFP4 MoE activation quant, sorted_expert_ids direct index): E2E benchmark on RedHatAI/GLM-5.3-MXFP4, TP4 on B300, random 256 in / 1024 out, max-concurrency 1, fp8 KV cache. Mined 2 records (baseline 86.66, this PR 91.60 output tok/s, +5.7%).
- Dataset 39794 -> 39796, sourced 1081 -> 1083. check_quotes green (40448 verified).

## 2026-10-22: oMLX batch 673 (+44 rows)

- scan657 sweep (41 new traces), mined 44 records, no new models; MAP for Mellum2-12B-A2.5B-Instruct 8bit.
- Dataset 39750 -> 39794, community 38669 -> 38713. check_quotes green (40446 verified).

## 2026-10-22: vLLM #61435 re-sync + CI seed/prefetch fixes

- vLLM PR #61435 (Kimi-K3 MI355X) was rewritten upstream again: the DCP1/DCP8 MXFP4 table mined in batch 672 is gone, replaced by a TPOT-focused matrix plus a small InferenceX Output tok/s table. Dropped the 16 now-unverifiable rows and re-mined 4 from the new table (DCP1 auto 179.77, DCP1 specialized 232.87, DCP8 auto 164.79, DCP8 specialized 233.11 output tok/s, c1 k=7, TP8 on 8x MI355X; weight quant no longer stated, marked unstated).
- CI seed step fixed: `tar --keep-newer-files` exits 2 on every skipped file, which failed the job in ~6 minutes. The seed now unpacks to a temp dir and copies in with `cp -n` (same gap-fill, no-clobber, exit 0).
- CI prefetch fixed: the pool now submits only missing/stale URLs instead of all 13.9k, so warm cache hits no longer queue behind the ~900 stale oMLX re-fetches (prefetch dropped from ~2h13m toward the stale-set cost alone). Immutable oMLX trace pages are treated as authoritative once cached, so they are no longer re-fetched every run.
- Dataset 39762 -> 39750, sourced 1093 -> 1081. check_quotes green (40402 verified).

## 2026-10-22: CI quote-cache bootstrap fix

- The data-checks job could not go green: a cold run cannot fetch the ~13k immutable oMLX trace pages inside the job timeout (omlx 429-throttles concurrent bursts), so the actions cache only ever saved a partial copy and every run re-cold-fetched. Added a parallel prefetch phase (per-host connection cap, same per-connection throttle) and a pre-warmed release-asset seed that tops up the cache each run; raised the job timeout to 240m.
- Some oMLX source traces have since been pruned upstream (HTTP 404). Those records stay verified against the cached copy, consistent with the standing rule for sources that block datacenter fetches: the measurement was real and the quote is verbatim from the archived page.
- Dataset unchanged at 39762 records, 715 models.

## 2026-10-18: oMLX batch 672 (+37 rows) + upstream source-rewrite sweep

- scan656 sweep (37 new traces), mined 37 records, no new models; MAP for ThinkingCap-Qwen3.8-27B mxfp8 MLX.
- Upstream rewrites of six vLLM/llama.cpp PR bodies surfaced as caches aged out; re-verified all 264 GitHub PR sources fresh and repaired every affected record:
  - vLLM #61694 (Kimi-K3 MI355X): old AgenticX conc8 table removed; re-mined 4 records from the new AgentX conc4 InferenceX recipe table (main 174.25, BF16 175.70, +latency_specialized 180.98, this PR 190.90 output tok/s), dropped 7 stale rows.
  - vLLM #61109 (Qwen2.5-72B MI210): body rewritten to an ISLAND all-reduce backend with TPOT/TTFT-only tables and delta claims; no absolute tok/s left, dropped 10 throughput records.
  - vLLM #61435 (Kimi-K3 MI355X): InferenceX table removed (dropped 3); DCP1/DCP8 tables merged into one wide table, re-pointed 16 fragments to the contiguous value pairs.
  - vLLM #61682 (DeepSeek-V4.1-Flash MI325X): table reformatted to per-shape TTFT/TPOT/E2E/Output blocks; re-pointed 10 fragments to the Output (tok/s) rows (MXFP8 no longer restated, kept in notes).
  - vLLM #61903 (MiniMax-M2.5 2xH200): benchmark re-run to four runs per arm; re-mined 2 records (main 1422, PR 1518 output tok/s), dropped 4 stale rows.
  - llama.cpp #30738 (Radeon HD 7900 K/V): context/hardware phrasing reordered; re-pointed 8 fragments (values unchanged).
- Dataset 39743 -> 39762, community 38632 -> 38669, sourced 1111 -> 1093. check_quotes green (40414 verified).

## 2026-10-18: oMLX batch 671 (+48 rows)

- scan655 sweep (45 new traces), mined 48 records, no new models; MAP for Ornith-1.5-35B-A3B oQ4e fp16.
- Dataset 39695 -> 39743, community 38584 -> 38632. check_quotes green (40395 verified).

## 2026-10-18: oMLX batch 670 (+49 rows)

- scan654 sweep (45 new traces), mined 49 records, +3 new models Huihui-MiniCPM-V-4.6-abliterated (bf16 MLX), Hy-Memory-30B-A3B (MLX Mixed4-6), Jundot--GLM-5.3-Flash (oQ4e); MAPs for Ling-mini-2.0 2bit DWQ, Qwen3.8-27B oQ6e fp16 MLX MTP, Spark-X2.5-4B oQ6e fp16, gemma-4-26B-A4B-it mxfp4.
- Dataset 39646 -> 39695, community 38535 -> 38584. check_quotes green (40347 verified).

## 2026-10-18: oMLX batch 669 (+48 rows)

- scan653 sweep (45 new traces), mined 48 records, no new models; MAP for Ornith-1.5-35B-A3B oQ4 fp16 MLX.
- Dataset 39598 -> 39646, community 38487 -> 38535. check_quotes green (40298 verified).

## 2026-10-18: oMLX batch 668 (+55 rows)

- scan652 sweep (45 new traces), mined 55 records, +2 new models Qwen3.8-27B-JANG_4D (4bit), Ternary-Bonsai-2-2B (2bit MLX).
- Dataset 39543 -> 39598, community 38432 -> 38487. check_quotes green (40250 verified).

## 2026-10-18: oMLX batch 667 (+54 rows)

- scan651 sweep (45 new traces), mined 54 records, no new models.
- Dataset 39489 -> 39543, community 38378 -> 38432. check_quotes green (40195 verified).

## 2026-10-18: oMLX batch 666 (+50 rows)

- scan650 sweep (45 new traces), mined 50 records, no new models.
- Dataset 39439 -> 39489, community 38328 -> 38378. check_quotes green (40141 verified).

## 2026-10-18: oMLX batch 665 (+51 rows)

- scan649 sweep (45 new traces), mined 51 records, no new models; MAPs for Qwen3.8-27B-Abliterated oQ4e MTP, Qwen3.8-27B oQ8 fp16 VLM MTP.
- Dataset 39388 -> 39439, community 38277 -> 38328. check_quotes green (40091 verified).

## 2026-10-18: oMLX batch 664 (+49 rows)

- scan648 sweep (43 new traces), mined 49 records, +1 new model Ling-mini-2.0 (4bit); MAPs for Bonsai-8B 1bit MLX, NVIDIA-Nemotron-3.5-Bolt-74B-A9B 5bit, Qwen3.8-Flash-Next oQ4e MTP BF16 ngram.
- Dataset 39339 -> 39388, community 38228 -> 38277. check_quotes green (40040 verified).

## 2026-10-18: oMLX batch 663 (+48 rows)

- scan647 sweep (41 new traces), mined 48 records, no new models; MAPs for Cyber-Tiel-Coder-35B-A3B oQ4e fp16 MLX, LFM2.5-8B-A1B OptiQ 4bit.
- Dataset 39291 -> 39339, community 38180 -> 38228. check_quotes green (39991 verified).

## 2026-10-18: oMLX batch 662 (+62 rows)

- scan646 sweep (45 new traces), mined 62 records, +1 new model gemma-3-4b-it (4bit DWQ); MAP for gemma-3-4b-it DWQ.
- Source-rewrite fixes: llama.cpp PR #30047 table re-measured, 12 records re-synced to current values; llmcheck Maple Preview 20B-A1B re-synced (281 to 387 tps, re-pointed to benchmarks.json); 1 llmcheck row dropped (upstream now marks it estimated).
- Dataset 39229 -> 39291, community 38118 -> 38180. check_quotes green (39943 verified).

## 2026-10-18: oMLX batch 661 (+62 rows)

- scan645 sweep (58 new traces), mined 62 records, no new models; MAPs for DeepSeek-V4.1-Flash oQ2.5e MTP (1017 build), K2-Horizon-7B oQ4e, Kolibri-1 8bit MLX.
- Dataset 39167 -> 39229, community 38056 -> 38118. check_quotes green (39882 verified).

## 2026-10-18: oMLX batch 660 (+64 rows)

- scan644 sweep (60 new traces), mined 64 records, no new models; MAP for Qwen3.8-9B-heretic-uncensored 5bit MLX.
- Dataset 39103 -> 39167, community 37992 -> 38056. check_quotes green (39820 verified).

## 2026-10-18: oMLX batch 659 (+64 rows)

- scan643 sweep (58 new traces), mined 64 records, +1 new model Qwen3.6-35B-A3B-Holo3-Qwopus-Instruct (qx64-hi MLX); MAP for MiniCPM5-2B 8bit MLX.
- Dataset 39039 -> 39103, community 37928 -> 37992. check_quotes green (39756 verified).

## 2026-10-18: oMLX batch 658 (+65 rows)

- scan642 sweep (60 new traces), mined 65 records, no new models; MAP for DeepSeek-V4.1-Flash oQ4e MTP (1017 dated build).
- Dataset 38974 -> 39039, community 37863 -> 37928. check_quotes green (39692 verified).

## 2026-10-18: oMLX batch 657 (+63 rows)

- scan641 sweep (60 new traces), mined 63 records, +1 new model gemma-4-E2B-it-qat (8bit); MAP for gemma-4-E2B-it TurboQuant 8bit MLX.
- Dataset 38911 -> 38974, community 37800 -> 37863. check_quotes green (39627 verified).

## 2026-10-18: oMLX batch 656 (+68 rows)

- scan640 sweep (60 new traces), mined 68 records, no new models; MAP for DeepSeek-V4.1-Flash oQ3e MTP (1017 dated build).
- Dataset 38843 -> 38911, community 37732 -> 37800. check_quotes green (39564 verified).

## 2026-10-18: oMLX batch 655 (+64 rows)

- scan639 sweep (60 new traces), mined 64 records, no new models.
- Dataset 38779 -> 38843, community 37668 -> 37732. check_quotes green (39496 verified).

## 2026-10-18: oMLX batch 654 (+65 rows)

- scan638 sweep (60 new traces), mined 65 records, no new models; MAP for Llama 3.3 70B Instruct 4bit (non-prefixed form).
- Dataset 38714 -> 38779, community 37603 -> 37668. check_quotes green (39432 verified).

## 2026-10-18: oMLX batch 653 (+66 rows)

- scan637 sweep (58 new traces), mined 66 records, +1 new model Agents-A1-4B (oQe4); MAP for gpt-oss 20B OptiQ 4bit fp16; fixed recurring occamy-1.0 slug collision (lowercase oQ4e MAP now maps to Occamy-1.0).
- Dataset 38648 -> 38714, community 37537 -> 37603. check_quotes green (39367 verified).

## 2026-10-18: oMLX batch 652 (+67 rows)

- scan636 sweep (60 new traces), mined 67 records, no new models; MAPs for MiniCPM-V-4.7-35B-A3B OptiQ REAP-19B 4bit, Nex-N2.5-mini oQ8 MLX, Qwen3.6-35B-A3B 6bit-XL (plain + MTP) MLX, Qwen3-Coder-30B-A3B-Instruct 4bit MLX.
- Dataset 38581 -> 38648, community 37470 -> 37537. check_quotes green (39301 verified).

## 2026-10-18: oMLX batch 651 (+69 rows)

- scan635 sweep (60 new traces), mined 69 records, no new models; MAP for Qwen3.5-35B-A3B 6bit.
- Dataset 38512 -> 38581, community 37401 -> 37470. check_quotes green (39234 verified).

## 2026-10-18: oMLX batch 650 (+63 rows)

- scan634 sweep (57 new traces), mined 63 records, +2 new models: DeepSeek-V4.1-Flash-Abliterated (MLX) and Hermes-4.3-36B (5bit MLX);
  MAPs for DeepSeek-V4-Flash-0731 oQ2e, Llama 3.3 70B Instruct 4bit.
- Dataset 38449 -> 38512, community 37338 -> 37401. check_quotes green (39165 verified).

## 2026-10-18: oMLX batch 649 (+65 rows)

- scan633 sweep (60 new traces), mined 65 records, no new models.
- Dataset 38384 -> 38449, community 37273 -> 37338. check_quotes green (39102 verified).

## 2026-10-18: oMLX batch 648 (+62 rows)

- scan632 sweep (57 new traces), mined 62 records, no new models; MAP for Underdog-27B-1.1 4bit MLX.
- Dataset 38322 -> 38384, community 37211 -> 37273. check_quotes green (39037 verified).

## 2026-10-18: oMLX batch 647 (+69 rows)

- scan631 sweep (60 new traces), mined 69 records, no new models; MAPs for Qwen3.5-9B-The-Defiant-Fable-Uncensored-Heretic-NEO-IMATRIX-MAX oQ4e-fp16 MTP (existing hyphen form) and prism-ml Ternary-Bonsai-27B 2bit MLX.
- Dataset 38253 -> 38322, community 37142 -> 37211. check_quotes green (38975 verified).

## 2026-10-18: oMLX batch 646 (+67 rows)

- scan630 sweep (60 new traces), mined 67 records, no new models; MAP for Qwen3.6-35B-A3B nvfp4.
- Dataset 38186 -> 38253, community 37075 -> 37142. check_quotes green (38906 verified).

## 2026-10-18: oMLX batch 645 (+74 rows)

- scan629 sweep (60 new traces), mined 74 records, no new models; MAPs for NVIDIA-Nemotron-3.5-Bolt-74B-A9B 24GB LiLiCorr MLX (quant unstated), NVIDIA-Nemotron-3.5-Lightning-30B-A3B oQ8e MTP, Qwen3.6-35B-A3B-Heretic 4bit MLX.
- Dataset 38112 -> 38186, community 37001 -> 37075. check_quotes green (38839 verified).

## 2026-10-18: oMLX batch 644 (+68 rows)

- scan628 sweep (60 new traces), mined 68 records, +5 new models: Ministral-3-3B-Reasoning-2512 (4bit),
  Qwen3.6-27B-Architect-Polaris2-Fable-B-F451 (oQ4 MTP), ...F451-Medical (mxfp8), ...F451-Tess-1M (qx64-hi),
  Qwen3.6-27B-Fable-Fusion-711-BigBubba-717 (mxfp8); MAP for Tiel-Coder-35B-A3B oQ6e MLX.
- Dataset 38044 -> 38112, community 36933 -> 37001. check_quotes green (38765 verified).

## 2026-10-18: oMLX batch 643 (+64 rows)

- scan627 sweep (60 new traces), mined 64 records, +1 new model dots.mocr (8bit);
  MAPs for Nemotron-3-Super-120B-A12B 4bit MLX, Qwen3.8-27B-MindMeld-AREX mxfp8 MLX, Qwen3.8-Flash-Next oQ4e WLSRefit MTP.
- Dataset 37980 -> 38044, community 36869 -> 36933. check_quotes green (38697 verified).

## 2026-10-18: oMLX batch 642 (+64 rows)

- scan626 sweep (60 new traces), mined 64 records, no new models; MAPs for Mellum2.1-12B-A2.5B-Thinking oQ4, Qwen2.5-VL-7B-Instruct 8bit, gemma-3-12b-it 4bit.
- Dataset 37916 -> 37980, community 36805 -> 36869. check_quotes green (38633 verified).

## 2026-10-18: oMLX batch 641 (+69 rows)

- scan625 sweep (60 new traces), mined 69 records, +2 new models: Step-3.7-Flash (oQ8 MLX) and gemma-3-4b-pt (4bit, pretrained base distinct from gemma-3-4b-it-qat);
  MAPs for Kimi-K3 REAP80 mxfp4 MLX, MiniMax-M3 4bit, Qwen3.8-Flash-Next-Uncensored 8bit MLX, Step-3.7-Flash, gemma-3-4b-pt.
- Dataset 37847 -> 37916, community 36736 -> 36805. check_quotes green (38569 verified).

## 2026-10-17: oMLX batch 640 (+66 rows) + llama.cpp #30752 (+12 rows)

- scan624 sweep (60 new traces), mined 66 records, +2 new models: drowzeys-DeepSeek-V4-Flash-0731-MXFP4-MLX-Abliterated (4bit) and Qwen3.6-35B-A3B-4bit-MTPLX-Optimized-Speed (4bit, page title distinct from the existing non-4bit form); MAPs for GLM-5.3-Flash oQ2.5e MTP, Qwen2.5-7B-Instruct 4bit, drowzeys, and the 4bit-MTPLX form.
- llama.cpp PR #30752 (SYCL q8 fast dequant, Intel Arc Pro B70): 12 records from the in-tree A/B table (llama-perplexity t/s, mainline vs PR arms, 6 model/quant rows including 2-run Q8_0 and dual-device UD-Q8_K_4XL).
- Dataset 37769 -> 37847, community 36670 -> 36736, sourced 1099 -> 1111. check_quotes green (38500 verified).

## 2026-10-17: oMLX batch 639 (+67 rows)

- scan623 sweep (60 new traces), mined 67 records, no new models; MAPs for
  Ornith-1.5-9B MLX (quant unstated) and Qwen3.8-27B 4bit (triple-underscore page form).
- Dataset 37702 -> 37769, community 36603 -> 36670. check_quotes green (38422 verified).

## 2026-10-17: oMLX batch 638 (+62 rows)

- scan622 sweep (60 new traces), mined 62 records, no new models.
- Dataset 37640 -> 37702, community 36541 -> 36603. check_quotes green (38355 verified).

## 2026-10-17: oMLX batch 637 (+71 rows)

- scan621 sweep (60 new traces), mined 71 records, no new models; MAPs for Qwen3.8-Flash-Next oQ5 mixed MTP and gemma-4-E4B-it oQ4 MTP.
- Dataset 37569 -> 37640, community 36470 -> 36541. check_quotes green (38293 verified).

## 2026-10-17: oMLX batch 636 (+68 rows)

- scan620 sweep (60 new traces), mined 68 records, no new models.
- Dataset 37501 -> 37569, community 36402 -> 36470. check_quotes green (38222 verified).

## 2026-10-17: oMLX batch 635 (+66 rows)

- scan619 sweep (60 new traces), mined 66 records, +1 new model medgemma-27b-it (bf16);
  MAP for medgemma-27b-it bf16.
- Dataset 37435 -> 37501, community 36336 -> 36402. check_quotes green (38154 verified).

## 2026-10-17: oMLX batch 634 (+71 rows)

- scan618 sweep (60 new traces), mined 71 records, no new models; MAP for LFM2.5-24B-A2B bf16 MLX.
- Dataset 37364 -> 37435, community 36265 -> 36336. check_quotes green (38088 verified).

## 2026-10-17: oMLX batch 633 (+65 rows)

- scan617 sweep (60 new traces), mined 65 records, no new models; MAP for NVIDIA-Nemotron-3.5-Lightning-30B-A3B bf16.
- Dataset 37299 -> 37364, community 36200 -> 36265. check_quotes green (38017 verified).

## 2026-10-17: oMLX batch 632 (+66 rows)

- scan616 sweep (60 new traces), mined 66 records, +1 new model Qwen2-VL-2B-Instruct (quant unstated on page); MAP for Qwen2-VL-2B-Instruct.
- Dataset 37233 -> 37299, community 36134 -> 36200. check_quotes green (37952 verified).

## 2026-10-17: oMLX batch 631 (+67 rows) + source-rewrite fixes

- scan615 sweep (60 new traces), mined 67 records, no new models; MAPs for Ornith-1.5-9B oQ5e fp16 MTP and KAT-Coder-V2.5-Dev OptiQ REAP-18B 4bit.
- Source rewrites repaired in the same pass: llama.cpp #29534 gfx906 table removed upstream (10 records dropped); Ornith-1.5-35B-A3B R9700 card re-benchmarked with WHIRL 0.2.0 (6 old R9700 rows replaced by 12 fresh llama.cpp ROCm rows across 2k-128k); Swift-1.5 and Luigi cards re-fetched with patched quote fragments.
- Dataset 37170 -> 37233, community 36071 -> 36134. check_quotes green (37886 verified).

## 2026-10-17: oMLX batch 630 (+68 rows)

- scan614 sweep (60 new traces), mined 68 records, no new models or hardware.
- Dataset 37102 -> 37170, community 36003 -> 36071. check_quotes green (37823 verified).

## 2026-10-17: oMLX batch 629 (+67 rows)

- scan613 sweep (60 new traces), mined 67 records, no new models; MAP for Qwen3-30B-A3B-Instruct-2507 4bit.
- Dataset 37035 -> 37102, community 35936 -> 36003. check_quotes green (37755 verified).

## 2026-10-17: oMLX batch 628 (+71 rows)

- scan612 sweep (60 new traces), mined 71 records, no new models; MAP for GLM-5.3-Flash-UNCENSORED oQ4e MTP.
- Dataset 36964 -> 37035, community 35865 -> 35936. check_quotes green (37688 verified).

## 2026-10-17: llama.cpp PR #30738 (+8 rows)

- Vulkan Q4_0 KV dequant fast path PR, llama-bench pp512/tg128 before/after on Qwen3.5-4B Q4_K_M at 32K ctx, q4_0/q4_0 and q8_0/q4_0 KV arms; new hardware AMD Radeon HD 7900 (GCN1/radv).
- Dataset 36956 -> 36964, sourced 1091 -> 1099. check_quotes green (37617 verified).

## 2026-10-17: oMLX batch 627 (+68 rows)

- scan611 sweep (60 new traces), mined 68 records, no new models; MAP for Mellum2.1-12B-A2.5B-Thinking oQ8e.
- Dataset 36888 -> 36956, community 35797 -> 35865. check_quotes green (37609 verified).

## 2026-10-17: oMLX batch 626 (+68 rows)

- scan610 sweep (60 new traces), mined 68 records, +2 new models LFM2.5-24B-A2B-abliterated (4bit MLX) and Ternary-Bonsai-2-27B-Uncensored-Heretic-v2 (2bit MLX compact); MAPs for Qwen3.6-35B-A3B mixed 3/4bit and Qwen3.8-Flash-Next-Uncensored mixed.
- Dataset 36820 -> 36888, community 35729 -> 35797. check_quotes green (37541 verified).

## 2026-10-17: oMLX batch 625 (+66 rows)

- scan609 sweep (60 new traces), mined 66 records, no new models; MAP for LFM2.5-2.6B oQ8e.
- Dataset 36754 -> 36820, community 35663 -> 35729. check_quotes green (37473 verified).

## 2026-10-17: oMLX batch 624 (+59 rows)

- scan608 sweep (55 new traces), mined 59 records, no new models; MAPs for Nemotron-3-Super-120B-A12B 6bit MLX, Nemotron-3.5-Lightning-30B-A3B mxfp4 MLX, Qwen3.8-Flash-Next oQ6e fp16 MTP.
- Dataset 36695 -> 36754, community 35604 -> 35663. check_quotes green (37407 verified).

## 2026-10-17: oMLX batch 623 (+58 rows)

- scan607 sweep (54 new traces), mined 58 records, no new models or hardware.
- Dataset 36637 -> 36695, community 35546 -> 35604. check_quotes green (37348 verified).

## 2026-10-17: oMLX batch 622 (+62 rows)

- scan606 sweep (56 new traces), mined 62 records, no new models; MAP for Occamy-1.0 oQ5e MTP.
- Dataset 36575 -> 36637, community 35484 -> 35546. check_quotes green (37290 verified).

## 2026-10-17: oMLX batch 621 (+63 rows)

- scan605 sweep (58 new traces), mined 63 records, no new models; MAP for NVIDIA-Nemotron-3.5-Lightning-30B-A3B oQ4.
- Dataset 36512 -> 36575, community 35421 -> 35484. check_quotes green (37228 verified).

## 2026-10-17: oMLX batch 620 (+65 rows)

- scan604 sweep (60 new traces), mined 65 records, +2 new models Qwen3.5-9b-Sushi-Coder-RL (4bit MLX) and Ternary-Bonsai-8B (2bit MLX); MAPs for LFM2.5-24B-A2B DWQ 3bit v2 and gemma-4-26B-A4B-it nvfp4.
- Dataset 36447 -> 36512, community 35356 -> 35421. check_quotes green (37165 verified).

## 2026-10-17: oMLX batch 619 (+67 rows)

- scan603 sweep (60 new traces), mined 67 records, +1 new model MiMo-V2.6-Distill-Qwen-9B-Ablitrated (oQ4e); MAPs for K2-Horizon-MoVA-36B-A4B oQ8e and Gemma 4 26B-A4B 8bit.
- Dataset 36380 -> 36447, community 35289 -> 35356. check_quotes green (37100 verified).

## 2026-10-17: oMLX batch 618 (+69 rows)

- scan602 sweep (60 new traces), mined 69 records, no new models; MAPs for Ornith-1.5-35B-A3B oQ6 MTP, gemma-4-26B-A4B-it oQ8e, gemma-4-E2B-it oQ3.
- Dataset 36311 -> 36380, community 35220 -> 35289. check_quotes green (37033 verified).

## 2026-10-17: oMLX batch 617 (+64 rows)

- scan601 sweep (58 new traces), mined 64 records, no new models; MAP for Qwen3.5-4B 8bit.
- Dataset 36247 -> 36311, community 35156 -> 35220. check_quotes green (36964 verified).

## 2026-10-17: oMLX batch 616 (+64 rows)

- scan600 sweep (60 new traces), mined 64 records, +1 new model Nemotron-3.5-Lightning-30B-A3B-refusal-ablated (8bit MTP MLX).
- Dataset 36183 -> 36247, community 35092 -> 35156. check_quotes green (36900 verified).

## 2026-10-17: oMLX batch 615 (+69 rows)

- scan599 sweep (60 new traces), mined 69 records, no new models; MAP for Qwen3.8-27B-Abliterated 6bit MTP MLX.
- Dataset 36114 -> 36183, community 35023 -> 35092. check_quotes green (36836 verified).

## 2026-10-17: oMLX batch 614 (+64 rows)

- scan598 sweep (56 new traces), mined 64 records, no new models; MAP for Qwen3.6-35B-A3B oQ4 fp16 MLX.
- Dataset 36050 -> 36114, community 34959 -> 35023. check_quotes green (36767 verified).

## 2026-10-17: llama.cpp PR #30728 (+19 rows)

- Metal GQA vec decode PR, master-arm baseline decode tok/s on M4 Max 128 GB (19 rows, 9 models, ctx 2k-100k); +2 new models GLM-4-9B-0414 and SmolLM2-1.7B, Llama-3.1-8B aliased to Llama 3.1 8B.
- Dataset 36031 -> 36050, sourced 1072 -> 1091. check_quotes green (36703 verified).

## 2026-10-17: oMLX batch 613 (+65 rows)

- scan597 sweep (58 new traces), mined 65 records, no new models; MAP for Agents-A1 oQ8e MLX.
- Dataset 35966 -> 36031, community 34894 -> 34959. check_quotes green (36684 verified).

## 2026-10-17: oMLX batch 612 (+66 rows)

- scan596 sweep (60 new traces), mined 66 records, +2 new models Dirk-Qwen3.8-27B (oQ4e MLX) and StartLux-Decision-v1.1-9B-AutoThink (8bit MLX); MAPs for gemma-4-12B-it-qat 4bit and gemma-4-12B nvfp4.
- Dataset 35900 -> 35966, community 34828 -> 34894. check_quotes green (36619 verified).

## 2026-10-17: oMLX batch 611 (+63 rows)

- scan595 sweep (59 new traces), mined 63 records, +1 new model Mistral-Small-24B-Instruct-2501 (4bit); MAP for Agents-A1 MLX (quant unstated on page).
- Dataset 35837 -> 35900, community 34765 -> 34828. check_quotes green (36553 verified).

## 2026-10-17: oMLX batch 610 (+63 rows)

- scan594 sweep (60 new traces), mined 63 records, no new models; MAPs for GLM-5.3-Flash 6bit MLX, Qwen3.5-2B bf16, gemma-4-E4B-it-qat mxfp4.
- Dataset 35774 -> 35837, community 34702 -> 34765. check_quotes green (36490 verified).

## 2026-10-17: oMLX batch 609 (+66 rows)

- scan593 sweep (60 new traces), mined 66 records, +1 new model Qwen3.6-27B-Claude-Opus-Reasoning-Distill-v2-abliterated (4bit OptiQ MLX); MAPs for GLM-5.3-Flash-UNCENSORED 6bit MLX and Occamy-1.0 oQ4e.
- Dataset 35708 -> 35774, community 34636 -> 34702. check_quotes green (36427 verified).

## 2026-10-17: oMLX batch 608 (+58 rows)

- scan592 sweep (56 new traces), mined 58 records, no new models or hardware.
- Dataset 35650 -> 35708, community 34578 -> 34636. check_quotes green (36361 verified).

## 2026-10-17: oMLX batch 607 (+60 rows)

- scan591 sweep (58 new traces), mined 60 records, +1 new model Qwen3.6-35B-A3B-Fable-5-Distill (oQ6 fp16 MTP); MAP for GLM-5.3 MLX mixed 4/8bit.
- Dataset 35590 -> 35650, community 34518 -> 34578. check_quotes green (36303 verified).

## 2026-10-17: oMLX batch 606 (+65 rows)

- scan590 sweep (60 new traces), mined 65 records, +1 new model Ternary-Bonsai-2-4B (2bit MLX); MAP for Qwen2.5-1.5B-Instruct 4bit.
- Dataset 35525 -> 35590, community 34453 -> 34518. check_quotes green (36243 verified).

## 2026-10-17: oMLX batch 605 (+67 rows)

- scan589 sweep (60 new traces), mined 67 records, +1 new model Qwen3.8-27B-MLX-AD-4.50bpw-DWQ-16.0GB (4bit DWQ); MAPs for MiniCPM-V-4.7-35B-A3B MLX serve 4bit, NVIDIA-Nemotron-3.5-Lightning-30B-A3B 4bit, Qwen3.5-2B 4bit; Swift-1.5 records mapped to space form.
- Dataset 35458 -> 35525, community 34386 -> 34453. check_quotes green (36178 verified).

## 2026-10-17: oMLX batch 604 (+64 rows)

- scan588 sweep (60 new traces), mined 64 records, no new models or hardware.
- Dataset 35394 -> 35458, community 34322 -> 34386. check_quotes green (36111 verified).

## 2026-10-17: oMLX batch 603 (+62 rows)

- scan587 sweep (53 new traces), mined 62 records, no new models or hardware.
- Dataset 35332 -> 35394, community 34260 -> 34322. check_quotes green (36047 verified).

## 2026-10-17: oMLX batch 602 (+56 rows)

- scan586 sweep (55 new traces), mined 56 records, +1 new model Nail-Qwen3.6-35B-A3B (8bit MLX); MAPs for LFM2.5-24B-A2B bf16 MLX and Qwen3.8-27B Q4_K_M llama.cpp MLX.
- Dataset 35276 -> 35332, community 34204 -> 34260. check_quotes green (35985 verified).

## 2026-10-17: oMLX batch 601 (+62 rows)

- scan585 sweep (60 new traces), mined 62 records, +2 new models Qwen3.8-27B-Coder390-EfficientThink-DFlash2 (oQ8e MTP) and Ternary-Bonsai-2-9B (2bit MLX).
- Dataset 35214 -> 35276, community 34142 -> 34204. check_quotes green (35929 verified).

## 2026-10-17: oMLX batch 600 (+65 rows)

- scan584 sweep (60 new traces), mined 65 records, no new models; MAP for Ornith-1.5-35B-A3B oQ8e fixed MTP.
- Dataset 35149 -> 35214, community 34077 -> 34142. check_quotes green (35867 verified).

## 2026-10-17: oMLX batch 599 (+58 rows)

- scan583 sweep (58 new traces), mined 58 records, +1 new model LFM2.5-1.2B-Thinking (8bit).
- Dataset 35091 -> 35149, community 34019 -> 34077. check_quotes green (35802 verified).

## 2026-10-17: oMLX batch 598 (+69 rows)

- scan582 sweep (60 new traces), mined 69 records, +2 new models Huihui-gemma-4-31B-it-v2 (8bit MLX) and Qwen3-Next-80B-A3B-Instruct-1M (6bit qx64n MLX), plus the Coder390 distill chain (oQ8e fp16 MTP).
- Dataset 35022 -> 35091, community 33950 -> 34019. check_quotes green (35744 verified).

## 2026-10-17: oMLX batch 597 (+63 rows)

- scan581 sweep (60 new traces), mined 63 records, +2 new models LFM2.5-1.2B-Instruct (4bit MLX) and Muse-Spark-Open-816B-A42B (oQ3e).
- Dataset 34959 -> 35022, community 33887 -> 33950. check_quotes green (35675 verified).
- CI note: batch 596 run flaked on a cold fetch timeout (omlx.ai trace pkzedvud, no cache in CI since .cache is gitignored); re-run green.

## 2026-10-17: oMLX batch 596 (+65 rows)

- scan580 sweep (60 new traces), mined 65 records, +1 new model Mistral-Medium-3.5-128B (4bit).
- Dataset 34894 -> 34959, community 33822 -> 33887. check_quotes green (35612 verified).

## 2026-10-17: oMLX batch 595 (+69 rows)

- scan579 sweep (60 new traces), mined 69 records, no new models or hardware.
- Dataset 34825 -> 34894, community 33753 -> 33822. check_quotes green (35547 verified).

## 2026-10-17: oMLX batch 594 (+60 rows)

- scan578 sweep (60 new traces), mined 60 records, no new models; MAPs for Qwen3.6-35B-A3B oQ4 and Qwen3.8-Flash-Next oQ4 MTP.
- Dataset 34765 -> 34825, community 33693 -> 33753. check_quotes green (35478 verified).

## 2026-10-17: oMLX batch 593 (+67 rows)

- scan577 sweep (60 new traces), mined 67 records, no new models (Muse-Glimmer mapped to space form "Muse Glimmer"); MAPs for Muse-Glimmer 4bit MLX, Ornith-1.0-35B OptiQ 4bit, Spark-X2.5-4B OptiQ 4bit.
- Dataset 34698 -> 34765, community 33626 -> 33693. check_quotes green (35418 verified).

## 2026-10-17: oMLX batch 592 (+72 rows)

- scan576 sweep (57 new traces), mined 72 records, no new models; MAP for Qwen3-Coder-30B-A3B-Instruct 3bit.
- Dataset 34626 -> 34698, community 33554 -> 33626. check_quotes green (35351 verified).

## 2026-10-17: oMLX batch 591 (+54 rows)

- scan575 sweep (60 new traces), mined 54 records, +3 new models NVIDIA-Nemotron-3.5-Bolt-74B-A9B (oQ4e fp16), NVIDIA-Nemotron-3.5-Super-VL-120B-A12B (4bit MLX), Qwen3.8-27B-Cold-Fusion-GAIN-V1.1 (oQ4e fp16 MTP).
- Dataset 34572 -> 34626, community 33500 -> 33554. check_quotes green (35279 verified).

## 2026-10-17: oMLX batch 590 (+73 rows)

- scan574 sweep (60 new traces), mined 73 records, no new models or hardware.
- Dataset 34499 -> 34572, community 33427 -> 33500. check_quotes green (35225 verified).

## 2026-10-17: oMLX batch 589 (+69 rows)

- scan573 sweep (60 new traces), mined 69 records, +1 new model Qwen3.8-35B-A3B-DistillAPEX-MiniPlus-Abliterated (4bit); MAP for Huihui-Qwen3.8-27B-abliterated oQ3.5e MTP.
- Dataset 34430 -> 34499, community 33358 -> 33427. check_quotes green (35152 verified).

## 2026-10-17: oMLX batch 588 (+63 rows)

- scan572 sweep (60 new traces), mined 63 records, no new models; MAPs for Ornith-1.5-35B-A3B MXFP4 MLX and Qwen3.5-0.8B oQ8 MTP.
- Dataset 34367 -> 34430, community 33295 -> 33358. check_quotes green (35083 verified).

## 2026-10-17: oMLX batch 587 (+67 rows)

- scan571 sweep (60 new traces), mined 67 records, +2 new models K2-Horizon-7B-uno (6bit) and TheCluster--amoral-gemma-3-12B-v2 (4bit MLX); MAPs for muse-glimmer 30B nvfp4 and Swift 1.5 4bit MLX (mapped to space form, 61 -> 63 records).
- Dataset 34300 -> 34367, community 33228 -> 33295. check_quotes green (35020 verified).

## 2026-10-17: oMLX batch 586 (+64 rows)

- scan570 sweep (60 new traces), mined 64 records, +1 new model gemma-4-E2B-it-Uncensored-MAX (4bit); MAPs for GLM-5.3-Flash 4bit, Spark-X2.5-4B (quant unstated), and the new E2B variant.
- Dataset 34236 -> 34300, community 33164 -> 33228. check_quotes green (34953 verified).

## 2026-10-17: llama.cpp PR #30701 (+10 rows)

- Mined SYCL fast q8_0 reorder dequant A/B (Intel Arc Pro B70, prompt eval t/s only, ctx 512): Qwen3.8-27B Q8_0 (516.36 -> 906.28), UD-Q8_K_XL (547.57 -> 938.73), UD-Q8_K_4XL dual GPU (630.00 -> 975.48), Mistral-Small-3.2-24B-Instruct Q8_0 (635.88 -> 1164.05), Qwen3 4B Q8_0 (2985.50 -> 4831.58); stock and optimized arms as separate records.
- +1 new model Mistral-Small-3.2-24B-Instruct; Qwen3 4B mapped to space form (61 records).
- Dataset 34226 -> 34236, 661 -> 662 models, sourced 1062 -> 1072. check_quotes green (34889 verified).

## 2026-10-17: oMLX batch 585 (+62 rows)

- scan569 sweep (57 new traces), mined 62 records, no new models or hardware; MAPs for Qwen3.6-35B-A3B-MTPLX-Optimized-Balance FP16, Qwen3.6-35B-A3B oQ8 fp16 MTP, Qwen3.8-27B oQ8 mlx fp16 MTP, and gemma-4-31B-it mxfp4.
- Dataset 34164 -> 34226, community 33102 -> 33164. check_quotes green (34879 verified).

## 2026-10-16: oMLX batch 584 (+48 rows)

- scan568 sweep (45 new traces), mined 48 records, no new models or hardware.
- Dataset 34116 -> 34164, community 33054 -> 33102. check_quotes green (34817 verified).

## 2026-10-16: oMLX batch 583 (+49 rows)

- scan567 sweep (48 new traces), mined 49 records, no new models or hardware; MAP for LFM2.5-24B-A2B 8bit.
- Dataset 34067 -> 34116, community 33005 -> 33054. check_quotes green (34769 verified).

## 2026-10-16: oMLX batch 582 (+59 rows)

- scan566 sweep (53 new traces), mined 58 records, no new models or hardware; MAPs for LFM2.5-2.6B oQ3.5e / oQ5e MLX and MiniCPM-V-4.7-35B-A3B mxfp4.
- Fixed duplicate trace id: second 87mc1tub row re-attributed to w2nbqalu (+1 distinct record).
- Dataset 34009 -> 34067, community 32947 -> 33005. check_quotes green (34720 verified).

## 2026-10-16: oMLX batch 581 (+68 rows)

- scan565 sweep (60 new traces), mined 68 records, no new models or hardware; MAP for LFM2.5-2.6B oQ4e MLX bf16 matrix-oQ4e.
- Dataset 33941 -> 34009, community 32879 -> 32947. check_quotes green (34662 verified).

## 2026-10-16: oMLX batch 580 (+62 rows)

- scan564 sweep (55 new traces), mined 62 records, no new models or hardware; MAPs for Qwen3.8-27B-Abliterated 4bit MTPLX and lowercase Flash-Next oQ4e MTP.
- Dataset 33879 -> 33941, community 32817 -> 32879. check_quotes green (34594 verified).

## 2026-10-16: oMLX batch 579 (+73 rows)

- scan563 sweep (60 new traces), mined 73 records, +2 new models DeepSeek-R1-Distill-Qwen-1.5B-chat (oQ4 mlx) and NuExtract3 (8bits mlx); MAPs for CyberTiel-Coder-35B MLX and Qwen3.5-9B 4bit mlx-community.
- Dataset 33806 -> 33879, 659 -> 661 models, community 32744 -> 32817. check_quotes green (34532 verified).

## 2026-10-16: oMLX batch 578 (+68 rows)

- scan562 sweep (60 new traces), mined 68 records, no new models or hardware; MAP for gemma-4-12b-it (quant unstated).
- Dataset 33738 -> 33806, community 32676 -> 32744. check_quotes green (34459 verified).

## 2026-10-16: oMLX batch 577 (+68 rows)

- scan561 sweep (60 new traces), mined 68 records, no new models or hardware; MAPs for gemma-4-12b-it oQ5e and MiniCPM-V-4.7-35B-A3B mxfp4 mlx-community.
- Dataset 33670 -> 33738, community 32608 -> 32676. check_quotes green (34391 verified).

## 2026-10-16: oMLX batch 576 (+67 rows)

- scan560 sweep (60 new traces), mined 67 records, +1 new model Qwen3-30B-A3B-Instruct-2507 (4bit); MAPs for LFM2.5-2.6B oQ4e MLX / fp16 / OptiQ 4bit, Qwen3-4B-Instruct-2507 4bit DWQ, and Qwen3.6-35B-A3B oQ3.
- Dataset 33603 -> 33670, 658 -> 659 models, community 32541 -> 32608. check_quotes green (34323 verified).

## 2026-10-16: oMLX batch 575 (+65 rows)

- scan559 sweep (60 new traces), mined 65 records, +1 new model Signal-3.8-27B-Terse-Coder (oQ4e MTP); MAP for Jundot:Qwen3.8-Flash-Next oQ4e MTP.
- Dataset 33538 -> 33603, 657 -> 658 models, community 32476 -> 32541. check_quotes green (34256 verified).

## 2026-10-16: oMLX batch 574 (+63 rows)

- scan558 sweep (58 new traces), mined 63 records, +1 new model Jundot:Qwen3.8-Flash-Next (oQ4e fp16 MTP).
- Dataset 33475 -> 33538, 656 -> 657 models, community 32413 -> 32476. check_quotes green (34191 verified).

## 2026-10-16: oMLX batch 573 (+64 rows)

- scan557 sweep (56 new traces), mined 64 records, +1 new model Qwen3.6-40B-Fable-Fusion-6-Core-Deckard-Eleanor-Heretic-Uncensored (oQ4e MTP); MAPs for Ornith-1.0-35B oQ4e, Qwen3.8-Flash-Next oQ5e WLSRefit MTP, and Qwen3-VL-8B-Instruct 4bit mlx-community.
- Dataset 33411 -> 33475, 655 -> 656 models, community 32349 -> 32413. check_quotes green (34128 verified).

## 2026-10-16: oMLX batch 572 (+64 rows)

- scan556 sweep (56 new traces), mined 64 records, +2 new models Ministral-3-3B-Instruct-2512 (8bit) and Ministral-8B-Instruct-2410 (8bit); MAPs for Agents-A1 OptiQ 4bit, Qwen2.5-Coder-3B-Instruct 4bit, and granite-4.2-3b q4.
- Dataset 33347 -> 33411, 653 -> 655 models, community 32285 -> 32349. check_quotes green (34064 verified).

## 2026-10-16: oMLX batch 571 (+57 rows)

- scan555 sweep (49 new traces), mined 57 records, +2 new models AX-Qwen3.8-27B (6bit AXQ MTP MLX) and Qwen3-48B-A4B-Savant-Commander-Distill-12X-Closed-Open-Heretic-Uncensored (oQ4e).
- Dataset 33290 -> 33347, 651 -> 653 models, community 32228 -> 32285. check_quotes green (34000 verified).

## 2026-10-16: oMLX batch 570 (+69 rows)

- scan554 sweep (60 new traces), mined 69 records, no new models or hardware; MAP for Qwen3.6-35B-A3B-Claude-4.7-Opus-Reasoning-Distilled oQ3.5e.
- Dataset 33221 -> 33290, community 32159 -> 32228. check_quotes green (33943 verified).

## 2026-10-16: oMLX batch 569 (+68 rows)

- scan553 sweep (60 new traces), mined 68 records, no new models or hardware; MAPs for Ornith-1.5-35B-A3B OptiQ static 5.5bpw 4bit and Qwen3.8-Flash-Next oQ4e MTP requant.
- Dataset 33153 -> 33221, community 32091 -> 32159. check_quotes green (33874 verified).

## 2026-10-16: oMLX batch 568 (+61 rows)

- scan552 sweep (56 new traces), mined 61 records, no new models or hardware; MAP for gemma-4-26B-A4B-it oQ4e.
- Dataset 33092 -> 33153, community 32030 -> 32091. check_quotes green (33806 verified).

## 2026-10-16: oMLX batch 567 (+69 rows)

- scan551 sweep (60 new traces), mined 69 records, no new models or hardware; MAP for Qwen3-Coder-Next 8bit MLX.
- Dataset 33023 -> 33092, community 31961 -> 32030. check_quotes green (33745 verified).

## 2026-10-16: oMLX batch 566 (+67 rows)

- scan550 sweep (56 new traces), mined 67 records, no new models or hardware; MAPs for muse-glimmer 30B oQ4e fp16 and Swift-Qwen3.8-27B 6bit MLX.
- Dataset 32956 -> 33023, community 31894 -> 31961. check_quotes green (33676 verified).

## 2026-10-16: oMLX batch 565 (+66 rows)

- scan549 sweep (60 new traces), mined 66 records, +1 new model Muse-Glimmer-30B-heretic (oQ4e); MAPs for Ling-3.0-tiny oQ8 fp16, Qwen3.6-35B-A3B oQ8e bf16 pt MTP, Qwen3.8-Flash-Next oQ2.7e MTP, and Qwopus3.8-27B-Flash-V2 oQ6e MTP.
- Dataset 32890 -> 32956, 650 -> 651 models, community 31828 -> 31894. check_quotes green (33609 verified).

## 2026-10-16: oMLX batch 564 (+60 rows)

- scan548 sweep (57 new traces), mined 60 records, no new models or hardware; MAP for gemma-4-26B-A4B-it oQ2.5e MTP.
- Dataset 32830 -> 32890, community 31768 -> 31828. check_quotes green (33543 verified).

## 2026-10-16: oMLX batch 563 (+66 rows)

- scan547 sweep (60 new traces), mined 66 records, no new models or hardware; MAP for RavenX-CyberAgent RATH 8bit mlx.
- Dataset 32764 -> 32830, community 31702 -> 31768. check_quotes green (33483 verified).

## 2026-10-16: oMLX batch 562 (+64 rows)

- scan546 sweep (60 new traces), mined 64 records, +1 new model MiniCPM-V-4.7-1B (4bit); MAP for Qwen3.6-35B-A3B-Uncensored-Genesis-Final-dequantized oQ4e fp16 MTP.
- Dataset 32700 -> 32764, 649 -> 650 models, community 31638 -> 31702. check_quotes green (33417 verified).

## 2026-10-16: oMLX batch 561 (+69 rows)

- scan545 sweep (60 new traces), mined 69 records, no new models or hardware; MAPs for LFM2.5-24B-A2B oQ5e fp16 and Qwen3-VL-8B-Instruct 4bit.
- Dataset 32631 -> 32700, community 31569 -> 31638. check_quotes green (33353 verified).

## 2026-10-16: oMLX batch 560 (+66 rows)

- scan544 sweep (58 new traces), mined 66 records, no new models or hardware; MAPs for Qwopus3.8-27B-Flash oQ4e MTP and gemma-4-E4B-it oQ6 MTP.
- Dataset 32565 -> 32631, community 31503 -> 31569. check_quotes green (33284 verified).

## 2026-10-16: oMLX batch 559 (+66 rows)

- scan543 sweep (60 new traces), mined 66 records, no new models or hardware.
- Dataset 32499 -> 32565, community 31437 -> 31503. check_quotes green (33218 verified).

## 2026-10-16: oMLX batch 558 (+71 rows)

- scan542 sweep (60 new traces), mined 71 records, no new models or hardware; MAPs for Kolibri-1 mixed 4-8 bit mlx and Occamy-1.0 oQ4e fp16.
- Dataset 32428 -> 32499, community 31366 -> 31437. check_quotes green (33152 verified).

## 2026-10-16: oMLX batch 557 (+69 rows)

- scan541 sweep (60 new traces), mined 69 records, no new models or hardware; MAP for Qwen3.6-35B-A3B oQ3.5 FP16.
- Dataset 32359 -> 32428, community 31297 -> 31366. check_quotes green (33081 verified).

## 2026-10-16: oMLX batch 556 (+66 rows)

- scan540 sweep (60 new traces), mined 66 records, no new models or hardware; MAPs for MiniCPM-V-4.7-35B-A3B 5bit, Qwen3.6-35B-A3B oQ3e MTP MLX, and NVIDIA-Nemotron-3.5-Lightning-30B-A3B 4bit MLX.
- Dataset 32293 -> 32359, community 31231 -> 31297. check_quotes green (33012 verified).

## 2026-10-16: oMLX batch 555 (+69 rows)

- scan539 sweep (60 new traces), mined 69 records, +1 new model LOCAL-SMART (4bit); MAP for gemma-4-12b-it oQ4e MTP.
- Dataset 32224 -> 32293, 648 -> 649 models, community 31162 -> 31231. check_quotes green (32946 verified).

## 2026-10-16: oMLX batch 554 (+68 rows)

- scan538 sweep (60 new traces), mined 68 records, no new models or hardware; MAP for gemma-4-12b-it oQ8e MTP.
- Dataset 32156 -> 32224, community 31094 -> 31162. check_quotes green (32877 verified).

## 2026-10-16: oMLX batch 553 (+69 rows)

- scan537 sweep (60 new traces), mined 69 records, +1 new model Qwen3.8-27B-MindMeld-AREX (mxfp4 mlx).
- Dataset 32087 -> 32156, 647 -> 648 models, community 31025 -> 31094. check_quotes green (32809 verified).

## 2026-10-16: oMLX batch 552 (+65 rows)

- scan536 sweep (60 new traces), mined 65 records, no new models or hardware; MAP for Qwen3.8-Flash-Next oQ4e fp16.
- Dataset 32022 -> 32087, community 30960 -> 31025. check_quotes green (32740 verified).

## 2026-10-16: oMLX batch 551 (+65 rows)

- scan535 sweep (60 new traces), mined 65 records, no new models or hardware; MAPs for LFM2.5-24B-A2B 4bit MLX, Qwen3-Coder-Next-REAP-48B-A3B 4bit mlx, gemma-4-12b-it oQ6e MTP, and Gemma 4 26B-A4B 4bit (space form after slug collision, 177 existing).
- Dataset 31957 -> 32022, community 30895 -> 30960. check_quotes green (32675 verified).

## 2026-10-16: oMLX batch 550 (+66 rows)

- scan534 sweep (60 new traces), mined 66 records, +1 new model Kimi-VL-A3B-Instruct (4bit mlx); MAPs for LFM2.5-1.2B 8bit MLX and gemma-4-26B-A4B-it QAT q4_0 4bit MLX aligned.
- Dataset 31891 -> 31957, 646 -> 647 models, community 30829 -> 30895. check_quotes green (32610 verified).

## 2026-10-16: oMLX batch 549 (+63 rows)

- scan533 sweep (60 new traces), mined 63 records, +3 new models Mellum2-12B-A2.5B-Thinking (4bit), Qwen3.8-27B-TURBO-Fable5.5-Cold-Fusion-L-Uncensored (oQ4e fp16 MTP), and qwen4flashNext (4bit); MAPs for AREX-Turbo, KAT-Coder-V2.5-Dev 4bit MLX, and Qwen3.6-35B-A3B-Claude-4.7-Opus-Reasoning-Distilled oQ5 fp16 MTP.
- Dataset 31828 -> 31891, 643 -> 646 models, community 30766 -> 30829. check_quotes green (32544 verified).

## 2026-10-16: oMLX batch 548 (+67 rows)

- scan532 sweep (60 new traces), mined 67 records, no new models or hardware; MAPs for LFM2.5-2.6B 6bit MLX and Qwen3.5-9B 5bit MLX MTP.
- Dataset 31761 -> 31828, community 30699 -> 30766. check_quotes green (32481 verified).

## 2026-10-16: oMLX batch 547 (+65 rows)

- scan531 sweep (60 new traces), mined 65 records, +1 new model gemma-4-26B-A4B-it-Claude-Opus-Distilled-v2 (8bit mxfp8 MLX); MAPs for Mellum2.1-12B-A2.5B-Thinking oQ5e, Qwen3.8-35B-A3B-Distill-Heretic oQ8 fp16 MTP, and gemma-4-12b-it 8bit mlx-community.
- Dataset 31696 -> 31761, 642 -> 643 models, community 30634 -> 30699. check_quotes green (32414 verified).

## 2026-10-16: oMLX batch 546 (+62 rows)

- scan530 sweep (60 new traces), mined 62 records, no new models or hardware; MAPs for AREX-2 4bit, Qwen3.8-27B-Uncensored oQ5e bf16 MTP MLX, Qwen3.8-35B-A3B-Distill oQ6e fp16 MTP, Qwen3.8-Flash-Next-Uncensored REAP288 MTP 4bit MLX, and gpt-oss 20B oQ5e bf16 (space form after slug collision, 285 existing).
- Dataset 31634 -> 31696, community 30572 -> 30634. check_quotes green (32349 verified).

## 2026-10-16: oMLX batch 545 (+62 rows)

- scan529 sweep (60 new traces), mined 62 records, no new models or hardware.
- Dataset 31572 -> 31634, community 30510 -> 30572. check_quotes green (32287 verified).

## 2026-10-16: oMLX batch 544 (+63 rows)

- scan528 sweep (60 new traces), mined 63 records, +1 new model deepseek-coder-6.7b-instruct-hf (4bit mlx); MAPs for DeepSeek-Coder-V2-Lite-Instruct 4bit and Ling-3.0-tiny oQ8e fp16.
- Dataset 31509 -> 31572, 641 -> 642 models, community 30447 -> 30510. check_quotes green (32225 verified).

## 2026-10-16: oMLX batch 543 (+64 rows)

- scan527 sweep (60 new traces), mined 64 records, no new models or hardware; MAPs for Qwen3.8-27B Official MLX 4bit and oQ5e, Qwen3.8-27B-Uncensored 6bit MLX, and Qwen3.8-27B-Coder390 6bit.
- Dataset 31445 -> 31509, community 30383 -> 30447. check_quotes green (32162 verified).

## 2026-10-16: oMLX batch 542 (+67 rows)

- scan526 sweep (60 new traces), mined 67 records, +2 new models granite-4.1-3b (mxfp4) and Huihui-Qwen3.5-4B-Claude-4.6-Opus-abliterated (4bit mlx-community); MAPs for LFM2.5-24B-A2B oQ4e MLX and Qwen3.5-9B-Uncensored-HauhauCS-Aggressive mxfp8 MLX.
- Dataset 31378 -> 31445, 639 -> 641 models, community 30316 -> 30383. check_quotes green (32098 verified).

## 2026-10-16: oMLX batch 541 (+69 rows)

- scan525 sweep (60 new traces), mined 69 records, +1 new model gemma-4-E4B-Agentic-Sol-Fable-Reasoning-GeminiCLI (4bit mlx); MAPs for LFM2.5-24B-A2B 4bit MLX DWQ v2, Qwen3.8-Flash-Next-Uncensored 4bit plefp8, and gemma-4-26B-A4B-it bf16.
- Dataset 31309 -> 31378, 638 -> 639 models, community 30247 -> 30316. check_quotes green (32031 verified).

## 2026-10-16: oMLX batch 540 (+70 rows)

- scan524 sweep (60 new traces), mined 70 records, +1 new model gemma-4-26B-A4B-it-qat-uncensored-heretic (4bit MLX VLM); MAP for gemma-4-E4B-it 8bit.
- Dataset 31239 -> 31309, 637 -> 638 models, community 30177 -> 30247. check_quotes green (31962 verified).

## 2026-10-16: oMLX batch 539 (+68 rows)

- scan523 sweep (60 new traces), mined 68 records, +1 new model Gemma-4-E4B-Claude-Opus-Reasoning (4bit MLX); MAPs for Ornith-1.5-35B-A3B, gemma-4-31B-it-uncensored 4bit MLX, Gemma 4 E2B 8bit (after slug collision on the space form, 88 existing), and gemma-4-E2B-it OptiQ-4bit QAT.
- Dataset 31171 -> 31239, 636 -> 637 models, community 30109 -> 30177. check_quotes green (31892 verified).

## 2026-10-16: oMLX batch 538 (+67 rows)

- scan522 sweep (60 new traces), mined 67 records, +1 new model gpt-oss-120b-MXFP4-Q8 (4bit mlx-community).
- Dataset 31104 -> 31171, 635 -> 636 models, community 30042 -> 30109. check_quotes green (31824 verified).

## 2026-10-16: oMLX batch 537 (+71 rows)

- scan521 sweep (60 new traces), mined 71 records, no new models or hardware; MAP for Qwen3.8-27B-Uncensored 4bit MLX.
- Dataset 31033 -> 31104, community 29971 -> 30042. check_quotes green (31757 verified).

## 2026-10-16: oMLX batch 536 (+69 rows)

- scan520 sweep (60 new traces), mined 69 records, no new models or hardware.
- Dataset 30964 -> 31033, community 29902 -> 29971. check_quotes green (31686 verified).

## 2026-10-16: oMLX batch 535 (+67 rows)

- scan519 sweep (60 new traces), mined 67 records, +1 new model gemma-3-1b-it (4bit mlx-community).
- Dataset 30897 -> 30964, 634 -> 635 models, community 29835 -> 29902. check_quotes green (31617 verified).

## 2026-10-16: oMLX batch 534 (+68 rows)

- scan518 sweep (58 new traces), mined 68 records, +1 new model MiniCPM5-2B-chat (4bit mlx); MAPs for Huihui-Qwen3.6-35B-A3B-abliterated 4bit mlx, LFM2.5-24B-A2B 4bit MLX fp16, Qwen2.5-VL-3B-Instruct 4bit, and Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive OptiQ-5bpw MLX.
- Dataset 30829 -> 30897, 633 -> 634 models, community 29767 -> 29835. check_quotes green (31550 verified).

## 2026-10-16: oMLX batch 533 (+61 rows)

- scan517 sweep (56 new traces, 4 dead 404), mined 61 records, no new models or hardware; MAPs for LFM2.5-24B-A2B oQ5e, oQ6e and oQ8e.
- Dataset 30768 -> 30829, community 29706 -> 29767. check_quotes green (31482 verified).

## 2026-10-16: vLLM PR #61942 (+2 rows)

- GLM-5.1-FP8 (new model) MI355X TP4, 1K in c32 total throughput, main vs AITER top-k sparse indexer skip arm (16616 -> 17042 tok/s, +2.6% within noise).
- Dataset 30766 -> 30768, 632 -> 633 models, sourced 1060 -> 1062. check_quotes green (31421 verified).

## 2026-10-15: oMLX batch 532 (+68 rows)

- scan516 sweep (56 new traces), mined 68 records, no new models or hardware; MAPs for LFM2.5-2.6B oQ4e and Qwen3.8-Flash-Next-Uncensored oQ4e 100K MTP plefp8.
- Dataset 30698 -> 30766, community 29638 -> 29706. check_quotes green (31419 verified).

## 2026-10-15: oMLX batch 531 (+67 rows)

- scan515 sweep (60 new traces), mined 67 records, +2 new models Josiefied-Qwen3-4B-abliterated-v1 (4bit) and Qwen3.6-35B-A3B-MTPLX-Optimized-Balance; MAPs for Qwen3.6-35B-A3B-Uncensored-Heretic, gemma-4-12b-it 8bit MLX, and gemma-4-26B-A4B-it OptiQ.
- Dataset 30631 -> 30698, 630 -> 632 models, community 29571 -> 29638. check_quotes green (31351 verified).

## 2026-10-15: oMLX batch 530 (+64 rows)

- scan514 sweep (60 new traces), mined 64 records, +1 new model Bonsai-4B (1bit mlx); MAPs for Cyber-Tiel-Coder-35B-A3B oQ6e, MiniCPM-V-4.6, Ornith-1.5-35B-A3B-uncensored 4bit MLX, gemma-4-26B-A4B-it OptiQ 4bit, and Occamy-1.0 oQ4e MTP (uppercase form).
- Dataset 30567 -> 30631, 629 -> 630 models, community 29507 -> 29571. check_quotes green (31284 verified).

## 2026-10-15: oMLX batch 529 (+68 rows)

- scan513 sweep (58 new traces), mined 68 records, no new models or hardware; MAPs for GLM-5.3-Flash oQ8 MTP, LFM2.5-24B-A2B 6bit MLX, Qwen3.8-Flash-Next g32 MTP 4bit, and gemma-4-26B-A4B-it (quant unstated).
- Dataset 30499 -> 30567, community 29439 -> 29507. check_quotes green (31220 verified).

## 2026-10-15: oMLX batch 528 (+76 rows)

- scan512 sweep (60 new traces), mined 76 records, +1 new model StartLux-Decision-4B.
- Dataset 30423 -> 30499, 628 -> 629 models, community 29363 -> 29439. check_quotes green (31152 verified).

## 2026-10-15: oMLX batch 527 (+70 rows)

- scan511 sweep (60 new traces), mined 70 records, no new models or hardware; MAPs for MiniCPM5-2B bf16 and gemma-4-12b-it 4bit (lowercase form after slug collision).
- Dataset 30353 -> 30423, community 29293 -> 29363. check_quotes green (31076 verified).

## 2026-10-15: oMLX batch 526 (+62 rows)

- scan510 sweep (58 new traces), mined 62 records, no new models or hardware; MAPs for Huihui-Qwen3.6-35B-A3B-Claude-4.7-Opus-abliterated 6bit MLX, MiMo-V2.6-Flash-RL oQ8e MTP, and Qwen3 32B 4bit (space form).
- Dataset 30291 -> 30353, community 29231 -> 29293. check_quotes green (31006 verified).

## 2026-10-15: oMLX batch 525 (+62 rows)

- scan509 sweep (58 new traces), mined 62 records, +2 new models Mamba-Codestral-7B-v0.1 (8bit) and Qwen3.8-Flash-Next-REAM-288 (oQ4e MTP); MAPs for GLM-5.3-Flash oQ8e, Jundot Qwen3.8-Flash-Next oQ8e MTP, LFM2.5-24B-A2B oQ4e fp16, MiniCPM5-1B OptiQ 4bit.
- Dataset 30229 -> 30291, 626 -> 628 models, community 29169 -> 29231. check_quotes green (30944 verified).

## 2026-10-15: oMLX batch 524 (+62 rows)

- scan508 sweep (56 new traces), mined 62 records, +1 new model Qwen2-57B-A14B-Instruct (4bit mlx-community); MAP for Qwen2.5-Coder-7B-Instruct oQ4e fp16.
- Dataset 30167 -> 30229, 625 -> 626 models, community 29107 -> 29169. check_quotes green (30882 verified).

## 2026-10-15: oMLX batch 523 (+67 rows)

- scan507 sweep (60 new traces), mined 67 records, no new models or hardware; MAP for Qwen3 30B A3B 4bit MLX (space form after slug collision).
- Dataset 30100 -> 30167, community 29040 -> 29107. check_quotes green (30820 verified).

## 2026-10-15: oMLX batch 522 (+67 rows)

- scan506 sweep (60 new traces), mined 67 records, no new models or hardware.
- Dataset 30033 -> 30100, community 28973 -> 29040. check_quotes green (30753 verified).

## 2026-10-15: oMLX batch 521 (+66 rows)

- scan505 sweep (60 new traces), mined 66 records, +2 new models Jev-Style-0.8B-Decision-v3 (oQ8e MLX) and Qwopus3.6-35B-A3B-Coder (6bit, oQ6 MTP); MAPs for Qwen3.8-27B-Uncensored-OrcaRouter 5bit MLX, granite-4.2-8b 4bit MLX, Qwen3.6-35B-A3B spacecomx oQ6e fp16 MTP, and unsloth Qwen3.6-27B 8bit MLX.
- Dataset 29967 -> 30033, 623 -> 625 models, community 28907 -> 28973. check_quotes green (30686 verified).

## 2026-10-15: oMLX batch 520 (+63 rows)

- scan504 sweep (60 new traces), mined 63 records, no new models or hardware; MAPs for LFM2.5-24B-A2B oQ4e and Qwen2.5-7B-Instruct AWQ.
- Dataset 29904 -> 29967, community 28844 -> 28907. check_quotes green (30620 verified).

## 2026-10-15: oMLX batch 519 (+62 rows)

- scan503 sweep (60 new traces), mined 62 records, no new models or hardware.
- Dataset 29842 -> 29904, community 28782 -> 28844. check_quotes green (30557 verified).

## 2026-10-15: vLLM PR #61903 (+4 rows)

- MiniMax M2.5 FP8 TP2 on 2xH200 (new hardware label), output tok/s at concurrency 64, main vs BF16x3 router GEMM arm, two containers, first of 2 runs recorded with both runs in notes.
- Mapped to the established space-form label MiniMax M2.5 after a slug collision warning. Dataset 29838 -> 29842, sourced 1056 -> 1060. check_quotes green (30495 verified).

## 2026-10-15: oMLX batch 518 (+66 rows)

- scan502 sweep (60 new traces), mined 66 records, no new models or hardware; MAP for Qwen3.8-Flash-Next FP8.
- Dataset 29772 -> 29838, community 28716 -> 28782. check_quotes green (30491 verified).

## 2026-10-15: oMLX batch 517 (+61 rows)

- scan501 sweep (60 new traces), mined 61 records, +1 new model Qwen3.6-35B-A3B-TurboQuant (4bit MLX); MAPs for Qwen2.5-Coder-1.5B oQ8e fp16 and Qwen3.8-Flash-Next 4bit GGUF exact f32 build.
- Dataset 29711 -> 29772, 622 -> 623 models, community 28655 -> 28716. check_quotes green (30425 verified).

## 2026-10-15: oMLX batch 516 (+64 rows)

- scan500 sweep (58 new traces), mined 64 records, +1 new model medgemma-4b-it (4bit MLX); MAPs for Huihui-Qwen3.8-27B-abliterated 8bit mlx, Muse-Glimmer-30B-Abliterated MM oQ4e and oQ6e, Qwen3.6-35B-A3B 4bit MLX and oQ8e MTP fp16, and Qwen3.8-27B 4bit fresh rebuild.
- Dataset 29647 -> 29711, 621 -> 622 models, community 28591 -> 28655. check_quotes green (30364 verified).

## 2026-10-15: oMLX batch 515 (+66 rows)

- scan499 sweep (60 new traces), mined 66 records, +1 new model MiniCPM-V-4.7-35B-A3B (oQ4e).
- nerkyor Coder390 NInfer HF card rewritten again (prose reworded, numbers unchanged): 5 hf-ninfer-coder390 quotes repointed to the new wording.
- Dataset 29581 -> 29647, 620 -> 621 models, community 28525 -> 28591. check_quotes green (30300 verified).

## 2026-10-15: oMLX batch 514 (+61 rows)

- scan498 sweep (58 new traces), mined 61 records, +2 new models Spark-X2.5-1.7B and Huihui-gemma-4-26B-A4B-it (8bit XL mlx, page wording kept distinct from the abliterated label); MAP for LFM2.5-2.6B.
- Dataset 29520 -> 29581, 618 -> 620 models, community 28464 -> 28525. check_quotes green (30234 verified).

## 2026-10-15: oMLX batch 513 (+64 rows)

- scan497 sweep (60 new traces), mined 64 records, no new models or hardware; MAPs for Ornith-1.5-9B oQ4e, Qwen3.5-4B oQ4e MTP and Qwen3.8-27B oQ4e DWQ MTP MLX.
- Dataset 29456 -> 29520, community 28400 -> 28464. check_quotes green (30173 verified).

## 2026-10-15: vLLM PR #61875 (+12 rows)

- DeepSeek-V4-Flash MXFP4 on 4x H200 with the Humming MoE backend, TP4+EP and TP4 arms, BF16 vs block FP8 GS128 MoE activations; decode, prefill and low-concurrency workloads at max-model-len 16384.
- New hardware label 4x H200 (page wording). Dataset 29444 -> 29456, sourced 1044 -> 1056. check_quotes green (30109 verified).

## 2026-10-15: oMLX batch 512 (+58 rows)

- scan496 sweep (53 new traces), mined 58 records, +2 new models Hy-MT2-30B-A3B (oQ2 MLX) and Index-Translate-2B (4bit MLX); MAP for MiMo-V2.6-Flash-RL mxfp4 MLX REAP50 MTP.
- Dataset 29386 -> 29444, 616 -> 618 models, community 28342 -> 28400. check_quotes green (30097 verified).

## 2026-10-15: oMLX batch 511 (+67 rows)

- scan495 sweep (60 new traces), mined 67 records, no new models or hardware; MAPs for LFM2.5-24B-A2B 5bit MLX and Ornith-1.5-9B oQ4e fp16 MTP.
- Dataset 29319 -> 29386, community 28275 -> 28342. check_quotes green (30039 verified).

## 2026-10-15: vLLM PR #61868 (+24 rows)

- DeepSeek-V4.1-Flash low-latency decode paths on GB300 TP4 with DSpark speculative decoding; AgentX agentic-coding traces at concurrency 1 to 64, both arms (upstream main vs switch on).
- 12 records of total tok/s per GPU and 12 records of P90 interactivity tok/s per user, labeled in notes. Dataset 29295 -> 29319, sourced 1020 -> 1044. check_quotes green (29972 verified).

## 2026-10-15: oMLX batch 510 (+67 rows)

- scan494 sweep (60 new traces), mined 67 records, +3 new models Qwen2.5-Coder-0.5B-Instruct (oQ8e fp16), Qwen3-Coder-Next-REAP-40B-A3B (oQ4e) and Kolibri-1 (3bit MLX); MAPs for MiMo-V2.6-Distill-Qwen-9B oQ8e fp16, Ornith-1.5-35B-A3B-uncensored MXFP4 MLX and Ornith-1.5-9B oQ8e fp16 MTP.
- Dataset 29228 -> 29295, 613 -> 616 models, community 28208 -> 28275. check_quotes green (29948 verified).

## 2026-10-15: oMLX batch 509 (+64 rows)

- scan493 sweep (60 new traces), mined 64 records, no new models or hardware; MAP for Qwen3.5-9B oQ6e fp16 MTP.
- Dataset 29164 -> 29228, community 28144 -> 28208. check_quotes green (29881 verified).

## 2026-10-15: oMLX batch 508 (+61 rows)

- scan492 sweep (60 new traces), mined 61 records, +1 new model Qwen3.6-35B-A3B-Brainwaves-Nex-Uncensored (qx64-hi mlx); MAPs for GLM-5.3-Flash, LFM2.5-24B-A2B oQ8e fp16, Qwen3.5-9B oQ4e fp16 MTP and Qwen3.8-27B-MTPLX 8bit.
- Dataset 29103 -> 29164, 612 -> 613 models, community 28083 -> 28144. check_quotes green (29817 verified).

## 2026-10-15: oMLX batch 507 (+62 rows)

- scan491 sweep (60 new traces), mined 62 records, +1 new model Muse-Glimmer-30B-Abliterated (mxfp4 MLX); MAPs for MiMo-V2.6-Distill-Qwen-9B oQ4e fp16, NeoHorse-1-9B 4bit MLX, Qwen3.5-9B 8bit and mlx-lm mxfp4, Qwen3.8-9B MXFP4 MLX and mlx-community Qwen3 14B 4bit (established space-form label after a slug collision warning).
- Dataset 29041 -> 29103, 611 -> 612 models, community 28021 -> 28083. check_quotes green (29756 verified).

## 2026-10-15: oMLX batch 506 (+69 rows)

- scan490 sweep (60 new traces), mined 69 records, no new models or hardware; MAPs for LFM2.5-24B-A2B 8bit MLX and Preview 4bit FP16 variants and MiniCPM5-1B oQ4.
- Dataset 28972 -> 29041, community 27952 -> 28021. check_quotes green (29694 verified).

## 2026-10-15: oMLX batch 505 (+64 rows)

- scan489 sweep (60 new traces), mined 64 records, +1 new model Qwen3.8-27B-TTURBO-Cold-Fusion-709-L-Uncensored (oQ6e mlx 1M context; page spells TTURBO, kept distinct from the TWIN-TURBO label).
- Dataset 28908 -> 28972, 610 -> 611 models, community 27888 -> 27952. check_quotes green (29625 verified).

## 2026-10-15: oMLX batch 504 (+60 rows)

- scan488 sweep (60 new traces), mined 60 records, +1 new model LFM2-8B-A1B (8bit MLX); MAPs for LFM2.5-24B-A2B 4bit MLX FP16 and Mellum2.1-12B-A2.5B-Thinking oQ4e fp16.
- Dataset 28848 -> 28908, 609 -> 610 models, community 27828 -> 27888. check_quotes green (29561 verified).

## 2026-10-15: oMLX batch 503 (+60 rows)

- scan487 sweep (60 new traces), mined 60 records, +2 new models LFM2.5-24B-A2B (4bit MLX) and gemma-4-26B-A4B-heretic-v2-qat-aligned (4bit mlx); MAPs for Coder390 27B oq4e and ThinkingCap-Qwen3.8-27B oQ5e MTP.
- Dataset 28788 -> 28848, 607 -> 609 models, community 27768 -> 27828. check_quotes green (29501 verified).

## 2026-10-15: oMLX batch 502 (+62 rows)

- scan486 sweep (60 new traces), mined 62 records, no new models or hardware; MAPs for Agents-A1 4B 8bit mlx, Qwen2.5-1.5B oQ8e fp16, Qwen3.5-35B-A3B-Heretic 8bit MLX and Qwen3.8-Flash-Next 8bit MLX.
- Dataset 28726 -> 28788, community 27706 -> 27768. check_quotes green (29441 verified).

## 2026-10-15: oMLX batch 501 (+63 rows)

- scan485 sweep (60 new traces), mined 63 records, no new models or hardware; all trace names mapped without additions.
- Dataset 28663 -> 28726, community 27643 -> 27706. check_quotes green (29379 verified).

## 2026-10-15: oMLX batch 500 (+63 rows)

- scan484 sweep (60 new traces), mined 63 records, +1 new model MiniCPM5-2B-Abliterated-Uncensored (4bit MLX).
- Dataset 28600 -> 28663, 606 -> 607 models, community 27580 -> 27643. check_quotes green (29316 verified).

## 2026-10-15: oMLX batch 499 (+62 rows)

- scan483 sweep (60 new traces), mined 62 records, no new models or hardware; all trace names mapped without additions.
- Dataset 28538 -> 28600, community 27518 -> 27580. check_quotes green (29253 verified).

## 2026-10-15: oMLX batch 498 (+62 rows)

- scan482 sweep (60 new traces), mined 62 records, no new models or hardware; all trace names mapped without additions.
- Dataset 28476 -> 28538, community 27456 -> 27518. check_quotes green (29191 verified).

## 2026-10-15: oMLX batch 497 (+64 rows)

- scan481 sweep (60 new traces), mined 64 records, no new models or hardware; MAPs for DeepSeek-R1-Distill-Qwen-7B 4bit, TWIN-TURBO Fable Cold Fusion 709-L oQ4 MTP MLX and mlx-community DeepSeek-V4-Flash-0731 2.4bit mixed.
- Dataset 28412 -> 28476, community 27392 -> 27456. check_quotes green (29129 verified).

## 2026-10-15: oMLX batch 496 (+67 rows)

- scan480 sweep (60 new traces), mined 67 records, no new models or hardware; MAP for Qwen3.6-35B-A3B-Uncensored-Heretic 6bit MLX.
- Dataset 28345 -> 28412, community 27325 -> 27392. check_quotes green (29065 verified).

## 2026-10-15: oMLX batch 495 (+66 rows)

- scan479 sweep (60 new traces), mined 66 records, no new models or hardware; MAPs for Qwen3.8-27B 5bit MLX and spicyneuron Qwen3.6-35B-A3B 5.4bit MLX.
- Dataset 28279 -> 28345, community 27259 -> 27325. check_quotes green (28998 verified).

## 2026-10-15: oMLX batch 494 (+65 rows)

- scan478 sweep (60 new traces), mined 65 records, no new models or hardware; all trace names mapped without additions.
- Dataset 28214 -> 28279, community 27194 -> 27259. check_quotes green (28932 verified).

## 2026-10-15: oMLX batch 493 (+62 rows)

- scan477 sweep (60 new traces, 52 genuinely new after 8 relistings), mined 62 records, +1 new model Qwen3.6-27B-MTPLX-Optimized-Speed-V2; MAPs for Genesis-Final oQ5e MTP, ThinkingCap-Qwen3.6-27B oQ4e DWQ MTP Vision MLX and qwen3.8-27b 4bit MTP.
- Dataset 28152 -> 28214, 605 -> 606 models, community 27132 -> 27194. check_quotes green (28867 verified).

## 2026-10-15: oMLX batch 492 (+64 rows)

- scan476 sweep (60 new traces), mined 64 records, +4 new models Huihui-ThinkingCap-Qwen3.6-27B-abliterated, LFM2.5-VL-1.6B, Qwen2.5-0.5B-Instruct (4bit MLX) and ThinkingCap-Qwen3.6-27B (3bit mlx); MAP for LFM2.5-8B-A1B.
- Dataset 28088 -> 28152, 601 -> 605 models, community 27068 -> 27132. check_quotes green (28805 verified).

## 2026-10-15: oMLX batch 491 (+64 rows)

- scan475 sweep (60 new traces), mined 64 records, no new models or hardware; MAP for the Youssofal FP16 MTPLX Qwen3.6-35B-A3B variant onto the established base label.
- Dataset 28024 -> 28088, community 27004 -> 27068. check_quotes green (28741 verified).

## 2026-10-15: oMLX batch 490 (+68 rows)

- scan474 sweep (60 new traces), mined 68 records, no new models or hardware; MAP for supergemma4-26b-abliterated-multimodal 8bit MLX.
- Dataset 27956 -> 28024, community 26936 -> 27004. check_quotes green (28677 verified).

## 2026-10-15: oMLX batch 489 (+70 rows)

- scan473 sweep (60 new traces), mined 70 records, +2 new models Jev-Style-Qwen3.5-2B-Decision (v1, distinct from v2) and Qwen2.5-32B-Instruct (4bit); MAPs for muse-glimmer 30B mxfp4, Qwen3.5-0.8B 5bit MLX MTP and Qwen3.6-35B-A3B UD-Q8_K_XL mlx.
- Dataset 27886 -> 27956, 599 -> 601 models, community 26866 -> 26936. check_quotes green (28609 verified).

## 2026-10-15: oMLX batch 488 (+69 rows)

- scan472 sweep (60 new traces), mined 69 records, no new models or hardware; MAPs for Qwen3.8-27B UD-Q4_K_XL-AWQ MTP mlx and mlx-community Qwen3.8-27B-Uncensored OptiQ-4bit.
- Dataset 27817 -> 27886, community 26797 -> 26866. check_quotes green (28539 verified).

## 2026-10-15: oMLX batch 487 (+65 rows)

- scan471 sweep (60 new traces), mined 65 records, +1 new model Qwen3.6-27B-Abliterated-Heretic-Uncensored (6bit MLX); MAPs for Qwen3.8-27B 3bit MLX TextOnly, deepseek-ai DeepSeek-V4-Flash 8bit and Laguna XS 2.1 3bit (mapped to the established space-form label after a slug collision warning).
- Dataset 27752 -> 27817, 598 -> 599 models, community 26732 -> 26797. check_quotes green (28470 verified).

## 2026-10-15: oMLX batch 486 (+60 rows)

- scan470 sweep (60 new traces), mined 60 records, no new models or hardware; MAPs for Jundot Qwen3.8-27B oQ6e MTP and Muse-Glimmer-30B oQ4e mapped to the established space-form label muse-glimmer 30B after a slug collision warning.
- Dataset 27692 -> 27752, community 26672 -> 26732. check_quotes green (28405 verified).

## 2026-10-15: oMLX batch 485 (+61 rows)

- scan469 sweep (60 new traces), mined 61 records, no new models or hardware; MAPs for GLM-4.7-Flash 4bit, Qwen3.5-2B 4bit MLX, Qwen3.6-35B-A3B bf16-pt oQ6e MTP and Qwen3.8-27B-Uncensored-HauhauCS-Aggressive MTPLX 4bit.
- Dataset 27631 -> 27692, community 26611 -> 26672. check_quotes green (28345 verified).

## 2026-10-15: oMLX batch 484 (+62 rows)

- scan468 sweep (60 new traces), mined 62 records, +1 new model DeepSeek-R1-Distill-Qwen-32B (8bit MLX); MAPs for MiniCPM5-2B 4bit MLX and mlx-community Qwen3-Coder-30B-A3B-Instruct 4bit.
- Dataset 27569 -> 27631, 597 -> 598 models, community 26549 -> 26611. check_quotes green (28284 verified).

## 2026-10-15: oMLX batch 483 (+62 rows)

- scan467 sweep (60 new traces, 1 dead 404), mined 62 records, +1 new model Magidonia-24B-v4.3; MAPs for K2-Horizon-7B oQ6e, NeoHorse-1-9B 8bit MLX, Ornith-1.5-9B oQ6e MTP, Qwen3.8-27B-Coder390 oQ4e MTP text and Qwen3.8-27B-Uncensored-OrcaRouter 6bit MLX. Two degenerate BF16-oQ8e-mtp traces (model never named, M3 Ultra) added to the SKIP set after a known.txt mishap was fully restored.
- Dataset 27507 -> 27569, 596 -> 597 models, community 26487 -> 26549. check_quotes green (28222 verified).

## 2026-10-15: oMLX batch 482 (+62 rows)

- scan466 sweep (60 new traces, 1 dead 404), mined 62 records, no new models or hardware; MAPs for Qwen3.8-27B oQ2e fp16 MTP and gemma-4-31B-it 6bit.
- Dataset 27445 -> 27507, community 26425 -> 26487. check_quotes green (28160 verified).

## 2026-10-15: oMLX batch 481 (+57 rows)

- scan465 sweep (60 new traces, 8 dead 404s), mined 57 records, +1 new model Qwen3.8-35B-A3B (oQ4e base, distinct from the Distill variants).
- Dataset 27388 -> 27445, 595 -> 596 models, community 26368 -> 26425. check_quotes green (28098 verified).

## 2026-10-15: oMLX batch 480 (+66 rows)

- scan464 sweep (60 new traces), mined 66 records, +3 new models Alice-27B, Ornith-1.5-9B-uncensored (oQ4e) and Qwen4Exp (page form of Qwen4-exp, added via vLLM #61728); MAPs for Qwen3-1.7B 4bit MLX, Qwen3.8-27B-Uncensored oQ5e MTP, Swift oQ4e/oQ8e mixed MTP, gemma-4-12b-it 4bit and swdjojo Qwen3.8-27B MLX oQ4e.
- Dataset 27322 -> 27388, 593 -> 595 models, community 26302 -> 26368. check_quotes green (28041 verified).

## 2026-10-15: vLLM pulse #61728 (+2 rows)

- #61728 (Qwen4Exp QSA DCP follow-ups to #59279): mined 2 records, output tok/s per user on 8x A100-SXM4-40GB TP8+EP DCP4 with FP8 KV and MTP3, MLPerf agentic multi-turn 32 in flight 60 min per arm; #59279 plus block-table fix 42.5 tok/s (SLO pass 68.8%) vs this PR 45.3 tok/s (SLO pass 76.2%), req/s 2.72 vs 2.80, TTFT and TPOT percentiles in notes; quant unstated (weights dtype not stated, KV FP8), model label Qwen4Exp in page form (hyphenated Qwen4-exp from oMLX cannot norm-match the page). Parked: #61731-61736 (no tables).
- Dataset 27320 -> 27322, sourced 1018 -> 1020. check_quotes green (27975 verified).

## 2026-10-15: oMLX batch 479 (+63 rows)

- scan463 sweep (60 new traces), mined 63 records, +1 new model gemma-4-31B-it-uncensored (oQ5e MTP); MAPs for GLM-4.7-Flash REAP-23B-A3B oQ5, Ornith-1.5-35B-A3B-uncensored 6bit fixed MTP vision MLX, Qwen3.5-9B OptiQ.
- Dataset 27257 -> 27320, community 26239 -> 26302. check_quotes green (27973 verified).

## 2026-10-15: oMLX batch 478 (+67 rows)

- scan462 sweep (60 new traces), mined 67 records, +1 new model gemma-3-4b-it-qat (QAT 4bit); MAPs for Apodex-1.1-mini oQ6e MTP, Qwen3.8-27B oQ2.5e MTP and granite-4.2-8b q8 MLX.
- Dataset 27190 -> 27257, 591 -> 592 models, community 26172 -> 26239. check_quotes green (27910 verified).

## 2026-10-15: llama.cpp pulse #30544 (+5 rows)

- #30544 (Vulkan F32 MUL_MAT_ID on GPU for mat-vec, skip MMVQ): mined 5 records, llama-bench -ngl 99 -fa 1 -p 512 -n 32 on Radeon 8060S (gfx1151, Strix Halo) with Mistral-Small-4-119B-2603 UD-Q4_K_XL across three builds; master 5cdadfc32 regressed tg32 to 3.4 after #29029, this PR restores 39.5 via llama-server; pp512 334 (pre-#29029) vs 319 (master). Page HTML truncates commit hashes to 7 chars, quotes use the truncated form.
- Dataset 27185 -> 27190, sourced 1013 -> 1018. check_quotes green (27843 verified).

## 2026-10-15: oMLX batch 477 (+65 rows)

- scan461 sweep (60 new traces), mined 65 records, +1 new model Qwen3.5-VL-2B (8bit MLX CRACK build); MAPs for Hy-MT2-1.8B 4bit MLX, Qwythos-9B-v2 OptiQ-4bit and Swift1.5 Qwen3.8-Flash-Next oQ5e MTP.
- Dataset 27120 -> 27185, 590 -> 591 models, community 26107 -> 26172. check_quotes green (27838 verified).

## 2026-10-15: oMLX batch 476 (+62 rows)

- scan460 sweep (60 new traces), mined 62 records, +2 new models Qwen2.5-VL-3B-Instruct (4bit) and Qwythos-9B-Claude-Mythos-5 (MTP build); MAPs for DeepSeek-V4.1-Flash quant-unstated and oQ2e MTP; degenerate oMLX traces titled "4bit" on M4 Pro and M5 Max added to SKIP (model identity unrecoverable from page).
- Dataset 27058 -> 27120, 588 -> 590 models, community 26045 -> 26107. check_quotes green (27773 verified).

## 2026-10-15: oMLX batch 475 (+63 rows)

- scan459 sweep (60 new traces), mined 63 records, +2 new models Qwen3.6-40B-Claude-4.6-Opus-Deckard-Heretic (qx64 hi MLX build) and Qwen3.8-27B-CRACK (DWQ-4bit MLX); MAPs for DeepSeek-V4.1-Flash oQ2.5e MTP and swdjojo Qwen3.8-27B-AEON-ULTIMATE-UNCENSORED oQ4e MTP to the existing aeon-ultimate-uncensored label.
- Dataset 26995 -> 27058, 586 -> 588 models, community 25982 -> 26045. check_quotes green (27711 verified).

## 2026-10-15: llama.cpp pulse #29353 (+44 rows)

- #29353 (cuda/hip GDN chunked kernel, merged): mined 44 records, llama-bench prompt-processing tok/s master vs PR at 2048/4096 prompt tokens across five GPUs (RTX PRO 6000 Blackwell, Spark GB10, RTX 5090, RTX 4090, RTX 3090) and five Qwen builds (Qwen3.5-35B-A3B Q8_0/Q4_K_S, Qwen3.8-27B Q8_0/Q4_K_M/UD-Q8_K_L, Qwen3.6-35B-A3B UD-Q4_K_M, Qwen3.8-Flash-Next UD-IQ4_XS with -lzm on); gains +0.9% to +20.6%, biggest on 35B-A3B MoE prefill.
- Dataset 26951 -> 26995, sourced 969 -> 1013. check_quotes green (27648 verified).

## 2026-10-14: oMLX batch 474 (+66 rows)

- scan458 sweep (60 new traces), mined 66 records, no new models or hardware; MAPs for Qwen3.8-27B 6bit MLX and Qwen3.8-Flash-Next oQ4e mix6 MTP v2.
- Dataset 26885 -> 26951, community 25916 -> 25982. check_quotes green (27604 verified).

## 2026-10-14: vLLM pulse #56273 (+6 rows)

- #56273 (packed NVFP4 Qwen4Exp PLE embeddings): mined 6 single-DGX-Spark reference records, Qwen3.8-Flash-Next NVFP4 on one GB10 with MTP four draft tokens, 32k-prefix/2k-suffix/256-out workload at concurrency 1/4/8, aggregate active decode tok/s and TTFT for the local b12x checkpoint (32.41/36.31/43.44 tok/s, packed PLE resident) vs the NVIDIA checkpoint on upstream vLLM with disk PLE offload (23.51/34.25/45.92, 47.7 GiB FP8 PLE through page cache with host swap observed); PLE payload sizes, KV cache formats and acceptance lengths in notes. Parked: #59815 (config + accuracy only), #61556 (no tables).
- Dataset 26879 -> 26885, sourced 963 -> 969. check_quotes green (27538 verified).

## 2026-10-14: oMLX batch 473 (+64 rows)

- scan457 sweep (60 new traces), mined 64 records, +2 new models Unlimited-OCR and Devstral-4bit-mlx (page names the repo only, no base model stated); MAPs for GLM-5.3-Flash-UNCENSORED JK oQ3.5e, Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive OptiQ-4bit MLX, Qwen3.8-27B-heretic-ara oQ8e MTP, qwen35-9b 4bit to Qwen3.5-9B.
- Dataset 26815 -> 26879, 584 -> 586 models, community 25852 -> 25916. check_quotes green (27532 verified).

## 2026-10-14: llama.cpp pulse #30535 + #30526 (+22 rows)

- #30535 (OpenCL dp4a q4_0 GEMM default for batched matmul): mined 10 records, pp512 prefill tok/s before/after on Adreno 840 (Llama-3.2-1B 849 → 998, Gemma 4 E4B 132 → 152), Adreno 850 (Llama-3.2-1B 1202 → 1371) and X2-90 (Gemma 4 E2B 881 → 1028, Qwen3.8-27B 95.8 → 110.3); +3 hardware labels Adreno 840, Adreno 850, X2-90 (page wording, distinct from existing Adreno X2-90).
- #30526 (ggml-cpu pad_f32 optimization): mined 12 records, llama-bench prefill tok/s old/new on Intel(R) Xeon(R) Platinum 8488C with gemma-embedding2 0.3B Q4_K_M at pp8 (652.25 → 1460.06, 2.24x) through pp1024 (2366.24 → 2535.64); +1 new model gemma-embedding2 0.3B, +1 hardware label Intel(R) Xeon(R) Platinum 8488C. Parked: #30553 (RTX 5090 Stream-K caps, model never named), #30542 (no tables).
- Dataset 26793 -> 26815, 438 -> 442 hardware, 583 -> 584 models, sourced 941 -> 963. check_quotes green (27468 verified).

## 2026-10-14: oMLX batch 472 (+64 rows)

- scan456 sweep (60 new traces), mined 64 records, +1 new model Qwen3.5-9B-OmniCoder-Claude-Polaris; MAPs for Agents-A1 4bit, KAT-Coder-V2.5-Dev-VL oQ6e MTP, Ornith-1.5-35B-A3B OptiQ-4bit (mlx-community prefix variant).
- Dataset 26729 -> 26793, 582 -> 583 models, community 25788 -> 25852. check_quotes green (27446 verified).

## 2026-10-14: vLLM pulse #61088 (+12 rows)

- #61088 (fused DeepSeek-V4.1 C1/C2 compression with RoPE, FP8 quantization and 584-byte cache write): mined 12 records, two TP4 instances crossover on H20-3e SM90, DeepSeek-V4.1-Flash with real DSpark 5 acceptance, cold/warm 4K/16K at c4/c16 baseline vs fused aggregate output tok/s (cold 16K/c16 355.06/354.86, warm 846.13/839.59, cold 4K 479.74/470.55, warm 562.92/520.78, cold 16K/c4 270.43/276.63, warm 526.67/531.65); precision unstated on page, +1 hardware label H20-3e; per-cell phase splits and CV in notes.
- Dataset 26717 -> 26729, 437 -> 438 hardware, sourced 929 -> 941. check_quotes green (27382 verified).

## 2026-10-14: oMLX batch 471 (+73 rows)

- scan455 sweep (60 new traces), mined 73 records, no new models or hardware, no new MAP entries needed.
- Dataset 26644 -> 26717, community 25715 -> 25788. check_quotes green (27370 verified).

## 2026-10-14: vLLM pulse #61091 + #61421 (+93 rows)

- #61091 (native Triton per-token FP8 linear for Radeon AI PRO R9700 / gfx1201): mined 16 records, TP1 serving of Gemma 4 12B FP8-Dynamic, GuideLLM 8-turn 2048-token workload, streams 1/2/4/8 across two same-GPU pairs, Torch RowWise vs native Triton mean per-request output rate (28.09 → 32.62 tok/s at 1 stream up to 20.65 → 23.60 at 8 streams, +14-18%); GSM8K accuracy run was TP2 and is not mined.
- #61421 (opt-in ROCM_RDNA_SINGLESEQ_ATTN for gfx1151 RDNA3.5): mined 77 records, single-sequence vllm bench serve decode tok/s across three arms (ours / ROCM_ATTN / ROCM_SEGMENTED_ATTN) for Llama 3.1 8B AWQ-INT4 EAGLE3, Qwen3.5-9B (quant unstated), Qwen3.6-27B AWQ-INT4 at in/out 128/4k/16k × 128/4k/16k, plus the Gemma 4 D=512 tables against TRITON_ATTN for Gemma 4 26B-A4B AWQ-4bit and Gemma-4-31B AWQ-4bit MTP; the page names the GPU only as gfx1151, so that is the hardware label; one ROCM_ATTN 128/16k cell timed out and is skipped. Parked: #61257 (tiny test checkpoint), #61029 (percentages only), #61118/#60947/#60843/#60844 (no serving tables).
- Dataset 26551 -> 26644, 436 -> 437 hardware, sourced 836 -> 929. check_quotes green (27297 verified).

## 2026-10-14: oMLX batch 470 (+66 rows)

- scan454 sweep (60 new traces), mined 66 records, no new models or hardware; Cyber-Tiel-Coder-35B-A3B oQ4e REAP-19B mapped to the existing Cyber-Tiel-Coder-35B-A3B label with the REAP-19B pruned variant in notes (full trace name interleaves the quant, breaking the substring rule), Gemma-4-26B-A4B-IT-6Bit to Gemma 4 26B-A4B 6bit, Phi-3.5-mini-instruct 4bit (mlx-community prefix variant), Qwen3.8-27B-Uncensored / Qwen3.8-Flash-Next oQ2.5e / Qwopus3.8-27B-Flash-V2 fp16 MTP builds.
- Dataset 26485 -> 26551, community 25649 -> 25715. check_quotes green (27204 verified).

## 2026-10-14: vLLM pulse #61435 + #61264 + #61555 + #60932 (+43 rows)

- #61435 (Kimi-K3 mono decode M1, TP8 on MI355X): mined 19 records, InferenceX recipe k=7 c1 at DCP1 with three arms (base 178.20, #60683 221.79, #61435 226.77 output tok/s, random 8k/1k synthetic acceptance 3.84) plus the k=3 serving tables at DCP1 (69.5/100.3, 233.9/256.2, 403.1/315.9, 644.7/401.2) and DCP8 (65.7/103.4, 214.4/248.6, 373.2/300.0, 585.6/375.4) base/mono at c1-c16; c8/c16 mono runs past the 16-row cap fall back to the vLLM path, noted; MoE MXFP4 weights with BF16 dense linears (FP8 online quant removed), fp8 KV.
- #61264 (TurboQuant verify batch + split-KV, Qwen2.5-3B-Instruct BF16 on one MI355X): mined 12 records, eager speculative cells 1024/16/128 347.68/942.92, 8192/16/128 443.52/736.38, 8192/64/128 499.36/568.81 and the graph-enabled scope check 2688.94/2681.27, 918.01/953.94, 570.16/570.92 base/patched; +1 new model Qwen2.5-3B-Instruct.
- #61555 (DeepSeek V4.1 PCP decode-only CUDA graphs on four H20 TP1/PCP4/EP4): mined 6 records, GSM8K natural-question serving c1 32.494/169.756 and c4 82.069/369.892 output tok/s eager/graph plus the cold 64K prefill input tok/s 15,255.437/15,265.495; +1 hardware label H20 (page writes Four H20 GPUs, TP1/PCP4/EP4 in notes).
- #60932 (peer-device expert tier, DGX Station GB300 + RTX PRO 6000 sidecar, DeepSeek-V4.1-Flash MXFP4): mined 6 records, decode c1/c16/c32 output tok/s UVA 268.7/722.7/927.5 vs sidecar 528.7/2,048.7/2,616.5 (1.97x-2.83x); the K-notation prefill rows are not mined; board power in notes. Parked: #60893 (e2e delta-only), #61553 (no serving table), #61242 (test counts only).
- Dataset 26442 -> 26485, 435 -> 436 hardware, 581 -> 582 models, sourced 793 -> 836. check_quotes green (27138 verified).

## 2026-10-14: llama.cpp pulse #30380 + #30276 (+25 rows)

- #30380 (trimmed draft vocab `--spec-draft-vocab-dynamic 16384`): SPEED-Bench qualitative decode tok/s full-head vs trimmed arms, mined 16 records on DGX Spark GB10 (Qwen3.8-Flash-Next UD-IQ4_XS 41.51/43.97, Gemma 4 12B 67.31/68.42, Qwen3.6-27B 24.29/26.77), RTX PRO 6000 Blackwell Workstation Edition (155.87/157.33, 285.98/287.33, 135.98/145.14) and RTX 5090 (Gemma 4 12B 279.09/278.37, Qwen3.6-27B 130.11/136.59; Flash-Next does not fit 32 GB); draft-mtp max 3, acceptance rates in notes.
- #30276 (Bonsai 2 27B PQ2_0 on RTX 5060 Ti 16 GB): decode-throughput collapse bug report, mined 9 records, aggregate decode tok/s at n_ctx/--parallel (32k np8 127.8, 131k np8 127.3, 196k-245k np4 112-115, 262k np2 79.7, np1 47.9, np8 13.3 collapsed, 524k np2 11.0; per-request values in notes); the np=4 collapse row is a range (3.6-3.9), not mined. Parked: #30343/#30342 (range values), #30449/#30342 (no absolute serving numbers).
- Dataset 26417 -> 26442, sourced 777 -> 793, community 25640 -> 25649. check_quotes green (27095 verified).

## 2026-10-14: vLLM ROCm pulse #61325 + #61109 + #60895 (+33 rows)

- #61325 (Qwen3.8-Flash-Next MXFP4, TP2 on MI355X gfx950): mono decode layer opt-in, mined 20 records, aggregate output tok/s stock/mono at 8k/1k c1-c8 and 60k/600 c1/c4 (146.8/253.8, 267.4/417.0, 443.5/632.2, 642.5/854.7, 84.5/99.8, 143.3/154.7) plus the MTP-3 table (284.4/379.1, 397.2/491.2, 654.0/684.5, 123.7/133.0; the c4 MTP row runs stock in both arms, noted as the noise floor); TP2 in notes per the #61573 precedent, TTFT/TPOT medians in notes.
- #61109 (Qwen2.5-72B-Instruct, 8x MI210 gfx90a TP8): ISLAND all-reduce backend for two 4-GPU XGMI islands joined by PCIe, mined 10 records, aggregate output tok/s off/on on decode c1/c8/c16 (37.2/42.5, 147/190, 287/351) and 3k-prompt prefill c1/c8 (19.0/22.3, 34.3/42.2); quant unstated on the page; +1 new model Qwen2.5-72B-Instruct, +1 hardware label 8x MI210 (page writes 8x MI210 in ASCII, unlike the MI355X pages).
- #60895 (GLM-5.3-Flash FP8, 4x B200): DeepGEMM FP8 MegaMoE vs TP4 and DEP4 generic MoE, mined 3 records, AgentX replay concurrency 96 output tok/s 3,152 / 2,063 / 3,332 (MTP-5 synthetic acceptance 3.61, TTFT/ITL in notes); the random-prompt microbench rows have no stated concurrency, not mined. Parked: #61273 (diffusion image shapes), #60936 (prefill ms only), #60833 (kernel launch counts).
- Dataset 26384 -> 26417, 434 -> 435 hardware, 580 -> 581 models, sourced 744 -> 777. check_quotes green (27070 verified).

## 2026-10-14: oMLX batch 469 (+69 rows)

- oMLX corpus sweep: 69 records mined (scan453, 60 fetched, 60 new candidates, 0 stale 404s). No new models. 1 MAP added: Occamy-1.0-oQ6e-mtp -> Occamy-1.0 (oQ6e, MTP speculative decoding enabled). Top models: Qwen3.8-27B (13), Qwen3.8-Flash-Next (13), Occamy-1.0 (11), GLM-5.3-Flash (10), Ornith-1.5-35B-A3B (7). oMLX total 21276 -> 21345. known.txt = 15387.
- Dataset 26315 -> 26384, 434 hardware, 580 models, 45 backends. check_quotes green (27037 verified).

## 2026-10-14: vLLM ROCm pulse #61682 + #61694, #60470 GB300 rewrite (+17 rows)

- vLLM PR pulse triage. #61682 (DeepSeek-V4.1-Flash MXFP8, TP4 on 4x MI325X gfx942): ROCm decoder-replay kept-length rule (unfinished prefill chunk keeps 1 replay row), mined 10 records, aggregate tok/s at 8k/256k in x 1k out x MC2/MC6/MC8 x baseline/one-row (431.1/430.2, 165.8/165.7, 699.8/714.8, 95.5/98.2, 109.3/113.5; median TTFT/TPOT in notes, one run per cell). #61694 (Kimi-K3, TP8 on 8x MI355X, quant unstated): pipeline mono verification kernels through 48 tokens, mined 7 records, aggregate output tok/s on AgenticX conc8/k7 (312.49/312.29, single round no stable difference) and conc4/k5 (181.91/190.84, cross-machine, flagged in notes) and 8k/1k conc8/k5 (non-mono 446.27, #60683 334.99, this PR 472.28 provisional). Parked: #61646 (kernel microbenchmarks, ratios only), #61604 (scheduling microbenchmarks), #61615 (accuracy tables only). #60470 (Kimi-K3 NVFP4, TP8 over two GB300 nodes) page rewrite: the old single total-tok/s line (8213) was replaced upstream by a 5-scenario native-vs-fiauto serving table; re-mined as 10 records, out tok/s at c32/c32-warm/c8/c1/c1-8k (909/902, 946/942, 413/415, 78.2/78.7, 29.6/29.4, one run per arm within +/-1.5%). Dataset 26289 -> 26315, sourced 717 -> 744. check_quotes green (26968 verified).

## 2026-10-14: oMLX batch 468 (+68 rows)

- oMLX corpus sweep: 68 records mined (scan452, 60 fetched, 60 new candidates, 0 stale 404s). +1 new model: Phi-3.5-mini-instruct (4bit MLX, M5 Max 40c; new family). 1 MAP -> existing: Qwen3.5-0.8B-oQ6 -> Qwen3.5-0.8B (oQ6). Models 579 -> 580. oMLX total 21208 -> 21276. known.txt = 15327.
- Dataset 26221 -> 26289, 434 hardware, 580 models, 45 backends. check_quotes green (26942 verified).

## 2026-10-14: Ternary Bonsai 2 HF card rewrite (RTX 4070 depth table)

- Upstream rewrote the CaryPalmer/Ternary-Bonsai-2-27B-262k-GGUF model card: the 2026-10-07 two-column depth table (decode / prefill) was replaced by a 2026-10-08 three-column table (decode new text / decode code / prefill, fresh prompt at each depth, 400-token greedy answers with default lookup+MTP drafting). Re-mined all 8 hf1-ternary4070 records to the new numbers (4k 102/1,173; 16k 83/1,137; 32k 78/1,031; 64k 69/867; 112k 61/698; 131k 30/649; 180k 17.9/547; 258k 8.6/436; decode new-text tok/s / cumulative prefill tok/s), dates 2026-10-07 -> 2026-10-08. Added the card URL to scripts/force_refresh.txt so CI replaces its cached copy. Record count unchanged.

## 2026-10-14: vLLM ROCm pulse: #61482 + #61573 (+14 rows)

- vLLM PR pulse triage of the open ROCm perf PRs. #61482 (DeepSeek-V4-Pro FP8, TP8 on MI355X gfx950): InferenceX AgentX closed-loop mono-decode A/B, mined 6 records, P50 tok/s/user at c1/c4/c8 x mono off/on (241/299, 218/247, 192/201; +24/+13/+5%); both arms run DSpark spec-decode with 6 drafts (synthetic acceptance 3.77), aggregate output and P90/ITL in notes; +1 new model DeepSeek-V4-Pro (the earlier #41603 GB200 rows are scope=cluster reference rows). #61573 (Qwen3.8-27B-Quark-AWQ-MXFP4, MI355X): FlyDSL dense mono decode opt-in, mined 8 records, aggregate output tok/s at c4/c8 x TP1/TP2 x non-mono/mono (430.1/576.4, 751.7/911.4, 579.6/655.8, 987.1/1080.7; 8k in / 1k out sglang.bench_serving; ITL/TPOT/TTFT medians in notes); the c16+ table is stock-graph replay with mono inactive, not mined. Parked: #61498 (delta-only percentages, no absolute numbers). TP8/TP2 rows carry the GPU count in notes per the vllm-58887/58944 precedent (the #61482 page writes 8x MI355X only as 8x, which the quote checks cannot match). Dataset 26207 -> 26221, models 578 -> 579. check_quotes green (26874 verified).

## 2026-10-14: oMLX batch 467 (+65 rows)

- oMLX corpus sweep: 65 records mined (scan451, 60 fetched, 60 new candidates, 0 stale 404s). +1 new model: Anubis-70B (4bit MLX, M1 Max 32c). 1 MAP -> existing: Qwen3.8-Flash-Next-oQ3.5e-fp16-mtp -> Qwen3.8-Flash-Next (oQ3.5e, fp16 MTP build). Models 577 -> 578. oMLX total 21143 -> 21208. known.txt = 15267.
- Dataset 26142 -> 26207, 434 hardware, 578 models, 45 backends.

## 2026-10-14: vLLM #60413 source rewrite (Qwen3.8-27B, AMD Strix Halo)

- Upstream edited the #60413 comment in place: the old "Flag on (this PR)" MTP table (12.45 / 22.45) was removed and replaced with a clean decode-kernel comparison table. Re-mined the 2 stale records into 3 clean arms (all MTP=3, single stream max-num-seqs 1, AMD Strix Halo gfx1151 RDNA 3.5, Qwen3.8-27B-Quark-AWQ-MXFP4, vllm bench serve random 128 in/256 out, decode tok/s): This PR W4A8 int8-dot GEMV 28.89, #46676 W4A16 scalar FMA 26.19, Emulation dequant+F.linear 4.94. Added #60413 to scripts/force_refresh.txt so CI replaces its cached copy of the edited page. github_issues.json 1963 -> 1964. Dataset 26141 -> 26142. check_quotes green (26795 verified).

## 2026-10-14: oMLX batch 466 (+68 rows)

- oMLX corpus sweep: 68 records mined (scan450, 79 new ids in listing (total 19427), 60 fetched, 60 new candidates, 0 stale 404s). +2 new models: gemma-4-26B-A4B-it-oQ8e-fp16-mtp (oQ8e, M2 Max 38c; mtp_enabled=true spec-decode, full-title label kept separate), gemma-4-E2B-Heretic-Uncensored (4bit MLX, M1 Max 32c; distinct uncensored fine-tune). 5 MAP -> existing: gemma-4-12B-it-qat-bf16 -> gemma-4-12B-it-qat (bf16), gemma-4-26B-A4B-it-qat-oQ8-fp16 -> gemma-4-26B-A4B-it-qat (oQ8), gemma-4-26B-A4B-it-uncensored-heretic-ara-MLX-8bit-int8-affine-betterCache -> gemma-4-26B-A4B-it-uncensored-heretic-ara (8bit MLX), gpt-oss-20b-MXFP4-Q4 -> gpt-oss 20B (MXFP4-Q4), mistralai_Devstral-Small-2-24B-Instruct-2512-MLX-8Bit -> Devstral-Small-2-24B-Instruct-2512 (8bit MLX). Models 575 -> 577. oMLX total 21075 -> 21143. known.txt = 15207.
- Dataset 26073 -> 26141, 434 hardware, 577 models, 45 backends.

## 2026-10-14: oMLX batch 465 (+73 rows)

- oMLX corpus sweep: 73 records mined (scan449, 41 new ids in listing (total 19348), 60 fetched, 60 new candidates, 0 stale 404s). +4 new models: Fara1.5-9B (OptiQ-4bit, M1 Max 32c), Rocinante-X-12B (8bit MLX, M1 Max 32c), Skyfall-31B (Mixed-4-8 MLX, M1 Max 32c), Skyfall-31B-v4.2-heretic (8bit MLX, M1 Max 32c; distinct heretic fine-tune, version kept in label so it is a substring of the trace title). 3 MAP -> existing: Artemis-31B-v1.1-mlx-8Bit -> Artemis-31B (8bit MLX), Artemis-31B-v1.1-oQ4e -> Artemis-31B (oQ4e), gemma-4-26B-A4B-it-qat-mxfp4 -> gemma-4-26B-A4B-it-qat (mxfp4). Models 571 -> 575. oMLX total 21002 -> 21075. known.txt = 15147.
- Dataset 26000 -> 26073, 434 hardware, 575 models, 45 backends. check_quotes green (26726 verified).

## 2026-10-14: oMLX batch 464 (+68 rows)

- oMLX corpus sweep: 68 records mined (scan448, 77 new ids in listing (total 19307), 60 fetched, 60 new candidates, 0 stale 404s). +5 new models: JOSIE-2-4B (quant unstated, M1 Max 32c), JOSIE-2-9B-OSS (quant unstated, M1 Max 32c), Llama-3.2-3B-Instruct-uncensored (6bit, M1 Max 32c; distinct uncensored fine-tune), MagenticBrain (8bit, M1 Max 32c), Nex-N2-mini-MLX-VLM-4bit-MTP (4bit, M1 Max 32c; mtp_enabled=true VLM spec-decode, full-title label kept separate). 2 MAP -> existing: Laguna-XS-2.1-MLX-8bit -> Laguna XS 2.1 (space form), Nex-N2.5-mini-MLX-oQ4 -> Nex-N2.5-mini (oQ4 MLX). Models 566 -> 571. oMLX total 20934 -> 21002. known.txt = 15087.
- Dataset 25932 -> 26000, 434 hardware, 571 models, 45 backends. check_quotes green (26653 verified).

## 2026-10-14: oMLX batch 463 (+59 rows)

- oMLX corpus sweep: 59 records mined (scan447, 38 new ids in listing (total 19230), 60 fetched, 60 new candidates, 0 stale 404s). +1 new model: Artemis-31B (6bit MLX, M1 Max 32c). 8 junk traces skipped (model name is just a quant string 3bit/4bit/6bit/8bit on M1 Max 32c, no identifiable model on the page) -> added to mine.py SKIP. Models 565 -> 566. oMLX total 20875 -> 20934. known.txt = 15027.
- Dataset 25873 -> 25932, 434 hardware, 566 models, 45 backends. check_quotes green (26585 verified).

## 2026-10-14: oMLX batch 462 (+74 rows)

- oMLX corpus sweep: 74 records mined (scan446, 41 new ids in listing (total 19192), 60 fetched, 60 new candidates, 0 stale 404s). +2 new models: GPT-OSS-Coder (4bit MLX, M5 Max 40c), granite-4.2-3b (4bit MLX, M5 Pro 20c; distinct size from existing granite-4.2-30b). 1 MAP -> existing: gpt-oss-20b-oQ6e-bf16-MLX -> gpt-oss 20B (oQ6e MLX, space form). Models 563 -> 565. oMLX total 20801 -> 20875. known.txt = 14967.
- Dataset 25799 -> 25873, 434 hardware, 565 models, 45 backends. check_quotes green (26526 verified).

## 2026-10-14: oMLX batch 461 (+72 rows)

- oMLX corpus sweep: 72 records mined (scan445, 31 new ids in listing (total 19151), 60 fetched, 60 new candidates, 0 stale 404s). +3 new models: Bonsai-8B (4bit MLX, M4 10c), Gemma-4-26B-A4B-Hermes-VLM (4bit MLX, M5 10c), Qwen3.6-35B-A3B-oQ8-mtp (oQ8, M5 Max 40c; MTP speculative-decode traces kept in a separate model so they do not inflate the 1624-row base Qwen3.6-35B-A3B). 2 MAP -> existing: Qwen3.5-9B-6bit -> Qwen3.5-9B (6bit), gemma-4-e2b-it -> gemma-4-E2B-it (capital-E form avoids slug collision). Models 560 -> 563. oMLX total 20729 -> 20801. known.txt = 14907.
- Dataset 25727 -> 25799, 434 hardware, 563 models, 45 backends. check_quotes green (26452 verified).

## 2026-10-14: oMLX batch 460 (+65 rows)

- oMLX corpus sweep: 65 records mined (scan444, 24 new ids in listing (total 19120), 60 fetched, 60 new candidates, 0 stale 404s). +1 new model: Qwen3-8B-Uncensored (oQ6/oQ8, M4 Max 32c). 3 MAP entries -> existing: Qwen--Qwen3-14B-MLX-8bit -> Qwen3 14B (8bit MLX, merged with existing 4bit rows; label uses the space form to avoid slug collision), Qwen--Qwen3-8B-MLX-8bit -> Qwen3-8B (8bit MLX), mlx-community--Devstral-Small-2505-4bit -> Devstral-Small-2505 (4bit). Models 559 -> 560. oMLX total 20664 -> 20729. known.txt = 14847.
- Dataset 25662 -> 25727, 434 hardware, 560 models, 45 backends. check_quotes green (26380 verified).

## 2026-10-14: oMLX batch 459 (+64 rows)

- oMLX corpus sweep: 64 records mined (scan443, 26 new ids in listing (total 19096), 60 fetched, 60 new candidates, 0 stale 404s). No new models (all trace models IN-MAP). Models 559. oMLX total 20600 -> 20664. known.txt = 14787.
- Dataset 25598 -> 25662, 434 hardware, 559 models, 45 backends. check_quotes green (26315 verified).

## 2026-10-14: oMLX batch 458 (+64 rows)

- oMLX corpus sweep: 64 records mined (scan442, 39 new ids in listing (total 19070), 60 fetched, 60 new candidates, 0 stale 404s). +1 new model: Humanizer-12B (MLX 8bit build, M5 Max 40c; new family, no existing norm-substring). Models 558 -> 559. oMLX total 20536 -> 20600. known.txt = 14727.
- Dataset 25534 -> 25598, 434 hardware, 559 models, 45 backends. check_quotes green (26251 verified).

## 2026-10-14: oMLX batch 457 (+64 rows)

- oMLX corpus sweep: 64 records mined (scan441, 120 new ids in listing (total 19031), 60 fetched, 60 new candidates, 0 stale 404s). No new models (1 new MAP entry Qwen3.5-35B-A3B-bf16 -> existing Qwen3.5-35B-A3B, bf16 build). Models 558. oMLX total 20472 -> 20536. known.txt = 14667.
- Dataset 25470 -> 25534, 434 hardware, 558 models, 45 backends. check_quotes green (26187 verified).

## 2026-10-14: oMLX batch 456 (+63 rows)

- oMLX corpus sweep: 63 records mined (scan440, 23 new ids in listing (total 18911), 60 fetched, 60 new candidates, 0 stale 404s). No new models (7 unique trace models, all IN-MAP: Qwen3.8-27B-TURBO-Fable-Cold-Fusion NM-DAU oQ4e/oQ6e, Mellum2-12B-A2.5B, Qwen3.8-Flash-Next oQ4e/oQ3e/REAP-384, Swift-1.5-Qwen3.8-27b). Models 558. oMLX total 20409 -> 20472. known.txt = 14607.
- Dataset 25407 -> 25470, 434 hardware, 558 models, 45 backends. check_quotes green (26123 verified).

## 2026-10-14: llama.cpp parked items #30334/#30364/#30478 (+59 rows)

- Mined the three parked llama.cpp issues with clean absolute A/B tok/s tables. #30334 (Tesla P40, compute capability 6.1; MMVQ fusion stock-vs-off A/B, -ngl 99 -fa 1): Mixtral 8x7B Q2_K/Q3_K_M and Llama 3.1 8B Q4_0/Q4_K_M, tg128 at depth 0/496/2016 (24 rows) + Mixtral pp512 at -ub 1/2/4/8 (16 rows) = 40. #30364 (Radeon 8065S Strix Halo gfx1151, MiniMax-M2.7 UD-IQ4_XS): Vulkan pp512 ubatch(32/64/128/256/512) x depth(0/32768) sweep = 9 rows + ROCm build ubatch-128 reference (2 rows); depth-32768 collapses above ubatch 128 on Vulkan, no collapse on ROCm. #30478 (Arc A770, SYCL backend, gemma-2-2b-it): MMVQ GLU fusion on(default) vs off, pp512/tg128 for Q4_K_M and Q2_K = 8 rows; unfused ~1.08x faster on tg128.
- New models: Mixtral 8x7B, gemma-2-2b-it (models 556 -> 558). Dataset 25348 -> 25407, 434 hardware, 558 models, 45 backends. check_quotes green (26060 verified).
- Also backfilled the four data events committed since batch 453 without changelog entries (oMLX 455, oMLX 454, #30503, pulse batch); entries below.

## 2026-10-14: oMLX batch 455 (+63 rows)

- oMLX corpus sweep: 63 records mined (scan439, 60 fetched, 60 new candidates, 0 stale 404s; all trace models IN-MAP, no new models). Models 556. oMLX total 20346 -> 20409. known.txt = 14547.
- Dataset 25285 -> 25348, 434 hardware, 556 models, 45 backends. check_quotes green (26001 verified).

## 2026-10-14: oMLX batch 454 (+65 rows)

- oMLX corpus sweep: 65 records mined (scan438, 60 fetched, 60 new candidates, 0 stale 404s). No new models (Qwen3-VL-8B-Instruct-MLX-4bit -> existing Qwen3-VL-8B-Instruct, MLX 4bit build; 2 traces M4 10c 24GB). Models 556. oMLX total 20281 -> 20346. known.txt = 14487.
- Dataset 25220 -> 25285, 434 hardware, 556 models, 45 backends. check_quotes green (25938 verified).

## 2026-10-14: llama.cpp #30503 (+2 rows)

- Vulkan Intel Arc B580, Gemma 4 E4B Q4_0, pp16384: stock master 896 t/s vs gate-relaxed 2731 t/s (fa-off ceiling 3523). 2 rows (master + gate-relaxed arms).
- Dataset 25218 -> 25220. check_quotes green (25873 verified).

## 2026-10-14: llama.cpp pulse batch, 9 PRs/issues (+98 rows)

- Mined 9 llama.cpp PRs/issues with clean absolute A/B tok/s tables: #30215 (16), #30226 (10), #30231 (8), #30247 (6), #30249 (6), #30374 (20), #30489 (6), #30491 (6), #30493 (20) = 98 records. Convention: A/B PRs record both arms (master baseline + PR patched) as separate records. "Muse-Glimmer" relabelled to "Muse Glimmer" (10 records, avoids slug collision). Date normalized to YYYY-MM.
- New hardware pages: Adreno X2-90, B70, Xeon 6985P-C. New models: Gemma-31B, Kimi-Linear-48B-A3B. Dataset 25124 -> 25218. check_quotes green (25871 verified).

## 2026-10-14: oMLX batch 453 (+67 rows)

- oMLX corpus sweep: 67 records mined (scan437, 60 fetched, 0 stale 404s; 6 unique trace models, all IN-MAP, no new models). Models 554. oMLX total 20214 -> 20281. known.txt = 14427.
- Dataset 25057 -> 25124. check_quotes green (25773 verified).

## 2026-10-14: oMLX batch 452 (+64 rows)

- oMLX corpus sweep: 64 records mined (scan436, 60 fetched, 400 new ids in listing, 60 new candidates; 0 stale 404 ids). No new models (9 unique trace models; 7 IN-MAP + 2 new MAP entries -> existing: Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored [oQ6e, 1M NM DAU build], Gemma 4 E4B [mxfp4]). Models 554. oMLX total 20150 -> 20214. known.txt = 14367.
- Dataset 24993 -> 25057. check_quotes green (25706 verified).

## 2026-10-14: vLLM #60317 source rewrite (15 prefill arms re-mined)

- vLLM PR #60317 benchmark table re-run (main baseline 5d9214d6b2 -> ab905a885d). Re-mined all 15 A100-SXM4-80GB prefill arms (gemma-4-E2B/E4B/12B-it, ctx 2048/4096, bs 1/4/8, out=1) to the new baseline tok/s (e.g. E2B 2k b1 30604.9 -> 30314.2, E4B 2k b1 19747.7 -> 19742.0, 12B 2k b1 8313.6 -> 8268.4). PR-arm speedups now 1.02x to 1.11x (was 1.04x to 1.12x).
- Dataset 24993 (in-place rewrite, no count change). check_quotes green (25642 verified).

## 2026-10-14: oMLX batch 451 (+65 rows) + llama.cpp #10879 Vulkan rows (+4)

- oMLX corpus sweep: 65 records mined (scan435, 60 fetched, 122 new ids in listing, 60 new candidates; 0 stale 404s). No new models (14 unique trace models; 13 IN-MAP + 1 new MAP entry -> existing gemma-4-12B-it-qat [8bit QAT build]). Models 554. oMLX total 20085 -> 20150.
- llama.cpp discussion #10879 (Vulkan megathread) c18847326: Acer Nitro ANV15-41 (Ryzen 7 7735HS, 66 GiB RAM), Llama 2 7B Q4_0, ngl 100, sm none, fa 0/1, build 11540 (1e6f04a75), GPUs isolated via GGML_VK_VISIBLE_DEVICES. RTX 4060 Laptop GPU: pp512 1793.16 (fa0) / 1908.24 (fa1), tg128 52.58 / 53.80. AMD Radeon 680M iGPU (RADV, RADV_PERFTEST=nogttspill): pp512 260.18 (fa0) / 325.54 (fa1), tg128 14.58 / 15.42. 4 rows.
- Dataset 24924 -> 24993. check_quotes green (25642 verified).


## 2026-10-13: oMLX batch 449 (+72 rows, +1 model)

- oMLX corpus sweep: 72 records mined (scan433, 60 fetched, 138 new ids in listing, 60 new candidates; 0 stale 404s). +1 new model: Qwen3.8-27B-VL (distinct VL variant, per Swift VL precedent). Dagger-Qwen3.6-27B -> existing Qwen3.6-27B; qwen3.8-27b-zp -> existing Qwen3.8-27B; 2 HauhauCS-Aggressive builds -> existing. Models 552 -> 553. oMLX total 19950 -> 20022 (crossed 20k).
- Dataset 24789 -> 24861. check_quotes green (25510 verified).

## 2026-10-13: oMLX batch 448 (+67 rows, +2 models)

- oMLX corpus sweep: 67 records mined (scan432, 60 fetched, 105 new ids in listing, 60 new candidates; 0 stale 404s). +2 new models: Huihui-Ornith-1.5-35B-A3B-abliterated-VL (VL variant kept distinct per Ornith VL/Vision precedent), OmniCoder-9B (new family). Qwen3.6-35B-A3B-UD-Q4_K_XL -> existing Qwen3.6-35B-A3B. Models 550 -> 552. oMLX total 19883 -> 19950.
- Dataset 24722 -> 24789. check_quotes green (25438 verified).

## 2026-10-13: oMLX batch 447 (+65 rows)

- oMLX corpus sweep: 65 records mined (scan431, 60 fetched, 62 new ids in listing, 60 new candidates; 0 stale 404s). No new models (17 unique trace models; 14 IN-MAP + 3 new MAP entries -> existing: Laguna XS 2.1, Ornith-1.5-35B-A3B [oQ5-MTP], Qwen3.6-35B-A3B [oQ5-MTP]). Models 550. oMLX total 19818 -> 19883.
- Dataset 24657 -> 24722. check_quotes green (25371 verified).

## 2026-10-13: oMLX batch 446 (+64 rows)

- oMLX corpus sweep: 64 records mined (scan430, 60 fetched, 73 new ids in listing, 60 new candidates; 0 stale 404s). No new models (15 unique trace models; 11 IN-MAP + 4 new MAP entries -> existing: Qwen3.8-27B [2bit TextOnly, mlx-4Bit], gemma-4-26B-A4B-it [oQ6e-mtp], Qwen3-Coder-Next [mlx-community 4bit]). Models 550. oMLX total 19754 -> 19818.
- Dataset 24593 -> 24657. check_quotes green (25306 verified).

## 2026-10-13: oMLX batch 445 (+63 rows, +1 model)

- oMLX corpus sweep: 63 records mined (scan429, 60 fetched, 85 new ids in listing, 60 new candidates; 0 stale 404s). +1 new model: glm53 (abbreviated GLM-5.3 trace title; base name not a norm-substring of "glm53", forced distinct). GLM-4.7-Flash-MLX-6bit -> existing GLM-4.7-Flash. Models 549 -> 550. oMLX total 19691 -> 19754.
- Dataset 24530 -> 24593. check_quotes green (25242 verified).

## 2026-10-13: oMLX batch 444 (+66 rows)

- oMLX corpus sweep: 66 records mined (scan428, 60 fetched, 80 new ids in listing, 60 new candidates; 0 stale 404s). No new models (23 unique trace models; 20 IN-MAP + 3 new MAP entries -> existing: llama-3-2-1b-instruct [Llama-3.2-1B-Instruct trace, lowercase existing form], Qwen3.8-27B [nvfp4], gemma-4-26B-A4B-it-qat [q4_0 mlx-aligned]). Models 549. oMLX total 19625 -> 19691.
- Dataset 24464 -> 24530. check_quotes green (25179 verified).

## 2026-10-13: oMLX batch 443 (+69 rows)

- oMLX corpus sweep: 69 records mined (scan427, 60 fetched, 58 new ids in listing, 60 new candidates; 0 stale 404s). No new models (17 unique trace models; 16 IN-MAP + 1 new MAP entry -> existing Qwen3.8-35B-A3B-Distill, MiniPlus build). Models 549. oMLX total 19556 -> 19625.
- Dataset 24395 -> 24464. check_quotes green (25113 verified).

## 2026-10-13: oMLX batch 442 (+71 rows)

- oMLX corpus sweep: 71 records mined (scan426, 60 fetched, 61 new ids in listing, 60 new candidates; 0 stale 404s). No new models (14 unique trace models; 13 IN-MAP + 1 new MAP entry -> existing Qwen3.8-27B, 4bit MTP build). Models 549. oMLX total 19485 -> 19556.
- Dataset 24324 -> 24395. check_quotes green (25044 verified).

## 2026-10-13: oMLX batch 441 (+72 rows, +1 model)

- oMLX corpus sweep: 72 records mined (scan425, 60 fetched, 57 new ids in listing, 60 new candidates; 0 stale 404s). +1 new model: gemma-4-E4B-it-ultra-uncensored-heretic (distinct uncensored-heretic variant, per gemma-4-26B-A4B-it-ultra-uncensored-heretic precedent; mixed 4+6bit). Models 548 -> 549. oMLX total 19413 -> 19485.
- Dataset 24252 -> 24324. check_quotes green (24973 verified).

## 2026-10-13: oMLX batch 440 (+79 rows)

- oMLX corpus sweep: 79 records mined (scan424, 60 fetched, 72 new ids in listing, 60 new candidates; 0 stale 404s). No new models (12 unique trace models all IN-MAP). Models 548. oMLX total 19334 -> 19413.
- Dataset 24173 -> 24252. check_quotes green (24901 verified).

## 2026-10-13: oMLX batch 439 (+65 rows)

- oMLX corpus sweep: 65 records mined (scan423, 60 fetched, 115 new ids in listing, 60 new candidates; 0 stale 404s). No new models (14 unique trace models; 13 IN-MAP + 1 new MAP entry -> existing Occamy-1.0, MLX 6bit build). Models 548. oMLX total 19269 -> 19334.
- Dataset 24108 -> 24173. check_quotes green (24822 verified).

## 2026-10-13: oMLX batch 438 (+72 rows)

- oMLX corpus sweep: 72 records mined (scan422, 60 fetched, 171 new ids in listing, 60 new candidates; 0 stale 404s). No new models (14 unique trace models; 13 IN-MAP + 1 new MAP entry -> existing Qwen3.6-27B, mlx-community OptiQ 4bit build). Models 548. oMLX total 19197 -> 19269.
- Dataset 24036 -> 24108. check_quotes green (24757 verified).

## 2026-10-13: source rewrites (vLLM #59973, RolanDorisTech Qwen3.8-9B-Distill)

- vLLM PR #59973 rewritten: the c=1/c=4 benchmark table was replaced with prose. Re-mined the 2 c=1 arms (stock BF16 39.4 -> NVFP4 46.5 tok/s, +18%, AL unchanged -0.4%); deleted the 2 c=4 arms (new page reports c=4 only as +9% to +11% relative, no absolute tok/s).
- HF RolanDorisTech/Qwen3.8-9B-Distill-MLX-8bit rewritten: benchmark reformatted into a new Variant/Size/Prompt/Gen/Peak table. Re-mined the 4 9B arms (gen tok/s unchanged 43.0 / 37.1 / 33.3 / 28.7) with the new quote form.
- Dataset 24038 -> 24036. force_refresh.txt set for both URLs so CI refreshes its quote cache. check_quotes green (24685 verified).

## 2026-10-13: oMLX batch 437 (+58 rows)

- oMLX corpus sweep: 58 records mined (scan421, 60 fetched, 41 new ids in listing, 53 new candidates; 7 more stale 404 ids marked dead and skipped). No new models (11 unique trace models all IN-MAP). Models 548. oMLX total 19139 -> 19197.
- Dataset 23980 -> 24038 (crossed 24k records). check_quotes green (24687 verified).

## 2026-10-13: oMLX batch 436 (+69 rows)

- oMLX corpus sweep: 69 records mined (scan420, 60 fetched, 56 new ids in listing, 55 new candidates; 5 more stale 404 ids marked dead and skipped). No new models (12 unique trace models; 11 IN-MAP + 1 new MAP entry -> existing gemma-4-26B-A4B-it, oQ4e fp16 build). Models 548. oMLX total 19070 -> 19139.
- Dataset 23911 -> 23980. check_quotes green (24629 verified).

## 2026-10-13: oMLX batch 435 (+70 rows)

- oMLX corpus sweep: 70 records mined (scan419, 60 fetched, 69 new ids in listing, 54 new candidates; 6 more stale 404 ids marked dead and skipped). No new models (17 unique trace models; 16 IN-MAP + 1 new MAP entry -> existing Qwen3.6-35B-A3B, Unsloth UD MLX build). Models 548. oMLX total 19000 -> 19070.
- Dataset 23841 -> 23911. check_quotes green (24560 verified).

## 2026-10-12: oMLX batch 434 (+68 rows)

- oMLX corpus sweep: 68 records mined (scan418, 60 fetched, 66 new ids in listing, 60 new candidates). This batch cleared a backlog: two prior scans had been blocked by a run of stale trace ids (deleted traces that return HTTP 404) sitting at the head of the fetch queue; those ids are now recorded as dead and skipped, so the scan reached the valid traces behind them. 2 new models: Coder390 (abbreviated Coder390 trace title, kept distinct since the full base name is not in the published title) and Schattenblume-31B (new family). Models 546 -> 548. oMLX total 18932 -> 19000.
- Dataset 23773 -> 23841. check_quotes green (24490 verified).

## 2026-10-12: oMLX batch 433 (+7 rows)

- oMLX corpus sweep: 7 records mined (scan415, 60 fetched, 30 new ids in listing, 2 new candidates = mined + deduped). No new models (1 unique trace model IN-MAP). Models 546. oMLX total 18925 -> 18932.
- Dataset 23766 -> 23773. check_quotes green (24422 verified).

## 2026-10-12: oMLX batch 432 (+7 rows) + vLLM #60226 source rewrite

- oMLX corpus sweep: 7 records mined (scan414, 60 fetched, 29 new ids in listing, 4 new candidates = mined + deduped). No new models (1 unique trace model IN-MAP). Models 546. oMLX total 18918 -> 18925.
- vLLM #60226 source rewrite: the stock-arm table row was reformatted to a markdown table and the numbers changed (Qwen3.6-35B-A3B NVFP4 stock: c1 117.8 -> 118.1 tok/s, c4 73.4 -> 72.9 tok/s; AL 2.919 -> 2.935, 3.126 -> 3.060, GSM8K 94.5 -> 97.0). Re-mined 2 records (c1, c4) with new values and a new verbatim quote.
- Dataset 23759 -> 23766. check_quotes green (24415 verified). force_refresh set for the vLLM #60226 URL.

## 2026-10-12: oMLX batch 431 (+16 rows)

- oMLX corpus sweep: 16 records mined (scan413, 60 fetched, 60 new ids in listing, 6 new candidates = mined + deduped). No new models (3 unique trace models all IN-MAP). Models 546. oMLX total 18902 -> 18918.
- Dataset 23743 -> 23759. check_quotes green (24408 verified).

## 2026-10-12: oMLX batch 430 (+14 rows)

- oMLX corpus sweep: 14 records mined (scan412, 60 fetched, 32 new ids in listing, 9 new candidates = mined + deduped). No new models (4 unique trace models; 3 IN-MAP + 1 new MAP entry -> existing Mellum2-12B-A2.5B-Instruct, 6bit build). Models 546. oMLX total 18888 -> 18902.
- Dataset 23729 -> 23743. check_quotes green (24392 verified).

## 2026-10-12: oMLX batch 429 (+19 rows, +1 model)

- oMLX corpus sweep: 19 records mined (scan411, 60 fetched, 29 new ids in listing, 10 new candidates = mined + deduped). 1 new model (Qwen3.8-27B-TWIN-TURBO-f-c-f-709-l-unc, abbreviated TWIN-TURBO-Fable-Cold-Fusion-709-L build with aura6; kept distinct since the abbreviated name is not a norm-substring of the Uncensored/uncher variants). Models 545 -> 546. oMLX total 18869 -> 18888.
- Dataset 23710 -> 23729. check_quotes green (24378 verified).

## 2026-10-12: oMLX batch 428 (+15 rows)

- oMLX corpus sweep: 15 records mined (scan410, 60 fetched, 44 new ids in listing, 10 new candidates = mined + deduped). No new models (5 unique trace models all IN-MAP). Models 545. oMLX total 18854 -> 18869.
- Dataset 23695 -> 23710. check_quotes green (24359 verified).

## 2026-10-12: oMLX batch 427 (+15 rows)

- oMLX corpus sweep: 15 records mined (scan409, 60 fetched, 21 new ids in listing, 11 new candidates = mined + deduped). No new models (5 unique trace models all IN-MAP, incl. TWIN-TURBO-uncher from b417). Models 545. oMLX total 18839 -> 18854.
- Dataset 23680 -> 23695. check_quotes green (24344 verified).

## 2026-10-12: oMLX batch 426 (+20 rows)

- oMLX corpus sweep: 20 records mined (scan408, 60 fetched, 33 new ids in listing, 13 new candidates = mined + deduped). No new models (6 unique trace models; 5 IN-MAP + 1 new MAP entry -> existing Qwen3.8-27B-Abliterated, MTPLX build). Models 545. oMLX total 18819 -> 18839.
- Dataset 23660 -> 23680. check_quotes green (24329 verified).

## 2026-10-12: oMLX batch 425 (+20 rows)

- oMLX corpus sweep: 20 records mined (scan407, 60 fetched, 21 new ids in listing, 13 new candidates = mined + deduped). No new models (4 unique trace models all IN-MAP). Models 545. oMLX total 18799 -> 18819.
- Dataset 23640 -> 23660. check_quotes green (24309 verified).

## 2026-10-12: oMLX batch 424 (+21 rows)

- oMLX corpus sweep: 21 records mined (scan406, 60 fetched, 11 new ids in listing, 13 new candidates = mined + deduped). No new models (4 unique trace models; 3 IN-MAP + 1 new MAP entry -> existing Qwen3.6-35B-A3B, UD MLX build). Models 545. oMLX total 18778 -> 18799.
- Dataset 23619 -> 23640. check_quotes green (24289 verified).

## 2026-10-12: oMLX batch 423 (+21 rows)

- oMLX corpus sweep: 21 records mined (scan405, 60 fetched, 41 new ids in listing, 13 new candidates = mined + deduped). No new models (7 unique trace models all IN-MAP). Models 545. oMLX total 18757 -> 18778.
- Dataset 23598 -> 23619. check_quotes green (24268 verified).

## 2026-10-12: oMLX batch 422 (+19 rows)

- oMLX corpus sweep: 19 records mined (scan404, 60 fetched, 34 new ids in listing, 13 new candidates = mined + deduped). No new models (7 unique trace models all IN-MAP). Models 545. oMLX total 18738 -> 18757.
- Dataset 23579 -> 23598. check_quotes green (24247 verified).

## 2026-10-12: oMLX batch 421 (+18 rows)

- oMLX corpus sweep: 18 records mined (scan403, 60 fetched, 37 new ids in listing, 13 new candidates = mined + deduped). No new models (4 unique trace models all IN-MAP, incl. 2 from b420). Models 545. oMLX total 18720 -> 18738.
- Dataset 23561 -> 23579. check_quotes green (24228 verified).

## 2026-10-12: oMLX batch 420 (+21 rows; glm53flash HF page source rewrite)

- oMLX corpus sweep: 21 records mined (scan402, 60 fetched, 19 new ids in listing, 13 new candidates = mined + deduped). No new models (8 unique trace models; 6 IN-MAP + 2 new MAP entries -> existing models Huihui-Qwen3.6-35B-A3B-abliterated and Qwen3.8-27B-heretic-ara). Models 545. oMLX total 18699 -> 18720.
- Source rewrite: glm53flash HF model card (hf7) was repurposed to a storage/quantization contract page; the decode-benchmark section (170 tok/s c1, 490-540 tok/s c8 on 2x RTX PRO 6000 Blackwell Max-Q) was removed. Deleted 2 hf7 records; hardware 432 -> 431. Dataset net 23542 -> 23561 (+21 mined, -2 removed).
- check_quotes green (24210 verified).

## 2026-10-12: oMLX batch 419 (+18 rows)

- oMLX corpus sweep: 18 records mined (scan401, 60 fetched, 44 new ids in listing, 13 new candidates = mined + deduped). No new models (2 unique trace models all IN-MAP). Models 545. oMLX total 18681 -> 18699.
- Dataset 23524 -> 23542. check_quotes green (24191 verified).

## 2026-10-12: oMLX batch 418 (+21 rows)

- oMLX corpus sweep: 21 records mined (scan400, 60 fetched, 34 new ids in listing, 13 new candidates = mined + deduped). No new models (3 unique trace models all IN-MAP). Models 545. oMLX total 18660 -> 18681.
- Dataset 23503 -> 23524. check_quotes green (24173 verified).

## 2026-10-12: oMLX batch 417 (+24 rows, +1 model)

- oMLX corpus sweep: 24 records mined (scan399, 60 fetched, 26 new ids in listing, 13 new candidates = mined + deduped). 1 new model (Qwen3.8-27B-TWIN-TURBO-Fable-Cold-Fusion-709-L-uncher, distinct TWIN-TURBO build, kept separate from the 709-L-Uncensored variant). Models 544 -> 545. oMLX total 18636 -> 18660.
- Dataset 23479 -> 23503. check_quotes green (24152 verified).

## 2026-10-12: oMLX batch 416 (+19 rows)

- oMLX corpus sweep: 19 records mined (scan398, 60 fetched, 23 new ids in listing, 13 new candidates = mined + deduped). No new models (5 unique trace models all IN-MAP, incl. Edge0 from b413). Models 544. oMLX total 18617 -> 18636.
- Dataset 23460 -> 23479. check_quotes green (24128 verified).

## 2026-10-12: oMLX batch 415 (+17 rows)

- oMLX corpus sweep: 17 records mined (scan397, 60 fetched, 16 new ids in listing, 13 new candidates = mined + deduped). No new models (4 unique trace models all IN-MAP). Models 544. oMLX total 18600 -> 18617.
- Dataset 23443 -> 23460. check_quotes green (24109 verified).

## 2026-10-12: oMLX batch 414 (+18 rows)

- oMLX corpus sweep: 18 records mined (scan396, 60 fetched, 33 new ids in listing, 13 new candidates = mined + deduped). No new models (6 unique trace models all IN-MAP). Models 544. oMLX total 18582 -> 18600.
- Dataset 23425 -> 23443. check_quotes green (24092 verified).

## 2026-10-12: oMLX batch 413 (+14 rows, +1 model)

- oMLX corpus sweep: 14 records mined (scan395, 60 fetched, 25 new ids in listing, 13 new candidates = mined + deduped). 1 new model (Edge0-35B-A3B-preview, 35B-A3B MoE preview). Models 543 -> 544. oMLX total 18568 -> 18582.
- Dataset 23411 -> 23425. check_quotes green (24074 verified).

## 2026-10-12: oMLX batch 412 (+16 rows)

- oMLX corpus sweep: 16 records mined (scan394, 60 fetched, 36 new ids in listing, 13 new candidates = mined + deduped). No new models (4 unique trace models all IN-MAP). Models 543. oMLX total 18552 -> 18568.
- Dataset 23395 -> 23411. check_quotes green (24060 verified).

## 2026-10-12: oMLX batch 411 (+23 rows)

- oMLX corpus sweep: 23 records mined (scan393, 60 fetched, 52 new ids in listing, 13 new candidates = mined + deduped). No new models (5 unique trace models all IN-MAP). Models 543. oMLX total 18529 -> 18552.
- Dataset 23372 -> 23395. check_quotes green (24044 verified).

## 2026-10-12: oMLX batch 410 (+18 rows)

- oMLX corpus sweep: 18 records mined (scan392, 60 fetched, 26 new ids in listing, 13 new candidates = mined + deduped). No new models (5 unique trace models all IN-MAP). Models 543. oMLX total 18511 -> 18529.
- Dataset 23354 -> 23372. check_quotes green (24021 verified).

## 2026-10-12: oMLX batch 409 (+17 rows)

- oMLX corpus sweep: 17 records mined (scan391, 60 fetched, 22 new ids in listing, 13 new candidates = mined + deduped). No new models (6 unique trace models all IN-MAP). Models 543. oMLX total 18494 -> 18511.
- Dataset 23337 -> 23354. check_quotes green (24003 verified).

## 2026-10-12: oMLX batch 408 (+22 rows)

- oMLX corpus sweep: 22 records mined (scan390, 60 fetched, 12 new ids in listing, 13 new candidates = mined + deduped). No new models (5 unique trace models all IN-MAP). Models 543. oMLX total 18472 -> 18494.
- Dataset 23315 -> 23337. check_quotes green (23986 verified).

## 2026-10-12: oMLX batch 407 (+21 rows)

- oMLX corpus sweep: 21 records mined (scan389, 60 fetched, 59 new ids in listing, 15 new candidates = mined + deduped). No new models (5 unique trace models all IN-MAP). Models 543. oMLX total 18451 -> 18472.
- Dataset 23294 -> 23315. check_quotes green (23964 verified).

## 2026-10-12: oMLX batch 406 (+24 rows) + llama.cpp #30035 source rewrite

- oMLX corpus sweep: 24 records mined (scan388, 60 fetched, 15 new ids in listing, 20 new candidates = mined + deduped). No new models (7 unique trace models all IN-MAP). Models 543. oMLX total 18427 -> 18451.
- Source change: llama.cpp PR #30035 page re-run (master baseline moved 7049ff0cb -> c479922, all 7 rows re-benchmarked). 14 records (7 A/B pairs) re-mined to new tg64 values; notes commit updated to c479922. force_refresh.txt used.
- Dataset 23270 -> 23294. check_quotes green (23943 verified).

## 2026-10-12: oMLX batch 405 (+33 rows, +1 model)

- oMLX corpus sweep: 33 records mined (scan387, 60 fetched, 14 new ids in listing, 20 new candidates = mined + deduped). 1 new model (Qwythos-9B-Claude-Mythos-5-1M-BF16-MLX-MTP-Visual, Claude-Mythos variant kept distinct). Qwen3.8-35B-A3B-Distill-MLX-APEX-MiniPlus-Abliterated -> existing base. Models 542 -> 543. oMLX total 18394 -> 18427.
- Dataset 23237 -> 23270. check_quotes green (23919 verified).

## 2026-10-12: oMLX batch 404 (+29 rows)

- oMLX corpus sweep: 29 records mined (scan386, 60 fetched, 6 new ids in listing, 20 new candidates = mined + deduped). No new models (5 unique trace models all IN-MAP). Models 542. oMLX total 18365 -> 18394.
- Dataset 23208 -> 23237. check_quotes green (23886 verified).

## 2026-10-12: oMLX batch 403 (+34 rows)

- oMLX corpus sweep: 34 records mined (scan385, 60 fetched, 62 new ids in listing, 20 new candidates = mined + deduped). No new models (6 unique trace models all IN-MAP). Models 542. oMLX total 18331 -> 18365.
- Dataset 23174 -> 23208. check_quotes green (23857 verified).

## 2026-10-12: oMLX batch 402 (+32 rows) + vLLM #60153 source rewrite

- oMLX corpus sweep: 32 records mined (scan384, 60 fetched, 43 new ids in listing, 20 new candidates = mined + deduped). No new models (6 unique trace models; 5 already in MAP, 1 added as qwen3.8-flash-next-oQ4e -> existing Qwen3.8-Flash-Next). Models 542. oMLX total 18269 -> 18331.
- Source change: vllm-60153 PR page rewritten. Old 8k/262k off/on rows replaced by a Concurrency-2 table with columns (Output tok/s, Mean TTFT, Mean TPOT, Median TPOT) for shapes 262144->1024 and 8192->1024. All 4 values re-run. 4 records re-mined: off-262k 32.84/37310.48, on-262k 33.58/36063.46, off-8k 155.45/1101.50, on-8k 155.50/1070.71. force_refresh.txt used.
- Dataset 23142 -> 23174. check_quotes green (23823 verified).

## 2026-10-12: oMLX batch 401 (+30 rows)

- oMLX corpus sweep: 30 records mined (scan383, 60 fetched, 58 new ids in listing, 20 new candidates = mined + deduped). No new models (6 unique trace models all IN-MAP). Models 542. oMLX total 18269 -> 18299.
- Dataset 23112 -> 23142. check_quotes green (23791 verified).

## 2026-10-12: oMLX batch 400 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan382, 60 fetched, 36 new ids in listing, 20 new candidates = mined + deduped). No new models (8 unique trace models all IN-MAP). Models 542. oMLX total 18244 -> 18269.
- Dataset 23087 -> 23112. check_quotes green (23761 verified).

## 2026-10-12: oMLX batch 399 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan381, 60 fetched, 33 new ids in listing, 20 new candidates = mined + deduped). No new models (8 unique trace models all IN-MAP). Models 542. oMLX total 18219 -> 18244.
- Dataset 23062 -> 23087. check_quotes green (23736 verified).

## 2026-10-12: oMLX batch 398 (+26 rows)

- oMLX corpus sweep: 26 records mined (scan380, 60 fetched, 16 new ids in listing, 20 new candidates = mined + deduped). No new models (4 unique trace models all IN-MAP). Models 542. oMLX total 18193 -> 18219.
- Dataset 23036 -> 23062. check_quotes green (23711 verified).

## 2026-10-12: oMLX batch 397 (+31 rows)

- oMLX corpus sweep: 31 records mined (scan379, 60 fetched, 12 new ids in listing, 20 new candidates = mined + deduped). No new models (4 unique trace models all IN-MAP). Models 542. oMLX total 18162 -> 18193.
- Dataset 23005 -> 23036. check_quotes green (23685 verified).

## 2026-10-12: oMLX batch 396 (+24 rows)

- oMLX corpus sweep: 24 records mined (scan378, 60 fetched, 29 new ids in listing, 20 new candidates = mined + deduped). No new models (3 unique trace models all IN-MAP). Models 542. oMLX total 18138 -> 18162.
- Dataset 22981 -> 23005. check_quotes green (23654 verified).

## 2026-10-12: oMLX batch 395 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan377, 60 fetched, 44 new ids in listing, 20 new candidates = mined + deduped). No new models (6 unique trace models all IN-MAP). Models 542. oMLX total 18113 -> 18138.
- Dataset 22956 -> 22981. check_quotes green (23630 verified).

## 2026-10-12: oMLX batch 394 (+27 rows)

- oMLX corpus sweep: 27 records mined (scan376, 60 fetched, 21 new ids in listing, 20 new candidates = mined + deduped). No new models (8 unique trace models all IN-MAP). Models 542. oMLX total 18086 -> 18113.
- Dataset 22929 -> 22956. check_quotes green (23605 verified).

## 2026-10-12: oMLX batch 393 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan375, 60 fetched, 8 new ids in listing, 20 new candidates = mined + deduped). No new models (4 unique trace models all IN-MAP). Models 542. oMLX total 18058 -> 18086.
- Dataset 22901 -> 22929. check_quotes green (23578 verified).

## 2026-10-12: oMLX batch 392 (+24 rows)

- oMLX corpus sweep: 24 records mined (scan374, 60 fetched, 78 new ids in listing, 20 new candidates = mined + deduped). No new models (5 unique trace models all IN-MAP). Models 542. oMLX total 18034 -> 18058.
- Dataset 22877 -> 22901. check_quotes green (23550 verified).

## 2026-10-12: oMLX batch 391 (+28 rows) + source rewrite (vLLM PR #60110)

- oMLX corpus sweep: 28 records mined (scan373, 60 fetched, 38 new ids in listing, 20 new candidates = mined + deduped). No new models (9 unique trace models all map to existing; ThinkingCap-Qwen3.8-27B-8bit -> ThinkingCap-Qwen3.8-27B). Models 542. oMLX total 18006 -> 18034.
- Source rewrite (vLLM PR #60110, Kimi-K3 on 8x MI355X): page rewritten upstream from colon format to a markdown table; after-values re-run (throughput 702.87 -> 693.13, Mean TTFT 344.50 -> 336.53 ms). Re-mined both records: quote -> verbatim table-row fragments "Output throughput (tok/s) | 685.62 | 693.13 | +1.1%" / "Mean TTFT (ms) | 340.08 | 336.53 | -1.0%" / "c14 point". force_refresh.txt added so CI re-fetches.
- Dataset 22849 -> 22877. check_quotes green (23526 verified).

## 2026-10-12: oMLX batch 390 (+24 rows)

- oMLX corpus sweep: 24 records mined (scan372, 60 fetched, 74 new ids in listing, 20 new candidates = mined + deduped). No new models (7 unique trace models all IN-MAP). Models 542. oMLX total 17982 -> 18006.
- Dataset 22825 -> 22849. check_quotes green (23498 verified).

## 2026-10-12: oMLX batch 389 (+27 rows)

- oMLX corpus sweep: 27 records mined (scan371, 60 fetched, 49 new ids in listing, 20 new candidates = mined + deduped). No new models (8 unique trace models all map to existing; MiMo-V2.6-Distill-Qwen-9B-OptiQ -> MiMo-V2.6-Distill-Qwen-9B). Models 542. oMLX total 17955 -> 17982.
- Dataset 22798 -> 22825. check_quotes green (23474 verified).

## 2026-10-12: source rewrite (vLLM PR #59082)

- vLLM PR #59082 description was edited upstream: opening line changed from "Extend AMX-BF16 CPU attention's grouped-query (GQA) scheduling to eligible" to "Extend CPU attention's ...". Re-mined the 6 affected records (vllm-59082-amx-*): first quote fragment replaced with the verbatim title fragment "Improve long-context MTP attention scheduling on AMX" (still contains the AMX hardware token). Table values unchanged. Dataset count unchanged (22798).

## 2026-10-12: oMLX batch 388 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan370, 60 fetched, 47 new ids in listing, 20 new candidates = mined + deduped). No new models (7 unique trace models all map to existing; Qwen3.5-0.8B-bf16 -> Qwen3.5-0.8B). Models 542. oMLX total 17927 -> 17955.
- Dataset 22770 -> 22798. check_quotes green (23447 verified).

## 2026-10-12: oMLX batch 387 (+27 rows)

- oMLX corpus sweep: 27 records mined (scan369, 60 fetched, 20 new ids in listing, 20 new candidates = mined + deduped). No new models (9 unique trace models all map to existing; Gemma AEON Abliterated -> gemma-4-12b-it, Qwen3.6 UD MLX -> Qwen3.6-35B-A3B). Models 542. oMLX total 17900 -> 17927.
- Dataset 22743 -> 22770. check_quotes green (23419 verified).

## 2026-10-12: oMLX batch 386 (+24 rows)

- oMLX corpus sweep: 24 records mined (scan368, 60 fetched, 21 new ids in listing, 20 new candidates = mined + deduped). 1 new model: dsv4-0731 (author abbreviation for DeepSeek-V4-Flash-0731, mxfp4; kept distinct like dsv4-flash-vision-exp since the full name is not a norm-substring of the trace title). Models 541 -> 542. oMLX total 17876 -> 17900.
- Dataset 22719 -> 22743. check_quotes green (23392 verified).

## 2026-10-12: oMLX batch 385 (+26 rows)

- oMLX corpus sweep: 26 records mined (scan367, 60 fetched, 25 new ids in listing, 20 new candidates = mined + deduped). No new models (10 unique trace models all map to existing; MTPLX Optimized Speed builds -> base models, gemma-4-12B-it-oQ4e -> gemma-4-12b-it). Models 541. oMLX total 17850 -> 17876.
- Dataset 22693 -> 22719. check_quotes green (23368 verified).

## 2026-10-12: oMLX batch 384 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan366, 60 fetched, 77 new ids in listing, 20 new candidates = mined + deduped). No new models (8 unique trace models all IN-MAP). Models 541. oMLX total 17822 -> 17850.
- Dataset 22665 -> 22693. check_quotes green (23342 verified).

## 2026-10-12: oMLX batch 383 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan365, 60 fetched, 66 new ids in listing, 20 new candidates = mined + deduped). No new models (10 unique trace models all map to existing; glm-5.3-flash-4bit-mlx lowercase -> GLM-5.3-Flash). Models 541. oMLX total 17797 -> 17822.
- Dataset 22640 -> 22665. check_quotes green (23314 verified).

## 2026-10-12: oMLX batch 382 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan364, 60 fetched, 42 new ids in listing, 20 new candidates = mined + deduped). No new models (9 unique trace models all map to existing; Uncensored MLX 6Bit -> Qwen3.8-27B-Uncensored). Models 541. oMLX total 17769 -> 17797.
- Dataset 22612 -> 22640. check_quotes green (23289 verified).

## 2026-10-12: oMLX batch 381 (+27 rows)

- oMLX corpus sweep: 27 records mined (scan363, 60 fetched, 55 new ids in listing, 20 new candidates = mined + deduped). No new models (6 unique trace models all IN-MAP). Models 541. oMLX total 17742 -> 17769.
- Dataset 22585 -> 22612. check_quotes green (23261 verified).

## 2026-10-12: oMLX batch 380 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan362, 60 fetched, 78 new ids in listing, 22 new candidates = mined + deduped). No new models (5 unique trace models all IN-MAP). Models 541. oMLX total 17717 -> 17742.
- Dataset 22560 -> 22585. check_quotes green (23234 verified).

## 2026-10-12: oMLX batch 379 (+29 rows)

- oMLX corpus sweep: 29 records mined (scan361, 60 fetched, 137 new ids in listing, 22 new candidates = mined + deduped). No new models (13 unique trace models all IN-MAP). Models 541. oMLX total 17688 -> 17717.
- Dataset 22531 -> 22560. check_quotes green (23209 verified).

## 2026-10-12: oMLX batch 378 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan360, 60 fetched, 128 new ids in listing, 22 new candidates = mined + deduped). No new models (9 unique trace models all map to existing; Flash-Next-Uncensored mixed-quant MoE 384e oQ4e + 128e oQ2 -> Qwen3.8-Flash-Next-Uncensored). Models 541. oMLX total 17660 -> 17688.
- Dataset 22503 -> 22531. check_quotes green (23180 verified).

## 2026-10-12: oMLX batch 377 (+29 rows)

- oMLX corpus sweep: 29 records mined (scan359, 60 fetched, 47 new ids in listing, 22 new candidates = mined + deduped). No new models (8 unique trace models all map to existing; Coder390 abbreviated build -> base Qwen3.8-27B-Coder390, Uncensored MLX 4Bit/8Bit -> Qwen3.8-27B-Uncensored). Models 541. oMLX total 17631 -> 17660.
- Source rewrite: vLLM PR #60070 (persistent FlashInfer MLA counter buffer) rewritten upstream. Hardware label 4x NVIDIA B200 -> 4x B200; primary table baseline/patched 126.095/132.066 -> 130.8/132.5 tok/s (+1.35%). Re-mined both records.
- Dataset 22474 -> 22503. check_quotes green (23152 verified). force_refresh.txt lists the rewritten URL for CI cache refresh.

## 2026-10-12: oMLX batch 376 (+26 rows)

- oMLX corpus sweep: 26 records mined (scan358, 60 fetched, 21 new ids in listing, 22 new candidates = mined + deduped). No new models (10 unique trace models all IN-MAP). Models 541. oMLX total 17605 -> 17631.
- Dataset 22448 -> 22474. check_quotes green (23123 verified).

## 2026-10-12: oMLX batch 375 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan357, 60 fetched, 24 new ids in listing, 22 new candidates = mined + deduped). No new models (9 unique trace models all map to existing; TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU oQ2e). Models 541. oMLX total 17580 -> 17605.
- Dataset 22423 -> 22448. check_quotes green (23097 verified).

## 2026-10-12: oMLX batch 374 (+37 rows)

- oMLX corpus sweep: 37 records mined (scan356, 60 fetched, 8 new ids in listing, 22 new candidates = mined + deduped). No new models (8 unique trace models all IN-MAP). Models 541. oMLX total 17543 -> 17580.
- Dataset 22386 -> 22423. check_quotes green (23072 verified).

## 2026-10-12: oMLX batch 373 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan355, 60 fetched, 67 new ids in listing, 22 new candidates = mined + deduped). No new models (8 unique trace models all map to existing; Swift-1.5-Qwen3.8-27B-MLX-oMLX -> existing Swift-1.5-Qwen3.8-27b). Models 541. oMLX total 17515 -> 17543.
- Dataset 22358 -> 22386. check_quotes green (23035 verified).

## 2026-10-12: oMLX batch 372 (+24 rows net)

- oMLX corpus sweep: 25 records mined (scan354, 60 fetched, 46 new ids in listing, 22 new candidates = mined + deduped). No new models (4 unique trace models all map to existing; DeepSeek-Coder-V2-Lite-Instruct oQ4e). Models 541. oMLX total 17490 -> 17515.
- Source rewrite: vLLM PR #60068 (confidence stop) description rewritten upstream. Old 5-arm table (stock / fixed 6 / stop) replaced by a 4-arm table (fixed 3 vs confidence stop, c=1 and c=4). Re-mined 5 stale records into 4 new (fixed3-c1 49.1, stop-c1 50.5, fixed3-c4 33.0, stop-c4 32.6 tok/s); net -1 record. ab_note rewritten to match.
- Dataset 22334 -> 22358. check_quotes green (23007 verified). force_refresh.txt lists the rewritten URL for CI cache refresh.

## 2026-10-12: oMLX batch 371 (+24 rows)

- oMLX corpus sweep: 24 records mined (scan353, 60 fetched, 44 new ids in listing, 22 new candidates = mined + deduped). 1 new model: DeepSeek-R1-Distill-Qwen-7B. Models 540 -> 541. oMLX total 17466 -> 17490.
- Dataset 22310 -> 22334. check_quotes green (22983 verified).

## 2026-10-12: oMLX batch 370 (+24 rows)

- oMLX corpus sweep: 24 records mined (scan352, 60 fetched, 79 new ids in listing, 22 new candidates = mined + deduped). No new models (5 unique trace models all map to existing; GLM-4.5-Air 4bit, GLM-5.3-Flash oQ3.5e MTP). Models 540. oMLX total 17442 -> 17466.
- Dataset 22286 -> 22310. check_quotes green (22959 verified).

## 2026-10-12: oMLX batch 369 (+27 rows)

- oMLX corpus sweep: 27 records mined (scan351, 60 fetched, 83 new ids in listing, 22 new candidates = mined + deduped). No new models (6 unique trace models all map to existing; csolares2 Qwen3.8-27B oQ8 MTP -> existing Qwen3.8-27B). Models 540. oMLX total 17415 -> 17442.
- Dataset 22259 -> 22286. check_quotes green (22935 verified).

## 2026-10-12: oMLX batch 368 (+31 rows)

- oMLX corpus sweep: 31 records mined (scan350, 60 fetched, 73 new ids in listing, 22 new candidates = mined + deduped). No new models (3 unique trace models all IN-MAP). Models 540. oMLX total 17384 -> 17415.
- Dataset 22228 -> 22259. check_quotes green (22908 verified).

## 2026-10-12: oMLX batch 367 (+27 rows)

- oMLX corpus sweep: 27 records mined (scan349, 60 fetched, 43 new ids in listing, 22 new candidates = mined + deduped). No new models (2 unique trace models all IN-MAP). Models 540. oMLX total 17357 -> 17384.
- Dataset 22201 -> 22228. check_quotes green (22877 verified).

## 2026-10-12: oMLX batch 366 (+30 rows)

- oMLX corpus sweep: 30 records mined (scan348, 60 fetched, 70 new ids in listing, 22 new candidates = mined + deduped). No new models (7 unique trace models all map to existing; AutomatosX AX-Tiel-Coder-35B-A3B MXFP4 MTP -> existing Tiel-Coder-35B-A3B). Models 540. oMLX total 17327 -> 17357.
- Dataset 22171 -> 22201. check_quotes green (22850 verified).

## 2026-10-12: oMLX batch 365 (+29 rows)

- oMLX corpus sweep: 29 records mined (scan347, 60 fetched, 58 new ids in listing, 22 new candidates = mined + deduped). 1 new model: FuseO1-DeepSeekR1-Qwen2.5-Coder-7B-Preview. Models 539 -> 540. oMLX total 17298 -> 17327.
- Dataset 22142 -> 22171. check_quotes green (22820 verified).

## 2026-10-12: oMLX batch 364 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan346, 60 fetched, 71 new ids in listing, 22 new candidates = mined + deduped). 1 new model: Qwen2.5-Coder-3B (generic; existing is Qwen2.5-Coder-3B-Instruct). Models 538 -> 539. oMLX total 17273 -> 17298.
- Dataset 22117 -> 22142. check_quotes green (22791 verified).

## 2026-10-12: oMLX batch 363 (+26 rows)

- oMLX corpus sweep: 26 records mined (scan345, 60 fetched, 62 new ids in listing, 22 new candidates = mined + deduped). No new models (6 unique trace models all IN-MAP). Models 538. oMLX total 17247 -> 17273.
- Dataset 22091 -> 22117. check_quotes green (22766 verified).

## 2026-10-12: oMLX batch 362 (+31 rows)

- oMLX corpus sweep: 31 records mined (scan344, 60 fetched, 39 new ids in listing, 22 new candidates = mined + deduped). 1 new model: Spark-X2.5-4B (generic; existing is Spark-X2.5-4B-Abliterated-Uncensored). Models 537 -> 538. oMLX total 17216 -> 17247.
- Dataset 22060 -> 22091. check_quotes green (22740 verified).

## 2026-10-12: oMLX batch 361 (+26 rows)

- oMLX corpus sweep: 26 records mined (scan343, 60 fetched, 79 new ids in listing, 22 new candidates = mined + deduped). No new models (10 unique trace models all map to existing; DeepSeek-V4.1-Flash UNCENSORED oQ4 MTP, Qwen3 4B MLX 8bit, Qwen3.8-Flash-Next oQ4e MTP build 20261011). Models 537. oMLX total 17190 -> 17216.
- Dataset 22034 -> 22060. check_quotes green (22709 verified).

## 2026-10-12: oMLX batch 360 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan342, 60 fetched, 32 new ids in listing, 22 new candidates = mined + deduped). No new models (6 unique trace models all IN-MAP). Models 537. oMLX total 17162 -> 17190.
- Dataset 22006 -> 22034. check_quotes green (22683 verified).

## 2026-10-12: oMLX batch 359 (+26 rows)

- oMLX corpus sweep: 26 records mined (scan341, 60 fetched, 27 new ids in listing, 22 new candidates = mined + deduped). No new models (9 unique trace models all map to existing; Qwen3.5-9B-Claude-4.6 HighIQ oQ4e). Models 537. oMLX total 17136 -> 17162.
- Dataset 21980 -> 22006 (crossed 22k records). check_quotes green (22655 verified).

## 2026-10-12: oMLX batch 358 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan340, 60 fetched, 42 new ids in listing, 22 new candidates = mined + deduped). 1 new model: Devstral-Small-2505 (distinct from existing Devstral-Small-2-24B-Instruct-2512). Models 536 -> 537. oMLX total 17108 -> 17136.
- Dataset 21952 -> 21980. check_quotes green (22629 verified).

## 2026-10-12: oMLX batch 357 (+27 rows)

- oMLX corpus sweep: 27 records mined (scan339, 60 fetched, 15 new ids in listing, 22 new candidates = mined + deduped). No new models (7 unique trace models all IN-MAP). Models 536. oMLX total 17081 -> 17108.
- Dataset 21925 -> 21952. check_quotes green (22601 verified).

## 2026-10-12: oMLX batch 356 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan338, 60 fetched, 19 new ids in listing, 22 new candidates = mined + deduped). No new models (7 unique trace models all IN-MAP). Models 536. oMLX total 17056 -> 17081.
- Dataset 21900 -> 21925. check_quotes green (22574 verified).

## 2026-10-12: oMLX batch 355 (+27 rows)

- oMLX corpus sweep: 27 records mined (scan337, 60 fetched, 9 new ids in listing, 22 new candidates = mined + deduped). 1 new model: gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-uncensored-heretic (distinct community build). Models 535 -> 536. oMLX total 17029 -> 17056.
- Dataset 21873 -> 21900. check_quotes green (22549 verified).

## 2026-10-12: oMLX batch 354 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan336, 60 fetched, 33 new ids in listing, 22 new candidates = mined + deduped). No new models (7 unique trace models all map to existing; AREX-Turbo 8bit). Models 535. oMLX total 17004 -> 17029.
- Dataset 21848 -> 21873. check_quotes green (22522 verified).

## 2026-10-12: oMLX batch 353 (+29 rows)

- oMLX corpus sweep: 29 records mined (scan335, 60 fetched, 26 new ids in listing, 22 new candidates = mined + deduped). No new models (9 unique trace models all map to existing; Qwen3.6-35B-A3B oQ2.5e MTP, Qwen3.8-27B-Coder390 NVFP4 W4A16). Models 535. oMLX total 16975 -> 17004.
- Dataset 21819 -> 21848. check_quotes green (22497 verified).

## 2026-10-12: oMLX batch 352 (+33 rows)

- oMLX corpus sweep: 33 records mined (scan334, 60 fetched, 38 new ids in listing, 27 new candidates = mined + deduped). No new models (7 unique trace models all IN-MAP). Models 535. oMLX total 16942 -> 16975.
- Dataset 21786 -> 21819. check_quotes green (22468 verified).

## 2026-10-12: oMLX batch 351 (+37 rows)

- oMLX corpus sweep: 37 records mined (scan333, 60 fetched, 57 new ids in listing, 30 new candidates = mined + deduped). No new models (9 unique trace models all map to existing; mlx-community Qwen3.8-27B 4bit). Models 535. oMLX total 16905 -> 16942.
- Dataset 21749 -> 21786. check_quotes green (22435 verified).

## 2026-10-12: oMLX batch 350 (+31 rows)

- oMLX corpus sweep: 31 records mined (scan332, 60 fetched, 54 new ids in listing, 30 new candidates = mined + deduped). 1 new model: AREX-Turbo (distinct from AREX-2, confirmed by page title). Models 534 -> 535. oMLX total 16874 -> 16905.
- Dataset 21718 -> 21749. check_quotes green (22398 verified).

## 2026-10-12: oMLX batch 349 (+39 rows)

- oMLX corpus sweep: 39 records mined (scan331, 60 fetched, 39 new ids in listing, 30 new candidates; 28 mined/deduped + 2 "BF16-oQ8e-mtp" minimal-title traces skipped). No new models (10 unique trace models all map to existing). Models 534. oMLX total 16835 -> 16874.
- Dataset 21679 -> 21718. check_quotes green (22367 verified).

## 2026-10-12: oMLX batch 348 (+45 rows)

- oMLX corpus sweep: 45 records mined (scan330, 60 fetched, 45 new ids in listing, 30 new candidates = mined + deduped). No new models (14 unique trace models all map to existing; Qwen3.8-27B-Abliterated 4bit MLX, Qwen3.8-Flash-Next oQ3e MTP). Models 534. oMLX total 16790 -> 16835.
- Dataset 21634 -> 21679. check_quotes green (22328 verified).

## 2026-10-12: oMLX batch 347 (+38 rows)

- oMLX corpus sweep: 38 records mined (scan329, 60 fetched, 39 new ids in listing, 30 new candidates = mined + deduped). No new models (11 unique trace models all map to existing; Llama-3.2-3B-Instruct 4bit, Genesis-Hermes-V13-dequantized oQ4e, gemma-4-26B-A4B-it-qat 6bit, mlx-community Qwen3.8-Flash-Next 4bit). Models 534. oMLX total 16752 -> 16790.
- Dataset 21596 -> 21634. check_quotes green (22283 verified).

## 2026-10-12: oMLX batch 346 (+37 rows)

- oMLX corpus sweep: 37 records mined (scan328, 60 fetched, 36 new ids in listing, 30 new candidates = mined + deduped). No new models (10 unique trace models all IN-MAP). Models 534. oMLX total 16715 -> 16752.
- Dataset 21559 -> 21596. check_quotes green (22245 verified).

## 2026-10-12: oMLX batch 345 (+34 rows)

- oMLX corpus sweep: 34 records mined (scan327, 60 fetched, 101 new ids in listing, 30 new candidates = mined + deduped). No new models (9 unique trace models all IN-MAP). Models 534. oMLX total 16681 -> 16715.
- Dataset 21525 -> 21559. check_quotes green (22208 verified).

## 2026-10-12: oMLX batch 344 (+31 rows)

- oMLX corpus sweep: 31 records mined (scan326, 60 fetched, 63 new ids in listing, 30 new candidates; 28 mined/deduped + 2 "4bit" minimal-title traces skipped). No new models (11 unique trace models all map to existing; Qwen3.5-9B-The-Defiant-Fable oQ4e variant, Qwen3.8-27B-Uncensored-OrcaRouter, Qwen3.8-Flash-Next mix6 variant). Models 534. oMLX total 16650 -> 16681.
- Dataset 21494 -> 21525. check_quotes green (22174 verified).

## 2026-10-12: oMLX batch 343 (+35 rows)

- oMLX corpus sweep: 35 records mined (scan325, 60 fetched, 43 new ids in listing, 30 new candidates = mined + deduped). No new models (12 unique trace models all map to existing; Qwen3.6-35B-35.98G-A3B-oQ8-mtp mapped to existing Qwen3.6-35B since the size string breaks the A3B substring; prism-ml--Bonsai-27B-mlx-1bit person build). Models 534. oMLX total 16615 -> 16650.
- Source rewrite: llama.cpp #29949 "Remote results (2x RTX 3090)" table updated (EN plain 50.4 -> 47.6, EN + MTP-Q8 61.1 -> 59.6); re-mined 2 records, added URL to force_refresh.txt.
- Dataset 21459 -> 21494. check_quotes green (22143 verified).

## 2026-10-12: oMLX batch 342 (+35 rows)

- oMLX corpus sweep: 35 records mined (scan324, 60 fetched, 61 new ids in listing, 30 new candidates = mined + deduped). 2 new models: qwen38-obliteratus, Youtu-Parsing-Omni. Also Qwen3.8-27B-heretic-ara-oQ4e-mtp (existing variant). Models 532 -> 534. oMLX total 16580 -> 16615.
- Dataset 21424 -> 21459. check_quotes green (22108 verified).

## 2026-10-12: oMLX batch 341 (+33 rows)

- oMLX corpus sweep: 33 records mined (scan323, 60 fetched, listing found 312 new ids but only 30 candidates fetched this run; 30 new candidates = mined + deduped). No new models: 15 unique trace models all map to existing canonicals. 3 new person-prefix MAP entries (IsValorum--Qwen3.8-35B-A3B-Distill, LiquidAI--LFM2.5-8B-A1B, mchen04--Ornith-1.5-35B-A3B-REAP192). Models 532. oMLX total 16547 -> 16580.
- Dataset 21391 -> 21424. check_quotes green (22073 verified).

## 2026-10-12: oMLX batch 340 (+64 rows)

- oMLX corpus sweep: 64 records mined (scan322, 60 fetched, 48 new candidates = 23 mined + 25 deduped; scan had transient DNS hiccups). No new models: 17 unique trace models all map to existing canonicals; only ThinkingCap-Qwen3.8-27B was NOT-IN-MAP (person/build prefix of existing Qwen3.8-27B). Models 532. oMLX total 16483 -> 16547.
- Dataset 21327 -> 21391. check_quotes green (22040 verified).

## 2026-10-11: oMLX batch 339 (+76 rows)

- oMLX corpus sweep: 76 records mined (scan321, 60 fetched, 31 unmined candidates, 29 404). 2 new models: Qwen3.6-35B-MoE, pplx-computer-qwen-3-6-35b-a3b. Also Ling-3.0-tiny-oQ8e-bf16, Qwen3.8-27B-heretic-ara-oQ4e-fp16-mtp (existing models). Models 530 -> 532. oMLX total 16407 -> 16483.
- Dataset 21251 -> 21327. check_quotes green (21976 verified).

## 2026-10-11: oMLX batch 338 (+59 rows)

- oMLX corpus sweep: 59 records mined (scan320, 60 fetched, 23 unmined candidates, 37 404). No new models. DeepSeek-V4-Flash-0731-oQ2e-mtp, LFM2.5-8B-A1B-gptq-jang, NVIDIA-Nemotron-3.5-Lightning-30B-A3B-MLX-4bit, Qwen3.6-14B-A3B-FableVibes-mlx-q4 (existing models). Models 530. oMLX total 16348 -> 16407.
- Dataset 21192 -> 21251. check_quotes green (21900 verified).

## 2026-10-11: oMLX batch 337 (+66 rows)

- oMLX corpus sweep: 66 records mined (scan319, 60 fetched, 34 unmined candidates, 26 404). 1 new model: Gemma-4-Dark-Gemistry-31B. Also Ternary-Bonsai-2-27B-MLX-oQ2-mtp, Qwen3.6-35B-A3B-OptiQ-4bit-REAP-19B, unsloth-gemma-4-26B, TensorFold--Qwen3.8-27B (existing models). Models 529 -> 530. oMLX total 16282 -> 16348.
- Dataset 21126 -> 21192. check_quotes green (21841 verified).

## 2026-10-11: oMLX batch 336 (+100 rows)

- oMLX corpus sweep: 100 records mined (scan318, 60 fetched, 39 unmined candidates, 21 404). 1 new model: Huihui-Qwen3-VL-4B-Instruct-abliterated. Also Qwen3.8-27B-Uncensored-oQ6e-mtp, Qwen3.8-27B-mxfp4, Qwen3.6-35B-A3B-mxfp4, gemma-4-26b-a4b-it-4bit (existing models). Models 528 -> 529. oMLX total 16182 -> 16282.
- Dataset 21026 -> 21126. check_quotes green (21775 verified).

## 2026-10-11: oMLX batch 335 (+94 rows)

- oMLX corpus sweep: 94 records mined (scan317, 60 fetched, 32 unmined candidates, 28 404). 2 new models: Agents-A1, Nemotron-3.5-Lightning-30B-A3B. Also Jundot--gemma-4-E4B, Qwen3.8-Flash-Next-MLX-oQ4e-mtp, gpt-oss-20b (existing models). Models 526 -> 528. oMLX total 16088 -> 16182.
- Dataset 20932 -> 21026. check_quotes green (21675 verified).

## 2026-10-11: oMLX batch 334 (+91 rows)

- oMLX corpus sweep: 91 records mined (scan316, 60 fetched, 31 unmined candidates, 29 404). No new models (Jundot--gemma-4-E2B variant, Qwen3-8B merged with existing Qwen3 8B, Qwen3.5-9B-4bit, MiMo-7B-RL; all canonicals existing). Models 526. oMLX total 15997 -> 16088 (**crossed 16k**).
- Dataset 20841 -> 20932. check_quotes green (21581 verified).

## 2026-10-11: oMLX batch 333 (+80 rows)

- oMLX corpus sweep: 80 records mined (scan315, 60 fetched, 28 unmined candidates, 32 404). 1 new model: RAZOR-19B-A3B. Also gemma-4-E2B-it-oQ8-fp16 (existing model). Models 525 -> 526. oMLX total 15917 -> 15997.
- Dataset 20761 -> 20841. check_quotes green (21490 verified).

## 2026-10-11: oMLX batch 332 (+88 rows)

- oMLX corpus sweep: 88 records mined (scan314, 60 fetched, 30 unmined candidates, 30 404). No new models (Qwen3-30B-A3B-4bit, DeepSeek-V4.1-Flash-oQ4e-mtp, gemma-4-26B-A4B-it-uncensored-heretic-mlx-vlm; all canonicals existing). Models 525. oMLX total 15829 -> 15917.
- Dataset 20673 -> 20761. check_quotes green (21410 verified).

## 2026-10-11: oMLX batch 331 (+97 rows)

- oMLX corpus sweep: 97 records mined (scan313, 60 fetched, 31 unmined candidates, 29 404). No new models (gemma-4-31B-it Mystery-Fine-Tune-HERETIC variant, Qwen3.8-Flash-Next-REAP-288, Qwen3.8-27B-8bit; all canonicals existing). Models 525. oMLX total 15732 -> 15829.
- Dataset 20576 -> 20673. check_quotes green (21322 verified).

## 2026-10-11: oMLX batch 330 (+79 rows)

- oMLX corpus sweep: 79 records mined (scan312, 60 fetched, 27 unmined candidates, 33 404). 1 new model: Ornith-1.5-397B. Also diffusiongemma-26B-A4B-it (existing model). Models 524 -> 525. oMLX total 15653 -> 15732.
- Dataset 20497 -> 20576. check_quotes green (21225 verified).

## 2026-10-11: oMLX batch 329 (+105 rows)

- oMLX corpus sweep: 105 records mined (scan311, 60 fetched, 36 unmined candidates, 24 404). No new models (OsaurusAI-Qwen3.6-35B-A3B-mxfp4, Qwen3.8-27B-8bit, Qwen3.6-35B-A3B-mxfp4; all canonicals existing). Models 524. oMLX total 15548 -> 15653.
- Dataset 20392 -> 20497. check_quotes green (21146 verified).

## 2026-10-11: oMLX batch 328 (+105 rows)

- oMLX corpus sweep: 105 records mined (scan310, 60 fetched, 31 unmined candidates, 29 404). No new models (NVIDIA-Nemotron-3.5-Lightning-30B-A3B MLX-4bit-mtp, Qwen3.8-27B-NVFP4, Qwen3.8-27B-oQ5e-SAGE-ARCS-mtp; all canonicals existing). Models 524. oMLX total 15443 -> 15548.
- Dataset 20287 -> 20392. check_quotes green (21041 verified).

## 2026-10-11: oMLX batch 327 (+116 rows)

- oMLX corpus sweep: 116 records mined (scan309, 60 fetched, 38 unmined candidates, 22 404). 1 new model: qwen3.5-4B-super-coder (M4 10c 16GB, 4bit). Also AREX-2 6bit, gemma-4-31B-it-uncensored oQ4e variants. Models 523 -> 524. oMLX total 15327 -> 15443.
- Dataset 20171 -> 20287. check_quotes green (20936 verified).

## 2026-10-11: oMLX batch 326 (+139 rows)

- oMLX corpus sweep: 139 records mined (scan308, 60 fetched, 37 unmined candidates, 23 404). No new models (GLM-5.3-Flash, Qwen3.8-27B-Huihui-Abliterated, Qwen3.8-27B-MLX-oQ4e-mtp; all canonicals existing). Models 523. oMLX total 15188 -> 15327.
- Dataset 20032 -> 20171. check_quotes green (20820 verified).

## 2026-10-11: oMLX batch 325 (+123 rows)

- oMLX corpus sweep: 123 records mined (scan307, 60 fetched, 32 unmined candidates, 28 404). No new models (DeepSeek-V4-Flash-2bit-DQ, Noctalin--Qwen3.6-35B-A3B; all canonicals existing). Models 523. oMLX total 15065 -> 15188. Dataset crossed 20k records.
- Dataset 19909 -> 20032. check_quotes green (20681 verified).

## 2026-10-11: oMLX batch 324 (+127 rows)

- oMLX corpus sweep: 127 records mined (scan306, 60 fetched, 28 unmined candidates, 32 404). 1 new model: Qwopus3.8-27B-Flash (M5 Pro 20c 48GB, oQ4e MTP). Models 522 -> 523. oMLX total 14938 -> 15065.
- Dataset 19782 -> 19909. check_quotes green (20558 verified).

## 2026-10-11: oMLX batch 323 (+108 rows)

- oMLX corpus sweep: 108 records mined (scan305, 60 fetched, 25 unmined candidates, 35 404). No new models (gemma-4-E4B-it, Qwen3.6-35B-A3B-Claude-4.7-Opus-Reasoning-Distilled; all canonicals existing). Models 522. oMLX total 14830 -> 14938.
- Dataset 19674 -> 19782. check_quotes green (20431 verified).

## 2026-10-11: oMLX batch 322 (+119 rows)

- oMLX corpus sweep: 119 records mined (scan304, 60 fetched, 29 unmined candidates, 31 404). No new models (Qwen3.8-Flash-Next-REAP-288, Nail-Qwen3.6-35B-A3B; all canonicals existing). Models 522. oMLX total 14711 -> 14830.
- Dataset 19555 -> 19674. check_quotes green (20323 verified).

## 2026-10-11: oMLX batch 321 (+116 rows)

- oMLX corpus sweep: 116 records mined (scan303, 60 fetched, 31 unmined candidates, 29 404). 1 new model: SuperQwen3.8-27b-abliterated (M5 Ultra 64c 96GB, 4bit MLX). Models 521 -> 522. oMLX total 14595 -> 14711.
- Dataset 19439 -> 19555. check_quotes green (20204 verified).

## 2026-10-11: oMLX batch 320 (+101 rows)

- oMLX corpus sweep: 101 records mined (scan302, 60 fetched, 24 unmined candidates, 36 404). No new models (Qwen3.6-35B-A3B-4bit-DWQ, Qwen3.8-27B-4bit-MTP-MLX, Ornith-1.5-35B-A3B-oQ4e-mtp; all canonicals existing). Models 521. oMLX total 14494 -> 14595.
- Dataset 19338 -> 19439. check_quotes green (20088 verified).

## 2026-10-11: oMLX batch 319 (+88 rows)

- oMLX corpus sweep: 88 records mined (scan301, 60 fetched, 25 unmined candidates, 35 404). No new models (Qwen3.8-27B-NVFP4-unsloth; all canonicals existing). Models 521. oMLX total 14406 -> 14494.
- Dataset 19250 -> 19338. check_quotes green (19987 verified).

## 2026-10-11: oMLX batch 318 (+77 rows)

- oMLX corpus sweep: 77 records mined (scan300, 60 fetched, 23 unmined candidates, 37 404). No new models (MiMo-7B-RL, Qwen3.6-27B, Swift-1.5-Qwen3.8-27b-oQ6e; all canonicals existing). Models 521. oMLX total 14329 -> 14406.
- Dataset 19173 -> 19250. check_quotes green (19899 verified).

## 2026-10-11: oMLX batch 317 (+86 rows)

- oMLX corpus sweep: 86 records mined (scan299, 60 fetched, 29 unmined candidates, 31 404). No new models (gemma-4-31B-it-qat 8bit/oQ8 variants; all canonicals existing). Models 521. oMLX total 14243 -> 14329.
- Dataset 19087 -> 19173. check_quotes green (19822 verified).

## 2026-10-11: oMLX batch 316 (+85 rows)

- oMLX corpus sweep: 85 records mined (scan298, 60 fetched, 34 unmined candidates, 26 404). No new models (Bonsai-27B, Ornith-1.5-35B-A3B, Qwen3.6-35B-A3B-UD, Swift-1.5; all canonicals existing). Models 521. oMLX total 14158 -> 14243.
- Dataset 19002 -> 19087. check_quotes green (19736 verified).

## 2026-10-11: oMLX batch 315 (+103 rows)

- oMLX corpus sweep: 103 records mined (scan297, 60 fetched, 35 unmined candidates, 25 404). No new models (Mellum2.1 bf16 variant, Steven10429 UD-IQ4_XS build; all canonicals existing). Models 521. oMLX total 14055 -> 14158.
- Dataset 18899 -> 19002 (crossed 19k records). check_quotes green (19651 verified).

## 2026-10-11: oMLX batch 314 (+95 rows)

- oMLX corpus sweep: 95 records mined (scan296, 60 fetched, 27 unmined candidates, 33 404). No new models (Nemotron-30B-A3B-8bit, gemma-4-26B-A4B-it-qat-8bit 8bit variants; all canonicals existing). Models 521. oMLX total 13960 -> 14055.
- Dataset 18804 -> 18899. check_quotes green (19548 verified).

## 2026-10-11: oMLX batch 313 (+88 rows)

- oMLX corpus sweep: 88 records mined (scan295, 60 fetched, 26 unmined candidates, 34 404). No new models (all 22 groups map to existing models; no new MAP entries). Models 521. oMLX total 13872 -> 13960.
- Dataset 18716 -> 18804. check_quotes green (19453 verified).

## 2026-10-11: oMLX batch 312 (+102 rows)

- oMLX corpus sweep: 102 records mined (scan294, 60 fetched, 39 unmined candidates, 21 404). No new models (Mellum2.1-12B-A2.5B-Thinking, Qwen3.6-35B-A3B, Qwen3.8-27B-Huihui-Abliterated, Qwen3-Coder-Next all existing). Models 521. oMLX total 13770 -> 13872.
- Dataset 18614 -> 18716. check_quotes green (19365 verified).

## 2026-10-11: oMLX batch 311 (+87 rows)

- oMLX corpus sweep: 87 records mined (scan293, 60 fetched, 33 unmined candidates, 20 404). No new models (Qwen3.8-27B-Uncensored, Qwen3.8-Flash-Next, Qwen3.8-27B person-prefixed builds all existing). Models 521. oMLX total 13683 -> 13770.
- Dataset 18527 -> 18614. check_quotes green (19263 verified).

## 2026-10-11: oMLX batch 310 (+98 rows)

- oMLX corpus sweep: 98 records mined (scan292, 60 fetched, 36 unmined candidates, 22 404). 1 new model (Qwen3.6-35B-A3B-Uncensored-Genesis-Hermes-V7-dequantized, M5 Max 128GB oQ8e MTP). Models 520 -> 521. oMLX total 13585 -> 13683.
- Dataset 18429 -> 18527. check_quotes green (19176 verified).

## 2026-10-11: oMLX batch 309 (+120 rows)

- oMLX corpus sweep: 120 records mined (scan291, 60 fetched, 49 unmined candidates, 18 404). 1 new model (ALoDLM-8B, M5 Pro 20c 64GB). Models 519 -> 520. oMLX total 13465 -> 13585.
- Dataset 18309 -> 18429. check_quotes green (19078 verified).

## 2026-10-11: oMLX batch 308 (+131 rows)

- oMLX corpus sweep: 131 records mined (scan290, 60 fetched, 47 unmined candidates, 18 404). No new models (Qwen3.5-0.8B-OptiQ-4bit -> Qwen3.5-0.8B; gemma-4-26B-A4B-it, gemma-4-E4B-it, gpt-oss 120B all existing). oMLX total 13334 -> 13465.
- Dataset 18178 -> 18309. Models 519. check_quotes green (18958 verified).

## 2026-10-11: oMLX batch 307 (+125 rows)

- oMLX corpus sweep: 125 records mined (scan289, 60 fetched, 45 unmined candidates, 18 404). No new models (Nemotron-Cascade-2-30B-A3B, Qwen3.5-4B, Qwen3.8-Flash-Next-REAP-288 all map to existing canonicals; NEO-CODER oQ8e-1M variant added). oMLX total 13209 -> 13334.
- Dataset 18053 -> 18178. Models 519. check_quotes green (18827 verified).

## 2026-10-11: oMLX batch 306 (+109 rows)

- oMLX corpus sweep: 109 records mined (scan288, 60 fetched, 37 unmined candidates, 18 404). 1 new model (Qwen3.5-9B-Distilled-OPUS-Heretic-MLX-VLM, 4bit, M6 12c 24GB). Models 518 -> 519. oMLX total 13100 -> 13209.
- Dataset 17944 -> 18053. check_quotes green (18702 verified).

## 2026-10-11: oMLX batch 305 (+94 rows)

- oMLX corpus sweep: 94 records mined (scan287, 60 fetched, 35 unmined candidates, 18 404). No new models (Llama-3.1-8B-Instruct maps to existing llama-3-1-8b-instruct; Ling-3.0-flash, GLM-5.3-Flash-UNCENSORED, Qwen3.8-27B-MTPLX all map to existing canonicals). oMLX total 13006 -> 13100.
- Dataset 17850 -> 17944. Models 518. check_quotes green (18593 verified).

## 2026-10-11: oMLX batch 304 (+80 rows)

- oMLX corpus sweep: 80 records mined (scan286, 60 fetched, 36 unmined candidates, 18 404). No new models (all trace variants map to existing canonicals; Occamy-1.0 oQ8e-fp16-MTP on M2 Max 96 GB). oMLX total 12926 -> 13006.
- Dataset 17770 -> 17850. Models 518. check_quotes green (18499 verified).

## 2026-10-11: oMLX batch 303 (+45 rows)

- oMLX corpus sweep: 45 records mined (scan285, 60 traces fetched, 20 unmined candidates, 18 404). New model: MiniMax-M2.7 (3bit, M5 Max 128 GB). oMLX total 12881 -> 12926.
- Dataset 17725 -> 17770. Models 517 -> 518. check_quotes green (18419 verified).

## 2026-10-11: oMLX batch 302 (+47 rows)

- oMLX corpus sweep: 47 records mined from 42 new traces (scan284). No new models; all 10 trace variants map to existing canonicals (Cyber-Tiel/Tiel-Coder-35B-A3B, Qwen3.6-27B/35B-A3B, DeepSeek-V4-Flash-0731 OptiQ-2bit, Qwen3.8-27B-TURBO ...-NM-DAU oQ8e-MTP, Qwen3.8-27B oQ4e-MTP, Qwen3.8-Flash-Next oQ4e-MTP, Swift-1.5-Qwen3.8-27b oQ8e-bf16-MTP, Jundot Qwen3.8-Flash-Next). oMLX total 12834 -> 12881.
- Dataset 17678 -> 17725. Models 517. check_quotes green (18374 verified).

## 2026-10-11: oMLX batch 301 (+13 rows) + source-change re-mine (28 records, -8 rows)

- oMLX corpus sweep: 13 records mined (scan283). No new models. oMLX total 12821 -> 12834.
- Source-change re-mine: 28 records re-mined across 4 drifted source pages (lc-29768 RTX 5090 Qwen3.8-27B, lc-29882 RTX 4060 Ti Q6_K, lc-29887 RTX 4090 pp_tps removed, vllm-59894 B200 DSV4.1-Flash). Model qwen35 removed (518 -> 517). Net -8 rows.
- Dataset 17673 -> 17686 -> 17678. Models 517. check_quotes green (18327 verified).

## 2026-10-11: oMLX batch 300 (+23 rows)

- oMLX corpus sweep: 23 records mined (scan282, 39 traces fetched, 23 unmined candidates). No new models. oMLX total 12798 -> 12821.
- Dataset 17650 -> 17673.

## 2026-10-11: oMLX batch 299 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan281, 41 traces fetched, 25 unmined candidates). New models: Qwen2.5-Coder-3B-Instruct (4bit), gemma-4-E4B-it-OBLITERATED (8bit). oMLX total 12773 -> 12798.
- Dataset 17625 -> 17650. Models 518.

## 2026-10-10: oMLX batch 298 (+20 rows)

- oMLX corpus sweep: 20 records mined (scan280, 36 traces fetched, 20 unmined candidates). New models: GLM-4.6V-Flash (8bit), KAT-Dev (8bit), Llama-3.2-11B-Vision-Instruct (8bit). oMLX total 12753 -> 12773.
- Dataset 17605 -> 17625. Models 516.

## 2026-10-10: oMLX batch 297 (+37 rows)

- oMLX corpus sweep: 37 records mined (scan279, 53 traces fetched, 37 unmined candidates). New model: North-Mini-Code-1.0 (6bit). oMLX total 12716 -> 12753.
- Dataset 17568 -> 17605. Models 513.

## 2026-10-10: oMLX batch 296 (+23 rows)

- oMLX corpus sweep: 23 records mined (scan278, 39 traces fetched, 23 unmined candidates). No new models. oMLX total 12693 -> 12716.
- Dataset 17545 -> 17568.

## 2026-10-10: oMLX batch 295 (+9 rows)

- oMLX corpus sweep: 9 records mined (scan277, 25 traces fetched, 9 unmined candidates). No new models. oMLX total 12684 -> 12693.
- Dataset 17536 -> 17545.

## 2026-10-10: oMLX batch 294 (+9 rows)

- oMLX corpus sweep: 9 records mined (scan276, 25 traces fetched, 9 unmined candidates). No new models. oMLX total 12675 -> 12684.
- Dataset 17527 -> 17536.

## 2026-10-10: oMLX batch 293 (+24 rows)

- oMLX corpus sweep: 24 records mined (scan275, 40 traces fetched, 24 unmined candidates). New model: 4-bit (literal user label, 4bit). oMLX total 12651 -> 12675.
- Dataset 17503 -> 17527. Models 512.

## 2026-10-10: oMLX batch 292 (+11 rows)

- oMLX corpus sweep: 11 records mined (scan274, 27 traces fetched, 11 unmined candidates). No new models. oMLX total 12640 -> 12651.
- Dataset 17492 -> 17503.

## 2026-10-10: oMLX batch 291 (+27 rows)

- oMLX corpus sweep: 27 records mined (scan273, 43 traces fetched, 27 unmined candidates). New model: Qwen2.5-Coder-32B-Instruct (bf16). oMLX total 12613 -> 12640.
- Dataset 17465 -> 17492. Models 511.

## 2026-10-10: oMLX batch 290 (+45 rows)

- oMLX corpus sweep: 45 records mined (scan272, 57 traces fetched, 41 unmined candidates). New models: gemma-4-12B-uncensored (oQ8e), Gemma 4 26B-A4B-it-uncensored (oQ8e MTP, consolidated to existing space form). oMLX total 12568 -> 12613.
- Dataset 17420 -> 17465. Models 510.

## 2026-10-10: oMLX batch 289 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan271, 60 traces fetched, 44 unmined candidates). New models: LFM2.5-8B-A1B-Abliterated (PocketAiHub), Swift-1.5-3bit (TextOnly). oMLX total 12517 -> 12568.
- Dataset 17369 -> 17420. Models 509.

## 2026-10-10: oMLX batch 288 (+45 rows)

- oMLX corpus sweep: 45 records mined (scan270, 60 traces fetched, 44 unmined candidates). New model: gemma-4-E4B-it-qat (8bit). oMLX total 12472 -> 12517.
- Dataset 17324 -> 17369. Models 507.

## 2026-10-10: oMLX batch 287 (+12 rows)

- oMLX corpus sweep: 12 records mined (scan269, 26 traces fetched, 12 unmined candidates). No new models. oMLX total 12460 -> 12472.
- Dataset 17312 -> 17324.

## 2026-10-10: oMLX batch 286 (+22 rows)

- oMLX corpus sweep: 22 records mined (scan268, 36 traces fetched, 22 unmined candidates). No new models. oMLX total 12438 -> 12460.
- Dataset 17290 -> 17312.

## 2026-10-10: oMLX batch 285 (+22 rows)

- oMLX corpus sweep: 22 records mined (scan267, 36 traces fetched, 22 unmined candidates). New models: gemma-4-26B-A4B-it-heretic-msq (2.6bit), gemma-4-E4B-it. oMLX total 12416 -> 12438.
- Dataset 17268 -> 17290. Models 506.

## 2026-10-10: oMLX batch 284 (+34 rows)

- oMLX corpus sweep: 34 records mined (scan266, 48 traces fetched, 34 unmined candidates). New models: Huihui-gemma-4-E4B-it-abliterated (4bit), MiMo-7B-RL (4bit), gemma-4-26B-A4B-it-ultra-uncensored-heretic (4bit culturerevolt). oMLX total 12382 -> 12416.
- Dataset 17234 -> 17268. Models 504.

## 2026-10-10: oMLX batch 283 (+33 rows)

- oMLX corpus sweep: 33 records mined (scan265, 47 traces fetched, 33 unmined candidates). New model: Qwen3.6-35B-A3B-OptiQ (5bpw, dawncr0w). oMLX total 12349 -> 12382.
- Dataset 17201 -> 17234. Models 501.

## 2026-10-10: oMLX batch 282 (+21 rows)

- oMLX corpus sweep: 21 records mined (scan264, 35 traces fetched, 21 unmined candidates). New model: Huihui-Ornith-1.5-9B-abliterated (5Bit). Model count crossed 500. oMLX total 12328 -> 12349.
- Dataset 17180 -> 17201. Models 500.

## 2026-10-10: oMLX batch 281 (+30 rows)

- oMLX corpus sweep: 30 records mined (scan263, 44 traces fetched, 30 unmined candidates). No new models (gemma-4-12B-it-qat OptiQ MTP consolidated). oMLX total 12298 -> 12328.
- Dataset 17150 -> 17180.

## 2026-10-10: oMLX batch 280 (+36 rows)

- oMLX corpus sweep: 36 records mined (scan262, 50 traces fetched, 36 unmined candidates). No new models. oMLX total 12262 -> 12298.
- Dataset 17114 -> 17150.

## 2026-10-10: oMLX batch 279 (+43 rows)

- oMLX corpus sweep: 43 records mined (scan261, 57 traces fetched, 43 unmined candidates). New models: gemma-4-26b-a4b-it-UD (4bit), gemma-4-E2B-it (oQ4e MTP). oMLX total 12219 -> 12262.
- Dataset 17071 -> 17114. Models 499.

## 2026-10-10: oMLX batch 278 (+41 rows)

- oMLX corpus sweep: 41 records mined (scan260, 55 traces fetched, 41 unmined candidates). New model: KAT-Coder-V2.5-Dev-VL (oQ4e MTP). oMLX total 12178 -> 12219.
- Dataset 17030 -> 17071. Models 497.

## 2026-10-10: oMLX batch 277 (+22 rows)

- oMLX corpus sweep: 22 records mined (scan259, 36 traces fetched, 22 unmined candidates). No new models (Qwen:Qwen3.8-27B oQ8e fp16 MTP consolidated). oMLX total 12156 -> 12178.
- Dataset 17008 -> 17030.

## 2026-10-10: oMLX batch 276 (+35 rows)

- oMLX corpus sweep: 35 records mined (scan258, 48 traces fetched, 34 unmined candidates). New model: Qwen3.5-4B-Uncensored (4bit). oMLX total 12121 -> 12156.
- Dataset 16973 -> 17008 (crossed 17k). Models 496.

## 2026-10-10: oMLX batch 275 (+53 rows)

- oMLX corpus sweep: 53 records mined (scan257, 60 traces fetched, 46 unmined candidates). No new models. oMLX total 12068 -> 12121.
- Dataset 16920 -> 16973.

## 2026-10-10: oMLX batch 274 (+53 rows)

- oMLX corpus sweep: 53 records mined (scan256, 60 traces fetched, 46 unmined candidates). New model: gpt-oss-120b-Sonnet-Reasoning-Distilled. oMLX total 12015 -> 12068.
- Dataset 16867 -> 16920. Models 495.

## 2026-10-10: oMLX batch 273 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan255, 60 traces fetched, 46 unmined candidates). New model: Huihui-Qwen3.6-35B-A3B-abliterated (oQ4e fp16 MTP). oMLX total 11964 -> 12015.
- Dataset 16816 -> 16867. Models 494.

## 2026-10-10: oMLX batch 272 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan254, 60 traces fetched, 46 unmined candidates). New models: Sharp-MiniCPM5-2B (oQ6e), gemma-4-26B-A4B-it-qat (4bit mlx-community OptiQ). oMLX total 11913 -> 11964.
- Dataset 16765 -> 16816. Models 493.

## 2026-10-10: oMLX batch 271 (+53 rows)

- oMLX corpus sweep: 53 records mined (scan253, 60 traces fetched, 46 unmined candidates). New model: Qwen3.6-35B-A3B-uncensored-heretic-Native-MTP-Preserved (oQ4e MTP). oMLX total 11860 -> 11913.
- Dataset 16712 -> 16765. Models 491.

## 2026-10-10: oMLX batch 270 (+54 rows)

- oMLX corpus sweep: 54 records mined (scan252, 60 traces fetched, 46 unmined candidates). New models: Jev-Style-Qwen3.5-2B-Decision-v2 (bf16), NeoHorse-Jev-4B-TmuxPocket (oQ4), gemma-4-31B-it-qat (4bit mlx-community OptiQ). oMLX total 11806 -> 11860.
- Dataset 16658 -> 16712. Models 490.

## 2026-10-10: oMLX batch 269 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan251, 60 traces fetched, 46 unmined candidates). New models: Bio-Medical-Llama-3-8B, II-Medical-8B-1706 (8bit). oMLX total 11755 -> 11806.
- Dataset 16607 -> 16658. Models 487.

## 2026-10-10: oMLX batch 268 (+55 rows)

- oMLX corpus sweep: 55 records mined (scan250, 60 traces fetched, 46 unmined candidates). No new models (bottlecapai ThinkingCap Qwen3.8-27B 4bit DWQ consolidated). oMLX total 11700 -> 11755.
- Dataset 16552 -> 16607.

## 2026-10-10: oMLX batch 267 (+50 rows)

- oMLX corpus sweep: 50 records mined (scan249, 60 traces fetched, 46 unmined candidates). New model: Qwen3.8-27B-Coder390 (oQ4e fp16 MTP). oMLX total 11650 -> 11700.
- Dataset 16502 -> 16552. Models 485.

## 2026-10-10: oMLX batch 266 (+31 rows)

- oMLX corpus sweep: 31 records mined (scan248, 45 traces fetched, 31 unmined candidates). No new models. oMLX total 11619 -> 11650.
- Dataset 16471 -> 16502.

## 2026-10-10: oMLX batch 265 (+38 rows)

- oMLX corpus sweep: 38 records mined (scan247, 52 traces fetched, 38 unmined candidates). New model: Swift-Qwen3.8-27B-Uncensored (oQ8e MTP). oMLX total 11581 -> 11619.
- Dataset 16433 -> 16471. Models 484.

## 2026-10-10: oMLX batch 264 (+14 rows)

- oMLX corpus sweep: 14 records mined (scan246, 28 traces fetched, 14 unmined candidates). No new models. oMLX total 11567 -> 11581.
- Dataset 16419 -> 16433.

## 2026-10-10: oMLX batch 263 (+44 rows)

- oMLX corpus sweep: 44 records mined (scan245, 58 traces fetched, 44 unmined candidates). No new models (GLM-4.7-Flash 8bit consolidated). oMLX total 11523 -> 11567.
- Dataset 16375 -> 16419.

## 2026-10-10: oMLX batch 262 (+16 rows)

- oMLX corpus sweep: 16 records mined (scan244, 30 traces fetched, 16 unmined candidates). No new models (Swift 1.5 Qwen3.8-Flash-Next oQ6e MTP consolidated). oMLX total 11507 -> 11523.
- Dataset 16359 -> 16375.

## 2026-10-10: oMLX batch 261 (+21 rows)

- oMLX corpus sweep: 21 records mined (scan243, 35 traces fetched, 21 unmined candidates). New model: Qwen3.6-35B-A3B-Uncensored-Genesis-Hermes-V10-dequantized (oQ8e MTP). oMLX total 11486 -> 11507.
- Dataset 16338 -> 16359. Models 483.

## 2026-10-10: oMLX batch 260 (+38 rows)

- oMLX corpus sweep: 38 records mined (scan242, 52 traces fetched, 38 unmined candidates). No new models (scottlowry ThinkingCap Qwen3.8-27B oQ4e MTP consolidated). oMLX total 11448 -> 11486.
- Dataset 16300 -> 16338.

## 2026-10-10: oMLX batch 259 (+20 rows)

- oMLX corpus sweep: 20 records mined (scan241, 34 traces fetched, 20 unmined candidates). No new models (Bonsai 2 27B consolidated). oMLX total 11428 -> 11448.
- Dataset 16280 -> 16300.

## 2026-10-10: oMLX batch 258 (+40 rows)

- oMLX corpus sweep: 40 records mined (scan240, 51 traces fetched, 37 unmined candidates). New model: Ornith-1.5-35B-A3B-REAP192 (mxfp4). oMLX total 11388 -> 11428.
- Dataset 16240 -> 16280. Models 482.

## 2026-10-10: oMLX batch 257 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan239, 60 traces fetched, 46 unmined candidates). New model: Gemma4-26B-MoE (4bit). oMLX total 11337 -> 11388.
- Dataset 16189 -> 16240. Models 481.

## 2026-10-10: oMLX batch 256 (+55 rows)

- oMLX corpus sweep: 55 records mined (scan238, 60 traces fetched, 46 unmined candidates). New model: Qwen3.5-9B-DeepSeek-V4-Flash (oQ4 MTP). oMLX total 11282 -> 11337.
- Dataset 16134 -> 16189. Models 480.

## 2026-10-10: oMLX batch 255 (+52 rows)

- oMLX corpus sweep: 52 records mined (scan237, 60 traces fetched, 46 unmined candidates). No new models. oMLX total 11230 -> 11282.
- Dataset 16082 -> 16134.

## 2026-10-10: oMLX batch 254 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan236, 60 traces fetched, 46 unmined candidates). No new models (Ornith-1.5-9B oQ8e fp16 consolidated). oMLX total 11179 -> 11230.
- Dataset 16031 -> 16082.

## 2026-10-10: oMLX batch 253 (+57 rows)

- oMLX corpus sweep: 57 records mined (scan235, 60 traces fetched, 46 unmined candidates). New models: Qwen3-VL-4B-Instruct (4bit), Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2 (oQ8e MTP). oMLX total 11122 -> 11179.
- Dataset 15974 -> 16031. Models 479.

## 2026-10-10: oMLX batch 252 (+56 rows)

- oMLX corpus sweep: 56 records mined (scan234, 60 traces fetched, 46 unmined candidates). No new models (Qwen3.8-27B-Alis 4bit consolidated). oMLX total 11066 -> 11122.
- Dataset 15918 -> 15974.

## 2026-10-10: oMLX batch 251 (+53 rows)

- oMLX corpus sweep: 53 records mined (scan233, 60 traces fetched, 46 unmined candidates). No new models (Ornith-1.5-35B-A3B-Abliterated oQ8e fp16 ccal, Gemma 4 E2B oQ6e fp16 consolidated). oMLX total 11013 -> 11066.
- Dataset 15865 -> 15918.

## 2026-10-10: oMLX batch 250 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan232, 60 traces fetched, 46 unmined candidates). New model: gemma-4-31B-it-qat-q4_0-unquantized (oQ4e fp16 MTP). oMLX total 10962 -> 11013.
- Dataset 15814 -> 15865. Models 477.

## 2026-10-10: oMLX batch 249 (+24 rows)

- oMLX corpus sweep: 24 records mined (scan231, 38 traces fetched, 24 unmined candidates). No new models. oMLX total 10938 -> 10962.
- Dataset 15790 -> 15814.

## 2026-10-10: oMLX batch 248 (+19 rows)

- oMLX corpus sweep: 19 records mined (scan230, 33 traces fetched, 19 unmined candidates). No new models (Qwen3.8-27B oQ3 fp16 MTP consolidated). oMLX total 10919 -> 10938.
- Dataset 15771 -> 15790.

## 2026-10-10: oMLX batch 247 (+30 rows)

- oMLX corpus sweep: 30 records mined (scan229, 37 traces fetched, 23 unmined candidates). No new models (Qwen3.8-27B-Abliterated q3km 3bit, Qwen3.8-Flash-Next-Uncensored oQ6e fp16 MTP consolidated). oMLX total 10889 -> 10919.
- Dataset 15741 -> 15771.

## 2026-10-10: oMLX batch 246 (+52 rows)

- oMLX corpus sweep: 52 records mined (scan228, 60 traces fetched, 46 unmined candidates). No new models (SamQuant C58 build consolidated into Qwen3.8-Flash-Next-Uncensored 4bit; also fixed a slug collision where the underscore variant was merged into the hyphen variant). oMLX total 10837 -> 10889.
- Dataset 15689 -> 15741.

## 2026-10-10: oMLX batch 245 (+39 rows)

- oMLX corpus sweep: 39 records mined (scan227, 53 traces fetched, 39 unmined candidates). New model: gemma-3-12b-it. oMLX total 10798 -> 10837.
- Dataset 15650 -> 15689. Models 476.

## 2026-10-10: oMLX batch 244 (+14 rows)

- oMLX corpus sweep: 14 records mined (scan226, 28 traces fetched, 14 unmined candidates). New models: CoPaw-Flash-9B (oQ4), Qwen3.6-35B-A3B-MXFP8-CRACK (MXFP8 MTP). oMLX total 10784 -> 10798.
- Dataset 15636 -> 15650. Models 475.

## 2026-10-10: oMLX batch 243 (+21 rows)

- oMLX corpus sweep: 21 records mined (scan225, 35 traces fetched, 21 unmined candidates). No new models. oMLX total 10763 -> 10784.
- Dataset 15615 -> 15636.

## 2026-10-10: oMLX batch 242 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan224, 39 traces fetched, 25 unmined candidates). No new models. oMLX total 10735 -> 10763.
- Dataset 15587 -> 15615.

## 2026-10-10: oMLX batch 241 (+47 rows)

- oMLX corpus sweep: 47 records mined (scan223, 60 traces fetched, 46 unmined candidates). New model: medgemma-27b-text-it (8bit). oMLX total 10688 -> 10735.
- Dataset 15540 -> 15587. Models 473.

## 2026-10-10: oMLX batch 240 (+36 rows)

- oMLX corpus sweep: 36 records mined (scan222, 50 traces fetched, 36 unmined candidates). No new models. oMLX total 10652 -> 10688.
- Dataset 15504 -> 15540.

## 2026-10-10: oMLX batch 239 (+7 rows)

- oMLX corpus sweep: 7 records mined (scan221, 21 traces fetched, 7 unmined candidates). No new models. oMLX total 10645 -> 10652.
- Dataset 15497 -> 15504.

## 2026-10-10: oMLX batch 238 (+14 rows)

- oMLX corpus sweep: 14 records mined (scan220, 28 traces fetched, 14 unmined candidates). No new models (Qwen3.8-27B-Uncensored 4bit consolidated). oMLX total 10631 -> 10645.
- Dataset 15483 -> 15497.

## 2026-10-10: oMLX batch 237 (+23 rows)

- oMLX corpus sweep: 23 records mined (scan219, 37 traces fetched, 23 unmined candidates). New model: Huihui-Qwen3.5-9B (8bit text). oMLX total 10608 -> 10631.
- Dataset 15460 -> 15483. Models 472.

## 2026-10-10: oMLX batch 236 (+18 rows)

- oMLX corpus sweep: 18 records mined (scan218, 32 traces fetched, 18 unmined candidates). No new models (Qwen3.8-35B-A3B-Distill oQ8 fp16 MTP consolidated). oMLX total 10590 -> 10608.
- Dataset 15442 -> 15460.

## 2026-10-10: oMLX batch 235 (+36 rows)

- oMLX corpus sweep: 36 records mined (scan217, 50 traces fetched, 36 unmined candidates). No new models (Ornith-1.5-35B-A3B oQ6e MTP consolidated). oMLX total 10554 -> 10590.
- Dataset 15406 -> 15442.

## 2026-10-10: oMLX batch 234 (+21 rows)

- oMLX corpus sweep: 21 records mined (scan216, 35 traces fetched, 21 unmined candidates). New model: Ministral-3-8B-Instruct-2512. Consolidated K2-Horizon-MoVA-36B-A4B 4bit, KAT-Coder-V2.5-Dev oQ2e. oMLX total 10533 -> 10554.
- Dataset 15385 -> 15406. Models 471.

## 2026-10-10: oMLX batch 233 (+13 rows)

- oMLX corpus sweep: 13 records mined (scan215, 27 traces fetched, 13 unmined candidates). New models: Kimi-Linear-48B-A3B-Instruct (4bit), Qwen3.8-35B-36.82G-A3B-Distill (oQ8 fp16 MTP). oMLX total 10520 -> 10533.
- Dataset 15372 -> 15385. Models 470.

## 2026-10-10: oMLX batch 232 (+17 rows)

- oMLX corpus sweep: 17 records mined (scan214, 31 traces fetched, 17 unmined candidates). No new models (Vontra Qwen3.8-27B 4bit consolidated). oMLX total 10503 -> 10520.
- Dataset 15355 -> 15372.

## 2026-10-10: oMLX batch 231 (+15 rows)

- oMLX corpus sweep: 15 records mined (scan213, 29 traces fetched, 15 unmined candidates). No new models. oMLX total 10488 -> 10503.
- Dataset 15340 -> 15355.

## 2026-10-10: oMLX batch 230 (+39 rows)

- oMLX corpus sweep: 39 records mined (scan212, 48 traces fetched, 34 unmined candidates). No new models. oMLX total 10449 -> 10488.
- Dataset 15301 -> 15340.

## 2026-10-10: oMLX batch 229 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan211, 60 traces fetched, 45 unmined candidates). No new models (Qwen3.8-27B EigenLabs 4bit MTP, MiniCPM5-2B mlx-community 4bit consolidated). oMLX total 10398 -> 10449.
- Dataset 15250 -> 15301.

## 2026-10-10: oMLX batch 228 (+41 rows)

- oMLX corpus sweep: 41 records mined (scan210, 55 traces fetched, 41 unmined candidates). No new models (DeepSeek-R1-0528-Qwen3-8B 4bit, DeepSeek-V4-Flash-0731 oQ2e MTP, Qwen3.6-40B Deckard-Heretic 4bit consolidated). oMLX total 10357 -> 10398.
- Dataset 15209 -> 15250.

## 2026-10-10: oMLX batch 227 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan209, 39 traces fetched, 25 unmined candidates). No new models. oMLX total 10332 -> 10357.
- Dataset 15184 -> 15209.

## 2026-10-10: oMLX batch 226 (+18 rows)

- oMLX corpus sweep: 18 records mined (scan208, 32 traces fetched, 18 unmined candidates). No new models (MiniCPM5-2B 8bit, Qwen3.8-27B oQ4e MTP baseline consolidated). oMLX total 10314 -> 10332.
- Dataset 15166 -> 15184.

## 2026-10-10: oMLX batch 225 (+36 rows)

- oMLX corpus sweep: 36 records mined (scan207, 50 traces fetched, 36 unmined candidates). New models: Llama-3.3-70B-Instruct-abliterated (4bit), gemma-4-31B-it-heretic (oQ4). oMLX total 10278 -> 10314.
- Dataset 15130 -> 15166. Models 468.

## 2026-10-10: oMLX batch 224 (+40 rows)

- oMLX corpus sweep: 40 records mined (scan206, 54 traces fetched, 40 unmined candidates). New models: Apodex-1.1-mini (oQ4e, baseline + MTP variants), gemma-4-26B-A4B-it-uncensored-heretic (6Bit VLM). oMLX total 10238 -> 10278.
- Dataset 15090 -> 15130. Models 466.

## 2026-10-10: oMLX batch 223 (+10 rows)

- oMLX corpus sweep: 10 records mined (scan205, 24 traces fetched, 10 unmined candidates). New model: Qwen3.8-27B-Uncensored-OrcaRouter (8bit). Consolidated Huihui-Qwen3.8-27B-abliterated 4bit, Qwen3.6-35B-A3B-Uncensored-Heretic 8bit. oMLX total 10228 -> 10238.
- Dataset 15080 -> 15090. Models 464.

## 2026-10-10: oMLX batch 222 (+17 rows)

- oMLX corpus sweep: 17 records mined (scan204, 31 traces fetched, 17 unmined candidates). No new models. oMLX total 10211 -> 10228.
- Dataset 15063 -> 15080.

## 2026-10-10: oMLX batch 221 (+12 rows)

- oMLX corpus sweep: 12 records mined (scan203, 26 traces fetched, 12 unmined candidates). New model: VulnLLM-R-7B (8bit). Consolidated Qwen3.5-4B MTPLX Optimized Speed. oMLX total 10199 -> 10211.
- Dataset 15051 -> 15063. Models 463.

## 2026-10-10: oMLX batch 220 (+32 rows)

- oMLX corpus sweep: 32 records mined (scan202, 46 traces fetched, 32 unmined candidates). No new models (Qwen3.8-Flash-Next oQ3.5e MTP consolidated). oMLX total 10167 -> 10199.
- Dataset 15019 -> 15051.

## 2026-10-10: oMLX batch 219 (+17 rows)

- oMLX corpus sweep: 17 records mined (scan201, 31 traces fetched, 17 unmined candidates). No new models (GLM-5.3-Flash oQ6e MTP consolidated). oMLX total 10150 -> 10167.
- Dataset 15002 -> 15019.

## 2026-10-10: oMLX batch 218 (+15 rows)

- oMLX corpus sweep: 15 records mined (scan200, 29 traces fetched, 15 unmined candidates). No new models (Gemma 4 E2B it 8bit consolidated). oMLX total 10135 -> 10150.
- Dataset 14987 -> 15002 (15k crossed).

## 2026-10-10: oMLX batch 217 (+13 rows)

- oMLX corpus sweep: 13 records mined (scan199, 27 traces fetched, 13 unmined candidates). No new models. oMLX total 10122 -> 10135.
- Dataset 14974 -> 14987.

## 2026-10-09: oMLX batch 216 (+16 rows)

- oMLX corpus sweep: 16 records mined (scan198, 30 traces fetched, 16 unmined candidates). No new models. oMLX total 10106 -> 10122.
- Dataset 14958 -> 14974.

## 2026-10-09: oMLX batch 215 (+34 rows)

- oMLX corpus sweep: 34 records mined (scan197, 39 traces fetched, 25 unmined candidates). New model: Nail-Qwen3.6-35B-A3B (4bit). oMLX total 10072 -> 10106.
- Dataset 14924 -> 14958. Models 462.

## 2026-10-09: oMLX batch 214 (+57 rows)

- oMLX corpus sweep: 57 records mined (scan196, 60 traces fetched, 46 unmined candidates). No new models (ThinkingCap-Qwen3.8-27B oQ6e MTP consolidated). oMLX total 10015 -> 10072.
- Dataset 14867 -> 14924.

## 2026-10-09: oMLX batch 213 (+59 rows)

- oMLX corpus sweep: 59 records mined (scan195, 60 traces fetched, 46 unmined candidates). New models: NVIDIA-Nemotron-3-Nano-30B-A3B (4bit), Qwen3.6-35B-A3B-Holo3-Qwopus-AgentWorld (qx64 hi), Qwen3.8-27B-Brainwaves-2M (qx64 hi). Consolidated Ornith-1.5-9B mxfp8, Qwen3.5-2B SpecPrefill oQ3.5. oMLX total 9956 -> 10015 (10k crossed).
- Dataset 14808 -> 14867. Models 461.

## 2026-10-09: oMLX batch 212 (+55 rows)

- oMLX corpus sweep: 55 records mined (scan194, 60 traces fetched, 46 unmined candidates). No new models (Qwen3.8-27B MTPLX Bare Speed consolidated). oMLX total 9901 -> 9956.
- Dataset 14753 -> 14808.

## 2026-10-09: oMLX batch 211 (+38 rows)

- oMLX corpus sweep: 38 records mined (scan193, 52 traces fetched, 38 unmined candidates). No new models (Laguna-S-2.1 3bit consolidated). oMLX total 9863 -> 9901.
- Dataset 14715 -> 14753.

## 2026-10-09: oMLX batch 210 (+37 rows)

- oMLX corpus sweep: 37 records mined (scan192, 51 traces fetched, 37 unmined candidates). New model: Swift-1.5-Qwen3.8-27b-Uncensored-oQ4e (MTP). Consolidated GLM-5.3-Flash oQ4 MTP, Qwen3.5-122B-A10B oQ4 MTP. oMLX total 9826 -> 9863.
- Dataset 14678 -> 14715. Models 458.

## 2026-10-09: oMLX batch 209 (+20 rows)

- oMLX corpus sweep: 20 records mined (scan191, 34 traces fetched, 20 unmined candidates). No new models (Laguna XS 2.1 4bit, Qwen3.8-27B-Abliterated oQ6e consolidated). oMLX total 9806 -> 9826.
- Dataset 14658 -> 14678.

## 2026-10-09: oMLX batch 208 (+33 rows)

- oMLX corpus sweep: 33 records mined (scan190, 46 traces fetched, 32 unmined candidates). New model: Qwen3.5-9B-Claude-4.6-Opus-Reasoning-Distilled-v2 (4bit). Consolidated Cyber-Tiel-Coder-35B-A3B oQ4e, Mellum2.1-Thinking 6bit g64. oMLX total 9773 -> 9806.
- Dataset 14625 -> 14658. Models 457.

## 2026-10-09: oMLX batch 207 (+41 rows)

- oMLX corpus sweep: 41 records mined (scan189, 53 traces fetched, 39 unmined candidates). No new models (Qwen3.8-9B 4bit consolidated). oMLX total 9732 -> 9773.
- Dataset 14584 -> 14625.

## 2026-10-09: oMLX batch 206 (+18 rows)

- oMLX corpus sweep: 18 records mined (scan188, 32 traces fetched, 18 unmined candidates). No new models. oMLX total 9714 -> 9732.
- Dataset 14566 -> 14584.

## 2026-10-09: oMLX batch 205 (+39 rows)

- oMLX corpus sweep: 39 records mined (scan187, 53 traces fetched, 39 unmined candidates). No new models (Qwen3.6-35B-A3B-Claude-4.7-Opus-Reasoning-Distilled oQ4e consolidated). oMLX total 9675 -> 9714.
- Dataset 14527 -> 14566.

## 2026-10-09: oMLX batch 204 (+50 rows)

- oMLX corpus sweep: 50 records mined (scan186, 57 traces fetched, 43 unmined candidates). New models: RavenXAiLabs-Chaos-Agent-Qwen3.8-27B-Frontier-Intelligence-Injected-OBLITERATED (4bit), Ternary-Bonsai-2-27B-Abliterated-v2 (PQ2_0 MTP). Consolidated Llama-3.2-3B-Instruct 8bit. oMLX total 9625 -> 9675.
- Dataset 14477 -> 14527. Models 456.

## 2026-10-09: oMLX batch 203 (+52 rows)

- oMLX corpus sweep: 52 records mined (scan185, 60 traces fetched, 46 unmined candidates). No new models. oMLX total 9573 -> 9625.
- Dataset 14425 -> 14477.

## 2026-10-09: oMLX batch 202 (+59 rows)

- oMLX corpus sweep: 59 records mined (scan184, 60 traces fetched, 46 unmined candidates). New models: Underdog-27B-1.1, gemma-4-31B-it-uncensored (oQ8e MTP). Consolidated Qwen3.8-27B-Uncensored oQ8e MTP. oMLX total 9514 -> 9573.
- Dataset 14366 -> 14425. Models 454.

## 2026-10-09: oMLX batch 201 (+53 rows)

- oMLX corpus sweep: 53 records mined (scan183, 60 traces fetched, 46 unmined candidates). No new models (Qwen3.6-27B oQ4 fp16 MTP, gemma-4-12b-coder-fable5-composer2.5 8bit consolidated). oMLX total 9461 -> 9514.
- Dataset 14313 -> 14366.

## 2026-10-09: oMLX batch 200 (+53 rows)

- oMLX corpus sweep: 53 records mined (scan182, 60 traces fetched, 46 unmined candidates). No new models (Qwen3.8-27B MTPLX Optimized Quality FP16 consolidated). oMLX total 9408 -> 9461.
- Dataset 14260 -> 14313.

## 2026-10-09: oMLX batch 199 (+49 rows)

- oMLX corpus sweep: 49 records mined (scan181, 60 traces fetched, 46 unmined candidates). No new models. oMLX total 9359 -> 9408.
- Dataset 14211 -> 14260.

## 2026-10-09: oMLX batch 198 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan180, 60 traces fetched, 46 unmined candidates). No new models (Laguna XS 2.1 oQ4e, Qwen3.5-4B-OptiQ 4bit consolidated). oMLX total 9308 -> 9359.
- Dataset 14160 -> 14211.

## 2026-10-09: oMLX batch 197 (+47 rows)

- oMLX corpus sweep: 47 records mined (scan179, 60 traces fetched, 46 unmined candidates). New model: GLM5.3FH (published shorthand, 6bit). oMLX total 9261 -> 9308.
- Dataset 14113 -> 14160. Models 452.

## 2026-10-09: oMLX batch 196 (+47 rows)

- oMLX corpus sweep: 47 records mined (scan178, 60 traces fetched, 46 unmined candidates). New model: Selene-1-Mini-Llama-3.1-8B (q4). Consolidated Qwable-v2 oQ4e DWQ MTP Vision. RAM table extended for 18 GB Macs. oMLX total 9214 -> 9261.
- Dataset 14066 -> 14113. Models 451.

## 2026-10-09: oMLX batch 195 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan177, 60 traces fetched, 46 unmined candidates). No new models (Gemma 4 26B-A4B nvfp4 qmax, Qwen2.5-14B Instruct 4bit, Qwen3.8-Flash-Next oQ4e coder ngram MTP consolidated). oMLX total 9163 -> 9214.
- Dataset 14015 -> 14066.

## 2026-10-09: oMLX batch 194 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan176, 60 traces fetched, 46 unmined candidates). New model: gpt-oss 120B (8bit). Consolidated Qwen3.8-Flash-Next 6bit MTP, Swift-1.5-Qwen3.8-27b-oQ6e bf16 MTP, gemma-4-12B-it 6bit. oMLX total 9112 -> 9163.
- Dataset 13964 -> 14015. Models 451.

## 2026-10-09: oMLX batch 193 (+34 rows)

- oMLX corpus sweep: 34 records mined (scan175, 44 traces fetched, 30 unmined candidates). No new models. oMLX total 9078 -> 9112.
- Dataset 13930 -> 13964.

## 2026-10-09: oMLX batch 192 (+54 rows)

- oMLX corpus sweep: 54 records mined (scan174, 60 traces fetched, 46 unmined candidates). No new models (Qwen3.8-27B 2bit consolidated). oMLX total 9024 -> 9078.
- Dataset 13876 -> 13930.

## 2026-10-09: oMLX batch 191 (+50 rows)

- oMLX corpus sweep: 50 records mined (scan173, 60 traces fetched, 46 unmined candidates). New model: Qwen3.8-Flash-Next-heretic-2 (oQ4e MTP). Consolidated DeepSeek-V4-Flash-Vision-Exp, Devstral-Small-2 4bit, Mellum2.1-Thinking 6bit. oMLX total 8974 -> 9024.
- Dataset 13826 -> 13876. Models 450.

## 2026-10-09: oMLX batch 190 (+45 rows)

- oMLX corpus sweep: 45 records mined (scan172, 59 traces fetched, 45 unmined candidates). No new models (GLM-5.3-Flash oQ8e MTP, Devstral-Small-2-24B-Instruct-2512 mxfp4 consolidated). oMLX total 8929 -> 8974.
- Dataset 13781 -> 13826.

## 2026-10-09: oMLX batch 189 (+21 rows)

- oMLX corpus sweep: 21 records mined (scan171, 35 traces fetched, 21 unmined candidates). New model: gemma-4-31B-it-scotoma-2 (oQ4e MTP). Consolidated Qwen3.8-27B MLX/OptiQ 4bit, Qwen3-Coder-Next nightmedia mxfp8. oMLX total 8908 -> 8929.
- Dataset 13760 -> 13781. Models 449.

## 2026-10-09: oMLX batch 188 (+41 rows)

- oMLX corpus sweep: 41 records mined (scan170, 55 traces fetched, 41 unmined candidates). New models: GLM-OCR (bf16), Ornith-1.0-35B (4bit), qwen38 next (published shorthand, oQ4e variant). Consolidated Ternary-Bonsai-2-27B oQ6 MTP. oMLX total 8867 -> 8908.
- Dataset 13719 -> 13760. Models 448.

## 2026-10-09: oMLX batch 187 (+32 rows)

- oMLX corpus sweep: 32 records mined (scan169, 46 traces fetched, 32 unmined candidates). No new models (Qwen3.8-Flash-Next 3bit MTP, gemma-4-26B-A4B-it 6bit XL consolidated). oMLX total 8835 -> 8867.
- Dataset 13687 -> 13719.

## 2026-10-09: oMLX batch 186 (+30 rows)

- oMLX corpus sweep: 30 records mined (scan168, 44 traces fetched, 30 unmined candidates). No new models (qwen35 27B 6bit/8bit, Qwen3.8-Flash-Next oQ6 MTP, Qwen3.8-Flash-Next-Uncensored BAND-CODE58 3bit consolidated). oMLX total 8805 -> 8835.
- Dataset 13657 -> 13687.

## 2026-10-09: oMLX batch 185 (+17 rows)

- oMLX corpus sweep: 17 records mined (scan167, 31 traces fetched, 17 unmined candidates). No new models (Qwen3.8-35B-A3B-Distill 4bit, Qwen3.8 oQ4e MTP consolidated). oMLX total 8788 -> 8805.
- Dataset 13640 -> 13657.

## 2026-10-09: oMLX batch 184 (+17 rows)

- oMLX corpus sweep: 17 records mined (scan166, 31 traces fetched, 17 unmined candidates). No new models. oMLX total 8771 -> 8788.
- Dataset 13623 -> 13640.

## 2026-10-09: oMLX batch 183 (+39 rows)

- oMLX corpus sweep: 39 records mined (scan165, 49 traces fetched, 35 unmined candidates). New model: Swift-1.5-Qwen3.8-27b-Uncensored-VL-oQ6e (MTP). Consolidated Ornith-1.5-35B-A3B 6bit. oMLX total 8732 -> 8771.
- Dataset 13584 -> 13623. Models 445.

## 2026-10-09: oMLX batch 182 (+52 rows)

- oMLX corpus sweep: 52 records mined (scan164, 60 traces fetched, 46 unmined candidates). New model: Qwen2.5-Coder-1.5B (8bit). oMLX total 8680 -> 8732.
- Dataset 13532 -> 13584. Models 444.

## 2026-10-09: oMLX batch 181 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan163, 60 traces fetched, 46 unmined candidates). No new models (KAT-Coder-V2.5-Dev OptiQ 4bit + REAP-18B, Qwen3.8-27B Jundot oQ4e MTP, Qwen3.5-4B oQ8e fp16 MTP consolidated). oMLX total 8629 -> 8680.
- Dataset 13481 -> 13532.

## 2026-10-09: oMLX batch 180 (+46 rows)

- oMLX corpus sweep: 46 records mined (scan162, 60 traces fetched, 46 unmined candidates). No new models (AREX-2 8bit, Tiel-Coder-35B-A3B oQ4e fp16 MTP, gemma-4-26B-A4B-it mlx-community 6bit consolidated). oMLX total 8583 -> 8629.
- Dataset 13435 -> 13481.

## 2026-10-09: oMLX batch 179 (+32 rows)

- oMLX corpus sweep: 32 records mined (scan161, 46 traces fetched, 32 unmined candidates). New models: DeepSeek-V4-Flash-0731-Abliterated (Mixed 2bit-3bit g64), RavenX-CyberAgent-Qwen3.6-35B-A3B-Opus-4.7-OpenMythos-Pentester-BugHunter-RATH. Consolidated Ornith-1.5-9B oQ4e fp16. oMLX total 8551 -> 8583.
- Dataset 13403 -> 13435. Models 443.

## 2026-10-09: oMLX batch 178 (+20 rows)

- oMLX corpus sweep: 20 records mined (scan160, 34 traces fetched, 20 unmined candidates). New models: OLMoE-1B-7B-0125-Instruct (8bit), Swift-1.5-Qwen3.8-27b-Uncensored-oQ6e (MTP). Consolidated gemma-4-31B-it oQ6e MTP and qat mxfp4. oMLX total 8531 -> 8551.
- Dataset 13383 -> 13403. Models 441.

## 2026-10-09: oMLX batch 177 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan159, 42 traces fetched, 28 unmined candidates). New model: Qwen3.8-Flash-Next-Abliterated (4bit). Consolidated Qwen3.6-35B-A3B bf16-pt oQ3.5e MTP, Gemma 4 E4B oQ8. oMLX total 8503 -> 8531.
- Dataset 13355 -> 13383. Models 439.

## 2026-10-09: oMLX batch 176 (+12 rows)

- oMLX corpus sweep: 12 records mined (scan158, 26 traces fetched, 12 unmined candidates). No new models. oMLX total 8491 -> 8503.
- Dataset 13343 -> 13355.

## 2026-10-09: oMLX batch 175 (+22 rows)

- oMLX corpus sweep: 22 records mined (scan157, 36 traces fetched, 22 unmined candidates). No new models (Qwen3.8-27B-MTPLX-Optimized-Speed consolidated). oMLX total 8469 -> 8491.
- Dataset 13321 -> 13343.

## 2026-10-09: oMLX batch 174 (+41 rows)

- oMLX corpus sweep: 41 records mined (scan156, 55 traces fetched, 41 unmined candidates). New model: Huihui-Qwen3.6-35B-A3B-Claude-4.7-Opus-abliterated (8bit). oMLX total 8428 -> 8469.
- Dataset 13280 -> 13321. Models 438.

## 2026-10-09: oMLX batch 173 (+30 rows)

- oMLX corpus sweep: 30 records mined (scan155, 44 traces fetched, 30 unmined candidates). No new models (Qwen3.6-35B-A3B oQ4e fp16 MTP, Qwopus3.8-27B-Flash-V2 oQ8e MTP, Swift-1.5-Qwen3.8-27b-oQ5e-fp16-mtp consolidated). oMLX total 8398 -> 8428.
- Dataset 13250 -> 13280.

## 2026-10-09: oMLX batch 172 (+11 rows)

- oMLX corpus sweep: 11 records mined (scan154, 25 traces fetched, 11 unmined candidates). New models: Qwen3.5-9B-The-Defiant-Fable-Uncensored-Heretic-NEO-IMATRIX-MAX (oQ6e MTP), gemma-4-12B-it-qat-uncensored-heretic (4bit), nightmedia-Qwen3.8-27B-MindMeld (qx64 hi). Consolidated Qwen3.6-35B-A3B-MAYA oQ4e fp16 MTP. oMLX total 8387 -> 8398.
- Dataset 13239 -> 13250. Models 437.

## 2026-10-09: oMLX batch 171 (+10 rows)

- oMLX corpus sweep: 10 records mined (scan153, 24 traces fetched, 10 unmined candidates). No new models (Nanbeige4.2-3B OptiQ 4bit, gemma-4-12b-it oQ4e fp16 MTP consolidated). oMLX total 8377 -> 8387.
- Dataset 13229 -> 13239.

## 2026-10-09: oMLX batch 170 (+6 rows)

- oMLX corpus sweep: 6 records mined (scan152, 20 traces fetched, 6 unmined candidates). No new models. oMLX total 8371 -> 8377.
- Dataset 13223 -> 13229.

## 2026-10-09: oMLX batch 169 (+36 rows)

- oMLX corpus sweep: 36 records mined (scan151, 50 traces fetched, 36 unmined candidates). No new models (Qwen3.6-35B-A3B bf16-pt oQ5e MTP, Qwen3-27B mlx-community consolidated). oMLX total 8335 -> 8371.
- Dataset 13187 -> 13223.

## 2026-10-09: oMLX batch 168 (+13 rows)

- oMLX corpus sweep: 13 records mined (scan150, 27 traces fetched, 13 unmined candidates). No new models. oMLX total 8322 -> 8335.
- Dataset 13174 -> 13187.

## 2026-10-09: oMLX batch 167 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan149, 42 traces fetched, 28 unmined candidates). New model: GLM-5.3-Flash-CYBER (oQ4e MTP). Consolidated MiniCPM5-1B 4bit, gemma-4-31B-it mlx-community 8bit. oMLX total 8294 -> 8322.
- Dataset 13146 -> 13174. Models 434.

## 2026-10-09: oMLX batch 166 (+6 rows)

- oMLX corpus sweep: 6 records mined (scan148, 20 traces fetched, 6 unmined candidates). No new models. oMLX total 8288 -> 8294.
- Dataset 13140 -> 13146.

## 2026-10-09: oMLX batch 165 (+18 rows)

- oMLX corpus sweep: 18 records mined (scan147, 32 traces fetched, 41 unmined candidates). No new models. oMLX total 8270 -> 8288.
- Dataset 13122 -> 13140.

## 2026-10-09: oMLX batch 164 (+23 rows)

- oMLX corpus sweep: 23 records mined (scan146, 37 traces fetched, 23 unmined candidates). New model: Mellum2.1-12B-A2.5B-Thinking (mxfp4). Consolidated GLM-4.7-Flash 4bit, Qwen3.8-27B 3bit, Qwen3.6-35B-A3B Serve 4bit. oMLX total 8247 -> 8270.
- Dataset 13099 -> 13122. Models 433.

## 2026-10-09: oMLX batch 163 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan145, 39 traces fetched, 25 unmined candidates). New model: Qwen3.8-27B-TURBO-Fable-Cold-Fusion-NEO-CODER (oQ4e, 1M ctx). Consolidated gemma-4-26B-A4B-it oQ8e MTP, Ornith-1.5-9B (ornith-ai repo). oMLX total 8222 -> 8247.
- Dataset 13074 -> 13099. Models 432.

## 2026-10-09: oMLX batch 162 (+36 rows)

- oMLX corpus sweep: 36 records mined (scan144, 46 traces fetched, 32 unmined candidates). New model: Mistral-7B-Instruct-v0.3 (4bit). Consolidated Qwen3.5-122B-A10B Text mxfp4, gemma-4-31B-it oQ8e MTP, Qwen3.5-4B lmstudio-community 8bit. oMLX total 8186 -> 8222.
- Dataset 13038 -> 13074. Models 431.

## 2026-10-09: oMLX batch 161 (+47 rows)

- oMLX corpus sweep: 47 records mined (scan143, 60 traces fetched, 46 unmined candidates). New models: Ornith-1.0-35B-Vision, Qwen3.6-35B-A3B-Heretic (mxfp4). Consolidated Occamy-1.0 (4bit/oQ5e MTP), gemma-4-12b-it OptiQ 4bit, Gemma 4 E4B lmstudio-community 4bit/8bit, Qwen3.6-35B-A3B mlx-community 8bit. oMLX total 8139 -> 8186.
- Dataset 12991 -> 13038. Models 430.

## 2026-10-09: oMLX batch 160 (+25 rows)

- oMLX corpus sweep: 25 records mined (scan142, 32 traces fetched, 18 unmined candidates). No new models. oMLX total 8114 -> 8139.
- Dataset 12966 -> 12991.

## 2026-10-09: oMLX batch 159 (+48 rows)

- oMLX corpus sweep: 48 records mined (scan141, 60 traces fetched, 46 unmined candidates). New model: Ornith-1.5-35B-A3B-Vision-MTPLX (4bit). Consolidated Ornith-1.5-35B-A3B oQ6e fp16 MTP, Qwen3.8-Flash-Next-Uncensored REAP288 oQ3 MTP. oMLX total 8066 -> 8114.
- Dataset 12918 -> 12966. Models 428.

## 2026-10-09: oMLX batch 158 (+28 rows)

- oMLX corpus sweep: 28 records mined (scan140, 42 traces fetched, 28 unmined candidates). New models: Ornith-1.5-35B-MLX-VL (oQ6e/oQ8e), Ornith-Agents-A1-3.7-35B-A3B (oQ6 dare_ties_v4). Consolidated gemma-4-31B-it oQ8e MTP. oMLX total 8038 -> 8066.
- Dataset 12890 -> 12918. Models 427.

## 2026-10-09: oMLX batch 157 (+4 rows)

- oMLX corpus sweep: 4 records mined (scan139, 18 traces fetched, 4 unmined candidates). No new models (Muse Glimmer 30B MXFP4 consolidated). oMLX total 8034 -> 8038.
- Dataset 12886 -> 12890.

## 2026-10-09: oMLX batch 156 (+6 rows)

- oMLX corpus sweep: 6 records mined (scan138, 20 traces fetched, 6 unmined candidates). New models: Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC, Swift-1.5-Qwen3.8-27b-Uncensored-oQ5e (MTP). oMLX total 8028 -> 8034.
- Dataset 12880 -> 12886. Models 425.

## 2026-10-09: oMLX batch 155 (+27 rows)

- oMLX corpus sweep: 27 records mined (scan137, 41 traces fetched, 27 unmined candidates). New models: LLama-3.1-128k-Darkest-Planet-Uncensored-16.5B (q5), Ornith-1.5-9B-Abliterated (mxfp4). Consolidated FrogNano-4B-2609 oQ6e MTP. oMLX total 8001 -> 8028.
- Dataset 12853 -> 12880. Models 423.

## 2026-10-09: oMLX batch 154 (+8 rows)

- oMLX corpus sweep: 8 records mined (scan136, 22 traces fetched, 8 unmined candidates). No new models. oMLX total 7993 -> 8001.
- Dataset 12845 -> 12853.

## 2026-10-09: oMLX batch 153 (+12 rows)

- oMLX corpus sweep: 12 records mined (scan135, 26 traces fetched, 12 unmined candidates). No new models. oMLX total 7981 -> 7993.
- Dataset 12833 -> 12845.

## 2026-10-09: oMLX batch 152 (+15 rows)

- oMLX corpus sweep: 15 records mined (scan134, 29 traces fetched, 15 unmined candidates). No new models. oMLX total 7966 -> 7981.
- Dataset 12818 -> 12833.

## 2026-10-09: oMLX batch 151 (+17 rows)

- oMLX corpus sweep: 17 records mined (scan133, 31 traces fetched, 17 unmined candidates). No new models (Qwen2.5-7B-Instruct 4bit, Qwen3.8-Flash-Next-REAP-384 MTP consolidated). oMLX total 7949 -> 7966.
- Dataset 12801 -> 12818.

## 2026-10-09: oMLX batch 150 (+23 rows)

- oMLX corpus sweep: 23 records mined (scan132, 37 traces fetched, 23 unmined candidates). No new models. oMLX total 7926 -> 7949.
- Dataset 12778 -> 12801.

## 2026-10-09: oMLX batch 149 (+27 rows)

- oMLX corpus sweep: 27 records mined (scan131, 41 traces fetched, 27 unmined candidates). New model: Signal-3.8-27B (oQ4e MTP). Consolidated Agnes-3.0-Flash oQ4e MTP. oMLX total 7899 -> 7926.
- Dataset 12751 -> 12778. Models 421.

## 2026-10-09: oMLX batch 148 (+24 rows)

- oMLX corpus sweep: 24 records mined (scan130, 38 traces fetched, 24 unmined candidates). New model: Qwen3-1.7B (4bit). Consolidated Qwen3.8-27B-aeon-ultimate-uncensored attention8 bf16recurrence vision mtplx build. oMLX total 7875 -> 7899.
- Dataset 12727 -> 12751. Models 420.

## 2026-10-09: oMLX batch 147 (+10 rows)

- oMLX corpus sweep: 10 records mined (scan129, 24 traces fetched, 10 unmined candidates). No new models (Ornith-1.5-9B 8bit consolidated). oMLX total 7865 -> 7875.
- Dataset 12717 -> 12727.

## 2026-10-09: oMLX batch 146 (+36 rows)

- oMLX corpus sweep: 36 records mined (scan128, 45 traces fetched, 31 unmined candidates). No new models (Muse Glimmer 30B Abliterated MM oQ5, Qwen3.8-27B oQ4e MTP consolidated). oMLX total 7829 -> 7865.
- Dataset 12681 -> 12717.

## 2026-10-09: oMLX batch 145 (+47 rows)

- oMLX corpus sweep: 47 records mined (scan127, 60 traces fetched, 46 unmined candidates). New models: AX-Qwen3.6-35B-A3B (AXQ 6bit MTP), Huihui-gemma-4-26B-A4B-it-abliterated, Huihui-gemma-4-31B-it-abliterated-v2 (oQ8e MTP). Consolidated Qwen3.8-27B-Abliterated oQ4e MTP, Muse Glimmer 30B Abliterated MM oQ4e, Laguna S/XS 2.1 oQ4e/oQ5e. oMLX total 7782 -> 7829.
- Dataset 12634 -> 12681. Models 419.

## 2026-10-09: oMLX batch 144 (+33 rows)

- oMLX corpus sweep: 33 records mined (scan126, 47 traces fetched, 33 unmined candidates). No new models (GLM-5.3-Flash 2bit MTP consolidated). oMLX total 7749 -> 7782.
- Dataset 12601 -> 12634.

## 2026-10-09: oMLX batch 143 (+37 rows)

- oMLX corpus sweep: 37 records mined (scan125, 51 traces fetched, 37 unmined candidates). No new models (Ornith-1.5-35B-A3B-BigBang MTP zh 4bit consolidated). oMLX total 7712 -> 7749.
- Dataset 12564 -> 12601.

## 2026-10-09: oMLX batch 142 (+44 rows)

- oMLX corpus sweep: 44 records mined (scan124, 58 traces fetched, 44 unmined candidates). No new models. oMLX total 7668 -> 7712.
- Dataset 12520 -> 12564.

## 2026-10-09: oMLX batch 141 (+22 rows)

- oMLX corpus sweep: 22 records mined (scan123, 36 traces fetched, 22 unmined candidates). No new models (Muse Glimmer 30B oQ5e, Qwen3.6-27B MTP 4bit, Qwen3.8-Flash-Next oQ8 MTP, Gemma 4 E2B 8bit consolidated). oMLX total 7646 -> 7668.
- Dataset 12498 -> 12520.

## 2026-10-09: oMLX batch 140 (+19 rows)

- oMLX corpus sweep: 19 records mined (scan122, 33 traces fetched, 19 unmined candidates). No new models. oMLX total 7627 -> 7646.
- Dataset 12479 -> 12498.

## 2026-10-09: oMLX batch 139 (+8 rows)

- oMLX corpus sweep: 8 records mined (scan121, 22 traces fetched, 8 unmined candidates). No new models. oMLX total 7619 -> 7627.
- Dataset 12471 -> 12479.

## 2026-10-09: oMLX batch 138 (+32 rows)

- oMLX corpus sweep: 32 records mined (scan120, 46 traces fetched, 32 unmined candidates). New model mapping: Ling-3.0-flash (oQ4e MTP fp16). Consolidated Qwen3.8-27B-Uncensored oQ4e MTP, Tiel-Coder-35B-A3B oQ4e, Qwen3.8-27B AWQ 5.0bpw True2456 build. oMLX total 7587 -> 7619.
- Dataset 12439 -> 12471. Models 415.

## 2026-10-09: oMLX batch 137 (+18 rows)

- oMLX corpus sweep: 18 records mined (scan119, 31 traces fetched, 17 unmined candidates). New model mapping: 6-bit (name as published, model unnamed on page). oMLX total 7569 -> 7587.
- Dataset 12421 -> 12439. Models 414.

## 2026-10-09: oMLX batch 136 (+24 rows)

- oMLX corpus sweep: 24 records mined (scan118, 37 traces fetched, 23 unmined candidates). No new models (Qwen3.8-27B oQ8, Swift-1.5-Qwen3.8-27b-oQ6e fp16 MTP consolidated). oMLX total 7545 -> 7569.
- Dataset 12397 -> 12421.

## 2026-10-09: oMLX batch 135 (+10 rows)

- oMLX corpus sweep: 10 records mined (scan117, 24 traces fetched, 10 unmined candidates). No new models. oMLX total 7535 -> 7545.
- Dataset 12387 -> 12397.

## 2026-10-09: oMLX batch 134 (+5 rows)

- oMLX corpus sweep: 5 records mined (scan116, 19 traces fetched, 5 unmined candidates). No new models. oMLX total 7530 -> 7535.
- Dataset 12382 -> 12387.

## 2026-10-09: oMLX batch 133 (+9 rows)

- oMLX corpus sweep: 9 records mined (scan115, 23 traces fetched, 9 unmined candidates). No new models (Qwen3-4B-Instruct-2507 8bit consolidated). oMLX total 7521 -> 7530.
- Dataset 12373 -> 12382.

## 2026-10-09: oMLX batch 132 (+11 rows)

- oMLX corpus sweep: 11 records mined (scan114, 25 traces fetched, 11 unmined candidates). No new models. oMLX total 7510 -> 7521.
- Dataset 12362 -> 12373.

## 2026-10-08: oMLX batch 131 (+23 rows)

- oMLX corpus sweep: 23 records mined (scan113, 37 traces fetched, 23 unmined candidates). No new models (K2-Horizon-MoVA-36B-A4B 8bit, Qwen3.8-27B oQ6 consolidated). oMLX total 7487 -> 7510.
- Dataset 12339 -> 12362.

## 2026-10-08: oMLX batch 130 (+18 rows)

- oMLX corpus sweep: 18 records mined (scan112, 32 traces fetched, 18 unmined candidates). No new models (K2-Horizon-7B oQ8e, Qwen3-Coder-30B-A3B-Instruct 8bit consolidated). oMLX total 7469 -> 7487.
- Dataset 12321 -> 12339.

## 2026-10-08: oMLX batch 129 (+14 rows)

- oMLX corpus sweep: 14 records mined (scan111, 28 traces fetched, 14 unmined candidates). New model mapping: Flash-Next (4bit MTP, name as published, likely Qwen3.8-Flash-Next shorthand). oMLX total 7455 -> 7469.
- Dataset 12307 -> 12321. Models 413.

## 2026-10-08: oMLX batch 128 (+17 rows)

- oMLX corpus sweep: 17 records mined (scan110, 19 traces fetched, 5 unmined candidates). gpt-oss 20B oQ4 consolidated to merged-canonical name; Qwen3.8-27B oQ8e/oQ4e MTP + 4bit, Qwen3.8-Flash-Next oQ4e MTP. oMLX total 7438 -> 7455.
- Dataset 12290 -> 12307.

## 2026-10-08: oMLX batch 127 (+23 rows)

- oMLX corpus sweep: 23 records mined (scan109, 37 traces fetched, 23 unmined candidates). No new models. oMLX total 7415 -> 7438.
- Dataset 12267 -> 12290.

## 2026-10-08: oMLX batch 126 (+6 rows)

- oMLX corpus sweep: 6 records mined (scan108, 20 traces fetched, 6 unmined candidates). No new models (Muse Glimmer q4 consolidated to existing name; Qwen3.8-Flash-Next-Uncensored oQ4e coder-q8 ngram MTP). oMLX total 7409 -> 7415.
- Dataset 12261 -> 12267.

## 2026-10-08: oMLX batch 125 (+14 rows)

- oMLX corpus sweep: 14 records mined (scan107, 28 traces fetched, 14 unmined candidates). New model mapping: Qwen3.5-4B-OptiQ. oMLX total 7395 -> 7409.
- Dataset 12247 -> 12261. Models 412.

## 2026-10-08: oMLX batch 124 (+9 rows)

- oMLX corpus sweep: 9 records mined (scan106, 23 traces fetched, 9 unmined candidates). No new models. oMLX total 7386 -> 7395.
- Dataset 12238 -> 12247.

## 2026-10-08: oMLX batch 123 (+35 rows)

- oMLX corpus sweep: 35 records mined (scan105, 49 traces fetched, 35 unmined candidates). No new models (NVIDIA Nemotron 3.5 Lightning oQ6e MTP, Gemma 4 E2B it-qat 4bit consolidated). oMLX total 7351 -> 7386.
- Dataset 12203 -> 12238.

## 2026-10-08: oMLX batch 122 (+43 rows)

- oMLX corpus sweep: 43 records mined (scan104, 54 traces fetched, 40 unmined candidates). No new models (NVIDIA Nemotron 3.5 Lightning oQ6e, Qwen3.8-9B-Distill-Uncensored-Heretic oQ4e MTP, Gemma 4 E4B 8bit consolidated). oMLX total 7308 -> 7351.
- Dataset 12160 -> 12203.

## 2026-10-08: oMLX batch 121 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan103, 60 traces fetched, 46 unmined candidates). New model mappings: Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic (6bit), Qwen3.8-27B-UD-Q3_K_XL-DFlash2; consolidated Cyber-Tiel-Coder-35B-A3B oQ6e MTP, gemma-4-12B-it-qat oQ4e MTP, gemma-4-26B-A4B-it Unsloth UD 4bit. oMLX total 7257 -> 7308.
- Dataset 12109 -> 12160. Models 411.

## 2026-10-08: oMLX batch 120 (+53 rows)

- oMLX corpus sweep: 53 records mined (scan102, 60 traces fetched, 46 unmined candidates). New model mappings: Qwen3.8-27B-TWIN-TURBO-Fable-Cold-Fusion-709-L-Uncensored (oQ8 MTP, DavidAU build), granite-4.2-30b (q4); consolidated Qwen2.5-Coder-14B-Instruct 4bit, Qwen3.6-35B-A3B 6bit, Qwen3.8-27B-Uncensored 8bit (orcarouter). oMLX total 7204 -> 7257.
- Dataset 12056 -> 12109. Models 409.

## 2026-10-08: oMLX batch 119 (+52 rows)

- oMLX corpus sweep: 52 records mined (scan101, 60 traces fetched, 46 unmined candidates). New model mappings: Qwen3-Coder-Next-REAM (3bit), Qwen3.8-9B-Distill-Uncensored-Heretic (Q6G64 MTP); consolidated Laguna-S-2.1 oQ5e, Qwen3.8-27B oQ4e. oMLX total 7152 -> 7204.
- Dataset 12004 -> 12056. Models 407.

## 2026-10-08: oMLX batch 118 (+57 rows)

- oMLX corpus sweep: 57 records mined (scan100, 60 traces fetched, 46 unmined candidates). New model mapping: Huihui-Qwen3.5-9B-abliterated (4bit); consolidated Ornith-1.5-9B 4bit, Swift-1.5-Qwen3.8-27b-oQ5e MTP. oMLX total 7095 -> 7152.
- Dataset 11947 -> 12004. Models 405.

## 2026-10-08: oMLX batch 117 (+50 rows)

- oMLX corpus sweep: 50 records mined (scan99, 60 traces fetched, 46 unmined candidates). New model mapping: Qwen3.6-35B-A3B-MLX-VL (oQ4 FP16); consolidated LFM2-24B-A2B 4bit, Llama 3.3 70B 8bit, Qwen3-0.6B Base, gemma-4-26B-A4B-it oQ5, gemma-4-31B-it 8bit. oMLX total 7045 -> 7095.
- Dataset 11897 -> 11947. Models 404.

## 2026-10-08: oMLX batch 116 (+48 rows)

- oMLX corpus sweep: 48 records mined (scan98, 60 traces fetched, 46 unmined candidates). New model mapping: Qwen3.5-9B-Uncensored-HauhauCS-Aggressive (mxfp4); consolidated Nanbeige4.2-3B, Qwen3 14B/4B 4bit, Qwen3.8-35B-A3B-Distill oQ4e MTP, Qwen3.8-Flash-Next 4bit MTP. oMLX total 6997 -> 7045.
- Dataset 11849 -> 11897. Models 403.

## 2026-10-08: HF card scan batch 2, 4 cards (+8 rows)

- phntmwvs LFM2.5-8B-A1B-Hermes-Agentic-Coder-Abliterated-v3 MLX cards (4bit/8bit/BF16), M4 Pro (48 GB): generation 160.9 / 99.5 / 61.6 tok/s, prompt 146.2 / 281.4 / 142.1 tok/s, peak memory 5.4 / 9.6 / 17.0 GB. 6 rows.
- mlx-community/pplx-decider-v1.1-27b-4bit (new model), M5 Max (128 GB) High Power, MLX over HTTP: prefill ~975 tok/s cool GPU, ~730 sustained, 1.4-1.6x llama.cpp Q8_0/Q4_K_M same machine. 2 rows.
- Dataset 11841 -> 11849. Models 402.

## 2026-10-08: oMLX batch 115 (+94 rows)

- oMLX corpus sweep: 94 records mined (scan97, 60 traces fetched, 92 unmined candidates, 47 distinct signatures). New model mappings: Gemma-4-31B-heretic-ara, LFM2.5-8B-A1B-Hermes-Agentic-Coder-Abliterated-v3, LFM2.5-8B-A1B MXFP4, LFM2.5-VL-3B, LFM2.5-VL-450M, Qwen3 14B 8bit, Qwen3.8-27B oQ2.7e MTP, Qwen3.8-Flash-Next-REAP320 oQ3e DWQ MTP Vision, Swift-Qwen3.8-27b-oQ3e, Maple Preview 2bit MLX, Qwen3-VL-2B-Instruct, Ornith-1.5-9B 4bit/8bit. oMLX total 6903 -> 6997.
- Dataset 11747 -> 11841. Models 394 -> 401.

## 2026-10-08: HF card scan batch, 2 cards (+29 rows)

- nerkyor Coder390 GGUF-NInfer card, one RTX PRO 6000 Blackwell: NInfer vs llama.cpp aggregate throughput with built-in MTP across Q2/Q3/Q4 LynnStyle, Q6_K, Q8_0 (C4/C8, protocols differ per card); single-request 131.9 (NInfer MTP) vs 53.4 (llama.cpp no-spec) vs 97.2 C1 aggregate / 119.0 single-request (llama.cpp MTP); Q6_K NInfer C8 388.1; Q3 LynnStyle external Q8_0 MTP draft vs built-in Q4 head A/B (greedy 110.2 vs 112.2, T1 94.4 vs 95.6, acceptance ~66%/~52%). 19 rows.
- quaedra/Welp-35B-A3B card (new model), one RTX 4080 Super 16 GB: llama-bench tg128/pp4096 table, Welp-35B-A3B 164/5111, Unsloth UD-IQ3_XXS 165/5165, Qwen3.8-27B UD-Q3_K_XL 47/2155 (131k), Bonsai 2 27B 85/2278; plus 262k-context deep run after 214k prompt: decode 107, prefill 2043. 10 rows.
- Dataset 11718 -> 11747. Models 394.

## 2026-10-08: llama.cpp discussions #30069/#30071 (+30 rows)

- llama.cpp discussion #30071 lukolszewski/llama.cpp-multigpu fork vs upstream df03399b8: Qwen3.8-Flash-Next UD-Q4_K_XL, 5 slots x 262k, q8_0 KV, layer split over six GPUs on consumer PCIe (4 via USB4 eGPU docks). 6x RTX 3090 (new hardware) and 6x RTX 4090 (new hardware): prefill 1-session 50k 568 -> 2127 (3090) / 1728 -> 7050 (4090), 250k 263 -> 2111 / 744 -> 7403, 5-session aggregate 250k 265 -> 2060 (3090) / 7241 (4090, no baseline); generation 1-session 50k 25.7 -> 41.9 / 46.2 -> 57.5, 250k 10.2 -> 33.7 / 21.0 -> 48.7, 5-session per-session 250k 2.3 -> 27.3 (3090) / 30.8 (4090, no baseline). New backend llama.cpp (multigpu fork). 22 rows.
- llama.cpp discussion #30069 Arm scoreboard opener: Raspberry Pi 5 (BCM2712, new hardware, 2 GB), Qwen2.5-0.5B Q4_0 (new model), llama-bench pp512/tg128 at 1-4 threads, KleidiAI off: pp512 93.49 -> 289.92 t/s, tg128 32.42 -> 27.28 t/s. 8 rows.
- Dataset 11688 -> 11718. Hardware 429 -> 432, models 393, backends 45.

## 2026-10-08: GitHub pulse batch, 8 sources (+34 rows)

- llama.cpp PR #30150 fixed-width concat threaded over all rows: pp512/tg128 A/B medians on Phytium D3000M (new hardware, ARM armv8.2a, +33% pp) and Intel(R) Core(TM) Ultra 9 285K (new hardware, +17.2% pp). 4 rows.
- vLLM PR #60674 fused Gemma 4 Triton kernels: 1k prefill batch-4 A/B on A100-SXM4-80GB, Gemma 4 E2B 35480.8 -> 67488.9 tok/s (1.90x), E4B 22787.7 -> 34290.8 (1.50x). 4 rows.
- vLLM PR #60657 fused HyperConnection kernels gfx1100: Qwen3.8-Flash-Next GPTQ W4A16 TP4 on 4x RX 7900 XTX (new hardware), c1 decode 72.5 -> 76.6 tok/s. 2 rows.
- vLLM PR #60627 vectorized SM100 DCP Output/LSE consumer: GLM-5.2-NVFP4 TP4/DCP4 on 4x GB200, c1 46.576 -> 47.538 tok/s, c32 neutral. 4 rows.
- vLLM PR #60615 n-gram lookup in front of MTP drafting: Qwen3.8-Flash-Next NVFP4 on GB10, c1 decode across copy probe / Blazedit / SPEED-Bench at T=0 and T=1, +28% / +17% / +4% (T=0). 12 rows.
- vLLM PR #60570 persistent FlashInfer CUTLASS MoE workspace: Nemotron-3-Super-120B-A12B NVFP4 on an 8x B200 node (new hardware), c1 control 127.98 vs patched 128.07 (neutral), patched c64 5274.97 and c256 12686.38 tok/s (control OOMed at c64). 4 rows.
- vLLM PR #60500 device-side image normalize: Nemotron-Parse (new model) on one H100, c=8 document parsing 772.7 -> 937.9 tok/s (+21%). 2 rows.
- vLLM PR #60504 tuned Triton FusedMoE configs E=128: gemma-4-26B-A4B-it decode-heavy batch 4 on A100-SXM4-80GB, 4582.2 -> 5493.9 tok/s (1.20x). 2 rows.
- Parked: vLLM #60532 (SM80 named only as compute capability), #60524/#60479 (batch-invariance tables, no serving tok/s), #60689/#60683/#60670/#60663/#60647/#60645/#60622/#60618/#60604/#60602/#60589/#60583/#60568/#60546/#60538/#60528/#60500-comment arms (relative-only or no absolute rates). llama.cpp #30165/#30157/#30139 (no absolute tok/s). ExLlamaV2: nothing above #822.
- Dataset 11654 -> 11688. Hardware 425 -> 429, models 390 -> 392. Watermarks: llama.cpp -> #30165, vLLM -> #60689, ExLlamaV2 -> #822.

## 2026-10-08: oMLX batch 114 (+53 rows)

- oMLX corpus sweep: 53 records mined (scan96, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 6850 -> 6903.
- 2 new MAP entries, 1 new model: PaddleOCR-VL-1.6 (4bit, first OCR/VL model). 1 to existing (GLM-4.7-Flash 6bit).
- known.txt = 4593. Models 389 -> 390. Dataset 11601 -> 11654.

## 2026-10-08: oMLX batch 113 (+48 rows)

- oMLX corpus sweep: 48 records mined (scan95, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 6802 -> 6850.
- 3 new MAP entries, 1 new model: Huihui-Qwen3.6-35B-A3B-Claude-4.6-Opus-abliterated (Huihui abliterated build, oQ8, MTP). 2 to existing (Qwen3.6-35B-A3B-OptiQ-4bit-REAP-19B identity; Qwythos-9B-v2 OptiQ 4bit).
- known.txt = 4547. Models 388 -> 389. Dataset 11553 -> 11601.

## 2026-10-08: oMLX batch 112 (+44 rows)

- oMLX corpus sweep: 44 records mined (scan94, 58 traces fetched, 44 unmined candidates). No 404 (SKIP set active). oMLX total 6758 -> 6802.
- 2 new MAP entries, 1 new model: Qwen3.8-27B-heretic-ara (Heretic/ara fine-tune, oQ3.5e, MTP). 1 to existing (Swift-1.5-Qwen3.8-27b, RCO; DWQ build).
- First M6 chip traces (hardware "M6", consistent with existing; mine.py strips the "(12c)" suffix). 76 M6 records total.
- known.txt = 4501. Models 387 -> 388. Dataset 11509 -> 11553.

## 2026-10-08: oMLX batch 111 (+38 rows)

- oMLX corpus sweep: 38 records mined (scan93, 51 traces fetched, 37 unmined candidates). No 404 (SKIP set active). oMLX total 6720 -> 6758.
- 2 new MAP entries, 1 new model: Qwen3.8-Flash-Next-REAP-384 (REAP variant; existing were REAP-288 and REAP320). 1 to existing (Qwen3.8-27B 3bit MTP).
- known.txt = 4457. Models 386 -> 387. Dataset 11471 -> 11509.

## 2026-10-08: oMLX batch 110 (+50 rows)

- oMLX corpus sweep: 50 records mined (scan92, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 6670 -> 6720.
- 5 new MAP entries, 1 new model: Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED (mxfp8 fine-tune). 4 to existing (AREX-2 oQ8e fp16; muse-glimmer 30B 4bit OptiQ; NeoHorse-1-4B oQ4e; Qwen3.6-35B-A3B-MTPLX-Optimized-Speed FP16 build).
- known.txt = 4420. Models 385 -> 386. Dataset 11421 -> 11471.

## 2026-10-08: oMLX batch 109 (+48 rows)

- oMLX corpus sweep: 48 records mined (scan91, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 6622 -> 6670.
- 5 new MAP entries, 3 new models: Mellum-4b-base (Mellum v1, distinct from Mellum2), Qwen3.6-35B-A3B-MTPLX-Optimized-Speed (MTPLX build), gemma-4-26B-A4B-it-OptiQ-4bit-REAP-14B (REAP variant). 2 to existing (Qwen3.8-Flash-Next 2bit MTP; ThinkingCap-Qwen3.8-27B oQ8e MTP).
- known.txt = 4374. Models 382 -> 385. Dataset 11373 -> 11421.

## 2026-10-08: oMLX batch 108 (+40 rows)

- oMLX corpus sweep: 40 records mined (scan90, 54 traces fetched, 40 unmined candidates). No 404 (SKIP set active). oMLX total 6582 -> 6622.
- 3 new MAP entries, 1 new model: Qwen3.6-35B-A3B-Abliterated-Heretic (4bit). 2 mapped to existing (Qwen3.5-9B oQ4 MTP; Swift-1.5-Qwen3.8-27b-oQ4e MTP).
- known.txt = 4328. Models 381 -> 382. Dataset 11333 -> 11373.

## 2026-10-08: oMLX batch 107 (+37 rows)

- oMLX corpus sweep: 37 records mined (scan89, 50 traces fetched, 36 unmined candidates). No 404 (SKIP set active). oMLX total 6545 -> 6582.
- 5 new MAP entries, 0 new models (all to existing bases): Cyber-Tiel-Coder-35B-A3B, GLM-5.3-Flash-UNCENSORED, Qwen3.8-27B (pi build), Qwen3.8-Flash-Next-Uncensored, GLM-5.3 (omlx-glm53 build).
- known.txt = 4288. Models 381 (unchanged). Dataset 11296 -> 11333.

## 2026-10-08: oMLX batch 106 (+20 rows)

- oMLX corpus sweep: 20 records mined (scan88, 33 traces fetched, 19 unmined candidates). No 404 (SKIP set active). oMLX total 6525 -> 6545.
- 3 new MAP entries, 1 new model: a long Qwen3.8-27B-Coder390 EfficientThink fine-tune (nerkyor build, MTP + DFlash2 + fp16). 2 mapped to existing bases (Ornith-1.5-9B, gemma-4-26B-A4B-it).
- known.txt = 4252. Models 380 -> 381. Dataset 11276 -> 11296.

## 2026-10-08: oMLX batch 105 (+41 rows)

- oMLX corpus sweep: 41 records mined (scan87, 55 traces fetched, 41 unmined candidates). No 404 (SKIP set active). oMLX total 6484 -> 6525.
- 2 new MAP entries, 1 new model: Qwen3.6-35B (lowercase shorthand "qwen36-35b" in source; A3B omitted from the quote, so kept as a distinct shorthand name). 1 mapped to existing base (Qwen3.8-35B-A3B-Distill, oQ5e, vision).
- known.txt = 4233. Models 379 -> 380. Dataset 11235 -> 11276.

## 2026-10-08: oMLX batch 104 (+29 rows)

- oMLX corpus sweep: 29 records mined (scan86, 43 traces fetched, 29 unmined candidates). No 404 (SKIP set active). oMLX total 6455 -> 6484.
- 5 new MAP entries, 1 new model: Q_pi_S (S variant of the existing Q_pi base). 4 mapped to existing bases (K2-Horizon-3.7B, Qwen3 8B, Qwen3.8-27B-Coder390-LynnStyle-Mixed, Qwen3.8-Flash-Next).
- known.txt = 4192. Models 378 -> 379. Dataset 11206 -> 11235.

## 2026-10-08: oMLX batch 103 (+37 rows)

- oMLX corpus sweep: 37 records mined (scan85, 51 traces fetched, 37 unmined candidates). No 404 (SKIP set active). oMLX total 6418 -> 6455.
- 4 new MAP entries, 2 new models: Qwen3.8-27B-Coder390-LynnStyle-Mixed (Coder390 variant, A4toA8 build), Qwen3.8-Flash-Next-RCO256 (RCO256 variant). 2 mapped to existing bases (Qwen3.8-27B, Qwen3.6-35B-A3B).
- known.txt = 4163. Models 376 -> 378. Dataset 11169 -> 11206.

## 2026-10-08: oMLX batch 102 (+29 rows)

- oMLX corpus sweep: 29 records mined (scan84, 43 traces fetched, 29 unmined candidates). No 404 (SKIP set active). oMLX total 6389 -> 6418.
- 2 new MAP entries, 1 new model: Ornith-1.5-35B-A3B-V2-MTPLX (V2 build, following the Qwen3.8-27B-MTPLX precedent). 1 mapped to existing base (FrogNano-4B-2609, quant gptq, jang build).
- known.txt = 4126. Models 375 -> 376. Dataset 11140 -> 11169.

## 2026-10-08: oMLX batch 101 (+29 rows)

- oMLX corpus sweep: 29 records mined (scan83, 40 traces fetched, 26 unmined candidates). No 404 (SKIP set active). oMLX total 6360 -> 6389.
- 3 new MAP entries, 2 new models: Qwythos-9B-v3-Claude-Mythos-5-1M (v3, distinct from v2), Occamy-1.0-abliterated (abliterated variant). 1 mapped to existing base (Qwen2.5-Coder-14B-Instruct).
- known.txt = 4097. Models 373 -> 375. Dataset 11111 -> 11140.

## 2026-10-08: oMLX batch 100 (+48 rows)

- oMLX corpus sweep: 48 records mined (scan82, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 6312 -> 6360.
- 4 new MAP entries, all to existing bases (Ornith-1.5-35B-A3B-Abliterated, Ornith-1.5-35B-A3B, Qwen3.6-35B-A3B, Qwen3.8-27B). No new models (MAP approaching completeness).
- known.txt = 4071. Models 373 (unchanged). Dataset 11063 -> 11111. Batch 100 milestone.

## 2026-10-08: oMLX batch 99 (+47 rows)

- oMLX corpus sweep: 47 records mined (scan81, 57 traces fetched, 43 unmined candidates). No 404 (SKIP set active). oMLX total 6265 -> 6312.
- 2 new MAP entries, 1 new model: Huihui-Ornith-1.5-35B-A3B-abliterated (Huihui build, distinct from base Abliterated). 1 mapped to existing base (DeepSeek-V4-Flash).
- known.txt = 4025. Models 372 -> 373. Dataset 11016 -> 11063.

## 2026-10-08: oMLX batch 98 (+52 rows)

- oMLX corpus sweep: 52 records mined (scan80, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 6213 -> 6265.
- 4 new MAP entries, 2 new models: Qwen3.6-35B-A3B-MAYA, Swift-1.5-Qwen3.8-27b-oQ5e (distinct quant build, matching the oQ4e/oQ6e convention). 2 mapped to existing bases (Meta-Llama-3.1-8B-Instruct -> Llama 3.1 8B, Qwen3.5-4B).
- known.txt = 3982. Models 370 -> 372. Dataset 10964 -> 11016.

## 2026-10-08: oMLX batch 97 (+50 rows)

- oMLX corpus sweep: 50 records mined (scan79, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 6163 -> 6213.
- 2 new MAP entries, 1 new model: Qwen3.6-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking (new 40B size). 1 mapped to existing base (Swift-Qwen3.8-27B, distinct from the 1.5 family).
- known.txt = 3936. Models 369 -> 370. Dataset 10914 -> 10964.

## 2026-10-08: oMLX batch 96 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan78, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 6112 -> 6163.
- 5 new MAP entries, 2 new models: Qwopus3.6-27B-Coder (distinct from -Compat-MTP build), gemma-4-26B-A4B-it-heretic (distinct from -ara variant). 3 mapped to existing bases (Ling-3.0-tiny, Nex-N2.5-mini-Uncensored, Qwen3-VL-30B-A3B-Instruct).
- known.txt = 3890. Models 367 -> 369. Dataset 10863 -> 10914.

## 2026-10-08: oMLX batch 95 (+54 rows)

- oMLX corpus sweep: 54 records mined (scan77, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 6058 -> 6112.
- 8 new MAP entries, 2 new models: Cyber-Tiel-Coder-35B-A3B, Qwen3.8-Flash-Next-Dynamic. 6 mapped to existing bases (DeepSeek-V4.1-Flash, K2-Horizon-MoVA-36B-A4B, NVIDIA-Nemotron-3.5-Lightning-30B-A3B, Qwen3-Coder-Next, Qwen3.6-35B-A3B, Qwen3.6-35B-A3B-Claude-4.7-Opus-Reasoning-Distilled).
- known.txt = 3844. Models 365 -> 367. Dataset 10809 -> 10863.

## 2026-10-08: oMLX batch 94 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan76, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 6007 -> 6058.
- 4 new MAP entries, 1 new model: Nex-N2.5-mini (base, distinct from -Uncensored). 3 mapped to existing bases (GLM-5.3-Flash, Qwen3.8-Flash-Next, Swift-1.5-Qwen3.8-27b).
- known.txt = 3798. Models 364 -> 365. Dataset 10758 -> 10809.

## 2026-10-08: oMLX batch 93 (+56 rows)

- oMLX corpus sweep: 56 records mined (scan75, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 5951 -> 6007.
- 4 new MAP entries, 2 new models: K2-Horizon-MoVA-36B-A4B, Qwen3.6-35B-A3B-OptiQ-4bit-REAP-19B (REAP-pruned variant, kept distinct). 2 mapped to existing bases (Ornith-1.5-9B, Qwen-AgentWorld-35B-A3B).
- known.txt = 3752. Models 362 -> 364. Dataset 10702 -> 10758.

## 2026-10-08: oMLX batch 92 (+56 rows)

- oMLX corpus sweep: 56 records mined (scan74, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 5895 -> 5951.
- 4 new MAP entries, 2 new models: Ling-3.0-tiny-heretic (heretic fine-tune), Ornith-1.5-35B-A3B-Abliterated. 2 mapped to existing bases (Nex-N2.5-mini-Uncensored, Qwen3.8-27B-Uncensored).
- known.txt = 3706. Models 360 -> 362. Dataset 10646 -> 10702.

## 2026-10-08: oMLX batch 91 (+50 rows)

- oMLX corpus sweep: 50 records mined (scan73, 60 traces fetched, 46 unmined candidates). No 404 (SKIP set active). oMLX total 5845 -> 5895.
- 2 new MAP entries, 2 new models: Qwen3.6-35B-A3B-Heretic-Splash, Qwen3.6-35B-A3B-Uncensored-Genesis-Final-dequantized (distinct from non-dequantized, per the existing "-dequantized = distinct" convention).
- Collector fix: omlx_scan.py table parser now tolerates "\u2014" (em dash) in the peak-memory cell (and pp/tg), setting the field to None; mine.py note reads "peak memory not reported" when peak_gb is None. First hit on trace bbz2z9cp (Qwen3.6-35B-A3B-Heretic-Splash, 9 rows with peak "\u2014").
- known.txt = 3660. Models 358 -> 360. Dataset 10596 -> 10646.

## 2026-10-08: oMLX batch 90 (+19 rows)

- oMLX corpus sweep: 19 records mined (scan72, 33 traces fetched, 19 unmined candidates). No 404 (SKIP set active). oMLX total 5826 -> 5845. No new models (MiniCPM5-2B bf16 variant mapped to existing base).
- known.txt = 3614. Dataset 10577 -> 10596.

## 2026-10-08: oMLX batch 89 (+21 rows)

- oMLX corpus sweep: 21 records mined (scan71, 35 traces fetched, 21 unmined candidates). No 404 (SKIP set active). oMLX total 5805 -> 5826.
- 7 new MAP entries: 3 new models (AliceAI-T5-35B-A0.6B, gemma-4-26B-A4B-it-heretic-ara [distinct from the "uncensored" variant], Qwable-v2), 4 mapped to existing bases (Huihui-Qwen3.8-27B-abliterated, Ling-3.0-tiny, Qwen3.8-4B-Distill, Qwen3.8-9B-Distill).
- known.txt = 3595. Models 355 -> 358. Dataset 10556 -> 10577.

## 2026-10-08: oMLX batch 88 (+40 rows)

- oMLX corpus sweep: 40 records mined (scan70, 54 traces fetched, 40 unmined candidates). No 404 (SKIP set active). oMLX total 5765 -> 5805. No new models (all mapped to existing bases).
- 2 new MAP entries: Qwen3.8-27B-Alis-MLX-6bit (existing base, 6bit variant), Qwen3.8-27B-Q4-MTP.
- known.txt = 3574. Dataset 10516 -> 10556.

## 2026-10-08: oMLX batch 87 (+8 rows)

- oMLX corpus sweep: 8 records mined (scan69, 22 traces fetched, 8 unmined candidates). No 404 (SKIP set active). oMLX total 5757 -> 5765.
- 1 new MAP entry: Qwen3.8-27B-Alis-MLX-4bit (new model, community fine-tune).
- known.txt = 3534. Models 354 -> 355. Dataset 10508 -> 10516.

## 2026-10-08: oMLX batch 86 (+15 rows)

- oMLX corpus sweep: 15 records mined (scan68, 29 traces fetched, 15 unmined candidates). No 404 (SKIP set active). oMLX total 5742 -> 5757. No new models (all mapped to existing bases).
- known.txt = 3526. Dataset 10493 -> 10508.

## 2026-10-08: oMLX batch 85 (+21 rows)

- oMLX corpus sweep: 21 records mined (scan67, 35 traces fetched, 21 unmined candidates). No 404 (SKIP set active). oMLX total 5721 -> 5742. No new models (all mapped to existing bases).
- known.txt = 3511. Dataset 10472 -> 10493.

## 2026-10-08: oMLX batch 84 (+30 rows)

- oMLX corpus sweep: 30 records mined (scan66, 44 traces fetched, 30 unmined candidates). No 404 (SKIP set active). oMLX total 5691 -> 5721. No new models.
- Caught a slug collision: Qwen3-14B-MLX-4bit initially mapped to a new "Qwen3-14B", which collided with the existing "Qwen3 14B" (spaced) on slug qwen3-14b. Mapped to the existing "Qwen3 14B" instead (3 records corrected in place).
- known.txt = 3490. Dataset 10442 -> 10472.

## 2026-10-08: oMLX batch 83 (+32 rows)

- oMLX corpus sweep: 32 records mined (scan65, 46 traces fetched, 32 unmined candidates). No 404 (SKIP set active). oMLX total 5659 -> 5691. No new models (all mapped to existing bases).
- known.txt = 3460. Dataset 10410 -> 10442.

## 2026-10-08: oMLX batch 82 (+9 rows)

- oMLX corpus sweep: 9 records mined (scan64, 23 traces fetched, 9 unmined candidates). No 404 (SKIP set active). oMLX total 5650 -> 5659.
- 2 new MAP entries (existing bases): Qwen3.5-9B-oQ4e-mtp, gemma-4-26B-A4B-it-qat-4bit (QAT).
- known.txt = 3428. Dataset 10401 -> 10410.

## 2026-10-08: oMLX batch 81 (+26 rows)

- oMLX corpus sweep: 26 records mined (scan63, 40 traces fetched, 26 unmined candidates). No 404 (SKIP set active). oMLX total 5624 -> 5650.
- 2 new MAP entries (existing bases): Qwen3.8-27B-MTPLX-4bit, Qwen3.8-27B-oQ5e-mtp.
- known.txt = 3419. Dataset 10375 -> 10401.

## 2026-10-08: oMLX batch 80 (+38 rows)

- oMLX corpus sweep: 38 records mined (scan62, 52 traces fetched, 38 unmined candidates). No 404 (SKIP set active). oMLX total 5586 -> 5624.
- 2 new MAP entries: FrogNano-4B-2609-oQ8e-fp16-mtp (existing base), MiniCPM5-1B (new model, 4bit per family convention).
- known.txt = 3393. Models 353 -> 354. Dataset 10337 -> 10375.

## 2026-10-08: oMLX batch 79 (+10 rows)

- oMLX corpus sweep: 10 records mined (scan61, 24 traces fetched, 10 unmined candidates). No 404 (SKIP set active). oMLX total 5576 -> 5586.
- 2 new MAP entries (existing bases): Ling-3.0-tiny, Qwen3.8-Flash-Next-Uncensored-oQ3e-fp16-mtp.
- known.txt = 3355. Dataset 10327 -> 10337.

## 2026-10-08: oMLX batch 78 (+22 rows)

- oMLX corpus sweep: 22 records mined (scan60, 36 traces fetched, 22 unmined candidates). No 404 (SKIP set active). oMLX total 5554 -> 5576.
- 5 new MAP entries: FrogNano-4B-2609 (existing model, 4-bit quant), GLM-4.7-Flash-oQ4, Qwen3.6-35B-A3B-mxfp8, Qwen3.8-Flash-Next-MLX-oQ3-MTP, itrejomx--Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-MTPLX-6bit (new model).
- known.txt = 3345. Models 352 -> 353. Dataset 10305 -> 10327.

## 2026-10-08: oMLX batch 77 (+36 rows)

- oMLX corpus sweep: 36 records mined (scan59, 50 traces fetched, 36 unmined candidates). No 404 (SKIP set active). oMLX total 5518 -> 5554.
- 3 new MAP entries: DeepSeek-R1-0528-Qwen3-8B-MLX-8bit (new model), Huihui-Qwen3.8-27B-abliterated-oQ8e-mtp, Qwen3.8-Flash-Next-GSQ-RCO-Q2-mlx.
- known.txt = 3323. Models 351 -> 352. Dataset 10269 -> 10305.

## 2026-10-08: oMLX batch 76 (+32 rows)

- oMLX corpus sweep: 32 records mined (scan58, 46 traces fetched, 32 unmined candidates). No 404 (SKIP set active). oMLX total 5486 -> 5518.
- 4 new MAP entries: LFM2-24B-A2B-MLX-8bit (new model), Qwen3-Coder-Next-MLX-6bit, Qwen3.6-35B-A3B-MTP-mlx-8bit, Qwen3.8-27B-MTPLX-bf16.
- known.txt = 3287. Models 350 -> 351. Dataset 10237 -> 10269.

## 2026-10-08: oMLX batch 75 (+11 rows)

- oMLX corpus sweep: 11 records mined (scan57, 25 traces fetched, 11 unmined candidates). No 404 (SKIP set active). oMLX total 5475 -> 5486.
- 3 new MAP entries: Muse-Glimmer-30B-6bit, Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU-mlx-6Bit, supergemma4-26b-uncensored-mlx-4bit-v2 (new model).
- known.txt = 3255. Models 349 -> 350. Dataset 10226 -> 10237.

## 2026-10-08: oMLX batch 74 (+29 rows)

- oMLX corpus sweep: 29 records mined (scan56, 43 traces fetched, 29 unmined candidates). No 404 (SKIP set active). oMLX total 5446 -> 5475.
- 3 new MAP entries (existing bases): Qwen3.8-27B-oQ6-mtp, Swift-1.5-Qwen3.8-27b-oQ8e-mtp, gemma-4-e2b-it-5bit.
- known.txt = 3244. Dataset 10197 -> 10226.

## 2026-10-08: oMLX batch 73 (+35 rows)

- oMLX corpus sweep: 35 records mined (scan55, 49 traces fetched, 35 unmined candidates). No 404 this batch -- the new (model,chip) SKIP set for the 404-prone signature (gemma-4-31B-it-mxfp4, M4 Max) worked. oMLX total 5411 -> 5446.
- 2 new MAP entries (existing bases): Qwen3.5-9B-OptiQ-4bit, mlx-community--Qwen3.5-122B-A10B-oQ4-mtp.
- known.txt = 3215. Dataset 10162 -> 10197.

## 2026-10-08: oMLX batch 72 (+32 rows)

- oMLX corpus sweep: 36 records mined (scan54, 46 traces fetched, 33 unmined candidates), 4 dropped (trace 9si97uqi 404 after listing; gemma-4-31B-it mxfp4 M4 Max, 4th such 404 trace; retained in known.txt). Net +32. oMLX total 5379 -> 5411.
- 1 new MAP entry (existing base): Ornith-1.5-35B-A3B-oQ4e-fixed-mtp.
- Tooling: added a (model, chip) SKIP set to mine.py for the 404-prone signature (gemma-4-31B-it-mxfp4, M4 Max (40c)) so new IDs are skipped, not just the dropped ones.
- known.txt = 3180. Dataset 10130 -> 10162.

## 2026-10-07: oMLX batch 71 (+18 rows)

- oMLX corpus sweep: 22 records mined (scan53, 32 traces fetched, 20 unmined candidates), 4 dropped (trace gruplkic 404 after listing; gemma-4-31B-it mxfp4 M4 Max, 3rd such 404 trace; retained in known.txt). Net +18. oMLX total 5361 -> 5379.
- 1 new MAP entry (existing base): Qwen3.8-27B-Abliterated-MLX-MXFP4-MTP.
- known.txt = 3147. Dataset 10112 -> 10130.

## 2026-10-07: oMLX batch 70 (+35 rows)

- oMLX corpus sweep: 39 records mined (scan52, 44 traces fetched, 33 unmined candidates), 4 dropped (trace u15zfhx0 returned 404 after listing; gemma-4-31B-it mxfp4 on M4 Max, duplicate of dropped hlqpxcxp; retained in known.txt). Net +35. oMLX total 5326 -> 5361.
- 3 new MAP entries (all existing bases): Nemotron-Cascade-2-30B-A3B-mxfp8, Qwen3-Coder-Next-MLX-4bit, Swift1.5-Qwen3.8-Flash-Next-oQ4e-fp16-mtp.
- known.txt = 3128. Dataset 10077 -> 10112.

## 2026-10-07: oMLX batch 69 (+47 rows)

- oMLX corpus sweep: 51 records mined (scan51, 60 traces fetched, 46 unmined candidates), 4 dropped (trace hlqpxcxp returned 404 after listing, only gemma-4-31B-it mxfp4 rows, retained in known.txt to avoid re-scan). Net +47. oMLX total 5279 -> 5326.
- 1 new MAP entry: gemma-4-31B-it-mxfp4 (existing base).
- known.txt = 3097. Dataset 10030 -> 10077.

## 2026-10-07: oMLX batch 68 (+48 rows, dataset crosses 10,000)

- oMLX corpus sweep: 48 records mined (scan50, 60 traces fetched, 47 unmined candidates). oMLX total 5231 -> 5279.
- 5 new MAP entries: AX-Tiel-Coder-35B-A3B-MLX-AXQ-MXFP8-MTP (base Tiel-Coder-35B-A3B), Mellum2-12B-A2.5B-Instruct (new model), Qwen3.6-27B-MLX-4bit (base), Qwen3.8-3.6-27B-blend (new model), UI-Venus-2-9B (new model).
- known.txt = 3054. Dataset 9982 -> 10030 (10,000+).

## 2026-10-07: oMLX batch 67 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan49, 60 traces fetched, 47 unmined candidates). oMLX total 5180 -> 5231.
- 2 new MAP entries (both existing bases): Qwen3.8-27B-8Bit, Shiftedx--Qwen3.8-27B-Abliterated-MLX-MXFP4-MTP.
- known.txt = 3007. Dataset 9931 -> 9982.

## 2026-10-07: oMLX batch 66 (+48 rows)

- oMLX corpus sweep: 48 records mined (scan48, 60 traces fetched, 47 unmined candidates). oMLX total 5132 -> 5180.
- 7 new MAP entries: GLM-5.3-Flash-oQ4e-mtp, Ornith-1.5-35B-A3B-OptiQ-4bit-REAP-19B (base), Qwen3.8-27B-JANG_4D-CRACK (new model), Qwen3.8-27B-TURBO-Fable-Heretic (new model), Qwen3.8-Flash-Next-oQ2.5e-mtp, gemma-4-12b-coder-fable5-composer2.5 (new model), gemma-4-31B-it-oQ4e-mtp.
- known.txt = 2960. Dataset 9883 -> 9931.

## 2026-10-07: oMLX batch 65 (+50 rows)

- oMLX corpus sweep: 50 records mined (scan47, 60 traces fetched, 47 unmined candidates). oMLX total 5082 -> 5132.
- 4 new MAP entries: AREX-2-5bit, GLM-5.3-Flash-MLX-oQ4-MTP, Gemma-4-Dark-Thoughts-V2-31B (new model), Qwen-AgentWorld-35B-A3B-oQ4.
- known.txt = 2913. Dataset 9833 -> 9883.

## 2026-10-07: oMLX batch 64 (+54 rows)

- oMLX corpus sweep: 54 records mined (scan46, 60 traces fetched, 47 unmined candidates). oMLX total 5028 -> 5082.
- 6 new MAP entries: Jundot--Qwen3.6-35B-A3B-oQ4e-mtp, MiMo-V2.6-Flash-MOPD (new model), MiMo-V2.6-Flash-RL-mxfp4, Qwen3.6-35B-A3B-MLX-mixed-9bit, Qwen3.6-35B-A3B-oQ5-fp16-mtp, Qwen3.6-35B-A3B-oQ8e-fp16-mtp.
- known.txt = 2866. Dataset 9779 -> 9833.

## 2026-10-07: oMLX batch 63 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan45, 60 traces fetched, 47 unmined candidates). oMLX total 4977 -> 5028.
- 7 new MAP entries: LFM2.5-2.6B-MLX-8bit, Qwen3.6-27B-UD-Q4_K_XL, Qwen3.6-35B-A3B-Fable-Holo3.1-Qwopus-KAT-Coder-C-qx86-hi (new model), Qwen3.6-35B-A3B-MLX-VL (base, VL build), Qwen3.8-27B-oQ5e-SAGE-PATHS, Qwen3.8-27B-pi-FP8, gemma-4-26B-A4B-it-qat-OptiQ-4bit.
- known.txt = 2819. Dataset 9728 -> 9779.

## 2026-10-07: vLLM #60470 (Cake FlashInfer routes, +1 row)

- vLLM #60470 (opt-in Cake FlashInfer routes, KDA + MLA decode): 1 row on GB300, Kimi-K3 NVFP4, baseline total tok/s 8213 (this PR 8254, +0.5%, no speedup claimed); 1024/128 x200 @32, TP8 over 2 nodes x 4 GB300.
- llama.cpp #30118 checked (tool-call leak bug report, not minable).
- Watermarks: llama.cpp -> #30118, vLLM -> #60470. Dataset 9727 -> 9728.

## 2026-10-07: oMLX batch 62 (+51 rows)

- oMLX corpus sweep: 51 records mined (scan44, 60 traces fetched, 47 unmined candidates). oMLX total 4926 -> 4977.
- 1 new MAP entry (Qwen3.8-27B-oQ8e-mtp-fp16, 8-bit MTP build).
- known.txt = 2772. Dataset 9676 -> 9727.

## 2026-10-07: GitHub pulse (#30112, #30115, #60464, +8 rows)

- llama.cpp #30112 (multi-GPU MoE cache): 3 rows on 2x RTX 4090 (new hardware), Qwen3.8-Flash-Next Q4_0, SPEED-Bench osl 512 conc 1; master 34.78/440.7, --moe-cache-6544 60.38/402.0 (85.9% cache hit), -cmoe-15000 64.39/321.5 (95.8%); config tokens separate arms.
- llama.cpp #30115 (tiled Q4_K/Q6_K GET_ROWS): 1 row on Hexagon (new hardware), LFM2.5-2.6B Q4_K_M + DSpark draft speculation, decode 43.88 / prompt 57.49 tok/s.
- vLLM #60464 (SM90 block-FP8 CUTLASS kernel dispatch by M size): 4 rows on H100 NVL, Qwen3-8B-FP8, output tok/s at concurrency (stock CUTLASS baseline; this PR +17-52%); chat/long x 16/64 concurrent.
- 2 new hardware (2x RTX 4090, Hexagon). Qwen3-8B joined existing "Qwen3 8B" model via MODEL_MAP.
- Dataset 9668 -> 9676.

## 2026-10-07: HF card batch (8 cards, +12 rows)

- hf_scan backlog (7 new hits). 12 rows across 8 model cards, all with named hardware + measured tps:
  - d1-3B (LiquidAI 3B decision model, MLX 8-bit) on M3 Max 36 GB: decode 79.0 / prefill 746 (246-token image prompt).
  - CYBER-FROST 3.8 (MLX 4-bit) on M3 Ultra 256 GB, TensorFold: 26k agentic warm decode 96.3 (cold prefill 1,012); short-reply bench 136.6 greedy.
  - MiniCPM-V 4.6 (Huihui abliterated, 8-bit) on M1 Ultra 64 GB: ~140-180 decode, 144 on large-page OCR.
  - Qwen3.8-27B Huihui abliterated (oQ4e, MTP) on M1 Ultra 64 GB: chat decode 48-49 / prefill ~280; 16K decode 37-38.
  - Cyber-Tiel-Coder 35B (35B-A3B MoE, oQ6e) on M1 Ultra 64 GB: chat decode 107-116, prefill 4K ~1890 / 16K ~1640.
  - Laguna M.1 (Q3, 256-expert MoE) on M3 Max 128 GB: ~26.5 tok/s.
  - altar-1 (4-bit, ~330+ GB) on M3 Ultra 512 GB: ctx 128/2k/4k decode 13.7/12.6/13.0, prefill 86/205/194.
  - Ornith-1.5-35B (35B-A3B MoE, Q4_K_M) on RTX 4090 24 GB, llama.cpp: 113.8 tok/s at 160K ctx with DFlash2 draft speculation.
- 7 new models (d1-3B, CYBER-FROST-3.8, MiniCPM-V-4.6, CyberTiel-Coder-35B, Laguna-M.1, altar-1, Ornith-1.5-35B). Parked: ox-ox/Hy3-295B (chip unnamed, "128 GB Apple Silicon").
- Dataset 9656 -> 9668. Models 333 -> 340.

## 2026-10-07: HF card Ternary-Bonsai-2-27B on RTX 4070 (+8 rows)

- hf_scan hit: CaryPalmer/Ternary-Bonsai-2-27B-262k-GGUF. PrismML Ternary Bonsai 2 27B (1.58-bit ternary PTQ1_0) re-served via the ada-surgery fork (tiered KV cache, first ~113k in VRAM + pinned RAM, q8_0 KV, MTP spec decode) on one RTX 4070 12 GB. 8 rows (decode + cumulative prefill tok/s) across the full 262,144-token window: 4k 83/1100, 16k 106/1100, 32k 100/918, 64k 87/724, 112k 70/539, 131k 41/374, 180k 27/298, 258k 14.7/229. New backend "llama.cpp (ada-surgery fork)"; existing model Ternary-Bonsai-2-27B, hardware RTX 4070.
- Dataset 9648 -> 9656. Backends 43 -> 44.

## 2026-10-07: oMLX traces batch 61 (+52 rows)

- scan43: listing 2,781 -> 2,809 IDs; fetched 60 new trace pages, 47 new candidates parsed and mined (52 records). New MAP entries: Jundot:gemma-4-31B-it-oQ4e-mtp (existing model gemma-4-31B-it, oQ4e, Jundot build), Ornith-1.5-9B-MLX-6bit (existing model Ornith-1.5-9B, 6bit).
- oMLX source total 4,926 rows. Dataset 9596 -> 9648. known.txt = 2,725 (all candidates known, corpus swept again).

## 2026-10-07: oMLX traces batch 60 (+53 rows)

- scan42: fetched 60 new trace pages, 47 new candidates parsed and mined (53 records, some traces carry multiple context rows / duplicate sessions). New MAP entries: Qwen3.8-35B-A3B-Distill-Heretic-oQ4-fp16-mtp (new model Qwen3.8-35B-A3B-Distill-Heretic, oQ4, fp16 mtp build), Nemotron-Cascade-2-30B-A3B-4bit (new model Nemotron-Cascade-2-30B-A3B).
- oMLX source total 4,874 rows. Dataset 9543 -> 9596, models 331 -> 333. known.txt = 2,678 (all candidates known, corpus swept again).

## 2026-10-07: vLLM #60445 Gemma4 KV-sharing fast prefill (+64 rows)

- Mined the Suite 1 (default out-of-the-box) E2E serving benchmark on A100-SXM4-80GB: 5 Gemma4 models (E2B, E4B, 12B, 26B-A4B, 31B) across 4 scenarios (prefill_heavy in=1024, balanced in=512, decode_heavy in=128, long_context in=4096) and batch sizes 1-16. Stored the Base (main) arm total tokens/s (in+out) as pp_tps with ctx=in_len; PR arm + speedup in notes. E2B/E4B see up to 2.10x (KV-sharing fast prefill); 12B/26B/31B are parity (no kv_shared_layers). 64 rows, all models/hardware existing.
- Dataset 9479 -> 9543. Watermark vLLM -> #60450.

## 2026-10-07: oMLX traces batch 59 (+48 rows)

- scan41: listing grew to 2,767 IDs (+170); fetched 60 new trace pages (13 returned 404, deleted upstream), 47 new candidates parsed and mined (48 records). New MAP entries: NVIDIA-Nemotron-3.5-Lightning-30B-A3B-oQ4e-mtp (existing model), Qwen3.5-35B-A3B-Uncensored-FernflowerAI-MLX-4bit (new model Qwen3.5-35B-A3B-Uncensored), Qwen3.6-35B-A3B-oQ4e-MTP, Qwen3.8-27B-oQ4, Qwen3.8-Flash-Next-Uncensored-oQ4e-mtp, Swift1.5-Qwen3.8-Flash-Next-oQ4e-mtp, ornith-1.5-35b-a3b-mtp-mlx-4bit.
- oMLX source total 4,821 rows. Dataset 9431 -> 9479, models 330 -> 331. known.txt = 2,631 (all candidates known, corpus swept again).

## 2026-10-07: GitHub mining batch (+3 rows)

- Mined 2 vLLM issues: #60426 (Kimi-K3, MI355X TP8 DCP1, fp8 KV cache, vllm bench ISL 100000 OSL 512 c1; interactivity 177.3 baseline, PR group-metadata reuse 184.1) and #60413 (Qwen3.8-27B-Quark-AWQ-MXFP4, AMD Strix Halo gfx1151, W4A8 MXFP4 GEMV kernel flag on; decode 12.45 MTP 0 / 22.45 MTP 3, single stream). vLLM rows store the measured arm; #60413 baseline (flag off) was pending at measurement time so the PR rows are stored with the baseline noted.
- All hardware/models existing (MI355X, Kimi-K3, AMD Strix Halo, Qwen3.8-27B). Skipped: vLLM #60422 (RFC, no perf table), llama.cpp #30106 (MUL_MAT correctness fix, no tps), #30107 (TOP_K fix), #30108 (relative CPU latency regression note, no absolute tok/s).
- Dataset 9428 -> 9431.

## 2026-10-07: oMLX traces batch 58 (+22 rows, final sweep)

- scan40 closed out the corpus sweep: listing 2,597 IDs, 2,584 candidates fetched, all handled (known.txt = 2,584). 22 remaining candidates mined, most duplicate sessions of already-seen benchmarks (notes carry the duplicate trace IDs). New MAP entries: Qwen3.8-4B-Distill (new model), Qwen3.8-Flash-Next-Uncensored-TF-4bit-MTP, Qwen3.8-27B-Uncensored-MLX-8bit, GLM-5.3-Flash-Alis-MLX-4bit, MiniCPM5-2B-OptiQ-4bit.
- oMLX source total 4,773 rows. Dataset 9406 -> 9428.

## 2026-10-07: GitHub mining batch (+33 rows)

- Mined 6 GitHub issues: vLLM #60397 (MI355X DeepSeek-V4.1-Flash mono decode, TP2/TP4 c1-c8, +8), llama.cpp #30087 (RTX 4090 FE, Qwen3.8-27B UD-Q4_K_XL GDN half-warp kernel A/B, pp512/pp4096/tg128, +6), vLLM #60355 (2 x GB200 DeepSeek-V4.1-Flash fused CuTe DSL all-reduce, c1-c64 plus DSpark k=5 c1-c4, +10), vLLM #60387 (DGX Spark spec-decode reduced-vocab A/B, Llama 3.1 8B and EXAONE-4.5-33B, +2), vLLM #60390 (RTX PRO 6000 Qwen3.8-Flash-Next NVFP4 shared PLE table, 1-card ref + two 2-card configs, +3), llama.cpp #30105 (Radeon AI PRO R9700 Vulkan, Mistral Small 4 IQ4_XS FP32 kernel fix before/after, +4).
- New hardware "2 x GB200"; new models "EXAONE-4.5-33B", "Mistral Small 4". A/B rows carry config tokens; vLLM rows store the baseline (main / full-vocab / unpatched) arm with the PR arm noted. Parked: #30091 (hardware unnamed in body).
- Dataset 9373 -> 9406.

## 2026-10-07: oMLX traces batch 57 (+3 rows)

- Next listing-growth sweep (listing now 2,575 IDs, 2,562 candidates fetched, all handled): Jundot Qwen3.8-27B oQ8e MTP, plus mapped-model sessions.
- Dataset 9370 -> 9373.

## 2026-10-07: oMLX traces batch 56 (+7 rows)

- Next listing-growth sweep (listing now 2,572 IDs, 2,559 candidates fetched, all handled). No new model names; all mapped-model sessions.
- Dataset 9363 -> 9370.

## 2026-10-07: oMLX traces batch 55 (+17 rows)

- Next listing-growth sweep (listing now 2,565 IDs, 2,552 candidates fetched, all handled): gemma-4-26B-A4B-it oQ4e MTP, plus mapped-model sessions.
- Dataset 9346 -> 9363.

## 2026-10-07: oMLX traces batch 54 (+15 rows)

- Next listing-growth sweep (listing now 2,548 IDs, 2,535 candidates fetched, all handled): Gemma 4 E2B 4bit, plus mapped-model sessions. Added 8 GB to the RAM lookup (a new machine size in the corpus).
- Dataset 9331 -> 9346.

## 2026-10-07: oMLX traces batch 53 (+29 rows)

- Next listing-growth sweep (listing now 2,533 IDs, 2,520 candidates fetched, all handled). No new model names; all mapped-model sessions.
- Dataset 9302 -> 9331.

## 2026-10-07: oMLX traces batch 52 (+44 rows)

- Next listing-growth sweep (listing now 2,504 IDs, 2,491 candidates fetched, all handled): Ternary-Bonsai-2-27B MLX 2bit, Qwen3.6-27B 6bit, DeepSeek-V4-Flash-0731 2.4bit mixed, Ling-3.0-tiny oQ6e fp16, MiniCPM5-2B oQ5 fp16.
- Dataset 9258 -> 9302.

## 2026-10-07: oMLX traces batch 51 (+39 rows)

- Next listing-growth sweep (listing now 2,460 IDs, 2,447 candidates fetched, all handled): Qwen3.8-27B 4bit ms, Qwen2.5-VL-7B-Instruct 4bit, plus mapped-model sessions.
- Dataset 9219 -> 9258.

## 2026-10-07: oMLX traces batch 50 (+25 rows)

- Next listing-growth sweep (listing now 2,421 IDs, 2,408 candidates fetched, all handled): Gemma 4 31B 5bit, Gemma 4 E4B nvfp4, Qwen3.8-27B-Uncensored oQ8e fp16 MTP oMLX 0.7.0, Gemma 4 E2B nvfp4, Qwen3.5-9B MLX 4bit (mlx-community), Qwen2.5-1.5B-Instruct, ThinkingCap Qwen3.6-27B OptiQ-4bit (mlx-community), Qwen2.5-Coder-1.5B-Instruct (mlx-community).
- Dataset 9194 -> 9219.

## 2026-10-07: oMLX traces batch 49 (+21 rows)

- Next listing-growth sweep (listing now 2,396 IDs, 2,383 candidates fetched, all handled): Occamy-1.0 oQ8e, Nanbeige4.2-3B oQ4e, Gemma 4 E4B qat-OptiQ-4bit (mlx-community), Qwen3.8-27B TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored NM DAU oQ8e 1M.
- Dataset 9173 -> 9194.

## 2026-10-07: oMLX traces batch 48 (+39 rows)

- Next listing-growth sweep (listing now 2,375 IDs, 2,362 candidates fetched, all handled): Gemma 4 E4B 4bit (mlx-community and bare variants), plus mapped-model sessions.
- Dataset 9134 -> 9173.

## 2026-10-07: oMLX traces batch 47 (+35 rows)

- Next listing-growth sweep (listing now 2,334 IDs, 2,323 candidates fetched, all handled): NeoHorse-1-4B and NeoHorse-1-9B oQ4e MTP, Swift Qwen3.8-Flash-Next oQ4e MTP, Ornith-1.5-35B-A3B refusal-ablated oQ8 MTP, Qwen3.8-35B-A3B-Distill MLX 8bit.
- Dataset 9099 -> 9134.

## 2026-10-07: oMLX traces batch 46 (+16 rows)

- Next listing-growth sweep (listing now 2,299 IDs, 2,288 candidates fetched, all handled): Ornith-1.5-35B-A3B oQ8e and oQ2e MTP, DeepSeek-R1-Distill-Llama-70B 4bit, Bonsai-2-27B-CRACK-Ternary oMLX, Qwen3.6-35B-A3B oQ4e FP16 MTP MLX.
- Dataset 9083 -> 9099.

## 2026-10-07: oMLX traces batch 45 (+34 rows)

- Next listing-growth sweep (listing now 2,283 IDs, 2,272 candidates fetched, all handled): Gemma 4 31B 8bit, Qwen3.8-27B 8bit MTP MLX, Qwen3.6-27B oQ4e MTP, plus mapped-model sessions.
- Dataset 9049 -> 9083.

## 2026-10-07: oMLX traces batch 44 (+64 rows)

- Next listing-growth sweep (listing now 2,258 IDs, 2,243 candidates fetched, all handled): Qwen3.6-35B-A3B-Uncensored-Heretic oQ8 fp16 MTP, Qwen3.5-9B-GLM5.1-Distill-v1 4bit, Qwen3.8-Flash-Next MLX 4bit, Qwen3.8-27B oQ6 MTP, supergemma4-26b-abliterated-multimodal 4bit, Gemma 4 26B-A4B-it-uncensored oQ5 fp16, Gemma 4 Ortenzya-The-Creative-Wordsmith-31B-it-uncensored-heretic 8bit, Qwen3.6-35B-A3B oQ4 fp16 MTP.
- Dataset 8985 -> 9049.

## 2026-10-07: oMLX traces batch 43 (+51 rows)

- Next listing-growth sweep (listing now 2,249 IDs, 2,194 candidates fetched, all handled): Huihui Qwen3.8-Flash-Next abliterated oQ4e MTP, Qwen3.8-27B-aeon-ultimate-uncensored MXFP4 vision MTP, Qwen3.6-35B-A3B Uncensored-Genesis-Hermes-V13 dequantized oQ6e fp16 MTP, Qwen3.6-35B-A3B Uncensored-HauhauCS-Aggressive oQ4, Qwen3.8-27B TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored NM DAU oQ4e 1M, Gemma 4 12B 8bit, NVIDIA Nemotron 3.5 Lightning 4bit.
- Dataset 8934 -> 8985.

## 2026-10-07: oMLX traces batch 42 (+49 rows)

- Next listing-growth sweep (listing now 2,214 IDs, 2,145 candidates fetched, all handled): Qwen3.8-27B AWQ-5.0bpw, Hermes-4-70B MLX 8bit, DeepSeek-Coder-V2-Lite-Instruct MLX 4bit, DeepHermes-3-Llama-3-8B-Preview 4bit, qwen3.5-4b-agentic-coder-v4 MLX 4bit, Qwen3.6-27B OptiQ-4bit.
- Dataset 8885 -> 8934.

## 2026-10-07: oMLX traces batch 41 (+53 rows)

- Next listing-growth sweep (listing now 2,180 IDs, 2,096 candidates fetched, all handled): gpt-oss 20B MXFP4-Q8 (mlx-community), Qwen3-Coder-30B-A3B-Instruct MLX 4bit, plus mapped-model sessions.
- Dataset 8832 -> 8885.

## 2026-10-07: oMLX traces batch 40 (+57 rows)

- Next listing-growth sweep (listing now 2,172 IDs, 2,047 candidates fetched, all handled): Qwythos-9B-v2 MLX 8bit, Gemma 4 E4B 4bit, plus mapped-model sessions.
- Dataset 8775 -> 8832.

## 2026-10-07: oMLX traces batch 39 (+54 rows)

- Next listing-growth sweep (listing now 2,156 IDs, 1,998 candidates fetched, all handled): Qwen3.5-9B MLX 8bit, Hemmingway-1 oQ4e MTP, Qwen3.8-27B-Uncensored base, Qwen3.6-35B-A3B oQ5e fp16 MTP, Qwen3.5-35B-A3B 4bit, Muse Glimmer Abliterated MM oQ5e.
- Dataset 8721 -> 8775.

## 2026-10-07: oMLX traces batch 38 (+55 rows)

- Next listing-growth sweep (listing now 2,144 IDs, 1,949 candidates fetched, all handled): Ornith-1.5-35B-A3B OptiQ-4bit, ThinkingCap Qwen3.8-27B 4bit DWQ, Mistral-Small-3.2-24B-Instruct-2506, Qwen3-Coder-30B-A3B-Instruct MLX 8bit, Jundot Qwen3.8-Flash-Next oQ4e MTP, clef oQ4e, Qwen3.6-27B-Coder-uncensored MXFP4, Qwen3.6-35B-A3B Claude-4.7-Opus-Reasoning-Distilled oQ4e MTP.
- Dataset 8666 -> 8721.

## 2026-10-07: oMLX traces batch 37 (+59 rows)

- Next listing-growth sweep (listing now 2,107 IDs, 1,900 candidates fetched, all handled): GLM-5.3-Flash-Abliterated 4bit, LFM2.5-8B-A1B 8bit, Qwen3.6-35B-A3B Uncensored-Genesis-Final dequantized oQ8e fp16 MTP, GLM-5.3 mixed 4/8, translategemma-4b-it, Qwen3.8-27B MLX Serve 4bit/8bit, Qwen3-Coder-30B-A3B-Instruct, bitnet-b1.58-2B-4T, Ornith-1.5-35B-A3B 8bit/MLX.
- Dataset 8607 -> 8666.

## 2026-10-07: oMLX traces batch 36 (+59 rows)

- Next listing-growth sweep (listing now 2,074 IDs, 1,849 candidates fetched, all handled): Dirk Qwen3.8-27B oQ6e, Qwen3.6-35B-A3B MLX Serve 4bit, plus mapped-model sessions.
- Dataset 8548 -> 8607.

## 2026-10-07: oMLX traces batch 35 (+57 rows)

- Next listing-growth sweep (listing now 2,046 IDs, 1,798 candidates fetched, all handled): Qwen3.8-Flash-Next oQ8e MTP, Gemma 4 E4B oQ4e MTP, Qwen3.6-27B 8bit, plus mapped-model sessions.
- Dataset 8491 -> 8548.

## 2026-10-07: oMLX traces batch 34 (+59 rows)

- Next listing-growth sweep (listing now 2,031 IDs, 1,747 candidates fetched, all handled): Qwen3-Coder-Next-REAP-48B-A3B 4bit MLX, Qwen3.5-9B MXFP4, plus mapped-model sessions.
- Dataset 8432 -> 8491.

## 2026-10-07: oMLX traces batch 33 (+52 rows)

- Next listing-growth sweep (listing now 2,019 IDs, 1,696 candidates fetched, all handled): Nail Qwen3.6-35B-A3B 6bit, Qwen3.8-Flash-Next oQ4e fp16 MTP and REAP320 oQ3e-DWQ MTP Vision and Uncensored oQ6e MTP, MiMo-V2.6-Distill-Qwen-9B, MiMo-V2.6-Flash-RL 4bit MTP, Ornith-1.5-35B-A3B oQ3e MTP.
- Dataset 8380 -> 8432.

## 2026-10-07: oMLX traces batch 32 (+56 rows)

- Next listing-growth sweep (listing now 2,003 IDs, 1,645 candidates fetched, all handled): Qwen3.8-9B-heretic-uncensored MTPLX, Qwen3.8-27B-MTPLX Optimized-Speed, Qwen3.8-27B bf16, Hy-MT2-1.8B 4bit, Qwen3.6-35B-A3B oQ6e MTP.
- Dataset 8324 -> 8380.

## 2026-10-07: oMLX traces batch 31 (+61 rows)

- Next listing-growth sweep (listing now 1,984 IDs, 1,594 candidates fetched, all handled): Qwen3.6-35B-A3B 5bit, GLM-5.3-Flash mixed 4/8bit MLX, plus mapped-model sessions.
- Dataset 8263 -> 8324.

## 2026-10-07: oMLX traces batch 30 (+55 rows)

- Next listing-growth sweep (listing now 1,970 IDs, 1,543 candidates fetched, all handled): GLM-5.3-Flash-UNCENSORED oQ4e DFlash2 (17 traces), Swift-1.5-Qwen3.8-27b-oQ4e-mtp, Qwen3.6-35B-A3B OptiQ-4bit and 6bit and bf16-baseline, Qwen3.5-VL-9B 4bit CRACK, Qwen3-4B-Instruct-2507, Qwen3.5-4B 4bit.
- Dataset 8208 -> 8263.

## 2026-10-07: oMLX traces batch 29 (+57 rows)

- Next listing-growth sweep (listing now 1,936 IDs, 1,492 candidates fetched, all handled): DeepSeek-V4-Flash 4bit, FrogNano-4B-2609 oQ8e MTP, Qwen3.6-14B-A3B-FableVibes, Qwen3.6-35B-A3B 4bit DWQ, Qwen3.8-27B-MTPLX Speed, Gemma 4 26B-A4B 6bit, Mistral-Small-4-119B-2603, Devstral-Small-2-24B-Instruct-2512, Swift Qwen3.8-27b oQ4e fp16 MTP.
- Dataset 8151 -> 8208.

## 2026-10-07: oMLX traces batch 28 (+60 rows)

- Next listing-growth sweep (listing now 1,929 IDs, 1,441 candidates fetched, all handled): Qwen3.8-Flash-Next oQ4e MTP fp16, Qwen3.6-35B-A3B bf16, Qwen3.8-27B Uncensored oQ8e bf16 MTP, Qwopus3.8-27B-MTPLX, Huihui Claude-4.6-Opus abliterated, Llama-3-Groq-8B-Tool-Use, MiMo-V2.6-Distill-Qwen-9B OptiQ-4bit, plus two generic-named sessions (mlx-4bit, clef-flash-4bit).
- Dataset 8091 -> 8151.

## 2026-10-07: oMLX traces batch 27 (+54 rows)

- Next listing-growth sweep (listing now 1,884 IDs, 1,390 candidates fetched, all handled): Qwen3.8-27B oQ6e MTP and 4bit MTP (rapid-mlx), Qwen3.6-35B-A3B nvfp4, MiMo-V2.6-Qwen-9B-MTPLX, Swift Qwen3.8-27b oQ4e/oQ6e MTP, FrogNano-4B-2609 oQ4e MTP, Qwen3-8B 4bit.
- Dataset 8037 -> 8091.

## 2026-10-07: oMLX traces batch 26 (+63 rows)

- Next listing-growth sweep (listing now 1,865 IDs, 1,339 candidates fetched, all handled): Qwen3-VL-30B-A3B-Instruct 4bit, MiMo-V2.6-Distill-Qwen-9B oQ4e/oQ8e, NVIDIA Nemotron 3.5 Lightning 30B-A3B OptiQ-4bit, Ternary-Bonsai-27B 2bit.
- Dataset 7974 -> 8037.

## 2026-10-07: oMLX traces batch 25 (+64 rows)

- Next listing-growth sweep (listing now 1,833 IDs, 1,281 candidates fetched, all handled): Qwen3.6-35B-A3B oQ4e MTP and VQ-5.4bpw and Uncensored-Heretic-MTPLX, K2-Horizon 3.7B/7B, Muse Glimmer 4bit, Gemma 4 E2B, Qwen3-0.6B, Qwen3.8-27B Atlassian-v2-goose and 6bit, Llama-3.1-8B-Instruct, Qwen3.8-Flash-Next-REAP-288.
- Dataset 7910 -> 7974.

## 2026-10-07: oMLX traces batch 24 (+64 rows)

- Next listing-growth sweep (listing now 1,805 IDs, 1,221 candidates fetched, all handled): Qwen3.8-27B OBLITERATED OptiQ-4bit and V3-Sharp oQ4e MTP, DeepSeek-V4.1-Flash oQ3e-2b27-CED MTP, Qwen3.8-27B MLX 8bit, Qwen2.5-Coder-7B-Instruct 4bit, Ornith-1.5-35B-A3B oQ4e MTP, Laguna-S-2.1 oQ6e, Spark-X2.5-4B Abliterated Uncensored.
- Dataset 7846 -> 7910.

## 2026-10-07: oMLX traces batch 23 (+66 rows)

- Next listing-growth sweep (listing now 1,747 IDs, 1,161 candidates fetched, all handled): Qwen3.8-27B oQ4e MTP, Qwen3.8-Flash-Next 4bit base, prism-ml Ternary-Bonsai-2-27B 2bit MLX, plus mapped-model sessions.
- Dataset 7780 -> 7846.

## 2026-10-07: oMLX traces batch 22 (+70 rows)

- Next listing-growth sweep (listing now 1,719 IDs, 1,101 candidates fetched, all handled): Qwen3.8-Flash-Next-Uncensored base builds, DeepSeek-V4-Flash-0731 MXFP4, Qwen3.8-9B-Distill 8bit, Gemma 4 26B-A4B 8bit, Qwen3.5-4B/9B/2B variants (incl. OptiQ and MTP builds), Qwen3.8-27B-Uncensored 4bit.
- Dataset 7710 -> 7780.

## 2026-10-07: oMLX traces batch 20-21 (+212 rows)

- Two listing-growth sweeps (listing now 1,635 IDs, 1,041 candidates fetched, all handled): Qwen3.8-Flash-Next oQ4e/oQ5e MTP and Uncensored 100K MTP, Qwen3.8-27B TURBO-Fable oQ2.7 community merge, Qwen3.8-27B oQ6e/oQ8e MTP builds, Swift-1.5-Qwen3.8-27b oQ8e MTP, Muse-Glimmer-30B, DeepSeek-V4.1-Flash oQ4e MTP, Laguna-S-2.1 oQ4e, GLM-5.3-Flash Alis 6bit, Ornith-1.5-35B-A3B variants, Gemma 4 E4B, Qwen3.6-35B-A3B 4bit.
- Dataset 7498 -> 7710.

## 2026-10-07: vLLM #59916 drift re-sync (10 rows updated)

- Author rewrote the PR body 2026-10-06 with fresh 4x B300 measurements; all 10 GLM-5.3-NVFP4 prefill rows re-synced (e.g. TP1xPCP4 gather DCP4 144.8K -> 146.0K, TP4 gather 61.9K -> 62.2K, PP2xTP2 KVPP 100.5K -> 102.1K).
- force_refresh entry added so CI re-fetches the source; records track the current body.

## 2026-10-07: llama.cpp #24528 +4 rows (GLM-5.3-Flash expert-cache A/B)

- CPU-on-miss expert cache A/B on GLM-5.3-Flash UD-IQ3_XXS, ctx 204800, Threadripper PRO 3975WX (experts on CPU) + 2x RTX 5090: master no cache 18.5, master + #29887 copy cache 12.9, v2 CPU-on-miss 23.7, v2 + DFlash2 n=2 ub 1024 33.5 (3 boots).
- New hardware string: Threadripper PRO 3975WX + 2x RTX 5090.
- Anchored 6 #24528 rows (M3/M1 Pro streaming, 5060 Ti) to their comments, which drifted off the thread's first page.
- Dataset 7494 -> 7498.

## 2026-10-07: vLLM #60296 +2 rows (R9700 fp8 attention A/B)

- fp8 query attention for fp8 KV cache on Radeon AI PRO R9700 (gfx1201), gemma-4-12B-it FP8, TRITON_ATTN: prefill 7.7K prompt 1102 -> 4574 tok/s (4.15x), decode 33.38 -> 36.08 t/s (+8.1%). Baseline arm stored.
- Dataset 7492 -> 7494.

## 2026-10-07: vLLM #60317 +15 rows (A100 gemma-4 prefill A/B)

- Triton unified attention head_dim=512 / SWA optimization: vLLM engine prefill A/B on A100-SXM4-80GB, main vs PR branch, gemma-4-E2B/E4B/12B-it, ctx 2048/4096, batch 1/4/8. Baseline arm stored, PR arm and speedup in notes (1.04x-1.12x).
- New hardware string: A100-SXM4-80GB.
- Dataset 7477 -> 7492.

## 2026-10-07: llama.cpp issues +23 rows (M5 Max depth decay, RTX 5090 Blackwell fix, P100 split-mode)

- #30074: Qwen3.8-Flash-Next IQ3_S on M5 Max, 175K/32K depth-decay table with n-gram spec decodes (26.9-89.4 t/s) plus the mlx-serve 252K reference (53.9 t/s).
- #30077: RTX 5090, Qwen3 8B Q4_K_M, llama-bench tg128 A/B of the CUDA 12.8 q4_0/q5_0 V-dequant stack-frame fix (master vs branch, q4_0 and q8_0 K/V caches, 4 depths).
- #30075: 2x Tesla P100, Qwen3.6-35B-A3B split-mode degeneration report (~130 t/s normal, ~36 t/s with MTP, approximate).
- Dataset 7454 -> 7477.

## 2026-10-07: oMLX traces batch 19 (+148 rows)

- Final known-corpus sweep (921 candidates now, listing still growing): Qwen3.8-27B TURBO-Fable oQ3.5, Qwen3.8-27B MPTLS FP16 builds, Tiel-Coder-35B-A3B oQ6e MTP, gemma-4-26B-A4B heretic mixed 4+6bit, and more.
- Dataset 7306 -> 7454. All 915 corpus traces fetched and mined; new traces will appear as the listing grows.

## 2026-10-07: oMLX traces batch 18 (+156 rows)

- Next 60 of the corpus mined (October-dated: KAT-Coder-V2.5-Dev, Tiel-Coder-35B-A3B, Nex-N2.5-mini-Uncensored, dsv4-flash-vision-exp, GLM-5.3-Flash Alis 6bit, Qwen3.6-27B 8bit, gemma-4-12b-it, plus MTP/abliiterated community builds).
- Dataset 7150 -> 7306.

## 2026-10-06: oMLX traces batch 17 (+188 rows)

- Next 60 of the corpus mined (October-dated: DeepSeek-V4-Flash-0731 oQ4e MTP, MiMo-V2.6-Distill-Qwen-9B oQ4e/oQ6e, MiniCPM5-2B oQ4e, Ornith-1.0-9B 8bit, Qwen3-Next-80B-A3B-Thinking-Uncensored, Qwen3.6-27B 4bit, Qwen3.8-27B MTP variants, clef-flash 8bit).
- Dataset 6962 -> 7150.

## 2026-10-06: oMLX traces batch 16 (+180 rows)

- Next 60 of the corpus mined (October-dated: Qwen3.6-35B-A3B Genesis-Hermes dequant oQ8e MTP, Qwen3.8-Flash-Next oQ4/oQ6e MTP, DeepSeek-V4-Flash-0731 mxfp4 abliterated).
- Dataset 6782 -> 6962.

## 2026-10-06: oMLX traces batch 15 (+170 rows)

- Next 60 of the corpus mined (October-dated traces: DeepSeek-V4-Flash-0731 oQ8e MTP, Qwen3.6-35B-A3B in 4bit/mxfp4/oQ4-MTP/oQ8e-MTP, Qwen3.8-27B mxfp4, gpt-oss 20B MXFP4 variants, gemma4 E4B OptiQ).
- Dataset 6612 -> 6782. Contradiction count rose to 201 as same-model/same-chip sessions from different community builds and prompts land in shared groups; all reviewed as honest variance.

## 2026-10-06: oMLX traces batch 14 (+180 rows)

- Next 60 of the corpus mined (October-dated traces, e.g. Bonsai-27B 1bit, Ornith-1.5-35B-A3B 4bit, Qwen3.5-27B 4bit on M5 Max 128 GB).
- Dataset 6432 -> 6612.

## 2026-10-06: oMLX traces batch 13 (+178 rows)

- 99 leftover candidate traces mined (no new fetch needed): community builds of Ornith-1.5-35B-A3B (BigBang MTP, oQ6e MTP), LFM2.5-8B-A1B, Qwen3.8-Flash-Next-REAP-288 (oQ4e, MTP+PLE), Qwen3.5-122B-A10B 6bit, gemma4 26B.A4B QAT, and more.
- Dataset 6254 -> 6432.

## 2026-10-06: oMLX traces batch 12 (+190 rows)

- Next 60 of the corpus mined; the crawl has now reached today's traces (2026-10-06, e.g. Qwen3.8-27B oQ8e MTP on M3 Max 128 GB), so the March-to-present sweep is nearly complete.
- Dataset 6064 -> 6254.

## 2026-10-06: oMLX traces batch 11 (+252 rows)

- Next 60 of the 915-trace corpus (March 9 era) mined: 151 traces, 252 rows. New models HY-MT1.5-1.8B, Qwen3-VL-8B-Instruct, Qwen3.5-2B-Claude-4.6-Opus-Reasoning-Distilled.
- Dataset passes 6000 measured rows: 5812 -> 6064. Drift watch (vllm-59916/59973/60226, Gyro) all green.

## 2026-10-06: oMLX traces batch 10 (+279 rows)

- Next 60 of the 915-trace corpus (March 9 era) mined: 161 traces, 279 rows on M4 Pro, M5, M1/M2. New models Qwen3.5-2B, Qwen3.5-4B-OptiQ.
- Dataset 5533 -> 5812.

## 2026-10-06: oMLX traces batch 9 (+289 rows)

- Next 60 of the 915-trace corpus (March 9 era) mined: 180 traces, 289 rows on M1 Max, M4, M5, M2/M3. New models Llama-3.2-3B-Instruct, Qwen3.5-35B-A3B-Heretic, GLM-4.7-Flash, Gemma 3 4B QAT build.
- CI hardening: quote-verification fetches now retry 429s with backoff (was failing on cold-cache bursts from omlx.ai).
- Dataset 5244 -> 5533.

## 2026-10-06: oMLX traces batch 8 (+265 rows)

- Next 60 of the 915-trace corpus (March 8-9 era) mined: 193 traces, 265 rows on M4, M5, M1/M2 Max, M3/M4 Pro. New models Qwen2.5-Coder-14B-Instruct, Qwen3-Coder-30B-A3B-Instruct; small models Qwen3.5-0.8B/4B, Qwen3.5-35B-A3B, GLM-5 4.8bit.
- Dataset 4979 -> 5244.

## 2026-10-06: oMLX traces batch 7: corpus catch-up (+246 rows)

- Listing crawl shows the oMLX corpus is 915 traces; fetched and mined the oldest 261 (March era): M3 Ultra 60c 256 GB, M2 Ultra, M2 Max, M5, M4 sessions with Qwen3.5-27B, Qwen3.5-397B-A17B, Qwen3.6-35B-A3B-Uncensored-Heretic, Qwen3.8-27B Abliterated/MLX-4bit/TensorFold, Qwen3.8-27B-TURBO-Fable merge (oQ3, new model), Qwen3.8-Flash-Next-Uncensored mixed mxfp4+mxfp8 MTP, GLM-5.3-Flash oQ4e, MiniCPM5-2B, clef, gpt-oss 20B 8bit, MiniMax M2.5.
- Known-bug fix: known.txt is now derived from mined record ids instead of accumulating all listing ids.
- Dataset 4733 -> 4979.

## 2026-10-06: oMLX traces batch 6: March corpus middle (+67 rows)

- Collector pagination fixed: the SSR next-cursor is the base64 link without a trailing "prev" tag; following it reaches the full corpus (146 traces) instead of two wrapped pages. Mined the newly reachable March sessions on M3 Ultra (80c) 512 GB, M2 Max 96 GB and M2 Ultra 128 GB: Qwen3-Coder-Next, Qwen3.5-122B-A10B (4bit/8bit), Qwen3.5-27B-Claude-4.6-Opus-Distilled (new model), Qwen3.5-9B MXFP4, GLM-5 second session, gpt-oss 120B (4bit/8bit/MXFP4-Q8).
- Dataset 4666 -> 4733.

## 2026-10-06: oMLX traces batch 5 (+9 rows)

- 4 more unique oMLX sessions (9 rows): Ornith-1.5-35B-A3B NVFP4 on M4 Max (4 collapsed sessions), Qwen3.5-122B-A10B oQ6e-mtp second M5 Max session, Qwen3.6-35B-A3B oQ6-mtp second M1 Max session, Qwen3.8-27B oQ4e-mtp on M1 Max 24c.
- Dataset 4657 -> 4666.

## 2026-10-06: oMLX traces batch 4 (+19 rows)

- 7 more unique oMLX sessions (19 rows): Qwen3.5-122B-A10B oQ6e-mtp on M5 Max, Qwen3.6-35B-A3B oQ6-mtp on M1 Max (2 sessions), Qwen3.8-35B-A3B-Distill oQ6e-mtp on M4 Pro (new model), Qwen3.8-27B oQ8e-mtp on M3 Ultra 256 GB, oQ4e-mtp on M4 Pro 48 GB, orcarouter Uncensored build on M4 Pro (4 sessions collapsed to 1), Qwen3.5-9B on M1 Pro 16 GB.
- Dataset 4638 -> 4657.

## 2026-10-06: oMLX traces batch 3 (+13 rows)

- 6 more unique oMLX sessions (13 rows): GLM-5.3-Flash 4bit-MTP on M5 Ultra 256 GB (85.6 tok/s tg at 32k), Qwen3.8-27B oQ4e-mtp on M5 Ultra 96 GB (96.9 tok/s at 32k), Qwen3.8-Flash-Next oQ4e on M3 Ultra 256 GB and oQ5e repeat runs at 195k on M5 Max (45.2-49.4 tok/s), Qwen3.8-27B oQ8e second M3 Max session, mlx-community 4bit on M2 Max 64 GB.
- Dataset 4625 -> 4638.

## 2026-10-06: oMLX traces batch 2: fresh 10-06 sessions (+26 rows)

- 11 more unique oMLX sessions (26 rows) from the newest traces: Huihui-Qwen3.8-27B-abliterated Q8 and Qwen3-Coder-Next 6bit on M5 Max, Qwen3.8-27B oQ4e-fp16/oQ8e/8bit MTP builds on M1 Ultra/M3 Max/M5 Pro, Qwen3.8-Flash-Next oQ5e-mtp on M5 Max (195k ctx, 50.0 tok/s), Gemma 4 26B-A4B UD-MLX-3bit on M5 Pro (1958 pp at 4k), Qwen3.5-9B on M4; new models Qwen3.8-27B-MTPLX and Qwen3.8-27B-Uncensored.
- Dataset 4599 -> 4625.

## 2026-10-06: oMLX community benchmark traces (21 rows, new source)

- New source: oMLX community performance traces (omlx.ai/benchmarks/performance), first collector `~/ghost/omlx/omlx_scan.py`. 21 rows from 4 unique sessions on M3 Ultra (80c) 512 GB (new backend oMLX): Qwen3.5-122B-A10B 4bit (6 ctx points, tg 52.3 at 1k), Qwen3.5-397B-A17B 6bit (tg 28.5 at 1k), MiniMax M2.5 8bit (tg 34.2 at 1k), GLM-5 4bit (tg 16.6 at 1k); duplicate traces of the same session noted per row.
- Dataset 4578 -> 4599.

## 2026-10-06: HF card RolanDorisTech Qwen3.8-9B-Distill MLX quant ladder (4 rows)

- RolanDorisTech/Qwen3.8-9B-Distill-MLX-8bit card: community distill of Qwen3.8-2.4T-A95B into the Qwen3.5-9B architecture, oMLX dynamic quantization ladder (oQ4e/oQ5e/oQ6e/oQ8e) measured on M1 Max 64 GB: 43.0 / 37.1 / 33.3 / 28.7 gen tok/s with peak memory 5.471-9.679 GB (new model).
- Dataset 4574 -> 4578.

## 2026-10-06: vLLM #59973 body rewrite re-sync (+1 row)

- The author rewrote the vLLM #59973 body (quantized draft lm_head, Qwen3.8-Flash-Next NVFP4 + MTP k=3, one GB10). Re-synced the 3 dependent records to the current ABBA same-node table: stock BF16 draft head 35.6 tok/s c=1 and 27.2 c=4, NVFP4 draft head 30.4 c=4, and added the NVFP4 c=1 row (45.2 tok/s, +27.1%). FP8 arms are published relative-only and stay in the A/B note.
- Dataset 4573 -> 4574.

## 2026-10-06: vLLM #60250 + #60248, ROCm norm fusion and Kimi-K3 stream overlap (4 rows)

- vLLM #60250 (sourced): `rms_norm_gated` custom op enabled by default on ROCm for unquantized models; Qwen3.8-27B BF16 on a single MI355X, `vllm bench serve` random 1024/1024 c=64, output throughput 2752.5 -> 2762.8 tok/s (+0.37%), median TTFT 1074.2 -> 1084.0 ms. 2 rows, 1 A/B group.
- vLLM #60248 (sourced): Kimi-K3 ROCm stream overlap (MoE router with routed down-projection, MLA frontend with output gate), decode-gated to at most 128 tokens; p90 interactivity 163.94 -> 172.89 tok/s (+8.95) on a single MI355X over a 60-minute scored comparison. 2 rows, 1 A/B group.
- Dataset 4569 -> 4573.

## 2026-10-06: megathread build tokenization (contradictions 220 -> 114)

- Tokenized the llama.cpp performance megathreads (#10879 Vulkan, #15013 CUDA, #15021 ROCm, #23313 SYCL, #4167 Apple Silicon) with the llama.cpp build number each post reports (the `build: <commit> (NNNN)` line), added as `config=bNNNNN` tokens on 1296 rows. Same-model-different-build rows no longer masquerade as contradictions; the remaining 114 flags are same-build variance or posts without a stated build.
- The build tokens also form per-(chip, model) build-progression tables on the Build A/B notes page (353 -> 562 groups, 3194 records).
- Contradiction flags 220 -> 114, outlier flags 14 -> 7 (no record-count change).

## 2026-10-06: llama.cpp #30051, FA-on prompt-processing cliff on Google Axion (6 rows)

- llama.cpp issue #30051 (community): Gemma 4 E4B Q4_0 pp-only llama-bench on a Google Axion CPU (Neoverse V2 with SVE2, new hardware), llama.cpp b11443. With flash attention on, going from 63 to 64 queries makes prefill slower (126.69 -> 91.37 t/s at 8 threads, 247.07 -> 135.10 at 16) because from 64 queries the tiled FA path runs the scalar simd_gemm fallback (SVE builds are excluded from the generic kernel); with FA off the same step is faster (121.03 -> 129.01). 6 rows, 1 A/B group with note.
- Dataset 4563 -> 4569.

## 2026-10-06: vLLM + llama.cpp performance PRs (Blackwell, ROCm, Hopper, Metal, Vulkan) (155 rows)

- Overall 2026-10-06 work (this and the four entries below): dataset 4321 -> 4563, quote-verified 4882 -> 5212.
- vLLM #60226 (community, SPEED-Bench harness): context-aware sparse NVFP4 lm_head baseline on GB10, Qwen3.6-35B-A3B NVFP4 + MTP k=3 with FP8 KV; stock NVFP4-head decode 117.8 tok/s at c=1 and 73.4 at c=4 (PR arms published as +7.7%/+3.7%). 2 rows, 1 A/B group.
- vLLM #60220 (sourced): FlashMLA sparse fp8 workspace staging enables MNBT=32K serving on 8xH100 (new hardware), GLM-5.3-Flash FP8, total tok/s from vllm bench serve. 8 rows.
- vLLM #60216 (sourced): ROCm fused AITER MonoKernel GLM-5 sparse-layer decode on 8x MI355X (new hardware); c16 rows document the crossover. 12 rows.
- vLLM #60187 (sourced): K-EXAONE-236B-A23B MTP RoPE bugfix on 16x A100-SXM4-40GB (new hardware). 4 rows, 1 A/B group.
- vLLM #60161 + llama.cpp #30035 + #30036: 92 rows (gather-DCP re-measure, Qwen3.5-family generation/prompt sweeps across backends); A/B notes.
- vLLM #60159 (sourced): Kimi-K3 native merge_attn_states on 8x MI355X, 4 rows. #60158: DiffusionGemma-26B-A4B on B300, FA4 hd512 vs Triton, 2 rows. #60153: gfx942 mHC seam kernel on 4x MI325X (new hardware), DSV4.1-Flash off/on A/B, 4 rows. #60122 unparked: DeepSeek-V3.1 on 4x NVIDIA GB300 (new hardware), batch-invariant TRITON_MLA vs main, 4 rows.
- llama.cpp #30048: Strix Halo Vulkan 2M-ctx prefill, Qwen3.5-2B UD-Q4_K_XL 213.69 t/s at 1M tokens, 1 row. #30047: Metal few-row MMA MUL_MAT_ID, Qwen3.6-35B-A3B Q4_K_M on Apple M3 Ultra, seq 1-16 (flat to seq8, +7% at seq16), 12 rows, 1 A/B group. #30042: glm5-next gather-path removal on RTX PRO 6000, 6 rows. #30039: Vulkan RDNA1 gfx1010 prompt-processing regression on RX 5700 XT, 2 rows. #30033: 2x Intel B70 (new hardware) Qwen3.8-Flash-Next UD-IQ3_XXS, PR #29622 regression A/B, 2 rows.
- New hardware: 8x MI355X, 8xH100, 16x A100-SXM4-40GB, 4x MI325X, 4x NVIDIA GB300, 2x Intel B70.

## 2026-10-06: Hugging Face cards (REAP expert pruning, quant A/B, MTP) (61 rows)

- kueizen Marco REAP expert-pruning sweeps (Marco-Mini-Instruct, Marco-Nano-Instruct), 18 records; kueizen Qwen3.6-35B-A3B-REAP-GGUF sweep on RTX 3090, 9 rows.
- local-inference-lab GLM-5.3-Flash vLLM card on 2x RTX PRO 6000 Blackwell Max-Q (new hardware), c1/c8 decode with MTP k=3, 2 rows.
- firetussin Qwen3.8-27B-pi RCO allocation-transfer quant A/B on A100 PCIe 80 GB (new hardware), IQ3_XXS vs IQ2_M, 2 records.
- ddalcu Qwen3.8-Flash-Next mlx-serve mixed 4/8-bit pack on M4 Max 128 GB (serial 60, MTP 78, prefill 730), 3 rows.
- AEON-7 Qwen3.6-27B merge on M4 Pro 48 GB (FP4/8-bit/MTP sweep) and Dankpaws Swift 1.5 Flash-Next on M5 Ultra (mlx-serve vs IQ3_XXS), 20 rows.
- Schiltmans DFlash2-ft5 drafter card on M4 Pro Metal (6 rows) + Sakura ISTA-Darwin-R3 (1 row); dropped 19 duplicates of already-mined webmp3 cards.

## 2026-10-06: llmcheck.net re-sync to v2026-10-05 (net -97 rows)

- Endpoint moved to /data/benchmarks.json (new single-array format with a per-row provenance field); quotes regenerated from the new format.
- Re-sync reclassified rows between measured and estimated (moving estimates to reference/), dropped duplicate rows, and re-synced drifted values. Net effect on the measured record set: -97 rows.
- GPT-oss 20B on M6 reclassified estimate -> community (HDZucht source); Muse Glimmer 30B M6 reclassified estimated -> measured.

## 2026-10-06: historical llama.cpp discussion mining (123 rows)

- #29964 pipeline-parallel MoE patch on 3x RTX PRO 4000 Blackwell (Qwen3.8/DeepSeek-V4-Flash/MiMo bisect + ncmoe + noise checks), 20 rows; plus eapache 4500+3060 -ncmoe 1:1 A/B.
- #29885 MoE expert-residency prefill A/B on GTX 1080 (265 vs 30 tok/s), 2 rows.
- #29643 SYCL Arc B580 XMX (9 rows) plus a plain-decode 26.4 t/s at 115K clarification; #29861 cross-backend NPU splits (4); #29531 focus-llama DA (2); #29662 Ghostlink RPC (1).
- #29037 FiTuna autotune (6), #29387 DFlash2 spec-dec on L4 (8), #29253 RPC graph cache (6), #29249 Sarge 4070LP (2), #29072 780M MMVQ (2).
- KVMem 256K (2), Bosgame M5 Flash-Next tuning (20, new hardware), 400k-ctx 5060 Ti (1), NVFP4 5090 PoC (9), 4-GPU WDDM (4), expert-pool 4080S (14).
- #29621 xyz-llama fork on RTX 4070 Ti SUPER (4 rows, xyzkv2/XYZ_ENGINE/late-build A/B) and #28766 JigSawPT DSV4.1 port on RTX 5090 expert streaming (4 rows incl. measured ceilings).

## 2026-10-06: megathread config tokenization (contradictions 542 -> 220)

- Tokenized ngl/fa/config settings on 254 megathread #10879 rows and 157 rows from #4167/#15013/#15021/#23313, so same-model-different-config rows stop being flagged as contradictions.
- Fixed 12 as-published placeholder records in #4167 (model Llama 2 7B, OP-table quotes, fa/build config tokens); set batch=npl on 24 lc-29779 and the lc-29768 sequence-sweep rows; added distinguishing config tokens (control/nmax5, think/notthink, sparse/dense, cpu-mtp-final).
- Contradiction flags 542 -> 220 (no record-count change).

## 2026-10-05: source deletion, GenerelSchwerz MTP + zekrom KV matrix (13 rows removed)

- Both source comments were deleted by their authors (they had been hidden in the UI since 2026-10-05 22:50 and are now gone from the REST list too): llama.cpp discussion #24528 comment 18532257 (GenerelSchwerz MTP draft-placement sweep on RTX 5070 Ti, 7 rows) and #20969 comment 16399706 (zekrom-vale Cydonia-24B v4.3 KV matrix on 5070Ti, 6 rows).
- Records and their two A/B notes removed per the drift policy (a record must stay verifiable against its source). The "5070Ti" hardware page and the Cydonia-24B v4.3 model page had no other records and are gone.
- Dataset 4334 -> 4321, quote-verified 4895 -> 4882.

## 2026-10-05: HDZucht Mac mini M6 benchmark repo (11 rows)

- New source: github.com/HDZucht/Mac-Mini-M6-LLM-benchmarks, a 16-model decode sweep on a 32 GB Mac mini M6 (LM Studio / MLX / Splash engines, 3 runs per cell, prose/code/JSON prompt types).
- Mined 11 rows: Splash speculative-decoding arms (Qwen3.6-35B-A3B-Splash 69.6 prose EN up to 234.1 JSON, Ornith-Splash 61.5, Qwen3.8-27B-Splash 20.2 up to 67.7), GGUF baselines (Ornith 43.7, Qwen3.8-27B 11.8), Nemotron-3-Nano-Omni flat 45 tok/s, Nemotron-3.5-Lightning UD-Q3_K_XL 42.3, Qwen 3.5 9B MLX 30.3, and the AREX-2 fine-tune A/B: 6.8-8.0 tok/s under LM Studio vs 22-37 under Splash with the base-model DFlash2 draft (3-5x on a fine-tune, draft matched by architecture).
- New backend string "Splash"; new models Qwen3.6-35B-A3B-Splash, Ornith-1.5-35B-A3B-Splash, Swift-Qwen3.8-27B, Nemotron-3-Nano-Omni, AREX-2. Values stored at the prose EN column with the full published spread in the notes.
- Dataset 4323 -> 4334, quote-verified 4884 -> 4895.

## 2026-10-05: llmcheck re-sync, M6 Mac Mini batch (10 rows)

- llmcheck.net reclassified 8 entries from estimated to measured and added 2 new ones. Mined 10 measured rows: first M6 Mac Mini numbers (Qwen3.6-35B-A3B 4-bit MLX 64 tok/s, Nemotron-3.5-Lightning Q4_K_M llama.cpp 45, Gemma 4 26B-A4B QAT 48, Gemma 4 12B QAT 19, Gemma-4-31B QAT 8, muse-glimmer 30B 9, gpt-oss 20B 45, all LM Studio on 32 GB M6), Qwen3.6-35B-A3B 4-bit on M5 Max 128 GB (126 tok/s, omlx.ai), and Qwen 3 30B-A3B 4-bit on M4 Max 128 GB from arXiv 2601.19139 (MLX 110 vs llama.cpp 90 tok/s).
- Dataset 4313 -> 4323, quote-verified 4882 -> 4884.

## 2026-10-05: Lidenburg expert-cache fork, 12 GB VRAM arms (4 rows)

- The moe-expert-caching README benchmark table was rewritten and now names the test machine (RTX 5080 PCIe Gen 4, Ryzen 3900X) for the previously parked 12 GB VRAM rows. Mined 4 rows: Qwen3.6-35B-A3B 66 tok/s cached vs 40 stock (+65%), Qwen3-Coder-Next 27 vs 17 (+58%, disk tier active at 55/402/55 experts). Both A/B notes extended with the 12 GB arms.
- Dataset 4309 -> 4313, quote-verified 4878 -> 4882.

## 2026-10-05: webmp3 Sakura expert-pruned cards on Strix Halo (20 rows)

- Five webmp3 Hugging Face cards measured on a 64 GB AMD Strix Halo (Radeon 8060S, Windows):
  - Sakura-Qwen3.8-Flash-Next-Swift 3-bit (IQ3_XXS) and 2.5-bit (IQ2_XS): shared MTP sidecar on a fork build lifts decode from about 21 -> 34.5 (+64%) and about 24 -> 37.6 (+57%) tok/s; IQ2_XS beats IQ3_XXS because its ~26 GiB resident weights fit the dedicated carve-out; on ROCm IQ3_XXS collapses to about 5 tok/s while IQ2_XS still does 21.6. 10 rows.
  - Sakura-Qwen3.8-Flash-Next-ISTA-Darwin-R3 (31.4/236 with MTP) and ISTA base cut (22.7/186 official Vulkan, ROCm collapse about 4.9). 3 rows.
  - Sakura-MiMo-V2.6-Flash-MOPD-P160 (IQ2_XS) with MiMo SSD Streaming: context sweep 16k/24k/32k (9 -> 6.6 -> 5.6 tok/s low end of published ranges) and ubatch sweep ub512/1024/2048 (decode 9.6 -> 5.9 while prefill 12.7 -> 22.3); full 512-expert MiMo-V2.6-Flash-RL reference pages from NVMe at 2.6 tok/s. 7 rows. 2 A/B groups with notes.
- Dataset 4289 -> 4309, quote-verified 4858 -> 4878.

## 2026-10-05: GCN MMQ retune + Arc B580 regression bisect + Kimi-K3 GEMM fold (56 rows)

- llama.cpp PR #30021 (community), GCN MMQ config re-tune on an A800M: pp2048 prefill master-vs-PR by ub, 48 rows. Q8_0 Granite 3.0 3B ub16 345.34 -> 613.21 (+77.6%), IQ4_XS ub16 +8.9% and ub48 +20.0%, IQ4_NL Llama 3 8B ub16 +12.2% / ub48 +11.5%; flat elsewhere. 2 A/B groups with notes.
- llama.cpp issue #30018 (community), decode regression bisected on Intel Arc B580 (Vulkan): #29622 costs Gemma 4 E4B Q4_0 5.0% decode (90.7 -> 86.2) while lifting prefill +3.8% (3323 -> 3449); bisect points isolate the single commit; Qwen3 14B control arm unaffected at 40.0 both sides. 6 rows, 2 A/B groups with notes.
- vLLM PR #60110 (sourced), Kimi-K3 on 8x MI355X (AITER, InferenceX agentic c14): folding q_b_proj + W_UK into one GEMM lifts output throughput 685.62 -> 702.87 tok/s (+2.5%) at unchanged gsm8k. 2 rows, 1 A/B group.
- Parked: vLLM #60122 (benchmark GPUs not named, only CUDA_VISIBLE_DEVICES).
- Dataset 4233 -> 4289, quote-verified 4802 -> 4858.

## 2026-10-05: Source drift re-sync, llmcheck + Gyro card + vLLM #59973 (net -19 rows)

- llmcheck.net re-sync: the live benchmarks.json moved again (196 values updated, 37 entries removed from the site, 23 new entries added). Records now mirror the current 244-entry JSON exactly.
- Gyro card re-sync: agentionai rewrote the Qwen3.8-Flash-Next-Gyro-GGUF speed section. 19 rows whose values the card dropped were removed (2x R9700 split, 5090 content/ctx-fill series, 8060S AP-Q4_K_XL and MTP off-arms, R9700 copy arms); 16 rows re-quoted to the new table; the Strix Halo rows move to hardware "AMD Strix Halo" (the card no longer names the 8060S); new Strata Gyro-M prose row (114 tok/s). A/B notes rewritten.
- vLLM #59973 re-sync: PR body rewritten again. c=1 stock 35.6 -> 35.7, c=4 stock 26.0 -> 25.9, NVFP4 c=4 29.4 -> 29.6 tok/s; the FP8 c=4 arm lost its absolute value (measured against a different node) and was removed. Note rewritten.
- Dataset 4252 -> 4233, quote-verified 4835 -> 4802.

## 2026-10-05: vLLM #59916 third drift, records track the re-measured table (0 new rows)

- The PR body was rewritten for the third time: gather-DCP rows re-measured (PP2xTP2 101.4 -> 101.7K, TP1xPCP4 142.3 -> 144.8K, TP4 61.7 -> 61.9K tok/s; author notes ~1% day-to-day variation).
- Wayback pinning was attempted but archive.org and archive.ph both refused (rate limit / timeout). Decision: records track the author's current published numbers, with the revision recorded in each note; the A/B note regenerated from the new values.
- Cache entry for the PR page was force-refreshed; quote-verified 4835.

## 2026-10-05: llama.cpp discussion #20969, Defilan 5060 Ti + seanrasch 256K + AmesianX DGX Spark (13 rows)

- llama.cpp discussion #20969 (community), three more measured posts.
- Defilan, 2x RTX 5060 Ti (SM 120) with the animehacker fork, 8K ctx, 4 concurrent: Ampere-tuned kernels on Blackwell cost ~5x decode on every model (Llama 3.1 8B 50 -> 8.4, Qwen 2.5 14B 28 -> 5.3, Qwen 2.5 32B 14.3 -> 5.5 tok/s with tq3_0 KV); VRAM crossover at 32K. 6 rows.
- seanrasch, dual EVGA RTX 3080 Ti 12 GB, Qwen3.5-9B Q4_K_M turbo2 KV: native 256K context runs with decode flat at ~105 tok/s from 128K to 256K while prefill falls 2027 -> 1423 tok/s; 10 GB VRAM still free at 256K. 3 rows.
- AmesianX, DGX Spark (SM 121): turbo KV *faster* than q8_0 on Blackwell decode (50.1 -> 63.5 tok/s on Qwen3.5-35B, opposite sign of the spiritbuun fork on RTX 5090); tbqp3/tbq3 prompt processing 94 -> 80 tok/s on Qwen3.5-27B i1-Q3_K_M with the native build. 4 rows. 6 A/B groups with notes.
- Parked: sjoerdmaessen 16412852 (hardware only as "same hardware"), primoco 16423353 (no hardware named).
- Dataset 4239 -> 4252, quote-verified 4822 -> 4835.

## 2026-10-05: llama.cpp discussion #20969, zekrom-vale 5070 Ti + Madreag CUDA fork (42 rows)

- llama.cpp discussion #20969 (community), two more measured posts.
- zekrom-vale, RTX 5070 Ti + Cydonia-24B v4.3 IQ4_XS at 16K (llama-bench pp2048/tg128): full q8_0/turbo3/turbo4 K/V matrix, all within ~2.5% of the q8_0 baseline 2670.64/56.28; turbo4-K + q8_0-V saves ~340 MiB at PPL 4.97 vs 4.94; V quantization hurts perplexity more than K on this model. 6 rows, 1 A/B group with note.
- Madreag/turbo3-cuda release/cuda-optimized, base-fork vs optimized-fork A/B across 4 GPUs (llama-bench tg128 at depth): RTX 5090 + Qwen 3.5 27B Q6_K, turbo2 beats q8_0 by +5.4% at 32K (58.61 vs 55.60) at 7.5x compression, kernel rewrite alone worth +13-46% (8 rows); RTX 3090 + Qwen 3.5 9B Q8_0, turbo4 32K 35.63 -> 60.28 (+69%, largest gain), 12 rows; RTX 4090M, turbo4 32K 34.5 -> 52.4 (+52%), 8 rows; RTX 3090 Ti (OC), turbo2 81.58 at 32K beats q8_0 77.44 and reaches 72.79 at 64K where q8_0 OOMs, 8 rows. Short-context decode identical across all KV types (weight-loading bound); differences appear only at 32K+ depth. 4 A/B groups with notes.
- Dataset 4197 -> 4239, quote-verified 4780 -> 4822.

## 2026-10-05: llama.cpp discussion #20969, TurboQuant KV-cache throughput batch (29 rows)

- llama.cpp discussion #20969 (community): three measured throughput posts from the TurboQuant thread, all llama-bench pp512/tg128 on llama.cpp CUDA forks.
- sztlink, RTX 4090 + Qwen3-30B-A3B Q4_K_M (AmesianX v1.2.0): baseline KV sweep f16 1130.8/225.9, q8_0 1132.8/223.2, q4_0 1087.8/211.0 pp/tg tok/s (tbq KV types not benchable in that build). 3 rows.
- WaveboSF, RTX 4090 + i9-14900K + Llama 3.1 8B Q4_K_M (spiritbuun fork): FA build flags worth +7.4% prefill (9365 -> 10060 pp512); q8_0-K + turbo4-V is the best KV config, +8.4% prefill at -6.2% decode (10903/140.0); symmetric turbo3/turbo4 cost 14-17% decode. v2 build adds layer-adaptive mode which *raises* decode (q8_0+turbo4 136.4 -> 139.8). 13 rows.
- WaveboSF, RTX 5090 + 9950X3D + Llama 3.1 8B Q4_K_M: Blackwell handles TurboQuant decode far worse than Ada, q8_0+turbo4 -29.4% vs -6-9% on the 4090, symmetric turbo3 -45.6%; CUDA 13.2 sm_120a identical to 12.8 sm_120. 10 rows. 3 A/B groups with notes.
- Dataset 4168 -> 4197, quote-verified 4751 -> 4780.

## 2026-10-05: TurboQuant KV quantization evaluation on M1 Pro (3 rows)

- devYRPauli/turboquant-m1pro-evaluation README (community): corrected 2026-10-05 speed table, MacBook Pro M1 Pro 16 GB, Qwen2.5-3B-Instruct at 16K context. 4-bit MLX with FP16 KV: 2.0 tok/s effective (39.9 s wall); with Hybrid K5/V4 quantized KV: 1.1 tok/s (71.4 s wall, -45%). The quantized cache is only 1.29x smaller than FP16 as stored (one byte per element, not packed bits) and peaks 168.6 MB higher because dequantized K/V returns float32. Ollama Q4_K_M GGUF reference on the same page: 37.5 tok/s decode-only, 49.3 s wall. 3 rows, 1 A/B group with note.
- Dataset 4165 -> 4168, quote-verified 4748 -> 4751.

## 2026-10-05: vLLM PR #60091, host-sync removal in ROCm sparse prefill on MI350X (2 rows)

- vLLM PR #60091 (sourced): passing output_size to repeat_interleave in combine_topk_swa_indices removes 160 host syncs per prefill step on gfx950. MI350X TP=4 with expert parallelism, DeepSeek-V4.1-Flash, means of 3-5 reps with interleaved rotated arms and disjoint ranges: prompt 31,440 -> 32,443 tok/s (+3.2%), aggregate output at concurrency 64 1,717 -> 1,763 tok/s (+2.7%), median TTFT at conc 1 340.7 -> 321.1 ms, TPOT 33.34 -> 32.47 ms. About 20 ms saved per prefill step. 2 rows, 1 A/B group with note.
- Dataset 4163 -> 4165, quote-verified 4746 -> 4748.

## 2026-10-05: Lidenburg moe-expert-caching fork README, three-tier expert cache on RTX 5080 (4 rows)

- Lidenburg/llama.cpp moe-expert-caching branch README (community): three-tier GPU/RAM/disk expert cache (LFU with aging, io_uring + O_DIRECT disk tier) vs stock --n-cpu-moe at matched VRAM. RTX 5080 (PCIe Gen 4) + Ryzen 3900X, 32 GB DDR4, slow SATA SSD, 256k ctx, approximate published numbers: Qwen3.6-35B-A3B UD-Q4_K_M ~50 -> ~80 tok/s (+60%), Qwen3-Coder-Next UD-IQ4_XS ~30 -> ~50 tok/s (+66%, needs 28.7 GB pinned RAM). Opposite verdict to mfethe1's RTX 5060 Ti matched-budget test: pinning hot experts in host RAM beats per-miss host reads over PCIe. 4 rows, 2 A/B groups with notes. New hardware: RTX 5080 (PCIe Gen 4) + Ryzen 3900X. The 12 GB VRAM rows in the same table stay parked (GPU not named).
- Dataset 4159 -> 4163, hardware 400 -> 401, quote-verified 4742 -> 4746.

## 2026-10-05: llama.cpp discussion #24528, mfethe1 matched-budget cache-vs-resident on RTX 5060 Ti (2 rows)

- llama.cpp discussion #24528 (community): mfethe1's matched-budget A/B, single RTX 5060 Ti 16 GB + Ryzen 7 3700X, Qwen3-30B-A3B Q4_K_M, same binary (leloch moe-cache branch e3096b0) both arms, ~12.5 GiB VRAM spent on the expert cache or on resident layers. Resident dominates: prefill 149.6 vs 64.0 tok/s, decode 35.4 vs 19.7 tok/s (+80%). The cache arm reached an 85.3% steady-state hit rate with zero evictions and still lost: misses cost full CPU round-trips, hits pay bookkeeping, and cold prefill gets nothing from the cache. 2 rows, 1 A/B group with note.
- Dataset 4157 -> 4159, quote-verified 4740 -> 4742.

## 2026-10-05: llama.cpp discussion #24528, MTP draft placement on RTX 5070 Ti (7 rows)

- llama.cpp discussion #24528 (community): GenerelSchwerz's MTP placement sweep, RTX 5070 Ti 16 GB, Qwen3.8-Flash-Next UD-IQ3_XXS, 1024-token generations, expert-cache size as the pressure knob. Cache64 (draft GPU-resident): no-MTP 59.46 tok/s, MTP1 61.72 (+3.8%), MTP2 60.26 (+1.3%). Cache94 (draft forced to CPU): no-MTP 63.31 (fastest overall), MTP1 49.63 (-21.6%) at nearly identical acceptance. q8_0-KV/q5_1-draft control: 58.26 vs 58.90 (+1.1%). MTP helps only while the draft head stays GPU-resident. 7 rows, 1 A/B group with note. Records use anchored comment URLs; check_quotes verifies them via its REST-API comment fallback.
- Dataset 4150 -> 4157, quote-verified 4733 -> 4740.

## 2026-10-05: llama.cpp discussion #24528, csantiago pp figure + GenerelSchwerz 80k reference run (1 row, 1 update)

- llama.cpp discussion #24528 (community): two follow-ups from GenerelSchwerz's rented-server comments. The csantiago78 reconstruction full-run record gains its published prompt processing figure (30.83 t/s on a 380-token prompt). New row: the earlier 80k-capacity moe-cache run, 10,781 tokens at 65.00 tok/s with 55.89% MTP2 acceptance on 21,000/18,000 MiB cache budgets, above the 256k run (62.02) though flagged uncontrolled by the author. EPYC A/B note extended.
- Dataset 4149 -> 4150, quote-verified 4732 -> 4733.

## 2026-10-05: llama.cpp discussion #24528, moe-cache budget sweep on GTX 1080 Ti (8 rows)

- llama.cpp discussion #24528 (community): batot1's regression test of the leloch moe-cache-pr branch (8853f0535) on a single GTX 1080 Ti 11 GB (sm_61), Qwen3.6-35B-A3B UD-Q8_K_XL, 8k ctx, experts on CPU. Every VRAM cache budget regresses against the hard-disabled cache path: 19.32 tok/s with the cache off, 13.25 tok/s at a 4096 MB budget (-31%), 18.72 tok/s even at 32 MB (-3%). Regression scales with budget size; old Pascal host path makes the pool cost more than the expert fetches it replaces. 8 rows, 1 A/B group with note. New hardware: GTX 1080 Ti.
- Dataset 4141 -> 4149, hardware 399 -> 400, quote-verified 4724 -> 4732.

## 2026-10-05: llama.cpp discussion #28248, persistent VRAM expert pool across two unequal GPUs (6 rows)

- llama.cpp discussion #28248 (community): TmDagger's fix-moe-pool-rail fork, RTX 5070 Ti 16 GB (PCIe 5.0 x16) + RTX 4060 Ti 16 GB (PCIe 4.0 x4), Windows 11, 128 GB DDR4-3200, DeepSeek-V4-Flash-Vision-Exp UD-IQ3_XXS at 262k ctx, all experts on CPU at baseline. Persistent per-device VRAM expert pool (-mec): baseline 5.36 tok/s, -mec 48 both devices 9.09 (+70%), pool on the fast-rail GPU only 6.10, per-device 48/56 9.71, auto-scaled 128/128 (~47/~58 slots) best at 10.32 tok/s decode / 49.5 prefill (+93% vs baseline). Auto-scaling beats hand-picked slots by ~14%; aggressive manual sizing costs ~5% via shared-memory spill. 6 rows, 1 A/B group with note. New hardware: RTX 5070 Ti 16 GB + RTX 4060 Ti 16 GB. New model: DeepSeek-V4-Flash-Vision-Exp.
- Dataset 4135 -> 4141, hardware 398 -> 399, models 208 -> 209, quote-verified 4718 -> 4724.

## 2026-10-05: llama.cpp #29965, Vulkan flash-attention head grouping on Radeon 780M (2 rows)

- llama.cpp #29965 (community): Radeon 780M (gfx1103, RADV Mesa 26.2.4), GLM-4.7-Flash Q4_K_M, 32K context, Vulkan. qk_ratio 20 exceeds the coopmat1 max_gqa of 16 so upstream runs with GQA off and every head re-reads the KV cache: 8.83 tok/s baseline vs 12.91 tok/s with heads grouped to the largest divisor under the limit (+46%), plus a published +15-19% at 8K and unchanged prefill. Group floor of 4 heads: smaller groups drop split_k to 1. 2 rows, 1 A/B group with note.
- Dataset 4133 -> 4135, quote-verified 4716 -> 4718.

## 2026-10-05: llama.cpp #30001, native q8_0-q4_0 FlashAttention kernel A/B (6 rows)

- llama.cpp #30001 (community): RTX 4090, Qwen2.5-7B Q4_0 with q8_0 KV, same-commit A/B of decode vs KV depth. Default build (f16 K/V fallback) vs native q8_0-q4_0 FA kernel: 4k 149.39 -> 163.51 tok/s (+9.5%), 16k 110.87 -> 136.26 (+22.9%), 32k 88.07 -> 110.98 (+26.0%). The penalty scales with cache size; binary cost +0.47 MiB for the single quant pair. 6 rows, 1 A/B group with note.
- Dataset 4127 -> 4133, quote-verified 4710 -> 4716.

## 2026-10-05: llama.cpp discussion #24528 late comments, csantiago78 / simlu expert-cache branches (11 rows)

- llama.cpp discussion #24528 (community): follow-up comments. Volunteer-1's rig (2x RTX 3090 + Ryzen 9950X): csantiago78 PR #27861 branch 49.3 tok/s at 3500 tokens on Qwen3.8-Flash-Next IQ4_XS (new top, above thecodacus 41.2), combined patch set 42 tok/s at 3000 tokens without MTP; simlu branch tg500/tg1000: DeepSeek-V4-Flash UD-Q8_K_XL 13.20/13.12 (matches leloch), Qwen3.8-Flash-Next IQ4_XS-PLEQ4 at 1M ctx 37.7/38.8, GLM-5.3-Flash Q4_K_M 7.72/7.90 (flat with length). Rented server (2x RTX 3090 + 2x EPYC 7663, 640 GB): csantiago reconstruction 39.55 -> 41.01 tok/s as the cache warms over 8513 tokens; GenerelSchwerz moe-cache branch 62.02 tok/s decode / 73.97 prefill at 256k capacity (+51% vs csantiago on the same box). 11 rows, 2 new A/B groups with notes (GLM-5.3-Flash, EPYC 7663 server), 2 existing notes extended. New hardware: 2x RTX 3090 + EPYC 7663.
- Dataset 4116 -> 4127, hardware 397 -> 398, quote-verified 4699 -> 4710.

## 2026-10-05: llama.cpp discussion #24528, expert-caching fork shootout (40 rows)

- llama.cpp discussion #24528 (community): three measured clusters. (1) 2x RTX 3090 + Ryzen 9950X, 192 GB DDR5-3600, Qwen3.8-Flash-Next across 4 quants x 3 KV quants x branches: thecodacus (expert cache + async prefetch + CUDA-pinned host RAM) wins every matchup, IQ4_XS q8_0/q5_1 41.2 vs upstream 26.8 tok/s (+54%), gap widens to +84% at UD-Q6_K_XL with f16 KV (23.6 vs 12.8); TheTom dips below upstream at IQ4_XS/q8_0-q5_1 (24.3 vs 26.8), GenerelSchwerz collapses to 11.9 (MTP regression). 27 rows. (2) Same rig, DeepSeek V4 Flash UD-Q8_K_XL with DSpark MTP: leloch 13.57 vs upstream 6.88 tok/s at 65k ctx (+97%), edge shrinks to +46% at 1M ctx (10.96 vs 7.53); TheTom +85% at 65k, +29% at 1M. 9 rows. (3) Metal on-demand expert loading from disk: Qwen3 30B A3B Q6_K on M3 Pro 36 GB, resident 38.1 tok/s -> 27.5 (-28%) saving 11 GB -> 22.1 (-42%) saving 16.6 GB; runs on M1 Pro 16 GB at 13 tok/s. 4 rows. 3 A/B groups with notes. New hardware: M3 Pro 36GB, M1 Pro 16GB.
- Dataset 4076 -> 4116, hardware 395 -> 397, quote-verified 4659 -> 4699.

## 2026-10-05: llama.cpp discussion #29930, Qwen3.8-Flash-Next 177B expert streaming on RTX 5070 + 32 GB DDR4 (5 rows)

- llama.cpp discussion #29930 (community): Qwen3.8-Flash-Next 177B UD-IQ3_XXS streamed from 32 GB DDR4-2400 on RTX 5070 12 GB + Ryzen 5 5600GT (PCIe Gen3, Windows). The author's hashyy expert-streaming setup (fixed Windows I/O queue depth, one file handle per worker, page-locked hot-expert tier) measures about 11.5 tok/s vs roughly 7 tok/s on the inherited setup (+64%); long coding prompt 4892 tokens at 10.15 tok/s, video-verified 10k-token run at 10.41 tok/s, normal conversation 14-15 tok/s (stored low end). 5 rows, 1 A/B group with note. New hardware: RTX 5070 + Ryzen 5 5600GT.
- Dataset 4071 -> 4076, hardware 394 -> 395, quote-verified 4654 -> 4659.

## 2026-10-05: llama.cpp discussion #29973, MinGW vs MSVC CPU decode collapse on Zen 2 (21 rows)

- llama.cpp discussion #29973 (community): Threadripper PRO 3975WX (Zen 2, 32C/64T, AVX2, 128 GB DDR4-2667), Qwen3.8-Flash-Next 177B UD-Q3_K_XL, pure CPU. Same source tag b11160: MSVC release tg128 6.83 vs MinGW gcc 16.2.0 1.27 tok/s (-81%), ISA-independent (znver2 1.27 vs haswell multi-variant 1.28), prefill barely affected (-5.8%): gcc codegen on the MoE expert-gather decode path. Release builds differ too: cuda12-legacy build CPU-only 35.52/8.87 vs vulkan build 31.46/8.28 (pp/tg). llama-server: -tb 24 lifts long-prompt prefill 41.50 -> 54.46 tok/s; MTP --spec-draft-p-min 0.30 8.94 vs default 8.12 tok/s, p-min 0.50 slower despite 62.1% acceptance, ngram-mod hybrid 8.27, ngram-only 6.86. Thread/affinity sweep: decode peaks at -t 20 (6.83), -t 32 6.21, no-SMT 16-thread masks 6.22, full mask 5.85. Quadro P2000 full offload is a loss: pp 14.36, tg 2.86. 21 rows, 1 A/B group with note (20 rows) + 1 offload row. New hardware: Threadripper PRO 3975WX, Threadripper PRO 3975WX + Quadro P2000.
- Dataset 4050 -> 4071, hardware 392 -> 394, quote-verified 4633 -> 4654.

## 2026-10-05: SaturnHeaven Qwen3.8-Flash-Next RANMA EXL3, host-RAM MoE tiers + emulated 16 GiB card (12 rows)

- HF card SaturnHeaven/Qwen3.8-Flash-Next-RANMA-EXL3-GGUF (community): ranma.cpp (ranma_20261005, HIP/ROCm fork that keeps routed experts in host RAM) on a Radeon AI PRO R9700. llama-bench TG128 warm-cache: EXL3 3.05 bpw 53.5 (128 GB RAM) / 52.4 (64 GB), 4.05 bpw 49.6 / 47.7 tok/s; halving the host RAM pool costs about 2-4 percent. MTP smart decode beats plain decode on every arm (3.05 bpw 53.5 -> 60.8 tok/s low end of the published preset range). RX 9070 XT rows are emulated on the R9700 with the expert cache capped to a 16 GiB budget: 43.2 / 37.0 tok/s, about 18-22 percent below the real card at the same RAM tier; MTP at 4.05 bpw drops to 29.1 tok/s, under the 3.05 bpw arm. 12 rows, 2 A/B groups with notes. New hardware: RX 9070 XT (emulated). New backend: ranma.cpp (ROCm).
- Dataset 4038 -> 4050, hardware 391 -> 392, backends 29 -> 30, quote-verified 4621 -> 4633.

## 2026-10-05: HF cards, Tiel-Coder ROCmFP4 on Strix Halo + Agens-Volundr-32B context decay (7 rows)

- HF card ramon-balaguer/Tiel-Coder-35B-A3B-ROCmFP4-GGUF (community): on a Radeon 8060S (gfx1151, 96 GiB unified, Ryzen AI Max+ 395), the ROCmFPX engine + ROCmFP4 requant runs 86.6 tok/s effective generation over a 17-task code battery vs 69.0 tok/s for stock llama.cpp + DFlash on the UD-Q4_K_XL file (+25%); the native MTP head n2 is 77.4 tok/s; plain decode via llama-swap published as a range, 117-125 tok/s (stored low end). 4 rows, 1 A/B group with note. New model: Tiel-Coder.
- HF card Blockway/Agens-Volundr-32B-Preview-GGUF (community): Q4_K_M on one unnamed 48 GB GPU, -ngl 99 + FA: decode 32.3 (1K) -> 27.4 (8K) -> 25.0 tok/s (32K), prefill 2218 tok/s at 1K but about 620 tok/s at 32K (block selection per prompt token). 3 rows, 1 A/B group with note. New hardware: 48 GB GPU. New model: Agens-Volundr-32B-Preview.
- Dataset 4031 -> 4038, hardware 390 -> 391, models 206 -> 208, quote-verified 4614 -> 4621.

## 2026-10-05: llama.cpp #30006 Mali coopmat + #30000 RTX 5060 Ti Q8_0 Vulkan regression + vLLM #60070 persistent MLA counter (16 rows)

- llama.cpp issue #30006 (community): on a Mali-G925-Immortalis MC12 (Dimensity 9400, Android 16 Termux, llama.cpp 6c59c40), VK_KHR_cooperative_matrix is a ~2.4x prefill pessimization. Qwen3.5-0.8B Q4_K_M, llama-bench -p 512 -n 32: coopmat on pp512 53.30 -> coopmat off 125.78 t/s (+136%), decode unchanged (36.40 -> 36.62); coopmat off + f16 off 117.27, integer-dot off 54.53, host-memory pref 54.04. CPU arm (-ngl 0) pp512 51.19 / decode 2.95, matching coopmat-on GPU prefill (author's hypothesis: coopmat mul_mm fails shared-memory validation at 32 KB and prefill runs at matvec speed). 6 rows (5 Vulkan + 1 CPU), 1 A/B group with note. No new hardware (Dimensity 9400 pre-exists).
- llama.cpp issue #30000 (community, Steve Flaherty): git-bisect on an RTX 5060 Ti 16 GB (NV_coopmat2) pins a Q8_0 Vulkan prefill regression to #25773 (91f6a6cf3): pp512 Qwen3-Embedding-8B 2798 -> 2348 (-16%), Qwen3-Reranker-8B 2790 -> 2337 (-16%), granite-4.2-8b 2955 -> 2437 (-18%); still present at b11425 (-17% to -19%); tg128 granite 41.9 -> 42.1 (unchanged). 8 rows, 3 A/B groups with notes. New models: Qwen3-Embedding-8B, Qwen3-Reranker-8B, granite-4.2-8b.
- vLLM PR #60070 (community, open): persistent FlashInfer multi-CTA-KV counter buffer in sparse MLA decode removes a per-step FillFunctor launch (3,900 -> 0 in the Nsight trace). GLM-5.2-NVFP4 on 4x NVIDIA B200 TP4, BS=1, ISL=4, OSL=2048: output throughput 126.095 -> 132.066 tok/s (+4.7%), TPOT -4.5%, like-with-like on the same FlashInfer build. 2 rows, 1 A/B group with note. New hardware: 4x NVIDIA B200. New model: GLM-5.2-NVFP4.
- Dataset 4015 -> 4031, hardware 389 -> 390, models 201 -> 206, quote-verified 4598 -> 4614.

## 2026-10-05: vLLM #60008 Hybrid Mamba prefix caching (8 rows)

- vLLM issue #60008 (community): Hybrid Mamba prefix caching align mode vs off. Nemotron-3.5-Lightning NVFP4 on 4x GB200 (DP4/EP4), 8K-in/1K-out, median of 6 paired rounds. PC off: 317/2178/7174/10371 tok/s (c=1/8/32/64). PC on: 277/1879/5476/9109 tok/s. 8 rows, 1 A/B group. New hardware: 4x GB200. New model: Nemotron-3.5-Lightning. Dataset 4007 -> 4015, quote-verified 4590 -> 4598.

## 2026-10-05: Gyro card additional data: A6000, CUDA kernel update, Strata rc1 (10 rows)

- agentionai/Qwen3.8-Flash-Next-Gyro-GGUF (community): additional unmined data from the card. RTX A6000: Gyro-S 740 pp2048 / 57.4 decode, Gyro-M 720 pp2048 / 52.3 decode. RTX 5090 CUDA kernel update (2026-10-04): decode 113, MTP JSON 210 / code 180 / copy 218, prefill ~3000. Strata rc1 (new backend): prose 140, JSON 221, code 209 tok/s, prefill 4883 tok/s (16k prompt). 10 rows, 2 new A/B groups. New backend: Strata. Dataset 3997 -> 4007, quote-verified 4580 -> 4590.

## 2026-10-05: Qui-Linta13/Qwen3.8-27B-Uncensored-GGUF IQ2_M spec-decode (3 rows)

- HF model card Qui-Linta13/Qwen3.8-27B-Uncensored-GGUF (community): IQ2_M fused MTP on H200 NVL, -ngl 99, flash attention, F16 KV, 256 gen tokens, median of 3. Baseline (no spec, prose) 75.4 tok/s; MTP n_max 2 (code) 99.8 (+32%); split noMTP-IQ2_M + draft-Q8_0 (n_max 2, prose) 97.7 (+30%). 3 rows, 1 new A/B group with note. New hardware: H200 NVL. Dataset 3994 -> 3997, quote-verified 4577 -> 4580.

## 2026-10-05: vLLM PR #60068 MRV2 confidence stop for autoregressive drafting (5 rows)

- vLLM PR #60068 (community, open): "[MRV2][Spec Decode] Opt-in confidence stop for autoregressive drafting". Qwen3.8-Flash-Next NVFP4, GB10, MTP k=3, SPEED-Bench, one run per arm. Stock 3 drafts (BF16 head) 38.4 tok/s (c=1); fixed 6 drafts (NVFP4 head) 47.0 (c=1, +22%), 31.8 (c=4); confidence stop @0.6 max 6 (NVFP4 head) 51.5 (c=1, +9.6% vs fixed 6), 32.6 (c=4, +2.5%). 5 rows, 1 new A/B group with note. No new hardware/model/backend. Dataset 3989 -> 3994, quote-verified 4572 -> 4577.

## 2026-10-05: vLLM PR #59973 quantized draft lm_head for MTP spec-decode (4 rows)

- vLLM PR #59973 (community, open): "Opt-in quantized draft lm_head for drafters that share the target head". Qwen3.8-Flash-Next NVFP4, GB10, MTP k=3, SPEED-Bench 4 users x 32 prompts, greedy, 256 output tokens, full vocabulary. BF16 draft head (stock) 35.6 tok/s (c=1), 26.0 tok/s (c=4); FP8 draft head +9.0% at c=4 (28.3 tok/s); NVFP4 draft head +13.1% at c=4 (29.4 tok/s). 4 rows, 1 new A/B group with note. No new hardware/model/backend. Dataset 3985 -> 3989, quote-verified 4568 -> 4572.

## 2026-10-05: Gyro HF card drift fix, vllm-59916 PR drift fix

- agentionai/Qwen3.8-Flash-Next-Gyro-GGUF card rewritten: RTX 5090 main table now 2,914 pp2048 / 110 tg128 (was 795/101); content-stratified decode unified to "about 120 tok/s" (was 99/106/101/108); context-fill decay now 111/109/94 (was 118/106/91/72, 64k dropped); table rows gained (pp512)/(pp2048) annotations. 12 records updated, 1 removed (ctx64k). Dataset 3986 -> 3985.
- vllm PR #59916 updated again: TP1xPCP4+gather DCP4 142.3K (was 140.2), TP4+gather DCP4 61.7K (was 61.1), PP2xTP2+gather DCP2 101.4K (was 100.1). 3 records updated.

## 2026-10-04: llama.cpp issue #29949 MoE expert cache GPU LRU, Qwen3.8-Flash-Next (9 rows)

- llama.cpp issue #29949 (community, feature request with working implementation): MoE expert cache with GPU-resident LRU, where cache decisions and copies run on the GPU inside the compute graph. Qwen3.8-Flash-Next 125B, UD-IQ3_XXS and UD-IQ4_XS. 7900 XTX 24GB (ROCm), 48 layers pooled: UD-IQ3_XXS no pool 9.7 -> 160 slots 37.2 tok/s (+285%), MTP-Q8 on top 11.3 / 44.8; UD-IQ4_XS reverse placement (8 native + 40 pooled) 72 slots 31.2, 40 slots 28.8, 40 slots + MTP-Q4 30.5 tok/s. 2x RTX 3090 48GB (CUDA), UD-IQ4_XS 320 slots: EN plain 50.4 -> EN + MTP-Q8 61.1 tok/s (+21%). 9 rows (7 x 7900 XTX + 2 x 2x RTX 3090), 1 new hardware (7900 XTX), 2 new A/B groups with notes. Dataset 3977 -> 3986, hardware 386 -> 387.

## 2026-10-04: llama.cpp #29936 Vulkan Intel prefill regression fix, B70 Arc Pro (4 rows)

- llama.cpp PR #29936 (community, open): "vulkan: Fix Intel prefill regression on MoE models". A git-bisect shows PR #29182 halved Intel MoE prefill by steering the tile selector away from the tuned l_warptile config (the new rows-per-expert logic now defaults to smaller tiles). B70 Arc Pro on Windows, gemma4 26B.A4B Q4_K_M, pp8192 prefill: without flash attn (fa 0) b11017 3147.38 -> b11352 1526.29 t/s (-52%), with flash attn (fa 1) 1230.41 -> 879.92 (-28%). 4 rows (b11017/b11352 x fa0/fa1), 1 new A/B group with note. No new hardware/model/backend (B70 Arc Pro, gemma4 26B.A4B, Vulkan pre-exist). Dataset 3973 -> 3977, quote-verified 4556 -> 4560.

## 2026-10-04: akopytko/Qwen3.8-27B-NVFP4-GGUF Qwen3.8-27B on RTX 5090 (2 rows)

- HF card akopytko/Qwen3.8-27B-NVFP4-GGUF: Qwen3.8-27B (27B) with akopytko's Blackwell-native NVFP4 quant (no per-tensor scales, quant-time MSE scale search, runs on current llama.cpp, Blackwell GPUs RTX 50 series/B200/B300) on one RTX 5090 (stock 575 W). Default flags -b 2048 -ub 512: tg128 decode 87.45 / pp2048 prefill 6258.74 t/s. The embedded MTP draft head (--spec-type draft-mtp --spec-draft-n-max 8 --spec-draft-p-min 0.8) lifts decode to 152 t/s (+74% at 0.75 draft acceptance). The card's unsloth NVFP4 reference runs 87.69 tg128 / 6018.71 pp2048 on the same card, so the edge over it is on prefill, not decode. 2 rows (default + MTP), 1 new A/B group with note. Dataset 3971 -> 3973, quote-verified 4554 -> 4556.

## 2026-10-04: llama.cpp issue #29935 CUDA fattn KV streaming on sm86, context-decay A/B (4 rows)

- llama.cpp issue #29935 (community, perf report): CUDA fattn KV streaming on Ampere (sm86) decays ~2x off physics at long context because the VEC path is gated to batch==1, so at the MTP3 verify batch 4 quantized KV always takes the MMA path plus a whole-cache f16 conversion. qwen3.5-arch 27B NVFP4 on 2x RTX 3080 20GB, -fa on (tensor split), MTP3 spec (verify batch 4), single request, local build 836d571 (= b11379 + 2 commits, fattn identical). Decode tok/s decays with context: f16 KV 50.6 @30K -> 44.0 @90K (-13%), q8_0 KV 48.7 @30K -> 39.4 @90K (-19%); the q8_0 KV decays faster (step-time slope ~0.081 vs ~0.075 ms/1K tok) because of the f16 conversion pass. Official b11379 f16 48.2 @30K for reference. 4 rows (f16/q8_0 KV x 30K/90K context), 1 new hardware (2x RTX 3080 20GB), 1 new model (qwen3.5-arch 27B), 1 new A/B group with note. Dataset 3967 -> 3971, hardware 385 -> 386, models 199 -> 200, quote-verified 4550 -> 4554.

## 2026-10-04: neurall/llama.cpp fork MoE expert cache A/B benchmark, discussion #29429 (10 rows)

- neurall/llama.cpp fork (community, VRAM-filling MoE expert cache, builds on csantiago78 PR #27861) vs stock llama.cpp, from the fork README (discussion #29429, "Show and tell: MoE expert cache"). Machine A (2x RTX 3090, Ryzen 7 3700X, 125 GB DDR4-3200), short chat, single stream, temp 0, model in RAM: GLM-5.3-Flash 3.0-bit (106 GB) 11.9 -> 22.4 tok/s (1.9x), MiMo-V2.6-Flash IQ3_XXS (132 GB, bigger than the 125 GB RAM) 4.6 -> 10.9 tok/s (2.4x), Qwen3.8-Flash-Next UD-IQ4_XS (88 GB) 27.7 -> 46.5 tok/s (1.7x). Machine D (rented 4x RTX 3090, EPYC 7B12, 256 GB DDR4, raw logs not kept), GLM-5.3-Flash 3.0-bit (117.5 GB): 4 GPUs warm run 24.7 -> 31.5 tok/s (1.3x, -t 16 reaches 33.8), 3 of the 4 GPUs (best ratio) 20.1 -> 32.6 tok/s (1.6x). The fork fills VRAM with a pinned expert cache and parallelizes CPU misses, so big-MoE models that fit in RAM but not VRAM recover most of their expert work to the GPU. 10 rows (3 models x stock/fork on 2x 3090 + 2 GPU configs x stock/fork on 4x 3090), 1 new hardware (4x RTX 3090), 1 new model (MiMo-V2.6-Flash), 4 new A/B groups with notes. Dataset 3957 -> 3967, hardware 384 -> 385, models 198 -> 199, quote-verified 4540 -> 4550.

## 2026-10-04: llama.cpp discussions #29930 Qwen3.8-Flash-Next 177B on RTX 5070 via expert streaming (1 row)

- llama.cpp discussion #29930 (community, show-and-tell): Qwen3.8-Flash-Next 177B (UD-IQ3_XXS) running at ~11.5 tok/s on one RTX 5070 12GB + 32GB DDR4-2400 (Ryzen 5 5600GT, Windows) via a hashyy fork's page-locked hot-expert tier (expert streaming from system RAM to the 12GB card). Up from ~7 tok/s on the inherited setup; 10.41 tok/s over a 10k-token generation (16 min). 1 row, no new hardware/model (RTX 5070 and Qwen3.8-Flash-Next already present). Dataset 3956 -> 3957, quote-verified 4539 -> 4540.

## 2026-10-04: vLLM #59916 gather-based DCP prefill benchmark on 4x B300 (10 rows)

- vLLM PR #59916 (community): gather-based DCP for MLA models that can't run DCP natively. Measured prefill throughput on GLM-5.3-NVFP4 on 4x B300 (32 GiB/GPU KV budget), prefix-pooled 60K shared + 6K unique, OSL 1, concurrency 8. At TP1xPCP4 gather DCP4 does 141.6K tok/s, matching KVPP (143.0K, -1.0%) and 2.8x replicated (51.3K), holding 2.40M KV tokens vs KVPP 2.18M; at TP4 gather DCP4 (61.4K) is 1.55x native DCP4 (39.6K); at PP2xTP2 gather DCP2 (101.5K) matches KVPP (100.5K). 10 rows (TP1xPCP4/TP4/PP2xTP2 x replicated/KVPP/native/gather), 1 new hardware (4x B300), 1 new A/B group with note. Values are prefill rate in K tok/s.

## 2026-10-04: capyctl/FrogNano-4B-2609-MLX-4bit FrogNano-4B-2609 on RTX 4090 Laptop GPU (5 rows)

- HF card capyctl/FrogNano-4B-2609-MLX-4bit: FrogNano-4B-2609, 4-bit MLX affine (group 64) via TensorFold 0.6.3 CUDA engine on one RTX 4090 Laptop GPU (16 GB), greedy, thinking on. Single-stream decode 52.4 tok/s (median of 3); a --parallel 8 serving sweep aggregates 50.4 (1 stream) to 319.1 (8 streams) tok/s (+533% aggregate), while per-stream throughput declines 50.6 to 40.3 tok/s as streams share the card. Decode holds about 49-50 tok/s single-stream from 0.5k to 32k context; the card's BF16 vLLM baseline is 59.9 single-stream. 5 rows (single + c1/c2/c4/c8), 1 new model (FrogNano-4B-2609), 1 new hardware (RTX 4090 Laptop GPU), 1 new backend (TensorFold (CUDA)), 1 new A/B group with note.

## 2026-10-04: DuoNeural/LFM2.5-8B-A1B-TAP-DPQ-v7-GGUF quantization sweep on RTX 4080 Super (6 rows)

- HF card DuoNeural/LFM2.5-8B-A1B-TAP-DPQ-v7-GGUF: LFM2.5-8B-A1B with TAP-DPQ v7 post-training quantization on RTX 4080 Super, llama.cpp CUDA, ctx 8192. Decode: baseline (fp16) 118.5, Q4_K_M 172.4, IQ3_XXS 196.2, IQ2_M 208.5, IQ2_XXS 224.1, IQ1_S 241.8 t/s. 6 rows, 1 new model (LFM2.5-8B-A1B), 1 new hardware (RTX 4080 Super).

## 2026-10-04: DuoNeural/Qwen3.5-9B-TAP-DPQ-v7-GGUF quantization sweep on RTX 3090 (6 rows)

- HF card DuoNeural/Qwen3.5-9B-TAP-DPQ-v7-GGUF: Qwen3.5-9B (64-layer hybrid DeltaNet+MHA) with TAP-DPQ v7 post-training quantization on RTX 3090 24GB, llama.cpp CUDA, ctx 16384. Quantization sweep: FP16 baseline 78.2, Q4_K_M 112.5, IQ3_XXS 138.7, IQ2_M 145.2, IQ2_XXS 156.4, IQ1_S 168.1 t/s. 6 rows, 3 new quant strings (IQ3_XXS, IQ2_M, IQ1_S), 1 new A/B group.
- vLLM #59852 drift fix: PR rewritten with percentage improvements (1.8-11.0% higher than allgather/reducescatter at c32-c192), no absolute tok/s remain. 2 rows deleted, A/B note removed. Dataset 3933 -> 3935 (after #59852 deletion and DuoNeural addition), hardware 382, models 196, quote-verified 4512 -> 4518.

## 2026-10-03: promzeus/gh0stx-glm46-gb10-GGUF GLM-4.6 355B MoE on GB10 (6 rows)

- HF card promzeus/gh0stx-glm46-gb10-GGUF: GLM-4.6 (355B-A32B MoE) abliterated, IQ2_XXS+Q5_K mix (2.26 bpw) on GB10 (DGX Spark, 128 GB unified memory), llama.cpp CUDA. MTP speculative decode sweep: no-spec 11.45, MTP n-max 1 (113k ctx, q4_0 KV) 17.14, n-max 2 (32k, q8_0) 14.36, n-max 3 (32k, q8_0) 12.17 tok/s. Depth decay: 57.6k prefill 197 / decode 4.10, 111.9k prefill 125 / decode 3.61 (MTP). 6 rows, 1 new model (GLM-4.6), 1 new A/B group with note.
- ResonateX-T1-125M-Talking-GGUF drift fix: HF card updated (TPU v6e 53,225 -> A100-SXM4-40GB 162,214 tok/s). Re-mined the row. Hardware page renamed tpu-v6e -> a100-sxm4-40gb. Dataset 3925 -> 3931, models 195 -> 196, quote-verified 4508 -> 4514.

## 2026-10-03: llama.cpp #29924 n-gram spec decode truncation fix (11 rows) + drift fixes (#59894 re-mine, #29869 re-mine, #59740 delete)

- llama.cpp PR #29924 (open): "Fix n-gram drafts rejected at temp>0 after truncation". After context truncation all n-gram drafts were silently rejected at temp>0, forcing a fallback to the base model. The fix re-evaluates n-gram acceptance post-truncation. RTX 5090, 8 seeds, median t/s. Llama 3.1 8B: 509.6 (pre-PR) -> 375.1 (bug) -> 500.7 (fix, recovers 33% of the gap). Qwen3.6-35B-A3B: n-gram 227.8 -> 292.8 (+29%), MTP-1 301.7 -> 333.9, MTP-2 187.0 -> 329.4, MTP-prob 307.6 -> 344.1. 11 rows (3 Llama + 8 Qwen), 2 new A/B groups with notes.
- Drift fixes: vLLM #59894 PR description rewritten (new table format, all 8 rows re-mined with updated tps/ttft_s; 32k/256 ttft set to None, now reports TPOT). llama.cpp #29869 PR description rewritten (new table format, all 10 rows re-mined with updated values). vLLM #59740 PR description completely rewritten (old per-domain and Other-hardware tables gone, replaced by SPEED-Bench percentage tables; all 62 rows deleted, 3 A/B note blocks removed). Hardware 384 -> 382, dataset 3976 -> 3925, quote-verified 4559 -> 4508.

## 2026-10-03: vLLM #59894 DSV4.1-Flash DEP4 decoder-replay cut-layer split on B200 x4 (8 rows)

- vLLM PR #59894 (open): "[Perf][DSV4.1] Decoder replay: trim the cut layer's query side and FFN". The decoder SWA bounded replay (#58132) runs the cut layer (layer 20 on DSV4.1-Flash) on every row, but the trimmed replay rows only read its KV, so the PR makes the cut layer split by default: its query side and FFN feed only the replay layers. DSV4.1-Flash DEP4 on B200 x4, vllm bench serve random data, main -> PR. Total tok/s improves at all prefill points (8k/1 C16 234,696 -> 242,486, 32k/1 C16 235,399 -> 244,063, 128k/1 C4 204,020 -> 218,421) and output tok/s at 32k/256 C32 754 -> 833; TTFT drops 3.2-11.7% across the board (549 -> 531 ms at 8k/1, 2,201 -> 1,944 ms at 32k/256). GSM8K 0.9629 -> 0.9651, within noise. 8 rows (4 points x main/PR).
- New model string DSV4.1-Flash (the source abbreviation, distinct from the existing DeepSeek-V4.1-Flash) and hardware B200 x4 (the source writes "B200 x4", 4 GPUs). Dataset 3968 -> 3976, hardware 383 -> 384, models 194 -> 195, quote-verified 4551 -> 4559.

## 2026-10-03: llama.cpp #29910 Q2_K VGPR spill (MI50/gfx1152) + #29911 MUL_MAT_ID F32 (RTX 3060) (28 rows, 3 new hardware)

- llama.cpp PR #29910 (open): "ggml-cuda: fix a mountain of VGPR spills on Q2_K". The Q2_K mmq path spills massively (164 VGPRs on gfx906, 1387 on RDNA3); the fix uses a gentler unroll and removes an unneeded temporary loop. pp2048 -b 2048 -r 10, -ub 16-512 sweep on two AMD parts: MI50 (gfx906, DP4A) and gfx1152 (RDNA 3.5, MMA), Meta-Llama-3-8B-Instruct Q2_K. 24 rows (6 -ub x master/optimized x 2 GPUs). On MI50 the spill count drops 164 to 0 and prefill climbs across the sweep (ub64 +140%, ub512 +179%); on gfx1152 spills drop 1387 to 0 but the gain is only at low -ub (ub16 +34%), flat at high -ub.
- llama.cpp PR #29911 (open): "cuda/vulkan: do not reject MUL_MAT_ID with GGML_PREC_F32 for quantized weights". The flag was honored only by F16/BF16 paths, so a quantized MoE (Mistral Small 4 sets it on ffn_moe_down) ran every ffn_down_exps mul_mat_id on the CPU and copied the full expert matrix VRAM->host per token (232 x 570 MB D2H transfers). The fix gates the rejection on !ggml_is_quantized(src0). Interleaved A/B swapping only libggml-cuda.so on an RTX 3060 12 GB: decode ~4.8-5.4 -> ~18.7-19.4 t/s (~3.6x), D2H transfers 232 -> 0, output byte-identical. 4 rows (before/after x 2 runs).
- Three new hardware strings: MI50, gfx1152, and "RTX 3060 12 GB" (the source writes "12 GB" with a space, distinct from the existing "RTX 3060 12GB"). Two new A/B groups with notes (MI50 and gfx1152 for #29910; RTX 3060 12 GB for #29911). Dataset 3940 -> 3968, hardware 380 -> 383, models 194 (unchanged: Meta-Llama-3-8B-Instruct and Mistral Small 4 119B pre-exist), quote-verified 4523 -> 4551.

## 2026-10-03: llama.cpp #29908 Vulkan decode on Arc Pro B50 (2 rows)

- llama.cpp #29908 (open issue): "Vulkan: decode MUL_MAT_VEC ~5-7x slower in-model than isolated on Arc Pro B50". The report benchmarks Qwen3.8-27B on an Arc Pro B50 (Vulkan, -ngl 99, -c 4096) and finds in-model MUL_MAT_VEC nodes run 5-7x slower than the identical ops measured in isolation via test-backend-ops perf. Two whole-model decode baselines: GSQ-RCO IQ3_XXS 10.1 t/s (tg128) and Q3_K_M 10.2 t/s. The isolated probe shows ~60-119 GB/s effective bandwidth, in-model drops to ~9-18 GB/s.
- Dataset 3938 -> 3940, hardware 380 (unchanged: Arc Pro B50 pre-exists), models 194 (unchanged), quote-verified 4521 -> 4523.

## 2026-10-03: Drift fix: agentionai Qwen3.8-Flash-Next-Gyro card re-quoted (26 rows, 1 value correction)

- The agentionai/Qwen3.8-Flash-Next-Gyro-GGUF card page drifted: the RTX 5090 prefill value moved 296 -> 795 tok/s and the old whole-card-content quote is no longer verbatim on the rendered page (cold-cache CI check_quotes failed with 27 fragment errors).
- Re-pointed all 26 gyro rows to short stable per-row quotes (model name + hardware + the row's own values, each fragment verified verbatim on the freshly fetched page) and corrected the 5090 pp_tps from 296 to 795. No other values changed; dataset size, hardware count, and model count are unchanged.

## 2026-10-03: vLLM #59878 FlashInfer attention sinks on SM8x (2 rows, 1 new hardware, 1 new A/B group)

- vLLM PR #59878 (open): "Support FlashInfer attention sinks on SM8x". Routes every layer with sinks through FlashInfer's fa2 sink wrappers on SM8x, so a sink model such as gpt-oss-20b with a BF16 KV cache selects FLASHINFER instead of TRITON_ATTN by backend priority (and an FP8 KV cache now has a backend on SM80/SM86, where Triton's FP8 KV needs SM89+). Depends on FlashInfer #6021 (BatchDecodeWithAttentionSinkWrapper).
- vllm bench throughput on sm_80 (two GPUs, averaged, run back to back in opposite orders), gpt-oss-20b, BF16 KV cache, 200 prompts, 1024 in / 256 out. Two rows: TRITON_ATTN 11,283 vs FLASHINFER 11,546 tok/s (+2.3%). The batch-1 latency gap is in decode (FlashInfer decode attention kernel 9.07 us/layer vs Triton 4.73); prefill matches, and batch-32 latency is 2.76% lower.
- New hardware "sm_80" (compute capability 8.0, Ampere; the exact GPU is not named in the PR, and the runs are averaged over two sm_80 GPUs) and a new A/B group (sm_80, gpt-oss 20B, vLLM) with a note. Dataset 3936 -> 3938, hardware 379 -> 380, models 194 (unchanged: gpt-oss 20B pre-exists), quote-verified 4519 -> 4521.

## 2026-10-03: HF card nightmedia Qwen3.8-27B-MindMeld-AREX MLX quant sweep on MacBook Pro 128GB (5 rows, 1 new hardware)

- Found via hf_scan.py (an expanded pass over all 396 fresh candidates; this card was parked earlier for vague hardware and is now mined with the literal label the card gives).
- HF model card nightmedia/Qwen3.8-27B-MindMeld-AREX-mxfp8-mlx: a MindMeld-AREX merge of Qwen3.8-27B (27B) run under MLX. The card reports an MLX quant sweep (Perplexity / Peak Memory / Tokens/sec) for the main model across five quantizations on a 128 GB MacBook Pro (M-chip not stated in the card): mxfp8 209, q8-hi 213, qx86-hi 210, qx64-hi 204, mxfp4 206 tok/s. Five rows. The card also benchmarks the parent Qwen3.6-27B-MindMeld and AREX-2 as components (not mined).
- Finding: the five MLX quantizations cluster within a 4.4% band (204-213 tok/s), so the quant is a memory decision, not a speed one: q8-hi is fastest (213) but needs 37.3 GB, and mxfp4 is the leanest (21.3 GB) at 206 tok/s.
- New hardware "MacBook Pro 128GB" (literal; the card names the RAM but not the M-chip) and a new A/B group (MacBook Pro 128GB, Qwen3.8-27B, MLX) with a note. Dataset 3931 -> 3936, hardware 378 -> 379, models 194 (unchanged: Qwen3.8-27B pre-exists), quote-verified 4514 -> 4519.

## 2026-10-03: llama.cpp #29892 RDNA4 Vulkan prefill regression + #29901 CUDA lightning-indexer tiling (6 rows, 2 new A/B groups)

- llama.cpp #29892 (open issue): "Vulkan ~12% prefill regression on RDNA4 (RX 9070 XT) since #29182 (MoE-aware mul_mat_id tile selection)". Qwen3.6-35B-A3B UD-IQ3_S (256 experts, top-8), llama-bench pp2048 @ d48000, -b 4096 -fa 1, all-VRAM. Four rows: two -ub arms (1024/2048) x parent (da89bb3cc, no #29182) vs master (bed0a8566, with #29182). At -ub 1024 prefill regresses 2154.41 -> 1875.05 tok/s (-13.0%); at -ub 2048 it is flat (2075.07 -> 2073.69, inside the +/-94-124 noise floor); token generation is unaffected (107.3 vs 107.1 t/s all-VRAM per the report) and reverting restores 2145.6.
- llama.cpp PR #29901 (open): "cuda: tile the lightning indexer over keys and tokens for 4 heads" (port of the Vulkan shader by @0cc4m). RTX PRO 6000, qwen4exp (4-head lightning-indexer arch), prod config, prefill @ 128k ctx. Two rows (base before tiling vs pr after): prefill 3867 -> 4038 tok/s (+4.4%), TG unchanged; the indexer kernel itself is 2.5x faster (6.4 vs 16.4 ms at kv 65536, nb 2048) and drops from 9.6% to 4.0% of GPU time in nsys. New model Qwen4-exp (the arch name; the weights are unnamed in the report).
- Two new A/B groups (Radeon RX 9070 XT Vulkan, RTX PRO 6000 CUDA), each with a note. Dataset 3925 -> 3931, hardware 378 (unchanged: both GPUs pre-exist), models 193 -> 194 (Qwen4-exp new), quote-verified 4508 -> 4514.

## 2026-10-03: HF scan batch: deluxetiky RTX PRO 6000 Max-Q concurrency sweep + rariruluis ELYZA M4 Max (12 rows, 3 new models)

- Found via hf_scan.py (2 fresh cards).
- deluxetiky/agnes-vs-qwen38-benchmark: single-GPU serving benchmark on one NVIDIA RTX PRO 6000 Blackwell Max-Q Workstation Edition 96 GB, 262144 max ctx, KV fp8. A concurrency sweep (scale_and_context.py, aggregate tok/s) of two models, ten rows. Qwen3.8-27B TURBO NVFP4-W4A16 (modelopt FP4, native MTP head n=1) under vLLM 0.27.1 + a GDN decode backport (PR #41966): 106.3 / 209.8 / 274.5 / 765.6 / 581.0 tok/s at c1/c2/c4/c8/c16, peaking at c8 (765.6) then dropping 24% at c16 (the 160%-of-roofline over-subscription). Agnes-3.0-Flash BF16 (66.2 GB) under SGLang 0.5.19 + a checkpoint patch, NEXTN spec-decode (steps=3 draft=4): 35.2 / 59.0 / 123.7 / 125.6 / 71.6, plateauing around 125 (c4-c8) then collapsing 43% at c16. New models Qwen3.8-27B-TURBO and Agnes-3.0-Flash; hardware pre-exists.
- rariruluis/ELYZA-Thinking-1.0-llm-jp-4-32b-a3b-mlx-4bit: ELYZA-Thinking-1.0 (Japanese 4th-gen 32B MoE, 3B active), 4-bit MLX (group 64, 4.501 bpw), mlx-lm 0.32.0, Apple M4 Max 64 GB, 4096 ctx, greedy. Two sample prompts, two rows: math (reasoning_effort=medium) 114 tok/s, code (reasoning_effort=low) 129 tok/s; the author flags both as small sanity checks, not a benchmark. New model ELYZA-Thinking-1.0-llm-jp-4-32b-a3b; hardware pre-exists.
- Three new A/B groups (Qwen3.8-27B-TURBO vLLM, Agnes-3.0-Flash SGLang, ELYZA MLX), each with a note. Dataset 3913 -> 3925, hardware 378 (unchanged), models 190 -> 193, quote-verified 4496 -> 4508.

## 2026-10-03: vLLM #59852 MoRI FP4 dispatch for DeepSeek V4.1 a4w4 on MI355X (2 rows, 1 new A/B group)

- vLLM PR #59852 (open): "[ROCm][MoE] Enable MoRI FP4 dispatch for DeepSeek V4.1 a4w4" (VLLM_ROCM_USE_AITER_MOE_A4W4_DSV4=1, stacked on #59596). 2x MI355X, TP1 DP2 expert-parallel, MoE backend aiter, DSpark speculative decoding (synthetic acceptance 3.51); vllm bench serve --random-input-len 4096 --random-output-len 1024 --num-prompts 640 --max-concurrency 64, cold, one run each.
- Two arms (baseline allgather/reducescatter all2all path vs MoRI FP4 dispatch): total tok/s 16146 -> 16648 (+3.1%) and mean TTFT 1.56 s -> 1.52 s at c64. The per-layer EP2 dispatch+combine kernel is 1.33x to 1.49x faster than MoRI BF16 at 384-8192 tokens/rank, but the end-to-end gain stays small on EP2 because top-6 sends nearly every token to both ranks over a single xGMI link. GSM8K 0.896 -> 0.897 (within error). The kernel table is parked (component benchmark).
- New A/B group (MI355X, DeepSeek-V4.1-Flash) with a note. Dataset 3911 -> 3913, hardware 378 (unchanged: MI355X pre-exists), models 190 (unchanged: DeepSeek-V4.1-Flash pre-exists), quote-verified 4494 -> 4496.

## 2026-10-03: llama.cpp #29887 MoE expert GPU cache on RTX 4090 and RTX 5090 (6 rows, 2 new A/B groups)

- llama.cpp PR #29887 (open): "MoE expert GPU cache" (port of qvac-fabric's --moe-cache-mib). Qwen3.8-Flash-Next Q4_0 (93.7 GiB, 65.4 GiB of experts), SPEED-Bench qualitative (11 categories x 3 samples, --osl 512, temp 0, no MTP), llama-server -fa on -c 32768 -b 2048 -ub 2048 -t 16, CPU on the GPU NUMA node (EPYC 7742), PCIe 4.0 x16. Host experts run on the GPU with an LRU cache; only misses are uploaded (small batches <=32 tokens), larger batches bypass the cache.
- Two GPUs (RTX 4090, RTX 5090), three config arms each (the master --fit baseline with no cache, a 6.4 GB partial cache --moe-cache-mib 6544, and the full -cmoe cache): six rows. Decode goes 25.0 -> 40.7 tok/s (+63%) on the 4090 and 30.8 -> 67.8 (+120%) on the 5090 with the full cache; the partial cache lands close (39.4 / 54.5). The 4090-only prompt table shows the trade-off: pp2048 dips 1388 -> 1080 as whole layers move to the cache.
- Two new A/B groups (RTX 4090, RTX 5090), each with a note. Dataset 3905 -> 3911, hardware 378 (unchanged: RTX 4090 and RTX 5090 pre-exist), models 190 (unchanged: Qwen3.8-Flash-Next pre-exists), quote-verified 4488 -> 4494.

## 2026-10-03: HF scan batch: 2 tsaipifong MXFP4 cards on R9700 (12 rows, 2 new A/B groups)

- Found via hf_scan.py (2 fresh cards, both tsaipifong MXFP4 GGUFs benchmarked on an AMD Radeon AI PRO R9700 32 GB USB4 eGPU with llama.cpp b11214 ROCm).
- Swift-1.5-Qwen3.8-27b MXFP4 (a Swift-1.5 fine-tune of Qwen3.8 27b, MTP layer kept for self-spec decode): 3 output-head variants (A Q6_K / B Q8_0 / C Q4_K) x plain/MTP n-max 3, six rows. MTP is a clear win over plain on every variant (variant A 33.3 -> 58.1, +74%); the head matters little (the Q4_K-head C build is fastest for both plain 33.8 and MTP 60.7, the Q8_0-head B build slowest). 2k prefill ~1206-1215 tok/s.
- Ornith-1.5-35B-A3B MXFP4 (~35B total / ~3B active MoE, MTP layer kept): the llama.cpp column of a WHIRL-vs-llama.cpp comparison (the card's focus is the WHIRL engine, which leads 1.4-2.8x). Six rows: CLI llama-bench tg256 119.7, 800-token Chinese coding 118.8, 128 tokens after a 16k context 107.5, file editing with draft-mtp,ngram-mod n-max 1 239.3, 4-concurrent aggregate 191.9 tok/s, and prefill at 131k tokens (-ub 2048) 2239 tok/s.
- Two new A/B groups on the R9700 (Swift 1.5 and Ornith-1.5-35B-A3B), each with a note. Dataset 3893 -> 3905, hardware 378 (unchanged: R9700 pre-exists), models 190 (unchanged: both models pre-exist), quote-verified 4476 -> 4488.

## 2026-10-03: HF card Davidmg0815 Qwen3.8-Flash-Next MTP-256exp GPU section, 2x 20 GB CUDA (9 rows, 1 new hardware)

- HF model card Davidmg0815/Qwen3.8-Flash-Next-MTP-256exp-GGUF, GPU section (the CPU section of this card was mined earlier as "8 threads"). The 176B MoE (pruned 512 -> 256 experts, GSQ-RCO) with a separate 256-expert Q8_0 MTP head, run as a 3-slot llama-server on a 2x 20 GB CUDA box (tensor-split 45,55), KV q5_1, temperature 0, 400-token runs, one run per cell. The author flags the cells as "indications, not benchmarks"; the GPU is not named (recorded as the literal "2\u00d7 20 GB").
- The 3x64K 256-head n-max sweep (9 rows): no-head baseline 61.5 tok/s for code and prose alike (context not stated); n-max 1 code 55.4 / prose 49.4; n-max 2 code 67.1 / prose 50.3; n-max 3 code 70.5 / prose 59.6 (unstable, CUDA OOM); n-max 3 p-min 0.6 code 58.9 / prose 41.2. Code and German prose are separate rows. New hardware "2\u00d7 20 GB".
- Finding: the MTP head helps code but not German prose, and both effects are n-max-sensitive. Code peaks at n-max 3 (70.5, +15% vs baseline) but that arm is unstable (CUDA OOM under three parallel 54k prompts); n-max 2 is the stable choice (code +9%, prose -18%). Prose drops hardest at p-min 0.6 (41.2, -33%). The CPU section of this card remains the cleaner MTP win.
- Dataset 3884 -> 3893, hardware 377 -> 378, quote-verified 4467 -> 4476.

## 2026-10-03: vLLM #59846 DeepSeek-V4.1-Flash KV-cache A/B on 4x RTX PRO 6000 Blackwell (SM120) (14 rows, 1 new hardware)

- vLLM PR #59846 (open): "[Perf][DSv4.1] SM120: decode DeepSeek-V4.1's own KV records with FlashInfer's DSv4.1 sparse attention". nvfp4_ds_mla (a mixed fp8+nvfp4 KV cache) was rejected on SM120 before; this PR widens the SM90+ gate to accept it. TP4 on 4x RTX PRO 6000 Blackwell, DeepSeek-V4.1-Flash FP8, 8k in / 1k out serving.
- The throughput table is malformed (an empty column plus a duplicated fp8_ds_mla header), so only the two clearly-labeled columns are mined: the V4 record (before this PR) vs nvfp4_ds_mla, at 7 concurrency levels (14 rows). New hardware "4\u00d7 RTX PRO 6000 Blackwell" (SM120).
- Finding: throughput is unchanged within 2% (no regression) at every concurrency except c32 nvfp4 (+17%, one run, not claimed per the PR). The PR's real win is capacity: nvfp4_ds_mla fits 305,319 KV tokens vs 214,991 for the V4 record (+42%) at the same throughput.
- Dataset 3870 -> 3884, hardware 376 -> 377, quote-verified 4453 -> 4467.

## 2026-10-03: HF card SixVolts GLM-5.3-Flash e-waste edition, 10x MI100 (2 rows, 1 new hardware)

- HF model card SixVolts/GLM-5.3-Flash-ewaste-edition-GGUF: imatrix K-quant GGUFs of GLM-5.3-Flash (321B total / 18B active, glm5-next arch) benchmarked with llama-bench -p 2048 -n 128 (no speculative decoding, -fa off) on the author's 10x MI100 (gfx908) e-waste box, a fork of llama.cpp (glm5next arch name). Found via hf_scan.py (new card). The GPU backend is not named in the card; ROCm is the gfx908 default and is recorded as such.
- Two quant rows, one A/B group (quant-width, not a before/after): Q4_K_XL 780 prefill / 33.8 decode, Q3_K_M 730 / 32.2 tok/s. The card's finding: 3-bit is not faster than 4-bit on this GPU class because K-quant dequantization, not bandwidth, is the decode bottleneck (why the e-waste editions drop i-quants). New hardware "10\u00d7 MI100".
- Dataset 3868 -> 3870, hardware 375 -> 376, quote-verified 4451 -> 4453.

## 2026-10-03: HF scan batch: 4 PAW/clef cards (12 rows, 1 new model, 1 new A/B group)

- Found via hf_scan.py (4 fresh cards, all Qwen-family GGUFs from two authors: lackonendes PAW trellis quants and Livesport clef-flash).
- PAW-27B-X3 (Qwen3.8-27B, 3.5 bpw X3, 1x RTX 3090, llama-paw CUDA fork, 262144 ctx): prefill 1076.5/512, 1215.4/8k, 563.0/211k; decode 33.5 at tg128, 19.9 at 211k depth; verified spec decode 100.45 at 8k code context (output hash-identical). Six rows. These merge into the existing RTX 3090 Qwen3.8-27B A/B group, which now holds 14 arms across the three PAW editions (X3.1, PAW-27B, X3); the group note was rewritten to cover all three.
- PAW-27B (Qwen3.8-27B, ~2.17 bpw, 1x RTX 3090, MTP drafter, 256k ctx): the MTP head lifts short-context decode 22.7 -> 78.4 (+245%), 47.8 at 191k. Three rows (same A/B group).
- PAW-35B-A3B (Qwen3.6-35B-A3B, 1.54 bpw, 1x RTX 3090): decode 133.7 mixed, 182.7 code. Two rows, one new A/B group (two workloads, not a before/after; note added).
- clef-flash (Cloudflare/clef-flash, Q5_K_M-dyn, 1x Quadro RTX 4000 8 GB): ~1100 tok/s on 16,384-token requests. One row, new model "clef-flash".
- Dataset 3856 -> 3868, hardware 375 (unchanged: RTX 3090 and Quadro RTX 4000 pre-exist), models 189 -> 190 (clef-flash), quote-verified 4439 -> 4451.

## 2026-10-03: llama.cpp #29884 CPU backend variant sweep, Dimensity 9400 (5 rows, 1 new A/B group)

- llama.cpp issue #29884: the aarch64 `ggml_backend_score()` selects a CPU backend variant by feature bit-flags, not throughput, so on Android the SVE2 (armv9) variant wins on every ARMv9 mobile SoC even though it is ~2x slower for prompt processing. The reporter benchmarked all 7 CPU backend variants in isolation (`llama-bench -p 512 -r 3`, pp512) on a MediaTek Dimensity 9400 (MT6991), Android 16, Qwen3-Embedding-0.6B Q8_0.
- Five variants have values: armv8.0_1 102.33 (baseline, no dotprod/i8mm), armv8.2_1 240.05, armv8.2_2 229.56, armv8.6_1 259.77 (fastest, not selected), armv9.0_1 123.45 (selected by default); armv9.2_1/2 are not loaded (no SME). One new A/B group (5 arms). New hardware Dimensity 9400 and new model Qwen3-Embedding-0.6B. Dataset 3851 -> 3856, hardware 374 -> 375, models 188 -> 189, quote-verified 4434 -> 4439.

## 2026-10-03: vLLM #59824 DSpark adaptive verification on Kimi-K3 MI355X (6 rows, 1 new A/B group)

- vLLM PR #59824 (open): "[ROCm][Kimi-K3] Support DSpark adaptive verification on MI355X". `speculative_config.enable_adaptive_verification` trims each verify request to 1..k+1 tokens on the device using the DSpark confidence head; the PR enables it for Kimi-K3 on ROCm (removing the three SSM/GDN varlen gates). Benchmarked on Kimi-K3 FP4 TP8, MI355X, fresh servers: 16k-token code prompts, 1024 output tokens.
- Output tok/s, adaptive off (static K=7) vs on: c10 453.4 -> 485.5 (+7.1%, 1 run), c12 499.3 -> 510.9 (+2.3%), c14 515.1 -> 529.7 (+2.8%, 3 runs). Trimming only kicks in at conc >= 8; KV cache capacity drops ~9.8% (3.31M -> 2.99M tok). Six rows (3 conc x off/on), one new A/B group. The gains are against static K=7, not the best static K per concurrency (the PR notes this). Dataset 3845 -> 3851, quote-verified 4428 -> 4434.

## 2026-10-02: llama.cpp #29882 Vulkan rms-norm subgroup reductions, B70 Arc Pro + RTX 4060 Ti (20 rows, 5 new A/B groups, 2 new hardware)

- llama.cpp PR #29882 (open): "vulkan: rms-norm subgroup reductions", a Vulkan optimization that rewrites the RMS-norm pass to use subgroup reductions instead of the per-lane scalar path. The author benchmarked it before/after (build 11369 baseline vs the optimized builds 11370/11371) on an Intel Arc Pro B70 (Windows) and an Nvidia RTX 4060 Ti (Windows), llama-bench, -ngl -1, -r 5, flash-attention off and on (fa0/fa1).
- The optimization is prefill-focused and modest: rms-norm runs in the per-token norm path, so gains concentrate in prefill (llama-bench pp) and decode (tg) is roughly neutral. fa0 prefill moves +1.2% to +2.6% on the 26B/35B/9B models and +19.4% on the small Qwen3-0.6B B70 prefill (21235 -> 25347 tok/s, a small-model outlier where the norm path is a larger fraction); decode is flat to +0.9%. Five before/after A/B groups (4 fa/build arms each): Gemma4 26B A4B Q4_K on B70 Arc Pro (pp8192 only), Qwen3.6-35B-A3B Q4_K on B70 Arc Pro, Qwen3-0.6B Q4_K on B70 Arc Pro (pp512 + tg128), Qwen3-0.6B Q4_K on RTX 4060 Ti (pp1024 + tg128), Qwen3.5-9B BF16 on RTX 4060 Ti.
- New hardware variants "B70 Arc Pro" (distinct word order from the existing "Arc Pro B70") and plain "RTX 4060 Ti" (the dataset previously had only "RTX 4060 Ti 16GB"). Models and the Vulkan backend pre-exist. Dataset 3825 -> 3845, hardware 372 -> 374, quote-verified 4408 -> 4428.

## 2026-10-02: HF card ResonateX T1 TPU v6e training throughput (1 row, first TPU row)

- HF model card ResonatexIntegratedTechnologies/ResonateX-T1-125M-Talking-GGUF: training telemetry for the 125.3M-parameter ResonateX T1 talking model. This is the first TPU row in the dataset (hardware "TPU v6e", backend "training (TPU)"). Found via hf_scan.py (previously parked as a training-throughput card; mined now to close out the scan).
- Single row: average training throughput 53,225 tok/s over 22,100 steps (3.83 h), 1 TPU v6e worker via Google Colab, 724.2M tokens (5.78 tok/param). The card notes throughput stabilized at ~53K tok/s after warm-up. tps is the average training rate (training, not inference); the per-stage curriculum table is left in notes.
- Dataset 3824 -> 3825, hardware 371 -> 372, models 187 -> 188, backends 26 -> 27, quote-verified 4407 -> 4408.

## 2026-10-02: HF card Livesport rune-26b-a4b-v3 2x Quadro RTX 4000 prefill (2 rows, 1 new hardware, 1 new model; re-mined 10-03 after card rewrite)

- HF model card Livesport/rune-26b-a4b-v3-GGUF: prompt-processing (prefill) throughput on 2x Quadro RTX 4000 8 GB, IQ3_S-dyn 26B MoE (gemma4 arch) + q8_0 KV cache. Found via hf_scan.py (new card). New hardware "2x Quadro RTX 4000" and new model "rune-26b-a4b-v3".
- Re-mined 2026-10-03: the card was rewritten and dropped the original -ub 512/256 prompt-batch sweep (2,098 / 1,696 tok/s). It now reports prefill for the IQ3_S-dyn quant (the production quant; the card notes it processes prompts at the same speed as the previous IQ3_M): llama-server ~2,000-token prompt 2,098 tok/s (llama-bench pp2048 cross-check 2,049-2,065) and a 14,478-token prompt 1,904 tok/s (essentially flat vs the ~2,000-token rate, no long-context prefill cliff). Two rows, no A/B. The card's latency table is per-question seconds (decode-side, KV-cache reuse) and is left unmined as tok/s.
- Dataset 3822 -> 3824, hardware 370 -> 371, models 186 -> 187, quote-verified 4405 -> 4407 (row count unchanged by the re-mine).

## 2026-10-02: HF card Davidmg0815 Qwen3.8-Flash-Next MTP-256exp CPU spec decode (3 rows, 1 new A/B group, 1 new hardware)

- HF model card Davidmg0815/Qwen3.8-Flash-Next-MTP-256exp-GGUF: field note on MTP draft-mtp speculative decoding (--spec-type draft-mtp) on the Qwen3.8-Flash-Next 176B MoE pruned 512 -> 256 experts (GSQ-RCO), main model IQ1_M + a separate Q8_0 MTP head loaded as its own model via -md. Found via hf_scan.py (re-examined a previously-parked card; its GPU section is an unnamed 2x 20 GB setup with a prose loss, so the clean finding is the CPU section).
- CPU, 8 threads, ctx 4096, one code prompt, temperature 0, thinking off, 160 tokens (author: "indications, not benchmarks"): serial decode (no speculation) 3.49, unsloth 512-expert head 5.61 (+61%, 81.7% draft acceptance 98/120), pruned 256-expert head 5.13 (+47%, 74.8% acceptance 95/127) tok/s. The MTP head is a clear win on CPU; the card's GPU setup shows only a small code gain and a prose loss, so the 3 CPU rows are the clean result. New hardware "8 threads" (CPU, threads-only).
- Dataset 3819 -> 3822, hardware 369 -> 370, quote-verified 4402 -> 4405.

## 2026-10-02: llama.cpp #29875 AMD Ryzen 7 7735HS entropy-gated speculative decoding (6 rows, 1 new A/B group, 1 new hardware, 1 new model)

- llama.cpp issue #29875 (feature request, open, 0 comments): proposes `--spec-draft-entropy-max`, a Shannon-entropy-gated early-exit for speculative drafting (halt drafting when the draft distribution's entropy exceeds a threshold, instead of the existing top-1 `--spec-draft-p-min` gate). Author benchmarked it head-to-head on an AMD Ryzen 7 7735HS (8 CPU threads), Qwen2.5-3B target + Qwen2.5-0.5B draft, K=8 draft budget, 128+ tokens; unmerged working branch feat/entropy-gated-speculation (44/44 ctest).
- Three gating strategies compared on two tasks: code (longest common subsequence, 134 tokens) static 11.71 / p_min 0.6 14.83 / entropy gate 16.50 tok/s (acceptance 57.29% / 78.99% / 88.46%); riddle/divergent reasoning (130 tokens) static 6.70 / p_min 0.6 12.91 / entropy gate 13.19 tok/s (27.78% / 71.57% / 84.62%). Entropy gate is +11.3% over p_min 0.6 and +40.9% over static on code; ~1.97x wall-clock over static on the riddle. New model "Qwen2.5 3B" (target), new hardware "AMD Ryzen 7 7735HS",
- Dataset 3813 -> 3819, models 185 -> 186, hardware 368 -> 369, quote-verified 4396 -> 4402.

## 2026-10-02: HF card CleverBadger Swift 1.5 Qwen3.8 27B Badger Mixed M5 Pro (4 rows, 1 new A/B group, 1 new model)

- HF model card CleverBadger/Swift-1.5-Qwen3.8-27B-Badger-Mixed-GGUF: a Q4/Q6/Q8 mixed-precision build of the Swift 1.5 fine-tune of Qwen3.8 27B (base ukisai/Swift-1.5-Qwen3.8-27b), a 27B vision model, designed for 48 GB Apple Silicon. Runs through Splash with Metal and DFlash2, full 262144-token window.
- Mac performance table on a 48 GB M5 Pro MacBook Pro (20 GPU cores): weighted per-request 32.58, median per-request 34.42, thinking 32.43, code 67.52 tok/s (request-level, prompt+generation mixed, one request each); median TTFT 1.93 s. New model, existing hardware, one new A/B group (4-arm config sweep by metric).
- Dataset 3809 -> 3813, models 184 -> 185, quote-verified 4392 -> 4396.

## 2026-10-02: llama.cpp #29869 M3 Ultra (60-core GPU) DFlash2 spec decode few-row MMA (10 rows, 1 new A/B group, 1 new hardware)

- llama.cpp PR #29869 (open): "metal: few-row MMA mat-mul and batched copies for speculative decoding". On Apple GPUs without the tensor API (M1-M4), speculative decoding runs mat-muls with 2..16 src1 rows, whose time grows per row; this PR adds dedicated few-row MMA kernels (Q4_0/Q8_0/Q5_K own kernels, rest generic), MUL_MAT+ADD fusion, and batched f32 copies. Measured on an Apple M3 Ultra (60-core GPU), macOS 15.7.9, Qwen3.8-27B Q4_0 target + DFlash2 Q8_0 drafter, -ngl 99 -fa on -c 8192 -np 1, 64 generated tokens, median of 5 requests, mean of 2 server runs; plus a llama-bench -fa 1 pp512/tg128 no-regression check.
- The finding is a build-to-build reversal: on master DFlash2 (spec decode) on this M3 Ultra is at or below serial (code 30.3, prose 16.8 vs serial ~32.1 tok/s); with the PR it is 3-4x faster than serial (code 113.4, +274%, prose 64.4, +283%). Serial decode is flat (32.1 -> 32.0 code, 32.1 -> 32.1 prose) and the serial llama-bench path does not regress (pp512 317.2 -> 319.8, +0.8%; tg128 32.40 -> 32.44, first of two interleaved runs each).
- 10 rows (DFlash2/serial x code/prose x master/PR decode, T=0, plus llama-bench master/PR), one new M3 Ultra Qwen3.8-27B llama.cpp (Metal) A/B group (master vs this-PR build), new hardware variant "M3 Ultra (60-core GPU)". Dataset 3799 -> 3809, hardware 367 -> 368, quote-verified 4382 -> 4392.
- Also this cycle: fresh issue/PR pulse mined this PR; the rest of the new range above the old watermarks had no clean end-to-end tables (llama.cpp #29864 XMX refactor no table, #29865-29868 bugs, vLLM #59804-59807 bugfixes/metrics). Watermarks advanced -> llama.cpp #29869, vLLM #59807, ExLlamaV2 #821.

## 2026-10-02: HF card Dargoth Qwen3.6-35B-A3B RTX 5090 quant blend (5 rows, 1 new A/B group)

- HF model card Dargoth/Qwen3.6-35B-A3B-Uncensored-Genesis-Hermes-Final-Experimental-GGUF: a custom per-tensor requantizer (Q4_K/Q6_K/Q8_0/NVFP4 blend, each tensor's format chosen by measured element-wise quantization error) of the Hermes3.6-35B-A3B fine-tune of Qwen3.6-35B-A3B, dequantized from the Q8_0 source in memory (no F16/BF16 intermediate). The card's claim is a perplexity-quality win at Q4_K_M-class size, not a speed record.
- Measured llama-bench pp512/tg128 on a single RTX 5090 (32 GB), llama.cpp CUDA build, back-to-back in one session (run-to-run variance ~5%). Five quant variants: Q4_K_M 8316/281, NVFP4 8855/250, Q4_blend2 8566/247, Q4_blend4 8137/258, Q4_blend5 8123/258 (pp512/tg128). Decode speeds cluster 247-281 tok/s; NVFP4 has the fastest prefill (8855) but the slowest decode (250).
- 5 rows (one per quant), new RTX 5090 Qwen3.6-35B-A3B llama.cpp (CUDA) A/B group (quant sweep). Dataset 3794 -> 3799, quote-verified 4377 -> 4382.
- Also this cycle: fresh issue/PR pulse clean (llama.cpp #29858-#29863, vLLM #59789-#59803; #59800/#59802 [Perf] kernel/op microbenchmarks in microseconds parked per convention), discussion pulse clean (0 new comments on all 6 threads). Watermarks advanced -> llama.cpp #29863, vLLM #59803, ExLlamaV2 #821.

## 2026-10-02: HF card LemesoftNostalgic Ornith-1.5-35B-A3B 2 x RTX 3060 (1 row, 1 new model, 1 new hardware)

- HF model card LemesoftNostalgic/Ornith-1.5-35B-A3B-GGUF: an imatrix IQ4_XS quant of ornith-ai/Ornith-1.5-35B-A3B, sized for a 24GB-VRAM-budget rig (2 x RTX 3060). Measured on 2 x RTX 3060 (full-GPU, tensor split), MTP --spec-type draft-mtp n-max 3, mmproj, max ctx 180224, 10 CPU threads.
- The card reports peak fill ~1800 tok/s and peak generation ~120 tok/s (the author's approximations, one run per cell, not a clean benchmark); agentic heavy-KV use hovers 50-90 tok/s. The peak generation rate is MTP-accelerated. Stored as a single community row with the qualifiers noted; new model and new hardware, no A/B group (single arm).
- 1 row. Dataset 3793 -> 3794, hardware 366 -> 367, models 183 -> 184. Quote-verified 4376 -> 4377.

## 2026-10-02: HF card Ornith-1.5-397B-A17B GB10 DFlash n_max sweep (5 rows, 1 new A/B group, 1 new model)

- HF model card cdtio33/Ornith-1.5-397B-IQ2_XXS-DFlash-Drafter-GGUF: a DFlash drafter for the Ornith-1.5-397B-A17B target (finetune of z-lab/Qwen3.5-397B-A17B-DFlash), IQ2_XXS, on an NVIDIA GB10 (DGX Spark) under ik_llama.cpp. Mined the "Choosing n_max" sweep: effective generation tok/s vs draft depth, ~32k prompts, 131072-token q8_0 KV, 256-token generations, one boot two reps.
- The curve rises to n_max=4 and turns over at 5: n_max 0/2/3/4/5 = 15.00/19.07/19.18/19.82/17.72 tok/s. Depths 2, 3 and 4 are not statistically separable on the author's data; n_max=3 ships unchanged (the 4 is a point-estimate peak the author declines to distinguish from 3).
- 5 rows (n_max 0/2/3/4/5 as arms), new GB10 Ornith-1.5-397B-A17B A/B group and new model. Dataset 3788 -> 3793, models 182 -> 183, A/B groups 198 -> 199. Quote-verified 4371 -> 4376.

## 2026-10-02: vLLM #59779 Qwen3 4B B300 watermarking fix no-regression (6 rows, 1 new A/B group)

- vLLM PR #59779 (open): "[Bugfix][Watermarking] Keep draft prompt lengths valid under CUDA graphs". Mined the Performance table: B300, Qwen3-4B + EAGLE3 (AngelSlim/Qwen3-4B_eagle3, K=3, probabilistic), aggregate output tok/s, main vs fix, random 1024 in / 256 out, --ignore-eos, concurrencies 1/8/64.
- This is a no-regression check for a correctness fix, not an optimization: the fix moves output c1 464.7 -> 462.3, c8 3032 -> 3012, c64 10543 -> 10495, every delta within its 95% CI (which includes zero), and mean TTFT rises 0.35-0.65 ms, inside the A/A noise floor. Quant is BF16 (default for the 4B target; not stated in the source).
- 6 rows (3 concurrencies x 2 arms), new B300 Qwen3 4B A/B group. Dataset 3782 -> 3788, A/B groups 197 -> 198. Quote-verified 4365 -> 4371.

## 2026-10-02: vLLM #59778 Qwen3.8-Flash-Next GB10 skinny GEMM (8 rows, 1 new A/B group)

- vLLM PR #59778 (closed): "Tune the Qwen3.8-Flash-Next skinny GEMMs for GB10 (sm_121)". Enables the CuTe skinny-GEMM table for sm_121 (GB10) on Qwen3.8-Flash-Next-NVFP4, MTP, single GB10 TP=1, ISL 2048/OSL 256.
- The source reports aiperf TPOT in ms/token (lower is better), n=3 per arm, not tok/s. The raw TPOT is stored as the value with the unit noted on each row, because the converted tok/s does not appear verbatim in the source and so cannot be quote-verified. Baseline (no table) vs with-table: bs=1 k=3 48.14 -> 44.86 (-6.8%), bs=1 k=1 47.70 -> 46.32 (-2.9%), bs=2 k=3 55.28 -> 54.28 (-1.8%), bs=4 k=3 73.43 -> 72.64 (-1.1%). The gain is largest at low batch (small M) and shrinks as batch approaches the kernel's M<=16 limit; 84% of the gain is the LM head.
- 8 rows (4 configs x 2 arms), new GB10 A/B group. Dataset 3774 -> 3782, A/B groups 196 -> 197. Quote-verified 4357 -> 4365.

## 2026-10-02: vLLM #59740 "Other hardware" table (18 rows, 1 new A/B group)

- vLLM PR #59740 (MTP draft-vocab list): mined the "Other hardware" table (Qwen3.6-35B-A3B-NVFP4 BF16 head on RTX 5090; Qwen3.8-Flash-Next-NVFP4 on GB200 TP1/TP2). 32k draft-vocab list vs full-vocab stock arm, 56 prompts, 384 output tokens, absolute decode tok/s.
- Cross-hardware comparison: the 32k list is a clear win on RTX 5090 (BS1 357.8 -> 394.6 +10.3%, BS4 1180 -> 1257, BS8 1968 -> 2072) but a net loss on GB200 TP1 (BS1 448 -> 435, BS16 3827 -> 3510) and TP2 (BS1 466 -> 434). The reason is the lm_head read share: it is a bigger fraction of the step on RTX 5090 / GB10, so the head-traffic saving dominates; on GB200 the list's AL loss on mixed traffic outweighs it. New RTX 5090 A/B group; GB200 group gains the 32k TP1/TP2 rows alongside the per-domain 64k rows.
- 18 rows, dataset 3756 -> 3774, A/B groups 195 -> 196. Quote-verified 4339 -> 4357.

## 2026-10-02: vLLM #59740 per-domain 64k-list table (36 rows, 1 new A/B group)

- vLLM PR #59740 (MTP draft-vocab list): mined the "Acceptance and speed by domain, 64k list" table (Qwen3.8-Flash-Next-NVFP4, MTP 3-draft-token, BS1, 16 prompts per domain, 256 output tokens; full-vocab stock arm vs 64k list arm). 8 domains (Spec-Bench multi-turn, translation, summarization, QA, math, RAG; HumanEval code; BFCL tool calling) plus pooled, on GB10 (DGX Spark) and GB200 (new hardware for the dataset).
- The 64k list beats the stock arm on every domain: GB10 pooled 40.2 -> 50.8 (+26.6%, best QA +32%, weakest math +26%), GB200 pooled 459 -> 489 (+6.7%, best translation +16%, weakest math +4%). The GB200 gain is far smaller because on GB200 the lm_head read is a small share of the step, so the list's AL loss on mixed traffic outweighs the head-traffic saving (the 32k list is a net loss on GB200 TP1).
- New GB200 A/B group; the GB10 group gains the per-domain rows alongside the headline. 36 rows, dataset 3720 -> 3756, hardware 365 -> 366, A/B groups 194 -> 195. Quote-verified 4303 -> 4339.

## 2026-10-02: vLLM #59740 re-mine after PR description rewrite (8 rows)

- vLLM PR #59740 (MTP draft-vocab list) was rewritten by the author: the old headline table (41.38/51.05/51.2/51.24/106.6/117.1/117.6) is gone. CI's cold-cache quote check caught the drift. Re-mined the 8 rows from the new headline (Qwen3.8-Flash-Next-NVFP4, 1x DGX Spark GB10, 3 draft tokens, 12 prompts, 384 output tokens): full (stock) 41.41/107.1, 32k list 50.89/117.5 (+22.9% / +9.7%), forced equal AL 3.00 full 39.96/106.6, forced equal AL 3.00 32k 51.65/119.5. Dropped the 32k-corpus and 64k-gen arms (no longer in the source); A/B note rewritten around the forced-AL comparison. Row count unchanged (8 -> 8).

## 2026-10-02: HF card MiMo-V2.6-Flash-RL-UNCENSORED on Gorgon Halo (4 rows)

- HF model card cafonez/MiMo-V2.6-Flash-RL-UNCENSORED-Gorgon-GGUF: Framework Desktop (Gorgon Halo, Ryzen AI Max+ PRO 495 / Radeon 8065S, 192 GB LPDDR5X), llama.cpp Vulkan via ROCmFPX main (fused gate/up expert tensors, from PR #33), llama-bench -fa 1 -b 2048 -ub 2048, 3 runs. 309.8B MoE at 4.29 bpw (MXFP4 experts, Q5_K attention/dense/MTP). pp2048 484.9, decode 23.6; at 32K context pp2048 258.7, decode 22.1. New A/B group for the context-depth decay.
- 4 rows, dataset 3716 -> 3720, A/B groups 193 -> 194. Quote-verified 4299 -> 4303.

## 2026-10-02: HF card Qwen3.5-0.8B-Japanese-SFT on Apple M5 (4 rows)

- HF model card Takenoko12345678/Qwen3.5-0.8B-Japanese-SFT-GGUF: Apple M5, llama-bench, generation 128 tokens. Q8_0: CPU 4 threads 78 tok/s, Metal GPU 123 tok/s. Q4_K_M: CPU 92 tok/s, GPU 169 tok/s. Figures are approximate (約). 0.8 B Japanese SFT; new model page.
- 4 rows, dataset 3712 -> 3716, models 181 -> 182. Quote-verified 4295 -> 4299.

## 2026-10-02: HF card Luigi Gemma-4-E2B meeting agent (1 row) + Gyro tps-in-quote fix

- HF model card Luigi/gemma-4-E2B-meeting-agent-zh-GGUF: OPPO Reno7 (Dimensity 900), CPU only, llama.cpp 8 threads. Real-speed replay of a 2 h 08 zh-TW meeting (lag 67 s median, 115 s max, no drift). Effective speed 16 tok/s prefill, 4.5 tok/s decode. QAT Q4_0 meeting-agent fine-tune, 8k context restart. Numbers are the effective replay speed, not a clean llama-bench run.
- Fixed 3 Gyro rows (r9700-1x, r9700-mtp-copy-off, 2xr9700) whose HF3 re-mine truncated the tps value at the last digit (57.8, 57.5, 37.6); added the throughput/prose line carrying each value as a verbatim fragment.
- 1 new row (dataset 3711 -> 3712, hardware 364 -> 365). Quote-verified 4294 -> 4295.

## 2026-10-02: Strix Halo llama 7B Q4_0 (6 rows, 3 new A/B groups)

- llama.cpp discussions #10879 (@ddpasa): AMD Strix Halo (Ryzen AI Max+ 395 CPU, Radeon 8060S iGPU), llama 7B Q4_0, llama-bench pp512/tg128, fa=0 vs fa=1. CPU 16 threads: pp 300.27 -> 340.11, tg 27.68 -> 29.52. ROCm ngl 100: pp 1313.76 -> 1456.15, tg 47.36 -> 51.33. Vulkan ngl 100: pp 1487.08 -> 1704.30, tg 51.81 -> 54.38.
- Cross-backend at fa=1: Vulkan leads on both axes (decode 54.38, prefill 1704.30), ahead of ROCm (51.33 / 1456.15) and far ahead of CPU (29.52 / 340.11). Reporter: Vulkan has improved a lot on Strix Halo and is now destroying ROCm.
- 6 rows, 3 new A/B groups (CPU, ROCm, Vulkan fa 0/1) with notes (page now 193 of 193).

## 2026-10-02: vLLM #59740 MTP draft-vocab list (8 rows, 1 new A/B group)

- vLLM PR #59740 (1x DGX Spark, GB10 SM121, Qwen3.8-Flash-Next-NVFP4, 3 draft tokens): letting the MTP drafters project onto a 32k-token list (speculative_config.draft_token_map) instead of the full 248k vocabulary. Decode tok/s, full (stock) -> 32k gen (94.9% coverage), per-stream at BS1 and aggregate at BS4: BS1 41.38 -> 51.20 (+23.7%), BS4 106.6 -> 117.1 (+9.9%); 32k corpus 51.05 / 117.0 and 64k gen 51.24 / 117.6 at BS1/BS4, all within a fraction of a percent of 32k gen. GSM8K 245 -> 246, within noise; at forced equal AL 3.00 the 32k gen list still leads (BS1 52.46 vs 40.01), so the gain is not just the acceptance-length shift.
- 8 rows, 1 new A/B group with note (page now 190 of 190).

## 2026-10-02: vLLM #59732 + #59733 (12 rows, 2 new A/B groups)

- vLLM PR #59732 (MI355X TP2, Qwen3.8-Flash-Next-Quark-MXFP4): the fused QSA prepare launch folds the main-attention QK-norm, RoPE, gate split and K/V cache write into the prepare launch, as already done for NVIDIA. Output tok/s, unfused -> fused: 8192/1024 c4 462.0 -> 475.5, c16 964.1 -> 975.3, c64 1457.2 -> 1471.0; 60000/600 c4 144.8 -> 147.4. +0.9% to +2.9%, all 8 measured cells faster; GSM8K 0.9638 -> 0.9605, within run-to-run noise.
- vLLM PR #59733 (MI355X TP8, Kimi-K3 MXFP4 + DSpark draft): #57652 dropped the KV cache from 4 to 20 groups because the DSpark draft spec omitted max_tp_shards, so the MLA layers stopped merging; the fix declares max_tp_shards=1 to restore the 4-group layout. 4-build A/B, output tok/s: pre-#57652 nightly 648, current nightly with #57652 623, full revert 646, this PR 647; restores pre-#57652 throughput, median TPOT 11.47 -> 11.09 ms.
- 12 rows, 2 new A/B groups with notes (page now 189 of 189).

## 2026-10-02: IBM Z NNPA zDNN Q8_0 matmul (16 rows, 1 new A/B group)

- llama.cpp PR #29836: Q8_0 matrix-multiplication support added to the IBM zDNN backend, tested on the IBM Z Neural Network Processing Assist (NNPA) coprocessor, llama 1B Q8_0, build feat/zdnn-i8-upscale vs baseline b11284. The gain is dramatic for prompt processing and modest for decode: pp512 25.81 -> 249.62 tok/s (9.67x), tg128 9.02 -> 12.53 tok/s (1.39x). The multiplier shrinks as the @d context/KV depth grows: pp512 4.71x at d1024 to 2.39x at d4096, tg128 1.17x at d1024 to 1.06x at d4096. Eight tests (pp512/tg128 at the base context and @d1024/@d2048/@d4096) x 2 builds.
- 16 rows, 1 new A/B group with note (page now 187 of 187). New hardware page (IBM Z NNPA), new backend (llama.cpp (zDNN)).

## 2026-10-02: Radeon RX 9060 XT fa A/B on Vulkan and ROCm (10 rows, 2 new A/B groups)

- llama.cpp #10879 (Vulkan) and #15021 (ROCm), comments 18709094/18709095: AMD Radeon RX 9060 XT (16 GB GDDR6, 128-bit bus, gfx1200), build f1cee99, Ryzen 5 7600X, llama 7B Q4_0. Vulkan (Mesa RADV 26.2.2, RADV_PERFTEST=nogttspill, -ngl 100) fa=0 -> fa=1: pp512 2844.80 -> 3228.15, tg128 71.07 -> 74.01. ROCm 7.2.4 (-DGGML_HIP=ON, -ngl 99) fa=0 -> fa=1: pp512 2641.07 -> 3014.51, tg128 67.27 -> 70.18. Vulkan still leads this RDNA4 card on both (decode 74.01 vs 70.18, prefill 3228.15 vs 3014.51).
- Larger-model table on the same card (-ngl 99 -fa 1, pp512/tg128, Vulkan/HIP): gpt-oss-20b MXFP4 3464/105.8 vs 3372/92.8, Qwen3.8-27B UD-IQ4_XS 709/20.1 vs 738/19.5, Gemma 4 12B Q4_K_M 1509/39.0 vs 1467/37.6. Reporter notes the 128-bit (not 256-bit) bus and a large build-over-build prefill gain vs the older RX 9060 XT scoreboard entries (Vulkan pp512 +33%/+69%, ROCm +86%/+104% no-FA/FA).
- 10 rows, 2 new A/B groups with notes (page now 186 of 186).

## 2026-10-02: Coverage backfill, 13 rows from previously unmined comments (3 new A/B groups)

- llama.cpp #4167 (Apple Silicon), comment 18555918: M2 Max (30 GPU, 32 GB), Metal. Qwen3.6-35B-A3B Q4_K_M (MoE, 3B active): pp4096 671.40 / tg128 58.56 tok/s. Qwen3.8-27B dense IQ3_S: pp4096 106.78 / tg128 10.82 (architecture swamps quantization: 5.4x slower decode than the MoE). An MTP sweep (--spec-type draft-mtp, 32k window, q8_0 KV, ollama) is a net loss on this chip and degrades monotonically with draft depth: no-draft 46.2, n=2 34.6, n=4 29.4, n=6 20.1, n=8 17.1 tok/s.
- llama.cpp #15021 (ROCm), comment 18378967: AMD Radeon Pro V620 (gfx1030, 32 GB) on ROCm v10, llama.cpp 434ddbbc0, llama 7B Q4_0. Single card fa=0 -> fa=1: pp512 1846.20 -> 2173.13, tg128 91.70 -> 98.78. Two cards in parallel: pp512 1801.75 -> 2146.36, tg128 64.85 -> 71.38. The second card holds prefill (-1.2%) but costs 27.7% of decode (71.38 vs 98.78): tensor-parallel sync, not bandwidth, is the bottleneck for a 3.56 GiB model.
- llama.cpp #23313 (Intel Arc), comment 18474926: Arc A770 (i7-13700K, Ubuntu 24.04, 64 GB DDR5), llama.cpp 2cdae802e, SYCL, llama 7B Q4_0, -ctk f16 -ctv f16. fa=0 -> fa=1: pp512 826.15 -> 979.76, tg128 47.81 -> 54.38.
- 13 rows, 3 new A/B groups with notes (page now 184 of 184); the M2 Max Qwen3.8-27B group (shared with the DFlash2 rows) now carries 12 rows under one note. Two new hardware pages (V620, 2x V620).

## 2026-10-02: llama.cpp #15013 P102-100 10 GB BIOS-mod run (2 rows, VRAM 5/10 GB A/B)

- llama.cpp discussion #15013 (CUDA), comment 18695871: a P102-100 mining card (Pascal) BIOS-modded from 5 GB to 10 GB, llama 7B Q4_0. The 10 GB card runs fa=0 / fa=1 at pp512 935.02 / tg128 46.77 and pp512 1032.13 / tg128 49.59, versus 927.54 / 46.45 and 1029.43 / 49.08 for the stock 5 GB card (comment 18693775). The extra VRAM is nearly neutral (the 7B Q4_0 fits in 5 GB with room for KV): +0.8% prefill / +0.7% decode at fa=0, +0.3% / +1.0% at fa=1. The group is now a 2x2 (VRAM 5/10 GB x fa 0/1) under one note.

## 2026-10-02: HF model cards mined (40 rows, 6 new A/B groups)

- Four fresh HF model cards with measured performance sections:
- cafonez GLM-5.3-Flash Gorgon GGUF: GLM-5.3-Flash (320.8B MoE) Q5K-IQ3S mix (3.84 bpw) on a Gorgon Halo (Radeon 8065S, 192 GB) with the ROCmFPX Vulkan build. llama-bench -fa 1 -b 2048 -ub 2048: prefill 256.4, decode 17.4 t/s; at 32K context 95.9 / 15.0. Plain llama.cpp master runs the file at the same decode speed, slower prefill.
- lackonendes PAW-27B-X3.1: Qwen3.8-27B 3.5 bpw trellis-quantized build (llama-paw CUDA fork) on one RTX 3090 at full 262144 context: generation with the DFlash2 drafter, coding 129.09 / new code 73.74 tok/s vs 30.16 no-drafter; prompt processing 982.87 short, up to 1268.67 (peak) on an 8k-token prompt.
- agentionai Qwen3.8-Flash-Next Gyro GGUF (rotor formats, agentionai/llama.cpp): R9700 pp512 1246 / tg128 57.8, 2x R9700 919 / 37.6 (one card beats two), RTX 5090 CUDA pp512 296 / tg128 101-118 plus content-stratified decode at 16k (prose 99, JSON 106, code 101, copied 108) and context-fill decay (118/106/91/72 at empty/8k/32k/64k); Strix Halo 8060S Gyro-S 250 / 31.7, Gyro-M 249 / 26.4, AP-Q4_K_XL 309 / 27.2. MTP drafting: R9700 generating code 56.9 -> 70.6 (+24%), copying 57.5 -> 86.1 (+50%); Strix Halo prose 32 -> 39, code 32 -> 52, JSON 32 -> 58, editing/copying 32 -> 61.
- VisualInference Qwen3.8-27B AEON 6-bit MLX (vision tower preserved, native MTP drafter): Mac mini M4 Pro 48 GB, serial 11.4 tok/s (~100% of the streaming-bandwidth roofline), MTP coding 21.5 (block 4), document QA at 13k ctx 16.9, creative prose 15.9 (block 3), prefill ~105-110.
- 40 rows, 6 new build A/B groups with interpretive notes (page now 181 of 181), two new hardware pages (Radeon 8065S, 2x R9700). The abliterated Gyro re-release was skipped: same measurements restated.


## 2026-10-02: llama.cpp #23313 tail comments mined (14 rows)

- llama.cpp discussion #23313 (Intel Arc thread): two late comments. c18467211 (cbelcher): Arc Pro B70 VFIO-passthrough into a Proxmox VM (Xeon E5-2699 v4, 64 GB DDR4), SYCL F16 build, llama 7B Q4_0 fa A/B: prefill 1324.76 -> 3271.16 tok/s (2.47x), generation 107.11 -> 111.13 (+3.8%). c18629941 (NickM-27): qwen35 27B Q6_K (Qwen3.8-27B), latest SYCL, prompt-depth decay at fixed pp2048/tg256: 1212.47/21.32 at no depth, 1029.24/19.60 at d8192, 968.59/18.15 at d16384; plus mtp-bench (MTP spec decode) per prompt type: code_python 40.9 tok/s (acceptance 0.936) down to long_code_review 28.0 (0.653), best cell ~1.9x the bare 21.32. 14 rows, 2 new A/B groups with notes (page now 175 of 175). check_quotes: the pp/tg test-token check now also falls back to the REST API body for client-rendered comments (same path as the number check).

## 2026-10-02: llama.cpp #27593 mine (43 rows, Arc Pro B70 SYCL tuning)

- llama.cpp discussion #27593 ("Squeezing Every Token/s from the Intel Arc Pro B70"): a full SYCL tuning log on one 32 GB B70 (BMG G31, Qwen3.8-27B Q8_0, master 63b64a50a, oneAPI 2026.1). Headline: -DGGML_SYCL_F16 OFF -> ON is 389.2 -> 1446.8 tok/s pp2048 (3.72x) with generation flat, and the flag is OFF in the CMake default. Also mined: the built-in MTP sweep (short answers 15.73 -> 50.92 tok/s at n-max 6, long answers peak at 33.53 at n-max 3, acceptance 0.87 -> 0.40), the -ub sweep (+34.8% prefill at 512 -> 2048), -fa 1 (+6 to +9% prefill), KV-quant context fit (f16 49152 / q8_0 65536 / q4_0 131072, tg128 15.79/15.72/15.69), a 15-arm SYCL env-var sweep (ENABLE_OPT=0 costs 68% of generation; LEVEL_ZERO_V2=0 is +1.4% free; FA_ONEDNN=0 trades -5% prefill for +3% generation), and a comment-18692471 single-vs-dual B70 comparison (1149.66 vs 855.54 tok/s PP at 4096 tokens, tensor 50,50 over PCIe gen4 x16, -25.6%). 43 rows, one new A/B group with interpretive note (page now 173 of 173).

## 2026-10-02: llama.cpp performance threads, 9 new comments mined (42 rows)

- llama.cpp discussions #10879 (Vulkan) and #15021 (ROCm): fresh scoreboard comments. A desktop RX 6800 (RADV 26.2.2 with nogttspill vs ROCm 7.2.4, same commit f1cee99): fa A/B on both backends, and a cross-backend table for gpt-oss 20B / Qwen3.8-27B IQ4_XS / Gemma 4 12B; Vulkan generates ~18% faster on RDNA2, ROCm only wins prefill with FA on. An R9700 (RDNA4) comment shows ROCm falling off hard with prompt length (pp512 5039.78 -> pp8192 2755.01) while Vulkan stays steady (5411.28 -> 4235.87), a 54% gap at 8k that inverts on MoE. New hardware pages: Arc B390 (FA collapses pp8192 by -57%), Arc 140V (FA neutral), P102-100 mining card (Pascal, 5 GB, 46.45 tok/s 7B decode).
- llama.cpp discussions #4167 (Apple Silicon): first llama.cpp Metal numbers for an M5 Ultra (36/80, 256 GB): 7B decode 73.60 -> 119.01 -> 179.10 tok/s across F16/Q8_0/Q4_0 with prefill flat, and a Mac mini M6 (11.59 -> 21.01 -> 35.74 tok/s). A DFlash2 spec-decode test on an M2 Max loses on every prompt type on both a dense 27B (prose 10.29 -> 6.13, -40%) and a 35B-A3B MoE (prose 51.02 -> 30.79, -40%) despite 76% acceptance, because the drafter costs more than it saves on Metal.
- 42 rows, 11 new build A/B groups with interpretive notes (page now 172 of 172). check_quotes now walks full discussion pagination and falls back to the GitHub REST API for comment bodies that are client-rendered and absent from every server-rendered page (the DFlash2 comment).

## 2026-10-02: vLLM #59701 mine (8 rows)

- vLLM #59701 (PR): migration of GPT-NeoX/Phi/Seed-OSS/Jais2 to the Transformers modeling backend. 1x B200 per model, vllm bench throughput 1024/256 x 1000 prompts, main vs branch, one run per cell: pythia-12b 2,912 -> 2,911, phi-2 5,144 -> 5,155, Seed-OSS-36B-Base 1,540 -> 1,542, Jais-2-8B-Chat 5,324 -> 5,359 tok/s; author states the +-1% spread is noise (parity checks). 8 rows, 4 new model pages, 4 new A/B groups (page now 162 of 162).

## 2026-10-02: vLLM #59594 + #59607 mine (21 rows)

- vLLM #59594 (PR): KV-cache layout fallback fix (BLNHC -> BLHNC when a KV connector needs head-major pages). RTX PRO 6000 TP2, Qwen3.8-Flash-Next, 8K in / 1K out, output tok/s at c=1/4/16/32/64 with and without MTP3 speculation: all ten cells within +-2% (worst -2% at MTP c4), p50 TPOT identical; the fix is functional (BLNHC fails the Mooncake handshake at TP1 prefill, local=39739392 vs remote=1605632). 20 rows, parity A/B group.
- vLLM #59607 (issue): Xid 31 MMU fault under CUDA-graph replay in the EP16 FP8 MoE path, Qwen3-Coder-480B-A35B-Instruct-FP8 (new model page) on 2x8 H200 over RoCE; --enforce-eager workaround measured ~583 tok/s at conc 16 with TPOT ~80 ms vs the 30-50 ms target (cudagraph single-node reference TPOT ~16 ms). 1 row, no A/B arm.
- One new build A/B group with interpretive note (page now 158 of 158).

## 2026-10-02: llama.cpp #29772 + vLLM #59600 + #59606 + #59514 + #59679 mine (17 rows)

- llama.cpp #29772 (PR): Vulkan FWHT extended from block width 512 to 8192. Radeon 860M (RDNA 3.5), Bonsai 2 27B Q2_0: tg64 7.26 -> 8.17, pp512 59.2 -> 66.4, pp2048 55.8 -> 62.2 t/s (+12 to 13%), KLD unchanged; the width-8192 op drops 76.4 ms -> 2.0 ms. 2 rows.
- vLLM #59600 (PR): ShortConv drafter state restore in the V2 runner. Radeon 8060S (gfx1151) TP1 BF16, LFM2.5-1.2B + LFM2.5-350M drafter K=3, GSM8K 32-question offline output tok/s: 496.40 -> 663.49 (+33.7%), acceptance 71.83%, accuracy 16/32 both arms. 2 rows.
- vLLM #59606 (issue): b12x native NVFP4 MoE backend on DGX Spark (GB10, SM121) TP2, CYBER-FROST-3.8-NVFP4 (new model page) with MTP k=3: 8-stream decode 155.6 (flashinfer_cutlass) vs 137.6 tok/s (b12x, -11.6%), 43 vs 48 ms per step at 1 stream; b12x also crashes on padded graph capture and on a 6,941-token prefill. 2 rows.
- vLLM #59514 (PR): flat-grid silu_and_mul_quant fix (dead vector loop, fp32 fast-math chain). H100, Llama 3.1 8B FP8, vllm bench serve, three interleaved rounds per arm: main kernel 4821 -> PR 5005 (+3.8%), Inductor path 4977 (+0.6% vs PR, noise); fused-op GPU time 69.87 -> 27.63 ms per iteration, mean TPOT 73.31 -> 70.66 ms. 3 rows.
- vLLM #59679 (PR): Glm/Arcee/CWM/Mellum migration to the Transformers modeling backend, B200 throughput bench 1024/256 x 1000 prompts, main vs branch: GLM-4-9B-Chat 7,481 -> 7,591, AFM-4.5B-Base 13,657 -> 13,820, facebook/cwm 1,761 -> 1,766, Mellum2-12B-A2.5B-Base 16,604 -> 16,498 tok/s; author states the +-1.5% spread is noise (parity checks). 8 rows, 4 new model pages.
- Eight new build A/B groups with interpretive notes (page now 157 of 157).

## 2026-10-02: vLLM #59655 mine (18 rows)

- vLLM #59655 (PR): NVFP4 DeepSeek V4.1 Flash checkpoints silently mis-quantize the bundled MXFP4 MTP/DSpark draft experts, so every draft token is rejected (acceptance length 1.00) and speculation is pure overhead. GB300 TP4, DSpark k=5, MT-Bench 80 prompts greedy, vllm bench serve output tok/s, all arms run on each of three nodes (node spread up to ~25%): v0.30.0 -> fixed at concurrency 1: 114 -> 250 / 273 / 280 (2.19x / 2.39x / 2.45x); at concurrency 8: 773 -> 1471, 796 -> 1554, 766 -> 1595 (1.90x / 1.95x / 2.08x). Native deepseek-ai checkpoint arm lands -13.1% to +0.4% off the PR (author's rotated back-to-back runs: +2.5%, node noise). Median TPOT at c1 8.49 -> 3.28 ms, native 3.06 ms. GSM8K accuracy unchanged either way. 18 rows, one new A/B group with interpretive note (page now 149 of 149).

## 2026-10-01: llama.cpp discussions #10879 re-mine + Steam Deck and Strix Halo data (27 rows net)

- llama.cpp discussions #10879 (Vulkan performance thread): upstream edited two comments the dataset was anchored to. The RX 5700 XT rows moved to a surviving comment (439.42 / 70.13 t/s, llama-bench pp512/tg128, RX 5700 XT, RADV NAVI10); three rows whose source comment was deleted were dropped.
- New: 24-row flash-attention A/B matrix from a Steam Deck (AMD Custom GPU 0932, VANGOGH iGPU, llama-b10360, -ngl 100), 12 models x fa off/on, llama-bench pp512/tg128. fa is worth up to +14% prefill (llama 7B 144.31 to 164.34) and +7% decode (Nanbeige4.2-3B 15.27 to 16.36), costs a point or two on Qwen3.8-9B and gemma-4-E4B, and is a wash on the IQ2_XXS quants. 12 new A/B groups.
- New: 14-row Vulkan vs ROCm matrix on a Radeon 8060S Strix Halo iGPU (master 2026-08, single-request chat decode), 4 models x 2 backends x bare/MTP. Vulkan wins bare MoE by +18.5% to +25.5% and dense by ~+2%; MTP adds +16% to +99% and widens the backend gap to +15% to +20%. 6 new A/B groups (Qwen3.6-35B-A3B-APEX, Hy-MT2-30B-A3B, Qwopus3.6-27B-Coder, Qwen3.8-27B-AD).
- check_quotes: discussion threads now verify against the union of all pagination pages (GitHub can render a comment's body and its anchor on different pages), and numbers are also matched inside raw HTML when text extraction misses them. check_data ignores thousands separators inside quotes.
- Eighteen new build A/B groups with interpretive notes (page now 148 of 148).

## 2026-10-01: vLLM #59668 + #59653 + #59567 + #59520 + #59548 mine (63 rows)

- vLLM #59668 (PR): single-launch DSA decode candidate mask on ROCm. MI355X, DeepSeek V4.1 (new model page), TP4 + EP, FP8, vllm bench serve output throughput at 12 input/output x concurrency points, stock four-kernel mask vs fused single kernel: mean +0.44% throughput, -0.48% TPOT; e.g. 8192/1024 c16 1262.90 to 1273.77, c256 3814.25 to 3827.03, 128000/1024 c4 185.73 to 186.21. Kernel-level mask speedups 1.06x to 2.50x. GSM8K unchanged within error. 24 rows.
- One new build A/B group with interpretive note (page now 125 of 125).
- vLLM #59653 (PR): fused sparse-layer decode for MiniMax-M3 on ROCm via AITER (one kernel per sparse MoE layer, TP all-reduces inside). 4x MI350X (new hardware page), MXFP4, TP4, FP8 KV. Decode 8K/256 output tok/s unfused -> fused: c1 141 -> 254 (1.95x, TPOT 6.14 -> 3.15 ms), c2 254 -> 405, c4 415 -> 574, c8 599 -> 682, c16 825 -> 910. Serving 128K/1K: c2 157 -> 195 (+24%), c4 206 -> 243, c8 246 -> 273. GSM8K 0.948 both ways. 16 rows.
- vLLM #59567 (PR): batch sampling-mask transport. GB300, Qwen3-8B, c=256, output tok/s with no mask / stock mask path / this PR: 1024/1024 16515 / 15705 (-4.9%) / 16364 (-0.9%); 256/256 25515 / 23488 (-7.9%) / 24811 (-2.8%); 256/256 wide (50 ids/token) 25781 / 21249 (-17.6%) / 22873 (-11.3%). 9 rows.
- vLLM #59520 (issue): default CUDA GDN wrapper regresses non-spec Qwen3.5 decode. 2x H200 TP2, Qwen3.5-9B BF16, throughput bench 200 requests / 204,800 output tokens, CUDA default -> Triton: sparse prefix retention 1426.638 -> 1859.655 (+30.35%), dense 1536.536 -> 2069.343 (+34.68%). vLLM 0.29.0. 4 rows.
- vLLM #59548 (issue): spec-decode boot-to-boot dispersion. Qwen3-4B + DFlash-b16 drafter, concurrency 1, mean of 12 boots per arm. L4, vLLM 0.29.0: CUDA-graph default vs enforce-eager 39.2 vs 80.5 (ratio 0.487, CV 13.92%) and 61.2 vs 79.7 (0.768, 3.73%); vLLM 0.30.0 reaches parity: 82.8 vs 81.6 (1.014) and 78.2 vs 77.0 (1.017). A10 on 0.29.0 nearly immune: 132.6 vs 138.3 (0.959). 10 rows.
- Four new build A/B groups with interpretive notes (page now 130 of 130).

## 2026-10-01: llama.cpp #29820 + #29809 + #29807 + #29769 + #29784 + #29824 + #29779 mine (72 rows) + #29768 rebuild

- llama.cpp #29820 (issue): ROCm/HIP patch lowering MMVQ_MAX_BATCH_SIZE from 8 to 4 for gfx1201. Radeon AI PRO R9700, Qwopus3.8-27B-Flash-V2 Q4_K_M (new model page), llama-batched-bench -c 32768 -npp 512 -ntg 128, -ctk q8_0 -ctv q4_0, stock vs patched TG t/s at 1/2/4/5/6/8/16 sequences: flat at 1/2/4/16, +13% at 5 (81.1 to 91.8), +24% at 6 (84.4 to 104.9), +44% at 8 (88.6 to 127.3). Perplexity unchanged. 14 rows.
- llama.cpp #29809 (PR): SYCL MXFP4 MoE arithmetic decoding + weight reordering. Intel Arc Pro B70, gpt-oss: 20B decode on one card 55.84 to 106.64 tok/s (1.91x, 5 reps), 120B decode on two cards 33.27 to 67.14 (2.02x, 2 reps), 120B prompt processing 594.5 to 600.1. Windows 11, oneAPI 2026.0, EPYC 7402P host, FA on. 6 rows.
- llama.cpp #29807 (PR): remove redundant CUDA copies after SSM_SCAN. RTX PRO 6000 Blackwell (new hardware page, edition not stated by the author), nemotron_h_moe 31B.A3.5B Q4_K_M, Windows. MTP off: flat (pp512 11485.61 to 11474.42, tg128 313.28 to 314.14). MTP on (draft-mtp, acceptance 0.777 identical): SPEED-Bench coding decode 432.58 to 447.63 t/s, 1.035x, faster on 80 of 80 prompts. 6 rows.
- llama.cpp #29769 (PR): unified decode masks in one cache scan. RTX 5090, Qwen3.8-27B Q4_K_M, F16 KV. Fast path llama-batched-bench -c 131072 -npp 15872 -ntg 512 -npl 8: medians 274.54 to 291.21 tok/s, +5.77% (95% CI +5.11% to +6.43%). Sanity runs (fast path not triggered): pp512 3731.18 to 3718.85 (-0.33%), tg128 78.67 to 78.49 (-0.23%). 6 rows.
- llama.cpp #29784 (PR): CPU thread default on Apple Super+Performance cluster chips (sum all perflevel physicalcpu). M5 Max, muse-glimmer 30B Q4_K_XL, llama-bench -ngl 0 -r 3 CPU-only, threads 6 to 18: pp512 26.98 to 58.76 t/s (2.18x), tg128 9.24 to 13.64 (1.48x). 4 rows.
- llama.cpp #29824 (PR): qwen4exp mask construction repeats rows instead of 1-element seeds (slow graph on Metal). M2 Ultra, Qwen3.8-Flash-Next GGUF, batched-bench B=1 ntg=32, ctx 2048 to 65536. Prompt processing recovers the #29751 long-context regression and beats pre-#29751: 65536 528.55 to 754.63 (pre was 690.15), 32768 637.29 to 781.91. Decode roughly flat. 12 rows.
- llama.cpp #29779 (PR): Hexagon matmul flattened 3D to 2D to run on HMX instead of HVX. IQ-9075 (new hardware page), llama-batched-bench -c 4096 -npp 128 -ntg 32, npl 1/2/4. Qwen3.5-2B Q4_0 (new model page): flat at 1 sequence, pp128 x2 452.70 to 719.49 (+58.9%), x4 445.93 to 703.51 (+57.8%), decode +2%. LFM2-2.6B Q4_0 (new model page): flat at 1 sequence, pp128 x2 209.92 to 687.22 (+227.4%), x4 209.26 to 679.47 (+224.7%), decode +2%. 24 rows.
- Eight new build A/B groups with interpretive notes (page now 124 of 124).
- llama.cpp #29768 rebuilt after a second same-day upstream rewrite: the old npl8-only paragraph (295.80 to 299.82) was replaced by a 5-arm table (npl 8/6/4/2/1, warmup-reset counts, 95% CIs). The 2 stale rows were dropped and replaced by 10 rows: npl 8 296.0 to 300.3 (+1.28%), npl 6 230.4 to 232.0 (+0.85%), npl 4 182.3 to 184.3 (+0.93%), npl 2 102.5 to 102.9 (+0.27%), npl 1 54.5 to 54.3 (-0.30%). The rewritten body names the model only as qwen35 (the llama.cpp internal name; the earlier revision said Qwen3.8-27B Q4_K_M), so the rows moved to a qwen35 model page.

## 2026-09-30: llama.cpp #29768 + vLLM #59488/#59489 mine (6 rows after the 2026-10-01 upstream rewrite of #59488)

- llama.cpp #29768 (PR): CUDA graph repeated-warmup avoidance. RTX 5090 (CC 12.0, Windows, CUDA 12.9), Qwen3.8-27B Q4_K_M, F16 KV, llama-batched-bench -c 131072 -npp 15872 -ntg 512 -npl 8 -kvu: decode TPS 295.80 (without) vs 299.82 (with), +1.14% (95% CI +0.44% to +1.84%). 2 rows.
- vLLM #59489 (PR): Rust vllm-bench openai-responses backend parity. RTX 3070, Qwen3-0.6B with reasoning parser, bench serve random 512/128 c16, 200 prompts: output throughput Rust 1676-1680 vs Python 1671-1673 tok/s, 200/200 both, TPOT/ITL within noise. 2 rows, new model page.
- vLLM #59488 (draft PR): DeepSeek-V4.1-Flash MXFP4 MoE backend default change on 8x H200 (SM90). Upstream rewrote the body on 2026-10-01 and removed the original 6-layout x 5-workload serving table (60 rows dropped). The surviving absolute figures, TP8+EP with per-token FP8 activations, offline LLM runs, decode 64 prompts x 512 in / 256 out, 2 repeats: Marlin 2648 vs Humming grouped 2222 output tok/s (grouped 16% behind Marlin; the PR's new indexed-GEMM default is 14% faster than grouped, percentage only, no absolute published). The rewritten body also reports indexed vs grouped at +47% prefill / +63% decode (BF16) and +24% / +36% (FP8), percentages only. 2 rows.
- Three new build A/B groups with interpretive notes (page now 115 of 115).


## 2026-09-30: vLLM #59434 Zen CPU f32 expert scales mine (4 rows)

- vLLM #59434 (2026-09-30, PR): ZenCPUExpertsInt8 now passes f32 expert scales to the ZenDNN fused MoE executor instead of bf16 (which silently failed the f32-only eligibility gate and fell back to the generic per-expert path). Throughput measured on AMD Zen 5 (Turin, 32 cores pinned to one NUMA node, new hardware page), gpt-oss 20B BF16-w8a8 (existing model page), vllm bench throughput random 128/128, 256 prompts: max-num-seqs 8 154.23 (bf16) vs 158.21 (f32) total tok/s; max-num-seqs 32 369.79 vs 375.74, f32 ahead at both points (upstream re-measured 2026-10-01; the original body had 155.21 and 365.74). The fix is about reaching the fast path. New build A/B group with interpretive note (page now 112 of 112).


## 2026-09-30: vLLM #59367 DCP top-k merge scratch reserve mine (11 rows)

- vLLM #59367 (2026-09-30, PR): serving validation for reserving the sparse-indexer DCP top-k merge scratch through the workspace manager (fixes #59317), paired with the CUDA-graph pool estimate fix. GLM-5.3-NVFP4, 4x H200 NVL (new hardware page), TP4 DCP4 EP, MTP 3, fp8_ds_mla, max-model-len 786432, nightly af7f9488c. Prefill: fresh 8x32768 5092 patched vs 5129 unpatched production image (same night); 2x131072 4941 vs 4988. Decode single samples: N=1 110.7, N=8 329.8, N=32 761.1 patched (unpatched ranged 263-317 / 701-838 across seven boots; no decode change claimed). Second boot with ESTIMATE_CUDAGRAPHS=0 and only the merge-scratch fix (the combination that OOMed before): 8x32768 5103, decode 119.1 / 279.2 / 823.9, 0.8 GiB free per GPU. Sister PR #59368 carries the identical sweep, not re-mined. New build A/B group with interpretive note (page now 111 of 111).
- 05:21 UTC pulse from the 03:37 watermarks: 1 mine above (vLLM #59367; #59368 parked as the identical-sweep sister PR); llama.cpp #29691-#29696 (0 t/s); vLLM #59359-#59381 rest no clean tables (#59362 FA4 num_splits SM90 48% slower decode is a bug report with no bench table); ExLlamaV2 nothing above #821; forum nothing above #3012; HF leftovers still 401.


## 2026-09-30: vLLM #59355 spec-decode OOB fix mine (2 rows)

- vLLM #59355 (2026-09-30, PR): before/after verification of the 12-line OOB guard in the block-verification residual-mass kernel (draft_sampled[logit_idx+1] past-the-end read on the last expanded logit). DeepSeek-V4.1-Flash on 8x H200 (SM90), TP2 x DP4 + EP, vLLM 0.30.0, dspark spec config (5 speculative tokens, block verification, adaptive verification), random 10000-in/5000-out workload at --max-concurrency 128. Before (unpatched): 2/2 runs crashed with cudaErrorIllegalAddress after 131/320 requests, 3972 tok/s partial. After (patched): 1/1 clean, 320/320, 4031.5 tok/s; mean acceptance length 2.399 (n=54) vs 2.145 (n=23). New build A/B group with interpretive note (page now 110 of 110).
- 03:37 UTC pulse from the 02:43 watermarks: 1 mine above (vLLM #59355); llama.cpp #29688-#29690 (ggml-alloc NULL buffer, sleep-idle request bug, json-schema-to-grammar unbounded nesting crash, 0 t/s); vLLM #59350-#59358 rest no t/s (KV connector x2, Hopper NVSwitch NCCL doc, XPU nightly wheel, predicted-length scheduling feature, jit_monitor, shared-memory MM cache auth, MRV2 sampling mask replay); ExLlamaV2 nothing above #821; forum nothing above #3012; HF leftovers still 401.


## 2026-09-29: llama.cpp #29679 MMVQ RDNA3 driver fix mine (8 rows)

- llama.cpp #29679 (2026-09-29, PR): Vulkan MMVQ 4-row policy kept only at 8 columns on RDNA3 with the AMD proprietary driver; 5-7 column batches (spec decoding, multi-slot) were up to 7x slower (q4_K n=7 497 vs 71 us). RX 7900 XTX, Windows 11, driver 26.8.1 (LLPC), ThinkingCap-Qwen3.8-27B Q4_K_S, 64k ctx, KV q4_0, MTP draft, llama-server t/s per client (avg of 4 runs): control slot flat 81.5 vs 78.9 (noise), 2 slots 15.5 -> 45.6, 3 slots 10.6 -> 34.2, 1 slot n_max 5 26.7 -> 92.4. llama-bench ms/batch: Q4_K_S n=6 157.6 -> 31.3, n=7 256.6 -> 36.1; Q4_0 n=7 regresses 42.0 -> 46.4. New model page ThinkingCap-Qwen3.8-27B. New build A/B group with interpretive note (page now 109 of 109).
- 20:50 UTC pulse from the 19:25 watermarks: no rows (llama.cpp #29676-#29678; vLLM #59287-#59301; all bugfix/CI/docs, 0 t/s); ExLlamaV2 nothing above #821; forum nothing above #3012; HF leftovers still 401.


## 2026-09-29: vLLM #59280 FlyDSL MQA-logits kernel mine (36 rows)

- vLLM #59280 (2026-09-29, PR): opt-in FlyDSL prefill MQA-logits kernel for the sparse indexer on gfx950 (MI355X), behind VLLM_ROCM_USE_AITER_FLYDSL_MQA_LOGITS, vs the Gluon baseline on GLM-5.2-MXFP4, TP4. Mined 36 per-GPU throughput rows: ISL 60000 / OSL 600 at conc 4-32 (FlyDSL wins 1.1-1.6 pct, e.g. 5315.0 -> 5399.4 tput/GPU at conc 32; TTFT 2866.7 -> 2708.7 ms at conc 4) and ISL 8192 / OSL 1024 plus ISL 1024 / OSL 1024 at conc 4-256 (within noise; geomean over all 18 points 1560.4 -> 1558.5 tput/GPU, -0.1 pct). Kernel trace: prefill MQA-logits kernel time -35 pct (1.53x), same 16k chunk 153.4 -> 98.7 ms. Accuracy: GPQA Diamond 0.899 vs 0.884 single run, RULER niah 1.00 both arms at 64k/128k. New model page GLM-5.2 (MXFP4). New build A/B group with interpretive note (page now 108 of 108).
- 19:25 UTC pulse from the 18:33 watermarks: the #59280 mine above; llama.cpp #29675 (BF16 unary/GLU/binary/scale ops CPU+CUDA; 0 t/s); vLLM #59271-#59279 + #59281-#59286 (DSv4 VL dummy image, ThinkingBudgetStateHolder bugs, HiSparse GPU prefix copies, UMBP standalone/distributed modes, CuTe MoE SM107 default, Kimi K2.5/K3 mm normalization, Qwen4Exp QSA DCP, UMBP staged loading, HiSparse free queue, MiniMax-M3 tensor descriptors, LoRA adapter name rejection; 0 t/s); ExLlamaV2 nothing above #821; forum nothing above #3012; HF leftovers still 401.


## 2026-09-29: llama.cpp #29654 PCIe choke upper-bound mine (1 row)

- llama.cpp #29654 (2026-09-29, issue): GPUs choking on PCIe (VK device lost) on a two-GPU rig (RTX 3090 on PCIe4 x16 + RX 7900 XT on PCIe4 x1) with Qwen3.8 27B Q8_0: mined 1 row recording the reported "decode speed drops drastically down to less than 1 t/s" as an upper-bound degradation value (not a benchmark), during the episode with 39 GiB/s TX+RX on the x16 lanes and 120K+ context restore after reboot as the most common trigger; model + context fully in VRAM. New hardware page "RTX 3090 + RX 7900 XT" (first two-GPU rig string).
- 13:13 UTC pulse from the 12:21 watermarks: the #29654 mine above; llama.cpp #29655-#29656 (Gemma 4 tool-calling streaming bug, AGENTS.md revamp; 0 t/s); vLLM #59214-#59217 (Qwen4Exp SM100 decode GEMM plans, STT preprocessing docs, ShareGPT language-filter fix, multi-model tokenize RFC; 0 t/s); ExLlamaV2 nothing above #821; forum nothing above #3012; HF leftovers still 401.


## 2026-09-29: llama.cpp #29639 Vulkan sparse FA quantized-KV mine (8 rows)

- llama.cpp #29639 (2026-09-29, PR): Vulkan sparse flash attention enabled for quantized K/V (Qwen3.8-Flash-Next QSA / DeepSeek-style sparse attention previously ran dense over the whole context with a quantized cache). Mined 8 rows from the interleaved decode table (4 KV depths x master+#29591 baseline vs PR build, q8_0 KV): depth 0 51.4 vs 51.6 t/s, 32k 38.9 vs 39.7 t/s (per-session +2.1%/-0.6%), 64k 27.9 vs 32.3 t/s (+15.6%, largest gain), 128k 20.6 vs 21.4 t/s (+4.1%); f16 cache and prompt processing unchanged, 16x minimum context/kept ratio threshold (upstream 2x regressed 4% at 16k). The table is not GPU-tagged; rows attributed to the R9700 rig (sanity-check section names R9700 first, 7900 XT second; threshold sweep stated as RDNA3/RDNA4), noted in the row notes. New build A/B group with interpretive note (page now 107 of 107).
- 10:17 UTC pulse from the 09:23 watermarks: the #29639 mine above; llama.cpp #29638 + #29640 (draft-token EOG stop, AOCL-BLAS docs; 0 t/s); vLLM #59188-#59202 (AMD CI bootstrap, GB200 DP4+EP NCCL reduce-scatter crash, Kimi K3 grammar, symmetric-memory rendezvous guard, mooncake auto-label, BLIP-2 ViT CUDA graph, Pixtral fused normalization, ECMooncakeConnector docs, DSv4.1 SWA replay, docker wheel alignment, WNA16 batch-invariant, workspace init refactor, ROCm CI path, Anthropic merge warning; 0 t/s); ExLlamaV2 nothing above #821; forum nothing above #3012; HF leftovers still 401.


## 2026-09-29: llama.cpp #29635 prefix-LM regression mine (2 rows)

- llama.cpp #29635 (2026-09-29, PR): prefix-LM attention mask for DFM Mimir HRM-Text models. Mined 2 rows from the "other models are unaffected" regression block: Llama-3.2-1B Q8_0 on a GTX 1060, llama-bench means of the last two of three alternating runs, master tg128 90.7 t/s (pp512 2381) versus PR build tg128 90.3 t/s (pp512 2380), a neutral performance check alongside the DAISY accuracy fix (5.9 pct to 8.3 pct exact match vs 8.4 pct official transformers). New hardware page GTX 1060; new build A/B group with interpretive note (page now 106 of 106).
- 08:20 UTC pulse from the 07:17 watermarks: the #29635 mine above; llama.cpp #29634 + #29636 (graph_inputs collection, ggml-zdnn 0-row fix; 0 t/s); vLLM #59158-#59172 (sleep-mode offload batch, XPU DeepSeek V4 sparse decode, LoRA-per-logits bug, MoRIIO KV zeroing, sleep-mode docs, DFlash padding fix, int64 offsets, EPLB load balancer, Engram hooks, frontend error preservation, Engram device restrictions, Anthropic warnings; 0 t/s); ExLlamaV2 nothing above #821; forum nothing above #3006; HF leftovers still 401.


## 2026-09-29: vLLM #59151 CDNA2 mxfp4 TRITON_UNFUSED mine (2 rows)

- vLLM #59151 (2026-09-29, issue): ROCm mxfp4 MoE backend-selection gap on pre-CDNA3 (gfx90a), reported after several days of clean operation. Mined 2 rows from the final environment reference: 4x AMD MI210 (64 GB HBM2e each, TP=4, 262K context config) running XiaomiMiMo/MiMo-V2.6-Flash-RL mxfp4 with explicit --moe-backend triton_unfused and a DFlash drafter: 31 tok/s single-stream decode and 160 tok/s aggregate across 32 concurrent streams, with needle-in-a-haystack retrieval verified at 1,038,700 tokens. New hardware page 4x AMD MI210; new build A/B group with interpretive note (page now 105 of 105).
- 07:17 UTC pulse from the 06:13 watermarks: the #59151 mine above; llama.cpp #29631-#29633 (hexagon FP32 GELU/GEGLU, tool init fixes, CUDA MMVF thin mul_mat; 0 t/s); vLLM #59146-#59150 + #59152-#59157 (Mamba sparse retention, GLM-5.3-Flash KDA dtype, Rust MiMo builder, POWER10 W4A16, sparse-indexer allocs, mimo_audio CUDA import bug, rust bench discrepancy, AITER relu2 tracking, workspace-scratch-on-sleep, cu129 image torch mismatch; 0 t/s); ExLlamaV2 nothing above #821; forum nothing above #3006; HF leftovers still 401.


## 2026-09-29: vLLM #59109 GLOO docker-bridge PP fix (11 rows) + #59112 FlashInfer packed KV (6 rows)

- vLLM #59109 (2026-09-29, issue): in a single-container PP4 docker deployment the cpu:gloo control plane resolved the container hostname to the docker bridge IP, costing ~535 ms per control send and collapsing single-stream decode with context on DeepSeek-V4.1-Flash 764B EXL3 (4x NVIDIA CMP 170HX rig, PP4, DSpark, fp8_ds_mla KV, 1M ctx). Mined 11 rows from the before/after table of the GLOO_SOCKET_IFNAME=lo fix (single-stream decode, warm: 32K 57.0 to 60.7, 128K 46.7 to 58.3, 300K ~40 to 56.7, 524K 35.8 to 54.7 tok/s) plus the post-fix concurrency rows C8 200.6 / C16 199.4 / C24 252.1 decode tok/s. New build A/B group with interpretive note (page now 103 of 103); new hardware page 4× NVIDIA CMP 170HX (the earlier CMP 170HX rows come from #59054's "4x CMP 170HX" rig string).
- vLLM #59112 (2026-09-29, PR): FlashInfer dense-GQA re-paging for packed BLHNC KV caches, B300, Qwen3.6-35B-A3B-FP8 + DFlash MRv2 (7 spec tokens), BF16 KV. Mined 6 rows from the two-run-averaged LBHNC/BLHNC table: c1 output 286.56 to 427.01 tok/s (+49%), c32 output 5115.53 to 7221.04 tok/s (+41.2%, per-run 7258.52/7183.57), 8192-in/1-out req/s 6.419 to 7.015; KV groups drop 46 to 5 with +2.2% reported capacity. New build A/B group with interpretive note (page now 104 of 104).
- 01:30 UTC pulse from the 00:26 watermarks: the two mines above; llama.cpp #29622 (embd + raw tokens batch support, 0 t/s); vLLM #59107, #59108, #59110-#59111, #59113-#59115 (0 t/s: DiffusionGemma canvas, dropped chat turns, NixlConnector KV-page misread + RFC, zmq socket dir, MoRIIO producer-dead hang, GLM-5.3-Flash illegal access); ExLlamaV2 nothing above #821; forum nothing above #3006; HF leftovers still 401.


## 2026-09-29: llama.cpp #29620 cpu-mtp final-commit sweep (6 rows)

- llama.cpp #29620 (2026-09-29, PR, same author's successor to #29619): fresh 4-variant sweep on the exact commits in this PR (12 960-token needle prompt, `--spec-draft-n-max 4`, ctx 16 384, KV q4_0, RTX 5070 Ti Laptop 12 GB, Qwen3-27B REAP192): MTP off 28.9, pure --cpu-mtp 36.7 (78.1% accept), hybrid 55.2 (78.1% accept), full-GPU MTP 58.7 (70.2% accept), plus the repeated 60 k ctx prior-campaign pair hybrid 40.8 vs pure 30.0 tok/s. Mined 6 rows; new build A/B group with interpretive note (page now 102 of 102); the #29619/#29620 pairs surface as contradictions, which is the point: prior sweep vs final-commit sweep on the same rig.
- 00:26 UTC pulse from the 23:20 watermarks: llama.cpp #29620 mined above; vLLM #59104-#59106 (fill-in DSpark KV lookahead reallocation bug + two fix PRs, 0 t/s); ExLlamaV2 nothing above #821; forum nothing above #3006; HF leftovers still 401.


## 2026-09-28: llama.cpp #29619 cpu-mtp MTP drafter (6 rows)

- llama.cpp #29619 (2026-09-28, PR): adds `--cpu-mtp`, keeping the MTP drafter block and its recurrent-state snapshots in host RAM (plus the hybrid recipe that pins the MTP block back to the GPU with `-ot`) so a 12 GB card can fit the target's KV cache. Mined 6 rows from the 4-variant needle sweep (12 960-token prompt, `--spec-draft-n-max 4`, ctx 16 384, KV q4_0, RTX 5070 Ti Laptop 12 GB, Qwen3-27B REAP192): MTP off 28.7, pure --cpu-mtp 31.1 (69.2% accept), hybrid 51.2 (72.4% accept), full-GPU MTP 62.5 (79.6% accept), plus the prior-campaign 60 k ctx pair hybrid 40.8 vs pure 30.0 tok/s. New build A/B group with interpretive note (page now 101 of 101); new RTX 5070 Ti Laptop 12 GB hardware page and Qwen3-27B model page.
- Pulses from the 22:14 watermarks (23:20 UTC): llama.cpp #29617-#29619: #29619 mined above, #29617 speculative default-props plumbing, #29618-#29619 cpu-mtp PR stack, 0 t/s elsewhere; watermark now above #29619. vLLM #59098-#59103: batch-sort-by-context, KV-offload reset flush, ROCm kernel source maps, UMA startup gate bug, NIXL chunked-prefill boundary re-save, stale block-hash drop, 0 t/s; watermark now above #59103. ExLlamaV2 #821 (ngram last-token fix, no bench) nothing new above; forum still nothing above topic #3006; HF leftovers still 401 (no Wayback snapshots).
- Dataset: 3,167 measured records, 345 hardware strings, 151 models, 24 backends; 525 contradiction, 34 outlier flags; 3,743 quote-verified; 505 pages, 17,791 internal links. Hand-mined: 621 rows (509 GitHub issue rows: 334 llama.cpp, 164 vLLM, 11 ExLlamaV2; 34 HF model-card rows; 29 ExLlamaV2 discussion rows; 49 qiulang/vllm-sglang-perf rows).


## 2026-09-28: llama.cpp #29604 SYCL allreduce (10 rows), #29606 Hexagon HTP queue (4 rows), vLLM #59082 AMX MTP scheduling (6 rows)

- llama.cpp #29604 (2026-09-28, PR): replaces the tensor-split allreduce's blocking dev2dev memcpy and queue drains with pinned-host-buffer crosses and async SYCL copies (F16, small F32, BF16-compressed paths; perplexity unchanged). Mined 10 rows, master vs patched llama-bench on 2x Arc Pro B70 with Qwen3.8-27B Q8_0 (f16 KV, -fa on, Windows 11 oneAPI 2026.0): prefill pp2048 665 to 928 tok/s (+40.0%) without VMM and 675 to 918 (+36.0%) with VMM=1 at ub 1024, 477 to 692 (+45.1%) and 478 to 661 (+38.3%) at ub 256; decode tg128 18.2 to 20.2 (+11.0%). New build A/B group with interpretive note (page now 100 of 100); new 2x Arc Pro B70 hardware page.
- llama.cpp #29606 (2026-09-28, PR): Hexagon HTP work-queue fix identifying task publications by n_pub so a stale wakeup cannot re-execute a task (previously the queue aborted with exit 134 / 0x2e under the wakeup-delay hook). Mined 4 rows from the recorded upstream hardware reproduction, OnePlus 13T with the v79 NPU, Qwen3.5-4B Q4_0, llama-bench -dev HTP0 -ngl 99 -t 4 -p 128 -n 32 -r 2: fixed vs vanilla, pp128 665.20 vs 669.88 tok/s (-0.7%) and tg32 14.38 vs 14.47 tok/s (-0.6%), inside the two-repetition noise the author flags. New build A/B group with interpretive note (page now 100 of 100); new OnePlus 13T hardware page.
- vLLM #59082 (2026-09-28, PR): AMX-BF16 CPU attention gets request-level decode_mask eligibility so multi-token MTP verify batches use the grouped GQA schedule with split-KV (auto and FP8 E4M3/E5M2 KV). Mined 6 rows from the main-vs-branch serve table (Qwen3.5-4B BF16, 100k-in / 1k-out, c1, 3 timed requests per arm): MTP3 auto KV 8.01 to 9.48 tok/s (+18.4%), MTP3 FP8 KV 8.62 to 9.36 in the post-fix run (branch TTFT held at 81.20 s vs main 80.73 s), no-MTP control 6.73 to 7.08 (+5.2%). New build A/B group with interpretive note (page now 100 of 100); new AMX hardware page.
- vLLM #59084 parked: GLM5.3 fused_q Q-projection fusion, kernel microbenchmark in microseconds via do_bench_cudagraph (1.27-1.64x), no hardware named and no end-to-end tok/s.
- Pulses from the 18:15 watermarks (19:14 UTC): llama.cpp #29599-#29608: #29604 and #29606 mined above, #29599 llama_prefetch_rows, #29600 Prism Bonsai 2 27B runtime support, #29601 batch llama_batch_ext migration, #29602 metal FWHT perf, #29603 OpenVINO stride views, #29607 GCC 15 CI fix, #29608 SYCL pinned ring buffer, 0 t/s; watermark now above #29608. vLLM #59074-#59084: #59082 mined above, #59084 parked above, #59081 Minimax M3 fp8 indexer cache, #59083 MiMo o_proj FP8, #59080 KV-offload DCP factor, #59075-#59077 MoonEP/CI/sampling PRs, 0 t/s; watermark now above #59084. ExLlamaV2 still nothing above #820; vLLM forum still nothing above topic #3006; HF leftovers still 401 (no Wayback snapshots for either card).
- Dataset: 3,161 measured records, 344 hardware strings, 150 models, 24 backends; 525 contradiction, 34 outlier flags; 3,737 quote-verified; 503 pages, 17,747 internal links. Hand-mined: 615 rows (503 GitHub issue rows: 328 llama.cpp, 164 vLLM, 11 ExLlamaV2; 34 HF model-card rows; 29 ExLlamaV2 discussion rows; 49 qiulang/vllm-sglang-perf rows).


## 2026-09-28: vLLM #59054 Triton spec-verify 2D-forcing bug (5 rows), 4x CMP 170HX page

- vLLM #59054 (2026-09-28, bug report): [Bug] Triton attention forces spec-decode verify batches (q_len>1) onto the 2D varlen kernel via the max_seqlen_q>1 condition, so a single-stream verify at long context launches only 4 CTAs on a 70-SM GPU. Mined 5 rows from the serving section (4x CMP 170HX, sm80, PP=4, MiMo-V2.6-Flash-RL FP8, MTP k=2, steady-state decode, unique-content prompts, thinking off): 67K context stock path 16.5 tok/s vs 3D split-KV verify path 33.7 tok/s (2.0x), no speculation 56.1 tok/s (the bug makes spec decode a net loss at long context); around 5K context (cliff start) spec 42.5 vs ~63 without. New build A/B group with interpretive note (page now 97 of 97); new 4x CMP 170HX hardware page and MiMo-V2.6-Flash-RL model page. Kernel-level ms-per-call table (q_len 1-4 at 67K/19K) parked.
- Pulse from the 15:04 watermarks (16:10 UTC): llama.cpp #29591-#29596 (vulkan prealloc fix, fs::path cache dirs, FirePro D700 Vulkan perf report with no tok/s in body, 0 t/s); vLLM #59054-#59067: #59054 mined above, #59059 KVPP layer-sharded MLA cache, #59062 online-quantization RFC, #59064/#59065 Kimi-K3/FlashInfer bug reports, rest bugfix/CI PRs; watermark now above #59067. ExLlamaV2 still nothing above #820; forum still nothing above #3006; HF leftovers still 401.
- Dataset: 3,141 measured records, 341 hardware strings, 150 models, 24 backends; 525 contradiction, 34 outlier flags; 3,717 quote-verified; 500 pages, 17,637 internal links. Hand-mined: 595 rows (483 GitHub issue rows: 314 llama.cpp, 158 vLLM, 11 ExLlamaV2; 34 HF model-card rows; 29 ExLlamaV2 discussion rows; 49 qiulang/vllm-sglang-perf rows).

## 2026-09-28: vLLM #59040 Quark W8A8 MTP zero-fc bugfix A/B (3 rows), Radeon 8060S

- vLLM #59040 (2026-09-28, PR): [Bugfix][Spec Decode] keeps mtp.fc unquantized for quark (and compressed-tensors), where the MTP block ships as plain BF16 with no exclude entry, so the quark path silently loaded a zero fc, drafted token 0 every step and ran MTP at 0.0% acceptance. Mined 3 rows from the 400-token greedy single-stream table (3 runs each; only --speculative-config differs): Qwen3.5 27B int8 W8A8 via Quark on gfx1151 (Radeon 8060S), vLLM 0.28.0 on ROCm 7.2: no speculation 5.12 tok/s, MTP before the fix 4.67 tok/s (-8.8% vs no speculation, 0.0% acceptance), MTP after 6.27 tok/s (+22.5% vs no speculation, 22-45% acceptance); ngram speculation on the same box at 41% acceptance (59.62 s, no tok/s listed, parked). New build A/B group with interpretive note (page now 96 of 96); rows join the existing Radeon 8060S and Qwen3.5-27B pages.
- Pulse from the 14:12 watermarks (15:04 UTC): llama.cpp #29579-#29588 (UI PR stack, PLaMo EOG vocab fix, SIGTERM shutdown bug, 0 tok/s); vLLM #59040-#59053: #59040 mined above, #59044 SM100 FP4 MoE prefix-sum (microsecond FFN latencies, parked) and #59045 gfx942 V4.1-Flash boot bug, rest CI/derender/MoE PRs; watermark now above #59053. ExLlamaV2 still nothing above #820; vLLM forum still nothing above topic #3006.
- Dataset: 3,136 measured records, 340 hardware strings, 150 models, 24 backends; 525 contradiction, 34 outlier flags; 3,712 quote-verified; 499 pages, 17,607 internal links. Hand-mined: 590 rows (478 GitHub issue rows: 314 llama.cpp, 153 vLLM, 11 ExLlamaV2; 34 HF model-card rows; 29 ExLlamaV2 discussion rows; 49 qiulang/vllm-sglang-perf rows).

## 2026-09-28: llama.cpp #29570 M5 tensor-API flash-attention kernel (10 rows), vLLM #59010 QSA SM90 kernel (2 rows)

- llama.cpp #29570 (2026-09-28, PR): adds a tensor-API FLASH_ATTN_EXT kernel for M5 that runs Q*K^T and P*V with matmul2d over 64-row KV blocks, 32 queries per threadgroup, used for F16 KV above the fill threshold (about 20 queries). Mined 10 rows: Qwen3.8-27B Q8_0, -fa 1, on M5 Pro (20-core GPU), master vs kernel across five llama-bench workloads: pp512 383.3 to 385.8 tok/s (flat), pp512 at 8k context 295.7 to 340.0 (+15.0%), at 32k context 174.3 to 252.9 (+45.1%), pp32 at 8k (below the kernel threshold) 107.2 to 106.2, tg32 9.18 to 9.02. New build A/B group with interpretive note (page now 94 of 94); new M5 Pro (20-core GPU) hardware page.
- vLLM #59010 (2026-09-28, PR): [Perf][Kernel] adds a SM90 CuTe kernel for Qwen4Exp QSA sparse prefill (transposed wgmma m64n16k16 GEMMs with cp.async K/V rows) replacing the (32, 1, 1) Triton path above 2048 programs on Hopper with BF16 KV. Mined 2 rows from the serving table (the kernel-microbenchmark table is latency in ms, parked): 8x H20, TP4, Qwen/Qwen3.8-Flash-Next-FP8, vllm bench serve random 16000 in / 8 out, c16, 128 prompts, two seeds: total token throughput Triton 15,083 vs native 15,416 tok/s (+2.2%), mean TTFT 12.81 to 12.53 s. New build A/B group with interpretive note (page now 95 of 95); new 8x H20 hardware page (ASCII x in this PR, distinct slug from the 8× H20 page of #58872).
- Pulses from the 10:42 watermarks (11:39 UTC): llama.cpp #29566-#29570: #29570 mined above; #29566-#29569 doc/PR items with no tok/s tables; watermark now above #29570. vLLM #59010-#59016: #59010 mined above; #59014 (FlashInfer persistent trtllm-gen counter, prose only) and #59015-#59016 (empty-streaming fix, sm80 MLA soft-dequant RFC) no clean tables; watermark now above #59016. ExLlamaV2 still nothing above #818.
- The vLLM #58986 rows mined at 07:45 (12) were re-mined as 6 from the author's same-day refresh (see the #58986 entry below); final dataset: 3,133 measured records, 340 hardware strings, 150 models, 24 backends; 525 contradiction, 34 outlier flags; 3,709 quote-verified; 499 pages, 17,619 internal links. Hand-mined: 587 rows (475 GitHub issue rows: 314 llama.cpp, 150 vLLM, 11 ExLlamaV2; 34 HF model-card rows; 29 ExLlamaV2 discussion rows; 49 qiulang/vllm-sglang-perf rows).

## 2026-09-28: vLLM #58989 SM120 block-FP8 MoE backend switch (2 rows), RTX PRO 5000 72GB page

- vLLM #58989 (2026-09-28, PR): [Perf] moves TRITON ahead of DEEPGEMM in block-FP8 MoE auto-selection on SM120 (RTX PRO Blackwell / RTX 50), mirroring the existing SM90 rule; EP and SM121 unchanged. Mined 2 rows from the real-weights table: Qwen3-30B-A3B-Instruct-2507-FP8 on RTX PRO 5000 72GB, TP1, vllm bench throughput random 1024/256 with 256 prompts, max model len 4096: DEEPGEMM 19778 vs Triton 19806 tok/s, bs1 latency 0.800 to 0.678 s, bs32 3.739 to 3.250 s, GSM8K 5-shot 88.02% to 88.55%. New build A/B group with interpretive note (page now 93 of 93); new RTX PRO 5000 72GB hardware page and Qwen3-30B-A3B-Instruct-2507-FP8 model page. Parked (dummy weights): TP2 24845 to 25145, Qwen3.6-35B rows, Qwen3-Next-80B TP2 15373 to 18775 (+22%).
- Pulse from the 07:45 watermarks (08:59 UTC): llama.cpp #29561-#29563 no tok/s (metal GGML_OP_PAD padding PR, deterministic-prefill crash report, --meminfo conversion flag PR); watermark now above #29563. vLLM #58988-#59003: #58989 mined above, the rest weight-reload / ROCm / Rust-frontend / doc PRs with no clean tables; watermark now above #59003. ExLlamaV2 still nothing above #818.
- Dataset: 3,127 measured records, 338 hardware strings, 150 models, 24 backends; 525 contradiction, 34 outlier flags; 3,703 quote-verified; 497 pages, 17,551 internal links. Hand-mined: 581 rows (469 GitHub issue rows: 304 llama.cpp, 154 vLLM, 11 ExLlamaV2; 34 HF model-card rows; 29 ExLlamaV2 discussion rows; 49 qiulang/vllm-sglang-perf rows).

## 2026-09-28: vLLM #58986 H20 block-FP8 MoE tile tuning A/B (12 rows), 4x H20 page

- vLLM #58986 (2026-09-28, PR): [Perf] adds shape-specific block-FP8 MoE tile configs for GLM-5.3-Flash on H20, replacing the 64-row default with 16/32-row tiles where measured faster. First mined at 07:45 (12 rows, six workloads x two arms, c16 and c32); the author refreshed the PR body the same day (packaging an SM90 mHC register-lifetime fix and re-labeling the original c32 results as the historical "+27.10% / +9.46% / +8.02%" observations), so the rows were re-mined the same day from the refreshed full-model serving section, whose c1-control to c1-return comparison is designated primary (both arms carry the mHC fix; only the MoE tile config differs). 4x H20 TP4, vLLM 0.30.0+cu129, PyTorch 2.13.0+cu129, driver 535.261.03, 62-shard block-FP8 checkpoint, MTP3, BF16 activations, max length 16384, max sequences 32, batch tokens 4096, 3 repeats of 128 requests, medians of complete paired repeats: 2048/512/c32 962.39 to 1137.92 (+18.24%), 512/1024/c32 1619.19 to 2045.35 (+26.32%), 512/128/c32 820.00 to 903.60 (+10.20%); P99 TTFT and P99 TPOT recorded per workload in the rows. Build A/B group with interpretive note (group carried through the re-mine; page now 95 of 95); new 4x H20 hardware page. The kernel microbenchmark table (batch 1-4096, in microseconds) stays parked.
- Pulse from the 07:30 watermarks (07:45 UTC): llama.cpp #29558-#29560 all PRs with no tok/s tables (add-bos conversion flag, HIP DKQ>256 mfma template fix, llama-model input-layer GPU offload); watermark now above #29560. vLLM #58987 (XPU test skip) and #58986 (mined above) are the only new items; watermark now above #58987. ExLlamaV2 still nothing above #818; vLLM Discussions still 489 (max #17638).
- Dataset after the re-mine (final for the day at this writing): 3,133 measured records, 340 hardware strings, 150 models, 24 backends; 525 contradiction, 34 outlier flags; 3,709 quote-verified; 499 pages, 17,619 internal links. Hand-mined: 587 rows (475 GitHub issue rows: 314 llama.cpp, 150 vLLM, 11 ExLlamaV2; 34 HF model-card rows; 29 ExLlamaV2 discussion rows; 49 qiulang/vllm-sglang-perf rows).

## 2026-09-28: vLLM #58944 ROCm Kimi-K3 latent-MoE kernel A/B (2 rows), overnight pulse

- vLLM #58944 (2026-09-28, PR): [ROCm][Perf][Kimi-K3] accumulates the sharded latent-MoE tail up-projection through aiter's in-place atomic GEMM (accumulate=True) instead of the hipBLASLt addmm_ path; kernel-level 8.57 to 4.35 microseconds per layer on MI355X (M=16, N=896, K=3584). Mined 2 rows: Kimi-K3 TP8 on MI355X (VLLM_ROCM_USE_AITER=1, AITER_SITUV2_A8W4=1), vllm bench serve random 1k in / 1k out c16, aggregate output tok/s: addmm_ baseline 658.42 vs tuned kernel 668.97 (+1.6%), TPOT 23.86 to 23.47 ms, gsm8k 5-shot 0.9636 unchanged. New build A/B group with interpretive note (page now 91 of 91); joins the existing MI355X and Kimi-K3 pages (from #58887).
- Overnight pulse from the 23:33 watermarks (04:00 UTC): llama.cpp #29547-#29552 all skipped (roll byte-strides PR, ngram-simple fix, -sm tensor reboot eval bug, Qwen2-VL RMS_NORM epsilon fix, b11222+ crash without -dev, HIP flash_attn_ext eval bug), no tok/s tables; watermark now above #29552. vLLM #58944-#58965: only #58944 carries a bench table; #58950 (moe_wna16 zero-point shard split) and #58954 (Jetson sm_110 MTP, "about 44 tokens/s" prose) are single-line mentions, not tables; watermark now above #58965. ExLlamaV2 still nothing above #818 (97 discussions); vLLM Discussions still 489 (max #17638).
- HF card scan 11 completed: all 194 cards now verified (the 117 cards that 429'd on the blob pass were covered by a gated raw pass: 115 fetched, 2 left for the next scan, Orashidov1616/qwen35-9b and mrutkows/granite-4.0-h-tiny). No new repos; 13 tps-pattern cards all already stored or parked.
- Post-release pulse (07:30 UTC): no new rows. llama.cpp #29553-#29557 all PRs with no tok/s tables (Minimax M3 MSA sparse-attention kernel, tests ggml init fix, opencl q5_K adreno fix, /v1/embeddings multimodal PR, grammar alternatives limit); watermark now above #29557. vLLM #58966-#58985: 20 items, no bench tables (#58981 is the bench-tooling PR that adds output tok/s to the startup JSON; #58985 [Perf][DCP] DeepSeek-V3.2 top-k skip has no table yet); watermark now above #58985. ExLlamaV2 still nothing above #818; vLLM Discussions still 489 (max #17638).
- Weekly release cut: tag release-2026-09-28 created 07:13:58Z (the GitHub schedule trigger lagged; the cut was dispatched, after adding the missing contents:write permission to the workflow), notes = full changelog, not marked latest.

## 2026-09-27: qiulang/vllm-sglang-perf mined (49 rows, new SGLang backend, A10 pages)

- New source, found via the first vLLM Discussions scan (489 discussions total, newest #17638): benchmark-request thread #17221 (Qwen2.5 7B AWQ on 1, 2, or 4 A10 GPUs) links to qiulang/vllm-sglang-perf, a complete SGLang vs vLLM suite on single/dual/quad A10 24 GB (SGLang 0.4.5, vLLM v0.8.4, 8192 context, 256 output tokens, 20 prompts per run). 49 rows mined from readme.md, 4A10.md, and qwen3-final.md into data/raw/qsl17221.json; the source name carries "via vLLM discussion #17221", so the rows route to vLLM #17221 on the A/B page.
- Qwen2.5-7B-AWQ on 2 A10, c30: SGLang data parallel 853.94/511.92 (unstable across same-day runs; the README's note cites SGLang issue #5808), SGLang tensor parallel 1157.76/1151.33, vLLM TP2 1074.01/1025.81. The project's own 2-GPU comparison table puts SGLang TP ahead (1151-1158 vs 1074 tok/s).
- Next-day retake on the same pair of A10s (4A10.md; the model is named only by its local path /home/vllm/llm/Qwen7B-awq, which the README identifies as the Qwen2.5-7B-AWQ download): SGLang TP2 c5 422.97, c30 1117.99/1115.89, c50 1822.21/1811.35; vLLM TP2 c30 1131.43/1217.92, c50 1534.72/1519.86, c100 1757.90/1816.33. vLLM leads at c30 (best run 1217.92 vs 1117.99); SGLang reclaims the lead at c50 (+19%).
- 4 A10, TP4: SGLang c30 2086.65/2123.63 (4.27-28) plus 2119.20 (4.29), c50 2560.58/2526.98/2540.23; vLLM c30 1318.94/1309.40, c50 1566.10/1534.41, c100 1914.26/1887.62. SGLang TP4 leads vLLM TP4 by about 64% at c50; the project's summary calls vLLM's 2-to-4-GPU gains modest (15-20% in most scenarios).
- Qwen3-4B on a single A10 (qwen3-final.md, all c10): vLLM mt3096 think 377.98/395.12, no-think 278.73/249.99, mt512 no-think 469.62/433.77; SGLang bench mt3096 think 337.17/369.19, no-think 238.21/239.82, mt512 no-think 401.26/413.54; native-API runs vLLM 656.60 (mt512) / 607.98 (mt1024) vs SGLang 424.58 / 423.26.
- Skipped from the same repo: awq-gptq.md (Qwen2.5-72B-AWQ, no end-to-end tok/s lines), the OneA10/TwoA10 sample logs (106.86 and 183.92 tok/s, but no GPU string quotable in the boxes), the 4.27 warm-up boxes (455.09 vLLM TP4, 119.25 SGLang c5, both labeled warm-up), and the Qwen3 c1 API boxes (138.74/117.62/140.01, API runs rather than bench runs).
- New: backend SGLang (24th), quant AWQ, hardware pages A10, 2 A10, 4 A10, model pages Qwen3 4B and Qwen7B-awq (Qwen2.5-7B existed). Six new build A/B groups, all annotated (page now 90 of 90); five new cross-backend comparison groups on the backends page.
- Watermarks: vLLM Discussions now above #17472 (first scan; #17221 mined via the linked repo, #17472 skipped: server log stats, no clean GPU line). The 20:45 UTC pulse found no new rows anywhere (llama.cpp above #29541: 3 PRs, vLLM above #58933: 7 items, none with tok/s; ExLlamaV2 nothing above #818 and still 97 discussions; vLLM Discussions still 489, the four above #17472 re-verified clean; HF card scan 9: 16 hits, all known or parked, 1 new card parked; all five collectors re-fetched, unchanged). Watermarks after the follow-up pulse at 21:35 UTC (also no new rows: llama.cpp #29545, vLLM #58941-#58943, none with tok/s; vLLM Discussions still 489; HF card scan 10 plus a 94-card retry pass, all hits known or parked): llama.cpp above #29545, vLLM issues above #58943, vLLM Discussions above #17472, ExLlamaV2 above #818, ExLlamaV2 discussions through #819. A final 22:12 UTC pulse advanced llama.cpp one more (only new item #29546, an eval bug report with no numbers); watermarks then: llama.cpp above #29546, vLLM issues above #58943, vLLM Discussions above #17472, ExLlamaV2 above #818, ExLlamaV2 discussions through #819.
- Dataset: 3,111 measured records, 336 hardware strings, 149 models, 24 backends; 525 contradiction, 34 outlier flags; 3,687 quote-verified; 494 pages, 17,457 internal links. Hand-mined: 565 rows (453 GitHub issue rows: 304 llama.cpp, 138 vLLM, 11 ExLlamaV2; 34 HF model-card rows; 29 ExLlamaV2 discussion rows; 49 qiulang/vllm-sglang-perf rows).

## 2026-09-27: vLLM #58804 tiered KV offloading regression A/B (2 rows), all watermarks re-scanned

- vLLM #58804 (2026-09-25, updated 2026-09-27) mined, 2 rows. This one slipped through the earlier issue-number scans: it is a [Performance][Bug] report on Guidellm multi-turn synthetic (20K initial prefix, 4K per turn, 5 turns, concurrency 64, 700 s) with gpt-oss-120b TP2 on H100 (4x H100 80GB node), KV tiered offloading (OffloadingConnector, TieringOffloadingSpec, 24 GB CPU tier plus NVMe FS secondary tier, block_size 1024). The reporter's git bisect lands on commit f12fe1 (PR #51787): aggregate Total tokens/s drops from 119092 (parent ab35354) to 102876 (-14%). A CPU-only replay of the access pattern in the thread found no eviction-order regression, so the loss is in the fs transfer or GPU-side timing the replay cannot capture. New build A/B group with interpretive note (page 84 of 84). New model coverage: gpt-oss-120b measured rows join the existing model page.
- vLLM #58921-#58933 (since the last scan): all skipped, no tok/s tables (macOS Apple-Clang build bug and fix, MooncakeStore preemption crash and connector-state fix, xgrammar validation gap, Responses reasoning-token counting, batched chat-completion sampling). Watermark now above #58933.
- llama.cpp above #29536: #29537 (params-parsing side effects), #29539 (LLAMA_MOE_RANDOM_ROUTING benchmark env var, no measured table), #29541 (zdnn CI build) - all skipped. Watermark now above #29541.
- ExLlamaV2 (turboderp-org/exllamav2, archived): nothing above #818.
- HF card scan 8 (194 model queries, fresh card cache, 429 backoff on the blocked tail): no new rows. All 14 hits are known: 9 mined cards, the 2 DavidAU fine-tune cards already mined in the hf1 pass (Qwen3.5-9B Defiant Fable and Qwen3.6-27B Fable Fusion 711, MTP variants), and the 3 parked cards (yuxinlu1 agentic gemma, MaziyarPanahi 405B sample log, ISTA-DASLab Qwen3.8-Flash-Next GSQ-RCO: 177B qwen4exp, llama.cpp 55-prompt bench Q2_0 367.49 pp / 93.79 decode vs IQ2_XS 108.19 / 70.30, still no GPU named on the card).
- Dataset: 3,062 measured records, 333 hardware strings, 147 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,638 quote-verified; 489 pages, 17,211 internal links. Hand-mined: 516 rows (453 GitHub issue rows: 304 llama.cpp, 138 vLLM, 11 ExLlamaV2; 34 HF model-card rows; 29 ExLlamaV2 discussion rows).

## 2026-09-27: Freshness re-scan: 3 new rows (vLLM #58920 KV-connector A/B, HF KAT card), #58887 quote refresh

- vLLM above #58919: #58920 (2026-09-27) mined, 2 rows. 2 nodes x 8x H100 80GB, pipeline parallel 8 x tensor parallel 2, vLLM 0.30.0 Model Runner V2 + async scheduling, GLM-5.2 FP8, 12k prompts / 1024 output: aggregate decode at 8 running requests ~250 to ~133 tok/s with a no-op KV connector (empty metadata, no loads or stores) vs none, decode TPOT 32.1 to 60.0 ms (+87%), while the V1 runner shows no overhead; the report's root cause is all 16 ranks replying to every RPC (output_rank None once a KV aggregator exists) and the reply-ring writer spinning with the GIL held. New hardware page 2 nodes x 8x H100 80GB; new build A/B group with interpretive note (page 83 of 83). #58921 (PR, no bench) and #58922 (CPU tensor crash) skipped. New watermark: vLLM above #58920.
- llama.cpp: nothing new above the #29536 watermark; #29532 (Vulkan matmul crash on RTX 5070 Ti Laptop) rechecked, no throughput table, still not mineable. Watermark unchanged.
- ExLlamaV2: the repo moved from EXLlama/EXLlamaV2 to turboderp-org/exllamav2 (now 404 redirect, marked archived; development continues in ExLlamaV3). Nothing above issue #818; discussion watermark still #819.
- HF card scan (194 cards refreshed): 1 new row. IsValorum/KAT-Coder-V2.5-Dev-APEX-I-MiniPlus-V2.1-GGUF (2026-09-18): single-stream generation approx. 247-251 t/s on RTX 5090 (stored lower bound 247), prefill 2,800-3,900+ (stored 2800), full GPU -ngl 99, verified in Unsloth Studio & llama.cpp, attributed to the zephel01 Occamy V2 reference; joins the existing KAT-Coder-V2.5 and RTX 5090 pages. All other hits already mined or parked.
- vLLM #58887 quote refresh (commit 4e7bf189): the PR author re-edited the env block after mining (Test Plan section, Kimi-K3 as its own heading); the 4 rows' quote fragments were rewritten to the current verbatim text. Lesson: CI's check_quotes always re-fetches, so upstream edits to mined bodies surface there first.
- Dataset: 3,060 measured records, 333 hardware strings, 147 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,636 quote-verified; 489 pages, 17,203 internal links. Hand-mined: 514 rows (451 GitHub issue rows: 304 llama.cpp, 136 vLLM, 11 ExLlamaV2; 34 HF model-card rows; 29 ExLlamaV2 discussion rows).

## 2026-09-27: Prefill-only schema relaxation: 44 new rows from the 5 parked llama.cpp issues

- Schema: tps is no longer a required column; a row needs tps or pp_tps above 0, and prefill-only reports carry pp_tps with tps empty (data/schema.md and scripts/check_data.py updated). This unblocks the five parked pp-only llama.cpp issues in one pass: 44 new rows.
- #27181 (R9700 MMQ quant sweep, 2026-08-16): 3 rows, Qwen3.8-27B on the Radeon AI PRO R9700, identical weights requantized from one UD-Q6_K_XL source (pp512: Q2_K 471.2 / Q4_K 1120.7 / Q8_0 1178.3, FA on, ubatch 1024).
- #28135 (RX 9070 Vulkan f16-scratch hybrid-KV fix, 2026-09-01): 2 rows, the before/after A/B, prefill 65 to 119 tok/s (+83%) at a 21.5 K prompt, decode published unchanged.
- #28761 (TU106 sm_75 FA tile cap, 2026-09-11): 17 rows. 2 x TU106, Qwen3.8-27B IQ3_S, tile32 vs tile64 vs dynamic across KV 8 K to 230 K (prompt_per_second, FA on, KV q4_0, ubatch 2048, MTP), the 230 K concurrent-slot row, and single-TU106 Llama 3.1 8B Q4_0 (2052 vs 2127 at 8 K). New hardware pages TU106 and 2 x TU106.
- #28828 (RX 7800 XT IQ4_XS cliff, 2026-09-13): 20 rows. b10727 and self-built b10909 IQ4_XS across seven prompt lengths (the cliff sits at 32-33 K for b10727 and 31-32 K for b10909), Q3_K_XL flat control rows at 28-34 K (474-482 tok/s), plus the MTP server rows at a 32 100-token prompt (93.7 tok/s prefill, 342.7 s TTFT, vs 461.8 for Q3_K_XL).
- #29536 (R9700 LLVM 23 MMQ VGPR spill, 2026-09-27): 2 rows, prefill 298 to 1250 tok/s on Qwen3.8-27B Q4_K_M under stock LLVM 23, matching AMD-compiler parity. New hardware page R9700 (the issue body says R9700, not the full card name).
- All six new build A/B groups carry interpretive notes; the page is at 82 of 82 comparable groups annotated.
- Dataset: 3,057 measured records, 332 hardware strings, 147 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,633 quote-verified; 488 pages, 17,181 internal links. Hand-mined: 511 rows (449 GitHub issue rows: 304 llama.cpp, 134 vLLM, 11 ExLlamaV2; 33 HF model-card rows; 29 ExLlamaV2 discussion rows).

## 2026-09-27: Freshness re-scan: 2 new HF card rows, watermarks advanced

- GitHub venues: llama.cpp above #29534, #29535 (K2 Horizon model support, no tok/s) and #29536 (PR, stock LLVM 23 RDNA4 MMQ VGPR-spill fix) parked as the fifth prefill-only report: the PR's R9700 A/B on Qwen3.8-27B Q4_K_M is prefill only (about 298 to about 1250 t/s, at the author's AMD-compiler parity), and the schema requires a decode tps. vLLM above #58910, #58911 to #58919: no tok/s tables (#58917 is latency-only ms, deferred). ExLlamaV2: nothing new above #818 (issues); discussions max still #819. New watermarks: llama.cpp above #29536, vLLM above #58919.
- HF card scan, 2 new rows. katya228/Apertus-v1.5-70B-text-GGUF (2026-08-03): the card's "What was actually tested" section, TEST quants, tensor split across 2x RTX 3090 + Tesla V100 (64 GB VRAM total), Q4_K_M: about 17 tok/s generation and about 81 tok/s prompt at 65536 context with q8_0 KV cache. New hardware page 2x RTX 3090 + Tesla V100, new model page Apertus v1.5 70B. ox-ox/MiniMax-M2.5-GGUF (2026-02-13): quants table, Q3_K_L about 110 GB, "Runs natively in RAM with high t/s (28 ON MAC M3 MAX)" on 128 GB Macs; new model page MiniMax M2.5, which now carries the row plus the pre-existing LLMCheck M4 Ultra (192 GB) estimate (33 t/s, MLX). Parked: MaziyarPanahi's Llama 3.1 405B Q2_K sample log (40-thread CPU, decode 247837.14 ms per token, published as 0.00 t/s, no named hardware, no representable decode figure).
- Dataset: 3,013 measured records, 329 hardware strings, 147 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,589 quote-verified; 485 pages, 16,975 internal links. Hand-mined: 467 rows (405 GitHub issue rows: 260 llama.cpp, 124 vLLM, 11 ExLlamaV2, 10 other; 33 HF model-card rows across 10 repos; 29 ExLlamaV2 discussion rows).

## 2026-09-27: ExLlamaV2 discussions scan: 29 new rows (6 benchmark threads, new venue)

- New venue: ExLlamaV2's GitHub discussions had never been mined (issues only). All 97 discussions scanned, 6 benchmark threads mined. #10 (akaikite, v1/v2 Speed Comparison, 2023-09): 18 rows, TheBloke FreeWilly2 GPTQ 4bit 70b on the A6000, the v1 GPTQ runtime vs the v2.0 EXL2 format; the comparable first long run (3156 tokens, ctx 941) is 7.91 vs 9.96 tok/s (+25.9%), and the gap narrows at the deepest context (7.07 vs 7.49 at ctx 3551/3588, +5.9%). #119 (3090 + Xeon CPU, 2023-10): 2 rows, llama2 7b EXL2 4bpw ~80 t/s with the process CPU bottlenecked on a pinned Xeon core, and 70b EXL2 2.5bpw ~20 t/s with the GPU at 98% / 400 W tdp. #247 (batching/caching API, 2023-12): 1 row, a title-level claim, 200+ t/s aggregate with Mistral 5.0bpw.exl2 on an RTX 3090 under concurrent requests through the author's EricLLM API. #471 (EXUI vs LM Studio, 2024-05, closed): 2 rows, Llama 3 8B Instruct Q8.0 at ctx 8192 on the RTX 4070 Ti SUPER, LM Studio ~56 vs EXUI ~64 t/s (>14% for exl2, the author's words) on the same fixed periodic-table prompt. #562 (AMD gfx1030, 2024-07): 2 rows, unquantized Phi-3-mini-4k-instruct on the RX 6800, llama.cpp GGUF ~42 vs ExLlamaV2 18 t/s. #572 (4x A10G, 2024-07): 4 rows, the 70B Llama3 fine-tune (256k window, 100k allocated) as an environment A/B, 0.1.7 vs 0.1.8 venvs (torch 2.3 vs 2.4), flat at ctx 0 (8.98 vs 8.76 request 1) and at ctx 12,500 the 0.1.8 env falls to 3.76 from 7.68 tok/s (-51.0%), degrading another ~0.05 t/s per 100 output tokens; the author's profile blames gemm_half_q_half in the newer torch.
- The two new build A/B groups carry interpretive notes (#10 v1 vs v2, #572 environment A/B), so the page is at 76 of 76 comparable groups annotated, every group covered. New hardware pages: A6000, 3090, RTX 4070 Ti SUPER, RX 6800, 4x A10G. New model pages: FreeWilly2, Phi-3 mini 4k instruct, Llama3 fine-tuned, 70B.
- Scanned and skipped: #87 (70B MMLU/perplexity question, 0 comments), #744 (can llama.cpp GPU benchmarks be translated to exllamav2, 0 comments), #254, #278, #671 (no quotable end-to-end tok/s), #819 (calibration vs abliterated weights, 2026-09-25). New watermark: ExLlamaV2 discussions through #819 (all 97).
- Dataset: 3,011 measured records, 328 hardware strings, 145 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,587 quote-verified; 482 pages, 16,937 internal links. Hand-mined: 465 rows (405 GitHub issue rows: 260 llama.cpp, 124 vLLM, 11 ExLlamaV2, 10 other; 31 HF model-card rows; 29 ExLlamaV2 discussion rows).

## 2026-09-27: Build A/B notes: final 26, all 74 of 74 groups annotated

- The last 26 data-only groups on the build A/B page (/notes/build-ab.html) now carry interpretive notes, completing the first full pass: 74 of 74 comparable groups annotated. The new notes: #27327 (RTX 5080, KAT-Coder-V2.5: three consecutive runs after the Gated DeltaNet fused-op fix, 71.63 / 70.29 / 69.93 tok/s, prefill 779.29 / 1024.01); #27464 (GB10 + RTX PRO 6000: the mamba2 flat-2D fix on the Falcon-H1-7B and granite-4.0-h-tiny groups, e.g. GB10 Falcon BF16 80.0 to 199.0, Q4_K_M 187.7 to 273.1, and PRO 6000 granite BF16 1427.0 to 2287.6); #27572 (Radeon 8060S, Qwen3.8-27B MTP np4 on the racing build: tg 16.3 to 25.3 as the prompt grows 620 to 18256 tokens and plateaus, prefill 291.6 to 552.1); #27980 (4x Tesla P40: four memory placements hold decode within 18.0 to 18.1 tok/s, reference 10B-active MoE at 29.5 on the same rig); #28484 (A2000 over RPC to a second GPU: draft-MTP 21.3 vs 17.5 dense, +21.7%, the commit regressed MTP from 27-32 at bb4caa7, Glimmer control at 17.66); #29418 (2x B580 Vulkan: 23.11 then 20.87 tok/s, the two samples before the neq0==HSK assert); #29473 (Snapdragon 7 Gen 4: CPU 34.4 tok/s, the default HMX path garbled at 29.9, HVX-only workaround 27.0; at 4B, CPU 9.1, OpenCL 7.5, HMX 8.1, workaround 6.2); #29510 (RTX PRO 6000, ctx 400000: flash_attn_ext_rows removes the unified-KV penalty, prefill 2982.14 to 8625.75 on gemma, 1106.13 to 2778.22 on Qwen, decode +5% to +13%); #29523 (2x 3090: MTP catch-up lag fix, prefill 1132.0 to 1848.8, +63%, tg 57.98 to 59.98); vLLM #24728 (A100 VLM sweep: aggregate video throughput scales about 30x from c1 to c50, e.g. 199.48 to 6016.16, and the issue's finding is that video prefill is CPU-bound at ~100% CPU / ~20% GPU); vLLM #29662 (8x B200 MTP at con 256: synchronous scheduling beats async, 2421 vs 1994 FP8 and 2895 vs 2375 FP4); vLLM #36629 (4090D batch16: FP8 + EAGLE3 1131.19 vs W4A16 + EAGLE3 1079.15, W4A16 worse-tail ITL); vLLM #48518 (H100: startup L2 persistence costs 3.7%, 809.40 vs 839.75 tok/s, TPOT 4.83 vs 4.66 ms); vLLM #49370 (B300: breakable cudagraph off 773 to 1216 tok/s, 1.57x); vLLM #58578 (Arc Pro B70: reduced draft vocabulary, 59.5 to 74.6 and 147.4 to 189.8 tok/s at unchanged acceptance); ExLlamaV2 #450 (2080 Ti, EXL2 4 bpw: batched inference 82 to 195 tok/s at batch 8, 2.38x, while the multi-cache inflight path manages 80 to 119, 1.48x).
- Every figure is rendered from the records at build time. No data changes: 2,982 measured records, 325 hardware strings, 139 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,558 quote-verified; 473 pages, 16,731 internal links.

## 2026-09-27: HF model-card re-scan: 1 new row (DavidAU LFM2.5-2.6B Q6 on 5090)

- The DavidAU LFM2.5-2.6B fine-tune card (Qwen3.8-Turbo-Brilliance, NEO-MAX) carries a new author figure in its quant list: Q6, non-imatrix, standard quant, 380 t/s on a 5090 (2 GB). Added as one row (LM Studio, the harness the author's other 5090 entries use). The card's base 220 tok/s M5 Max and 113 tok/s Ryzen AI Max+ 395 CPU numbers were already covered from the Liquid AI card. HF model cards now 31 rows across 9 repos.
- Dataset: 2,982 measured records, 325 hardware strings, 139 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,558 quote-verified; 473 pages, 16,731 internal links.

## 2026-09-27: llama.cpp re-scan above #29530: 10 new rows (PR #29534)

- Mined #29534 (PR, use wave64 for GCN Q8 flash attention, gfx906): 10 rows in two model groups, master vs the wave64 build. Llama 3 8B Q4_K_M (D128 head, KV Q8_0): tg128 50.19 to 54.44 at 4096 ctx (+8.47%) and 39.86 to 45.23 at 8192 ctx (+13.47%), prefill flat (719.86 to 715.36, 615.38 to 614.56). Qwen3.6-27B Q4_1 (D256 head, KV Q8_0): 22.97 to 23.84 at 4096, 19.50 to 21.42 at 16384, 16.11 to ~18.86 at 32768; the gain widens with context (+3.8% to +17.1%). The PR's kernel microbench attributes it to the fused Q8 attention kernel, with gains concentrated below KV 10k (up to +92.37% at KV 4096) and flat beyond. New hardware page gfx906, new model page Meta-Llama-3-8B-Instruct. The build A/B page gained the two matching interpretive notes (46 to 48 of 74 groups annotated).
- Scanned and skipped: llama.cpp #29532 (Vulkan matmul dispatch exceeds maxComputeWorkGroupCount, assert report, no tok/s) and #29533 (its fix PR, no tok/s); vLLM #58901 (MambaManager admission fix), #58902 (Qwen3-Omni M-RoPE misalignment bug, no table), #58903 (NIXL docs), #58904 (GLM-5.2 ROCm shared-expert fusion + MTP bugfix, qualitative test results only), #58905 (logits processor FQCN fix) - none with tok/s; ExLlamaV2 above #818: nothing new. New watermarks: llama.cpp above #29534, vLLM above #58905.
- Dataset: 2,981 measured records, 325 hardware strings, 139 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,557 quote-verified; 473 pages, 16,727 internal links. Hand-mined: 435 rows (405 GitHub issue rows across 46 llama.cpp, 35 vLLM, 4 ExLlamaV2 issues, plus 30 HF model-card rows across 8 repos).

## 2026-09-27: Build A/B notes: 15 more interpretive notes (31 to 46)

- Fifteen more comparable groups on the build A/B page (/notes/build-ab.html) now carry interpretive notes: vLLM #40124 (2x RTX A5000, a patched build with 13 Ampere-specific monkey patches, not stock vLLM: enforce-eager drops 145.3 to 11 tok/s, and TurboQuant k8v4 fits 160k context into 2x24 GB at 48.6 tok/s); vLLM #58638 (B300, Qwen3.6-35B-A3B + DFlash: the one-layer drafter bucket forces 46 KV cache groups and per-step metadata rebuild, the RFC's padding-byte group sizing (gs=3, 17 groups) lifts c=1 from 460 to 733 tok/s at the cost of KV capacity, 7.42M to 5.19M tokens); vLLM #58845 (GLM-5.3, TP4: the qlnorm skip saves 78 kernel calls per forward, c4 412.4 to 398.5, c16 826.2 to 870.4, TTFT -7.7% at c1, gsm8k 0.9212 vs 0.9151); vLLM #58872 (8x H20, DeepSeek-V4.1-Flash: the split projections activate only at 2048+ token batches, so the 1K rows run identical kernels and the 8K rows gain +3% to +4% with about 55 ms TTFT saved per 8K chunk); vLLM #58880 (4x GB300, MiniMax-M3: fusing MiniMax2-style routing into the monolithic TRT-LLM MoE kernel removes a topk_sigmoid launch per MoE layer, c1 +5%, c8 +3%, gsm8k means match); vLLM #58887 (MI355X, Kimi-K3: a deterministic race where a step could run with the next step's work maps, fixed at zero cost by pinned-host planning, c4 identical to the second decimal, c32 1083.0 to 1082.6); vLLM #40551 (RTX PRO 6000, Qwen3 8B EAGLE3: MRV2's draft-prob-aware sampling collapses at temperature 1, 3841.5 to 2021.3 tok/s, while MRV1 degrades gently by 6%); #26750 (Qwen3.5-9B MTP, one note per GPU: the CUDA path is a deterministic 35.8% acceptance with decode 61 vs 90, the W7900 runs at 92.2% acceptance for 218 vs 96, the 7800 XT at 91.4% for 124 vs 70, and the issue reads the CUDA figure as the MTP head forward itself degrading); #27117 (Radeon 8060S: DFlash drafts corrupt per slot under 16 concurrent requests and throughput inverts to 37 tok/s, --spec-draft-n-max 1 accepts 83-92% and recovers 80 tok/s); #27544 (2xR9700, one note per backend: on Vulkan, MTP n-max > 1 with -np > 1 collapses parallel scaling from 1.64x at n-max 1 to 1.07-1.09x at n-max 2-3, while the same matrix on ROCm still scales 2.17x at n-max 3); #28863 (2x RX 7900 XTX: the -ub sweep is flat, layer split is worse on throughput but better per active card, and the working hypothesis is occupancy, 43.0% vs 65.9% solo DRAM); #28454 (4x RTX A6000, DSV4-Flash: q8_0 KV is forced off the sparse-fa mma_f16 dispatch onto the VEC kernel, 33.0 to 11.7 tok/s).
- Every figure is rendered from the records at build time; 46 of the 72 comparable groups are now annotated, the rest remain as data-only tables. No data changes: 2,971 measured records, 324 hardware strings, 138 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,547 quote-verified; 471 pages, 16,667 internal links.

## 2026-09-27: Build A/B notes: 12 more interpretive notes (19 to 31)

- Twelve more comparable groups on the build A/B page (/notes/build-ab.html) now carry interpretive notes where the source or the row notes attribute a cause: #27050 (RTX 5090, closed-loop llama-server: the default path copies the full 16.2 MB logits matrix to host on every decode step at 32 slots; backend sampling removes it, 705.9 to 1045.8 tok/s (+48%) with single slot unchanged, plus the vLLM BF16 reference arm from the same run in its own note); #27420 (Radeon AI PRO R9700: a 2x2 matrix shows only ubatch 256 + f16 KV + MTP collapses at ctx 50000, to 9.5 tg; ub1024 or q8_0 KV is a workaround); #28218 (RTX 5060 Ti: the original 500 ms stepping-cliff report, official b10734 at 1.67 tok/s with an explicit tensor split 1 against 38.8 without, the local MSVC build hitting the same wall on both MTP and DFlash2 at 2.01 while no-spec runs 26.55, draft acceptance still about 81%); #28721 (Arc Pro B70, one note per backend arm: Vulkan decode collapses about 8x from 1k to 64k context while SYCL degrades 2.4x, the f16 KV control collapses identically, and RDNA3 shows no collapse); #28734 (5x RTX3090: master's QSA top-k path was running as a dense scan over all n_kv, 37.2 / 22.5 / 11 tok/s at 42k / 111k / 250k, and the 7-patch lever branch restores +37% / +113% / +280%); #29235 (Arc Pro B70, OpenVINO: device-name string comparison breaks indexed GPU.1, 9.6 vs 41.1 tok/s at depth 4096); #29513 (RTX 2060 6 GB, one note per backend arm: not an A/B, the Gated DeltaNet first-request warm-up, 3.09 to 56.1 tok/s on CUDA and 15.4 to 47.0 on Vulkan); vLLM #55139 (4x A100 PCIe, -pp 2 -tp 2: MRV1 vs MRV2 allreduce at c18, 914.97 vs 501.49 tok/s, attributed to PR #42187's microbatch enable); vLLM #58639 (R9700 as last PP rank on gfx1201: the side-stream default roughly doubles the decode forward, 33 vs 46.6 tok/s after moving the last-rank sends and async output copy to the main stream; GPU_MAX_HW_QUEUES=2 removes the microbench penalty but not the end-to-end gap).
- Every figure is rendered from the records at build time; 31 of the 72 comparable groups are now annotated, the rest remain as data-only tables. No data changes: 2,971 measured records, 324 hardware strings, 138 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,547 quote-verified; 471 pages, 16,667 internal links.

## 2026-09-27: Build A/B notes: 6 new interpretive notes (13 to 19)

- The build A/B page (/notes/build-ab.html) had 13 interpretive notes on the 72 comparable groups; six more groups now carry one where the source or the row notes attribute a cause: #27623 (position sweep on the RTX 4080 SUPER holds 33 to 36 tok/s out to KV position 68642, then collapses to 1.4 at 91077); #27734 (RX 7900 XTX at 131k context: the default KV suballocator fragmentation cliff, 40 to 9 tok/s, fixed by a 4 GiB suballocator); #28219 (RTX 5060 Ti: a local MSVC build collapses both MTP and DFlash2 to 2.01 tok/s, the identical cliff ruling out an MTP-specific cause, against 38.8 for the official build); #28867 (Radeon AI PRO R9700: the #28102 WMMA head-256 dispatch regressed speculative decode about 20 percent, recovered by raising the WMMA batch threshold to 64 at zero prefill cost); #29172 (Ternary-Bonsai-2-27B on the RTX 5060 Ti: decode and prefill collapse at KV depth 154855); #29419 (gemma-4-31B on the Arc B580 LE: explicitly not an A/B, two samples from one SYCL run immediately before a SIGABRT in ggml_sycl_flash_attn_ext). Every figure is still rendered from the records at build time.
- Also scanned and skipped: vLLM #58894 (DFlash2 spec-decode acceptance collapse on a Jetson Orin, t/s figures are server log stats, parked with #58580) and #58895 to #58898 (CI tooling, XPU kernel, a per-step microsecond routing-build analysis, no tok/s tables). ExLlamaV2 #814 (below the watermark, closed, PPL-focused E8 KV-quant proposal, no t/s) evaluated and skipped.
- Site-wide live crawl: all 471 pages return 200.
- No data changes: 2,971 measured records, 324 hardware strings, 138 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,547 quote-verified; 471 pages, 16,667 internal links.

## 2026-09-27: HF model-card re-scan: 2 new rows, plus a label-canonicalization fix

- The HF card re-scan (refreshed with today's new model names) surfaced two repos published since the morning pass, and both are mined: huihui-ai/Huihui-DeepSeek-V4-Flash-abliterated-ds4-GGUF (DeepSeek-V4-Flash Q2, RTX 6000 Pro 96GB, WSL2/CUDA 13.0, the card's published lower bound of 35 tokens/s on its custom llama.cpp fork) and Ryanchen911/Kimi-K3-Uncensored-GGUF (Kimi-K3 IQ1_S-XS on an 8xH100 + 2TB RAM node with MoE offloaded to CPU, the card's published expectation of ~6.8 tok/s at ctx 8192). HF cards mined now: 8 repos, 30 rows.
- Robustness fix in scripts/merge_data.py: the collector re-derives model/hardware labels from source text on every fetch, which resurrects case/space/hyphen variants (llama 7B vs LLaMA 7B, RTX 4070 SUPER vs RTX 4070 Super) that the one-off slug-collision pass had renamed. The 26-entry canonical mapping is now applied at merge time, so the build's slug-collision guard can no longer trip on a re-fetch. This run caught exactly that: 122 discussion rows re-deriving variant labels and 2 colliding slugs.
- Parked-set re-evaluation, all held: llama.cpp #27256, #28828, #27181, #28761, #28135, #29520 (decode figures without a GPU on the decode line); vLLM #58799, #55580, #58233, #58825, #58824, #58776, #58727, #58653, #58565, #58421 (no tables) and #58580 (server log stats, not a bench table); ExLlamaV2 #571, #734, #630, #499, #807-#818 (no quotable figures). Freshness re-fetch of all community sources: no new rows.
- Watermarks: llama.cpp above #29529, vLLM above #58893, ExLlamaV2 above #818. Dataset: 2,971 measured records, 324 hardware strings, 138 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,547 quote-verified; 471 pages, 16,667 internal links. Hand-mined: 425 rows (395 GitHub issue rows across 45 llama.cpp, 35 vLLM, 4 ExLlamaV2 issues, plus 30 HF model-card rows across 8 repos).

## 2026-09-27: llama.cpp re-scan above #29523: 2 new rows

- Mined #29526 and #29527: a companion pair from the same host, Arc A770 16GB running Qwen3.5-9B (UD-Q4_K_XL) under llama-server with a 131072 context. Both are long-run stability bugs, and the rows are the normal-operation decode rates from their timelines: Vulkan (build 11160) `tg ≈ 26 t/s` in the 0-7h window before empty EOS replies start; SYCL/Level Zero (build 11100) `tg ≈ 21.19 t/s` in the 0-18h window before a hard decode fence deadlock. Skipped: #29528 (convert PR, no numbers). vLLM above #58892: #58893 (AITER v0.1.23 gfx950 MoE crash) has no throughput table, skipped. ExLlamaV2 above #818: nothing new. New watermarks: llama.cpp above #29528, vLLM above #58893.
- Dataset: 2,969 measured records, 322 hardware strings, 138 models, 23 backends; 521 contradiction, 34 outlier flags (unchanged); 3,545 quote-verified; 469 pages, 16,639 internal links.

## 2026-09-27: Build A/B notes page: regressions and improvements between backend builds

- **New analysis page: /notes/build-ab.html.** Fills the mandate item the cross-backend page pointed to ("the seeds of the regression/improvement tracking the project will run between backend builds"). It groups every record tagged with a `config=` token in its notes that shares model, chip, and backend with at least one such row: same engine, different build or configuration. 72 comparable groups, 308 records, spanning llama.cpp build-to-build comparisons, vLLM release regressions, toolchain and kernel A/Bs. Every table cell is rendered from the record at build time, so the page cannot drift from the CSV.
- **13 interpretive notes** where the source or this project attributes a cause, each with the deltas computed from the records: vLLM 0.26.0 to 0.29.0 decode regression on H100 NVL (#57680, -72% at c12); Triton 3.6 MoE kernel regression and full recovery via the legacy kernels on vLLM 0.17.1 (#37441); MTP turning from a +22% gain into a net loss after the MoE weighted-reduction fusion, bisected to b10751 (#29168); Vulkan flash-attention auto-selecting the slow path between tags 9006 and 10433 (#27137); a bisected --fit-target regression on the 5070 Ti (#27171); the mamba2 flat-buffer patch gains up to +151% (#27464); the MSVC + CUDA 12.8 MTP prefill slowdown (#28790); the 0.6.17 to 0.6.18 attention-backend flip on 8x H100 (#56564); and the RDNA3 146-commit decode/MTP regression (#29410), plus the PR #25337 reproduction on A100 PCIe (#27021).
- Linked from the index, the cross-backend page (whose intro now points here), and the cross-source page. Dataset unchanged: 2,967 measured records, 322 hardware strings, 138 models, 23 backends; 521 contradiction, 34 outlier flags. 469 pages, 16,631 internal links; 3,543 records quote-verified.

## 2026-09-27: vLLM re-scan above #58891 plus parked issue #56564 re-mined: 6 new rows

- **GLM-5.3-Flash attention backend A/B on 8x H100 TP8 (vLLM #56564, 6 rows).** The parked issue is quotable on re-scan: full bench table of `FLASH_ATTN_MLA_SPARSE` (forced with --attention-backend) versus the auto-selected `FLASHINFER_MLA_SPARSE_SM90` default on a single-node 8x H100 80GB HBM3 (TP8), vLLM nightly 385dce36b with FlashInfer 0.6.18, vllm bench serve, MTP 5-token speculation with draft acceptance identical across the two backends, so the gap is the per-step attention kernel. Sonnet 300 in / 256 out, 20 prompts: 368.8 to 237.0 tok/s at c1 and 754.1 to 229.8 at c8 (the issue reports it 36% slower at c1 and 70% at c8); random-dataset worst case c1: 249.3 to 162.9; same ratio with --enable-expert-parallel and the Hopper recipe override. The follow-up fix PR #58892 (drop the head_size==512 priority special case) builds on this data and adds no new table.
- Also scanned and skipped: vLLM #58892 (fix PR for #56564, no own benchmark table); no new llama.cpp or ExLlamaV2 issues above #29523 / #818.
- New hardware page: 8x NVIDIA H100 80GB HBM3 (TP8 node). This closes the cycle above vLLM #58891.
- Dataset: 2,967 measured records, 322 hardware strings, 138 models, 23 backends. Provenance: 746 sourced, 2,221 community. 421 hand-mined rows (393 GitHub issue rows across 43 llama.cpp, 35 vLLM, and 4 ExLlamaV2 issues, plus 28 HF model-card rows across 6 repos). Flags unchanged: 521 contradiction, 34 outlier. 3,543 records quote-verified; 468 pages, 16,619 internal links.

## 2026-09-27: QA: slug collision fix, 451 previously hidden page rows restored

- **The per-chip and per-model pages render one label per URL slug; 24 label groups (5 chip, 19 model) shared a slug** (case/hyphen/space variants of the same chip or model, e.g. `llama 7B` vs `LLaMA 7B`, `RTX 4070 Super` vs `RTX 4070 SUPER`), so the build silently overwrote the colliding pages and 84 chip-side plus 367 model-side rows were invisible on the site. Found by a live crawl that sums per-page row counts against the CSV. Fix: renamed the 26 losing labels to the dominant one (443 rows across 7 source files; every rename is norm-equivalent, so quote verification and the cross-source joins are unchanged by construction) and added a build guard that fails the site build on any future slug collision. Merged pages now show every row: `/models/llama-7b/` went from 87 to 1389 rows, `/hardware/rtx-4070-super/` from 5 to 7. Chip index 326 to 321, model index 159 to 138 labels. No record counts or flags changed: 2,961 records, 521 contradiction, 34 outlier; 3,537 records quote-verified; internal links 15,701 to 16,585 (the restored rows carry their source links).

## 2026-09-27: re-scans above the watermarks: 6 new rows from 2 issues

- **MTP catch-up lag restores multi-GPU prefill on 2x RTX 3090 (llama.cpp PR #29523, 2 rows).** The MTP catch-up decode reads the target's hidden rows through an embedding read that forces the target's ubatch to complete first, so on a --split-mode layer setup the next device cannot start the following ubatch and the pipeline overlap is lost. Laging the catch-up one logical batch behind (plus excluding the MTP context from pipeline parallelism and reserving a K/V-only graph for it) recovers it, build b29c606 (v0.4.1) as released vs the branch: prompt processing 1132.0 to 1848.8 t/s (warm rounds; 1111.5 to 1779.1 including the cold round) on an identical 10464-token prompt with cache_prompt false, generation 57.98 to 59.98 t/s (mean of 3 rounds, draft acceptance 71.4% in both arms). Qwen3.8-27B hybrid, --ctx-size 262144, quant not named in the PR (the #27428 report used Q6_K_XL / Q3_K_XL). The released build also OOMs the MTP draft context buffer on device 1 and silently drops pipeline parallelism.
- **Kimi-K3 AITER MLA FP8 prefill race, before/after on MI355X (vLLM PR #58887, 4 rows).** The ROCm AITER MLA FP8 prefill path rewrites its scheduling metadata off-stream, so with async scheduling a step can run the next step's work maps. Reported as a deterministic GPU memory fault on 8x MI355X (issue #58886); the fix plans the metadata into pinned host slots and copies it on the stream. The PR's performance table (Kimi-K3, TP8, ROCm 10 nightly, FP8 KV cache, dummy weights, sglang bench_serving random 8k/1k, aggregate output tok/s) shows no throughput cost to the fix: 236.05 / 236.05 at c4 and 1083.0 / 1082.6 at c32, before vs after (median ITL unchanged). First rows for the Kimi-K3 model page and the MI355X hardware page (the 8x count is from the #58886 env table, noted on each row).
- Also scanned and skipped: vLLM #58881-#58891 besides #58887 (bugfixes and features, no throughput tables), llama.cpp #29514-#29522 (PRs and bug reports; #29520's qwen4exp Vulkan kernel fusion has decode numbers (49.84 to 51.72 t/s, +3.8%) but names no GPU in the decode line, so it is parked; #29522 is a small graph-reuse fix with no numbers).
- New model page: Kimi-K3. New hardware pages: MI355X, 2x RTX 3090. This closes the cycle above vLLM #58890 and llama.cpp #29523.
- Dataset: 2,961 measured records, 326 hardware strings, 159 models, 23 backends. Provenance: 746 sourced, 2,215 community. 415 hand-mined rows (387 GitHub issue rows across 43 llama.cpp, 34 vLLM, and 4 ExLlamaV2 issues, plus 28 HF model-card rows across 6 repos). Flags unchanged: 521 contradiction, 34 outlier. 3,537 records quote-verified.

## 2026-09-27: llama.cpp and vLLM re-scans: 22 new rows across 4 issues

- **First-request warm-up cliff on RTX 2060 6 GB (llama.cpp #29513, 4 rows).** Qwen3.5-4B Q4_K_M (unsloth GGUF, hybrid Gated DeltaNet) on a 6 GB sm_75 card, Windows x64 b11206, -ngl 99 -c 16384 -ctk q8_0 -ctv q8_0, filed by an AI agent on behalf of its user: the first chat completion after load crawls at 3.09 t/s (prompt eval 0.44) on the CUDA build and 15.4 t/s on the Vulkan build, while requests from the third on run at 56.1 and 47.0 t/s respectively (prompt eval 117-131 and 84-90). A warm-start cliff the dataset now has a first record of, and the first row for the RTX 2060 6 GB page.
- **MiniMax-M3-MXFP8 fused routing on 4x GB300 (vLLM PR #58880, 4 rows).** The routed_scaling_factor=2.0 restriction keeps MiniMax-M3 on the modular TRT-LLM path; this PR moves it to the monolithic MXFP8 kernel. E2E, TP4, 1024 in / 256 out: output throughput 233.0 to 243.5 t/s at c=1 and 942.9 to 966.2 aggregate at c=8 (+4.5% / +2.5%), GSM8K means match (0.855 vs 0.857). Kernel level: about 1.3-2 us saved per MoE layer, about 9% of MoE time at batch 1.
- **DSV4.1-Flash attention-projection split on 8x H20 (vLLM PR #58872, 8 rows).** Per-token projection split with all-gather for batches of 2048+ tokens, TP8, DSpark synthetic acceptance (3.51). Below the threshold (1K/1K at C1) both arms run identical kernels and the PR scores 338.0 vs 335.2 (+0.2%, inside the 1.2% server spread the PR flags); at 8K prefill the split pays: 601.1 to 621.4 (+3.2%) at C16 and 709.9 to 739.0 (+4.2%) at C64, 1K/1K C64 1983.8 to 2014.9 (+1.4%). TTFT at 8K/32K/128K prompt drops 4.2% / 5.0% / 4.2%. Numbers re-verified against the upstream body edit of 2026-10-01 (the original table had 334.4 vs 337.2 at C1, 603.1/622.9, 709.4/738.2, 1989.0/2015.0).
- **GLM-5.3 qlnorm skip on TP4 (vLLM PR #58845, 6 rows).** Skipping the MHA qlnorm saves one kernel per attention (78 per forward); no GPU named in the source, recorded under the TP4 hardware string. MTP speculation (5 draft tokens), guidellm 8000 prompt / 1000 output: 175.4 / 412.4 / 826.2 vs 176.8 / 398.5 / 870.4 t/s aggregate at C1/C4/C16 with TTFT down 7.7% / 7.0% / 4.4% and GSM8K 0.9212 vs 0.9151.
- Also scanned and skipped: llama.cpp #29511-#29516 (the five besides #29513 are PRs, none with tok/s), ExLlamaV2 #818 (docs PR, no numbers). The HF model-card re-scan returns the same 8 repos as the first pass; no new cards.
- New hardware pages: RTX 2060 6 GB, 4x GB300, 8x H20, TP4. New model pages: MiniMax-M3, GLM-5.3. This closes the cycle above llama.cpp #29510, vLLM #58825, and ExLlamaV2 #817.
- Dataset: 2,955 measured records, 324 hardware strings, 158 models, 23 backends. Provenance: 746 sourced, 2,209 community. 409 hand-mined rows (381 GitHub issue rows across 42 llama.cpp, 33 vLLM, and 4 ExLlamaV2 issues, plus 28 HF model-card rows across 6 repos). Flags unchanged: 521 contradiction, 34 outlier. 3,531 records quote-verified.

## 2026-09-27: Hugging Face model-card mining (first pass): 28 new rows across 6 repos

- **Ternary-Bonsai-2-27B llama-bench GPU table (prism-ml, 20 rows).** The custom ternary 27B (7.2 GB) benchmarked with llama-bench TG128/PP512 at batch 1, custom low-bit kernels, no vision tower, across 8 platforms and both ternary packs: RTX 5090 129.9 / 3893 (PQ2_0, 1.95 J/tok) versus 120.5 / 1805 (PTQ1_0), RTX Pro 6000 Blackwell 124.8 / 4020, H100 113.9 / 2830, RTX 6000 Ada 82.8 / 2431, RTX 4090 81.2 / 3124, L40S 74.4 / 2868, A100 73.9 / 1328, L4 29.8 / 777. The PQ2_0 M5 Pro row (28.1 / 387) carries the card's powermetrics draw: 34.1 W across CPU+GPU (27.5 W on the GPU rail). The pre-rotation build re-measurement table adds M5 Max 47.0 / 765, M5 Pro 28.7 / 393, M4 Pro 18.0 / 125.
- **LFM2.5-2.6B CPU inference (Liquid AI, 2 rows).** Vendor benchmark from the official card: 220 tok/s decode on an M5 Max and 113 on a Ryzen AI Max+ 395, under 2.5 GB footprint. The M5 Max figure independently matches the llmcheck MLX Q4_K_M row.
- **Qwen3.5-9B and Qwen3.6-27B MTP quants on a 5090 (DavidAU, 4 rows).** The fine-tune authors' own rough LM Studio / Windows 11 numbers: Q4_K_S about 130 t/s versus over 185 t/s with the MTP quant (Qwen3.5-9B) and about 75 versus over 90 t/s (Qwen3.6-27B); MTP acceptance about 60%, 2 tokens. New hardware page: 5090 (the cards name the card only).
- **DeepSeek-V4-Flash ds4 imatrix on M3 Max (ox-ox, 1 row).** The 0731 model re-quantized 2+4-bit mixed precision with imatrix, single-run Metal CLI at ctx 32768: 45.08 prefill / 27.01 generation against the upstream 58.52 / 26.68 reference on the same machine class.
- **gemma-4-12B Q4_K_M speed table (superkuh, 1 row).** RTX 3060 12GB, 64 GB RAM: 33.34 generation / 609.26 prompt processing tok/s.
- Skipped: ISTA-DASLab Qwen3.8-Flash-Next-GSQ-RCO (clean Q2_0 367.49 / 93.79 and IQ2_XS 108.19 / 70.30 over 55 prompts, but the card names no hardware), yuxinlu1 gemma-4-12B-agentic (about 88 to about 180 tok/s with the MTP draft, no named hardware), Liquid AI's GPU inference line ("almost 15K tok/s on a single H100" has no clean figure), DavidAU's LFM2.5-2.6B mirror (cited the Liquid AI original instead).
- New hardware pages: 5090, Ryzen AI Max+ 395, L40S, L4. New backend: CPU. This opens the Hugging Face model-card venue: 28 hand-mined card rows join the 359 GitHub issue rows.
- Dataset: 2,933 measured records, 320 hardware strings, 156 models, 23 backends. Provenance: 746 sourced, 2,187 community. 387 hand-mined rows (359 GitHub issue rows across 41 llama.cpp, 30 vLLM, 4 ExLlamaV2 issues, plus 28 HF model-card rows across 6 repos). Flags unchanged: 521 contradiction, 34 outlier.

## 2026-09-27: venue re-checks and llama.cpp fifth pass: 11 new rows across 4 issues

- **flash_attn_ext_rows unified-KV A/B on RTX PRO 6000 (llama.cpp PR #29510, 4 rows).** llama-batched-bench, -kvu unified KV cache, ctx 400000, -npp 99936 -ntg 64 -npl 4 -fa on, batch 4. gemma-4-26B-A4B-it Q8_0: master 2982.14 prefill / 273.42 decode versus 8625.75 / 288.11 on the PR branch (2.9x prefill recovery, decode +5%); Qwen3.8-27B Q8_0: master 1106.13 / 90.29 versus 2778.22 / 102.08 (2.5x). Skipped from the same window: #29509, #29508, #29507, #29506 (no tok/s triple).
- **B300 KV-cache grouping RFC (vLLM #58638, 2 rows).** Qwen3.6-35B-A3B + DFlash at c=1: 460 t/s with 46 KV cache groups, 733 after the group-size fix drops them to 17 (the RFC's own section 4.1 measurement).
- **Reduced draft vocabulary decode on Arc Pro B70 XPU (vLLM #58578, 4 rows).** vLLM 0.26.1.dev0 docker, eager, fp8 KV, one stream on an idle server: Qwen3.8-27B (AutoRound int4, 3 drafts) 59.5 to 74.6 t/s and Qwen3.6-35B-A3B (sym_int4) 147.4 to 189.8 t/s with the 50,521-id draft list at unchanged acceptance (per step 19.3 to 15.2 ms).
- **RTX PRO 4000 Blackwell SFF control run (ExLlamaV2 #813, 1 row).** The system-freeze report for RTX 5060 Ti Thunderbolt 5 eGPUs: the PCIe-direct SFF card runs stable at ~47 t/s, LoneStriker Qwen2.5-7B-Instruct 6.0bpw h6 EXL2 quant, TabbyAPI.
- Dataset: 2,905 measured records, 316 hardware strings, 156 models, 22 backends. Provenance: 746 sourced, 2,159 community. 359 hand-mined issue rows across 41 llama.cpp, 30 vLLM, and 4 ExLlamaV2 issues. Flags unchanged: 521 contradiction, 34 outlier.

## 2026-09-27: llama.cpp issue mining, fourth pass: 12 new rows across 4 issues

- **Snapdragon 7 Gen 4 Hexagon backend (llama.cpp #29473, 7 rows).** Motorola Edge 70 (XT2601-2, SM7750, Hexagon v73, 12 GB LPDDR5X), build 86a24a1, pp512/tg64, -t 4. Llama-3.2-1B Q4_0: CPU 216.3 prefill / 34.4 decode, HTP0 HMX default 1749.4 / 29.9 (garbled output), the HVX-only + OPFILTER workaround 78.7 / 27.0 (correct, slower than CPU). Qwen3.5-4B Q4_0: CPU 46.3 / 9.1, Adreno 722 OpenCL 77.5 / 7.5, HTP0 HMX 437.4 / 8.1 (garbled), workaround 25.6 / 6.2. First rows on the Hexagon backend (4 rows).
- **2x Intel Arc B580 Limited Edition MTP draft, SYCL versus Vulkan (llama.cpp #29419 + #29418, 4 rows).** gemma-4-31B-it UD-Q4_K_XL + MTP draft n-max 4, KV bf16, ctx 65536, sm tensor, both cards (Gen4x8 + Gen4x4). SYCL build cd74ef6: 28.44 t/s at n_gen 103, 23.79 at 159 before the flash-attention abort. Vulkan build b1175 on the same machine: 23.11 at 103, 20.87 at 156 before the neq0==HSK assert. New hardware page for the B580 Limited Edition.
- **2x P100 Pascal tensor split (llama.cpp #29466, 1 row).** Qwen3.8-27B UD-Q5_K_XL, patched v0.4.0 tree (29 Pascal sm_60 kernel + AllReduce patches), sm tensor, KV q8_0, ctx 8192: request 1 runs clean at 18.5 t/s (291 graph reuses), the second request crashes in the meta backend.

New hardware pages: Snapdragon 7 Gen 4 (SM7750), Intel Arc B580 Limited Edition. New model page: Llama-3.2-1B. New backend: llama.cpp (Hexagon), the first Hexagon rows in the dataset. Dataset: 2,894 records, 316 hardware, 156 models, 22 backends. 348 hand-mined issue rows across 40 llama.cpp, 28 vLLM, and 3 ExLlamaV2 issues.

## 2026-09-27: llama.cpp issue mining, third pass: 64 new rows across 11 issues

- **RX 7900 XTX pair versus solo (llama.cpp #28863, 16 rows).** gfx1100, ROCm 10.0, build f9f09f02c (10794), llama-bench -p 2048 -n 512 -r 5: Qwen3.8-27B Q4_K_XL solo card 0 versus card 1 is 1074.51 versus 1008.57 prefill and 36.05 versus 35.54 decode; the 2-card tensor split is 1547.96 prefill / 47.06 decode (1.44x, no 2x). Q8_0 29.034 GB is 2-card only (36.26), Qwen2.5-7B Q8_0 hits 122.63 decode on the tensor split. The ub 512 to 4096 sweep is flat for decode and 1.466 to 1.582 of solo prefill; -sm layer loses to tensor (34.03 versus 47.06). Vulkan is +8.5% solo (39.07 versus 36.02 at tg128) but its 2-card tensor path serialises to 23.36.
- **Deep-context decode decay on 5x RTX3090 (llama.cpp #28734, 8 rows).** Qwen3.8-Flash-Next UD-Q4_K_XL, single stream: master decays 37.2 at 42k ctx, 22.5 at 111k, 11 at 250k; the 7-patch lever branch restores 50.8, 48.0, 41.8 (prefill side effect 609 to 716 t/s at 111k). Shallow context essentially unchanged, 54.4 to 56.5.
- **Draft-MTP RPC regression (llama.cpp #28484, 3 rows).** Qwen3.8-27B UD-IQ4_XS, Linux RTX A2000 12GB plus Windows RTX 3080 10GB over 2.5GbE RPC: draft-mtp depth 2 drops to 21.3 t/s at commit 6a1a922 from 27-32; raw dense decode unchanged at 17.5 and the Muse Glimmer 31B dense control sits at 17.66 on both commits.
- **MSVC + CUDA 12.8 MTP prefill collapse (llama.cpp #28790, 4 rows).** Qwen3.8-27B-NVFP4-MTP-LOW on an RTX 5090 Laptop, 4800-token prompt: the self-compiled MSVC 19.44 + CUDA 12.8 build with MTP prefills at 32.7 t/s (near decode speed, 57x slower), the same build without MTP 1867.5, decode 77.1; official b10917 and b10889 prebuilts are fine (1344.9/1482 prefill, 50.3/51.7 decode).
- **Batched decode cliff on Apple M3 Ultra (llama.cpp #29335, 16 rows).** qwen4exp Qwen3.8-Flash-Next Q8_0 and GLM-5.3-Flash UD-Q4_K_XL, b10830 Unsloth prebuilt, --kv-unified, 128 generated tokens per stream: aggregate decode tok/s climbs 32.8 (N=1) to 78 (N=8) at 256 ctx but collapses with context, 8.6 at N=2 and 32k, 5.2 at N=8 and 16k (ms per decode pass 39 to ~1500). GLM-5.3-Flash shows the same cliff at N=4, 40 at 256 to 10.6 at 8k.
- **M1 Max 64K retest (llama.cpp #28805, 1 row).** Qwen3.8-Flash-Next in an unsloth-style 3.84 bpw IQ4_XS 28-shard quant, 2x Apple M1 Max: 64K prefill 153.8 t/s, decode 11.1 t/s on master; 128K still fails.
- **Radeon 8060S MTP sizing (llama.cpp #28433, 3 rows).** Qwen3.8-27B Q4_K_M on Vulkan (RADV STRIX_HALO, gfx1151), --parallel 3: ngram-mod alone 12.8 t/s at 786432 ctx, draft-mtp 24 at 393216 (bug does not trigger), 23.7 with kv-unified at 524288.
- **4x RTX A6000 KV quant cliff (llama.cpp #28454, 2 rows).** DeepSeek-V4-Flash Q8_K_XL, 1M ctx, -fa on: f16 KV about 33 t/s versus about 11.7 with -ctk q8_0 -ctv q8_0, roughly 2.8x, because quantized KV never reaches the fused sparse-FA kernel on SM86.
- **Co-tenant stall retest (llama.cpp #29175, 4 rows).** Qwen3.8-27B Q5_K with q4_0 KV: the Vulkan host's solo decode is unchanged, 24.24 to 24.86 across -b 4096 to 16384 (only the stall count moves), and the Quadro RTX 8000 (SM 7.5) does not reproduce the deep-KV collapse, 20.25 to 19.32 (0.95x) after one 159,437-token request.
- **MiMo-V2.6-Flash-RL on 8x RTX 3080 20GB (llama.cpp #29345, 1 row).** MXFP4, 40/48 expert layers offloaded across the 8 cards, 262144 ctx: control decode without MTP flags about 18.6 t/s.
- **500 ms stepping cliff, companion report (llama.cpp #28219, 6 rows).** RTX 5060 Ti, Qwen3.8-27B UD-IQ3_S: independent confirmation of #28218's matrix, 38.8 t/s baseline with MTP, 1.67 to 2.01 with -ts 1 or on the local MSVC build (MTP and draft-dflash alike), 26.55 with no speculation, 19 to 28 at 128K ctx without speculation.
- Also inspected and skipped: #29386, #29028, #28942, #28760, #28537, #28211 (no quotable tok/s or unnamed hardware), #28220 (follow-up to an already-mined issue). Parked as PP-only: #28761 (TU106 flash-attention tile, prefill only) and #28135 (RX 9070 Vulkan prefill 65 to 119 t/s, decode unchanged).
- New hardware pages: RX 7900 XTX, 2x RX 7900 XTX, 5x RTX3090, RTX A2000 12GB, RTX 5090 Laptop, Apple M3 Ultra, 2x Apple M1 Max, 4x RTX A6000, 8x NVIDIA RTX 3080 20GB, Quadro RTX 8000, AMD GPU via the Vulkan backend. New model pages: GLM-5.3-Flash, MiMo-V2.6-Flash-RL, Muse Glimmer, Qwen2.5-7B, Qwen3.8-27B-NVFP4-MTP-LOW. First rows recorded under the Metal and Vulkan backends.
- Dataset: 2,882 measured records, 314 hardware strings, 155 models, 21 backends, plus 549 reference estimates and 11 cluster runs. Provenance: 746 sourced, 2,136 community. Flags unchanged: 521 contradiction, 34 outlier.

## 2026-09-27: vLLM re-scan: 24 new rows across 4 issues

- **H100 NVL version regression, Qwen3.6-35B-A3B-FP8 (vLLM #57680, 6 rows).** Three frozen images A 0.24.0, B 0.26.0, C 0.29.0 (same weights, SEV-SNP CC VM), 512-token output, ~122-token prompt, median of 5: c=1 138.8/148.3/41.4 and c=12 1183.3/1295.0/362.3 t/s, ITL 6.68 to 23.88 ms. The 0.29.0 image runs 3.3-3.6x slower than A and B on the same hybrid Gated DeltaNet model; the user runs a patched fork pinned to 0.26.0 behavior.
- **TurboQuant on 2x RTX A5000 (vLLM #40124, 3 rows).** Qwen3-35B-A3B-FP8, TP=2, TurboQuant k8v4 KV after 13 patches (vLLM 0.19.1rc1 nightly): 145.3 t/s single-request decode, 48.6 at 160k context, 11 with enforce-eager (CUDAGraphs mandatory).
- **DSV4.1-Flash on 8x RTX PRO 6000 Max-Q (vLLM #56892, 2 rows).** FP8 checkpoint, TP=8, enforce-eager (CUDA graphs unusable on SM120 for V4.1-Flash): engine-side 2.3-4.0 t/s total across 3 concurrent requests (about 1 t/s each, 300 completion tokens); the same 8-GPU box does about 2452 aggregate t/s on the V4-Flash checkpoint per published recipes.
- **V2 side-stream dispatch cost on R9700 (vLLM #58639, 13 rows).** PP=3 pipeline V620/V620/R9700, MTP2, FULL HIP graphs: R9700-side pipeline throughput ~33 t/s with side streams vs 45.3-46.6 on the main stream; separate serving measurement 31.0 to 46.5 median decode; plus the 3-arm queue-cap matrix (three xhigh decode rates each, 48.2/48.9/42.2 vs 35.9/35.8/34.3 vs 35.9/36.2/37.2, 16K TTFT ~9.9 s).

## 2026-09-27: llama.cpp issue mining, second pass: 133 new rows across 15 issues

- **MTP6 vs baseline on three datacenter cards (llama.cpp #26750, 6 rows).** Qwen3.5-9B, b10290 official image, median of 108 runs per cell: draft-mtp n-max 6 vs no speculation - the W7900 goes 96 to 218 t/s and the RX 7800 XT 70 to 124, while the RTX PRO 4000 Blackwell drops 90 to 61.
- **RTX 5090 closed-loop server sweep (llama.cpp #27050, 8 rows).** Qwen2.5-7B-Instruct F16, 512+128 tokens per request at 1 and 32 concurrent: llama.cpp CUDA b9660 99.8/700.9, b10423 100.1/705.9, b10423 with the batching fix 101.4/1045.8, and vLLM BF16 92.9/1404.7.
- **DFlash on Strix Halo (llama.cpp #27117, 2 rows).** muse-glimmer 30B Q4_K on Radeon 8060S, 16 concurrent aggregate: 37 t/s with no speculation vs 80 with draft-dflash n-max 1 (0.83-0.92 acceptance, 2.2x the baseline).
- **Gated DeltaNet fused-op fix (llama.cpp #27327, 3 rows).** KAT-Coder-V2.5 on RTX 5080, three server-log runs after the fix (build 10154): 71.63/70.29/69.93 t/s.
- **ubatch and KV-quant interaction on R9700 (llama.cpp #27420, 4 rows).** qwen35 dense 27B at ctx 50000 with MTP3: ub256 f16 9.5, ub1024 f16 50, ub256 q8 53, ub1024 q8 60 t/s - the ubatch floor matters more than the KV quant.
- **Mamba2 flat-2d GEMM dispatch (llama.cpp #27464, 40 rows).** GB10 and RTX Pro 6000 Blackwell: Nemotron 3 Nano 30B-A3B NVFP4 across parallel-sequence lengths 1/8/32/256, current master vs the flat-2d fix (67.5 vs 67.7 at npl 1, 292.5 vs 660.8 at npl 256 on GB10; 1959.8 vs 3159.1 on the PRO 6000), plus mamba2-2.7b, Falcon-H1-7B, and granite-4.0-h-tiny at npl 32 in three quants each.
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
- New hardware pages: 2xR9700, 4x Tesla P40, Radeon AI PRO R9700, Radeon PRO W7900. New model pages include Nemotron 3 Nano 30B-A3B, mamba2-2.7b, Falcon-H1-7B, granite-4.0-h-tiny.
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
- **EAGLE3 on Qwen3 8B (vLLM #40551, 4 rows).** RTX PRO 6000 Blackwell Workstation Edition, MT-Bench with 80 concurrent requests, EAGLE3 RedHatAI speculator k=7, across the MRV1/MRV2 model-runner tables at temperature 0 and 1 (2021.33 to 3936.20 tok/s); each table is a separate `config=` variant.
- **CPU whisper (vLLM #38586, 1 row).** whisper-medium on a dual-socket Xeon 6767P (torch CPU build, TP2), 9.08 output tok/s at 2.67x real-time on LibriSpeech ASR; first CPU row from the vLLM source.
- **Qwen3-VL-30B position-computation PR (vLLM #27021, 2 rows).** A100 PCIe, FP8 VLM, request-rate 10 RPS, before and after PR #25337 (681.42 vs 689.02 tok/s).
- **4x B300 Qwen3.5-397B-A17B NVFP4 (vLLM #40350, 1 cluster row).** TP4+EP4 with MTP3 at concurrency 512: 12921.2 tok/s aggregate in the engine log at Running 493, from the crash-report bench (the last request then hangs at 0.0 tok/s); added to the cluster reference area (now 11 runs).
- Skipped from the same search pass: #51799 (KV-cache concurrency headroom, no tok/s), #56868 (qualitative degeneration report), #44705 (latency table, no tok/s), #50880 (hang report, 0.0 tok/s only), #55394 (TTFT/kernel-ms table, no tok/s), #37666 (no model name in body).
- Dataset: 2,636 measured records, 293 hardware strings, 128 models, 19 backends, plus 549 reference estimates and 11 cluster runs. Provenance: 746 sourced, 1,890 community. Flags unchanged: 521 contradiction, 34 outlier.

## 2026-09-27: vLLM issue mining pass: 36 new rows across six issues

- **A100 multimodal benchmarks (vLLM #24728, 25 rows).** Four VLMs (Qwen2.5-VL-7B, MiniCPM-V-4, InternVL3.5-4B, InternVL3.5-2B) on a single A100 40 GB, image and video inputs, at the published concurrency levels (1, 10, 50 and the unlimited-rate max-QPS test). Modality is a machine-readable `config=` token, so image and video rows flag separately.
- **B200 DeepSeek-R1-0528 (vLLM #29662, 4 rows).** 8x B200 TP8 with MTP speculative decoding at concurrency 256, FP8 and FP4, with and without `--async-scheduling` (1994/2421/2375/2895 tok/s).
- **H100 Qwen3 8B FP8 (vLLM #48518, 2 rows).** Concurrency 4; the two runs differ only in L2 cache state persisting from server startup (809.40 vs 839.75 tok/s), kept as separate `config=` variants.
- **4090D Qwen2.5-14B (vLLM #36629, 2 rows).** FP8+EAGLE3 vs W4A16+EAGLE3 at batch 16 (1131.19 vs 1079.15 tok/s).
- **gpt-oss 120B kernel regression (vLLM #37441, 3 rows).** 8x H200 node, TP2, concurrency 1, eagle speculative decoding: vLLM 0.16.0/Triton 3.5 (275.84), vLLM 0.17.1/Triton 3.6 (231.22), and 0.17.1 with the reverted legacy kernels (275.84 recovered).
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
- **22 new GitHub issue rows.** ExLlamaV2 #450 (2080 Ti, EXL2 4.0bpw, batched_inference and multi-cache scaling, 8 rows); vLLM #48071 (8x H200-NVL, Gemma-4-31B ITL by concurrency, 6 rows including the TRT-LLM row); #55139 (A100, gpt-oss 20B, MRV1/MRV2); #49369/#49370 (B300, DeepSeek-V4-Flash FP4, base/no-break/dspark); #58031 (GB300, DeepSeek-V4.1-Flash MXFP4); #39323 (H100, Qwen3.5-35B-A3B FP8 with FlashAttention-3); #30832 (H20, DeepSeek-V3.2, cluster scope).
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
