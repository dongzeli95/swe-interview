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

    4. "For tasks at the same dependency level — say D and G both depend
        on A, B, C but neither depends on the other — do you care about
        their relative order in the output? Or is any valid topological
        order fine?"
        → Ask this BEFORE coding. Topo sort is not unique; independent
          nodes can appear in ANY order. If the interviewer doesn't care,
          say so out loud and move on. If they want a specific tiebreak
          (usually alphabetical), swap Kahn's queue for a min-heap
          (O((V+E) log V) instead of O(V+E)) — plan for that upfront so
          you don't have to refactor midway through.
        → Also flag: independent leaf nodes {A, B, C} can appear in any
          order among themselves for the same reason.

    5. "Can `targets` contain duplicates? (e.g., ['D', 'F', 'D'])"
        → If yes: the BFS seeding loop needs an `if tgt not in reachable`
          guard to avoid enqueueing the same target twice. Without the
          guard, correctness is unaffected (the inner visited check
          catches everything) but you waste one queue pop per duplicate.
        → If the interviewer says "assume no duplicates," the guard is
          dead code and can be removed.

    6. "Can a dep id reference a task not in `all_tasks`? Empty targets
        list? Duplicate ids in `all_tasks`?"
        → Usually no on all three, but ask — cheap to check, large
          downside if wrong. Empty targets should return []; missing
          deps should probably raise (see the KeyError guard).

───────────────────────────────────────────────────────────────────────────
STEP 2 — SOLUTION PROGRESSION (narrate this out loud)
───────────────────────────────────────────────────────────────────────────
The interviewer scores your reasoning, not just the final code. Walk them
through the progression:

  APPROACH A — recursive post-order DFS from each target  (see: dependencies_of_targets_dfs)
    def dfs(node):
        if node in visited: return
        if node in on_stack: raise CycleError
        on_stack.add(node)
        for dep in by_id[node].dependencies:
            dfs(dep)
        on_stack.remove(node); visited.add(node)
        if node not in target_set:
            result.append(node)   # post-order → topo order for free
    for tgt in targets: dfs(tgt)

    ✓ Reachability + ordering in ONE pass (post-order emission).
    ✓ Visited set shared across all targets — no wasted re-traversal.
    ✓ Naturally scopes to reachable subgraph — no separate BFS pre-pass needed.
    ✗ Python recursion limit (~1000) blows up on deep dep chains.
      Fix: sys.setrecursionlimit(N) or iterative version with ENTER/EXIT
      markers on an explicit stack (2-state trick — see impl note below).
    ✗ Cycle detection needs a separate on_stack set (GRAY nodes in the
      textbook WHITE/GRAY/BLACK 3-color scheme). Easy to forget.
    Complexity: O(V + E).

  APPROACH B — two-pass, multi-source BFS + Kahn's  (see: dependencies_of_targets)
    Pass 1: ONE BFS starting from ALL targets simultaneously, sharing a
            single `reachable` set. Each node enqueued at most once.
    Pass 2: Kahn's topo sort restricted to `reachable`.

    ✓ Iterative — no recursion limit.
    ✓ Cycle detection free (len(order) != len(reachable)).
    ✓ Same shared-visited efficiency as approach A.
    ✗ Two passes vs one — needs the BFS pre-pass to scope down before it
      can compute in-degrees over the reachable subgraph.
    Complexity: O(V + E) total.

⚠ INTERVIEW FRAMING TRAP (from Vanta phone screen 2026-08-04):
    Some interviewers use "topological sort" to mean Kahn's specifically,
    and treat DFS post-order as "a different approach" — even though
    mathematically it IS a topological sort algorithm (Cormen ch. 22).
    If you only present Kahn's and they ask "is there another way?", the
    intended answer is DFS post-order. Pre-empt this by naming BOTH
    algorithms in your opening narration (see template below), then pick
    one to implement.

Narration template (defuses the trap):
    "There are two canonical algorithms for topological sort — Kahn's
     algorithm (BFS + in-degree tracking) and DFS post-order (emit nodes
     as recursion unwinds). For this problem I'd lean toward DFS
     post-order because it does reachability and ordering in a single
     pass — we're topo-sorting from a specific set of targets, not the
     whole graph, so DFS from targets scopes down for free. The trade-off
     is Python's recursion limit on very deep chains. I can code either;
     which would you prefer to see?"

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

