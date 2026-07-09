"""
Detonate the Maximum Bombs
https://leetcode.com/problems/detonate-the-maximum-bombs/description/

Given a list of bombs (each with x, y, r), detonating one bomb triggers all bombs
within its circular range, which cascade further. Return the maximum number of
bombs that can be detonated starting from a single bomb.

Approaches:
1. DFS from each bomb over an implicit adjacency (recompute distances on the fly).
   Time:  O(n^3) -- n starting bombs, each DFS traverses up to n^2 edges.
   Space: O(n) for the visited set and recursion stack
          (O(n^2) if an explicit adjacency graph were precomputed).
"""

from typing import List, Set


# Cannot use naive approach for x+r, x-r, y+r, y-r because that's a rectangular
# coverage, we want circular.
def distanceSquare(x1: int, x2: int, y1: int, y2: int) -> int:
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)


# Time: O(n^3), we are trying for n bombs and each graph have worst of n^2 edges.
# Space: O(n), but if we build our own graph for saving avg time complexity,
# space would be O(n^2)
def dfs(bombs: List[List[int]],
        idx: int,
        x: int, y: int, r: int,
        detonated: Set[int]) -> None:
    n = len(bombs)
    for i in range(n):
        nx = bombs[i][0]
        ny = bombs[i][1]
        nr = bombs[i][2]
        if r * r < distanceSquare(x, nx, y, ny):
            continue
        if i in detonated:
            continue
        detonated.add(i)

        dfs(bombs, i, nx, ny, nr, detonated)


def maximumDetonation(bombs: List[List[int]]) -> int:
    n = len(bombs)
    res = 0
    for i in range(n):
        detonated: Set[int] = set()
        detonated.add(i)
        dfs(bombs, i, bombs[i][0], bombs[i][1], bombs[i][2], detonated)
        count = len(detonated)
        res = max(res, count)

    return res
