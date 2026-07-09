"""
LeetCode 399: Evaluate Division

Given equations A / B = value, answer queries C / D = ?. Return -1.0 when
unreachable or when a variable is undefined.

Approaches:
    1. DFS with memoization on a weighted graph.
       Build a bidirectional graph where edge (A -> B) carries weight A/B and
       edge (B -> A) carries weight 1/(A/B). For each query, DFS from the
       source until we reach the destination, multiplying edge weights along
       the way. A per-query cache stores intermediate results.
       Time:  O(M * N) where M = number of queries, N = number of equations.
       Space: O(N) for the graph, cache, and visited set.
"""

from collections import defaultdict
from typing import Dict, List, Set, Tuple


def dfs(
    curr: str,
    dest: str,
    graph: Dict[str, List[Tuple[str, float]]],
    cache: Dict[str, float],
    visited: Set[str],
) -> float:
    if curr in cache:
        return cache[curr]

    if curr not in graph:
        return -1.0

    if curr == dest:
        return 1.0

    res = -1.0
    # Iterate neighbors of curr; skip already-visited nodes.
    neighbors = graph[curr]
    for nxt, val in neighbors:
        if nxt in visited:
            continue

        visited.add(nxt)

        sub_val = dfs(nxt, dest, graph, cache, visited)
        if sub_val != -1:
            res = val * sub_val
            break

    cache[curr] = res
    return res


def calcEquation(
    equations: List[List[str]],
    values: List[float],
    queries: List[List[str]],
) -> List[float]:
    res: List[float] = []
    graph: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
    n = len(equations)

    for i in range(n):
        s1 = equations[i][0]
        s2 = equations[i][1]
        graph[s1].append((s2, values[i]))
        graph[s2].append((s1, 1.0 / values[i]))

    for i in range(len(queries)):
        s1 = queries[i][0]
        s2 = queries[i][1]
        cache: Dict[str, float] = {}
        visited: Set[str] = set()
        visited.add(s1)
        res.append(dfs(s1, s2, graph, cache, visited))

    return res


if __name__ == "__main__":
    equations1 = [["a", "b"], ["b", "c"]]
    values1 = [2.0, 3.0]
    queries1 = [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]
    expected1 = [6.00000, 0.50000, -1.00000, 1.00000, -1.00000]
    assert calcEquation(equations1, values1, queries1) == expected1

    equations2 = [["a", "b"], ["b", "c"], ["bc", "cd"]]
    values2 = [1.5, 2.5, 5.0]
    queries2 = [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]]
    expected2 = [3.75000, 0.40000, 5.00000, 0.20000]
    assert calcEquation(equations2, values2, queries2) == expected2

    equations3 = [["a", "b"]]
    values3 = [0.5]
    queries3 = [["a", "b"], ["b", "a"], ["a", "c"], ["x", "y"]]
    expected3 = [0.50000, 2.00000, -1.00000, -1.00000]
    assert calcEquation(equations3, values3, queries3) == expected3

    equations4 = [["x1", "x2"]]
    values4 = [3.0]
    queries4 = [["x9", "x2"], ["x9", "x9"]]
    expected4 = [-1.0, -1.0]
    assert calcEquation(equations4, values4, queries4) == expected4

    print("All tests passed.")
