"""
Equal Row and Column Pairs
https://leetcode.com/problems/equal-row-and-column-pairs

Given a 0-indexed n x n integer matrix grid, return the number of pairs
(ri, cj) such that row ri and column cj are equal.

Approaches:
1. equalPairs - Hash map keyed by row/column labels storing serialized
   sequences, then pairwise compare. Time: O(n^2), Space: O(n^2).
"""

from typing import List


# Time: O(n^2), Space: O(n^2)
def equalPairs(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0

    n = len(grid)

    res = 0

    m: dict = {}
    for i in range(n):
        rk = "row" + str(i)
        ck = "col" + str(i)
        for j in range(n):
            if rk not in m:
                m[rk] = str(grid[i][j])
            else:
                m[rk] += chr(grid[i][j] + ord('0'))

            if ck not in m:
                m[ck] = str(grid[j][i])
            else:
                m[ck] += chr(grid[j][i] + ord('0'))

    for i in range(n):
        for j in range(n):
            rk = "row" + str(i)
            ck = "col" + str(j)
            if m[rk] == m[ck]:
                res += 1

    return res


if __name__ == "__main__":
    grid1 = [[3, 2, 1], [1, 7, 6], [2, 7, 7]]
    assert equalPairs(grid1) == 1

    grid2 = [[3, 1, 2, 2], [1, 4, 4, 5], [2, 4, 2, 2], [2, 4, 2, 2]]
    assert equalPairs(grid2) == 3
