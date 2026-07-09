"""
Max Consecutive Ones III
https://leetcode.com/problems/max-consecutive-ones-iii

Given a binary array nums and an integer k, return the maximum number of
consecutive 1's in the array if you can flip at most k 0's.

Approaches:
    1. Sliding window (two pointers) -- Time O(n), Space O(1).
"""

from typing import List


# Time complexity: O(n), Space complexity: O(1)
def longestOnes(nums: List[int], k: int) -> int:
    if not nums:
        return 0

    n = len(nums)
    l, r = 0, 0
    cnt = 0
    res = 0

    while r < n:
        if nums[r] == 1:
            cnt += 1
            r += 1
        else:
            if k > 0:
                cnt += 1
                k -= 1
                r += 1
            else:
                if nums[l] == 0:
                    k += 1
                cnt -= 1
                l += 1

        res = max(res, cnt)

    return res


if __name__ == "__main__":
    nums1 = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
    assert longestOnes(nums1, 2) == 6

    nums2 = [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1]
    assert longestOnes(nums2, 3) == 10
