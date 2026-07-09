# Quant SWE — 6 Week Roadmap

Assumes DSA baseline is already reasonable (i.e., you're also running the SWE senior/staff track). This roadmap layers quant-specific prep on top.

## Week 1: Language & fluency

- If not fluent in C++: read Effective Modern C++ (Meyers) Ch. 1–5, and skim [`cpp-fundamentals.md`](./cpp-fundamentals.md).
- If Jane Street-bound: install OCaml + go through the first 3 chapters of Real World OCaml. Otherwise skip.
- Warm up: 5–10 easy LC problems in C++ (not Python) to get syntax back.

## Weeks 2–3: Probability & brainteasers

- Work through [`probability.md`](./probability.md) end to end. Every problem, first attempt cold. If stuck ≥10 min, read solution, redo the next day.
- Supplement: *A Practical Guide to Quantitative Finance Interviews* (Zhou), *Heard on the Street* (Crack). See [`resources.md`](./resources.md).
- Daily: 3 probability puzzles + 2 LC mediums (mixed topics) in C++.

## Week 4: DSA / algorithm re-pass in C++

- Re-solve one problem per category from `algorithm/<cat>/python/` in **C++** using the sibling `cpp/` file only as a hint if fully stuck.
- Focus categories for quant: array/two-pointer, heap, dp (path counting / expected value), monotonic stack, trie, segment tree/Fenwick.
- Introduce mock coding rounds (mixed FAANG-style + brainteaser rounds).

## Week 5: Domain systems

- Read [`systems.md`](./systems.md).
- Build one small project: an in-memory limit order book with add/cancel/match, or a market data replay tool that ingests LOBSTER-format ticks.
- Learn to talk about: kernel bypass (DPDK/Solarflare), lock-free queues, cache line contention, NUMA, hot path vs cold path.

## Week 6: Company-specific mocks + polish

- Citadel: expect deep C++ trivia (destructor order, RAII, undefined behavior), plus probability + coding. See `company-tags/citadel/`.
- Two Sigma: heavy on data structures, plus systems / OS. Less brainteaser than Citadel.
- Jump: probability + coding, tends to be less flashy than Citadel.
- HRT: multiple long-form coding rounds, deep C++.
- Jane Street: OCaml + probability, "market making" mental math.

## Ongoing

- 1 brainteaser + 1 C++ problem daily.
- Read *Trading and Exchanges* (Harris) — 1 chapter/week — even if you never talk about microstructure in the loop, it changes how you reason about the domain.
