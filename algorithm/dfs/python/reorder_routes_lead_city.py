"""
Reorder Routes to Make All Paths Lead to the City Zero
https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero

Approaches:
1. DFS from city 0 on an undirected graph where each edge carries a weight
   (1 if it points away from 0 in the original direction, 0 otherwise).
   Sum the weights of edges traversed from 0. Time O(N), Space O(N).
"""

from collections import defaultdict
from typing import Dict, List, Tuple


def dfs(i: int, graph: Dict[int, List[Tuple[int, int]]], visited: List[bool]) -> int:
    if visited[i]:
        return 0

    visited[i] = True
    count = 0
    for neighbor, weight in graph[i]:
        if not visited[neighbor]:
            count += weight
            count += dfs(neighbor, graph, visited)

    return count


def minReorder(n: int, connections: List[List[int]]) -> int:
    if n == 0 or not connections:
        return 0

    graph: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    visited = [False] * n

    for i in range(n - 1):
        graph[connections[i][0]].append((connections[i][1], 1))
        graph[connections[i][1]].append((connections[i][0], 0))

    return dfs(0, graph, visited)


if __name__ == "__main__":
    connections1 = [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]
    assert minReorder(6, connections1) == 3

    connections2 = [[1, 0], [1, 2], [3, 2], [3, 4]]
    assert minReorder(5, connections2) == 2

    connections3 = [[1, 0], [2, 0]]
    assert minReorder(3, connections3) == 0

    print("All tests passed.")
