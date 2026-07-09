"""
Find the Highest Altitude
https://leetcode.com/problems/find-the-highest-altitude

Approaches:
1. largestAltitude: Running prefix sum, track max. Time: O(n), Space: O(1).
"""

from typing import List


# Time: O(n), Space: O(1)
def largestAltitude(gain: List[int]) -> int:
    res = 0
    cur_sum = 0
    n = len(gain)

    for i in range(n):
        cur_sum += gain[i]
        res = max(res, cur_sum)

    return res


if __name__ == "__main__":
    gain1 = [-5, 1, 5, 0, -7]
    assert largestAltitude(gain1) == 1

    gain2 = [-4, -3, -2, -1, 4, 3, 2]
    assert largestAltitude(gain2) == 0
