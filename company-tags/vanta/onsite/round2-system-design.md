# Round 2 — System Design: DAU / MAU Tracking

Reported multiple times as the specific prompt: **Design a system to track Daily Active Users (DAU) and Monthly Active Users (MAU).** Vanta's product is compliance-facing so the "user" is a customer employee touching the platform; scale is modest by consumer-app standards (~millions of end-users across their customer base, not billions).

Use Alireza's/ByteByteGo-style scaffold — the interviewer wants to see structure, not cleverness.

## 1. Clarifying questions (spend 5 min here)

- **Definition of "active":** any HTTP request? A meaningful action (login, doc upload, evidence review)? Ask.
- **Scale:** how many customers × employees each × avg actions/day? Rough order: 10K customers × 100 users × 20 actions/day ≈ 20M events/day.
- **Latency requirements:** query freshness — real-time (last-minute) or 15-min-lagging is OK?
- **Precision:** must DAU/MAU be exact, or is an HLL-based approximate count acceptable? (Approximate is usually fine.)
- **Retention:** how long do we keep event-level data vs aggregates?
- **Tenancy:** DAU/MAU per-customer (tenant), or global? (Almost certainly per-tenant for a B2B compliance product.)
- **Auditability:** since this is compliance, do we need immutable event logs?

## 2. Functional requirements

- Ingest user activity events at high write throughput.
- Compute DAU (unique users in the last calendar day) and MAU (unique users in the last 30 days).
- Query: per tenant, per date range, current running total.
- Historical time-series: show DAU over the last N days.

## 3. Non-functional

- Availability: 99.9%.
- Freshness: <5 min for the current day's counter.
- Cost: linear in events, ideally sub-linear in queries.
- Correctness under retries: idempotent event ingestion (dedup on client-side event id).

## 4. Estimate

- 20M events/day = 230 events/sec average, ~1K peak.
- Event payload: 200 bytes → 4 GB/day raw. 1.5 TB/year retained.

## 5. High-level architecture

```
Clients ─→ API Gateway ─→ Kafka (activity_events topic)
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
       Real-time counter   Batch aggregator   Raw log sink
       (Redis + HLL)       (Spark / dbt      (S3 / data lake)
                            per-day rollup)
                                │
                                ▼
                        Time-series store
                        (Postgres w/ TimescaleDB,
                         or ClickHouse)
                                │
                                ▼
                        Query API + dashboard
```

## 6. Design decisions to defend

### HyperLogLog (HLL) for the hot path

- DAU/MAU are cardinality queries. Exact set counting scales as O(n) memory per (day, tenant) — 100K employees × 10K tenants × 30 days quickly blows up.
- HLL gives you a **fixed-size sketch (~1.5 KB per bucket) with ~2% relative error**. Redis has native `PFADD` / `PFCOUNT` / `PFMERGE`.
- MAU can be computed by merging 30 daily HLL sketches → single-pass, ~50KB.

Trade-off: HLL is approximate. If the interviewer asks for exact counts, discuss bitmap-per-user-per-day (`Roaring bitmaps`) as an alternative — exact but heavier.

### Deduplication

- Client sends `event_id` (UUID). Ingestion side stores recent event ids in a bloom filter (or Redis SET with TTL) to drop duplicates before they hit the counter.

### Tenant isolation

- Keys are namespaced: `dau:{tenant_id}:{date}` and `mau:{tenant_id}:{date_prefix}`.
- Query API enforces tenant ID from the auth context; never trust the URL.

### Time-series storage

- Rollups written daily to Postgres/Timescale hypertable OR ClickHouse. One row per (tenant, date, dau, mau).
- Retention: raw events S3 for N years (compliance), sketches Redis for 32 days, rolled-up counts forever.

## 7. Deep dives the interviewer might drill

- **Late-arriving events.** An event with `timestamp = yesterday` shows up today. Options: window-of-tolerance, replay job, or "at write time we bucket by event.timestamp not receive_time".
- **HLL bias correction.** For small cardinalities HLL over-estimates. Redis's implementation uses HLL++ which handles this. Say so.
- **Scaling ingestion.** Kafka partitions by tenant_id → per-tenant ordering, hot tenants get more partitions.
- **Timezone.** DAU "day" — UTC or tenant's local timezone? Cheap gotcha; ask upfront.
- **Multi-region.** If tenants span regions, do we keep tenants on the region where they were provisioned, or replicate?
- **Backfill.** Someone asks for DAU/MAU for a period before the system existed. Show: replay raw events from S3 → regenerate sketches.

## 8. Considerations

- **Compliance-flavored twist:** since Vanta sells SOC 2, they DO care about immutability of audit logs. The raw event sink to S3 with object lock is not just for "cost", it's a compliance artifact.
- **Cost:** ~20M events/day at Kafka cost is trivial; the HLL memory is trivial; the biggest cost is retention of raw logs.
- **Privacy:** GDPR right-to-delete. HLL sketches can't be selectively edited — plan for periodic recomputation from raw logs after deletions.

## 9. Iteration / follow-ups

- V2: cohort retention (DAU by signup cohort).
- V3: feature-level DAU (which product surface is being used).
- V4: anomaly detection on DAU curves.

## Related material in this repo

- `system-design/mocks/` — general system design mock catalog
- [`tracks/genai-mle/ml-sys-design.md`](../../../tracks/genai-mle/ml-sys-design.md) — Alireza's 9-step scaffold (though this one is a classic sys design, not ML sys design)
