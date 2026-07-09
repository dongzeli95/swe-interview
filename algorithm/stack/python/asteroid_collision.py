"""
Asteroid Collision (LeetCode 735)
https://leetcode.com/problems/asteroid-collision

Approaches:
1. asteroidCollision: Stack-based simulation. For each incoming asteroid,
   resolve collisions against the top of the result stack until stable.
   Time: O(n), Space: O(n).
"""

from typing import List


# Time: O(n), Space: O(n)
def asteroidCollision(asteroids: List[int]) -> List[int]:
    if not asteroids:
        return []

    res: List[int] = []
    n = len(asteroids)
    for i in range(n):
        if not res:
            res.append(asteroids[i])
        else:
            need_insert = False
            while res:
                d1 = 1 if res[-1] > 0 else -1
                d2 = 1 if asteroids[i] > 0 else -1
                if d1 == 1 and d2 == -1:
                    if abs(res[-1]) > abs(asteroids[i]):
                        need_insert = False
                        break
                    if abs(res[-1]) == abs(asteroids[i]):
                        res.pop()
                        need_insert = False
                        break

                    if abs(res[-1]) < abs(asteroids[i]):
                        res.pop()
                        need_insert = True
                else:
                    res.append(asteroids[i])
                    need_insert = False
                    break

            if need_insert:
                res.append(asteroids[i])

    return res


if __name__ == "__main__":
    asteroids1 = [5, 10, -5]
    res1 = [5, 10]
    assert asteroidCollision(asteroids1) == res1

    asteroids2 = [8, -8]
    res2 = []
    assert asteroidCollision(asteroids2) == res2

    asteroids3 = [10, 2, -5]
    res3 = [10]
    assert asteroidCollision(asteroids3) == res3
