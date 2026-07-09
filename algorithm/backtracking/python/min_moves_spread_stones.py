"""
Minimum Moves to Spread Stones Over Grid
https://leetcode.com/problems/minimum-moves-to-spread-stones-over-grid/

Approaches:
1. Backtracking / DFS over grid states -- for each empty cell, try donating a
   stone from every cell with count > 1. Time O((N*N)!) in the worst case,
   Space O(D) where D is the max recursion depth.
"""

from typing import List


def minimumMoves(grid: List[List[int]]) -> int:
    # Base Case: count empty cells
    t = 0
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                t += 1

    if t == 0:
        return 0

    ans = float("inf")
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                for ni in range(3):
                    for nj in range(3):
                        if grid[ni][nj] <= 1:
                            continue
                        d = abs(ni - i) + abs(nj - j)
                        grid[ni][nj] -= 1
                        grid[i][j] += 1
                        ans = min(ans, d + minimumMoves(grid))
                        grid[ni][nj] += 1
                        grid[i][j] -= 1
    return ans
