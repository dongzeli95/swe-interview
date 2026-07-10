"""
Vanta phone screen: Task Dependency.

═══════════════════════════════════════════════════════════════════════════
                   INTERVIEW APPROACH — READ THIS FIRST
═══════════════════════════════════════════════════════════════════════════

PROBLEMS
--------
Q1: Given `all_tasks` (each task has an id + list of dependency ids) and
    `targets` (list of task ids), return every task that any target
    transitively depends on, in a valid execution order (a dep must
    appear before anything that depends on it). Excludes the targets
    themselves. Deduped across targets.

Q2: Given the same input + a single target id, return every task that
    transitively depends ON the target (its "ancestors" up the graph).

───────────────────────────────────────────────────────────────────────────
STEP 1 — CLARIFYING QUESTIONS (ASK 2-3 BEFORE CODING)
───────────────────────────────────────────────────────────────────────────
Interviewers score you on these. Jumping straight to code signals you're
guessing. If the prompt is sparse, ask:

    1. "Should the output include the target ids themselves, or only
        their dependencies?"
        → This impl excludes targets (common Vanta framing: "extra work
          needed before completing the targets"). Confirm.

    2. "Is the graph guaranteed to be a DAG, or should I detect cycles
        like A depends on B and B depends on A?"
        → If cycles possible: raise on detection.
        → Kahn's algorithm catches them for free
          (len(topo_order) != len(reachable_set) ⇒ cycle).

    3. "Will `all_tasks` contain tasks that no target depends on —
        unrelated islands in the graph?"
        → Almost always yes. Those tasks MUST NOT appear in the output.
        → This is what motivates the reachability (BFS) step.

    4. "Is any valid topological order acceptable, or do you want a
        specific tiebreak (e.g., alphabetical among equals)?"
        → Usually any valid order. If specific, swap Kahn's queue for a heap.

    5. "Can a dep id reference a task not in `all_tasks`? Duplicate ids
        in all_tasks or in targets? Empty targets list?"
        → Usually no on all three, but confirm — cheap questions with
          large downside if wrong.

───────────────────────────────────────────────────────────────────────────
STEP 2 — SOLUTION PROGRESSION (narrate this out loud)
───────────────────────────────────────────────────────────────────────────
The interviewer scores your reasoning, not just the final code. Walk them
through the progression:

  APPROACH A — recursive post-order DFS from each target
    def dfs(node):
        if node in visited: return
        visited.add(node)
        for dep in by_id[node].dependencies:
            dfs(dep)
        if node not in target_set:
            result.append(node)   # post-order → topo order for free
    for tgt in targets: dfs(tgt)

    ✓ Reachability + ordering in ONE pass (post-order emission).
    ✗ Python recursion limit (~1000) blows up on deep chains.
    ✗ Cycle detection needs 3-color DFS (WHITE/GRAY/BLACK).
    Complexity: O(V + E).

  APPROACH B — two-pass, per-target BFS + Kahn's  (see: dependencies_of_targets_brute)
    Pass 1: For each target, BFS its deps into a fresh visited set. Union.
    Pass 2: Kahn's topo sort restricted to the union.

    ✓ Iterative — no recursion limit.
    ✓ Cycle detection free from Kahn's.
    ✗ Pass 1 re-walks shared subgraphs across targets.
    Complexity: O(k*(V + E)) + O(V + E) where k = len(targets).

  APPROACH C — two-pass, multi-source BFS + Kahn's  (see: dependencies_of_targets)
    Pass 1: ONE BFS starting from ALL targets simultaneously, sharing a
            single `reachable` set. Each node enqueued at most once.
    Pass 2: Same Kahn's as B.

    ✓ Every advantage of B, without the k-fold waste.
    Complexity: O(V + E) total.

Narration template:
    "I'd start with recursive post-order DFS — clean and one-pass. But two
     concerns: Python's recursion limit on deep chains, and cycle detection
     is finicky (3-color). Let me switch to iterative Kahn's — that gives
     cycle detection for free. First pass finds the reachable subgraph
     from the targets, second pass topo-sorts it. One optimization: instead
     of a fresh BFS per target, one multi-source BFS with a shared visited
     set — same work regardless of overlap."

───────────────────────────────────────────────────────────────────────────
STEP 3 — MENTAL MODEL
───────────────────────────────────────────────────────────────────────────
The whole algorithm is a two-phase pipeline: SCOPE DOWN, then ORDER.

  Phase 1 (BFS reachability): "Which tasks are we even talking about?"
                              Prunes unrelated tasks from all_tasks so
                              phase 2 doesn't waste work on them.

  Phase 2 (Kahn's topo sort): "In what order should we run them?"
                              Also gives cycle detection for free.

Any graph problem shaped like "given a big graph + a starting set, do X
only within reach" tends to fit this shape (Course Schedule II, Clone
Graph, etc.). Q2 is Q1 with edges reversed — "what depends on me?" walks
the graph backwards.

COMPLEXITY
----------
Q1 brute:      O(k*(V+E)) reachability + O(V+E) topo = O(k*(V+E))
Q1 optimized:  O(V + E)
Q2:            O(V + E)
═══════════════════════════════════════════════════════════════════════════
"""

