"""
Disconnect Path in a Binary Matrix by At Most One Flip
https://leetcode.com/problems/disconnect-path-in-a-binary-matrix-by-at-most-one-flip/

You can move from (r, c) to (r+1, c) or (r, c+1) only if the destination cell is 1.
Return True if flipping at most one cell (not (0,0) or (m-1,n-1)) can disconnect
(0,0) from (m-1,n-1).

Approaches:
1. isPossibleToCutPath (DFS, greedy path erase): run DFS from (0,0), erase cells
   along the first path found, then DFS again; if the second DFS cannot reach the
   end, the two paths shared a cut vertex. Time O(m+n), Space O(m+n).
2. isPossibleToCutPathDP (DP, path counting): count paths from (0,0) to each cell
   (dp) and from each cell to (m-1,n-1) (dp2). If any intermediate cell (i,j)
   with grid[i][j]==1 satisfies dp[i][j]*dp2[i][j] == total_paths, that cell lies
   on every path and flipping it disconnects the grid. Time O(m*n), Space O(m*n).
"""

from typing import List


def _dfs(grid: List[List[int]], x: int, y: int, state: List[bool]) -> None:
    if state[0]:
        return
    m = len(grid)
    n = len(grid[0])

    if x == m - 1 and y == n - 1:
        state[0] = True
        return
    if x >= m or y >= n or grid[x][y] == 0:
        return

    _dfs(grid, x + 1, y, state)
    if state[0]:
        grid[x][y] = 0
        return

    _dfs(grid, x, y + 1, state)
    if state[0]:
        grid[x][y] = 0
    return


# Time: O(m+n), Space: O(m+n)
def isPossibleToCutPath(grid: List[List[int]]) -> bool:
    state = [False]  # mutable "canReachEnd" flag
    _dfs(grid, 0, 0, state)
    if not state[0]:
        return True

    state[0] = False
    grid[0][0] = 1
    _dfs(grid, 0, 0, state)
    return not state[0]


# Time: O(m*n), Space: O(m*n)
def isPossibleToCutPathDP(grid: List[List[int]]) -> bool:
    m = len(grid)
    n = len(grid[0])

    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            if grid[i][j] == 0:
                continue
            path1 = dp[i - 1][j] if i - 1 >= 0 else 0
            path2 = dp[i][j - 1] if j - 1 >= 0 else 0
            dp[i][j] = path1 + path2

    dp2 = [[0] * n for _ in range(m)]
    dp2[m - 1][n - 1] = 1
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if i == m - 1 and j == n - 1:
                continue
            if grid[i][j] == 0:
                continue
            path1 = dp2[i + 1][j] if i + 1 < m else 0
            path2 = dp2[i][j + 1] if j + 1 < n else 0
            dp2[i][j] = path1 + path2

    target = dp[m - 1][n - 1]
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            if i == m - 1 and j == n - 1:
                continue
            if grid[i][j] == 0:
                continue
            # Any intermediate cell that lies on EVERY path satisfies
            # dp[i][j] * dp2[i][j] == total_paths. Flipping it disconnects
            # the grid.
            if dp[i][j] * dp2[i][j] == target:
                return True

    return False


if __name__ == "__main__":
    grid1 = [[1, 1, 1], [1, 0, 0], [1, 1, 1]]
    # isPossibleToCutPath mutates the grid, so pass copies.
    assert isPossibleToCutPath([row[:] for row in grid1]) is True
    assert isPossibleToCutPathDP([row[:] for row in grid1]) is True

    grid2 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    assert isPossibleToCutPath([row[:] for row in grid2]) is False
    assert isPossibleToCutPathDP([row[:] for row in grid2]) is False

    print("All tests passed.")
