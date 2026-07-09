# Vanta Phone Screen — Strategy & Problems

- **Duration:** ~60 minutes.
- **Environment:** CoderPad. Some candidates reported running locally instead (`python solution.py < input.txt`) — have a local Python env warm.
- **Structure:** 2 problems (Q1 + Q2 flavor). Q1 is a warmup; Q2 is a follow-up that reuses the data model.
- **Interviewer style:** quiet, slow to respond. You drive the discussion, verbalize your plan, ask clarifying questions.

## Time budget (60 min)

| Minute | What |
|---|---|
| 0–3 | Intros, high-level "tell me about yourself" |
| 3–8 | Clarify Q1 requirements — input format, output format, edge cases, expected complexity |
| 8–25 | Code Q1. Walk through 1 example before hitting "run". |
| 25–30 | Run Q1, verify output. Fix bugs if any. |
| 30–35 | Q2 setup — this is when you learn the follow-up. Clarify. |
| 35–52 | Code Q2. Reuse Q1 helpers where possible. |
| 52–58 | Test Q2, verify. |
| 58–60 | Q&A, wrap. |

If you're at min 25 and still debugging Q1: **stop, tell the interviewer what's broken, ask if you can move on and come back**. Reports suggest this is a common failure mode — one small bug in Q1 sinks Q2 entirely.

## Problem 1 (dominant — 5+ reports)

**Task Dependency** — see [`task_dependency.py`](./task_dependency.py) and [`task_dependency_test.py`](./task_dependency_test.py).

```
class Task:
    id: str
    dependencies: list[str]  # ids of tasks this task depends on

Q1: Given `all_tasks: list[Task]` and `targets: list[str]`,
    return ALL dependencies of the target tasks in dependency order,
    with no duplicates across targets.
    (Transitive deps of every target, deduped, in topological order.)

Q2: Given the same data, find all ANCESTOR tasks of a target
    (tasks that transitively depend ON the target).
    (Reverse graph, BFS/DFS from target.)
```

### Common bugs (from candidate reports)

- Not handling shared deps between targets — dedup must be across all targets, not per target.
- Emitting the target itself in the output. Q1 typically wants *deps only*, exclude the target. Clarify.
- Iterating `list.append` while iterating the same list.
- Cycle detection — the problem statement doesn't guarantee a DAG. Ask upfront: "Can I assume no cycles?"
- Confusing "depends on" vs "ancestor" directions. Draw the arrow direction on paper before coding.

## Problem 2 (backup — also multiple reports)

**Employee Security Training / Group aggregation** — see [`employee_training.py`](./employee_training.py) and [`employee_training_test.py`](./employee_training_test.py).

```
class Employee:
    id: str
    start_day: int
    training_days_required: int  # days after start_day by which they must complete training

Q1: Given `check_day`, is the employee compliant?
    If not, how many days overdue?
    Overdue = check_day - (start_day + training_days_required), or 0 if compliant.

Q2: Employees are in a TREE of groups:
    groups: dict[group_id, list[group_id]]  # parent → subgroups
    employees_by_group: dict[group_id, list[Employee]]

    For every group in the tree, compute:
        - total employee count (this group + all descendants)
        - total overdue days (summed over all employees in this + descendants)
```

### Common bugs

- Off-by-one in overdue calc. If they're due on day `S + T`, is `check_day = S + T` compliant or not? **Ask.**
- Q2: recomputing subtree state per group instead of caching (O(n²) instead of O(n)).
- Assuming the tree has a single root — the problem may have a forest. Ask.
- Missing groups with no direct employees but with subgroups.

## What NOT to spend time on

- Fancy Python (dataclasses, dunder methods) — plain dict + list is fine.
- Reading a file. Unless the interviewer explicitly asks, take the input as a Python literal in the same file.
- Comments beyond one-liners. The interviewer will read the code as you write it.

## Post-mortem template (fill after your drill)

- Q1 finished at min ___ / expected ~25. Bugs? ___
- Q2 finished at min ___ / expected ~52. Bugs? ___
- Which clarifying question would have saved you time?
- What did you not verbalize that you should have?
