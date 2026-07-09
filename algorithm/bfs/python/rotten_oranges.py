"""
Rotting Oranges - https://leetcode.com/problems/rotting-oranges

You are given an m x n grid where each cell can have one of three values:
    0 - empty cell
    1 - fresh orange
    2 - rotten orange

Every minute, any fresh orange that is 4-directionally adjacent to a rotten
orange becomes rotten. Return the minimum number of minutes that must elapse
until no cell has a fresh orange, or -1 if impossible.

Approaches:
  1. Multi-source BFS: seed queue with all rotten oranges, expand level-by-level.
     Time: O(m*n), Space: O(m*n)
"""

from collections import deque
from typing import List


# Time: O(m*n), Space: O(m*n)
def orangesRotting(grid: List[List[int]]) -> int:
    if not grid:
        return 0

    m = len(grid)
    n = len(grid[0])

    neighbors = [-1, 0, 1, 0, -1]

    q = deque()
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2:
                q.append((i, j))

    res = 0
    while q:
        s = len(q)
        for _ in range(s):
            x, y = q.popleft()

            for j in range(4):
                nx = x + neighbors[j]
                ny = y + neighbors[j + 1]
                if nx < 0 or ny < 0 or nx >= m or ny >= n or grid[nx][ny] == 0 or grid[nx][ny] == 2:
                    continue

                grid[nx][ny] = 2
                q.append((nx, ny))

        if q:
            res += 1

    for row in grid:
        for cell in row:
            if cell == 1:
                return -1

    return res


if __name__ == "__main__":
    grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    assert orangesRotting(grid) == 4

    grid = [[2, 1, 1], [0, 1, 1], [1, 0, 1]]
    assert orangesRotting(grid) == -1

    grid = [[0, 2]]
    assert orangesRotting(grid) == 0
