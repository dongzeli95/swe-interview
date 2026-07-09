"""
Vanta phone screen: Task Dependency.

Q1: Given all tasks + a list of target ids, return every task that any target
    depends on (transitively), in dependency order (a dep must appear before
    any task that depends on it), deduped across targets. Excludes the target
    ids themselves.

Q2: Given the same data + a single target id, return every task that
    transitively depends ON the target (its "ancestors").

Assumptions to CLARIFY with the interviewer before coding:
    - Is the graph guaranteed to be a DAG? (Defensively raise on cycle.)
    - For Q1, does the output include the target ids? (This impl excludes them.)
    - "Dependency order" = a topological order of the dep subgraph. Any valid
      topo order is accepted unless a specific tiebreak is requested.

Complexity: O(V + E) for both Q1 and Q2.
"""

from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class Task:
    id: str
    dependencies: list[str] = field(default_factory=list)


# ---------- Q1: transitive dependencies of a set of targets ----------

def dependencies_of_targets(all_tasks: list[Task], targets: list[str]) -> list[str]:
    by_id: dict[str, Task] = {t.id: t for t in all_tasks}
    target_set: set[str] = set(targets)
    for tgt in targets:
        if tgt not in by_id:
            raise KeyError(f"target {tgt!r} not found in all_tasks")

    # 1. Reachable-as-dependency set — DFS on dep edges from every target.
    #    A target can itself be reachable as a dep of another target
    #    (targets = [F, D], F depends on D). We collect all reachable ids
    #    here — including targets that surface as deps — because the topo
    #    sort needs the full induced subgraph. We drop targets from the
    #    final output at step 3.
    reachable: set[str] = set()
    stack: list[str] = []
    for tgt in targets:
        for dep in by_id[tgt].dependencies:
            if dep not in reachable:
                reachable.add(dep)
                stack.append(dep)
    while stack:
        node = stack.pop()
        for dep in by_id[node].dependencies:
            if dep not in reachable:
                reachable.add(dep)
                stack.append(dep)

    # 2. Topological sort restricted to `reachable` via Kahn's algorithm.
    #    Edge convention: dep → dependent (so a dep is emitted before what depends on it).
    reverse_adj: dict[str, list[str]] = defaultdict(list)
    in_degree: dict[str, int] = {node: 0 for node in reachable}
    for node in reachable:
        for dep in by_id[node].dependencies:
            if dep in reachable:
                reverse_adj[dep].append(node)
                in_degree[node] += 1

    queue: deque[str] = deque(n for n, d in in_degree.items() if d == 0)
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for dependent in reverse_adj[node]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    if len(order) != len(reachable):
        raise ValueError("cycle detected in dependency graph")

    # 3. Exclude targets from the final output. Ask the interviewer whether they
    #    want the targets in the answer; the common Vanta framing wants "extra
    #    work to complete before the targets", which excludes them.
    return [n for n in order if n not in target_set]


# ---------- Q2: transitive ancestors of a single target ----------

def ancestors_of_target(all_tasks: list[Task], target: str) -> list[str]:
    by_id: dict[str, Task] = {t.id: t for t in all_tasks}
    if target not in by_id:
        raise KeyError(f"target {target!r} not found in all_tasks")

    reverse_adj: dict[str, list[str]] = defaultdict(list)
    for task in all_tasks:
        for dep in task.dependencies:
            reverse_adj[dep].append(task.id)

    ancestors: list[str] = []
    seen: set[str] = {target}
    queue: deque[str] = deque([target])
    while queue:
        node = queue.popleft()
        for parent in reverse_adj[node]:
            if parent not in seen:
                seen.add(parent)
                ancestors.append(parent)
                queue.append(parent)

    return ancestors


# ---------- demo ----------

if __name__ == "__main__":
    #
    #   A ──┐
    #   B ──┤─→ D ─→ F
    #   C ──┘       ↑
    #          E ───┘
    #
    tasks = [
        Task("A"),
        Task("B"),
        Task("C"),
        Task("D", ["A", "B", "C"]),
        Task("E"),
        Task("F", ["D", "E"]),
    ]

    print("Q1  deps of [F]         :", dependencies_of_targets(tasks, ["F"]))
    print("Q1  deps of [D, E]      :", dependencies_of_targets(tasks, ["D", "E"]))
    print("Q1  deps of [F, D]      :", dependencies_of_targets(tasks, ["F", "D"]))
    print("Q2  ancestors of A      :", ancestors_of_target(tasks, "A"))
    print("Q2  ancestors of E      :", ancestors_of_target(tasks, "E"))
    print("Q2  ancestors of F      :", ancestors_of_target(tasks, "F"))
