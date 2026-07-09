"""
Walls and Gates (LeetCode 286)
https://leetcode.com/problems/walls-and-gates/description/

You are given an m x n grid `rooms` with values:
    -1  : wall/obstacle
     0  : gate
    INF : empty room (2**31 - 1)

Fill each empty room with the distance to its nearest gate. If a room cannot
reach any gate, leave it as INF.

Approaches:
    1. DFS from every gate. For each gate cell, run a DFS that walks into
       neighbors only when the neighbor's stored value is strictly greater
       than the new distance we would write. This naturally prunes revisits.
       Time: O(m * n) amortized, Space: O(m * n) recursion in the worst case.
"""

from typing import List


# Time: O(m*n), Space: O(m*n)
def wallsAndGates(rooms: List[List[int]]) -> None:
    for i in range(len(rooms)):
        for j in range(len(rooms[i])):
            if rooms[i][j] == 0:
                dfs(rooms, i, j, 0)


def dfs(rooms: List[List[int]], i: int, j: int, val: int) -> None:
    if (
        i < 0
        or i >= len(rooms)
        or j < 0
        or j >= len(rooms[i])
        or rooms[i][j] < val
    ):
        return
    rooms[i][j] = val
    dfs(rooms, i + 1, j, val + 1)
    dfs(rooms, i - 1, j, val + 1)
    dfs(rooms, i, j + 1, val + 1)
    dfs(rooms, i, j - 1, val + 1)