───────────────────────────────────────────────────────────────────────────
STEP 4 — WHEN TO REACH FOR KAHN'S vs DFS POST-ORDER (reusable rubric)
───────────────────────────────────────────────────────────────────────────
Both are O(V+E) topological sort algorithms. Pick based on the SHAPE of
the problem, not personal preference — the interviewer will judge the
choice.

  Prefer DFS POST-ORDER when:
    • Topo-sorting from a SPECIFIC starting set (this problem, "build
      order for a specific target"). Reachability + ordering in one pass.
    • You want the shortest code. ~10 lines for the core recursion.
    • Post-order emission naturally maps to the mental model
      "everything I depend on must appear before me."

  Prefer KAHN'S ALGORITHM when:
    • Topo-sorting the WHOLE graph (Course Schedule, package resolution
      over all packages).
    • You want an iterative solution — recursion limit is a real risk.
    • You want ordering by "level" / dependency depth (Kahn's naturally
      layers nodes by when their in-degree hits 0 — useful for parallel
      scheduling: "run these 3 first in parallel, then these 2, ...").
    • You want cycle detection with a trivially simple check
      (len(order) != len(nodes)).

  Cycle detection cheat sheet:
    • Kahn's:  cycle ⇔ some node never gets in-degree 0 ⇔ order shorter
               than reachable set at the end.
    • DFS:     cycle ⇔ during recursion, hit a node that's already on the
               current DFS path (the "gray" set / on_stack). NOT the
               same as `visited` — visited = fully processed (black).

COMPLEXITY
----------
Q1:  O(V + E)   (both approach A and approach B)
Q2:  O(V + E)
═══════════════════════════════════════════════════════════════════════════
"""

from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class Task:
    id: str
    dependencies: list[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════
# Q1 APPROACH B (production): multi-source BFS + Kahn's topo sort
# ═══════════════════════════════════════════════════════════════════════════

def dependencies_of_targets(all_tasks: list[Task], targets: list[str]) -> list[str]:
    """APPROACH B — iterative two-pass version. What to write for production.

    Motivation vs. the naive recursive DFS (approach A in the top docstring):
        Approach A is fine for scratch code but has two issues in real use:
          - Python's recursion limit (~1000) crashes on deep dep chains.
          - Cycle detection in a recursive DFS needs 3-color marking
            (WHITE/GRAY/BLACK), which is easy to get subtly wrong.
        Rewriting iteratively as two passes fixes both — and Kahn's gives
        us cycle detection for free (len(order) != len(reachable)).

    Mental model — SCOPE DOWN then ORDER:
        Pass 1: Multi-source BFS builds `reachable`, the induced subgraph
                of tasks the targets transitively depend on. `reachable`
                doubles as the BFS visited set — shared across all targets,
                so overlapping subgraphs are walked exactly once.
        Pass 2: Kahn's topological sort restricted to `reachable`.
        Pass 3: Drop targets from the final list (per problem framing).

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
    # Kahn's gives us:
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
# Q1 APPROACH A: recursive post-order DFS  (the "other approach" some
# interviewers expect when they say "besides topological sort" — even
# though DFS post-order IS a topological sort algorithm)
# ═══════════════════════════════════════════════════════════════════════════

def dependencies_of_targets_dfs(all_tasks: list[Task], targets: list[str]) -> list[str]:
    """APPROACH A — recursive post-order DFS. Single pass.

    THE CORE IDEA (memorize this — reuse for any "topo sort from a set of
    targets" problem):
        Recurse into a node's deps first. Once they've all returned, they
        are already in `result`. NOW append the current node. Post-order
        emission ⇒ every node appears AFTER all its deps ⇒ valid topo order.

    Cycle detection uses two sets — the standard 3-color scheme:
        WHITE = not in `visited` and not in `on_stack`  → not yet touched
        GRAY  = in `on_stack`                            → on current DFS path
        BLACK = in `visited`                             → fully processed
        A cycle exists iff DFS revisits a GRAY node. Revisiting a BLACK
        node is fine — it just means shared subgraph, already emitted.

    Why the visited/on_stack DISTINCTION matters:
        Two targets sharing a dep D → the second target's DFS hits D, sees
        it's BLACK (visited), returns immediately. Correct — D and its
        subtree are already in `result`. If we treated any prior visit as
        a "cycle", we'd get false positives on shared deps.

    Complexity: O(V + E).

    Trade-off vs Kahn's:
        + One pass (reachability + ordering fused via post-order emission).
        + Shorter code, cleaner mental model.
        − Recursion depth capped by Python's limit (~1000). Deep chains
          need sys.setrecursionlimit(N) or the iterative version below.
    """
    by_id: dict[str, Task] = {t.id: t for t in all_tasks}
    target_set: set[str] = set(targets)

    for tgt in targets:
        if tgt not in by_id:
            raise KeyError(f"target {tgt!r} not found in all_tasks")

    result: list[str] = []
    visited: set[str] = set()   # BLACK — fully processed, already in result
    on_stack: set[str] = set()  # GRAY — on current DFS path (cycle sentinel)

    def dfs(node: str) -> None:
        if node in visited:
            return                                       # shared subgraph — fine
        if node in on_stack:
            raise ValueError(f"cycle detected involving {node!r}")
        on_stack.add(node)
        for dep in by_id[node].dependencies:
            dfs(dep)                                     # deps emitted FIRST
        on_stack.remove(node)
        visited.add(node)
        if node not in target_set:                       # exclude targets
            result.append(node)                          # post-order emit

    for tgt in targets:
        dfs(tgt)
    return result


def dependencies_of_targets_dfs_include(all_tasks: list[Task], targets: list[str]) -> list[str]:
    """APPROACH A, include variant. Same DFS, drop the target filter.

    Only difference vs `dependencies_of_targets_dfs`: no `if node not in
    target_set` guard around the append. Targets end up in the topo order
    at their correct position (after all their deps).
    """
    by_id: dict[str, Task] = {t.id: t for t in all_tasks}

    for tgt in targets:
        if tgt not in by_id:
            raise KeyError(f"target {tgt!r} not found in all_tasks")

    result: list[str] = []
    visited: set[str] = set()
    on_stack: set[str] = set()

    def dfs(node: str) -> None:
        if node in visited:
            return
        if node in on_stack:
            raise ValueError(f"cycle detected involving {node!r}")
        on_stack.add(node)
        for dep in by_id[node].dependencies:
            dfs(dep)
        on_stack.remove(node)
        visited.add(node)
        result.append(node)

    for tgt in targets:
        dfs(tgt)
    return result


# ─── ITERATIVE VARIANT (for the "what if the chain is 10,000 deep?" follow-up) ──
# Same algorithm, explicit stack, 2-state markers to simulate post-order.
# The trick: push (ENTER, node) to start processing, and BEFORE recursing
# into deps push (EXIT, node) so it's processed AFTER all deps drain.
#
# def dependencies_of_targets_dfs_iterative(all_tasks, targets):
#     by_id = {t.id: t for t in all_tasks}
#     target_set = set(targets)
#     result, visited, on_stack = [], set(), set()
#     ENTER, EXIT = 0, 1
#     for tgt in targets:
#         if tgt in visited: continue
#         stack = [(ENTER, tgt)]
#         while stack:
#             state, node = stack.pop()
#             if state == EXIT:
#                 on_stack.discard(node); visited.add(node)
#                 if node not in target_set: result.append(node)
#                 continue
#             if node in visited: continue
#             if node in on_stack: raise ValueError(f"cycle at {node!r}")
#             on_stack.add(node)
#             stack.append((EXIT, node))              # emit AFTER deps
#             for dep in by_id[node].dependencies:
#                 if dep not in visited:
#                     stack.append((ENTER, dep))
#     return result


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


def _manual_smoke_test() -> None:
    """Hand-rolled smoke test — the "original" fixture graph, built inline.

    Easy to reproduce from memory in an interview: F needs D and E, D needs
    A, B, C. Eyeball the printed outputs — deps should appear before their
    dependents in each list.

          A ──┐
          B ──┤─→ D ─→ F
          C ──┘       ↑
                 E ───┘
    """
    tasks = [
        Task("A"),
        Task("B"),
        Task("C"),
        Task("D", ["A", "B", "C"]),
        Task("E"),
        Task("F", ["D", "E"]),
    ]

    print("Q1 Kahn's exclude, F     :", dependencies_of_targets(tasks, ["F"]))
    print("Q1 Kahn's include, F     :", dependencies_of_targets_include(tasks, ["F"]))
    print("Q1 DFS   exclude, F      :", dependencies_of_targets_dfs(tasks, ["F"]))
    print("Q1 DFS   include, F      :", dependencies_of_targets_dfs_include(tasks, ["F"]))
    print("Q2 ancestors of 'A'      :", ancestors_of_target(tasks, "A"))
    print("Q2 ancestors of 'F'      :", ancestors_of_target(tasks, "F"))

    # Cycle detection — A→B→A should raise from BOTH approaches.
    cyclic = [Task("A", ["B"]), Task("B", ["A"]), Task("C", ["A"])]
    for label, fn in [("Kahn's", dependencies_of_targets),
                      ("DFS   ", dependencies_of_targets_dfs)]:
        try:
            fn(cyclic, ["C"])
            print(f"cycle test {label}         : FAIL (no exception)")
        except ValueError as e:
            print(f"cycle test {label}         : raised ValueError({e})")


if __name__ == "__main__":
    _manual_smoke_test()
    print()

    # Fixture-driven demo. Cases live in test_fixtures.json alongside this
    # file. The runner loads the fixture, executes each case against both
    # Q1 variants (exclude, include) and Q2, and validates results by
    # (a) set equality vs expected, (b) topological validity.
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
                ("Kahn exclude", dependencies_of_targets,             case["expected_exclude"]),
                ("Kahn include", dependencies_of_targets_include,     case["expected_include"]),
                ("DFS  exclude", dependencies_of_targets_dfs,         case["expected_exclude"]),
                ("DFS  include", dependencies_of_targets_dfs_include, case["expected_include"]),
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
