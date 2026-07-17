# Vanta — Interview Prep

Vanta is a compliance automation platform (SOC 2, ISO 27001, HIPAA, GDPR). Their engineering interview loop, based on candidate reports from 1point3acres (June 2025 – June 2026):

| Stage | Format | What they test |
|---|---|---|
| **Phone screen** | 60 min, CoderPad (sometimes local Python) | Working code on 2 practical problems (see [`phone-screen.md`](./phone-screen.md)) |
| Onsite Round 1 | Coding — practical | Same problem *family* as phone screen; may involve reading from a file |
| Onsite Round 2 | System design | **DAU/MAU tracking system** — event ingestion → aggregation → query |
| Onsite Round 3 | "Principle" (scenario behavioral) | Hypothetical scenarios, not standard STAR. Bring stories anyway. |
| Onsite Round 4 | HM / Project deep-dive | Ownership, scope, cross-functional impact |
| Onsite Round 5 | AI technical deep-dive | Design a RAG pipeline (compliance-doc flavored) |

## Priority for Ben's phone screen

1. **Task Dependency** — 5+ reports. Both Q1 (deps of targets) and Q2 (ancestors). Solve cleanly in <30 min combined.
2. **Employee Training / Group aggregation** — backup problem, also reported multiple times.
3. **Time management** — don't get stuck debugging Q1; move on and come back.
4. **Environment** — Ben's screen is CoderPad (confirmed), but keep a local Python env ready in case they switch.

## Files

- [`phone-screen.md`](./phone-screen.md) — strategy, format notes, links to both problems.
- [`task_dependency.py`](./task_dependency.py) — reference solution for Q1 + Q2. Runnable.
- [`task_dependency_test.py`](./task_dependency_test.py) — test cases mirroring reported variants.
- [`employee_training.py`](./employee_training.py) — reference solution.
- [`employee_training_test.py`](./employee_training_test.py) — test cases.
- [`onsite/`](./onsite/) — one file per onsite round.

## How to drill

- 25-min timer per problem, cold start. Solve in a scratch file, then diff against the reference.
- Verbalize as you code — the interviewer is quiet by report; you drive the discussion.
- If stuck at 10 min: state your current thinking out loud. Interviewers grade communication as much as code.
- After the drill: read the "common bug" section in the problem file to catch what you'd have missed.