from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class Task:
    id: str
    dependencies: list[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════
# Q1 APPROACH B (brute force): per-target BFS + Kahn's topo sort
# ═══════════════════════════════════════════════════════════════════════════

def dependencies_of_targets_brute(all_tasks: list[Task], targets: list[str]) -> list[str]:
    """APPROACH B — the natural first version to code in an interview.

    Intuition:
        Two questions, two passes.
        Q1: "Which tasks matter?"   → BFS from each target, union the results.
        Q2: "In what order?"        → Kahn's topo sort on that subgraph.

    Why not just Kahn's on all_tasks?
        Kahn's would happily topo-sort the entire task universe, including
        unrelated islands (tasks no target depends on). We'd have to filter
        those out at the end — and filtering requires the reachability info
        anyway. So we compute reachability first and prune upfront.

    Why not optimal?
        Pass 1 uses a fresh visited set per target. If F and G both depend
        on D, D's whole subtree gets walked twice. See `dependencies_of_targets`
        below for the fix (shared visited set).

    Complexity: O(k*(V+E)) reachability + O(V+E) topo, where k = |targets|.
    """
    by_id: dict[str, Task] = {t.id: t for t in all_tasks}
    target_set: set[str] = set(targets)

    # Defensive: catch bad input at the boundary. Cheap to check, hard to debug otherwise.
    for tgt in targets:
        if tgt not in by_id:
            raise KeyError(f"target {tgt!r} not found in all_tasks")

    # ─── PASS 1: Reachability (per-target BFS, union results) ──────────
    # WHY: We must know which tasks the targets transitively depend on so
    # we can (a) prune the input for pass 2 and (b) exclude unrelated
    # tasks from the final output.
    #
    # WHY per-target (not multi-source): This is the "naive" version — for
    # each target, we run a full BFS with a fresh `per_target_seen` set.
    # Then we union everything into `reachable`. Wasteful when targets
    # share deps, but very easy to reason about.
    reachable: set[str] = set()
    for tgt in targets:
        per_target_seen: set[str] = set()
        queue: deque[str] = deque()
        # Seed with target's *direct* deps — not the target itself, since
        # we want to exclude targets from the output.
        for dep in by_id[tgt].dependencies:
            if dep not in per_target_seen:
                per_target_seen.add(dep)
                queue.append(dep)
        while queue:
            node = queue.popleft()
            for dep in by_id[node].dependencies:
                if dep not in per_target_seen:
                    per_target_seen.add(dep)
                    queue.append(dep)
        reachable |= per_target_seen

    # ─── PASS 2: Kahn's topological sort restricted to `reachable` ─────
    # WHY Kahn's over recursive DFS: (1) iterative → no Python stack
    # limit; (2) built-in cycle detection via `len(order) != len(reachable)`.
    #
    # Edge convention: dep → dependent (so a dep is emitted before what
    # depends on it). in_degree[X] = "how many deps X has that are still
    # unprocessed." When in_degree[X] == 0, X's deps are all done → emit X.
    reverse_adj: dict[str, list[str]] = defaultdict(list)
    in_degree: dict[str, int] = {node: 0 for node in reachable}
    for node in reachable:
        for dep in by_id[node].dependencies:
            if dep in reachable:  # (redundant given BFS invariant, kept for clarity)
                reverse_adj[dep].append(node)
                in_degree[node] += 1

    queue = deque(n for n, d in in_degree.items() if d == 0)
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for dependent in reverse_adj[node]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    # WHY this check: if a cycle exists, some nodes never reach in_degree
    # 0, so they're never emitted. len(order) < len(reachable) is the tell.
    if len(order) != len(reachable):
        raise ValueError("cycle detected in dependency graph")

    # ─── PASS 3 (trivial): filter out targets from the output ──────────
    # WHY: The problem asks for "extra work needed before the targets."
    # Targets in `reachable` (when one target depends on another) must be
    # dropped here. Confirm this framing with the interviewer upfront.
    return [n for n in order if n not in target_set]


# ═══════════════════════════════════════════════════════════════════════════
# Q1 APPROACH C (optimized): multi-source BFS + Kahn's topo sort
# ═══════════════════════════════════════════════════════════════════════════

def dependencies_of_targets(all_tasks: list[Task], targets: list[str]) -> list[str]:
    """APPROACH C — the optimization to converge on if you have time.

    The ONE key insight vs. brute:
        Instead of running a fresh BFS per target, seed a single BFS queue
        with the direct deps of EVERY target upfront and share ONE visited
        set (`reachable`) across the whole traversal. This turns k separate
        BFSes into one multi-source BFS. Any node reachable from multiple
        targets gets processed exactly once.

    Pass 2 (Kahn's) and pass 3 (filter) are byte-identical to brute — the
    only diff is pass 1. That's the "diff between naive and optimized" you
    can point at during the interview.

    Complexity: O(V + E) total.
    """
    by_id: dict[str, Task] = {t.id: t for t in all_tasks}
    target_set: set[str] = set(targets)

    for tgt in targets:
        if tgt not in by_id:
            raise KeyError(f"target {tgt!r} not found in all_tasks")

    # ─── PASS 1: Multi-source BFS (SHARED visited set) ─────────────────
    # `reachable` does double duty: (a) the visited set that prevents
    # re-processing shared subgraphs and cycles, (b) the final set of
    # in-scope tasks that pass 2 will topo-sort.
    #
    # Seeding: enqueue every target's direct deps upfront (not the targets
    # themselves — we want to exclude targets from output). Then a single
    # BFS drains the queue. The `if dep not in reachable` guard means each
    # node enters the queue at most once, regardless of how many paths
    # reach it.
    #
    # Edge case worth mentioning: if targets = [F, D] and F depends on D,
    # then D ends up in `reachable` (F pulls it in). Its own deps then get
    # explored during BFS. We drop D from the final output in step 3.
    reachable: set[str] = set()
    queue: deque[str] = deque()
    for tgt in targets:
        for dep in by_id[tgt].dependencies:
            if dep not in reachable:
                reachable.add(dep)
                queue.append(dep)
    while queue:
        node = queue.popleft()
        for dep in by_id[node].dependencies:
            if dep not in reachable:
                reachable.add(dep)
                queue.append(dep)

    # ─── PASS 2: Kahn's topological sort restricted to `reachable` ─────
    # Identical to brute. Kahn's gives us:
    #   (1) a valid topo order (deps before dependents), and
    #   (2) cycle detection for free.
    reverse_adj: dict[str, list[str]] = defaultdict(list)
    in_degree: dict[str, int] = {node: 0 for node in reachable}
    for node in reachable:
        for dep in by_id[node].dependencies:
            if dep in reachable:
                reverse_adj[dep].append(node)
                in_degree[node] += 1

    queue = deque(n for n, d in in_degree.items() if d == 0)
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

    # ─── PASS 3: Filter targets from output ────────────────────────────
    return [n for n in order if n not in target_set]


# ═══════════════════════════════════════════════════════════════════════════
# Q1 VARIANT: same problem, but INCLUDE the targets in the output
# ═══════════════════════════════════════════════════════════════════════════

def dependencies_of_targets_include(all_tasks: list[Task], targets: list[str]) -> list[str]:
    """Variant of `dependencies_of_targets` that INCLUDES the target ids in
    the output, in valid topo order alongside their deps.

    Use this when the interviewer answers clarifying question #1 with
    "include the targets" instead of "just their deps."

    Two changes vs the exclude version:
        1. BFS init seeds with the TARGETS THEMSELVES, not their deps.
           (This ensures every target lands in `reachable`, including
            targets that no other target depends on.)
        2. No filter step at the end — return the topo order as-is.

    Complexity: O(V + E) — same as the exclude version.
    """
    by_id: dict[str, Task] = {t.id: t for t in all_tasks}
    for tgt in targets:
        if tgt not in by_id:
            raise KeyError(f"target {tgt!r} not found in all_tasks")

    # PASS 1: Multi-source BFS — seed with targets THEMSELVES.
    reachable: set[str] = set()
    queue: deque[str] = deque()
    for tgt in targets:
        if tgt not in reachable:
            reachable.add(tgt)
            queue.append(tgt)
    while queue:
        node = queue.popleft()
        for dep in by_id[node].dependencies:
            if dep not in reachable:
                reachable.add(dep)
                queue.append(dep)

    # PASS 2: Kahn's — identical to exclude version.
    reverse_adj: dict[str, list[str]] = defaultdict(list)
    in_degree: dict[str, int] = {node: 0 for node in reachable}
    for node in reachable:
        for dep in by_id[node].dependencies:
            if dep in reachable:
                reverse_adj[dep].append(node)
                in_degree[node] += 1

    queue = deque(n for n, d in in_degree.items() if d == 0)
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

    # PASS 3: No filter — targets are already in the topo order in the
    # correct position (after their deps).
    return order


# ═══════════════════════════════════════════════════════════════════════════
# Q2: transitive ancestors of a single target
# ═══════════════════════════════════════════════════════════════════════════

def ancestors_of_target(all_tasks: list[Task], target: str) -> list[str]:
    """Q2 is Q1 with the edges reversed.

    Q1 asks: "what does target DEPEND on?" — walk forward along dep edges.
    Q2 asks: "what DEPENDS on target?" — walk backward along dep edges.

    Trick: build the REVERSE adjacency list once (`dep → list of dependents`),
    then BFS from the target. No topo sort needed — the problem doesn't ask
    for order among ancestors, so plain BFS discovery order is fine.

    Complexity: O(V + E) — build reverse adj is O(V + E), BFS is O(V + E).

    If the interviewer wants a specific order among ancestors, confirm
    what they want (topological? alphabetical?) before coding.
    """
    by_id: dict[str, Task] = {t.id: t for t in all_tasks}
    if target not in by_id:
        raise KeyError(f"target {target!r} not found in all_tasks")

    # ─── Build reverse adjacency: dep → list of things that depend on it ─
    # WHY: The input gives us "who I depend on" per task. To answer "who
    # depends on ME," we need to flip the edges once and then walk normally.
    reverse_adj: dict[str, list[str]] = defaultdict(list)
    for task in all_tasks:
        for dep in task.dependencies:
            reverse_adj[dep].append(task.id)

    # ─── BFS from target along the reverse edges ───────────────────────
    # `seen` starts with target because we don't want target in the output
    # (we're returning ancestors, which by definition excludes self).
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


# ═══════════════════════════════════════════════════════════════════════════
# demo — verify both Q1 versions produce valid topo orders
# ═══════════════════════════════════════════════════════════════════════════

def _validate_topo(output: list[str], tasks_by_id: dict[str, Task], expected: list[str]) -> str:
    """Return 'PASS' if `output` (a) contains exactly the expected set of ids
    and (b) is a valid topological order (every dep appears before its
    dependent). Otherwise a diagnostic string.

    Topo order isn't unique, so we can't string-match — we check the two
    properties that DEFINE correctness instead.
    """
    if set(output) != set(expected):
        missing = sorted(set(expected) - set(output))
        extra = sorted(set(output) - set(expected))
        return f"FAIL (content) — missing={missing}, extra={extra}"
    positions = {n: i for i, n in enumerate(output)}
    for tid in positions:
        task = tasks_by_id.get(tid)
        if task is None:
            continue
        for dep in task.dependencies:
            if dep in positions and positions[dep] >= positions[tid]:
                return f"FAIL (order) — {dep!r} must appear before {tid!r} in {output}"
    return "PASS"


if __name__ == "__main__":
    # Fixture-driven demo. Cases live in test_fixtures.json alongside this
    # file. The runner loads the fixture, executes each case against all
    # three Q1 variants (brute, optimized, include) and Q2, and validates
    # results by (a) set equality vs expected, (b) topological validity.
    #
    # Topological order is NOT unique — if A, B, C all have no deps, any
    # order among them is valid. That's why validation checks content +
    # topo validity, not string equality.
    import json
    from pathlib import Path

    fixture_path = Path(__file__).parent / "test_fixtures.json"
    with open(fixture_path) as f:
        fixtures = json.load(f)

    total, passed = 0, 0

    for graph_spec in fixtures["graphs"]:
        print("=" * 76)
        print(f"GRAPH: {graph_spec['name']}")
        print(f"  {graph_spec['description']}")
        for line in graph_spec.get("ascii_art", []):
            print(f"  {line}")
        print("=" * 76)

        tasks = [Task(t["id"], t.get("deps", [])) for t in graph_spec["tasks"]]
        tasks_by_id = {t.id: t for t in tasks}

        for case in graph_spec.get("q1_cases", []):
            targets = case["targets"]
            print(f"\nQ1 targets = {targets}")
            if case.get("notes"):
                print(f"   notes: {case['notes']}")

            for label, fn, expected in [
                ("exclude (brute)", dependencies_of_targets_brute, case["expected_exclude"]),
                ("exclude (opt)  ", dependencies_of_targets,       case["expected_exclude"]),
                ("include        ", dependencies_of_targets_include, case["expected_include"]),
            ]:
                actual = fn(tasks, targets)
                status = _validate_topo(actual, tasks_by_id, expected)
                total += 1
                if status == "PASS":
                    passed += 1
                print(f"   {label}: {actual}  [{status}]")

        for case in graph_spec.get("q2_cases", []):
            target = case["target"]
            actual = ancestors_of_target(tasks, target)
            expected = case["expected_ancestors"]
            # Q2 doesn't require topo order — the problem statement doesn't
            # specify an order among ancestors. We validate set equality only.
            if set(actual) == set(expected):
                status = "PASS"
                passed += 1
            else:
                missing = sorted(set(expected) - set(actual))
                extra = sorted(set(actual) - set(expected))
                status = f"FAIL — missing={missing}, extra={extra}"
            total += 1
            print(f"\nQ2 target = {target!r}")
            if case.get("notes"):
                print(f"   notes: {case['notes']}")
            print(f"   ancestors: {actual}  [{status}]")

    print()
    print("=" * 76)
    print(f"RESULTS: {passed}/{total} passed")
    print("=" * 76)
