"""
Find Pivot Index
https://leetcode.com/problems/find-pivot-index

Given an array of integers nums, return the leftmost pivot index where the sum
of elements strictly to the left equals the sum of elements strictly to the
right. Return -1 if no such index exists.

Approaches:
    1. pivotIndex - Prefix sum with total tracking. Time: O(n), Space: O(1).
"""

from typing import List


# Time: O(n), Space: O(1)
def pivotIndex(nums: List[int]) -> int:
    if not nums:
        return -1

    res = -1
    n = len(nums)
    total = sum(nums)
    left_sum = 0

    for i in range(n):
        if total - nums[i] == left_sum * 2:
            res = i
            break
        left_sum += nums[i]

    return res


if __name__ == "__main__":
    nums1 = [1, 7, 3, 6, 5, 6]
    assert pivotIndex(nums1) == 3

    nums2 = [1, 2, 3]
    assert pivotIndex(nums2) == -1

    nums3 = [2, 1, -1]
    assert pivotIndex(nums3) == 0
