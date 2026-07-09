# Quant SWE — Reading List

## Books (probability / brainteasers)

- **Zhou, *A Practical Guide to Quantitative Finance Interviews*** — the canonical prep book. Work every problem.
- **Crack, *Heard on the Street*** — dense, mix of quant finance and general brainteasers.
- **Falkoff, *Fifty Challenging Problems in Probability*** — Mosteller. Short, deep.
- **Ross, *A First Course in Probability*** — reference textbook when a puzzle needs a refresher.

## Books (C++ / systems)

- **Meyers, *Effective Modern C++*** — 42 items on move semantics, `auto`, smart pointers, concurrency.
- **Williams, *C++ Concurrency in Action*** — actually read Ch. 1–5 before any HRT / Citadel loop.
- **Fedor Pikus, *The Art of Writing Efficient Programs*** — cache, branch prediction, SIMD.
- **Sutter, *Exceptional C++* series** — for the trivia rounds.
- **Kerrisk, *The Linux Programming Interface*** — reference for syscalls, epoll, signals.

## Books (trading domain)

- **Harris, *Trading and Exchanges*** — how markets actually work.
- **Cartea/Jaimungal/Penalva, *Algorithmic and High-Frequency Trading*** — quant researcher-flavored but the SWE benefits from the vocabulary.
- **Aldridge, *High-Frequency Trading*** — dated but useful primer.

## Blogs & sites

- **Optiver Insights** — https://optiver.com/insights/ — genuinely technical, often trading-system topics.
- **Jane Street Tech Blog** — https://blog.janestreet.com/ — OCaml-heavy but the engineering thinking generalizes.
- **HRT Beacon** — https://www.hudson-trading.com/hrt-beacon — company culture + tech.
- **Databento Engineering Blog** — https://databento.com/blog — very concrete market data internals.
- **Mechanical Sympathy** (Martin Thompson) — foundational LMAX Disruptor writing.
- **Erik Rigtorp** — https://rigtorp.se/ — SPSC queues, memory ordering, lock-free primitives.

## GitHub repos

- `rigtorp/SPSCQueue` — lock-free single-producer single-consumer queue, MIT-licensed reference.
- `preshing/junction` — concurrent hash map benchmarks.
- `abseil/abseil-cpp` — production-quality hash maps (Swiss tables).
- `alphaville/adept` — auto-differentiation in C++ (relevant if you touch quant research infra).
- `Adamage/QuantitativeInterviews` — mixed problem set, useful for warmup.

## Video / lectures

- Andrei Alexandrescu talks on `std::allocator`, small string optimization.
- CppCon talks by Fedor Pikus (branch prediction), Chandler Carruth (compilers).
- QuantResearch YouTube — mixed quality but some good problem walkthroughs.

## Company-specific mock questions

Already in this repo:
- [`../../company-tags/citadel/`](../../company-tags/citadel/) — 面经 collection and problems.

Add-on (not in repo):
- Glassdoor + Blind (search `<company> <role> interview`) — mine the last 12 months.
- 1point3acres (Chinese) — Citadel / Two Sigma / Jump 面经 threads.
