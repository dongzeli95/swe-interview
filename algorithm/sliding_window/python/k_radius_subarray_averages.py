"""
K Radius Subarray Averages
https://leetcode.com/problems/k-radius-subarray-averages/description/

Given a 0-indexed array `nums` of length n and an integer k, build an array
`avgs` of length n where avgs[i] is the integer-division average of the
subarray centered at i with radius k (indices i-k .. i+k inclusive). When
there are fewer than k elements on either side of i, avgs[i] = -1.

Approaches:
    1. Sliding window with running sum -- O(n) time, O(n) space.
"""

from typing import List


# Time: O(n), Space: O(n)
def getAverages(nums: List[int], k: int) -> List[int]:
    if not nums:
        return []

    total = 0
    n = len(nums)
    res = [-1] * n
    for i in range(n):
        total += nums[i]
        if i >= 2 * k:
            res[i - k] = total // (2 * k + 1)
            total -= nums[i - 2 * k]

    return res
