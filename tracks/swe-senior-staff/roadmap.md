# Senior/Staff SWE — 8 Week Roadmap

Assumes ~10–15 hrs/week alongside a full-time job. Slide the phases as needed.

## Weeks 1–2: DSA breadth pass

Goal: touch every category in `algorithm/`, warm up in Python, identify weak spots.

- 1 category per day. Read the category's `README.md` and `md/` writeups, then solve 2–3 problems from `python/` from memory (peek at C++ ref if stuck).
- Weak categories to prioritize for round 2: DP, graph (BFS/DFS/union-find), monotonic stack, segment tree/Fenwick.
- End of week 2: run through [`problems.md`](./problems.md) — mark ✅/⚠️/❌ per problem.

## Weeks 3–4: DSA depth + timed reps

- Focus on ⚠️/❌ problems from problems.md. Do them under 25-min timer, cold, in a text file.
- Introduce mock coding rounds: 2 per week (Interviewing.io, Pramp, or with a peer).
- Start reading Alex Xu Vol. 1 / DDIA in parallel — 1 chapter per week.

## Weeks 5–6: System design

- Repo has `system-design/ddia/`, `system-design/deep-dive/`, `system-design/mocks/`.
- Cover the 10 classic mocks (URL shortener, chat, feed, ride share, distributed cache, rate limiter, geohash search, video streaming, notification system, ad click aggregator).
- For staff loops: add end-to-end product design (design a checkout flow, design a spam pipeline) and a 1-on-1 deep-dive (locks & consistency, replication, indexing).

## Week 7: Behavioral / leadership rehearsal

- Assemble 8 hero stories from the Amazon LP prep doc, tuned to STAR + LP.
- Map stories to common staff prompts: hardest bug, biggest tech disagreement, org-level influence, ambiguous mandate, mentorship, failed project + learnings.
- Do 2 behavioral mocks — even a peer reading the prompts aloud helps.

## Week 8: Full-loop simulation + polish

- Simulate a full onsite in a single day: 2 coding + 2 system design + 1 behavioral.
- Post-mortem each round, note what leaked context / time / clarity.
- Retire.

## Ongoing (parallel to all weeks)

- 1–2 LC problems/day from the `problems.md` "spaced repetition" section.
- Read 1 engineering blog post/week (High Scalability, ByteByteGo Newsletter).
- Keep a "questions I asked" note per company — signals engagement in the loop.
