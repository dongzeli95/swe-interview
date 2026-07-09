"""
Nearest Exit from Entrance in Maze
https://leetcode.com/problems/nearest-exit-from-entrance-in-maze

Approaches:
  1. BFS from the entrance, marking visited cells as walls in-place.
     Time: O(m*n), Space: O(m*n)
"""

from collections import deque
from typing import List


def is_border(pos, m: int, n: int) -> bool:
    r, c = pos
    return r == 0 or r == m - 1 or c == 0 or c == n - 1


# Time: O(m*n), Space: O(m*n)
def nearestExit(maze: List[List[str]], entrance: List[int]) -> int:
    if not maze or not maze[0]:
        return -1

    m = len(maze)
    n = len(maze[0])

    neighbors = [-1, 0, 1, 0, -1]
    q = deque()
    q.append((entrance[0], entrance[1]))
    # Don't forget to mark the entrance as visited
    maze[entrance[0]][entrance[1]] = '+'

    res = 0
    while q:
        s = len(q)

        for _ in range(s):
            curr = q.popleft()

            if res > 0 and is_border(curr, m, n):
                return res

            x, y = curr
            for i in range(4):
                nx = x + neighbors[i]
                ny = y + neighbors[i + 1]
                if nx < 0 or ny < 0 or nx >= m or ny >= n or maze[nx][ny] == '+':
                    continue

                maze[nx][ny] = '+'
                q.append((nx, ny))
        res += 1

    return -1


if __name__ == "__main__":
    maze1 = [['+', '+', '.', '+'],
             ['.', '.', '.', '+'],
             ['+', '+', '+', '.']]
    entrance = [1, 2]
    res = nearestExit(maze1, entrance)
    assert res == 1, res

    maze2 = [['+', '+', '+'],
             ['.', '.', '.'],
             ['+', '+', '+']]
    entrance = [1, 0]
    res = nearestExit(maze2, entrance)
    assert res == 2, res

    maze3 = [['.', '+']]
    entrance = [0, 0]
    res = nearestExit(maze3, entrance)
    assert res == -1, res

    maze4 = [['+', '.', '+', '+', '+', '+', '+'],
             ['+', '.', '+', '.', '.', '.', '+'],
             ['+', '.', '+', '.', '+', '.', '+'],
             ['+', '.', '.', '.', '+', '.', '+'],
             ['+', '+', '+', '+', '+', '.', '+']]
    entrance = [0, 1]
    res = nearestExit(maze4, entrance)
    assert res == 12, res

    print("All tests passed.")
