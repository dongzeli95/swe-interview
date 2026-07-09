"""
Minimum Knight Moves
https://leetcode.com/problems/minimum-knight-moves/

On an infinite chess board with a knight starting at (0, 0), return the minimum
number of steps needed to reach the square (x, y).

Approaches:
    1. minKnightMoves            - Standard BFS from origin.
       Time:  O(max(|x|, |y|)^2)
       Space: O(max(|x|, |y|)^2)

    2. minKnightMovesBidirectional - Bi-directional BFS from both origin and target.
       Time:  O(max(|x|, |y|)^2) but with a much smaller constant factor.
       Space: O(max(|x|, |y|)^2)
"""

from collections import deque


def _hash_position(x: int, y: int) -> str:
    return f"{x}#{y}"


# Time: O(max(x, y) ^ 2), Space: O(max(x, y) ^ 2)
def minKnightMoves(x: int, y: int) -> int:
    neighbors = [(-1, 2), (1, 2),
                 (2, 1), (2, -1),
                 (1, -2), (-1, -2),
                 (-2, -1), (-2, 1)]

    visited = set()
    q = deque()
    # Each entry: (x, y, steps)
    q.append((0, 0, 0))
    visited.add("0#0")

    while q:
        cx, cy, steps = q.popleft()
        # Found our destination
        if cx == x and cy == y:
            return steps

        # Explore next step
        for dx, dy in neighbors:
            temp_x = cx + dx
            temp_y = cy + dy

            h = f"{temp_x}#{temp_y}"
            if h in visited:
                continue
            visited.add(h)

            q.append((temp_x, temp_y, steps + 1))

    return -1


# Bi-directional BFS
def minKnightMovesBidirectional(x: int, y: int) -> int:
    offsets = [
        (1, 2), (2, 1), (2, -1), (1, -2),
        (-1, -2), (-2, -1), (-2, 1), (-1, 2),
    ]

    origin_queue = deque()
    target_queue = deque()
    origin_queue.append((0, 0, 0))
    target_queue.append((x, y, 0))

    origin_distance = {}
    target_distance = {}
    origin_distance[_hash_position(0, 0)] = 0
    target_distance[_hash_position(x, y)] = 0

    while True:
        origin_x, origin_y, origin_steps = origin_queue.popleft()

        origin_xy = _hash_position(origin_x, origin_y)
        if origin_xy in target_distance:
            return origin_steps + target_distance[origin_xy]

        target_x, target_y, target_steps = target_queue.popleft()

        target_xy = _hash_position(target_x, target_y)
        if target_xy in origin_distance:
            return target_steps + origin_distance[target_xy]

        for dx, dy in offsets:
            # expand from the origin
            next_origin_x = origin_x + dx
            next_origin_y = origin_y + dy
            next_origin_xy = _hash_position(next_origin_x, next_origin_y)

            if next_origin_xy not in origin_distance:
                origin_queue.append((next_origin_x, next_origin_y, origin_steps + 1))
                origin_distance[next_origin_xy] = origin_steps + 1

            # expand from the target
            next_target_x = target_x + dx
            next_target_y = target_y + dy
            next_target_xy = _hash_position(next_target_x, next_target_y)

            if next_target_xy not in target_distance:
                target_queue.append((next_target_x, next_target_y, target_steps + 1))
                target_distance[next_target_xy] = target_steps + 1


if __name__ == "__main__":
    assert minKnightMoves(2, 1) == 1
    assert minKnightMovesBidirectional(2, 1) == 1

    assert minKnightMoves(5, 5) == 4
    assert minKnightMovesBidirectional(5, 5) == 4

    print("All tests passed.")
