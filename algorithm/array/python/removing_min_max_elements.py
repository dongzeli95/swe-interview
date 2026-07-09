"""
Removing Minimum and Maximum From Array
https://leetcode.com/problems/removing-minimum-and-maximum-from-array/

You are given a 0-indexed array of distinct integers nums.
There is an element with the lowest value (minimum) and an element with the
highest value (maximum). Removing an element means popping from the front or
the back of the array. Return the minimum number of deletions required to
remove both the minimum and the maximum element.

Approaches:
    1. Single pass to locate min/max indices, then pick the best of three
       deletion strategies (front-only, back-only, both ends).
       Time: O(n), Space: O(1)
"""

from typing import List


# Time: O(n), Space: O(1)
def minimumDeletions(nums: List[int]) -> int:
    # finding index of minimum and maximum element
    idx_max = -1
    idx_min = -1
    mini = float('inf')
    maxi = float('-inf')
    n = len(nums)

    for i in range(n):
        if nums[i] < mini:
            mini = nums[i]
            idx_min = i

        if nums[i] > maxi:
            maxi = nums[i]
            idx_max = i

    # Three possibilities of answer
    num1 = max(idx_min + 1, idx_max + 1)                                # from front deletion only
    num2 = max(n - idx_min, n - idx_max)                                # from back deletion only
    num3 = min(idx_min + 1, idx_max + 1) + min(n - idx_min, n - idx_max)  # from front and back deletion both

    # minimum of all three possibilities
    return min(num1, num2, num3)
