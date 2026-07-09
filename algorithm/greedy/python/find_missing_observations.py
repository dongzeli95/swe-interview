"""
Find Missing Observations
https://leetcode.com/problems/find-missing-observations/

Approaches:
    1. missingRolls: Compute the required missing sum, distribute it evenly
       across n dice, and add 1 to the first `rem` entries.
       Time: O(n), Space: O(n)
"""

from typing import List


# Time: O(n), Space: O(n)
def missingRolls(rolls: List[int], mean: int, n: int) -> List[int]:
    cur_sum = sum(rolls)
    m = len(rolls)
    missing_sum = mean * (n + m) - cur_sum
    if missing_sum < n or missing_sum > 6 * n:
        return []

    part, rem = divmod(missing_sum, n)
    ans = [part] * n
    for i in range(rem):
        ans[i] += 1
    return ans
