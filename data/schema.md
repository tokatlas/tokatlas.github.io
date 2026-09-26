# Token Atlas data schema

Every record is one measured (or explicitly estimated) inference speed figure
with full provenance. **No record without a source URL, retrieval date, and
the exact quoted values.**

## Fields

| field | type | meaning |
|---|---|---|
| `id` | string | stable unique slug (source+model+hardware+quant+backend) |
| `model` | string | model name as published by the source |
| `params` | string | parameter size as published (e.g. `8B`, `3.8B`); may be empty |
| `quant` | string | quantization, as published (e.g. `Q4_K_M`) |
| `hardware` | string | chip identifier as published (e.g. `M5 Max`, `RTX 4090`) |
| `ram_gb` | number | memory in GB, when the source states it; else empty |
| `backend` | string | inference backend/engine as published (llama.cpp, MLX, Ollama, LM Studio, vLLM, ExLlama, …) |
| `ctx` | number | context length in tokens, when stated; else empty |
| `batch` | number | batch size, when stated; else empty |
| `tps` | number | **generation** tokens/second |
| `pp_tps` | number | prompt-processing tokens/second, when reported; else empty |
| `ttft_s` | number | time to first token in seconds, when reported; else empty |
| `power_w` | number | power draw in watts, when reported; else empty |
| `date` | string | original measurement date as published (month or day granularity) |
| `provenance` | enum | `sourced` (linked public page with the quoted number), `community` (community-measured run carried in the source dataset), `estimated` (the source's own model-based estimate) |
| `source_url` | url | where the figure was retrieved from (per-row page when available, else the dataset download URL) |
| `source_name` | string | name of the source dataset/page |
| `retrieved` | date | UTC date the record was retrieved |
| `quote` | string | the exact values as they appear in the source (comma-joined row) |
| `notes` | string | collector notes (e.g. "LLMCheck model-based estimate (bandwidth model)") |

## Rules

1. **Provenance is mandatory.** Every row must pass `scripts/check_data.py`:
   required fields non-empty, `tps > 0`, `retrieved` not in the future,
   valid URL, unique id, and every recorded number must appear in `quote`.
2. **Normalize, don't rewrite.** Model/chip/quant names keep the source's
   spelling; normalization happens in presentation (slugs, grouping), never by
   silently editing values.
3. **Dedupe, then flag.** Duplicate records for the same
   (model, hardware, quant, backend) are collapsed to the newest retrieval;
   contradictions between sources for the same configuration are kept as
   separate rows and flagged on the site.
4. **Outliers** (e.g. tok/s more than 3× the median for the same
   (model, hardware, quant)) are kept but annotated, not deleted.
5. **Estimates are badged** everywhere and never mixed into measured-only
   aggregates.
6. **Attribution** is per source dataset, with its license recorded in
   `data/sources.json`.

## Current sources

See `data/sources.json` (machine-readable registry) and the site's
[complementary projects](https://tokatlas.github.io/) page.
