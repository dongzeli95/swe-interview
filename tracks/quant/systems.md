# Trading Systems — Design Primers

The system-design rounds at quant SWE loops don't ask about newsfeeds or ride sharing. They ask about domain-specific systems where microseconds matter. This document primes you on the models interviewers expect you to reach for.

## Order book (limit order book / LOB)

- **Data structure:** sorted price levels + FIFO queue at each level. Common shapes:
  - `std::map<Price, Level>` — O(log P) insert, ordered iteration.
  - `array indexed by price ticks` — O(1) if price range is bounded and dense.
  - Hybrid: hot ± N ticks in an array, cold levels in a `map`.
- **Operations to support:** add, cancel, modify, match. Each must be O(1) or O(log n).
- **Common ask:** implement `add` and `cancel` given an order ID; discuss data structures to enable O(1) cancel-by-id (index of order id → level and position).
- **Follow-up:** how do you replay a session? How do you handle a market data snapshot + incremental updates?

## Matching engine

- Price/time priority is standard for equities. Pro-rata for some futures.
- Self-match prevention (an aggressor from participant X shouldn't match its own resting quote).
- Cross prevention across venues.
- What happens on a locked market (bid == ask)? Auction.
- Discuss: how to make matching deterministic across replicas (sequencer pattern).

## Market data pipeline

- **Ingest:** FIX / ITCH / OUCH / SBE / proprietary binary. Multicast UDP (SIAC, OPRA), gap detection, arbitrage of A/B feeds.
- **Normalization:** venue-specific → canonical schema.
- **Fan-out:** shared memory ring buffer to N consumer processes on same host.
- **Latency budget:** decode + normalize + publish in <1µs is the bar.

## Order gateway / OMS

- Session management (FIX login, sequence numbers, resend requests).
- Order lifecycle: NEW → ACK / REJECT → PARTIAL_FILL → FILL → CANCELED / EXPIRED.
- Risk checks pre-trade: max position, max notional, fat-finger, kill switch.
- Idempotency — what if the exchange ACK is lost?

## Backtesting

- Event-driven: process ticks in chronological order, invoke strategy callback.
- Vectorized: bar-level, pandas-heavy, faster but hides intra-bar behavior.
- Reproducibility: fixed random seed, versioned data snapshots, deterministic ordering when two events have the same timestamp.

## Low-latency techniques

- **Kernel bypass:** DPDK, Solarflare Onload, Mellanox VMA. NIC → user space directly.
- **Busy polling** vs interrupt-driven — trade CPU for latency.
- **CPU pinning + isolcpus** to avoid preemption.
- **NUMA awareness:** allocate memory on the same node as the thread using it.
- **Cache lines:** 64B. Pad hot atomics; group cold fields separately.
- **Branch-free code paths** in the hot loop.
- **Lock-free queues:** SPSC ring buffer (Vyukov) is the common ask.
- **Timestamps:** use `rdtsc` calibrated against a monotonic clock; know its pitfalls (CPU migration invariance).

## Common design questions

1. Design an order book that supports 1M inserts/sec with O(1) cancel.
2. Design a market data replay system that reads a 100GB log and emits ticks at recorded pacing.
3. Design a persistence layer for orders that survives crash but adds <1µs latency to the hot path.
4. Two servers must agree on a single price; describe a sequencer.
5. Design a strategy sim that runs the same code against paper trading and live — what stays the same, what varies?

## Books & blogs

- *Trading and Exchanges* — Larry Harris. Domain foundation.
- *Flash Boys* — Michael Lewis. Culture and context, not technical.
- *Algorithmic and High-Frequency Trading* — Cartea, Jaimungal, Penalva. More quant researcher than SWE, but useful.
- Optiver tech blog, Jane Street tech blog, HRT blog on `hudson-trading.com`.
- Databento's engineering blog — very hands-on with market data internals.
