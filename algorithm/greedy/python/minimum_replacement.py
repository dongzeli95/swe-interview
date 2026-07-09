"""
Minimum Replacements to Sort the Array
https://leetcode.com/problems/minimum-replacements-to-sort-the-array/

You are given a 0-indexed integer array nums. In one operation you can replace
any element of the array with any two elements that sum to it. Return the
minimum number of operations to make the array sorted in non-decreasing order.

Approaches:
1. Greedy from right to left: for each nums[i] > nums[i+1], split it into the
   fewest pieces (ceil(nums[i] / nums[i+1])) such that every piece is <= nums[i+1],
   and set nums[i] to the smallest piece (nums[i] // pieces) to maximize the
   ceiling for the next-left element.
   Time: O(n), Space: O(1)
"""

from typing import List


def minimumReplacement(nums: List[int]) -> int:
    if not nums:
        return 0

    n = len(nums)
    res = 0
    for i in range(n - 2, -1, -1):
        if nums[i] > nums[i + 1]:
            mod = nums[i] % nums[i + 1]
            num_elements = (nums[i] // nums[i + 1]) + (0 if mod == 0 else 1)
            smallest = nums[i] // num_elements
            operations = num_elements - 1
            res += operations
            nums[i] = smallest

    return res
