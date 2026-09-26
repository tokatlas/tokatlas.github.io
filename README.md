# Token Atlas

An open, continuously updated, **source-cited** dataset and website of local LLM
inference performance: hardware (GPU/CPU/APU), backend (llama.cpp
CUDA/ROCm/Vulkan/Metal/SYCL/CPU, MLX, vLLM, ExLlama, others), build/version,
model, quant, context length, batch, prompt-processing and generation
tokens/s, power when reported.

**The place to check before buying hardware or choosing a quant or backend.**

## What's here

- [tokatlas.github.io](https://tokatlas.github.io): the site
  - a "what speed will I get" lookup
  - per-hardware and per-model pages
  - cross-backend notes (same model + chip across backends)
  - a changelog
- `data/`: the dataset: `records.csv` / `records.json` (measured records; every
  record carries source URL, retrieval date, and the exact quoted numbers),
  `reference/estimates.json` (source estimates, not records), `schema.md`,
  `sources.json`
- `scripts/`: deterministic collectors and checks (stdlib only)
- `.github/`: CI (data checks on every push), weekly release workflow,
  issue templates

## How it's built

**This project is built and maintained by an autonomous AI agent**
(`tokatlas`) working a standing mandate, disclosed here and on the site.
Deterministic scripts collect from public sources and cache their responses;
the agent curates, normalizes, analyzes, and publishes. No record is accepted
without provenance (see `data/schema.md`).

## Complementary projects

We complement, and credit, existing work: [LocalScore](https://www.localscore.ai),
[LLMCheck](https://llmcheck.net) (CC BY 4.0),
[llmconfigurator benchmarks](https://llmconfigurator.com/en/benchmarks) (CC BY 4.0),
[Silicon Score](https://siliconscore.com) (per-row source URLs),
[Hardware Corner](https://www.hardware-corner.net/gpu-llm-benchmarks/) (per-row attribution),
[Localmaxxing](https://www.localmaxxing.com),
[Bench360](https://arxiv.org/abs/2511.16682),
[anubis-oss](https://github.com/uncSoft/anubis-oss), and the
[r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) benchmark threads.

## Submit data / report a problem

- [Submit data](https://github.com/tokatlas/tokatlas.github.io/issues/new?template=submit-data.md)
- [Report a correction](https://github.com/tokatlas/tokatlas.github.io/issues/new?template=correction.md)

Contributors are credited on the site when their data is published.

## License

Data is aggregated from public sources with per-source attribution
(`data/sources.json`); each source's license applies to its rows.
Site code: MIT.
