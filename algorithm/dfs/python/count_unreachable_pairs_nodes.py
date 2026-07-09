"""
Count Unreachable Pairs of Nodes in an Undirected Graph
https://leetcode.com/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/

Approaches:
    1. DFS to find each connected component's size, then multiply component
       size by remaining nodes to accumulate unreachable pairs.
       Time: O(n + e), Space: O(n + e)
"""

from collections import defaultdict
from typing import Dict, List, Set


def dfs(graph: Dict[int, List[int]], visited: Set[int], curr: int, res: List[int]) -> None:
    res[0] += 1
    for nxt in graph[curr]:
        if nxt in visited:
            continue
        visited.add(nxt)
        dfs(graph, visited, nxt, res)


# Time: O(n+e), Space: O(n+e)
def countPairs(n: int, edges: List[List[int]]) -> int:
    graph: Dict[int, List[int]] = defaultdict(list)
    for node1, node2 in edges:
        graph[node1].append(node2)
        graph[node2].append(node1)

    visited: Set[int] = set()

    numberOfPairs = 0
    remainingNodes = n
    for i in range(n):
        if i in visited:
            continue
        visited.add(i)
        res = [0]
        dfs(graph, visited, i, res)

        numberOfPairs += res[0] * (remainingNodes - res[0])
        remainingNodes -= res[0]

    return numberOfPairs


if __name__ == "__main__":
    n = 3
    edges = [[0, 1], [0, 2], [1, 2]]
    assert countPairs(n, edges) == 0

    n = 7
    edges = [[0, 2], [0, 5], [2, 4], [1, 6], [5, 4]]
    assert countPairs(n, edges) == 14
