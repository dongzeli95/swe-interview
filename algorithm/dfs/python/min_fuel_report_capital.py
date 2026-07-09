"""
Minimum Fuel Cost to Report to the Capital
https://leetcode.com/problems/minimum-fuel-cost-to-report-to-the-capital/

Approaches:
    1. Solution (DFS from capital): Build adjacency list, DFS from node 0, at each
       non-root node accumulate ceil(representatives_in_subtree / seats) fuel.
       Time: O(n), Space: O(n) for adjacency list + recursion stack.
"""

from collections import defaultdict
from math import ceil
from typing import List


class Solution:
    def __init__(self) -> None:
        self.fuel: int = 0

    def dfs(self, node: int, parent: int, adj: List[List[int]], seats: int) -> int:
        # The node itself has one representative.
        representatives = 1
        for child in adj[node]:
            if child != parent:
                # Add count of representatives in each child subtree to the parent subtree.
                representatives += self.dfs(child, node, adj, seats)

        if node != 0:
            # Count the fuel it takes to move to the parent node.
            # Root node does not have any parent so we ignore it.
            self.fuel += ceil(representatives / seats)
        return representatives

    def minimumFuelCost(self, roads: List[List[int]], seats: int) -> int:
        n = len(roads) + 1
        adj: List[List[int]] = [[] for _ in range(n)]
        for road in roads:
            adj[road[0]].append(road[1])
            adj[road[1]].append(road[0])
        self.dfs(0, -1, adj, seats)
        return self.fuel
