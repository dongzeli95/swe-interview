"""
Count Fertile Pyramids in a Land
https://leetcode.com/problems/count-fertile-pyramids-in-a-land/

Given a 0-indexed m x n binary matrix grid representing farmland, return the
total number of pyramidal and inverse pyramidal plots that can be found.

Key insight:
A pyramid of height h at (r, c) can be seen as two joint pyramids of height
h - 1 plus two extra fertile cells (the peak and one just below it). If we
treat every fertile cell as a pyramid of height 1, we can compute the height
of a pyramid whose tip is (i, j) as:
    grid[i][j] = min(grid[i-1][j-1], grid[i-1][j+1]) + 1
whenever grid[i][j] and grid[i-1][j] are both fertile. A pyramid of size n
contributes n - 1 valid pyramids. We only need to write the code for the
inverse pyramid case; reversing the rows and running it again counts the
simple pyramids.

Approaches:
  1. Solution.countPyramids - DP in place, O(m*n) time, O(1) extra space
     (mutates grid). Counts inverse pyramids, then reverses rows and counts
     the simple pyramids on the reversed grid.
"""

from typing import List


class Solution:
    # Time: O(m*n), Space: O(m*n) (in-place mutation of the input)
    def count(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        ans = 0
        for i in range(1, n):
            for j in range(1, m - 1):
                if grid[i][j] and grid[i - 1][j]:
                    # if current cell can be a tip of a pyramid, compute height.
                    grid[i][j] = min(grid[i - 1][j - 1], grid[i - 1][j + 1]) + 1
                    ans += grid[i][j] - 1
                    # pyramid of size n contributes n - 1 times to the answer.
        return ans

    def countPyramids(self, grid: List[List[int]]) -> int:
        ans = self.count(grid)  # counts inverse pyramids.
        grid.reverse()
        ans += self.count(grid)  # counts simple pyramids after reversing rows.
        return ans
