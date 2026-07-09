# Quant Trading — SWE Track

## Target

SWE (not researcher) roles at quantitative trading firms:

- **Tier 1:** Citadel, Citadel Securities, Two Sigma, Jane Street, Jump Trading, Hudson River Trading (HRT)
- **Tier 2:** Optiver, IMC, DRW, Tower Research, SIG, DE Shaw, Millennium
- **Ancillary:** Belvedere, Akuna, Radix, Old Mission, Squarepoint

These firms hire SWEs to build low-latency systems, market data pipelines, exchange gateways, and trading tools. Interview loops mix classical CS with domain-specific rigor.

## What's different from a FAANG loop

| Dimension | FAANG | Quant firm |
| --- | --- | --- |
| Coding language | Any | Usually **C++** (Citadel, HRT, Optiver, DRW) or **OCaml/F#** (Jane Street, some SIG). Python often accepted for phone screens. |
| Coding bar | Correctness + trade-offs | Correctness + **latency**, memory layout, cache behavior, and lock-free constructs at senior tiers |
| Probability/math | Rare | **Mandatory** — 1–2 rounds of brainteasers, Bayes, expected value, coin/dice puzzles |
| System design | Product-scale (feed, chat) | **Trading system-scale** — order book, matching engine, market data replay, backtesting infra |
| Behavioral | LP-flavored | Lightweight; more "why quant / why us" than STAR stories |

## What to prep — quick map

- **Coding:** algorithm/ (top-level) — Python-first, but must be able to translate to C++ under pressure for on-site rounds. C++ solutions under `algorithm/<cat>/cpp/` are your bilingual reference.
- **C++ fluency:** [`cpp-fundamentals.md`](./cpp-fundamentals.md) — cheat sheet for the C++ concepts that show up in Citadel-style rounds.
- **Probability & brainteasers:** [`probability.md`](./probability.md) — coin/dice puzzles, Bayes, expected value.
- **Domain systems:** [`systems.md`](./systems.md) — order book, matching engine, market data.
- **Company mocks:** [`../../company-tags/citadel/`](../../company-tags/citadel/) has real 面经 (interview reports).

## Files in this track

- [`roadmap.md`](./roadmap.md) — 6-week phased plan.
- [`cpp-fundamentals.md`](./cpp-fundamentals.md) — moved from `company-tags/citadel/` and expanded.
- [`probability.md`](./probability.md) — probability & brainteasers with worked solutions.
- [`systems.md`](./systems.md) — low-latency & trading system design primers.
- [`resources.md`](./resources.md) — books, blogs, GitHub repos.
