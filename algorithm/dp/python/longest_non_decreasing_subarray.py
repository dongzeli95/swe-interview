"""
Longest Non-Decreasing Subarray From Two Arrays
https://leetcode.com/problems/longest-non-decreasing-subarray-from-two-arrays

Given two 0-indexed integer arrays nums1 and nums2 of length n, construct nums3
of length n by picking nums1[i] or nums2[i] at each index. Return the length of
the longest non-decreasing subarray achievable in nums3.

Approaches:
    1. maxNonDecreasingLen: 2D DP where dp[i][j] is the length of the longest
       non-decreasing subarray ending at index i using nums(j+1)[i].
       Time: O(n), Space: O(n).
"""

from typing import List


# Time: O(n), Space: O(n)
def maxNonDecreasingLen(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)
    if n == 0:
        return 0

    res = 1
    dp = [[1, 1] for _ in range(n)]
    for i in range(1, n):
        for j in range(2):
            val = nums1[i] if j == 0 else nums2[i]
            if val >= nums1[i - 1]:
                dp[i][j] = max(dp[i][j], 1 + dp[i - 1][0])
            if val >= nums2[i - 1]:
                dp[i][j] = max(dp[i][j], 1 + dp[i - 1][1])

            res = max(res, dp[i][j])

    return res


if __name__ == "__main__":
    nums1 = [2, 3, 1]
    nums2 = [1, 2, 1]
    assert maxNonDecreasingLen(nums1, nums2) == 2

    nums1 = [1, 3, 2, 1]
    nums2 = [2, 2, 3, 4]
    assert maxNonDecreasingLen(nums1, nums2) == 4

    nums1 = [1, 1]
    nums2 = [2, 2]
    assert maxNonDecreasingLen(nums1, nums2) == 2

    nums1 = [1]
    nums2 = [2]
    assert maxNonDecreasingLen(nums1, nums2) == 1
