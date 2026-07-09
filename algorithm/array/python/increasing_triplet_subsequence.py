"""Increasing Triplet Subsequence.

https://leetcode.com/problems/increasing-triplet-subsequence

Given an integer array nums, return True if there exists a triple of indices
(i, j, k) such that i < j < k and nums[i] < nums[j] < nums[k]. If no such
indices exist, return False.

Approaches:
    1. Two-variable tracking (num1, num2): single pass maintaining the smallest
       seen value (num1) and the smallest value greater than num1 (num2).
       If we ever see a value greater than num2, a triplet exists.
       Time: O(n), Space: O(1)
"""

from typing import List


# Time: O(n), Space: O(1)
def increasingTriplet(nums: List[int]) -> bool:
    if not nums:
        return False

    n = len(nums)
    num1 = nums[0]
    num2 = float("inf")

    for i in range(1, n):
        # Need <= here to handle cases like [1, 1, 1, 1, 1].
        # We only place the number at the next position if it is strictly
        # larger than the current number. If less or equal, we just update
        # the number at the current position.
        if nums[i] <= num1:
            num1 = nums[i]
        elif nums[i] <= num2:
            num2 = nums[i]
        else:
            return True

    return False


if __name__ == "__main__":
    nums = [2, 1, 5, 0, 4, 6]
    assert increasingTriplet(nums) is True

    nums = [1, 1, 1, 1, 1]
    assert increasingTriplet(nums) is False

    nums = [2, 1, 5, 0, 6]
    assert increasingTriplet(nums) is True

    nums = [2, 1, 5, 0, 1, 2]
    assert increasingTriplet(nums) is True

    nums = [5, 4, 3, 2, 1]
    assert increasingTriplet(nums) is False

    nums = [1, 2, 3, 4, 5]
    assert increasingTriplet(nums) is True
