"""
Find Number of Coins to Place in Tree Nodes
https://leetcode.com/problems/find-number-of-coins-to-place-in-tree-nodes/

Approaches:
1. Solution.placedCoins: DFS post-order that, for every subtree, tracks the
   top-3 positive costs and the bottom-2 negative costs (a fixed-size summary).
   Time O(n), space O(n) for the graph plus O(h) recursion.
"""

from collections import defaultdict
from typing import Dict, List, Set, Tuple


class Solution:
    # Subtree summary tuple: (pos1, pos2, pos3, neg1, neg2, size)
    # pos1 >= pos2 >= pos3 are the top three non-negative costs.
    # neg1 <= neg2 are the two smallest (most negative) costs.

    def updateMax(
        self,
        pos1: int,
        pos2: int,
        pos3: int,
        neg1: int,
        neg2: int,
        cost: int,
    ) -> Tuple[int, int, int, int, int]:
        if cost > 0:
            if cost >= pos1:
                pos3 = pos2
                pos2 = pos1
                pos1 = cost
            elif cost >= pos2:
                pos3 = pos2
                pos2 = cost
            elif cost >= pos3:
                pos3 = cost
        else:
            if cost <= neg1:
                neg2 = neg1
                neg1 = cost
            elif cost <= neg2:
                neg2 = cost
        return pos1, pos2, pos3, neg1, neg2

    def dfs(
        self,
        graph: Dict[int, List[int]],
        curr: int,
        res: List[int],
        cost: List[int],
        visited: Set[int],
    ) -> Tuple[int, int, int, int, int, int]:
        # Leaf: single neighbor and it is already visited (the parent).
        if len(graph[curr]) == 1 and graph[curr][0] in visited:
            res[curr] = 1
            pos = max(cost[curr], 0)
            neg = min(cost[curr], 0)
            return (pos, 0, 0, neg, 0, 1)

        s = 0
        pos1 = pos2 = pos3 = 0
        neg1 = neg2 = 0
        for neighbor in graph[curr]:
            if neighbor in visited:
                continue
            visited.add(neighbor)
            sub_pos1, sub_pos2, sub_pos3, sub_neg1, sub_neg2, sub_size = self.dfs(
                graph, neighbor, res, cost, visited
            )
            s += sub_size
            pos1, pos2, pos3, neg1, neg2 = self.updateMax(
                pos1, pos2, pos3, neg1, neg2, sub_pos1
            )
            pos1, pos2, pos3, neg1, neg2 = self.updateMax(
                pos1, pos2, pos3, neg1, neg2, sub_pos2
            )
            pos1, pos2, pos3, neg1, neg2 = self.updateMax(
                pos1, pos2, pos3, neg1, neg2, sub_pos3
            )
            pos1, pos2, pos3, neg1, neg2 = self.updateMax(
                pos1, pos2, pos3, neg1, neg2, sub_neg1
            )
            pos1, pos2, pos3, neg1, neg2 = self.updateMax(
                pos1, pos2, pos3, neg1, neg2, sub_neg2
            )

        pos1, pos2, pos3, neg1, neg2 = self.updateMax(
            pos1, pos2, pos3, neg1, neg2, cost[curr]
        )

        if s + 1 < 3:
            res[curr] = 1
        else:
            new_cost = pos1 * pos2 * pos3 if (pos1 != 0 and pos2 != 0 and pos3 != 0) else 0
            new_cost2 = pos1 * neg1 * neg2 if (neg1 != 0 and neg2 != 0 and pos1 != 0) else 0
            final_cost = new_cost if new_cost > new_cost2 else new_cost2
            if final_cost < 0:
                res[curr] = 0
            else:
                res[curr] = final_cost

        return (pos1, pos2, pos3, neg1, neg2, s + 1)

    def placedCoins(self, edges: List[List[int]], cost: List[int]) -> List[int]:
        # constructing the graph.
        graph: Dict[int, List[int]] = defaultdict(list)
        n = len(edges)
        for i in range(n):
            s = edges[i][0]
            e = edges[i][1]
            graph[s].append(e)
            graph[e].append(s)

        coins: List[int] = [-1] * len(cost)
        visited: Set[int] = set()
        visited.add(0)
        self.dfs(graph, 0, coins, cost, visited)
        return coins
