# Cross-provider seats — verification receipts (11/11/26)

OpenRouter key confirmed by Sharon 11/11, before the Thursday 11/12 freeze. Per
`2026-11-10-convening-decisions.md` §lineup, the primary lineup therefore becomes:
Haiku 5.5 (same-API anchor) + one OpenAI seat + one open-weights seat, replacing
Sonnet 5.5 and Opus 5.5. Fable family remains recused. All hypothesis tests remain
within-model; cross-model comparison stays descriptive.

## Proposed seats (to freeze Thursday night)

| Seat | Model ID | Pricing (in/out per M) | Why |
|---|---|---|---|
| Anchor | `claude-haiku-5-5` (Anthropic API direct) | — | unchanged from decisions doc |
| OpenAI | `openai/gpt-5.6-terra` (OpenRouter) | $2.00 / $12.00 | mid-tier Sonnet-analog; Luna is Haiku-class, Sol/5.5-pro adds cost not inferential power in a within-model design |
| Open-weights | `deepseek/deepseek-v4-pro-0813` (OpenRouter) | $0.11 / $4.44 | dated snapshot (reproducible under the freeze hash, unlike `-latest` aliases); weights publicly on Hugging Face |

## Open-weights licensing check (11/11)

- **DeepSeek V4 Pro 0813** — weights published on Hugging Face (~1.7T params, 893 GB), reported by
  [Simon Willison](https://simonwillison.net/b/9595); DeepSeek V4 family released under MIT per
  [April 2026 release coverage](https://doolpa.com/news/deepseek-v4-preview-1m-context-mit-license-april-24-2026).
  Cleanest "open-weights" claim among current-gen candidates. **Chosen.**
- **Kimi K3** — weights released 7/27/26 but under a custom revenue-tiered license
  (commercial gate reported around $20M/yr revenue; sources disagree on mechanics:
  [VentureBeat](https://venturebeat.com/technology/kimi-k3s-full-weights-are-here-but-theyre-open-with-a-caveat-what-enterprises-should-know),
  [Unite.AI](https://www.unite.ai/moonshot-opens-kimi-k3-weights-under-a-revenue-tiered-license/)).
  Open-weights-with-caveat; rejected to keep the pre-reg claim clean.
- **Qwen dense (27b-class)** — likely Apache but a capability tier below the Sonnet-analog slot. Not pursued.

## Verification receipts (all calls 11/11, through the project `.env` keys)

- `openai/gpt-5.6-luna` → "pipe verified", cost $0.0000096 (first end-to-end OpenRouter call)
- `claude-haiku-5-5` → "anchor verified" (Anthropic API direct)
- `openai/gpt-5.6-terra` → "seat verified", cost $0.000096
- `deepseek/deepseek-v4-pro-0813` → "seat verified", cost $0.000073

Total verification spend: ~$0.0002.

## Key handling

Keys live only in the gitignored `.env` (shape documented in `.env.example`, commit b20e449).
OpenRouter is prepaid with a per-key spending cap available at openrouter.ai/settings/keys.
