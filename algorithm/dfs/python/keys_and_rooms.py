"""Keys and Rooms — https://leetcode.com/problems/keys-and-rooms

Approaches:
    1. DFS with a visited set. N = number of rooms, E = number of keys.
       Time: O(N + E), Space: O(N).
"""

from typing import List, Set


# N is number of rooms, E is number of keys
# Time: O(N+E), Space: O(N)
def dfs(curr: int, rooms: List[List[int]], visited: Set[int]) -> None:
    for nxt in rooms[curr]:
        if nxt in visited:
            continue
        visited.add(nxt)
        dfs(nxt, rooms, visited)


def canVisitAllRooms(rooms: List[List[int]]) -> bool:
    n = len(rooms)
    visited: Set[int] = set()
    visited.add(0)
    dfs(0, rooms, visited)

    return len(visited) == n


if __name__ == "__main__":
    rooms1 = [[1], [2], [3], []]
    assert canVisitAllRooms(rooms1) is True

    rooms2 = [[1, 3], [3, 0, 1], [2], [0]]
    assert canVisitAllRooms(rooms2) is False
