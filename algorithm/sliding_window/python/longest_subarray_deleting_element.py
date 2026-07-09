"""
Longest Subarray of 1's After Deleting One Element
https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element

Given a binary array nums, you must delete one element from it.
Return the size of the longest non-empty subarray containing only 1's in the
resulting array. Return 0 if there is no such subarray.

Approaches:
    1. Sliding window with a single "deleted" flag - O(N) time, O(1) space.
"""

from typing import List


# Time complexity: O(N), Space complexity: O(1)
def longestSubarray(nums: List[int]) -> int:
    if not nums:
        return 0

    res = 0
    l, r = 0, 0
    n = len(nums)
    deleted = False

    while r < n:
        if nums[r] == 1:
            r += 1
        else:
            if deleted:
                if nums[l] == 0:
                    deleted = False
                l += 1
            else:
                deleted = True
                r += 1

        res = max(res, r - l - 1)  # -1 is for the deleted element

    return res


if __name__ == "__main__":
    nums1 = [1, 1, 0, 1]
    assert longestSubarray(nums1) == 3

    nums2 = [0, 1, 1, 1, 0, 1, 1, 0, 1]
    assert longestSubarray(nums2) == 5

    nums3 = [1, 1, 1]
    assert longestSubarray(nums3) == 2
