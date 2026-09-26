name: Submit a data point
about: Submit a local LLM inference result for inclusion in the dataset
title: "[data] "
labels: [data]
body:
  - type: markdown
    attributes:
      value: |
        Submit a measured result. We include what can be cited: **please link the
        public page where the number appears** (GitHub issue/discussion, forum
        post, blog, HN thread). If you ran it yourself, paste the exact command
        and the exact output so we can verify and quote it.
  - type: input
    id: model
    label: Model (name + params)
    required: true
    placeholder: e.g. Llama 3.1 8B Instruct
  - type: input
    id: quant
    label: Quantization
    required: true
    placeholder: e.g. Q4_K_M
  - type: input
    id: hardware
    label: Hardware
    required: true
    placeholder: e.g. RTX 4090 24GB, M4 Max 36GB, Ryzen 7945HX 32GB
  - type: input
    id: backend
    label: Backend + version/build
    required: true
    placeholder: e.g. llama.cpp b4962 CUDA, MLX 0.28, vLLM 0.8.5, Ollama 0.9
  - type: input
    id: ctx
    label: Context length
    placeholder: e.g. 4096
  - type: input
    id: tps
    label: Generation tokens/s
    required: true
  - type: input
    id: pp
    label: Prompt-processing tokens/s (optional)
  - type: input
    id: ttft
    label: Time to first token, s (optional)
  - type: input
    id: power
    label: Power draw, W (optional)
  - type: input
    id: date
    label: When you measured (optional)
  - type: input
    id: source
    label: Public URL with the exact numbers (or "self-run" + paste output below)
    required: true
  - type: textarea
    label: Exact output / command / notes
    placeholder: |
      e.g. the llama-bench output block, or:
      ./llama-bench -m model.gguf -p 512 -n 128
      load: 1.23s
      pp512: 345.6 tok/s
      tg128: 42.1 tok/s
