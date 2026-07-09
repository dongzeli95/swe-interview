"""
Maximum Strictly Increasing Cells in a Matrix
LeetCode: https://leetcode.com/problems/maximum-strictly-increasing-cells-in-a-matrix/

Given an m x n matrix, starting from any cell you may move to any other cell in
the same row or column whose value is strictly greater than the current cell.
Return the maximum number of cells you can visit.

Approaches:
  1. Solution: DFS with memoization. For each row and column, keep a list of
     (x, y, value) triples sorted by value. From cell (x, y), use bisect to
     jump to the first strictly-greater candidate in its row / column and
     recurse. Memoize the best length starting at each cell.
     Time: roughly O(m*n*(m+n)) worst case, Space: O(m*n).
"""

from bisect import bisect_right
from typing import Dict, List, Tuple


class Solution:
    def _get_key(self, x: int, y: int) -> str:
        return f"{x}#{y}"

    def dfs(
        self,
        graph: Dict[str, List[Tuple[int, int, int]]],
        mat: List[List[int]],
        x: int,
        y: int,
        cache: Dict[str, int],
        visited: List[List[bool]],
    ) -> int:
        k = self._get_key(x, y)
        if k in cache:
            return cache[k]

        res = 1

        row_k = f"r{x}"
        col_k = f"c{y}"
        cur_v = mat[x][y]

        # Row: find first entry strictly greater than cur_v (upper_bound by value).
        row_entries = graph[row_k]
        row_values = [entry[2] for entry in row_entries]
        i_pos = bisect_right(row_values, cur_v)
        for i in range(i_pos, len(row_entries)):
            temp_x, temp_y, v = row_entries[i]
            if v <= cur_v or visited[temp_x][temp_y]:
                continue
            visited[temp_x][temp_y] = True
            cells = self.dfs(graph, mat, temp_x, temp_y, cache, visited)
            visited[temp_x][temp_y] = False
            res = max(res, 1 + cells)

        # Column: same as above but along the column-sorted list.
        col_entries = graph[col_k]
        col_values = [entry[2] for entry in col_entries]
        i_pos = bisect_right(col_values, cur_v)
        for i in range(i_pos, len(col_entries)):
            temp_x, temp_y, v = col_entries[i]
            if v <= cur_v or visited[temp_x][temp_y]:
                continue
            visited[temp_x][temp_y] = True
            cells = self.dfs(graph, mat, temp_x, temp_y, cache, visited)
            visited[temp_x][temp_y] = False
            res = max(res, 1 + cells)

        cache[k] = res
        return res

    def maxIncreasingCells(self, mat: List[List[int]]) -> int:
        cache: Dict[str, int] = {}
        m, n = len(mat), len(mat[0])
        visited = [[False] * n for _ in range(m)]
        graph: Dict[str, List[Tuple[int, int, int]]] = {}

        for i in range(m):
            row = [(i, j, mat[i][j]) for j in range(n)]
            row.sort(key=lambda t: t[2])
            graph[f"r{i}"] = row

        for j in range(n):
            col = [(i, j, mat[i][j]) for i in range(m)]
            col.sort(key=lambda t: t[2])
            graph[f"c{j}"] = col

        res = 1
        for i in range(m):
            row = graph[f"r{i}"]
            x, y, _ = row[0]
            visited[x][y] = True
            res = max(res, self.dfs(graph, mat, x, y, cache, visited))
            visited[x][y] = False

        for j in range(n):
            col = graph[f"c{j}"]
            x, y, _ = col[0]
            visited[x][y] = True
            res = max(res, self.dfs(graph, mat, x, y, cache, visited))
            visited[x][y] = False

        return res

    def debug(self, row: List[Tuple[int, int, int]]) -> None:
        print("row")
        for x, y, v in row:
            print(f"x: {x} y: {y} v: {v}")
