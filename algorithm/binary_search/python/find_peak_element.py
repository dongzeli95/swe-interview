"""
Find Peak Element
https://leetcode.com/problems/find-peak-element

A peak element is strictly greater than its neighbors. Given a 0-indexed integer
array nums, return the index of any peak. nums[-1] = nums[n] = -inf.

Approaches (mirroring the C++ source 1-to-1):
1. findPeakElement: Binary search for a strict peak. Time O(log n), Space O(1).
2. findLowElement:  Binary search for a strict valley. Time O(log n), Space O(1).
"""

from typing import List


# Time: O(log n), Space: O(1)
def findPeakElement(nums: List[int]) -> int:
    if not nums:
        return -1

    if len(nums) == 1:
        return 0

    n = len(nums)
    l = 0
    r = n - 1

    if nums[l] > nums[l + 1]:
        return l

    if nums[r] > nums[r - 1]:
        return r

    while l <= r:
        m = l + (r - l) // 2
        # We find a peak.
        greater_than_left = (m - 1 < 0) or (nums[m] > nums[m - 1])
        greater_than_right = (m + 1 >= n) or (nums[m] > nums[m + 1])
        if greater_than_left and greater_than_right:
            return m
        elif greater_than_left:
            l = m + 1
        else:
            r = m - 1

    return -1


# Time: O(log n), Space: O(1)
def findLowElement(nums: List[int]) -> int:
    if not nums:
        return -1

    if len(nums) == 1:
        return 0

    n = len(nums)
    l = 0
    r = n - 1

    if nums[l] < nums[l + 1]:
        return l

    if nums[r] < nums[r - 1]:
        return r

    while l <= r:
        m = l + (r - l) // 2
        # We find a valley.
        less_than_left = (m - 1 < 0) or (nums[m] < nums[m - 1])
        less_than_right = (m + 1 >= n) or (nums[m] < nums[m + 1])
        if less_than_left and less_than_right:
            return m
        elif less_than_left:
            l = m + 1
        else:
            r = m - 1

    return -1


if __name__ == "__main__":
    nums = [1, 2, 3, 1]
    res = findPeakElement(nums)
    assert res == 2
    low = findLowElement(nums)
    print(f"low: {low}")

    nums = [1, 2, 1, 3, 5, 6, 4]
    res = findPeakElement(nums)
    assert res == 5
    low = findLowElement(nums)
    print(f"low: {low}")

    # [3,4,3,2,1]
    nums = [3, 4, 3, 2, 1]
    res = findPeakElement(nums)
    assert res == 1
    low = findLowElement(nums)
    print(f"low: {low}")

    nums = [5, 4, 3, 4]
    low = findLowElement(nums)
    print(f"low: {low}")
