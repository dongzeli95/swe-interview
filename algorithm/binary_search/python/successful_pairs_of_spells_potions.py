"""
Successful Pairs of Spells and Potions
https://leetcode.com/problems/successful-pairs-of-spells-and-potions

Approaches:
1. successfulPairs: Sort potions, then binary search per spell for the first
   potion whose product with the spell meets `success`.
   Time: O(m log m + n log m), Space: O(1) extra (in-place sort).
"""

from typing import List
from bisect import bisect_left


# Time: O(n log m), Space: O(1), where n = len(spells), m = len(potions)
def successfulPairs(spells: List[int], potions: List[int], success: int) -> List[int]:
    if not spells or not potions:
        return []

    n = len(spells)
    m = len(potions)

    potions.sort()

    res = [0] * n
    for i in range(n):
        l = 0
        r = m - 1
        idx = -1
        # Find the index of the first element that is greater than or equal to success / spells[i].
        while l <= r:
            mid = l + (r - l) // 2
            # To prevent overflow (mirrors the C++ double comparison).
            if spells[i] < success / potions[mid]:
                l = mid + 1
            else:
                idx = mid
                r = mid - 1

        res[i] = 0 if idx == -1 else m - idx

    return res


if __name__ == "__main__":
    spells = [5, 1, 3]
    potions = [1, 2, 3, 4, 5]
    res = successfulPairs(spells, potions, 7)
    expected = [4, 0, 3]
    for i in range(len(res)):
        assert res[i] == expected[i]

    spells = [3, 1, 2]
    potions = [8, 5, 8]
    res = successfulPairs(spells, potions, 16)
    expected = [2, 0, 2]
    for i in range(len(res)):
        assert res[i] == expected[i]

    spells = [1, 2, 3, 4, 5, 6, 7]
    potions = [1, 2, 3, 4, 5, 6, 7]
    res = successfulPairs(spells, potions, 25)
    expected = [0, 0, 0, 1, 3, 3, 4]
    for i in range(len(res)):
        assert res[i] == expected[i]
