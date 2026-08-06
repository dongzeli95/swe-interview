# Minimum Height Tree — LC 310

**Pattern:** Topological-source-style BFS on undirected tree (leaf-peeling / onion-peeling)
**Trigger:** "undirected tree, find root(s) that minimize height" → peel leaves inward toward the center(s)

Link: https://leetcode.com/problems/minimum-height-trees/

## Problem
Given an undirected tree of `n` nodes labeled `0..n-1` and `n-1` edges, return all node labels that, when chosen as root, produce a tree of minimum height.

**Ex 1:** `n=4, edges=[[1,0],[1,2],[1,3]]` → `[1]`
**Ex 2:** `n=6, edges=[[3,0],[3,1],[3,2],[3,4],[5,4]]` → `[3, 4]`

## Intuition

The MHT roots are the tree's **center(s)** — the node(s) minimizing max distance to any leaf. A tree has **at most 2 centers**, both sitting in the middle of the diameter (longest path).

### Why peel from the leaves inward?

Rooting at a leaf gives the worst-case height (path across the whole diameter). Walking inward one step drops height on that side by 1 and grows the other side by at most 1 — you win until you hit the middle. That "middle" is what BFS-from-leaves finds.

### The algorithm shape (not strictly Kahn's, but same skeleton)

| Kahn's on a DAG | MHT leaf-peeling |
|---|---|
| Sources = `indegree == 0` | "Sources" = `degree == 1` (leaves) |
| Remove source, decrement neighbors | Remove leaf, decrement neighbor's degree |
| New sources emerge | New leaves emerge |
| Stop when queue empty | Stop when `remaining ≤ 2` |

### The key mechanical invariant

**A node is added to `leaves` the moment its degree hits `1`.**

- Every node starts with `degree ≥ 1` (n ≥ 2, connected tree).
- Degree is **monotonically decreasing** during the algorithm.
- The `if degree[nb] == 1` guard therefore fires **exactly once per node** — the moment it transitions to a leaf.
- This is why no separate `visited` set is needed: the degree counter *is* the visited marker.

### Why level-by-level matters

The `size = len(queue)` snapshot enforces synchronous peeling — every side of the tree erodes at the same rate.

If you peeled one leaf at a time, one side of the diameter could strip completely before touching the other, drifting the "surviving" node away from the true center. Think of it as water rising from all leaves at once: the last dry land is the center only if the flood is symmetric.

### Why survivors end up in the queue

The `size` snapshot also protects survivors. A node added during round `K` is *not* popped in round `K` (size was already captured). It's popped only if we enter round `K+1`. Since we stop entering rounds once `remaining ≤ 2`, the nodes added during the **final completed round** stay in the queue — those are exactly the centers.

### Stop condition: why `> 2`?

- Even-length diameter → single center → 1 node remains.
- Odd-length diameter → two adjacent centers → 2 nodes remain.
- Three-or-more centers is impossible: a tree with ≥3 nodes always has a peelable leaf.

## Solution

```python
from collections import deque

def minHeightTree(n, edges):
    if n == 1:
        return [0]

    graph: list[list[int]] = [[] for i in range(0, n)]
    # construct the graph
    for pair in edges:
        x = pair[0]
        y = pair[1]
        graph[x].append(y)
        graph[y].append(x)

    branches: list[int] = [len(i) for i in graph]
    queue: deque[int] = deque({i for i in range(len(branches)) if branches[i] == 1})
    remaining: int = n
    while remaining > 2:
        s = len(queue)
        remaining -= s
        for i in range(0, s):
            curr = queue.popleft()
            for j in graph[curr]:
                branches[j] -= 1
                if branches[j] == 1:
                    queue.append(j)

    return list(queue)


def main():
    n = 4
    edges = [(1, 0), (1, 2), (1, 3)]
    res = minHeightTree(n, edges)
    print(res)

    n = 6
    edges = [(3, 0), (3, 1), (3, 2), (3, 4), (5, 4)]
    res = minHeightTree(n, edges)
    print(res)


if __name__ == "__main__":
    main()
```

## Complexity

**Time: O(n)**
| Step | Cost | Reason |
|---|---|---|
| Build adjacency list | O(n) | `n - 1` edges in a tree, each appended twice |
| Initialize `branches` | O(n) | one `len()` per node |
| Initial leaf scan | O(n) | one pass over `branches` |
| BFS peel loop | O(n) | each node enqueued + popped once; each edge's degree decremented exactly twice (once per endpoint) across the whole run |

Overall dominated by the BFS: **O(n)**. Note this is O(n), *not* O(n + E), because in a tree E = n - 1.

**Space: O(n)**
| Structure | Size |
|---|---|
| `graph` adjacency list | 2·(n − 1) entries → O(n) |
| `branches` degree array | O(n) |
| `queue` | O(n) worst case (e.g. star graph — all leaves enqueued at once) |
| Output list | O(n) worst case (at most 2 centers, so really O(1), but caller-owned) |

Overall: **O(n)** auxiliary space.

**Why not O(n²)?** A naïve "try every node as root, compute height via BFS" approach costs O(n) per root × n roots = O(n²). Leaf-peeling collapses this to a single sweep because the center is found *structurally* instead of by exhaustive search.

## Design choices worth defending in interview
- **List over dict for `graph` / `branches`:** nodes are dense `0..n-1`, so array indexing beats hash lookup (faster, cache-friendlier, no `defaultdict` needed).
- **No `visited` set:** the degree array doubles as the visited marker via the `== 1` guard (only works because it's a tree — cycles would break this).
- **`remaining` counter over `visited` set:** O(1) update per round vs. O(n) set membership checks.
- **`size = len(queue)` snapshot:** level-synchronized peel is required for correctness, not just style.

## Sibling problems (same shape)
- LC 802 Find Eventually Safe Nodes (peel from terminals inward on a directed graph)
- LC 207 / 210 Course Schedule (Kahn's on a DAG — same skeleton, indegree instead of degree)
- LC 269 Alien Dictionary (build DAG, then Kahn's)
