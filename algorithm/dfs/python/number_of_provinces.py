"""
Number of Provinces
https://leetcode.com/problems/number-of-provinces

Approaches:
1. Build an adjacency-list graph, then DFS from each unvisited node.
   Time: O(N^2) to build the graph (dense) and DFS. Space: O(N^2).
2. DFS directly on the adjacency matrix without building a separate graph.
   Time: O(N^2). Space: O(N).
"""

from collections import defaultdict
from typing import Dict, List, Set


class Solution:
    # Time: O(N^2), we need N^2 time to construct graph, and a dense graph can have N^2 edges.
    # Space: O(N^2)
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        if not isConnected or not isConnected[0]:
            return 0

        graph: Dict[int, List[int]] = defaultdict(list)

        n = len(isConnected)
        for i in range(n):
            for j in range(n):
                if isConnected[i][j] == 1:
                    graph[i].append(j)
                    graph[j].append(i)

        res = 0
        visited: Set[int] = set()
        for i in range(n):
            if i in visited:
                continue
            visited.add(i)
            self._dfs(i, graph, visited)
            res += 1

        return res

    def _dfs(self, curr: int, graph: Dict[int, List[int]], visited: Set[int]) -> None:
        for nxt in graph[curr]:
            if nxt in visited:
                continue
            visited.add(nxt)
            self._dfs(nxt, graph, visited)


class Solution2:
    # Time: O(N^2), Space: O(N)
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        res = 0
        visited: Set[int] = set()

        for i in range(n):
            if i in visited:
                continue
            visited.add(i)
            self._dfs(isConnected, i, visited)
            res += 1

        return res

    def _dfs(self, isConnected: List[List[int]], curr: int, visited: Set[int]) -> None:
        for i in range(len(isConnected[curr])):
            neighbor = i
            if neighbor in visited or isConnected[curr][neighbor] == 0:
                continue
            visited.add(neighbor)
            self._dfs(isConnected, neighbor, visited)


if __name__ == "__main__":
    isConnected1 = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    assert Solution().findCircleNum(isConnected1) == 2
    assert Solution2().findCircleNum(isConnected1) == 2

    isConnected2 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert Solution().findCircleNum(isConnected2) == 3
    assert Solution2().findCircleNum(isConnected2) == 3
