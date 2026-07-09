# GenAI Machine Learning Engineer — Track

## Target

Pivot into an MLE role with GenAI / LLM specialization. Two tiers:

- **Frontier labs:** OpenAI, Anthropic, Google DeepMind, Mistral, Meta FAIR-adjacent product teams, xAI.
- **GenAI product teams:** Instacart AI, Uber AI FDE, LinkedIn Gen AI, Airbnb applied ML, Stripe, Fireworks AI, Perplexity, Together AI, Cursor / Sourcegraph / Replit applied ML.

The role sits between SWE and researcher: you're expected to (a) ship production ML systems, (b) reason about model behavior at a mechanistic level, and (c) design GenAI applications end-to-end (prompt strategy, RAG, evals, fine-tuning, guardrails).

## What's different from a SWE loop

| Dimension | Regular SWE | GenAI MLE |
| --- | --- | --- |
| Coding | LC-style DSA | LC + ML coding (implement attention, tokenizer, k-means, PCA) |
| System design | Product-scale | **ML system design** — feature store, model serving, training pipeline, feedback loop, evals |
| Domain knowledge | Optional | **Required** — transformer internals, RLHF vs DPO, RAG patterns, quantization, distributed training |
| Behavioral | Standard | Often includes "case study" or product-flavored round for GenAI PM-adjacent roles |

## Files in this track

- [`roadmap.md`](./roadmap.md) — 12-week plan (this pivot takes longer than the other tracks).
- [`resources.md`](./resources.md) — books, courses, papers, GitHub repos. **Extracted from the 1point3acres thread** you provided plus canonical additions.
- [`ml-coding.md`](./ml-coding.md) — the ~15 "implement X from scratch" problems that show up in MLE loops.
- [`ml-sys-design.md`](./ml-sys-design.md) — ML system design cheatsheet (Alireza's 9-step formula + variations).
- [`interview-loops.md`](./interview-loops.md) — company-specific loop structures (OpenAI/Anthropic/DeepMind reported flows).

## Where to start

If you're new to LLMs: **Karpathy's [nn-zero-to-hero](https://github.com/karpathy/nn-zero-to-hero)**. Build makemore → GPT from scratch. 40 hours well spent.

Then work `roadmap.md` sequentially.
