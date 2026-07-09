"""
Koko Eating Bananas — https://leetcode.com/problems/koko-eating-bananas

Approaches:
1. minEatingSpeed: Binary search on the eating speed k in [1, max(piles)].
   For each candidate speed, compute total hours needed and shrink the
   search window. Time: O(n log m) where m = max(piles), Space: O(1).
"""

from typing import List


def getHours(piles: List[int], speed: int) -> int:
    res = 0
    for p in piles:
        res += p // speed
        if p % speed != 0:
            res += 1
    return res


# Time: O(n log m) where m is the max element in piles, Space: O(1)
def minEatingSpeed(piles: List[int], h: int) -> int:
    if not piles:
        return 0

    minSpeed = 1
    maxSpeed = piles[0]

    for i in range(1, len(piles)):
        maxSpeed = max(maxSpeed, piles[i])

    while minSpeed < maxSpeed:
        mid = minSpeed + (maxSpeed - minSpeed) // 2
        hours = getHours(piles, mid)
        if hours > h:
            minSpeed = mid + 1
        else:
            maxSpeed = mid

    return maxSpeed


if __name__ == "__main__":
    piles = [3, 6, 7, 11]
    h = 8
    res = minEatingSpeed(piles, h)
    assert res == 4, res

    piles = [30, 11, 23, 4, 20]
    h = 5
    res = minEatingSpeed(piles, h)
    assert res == 30, res

    piles = [30, 11, 23, 4, 20]
    h = 6
    res = minEatingSpeed(piles, h)
    assert res == 23, res

    piles = [312884470]
    h = 968709470
    res = minEatingSpeed(piles, h)
    assert res == 1, res
