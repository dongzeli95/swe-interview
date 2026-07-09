"""
Longest Increasing Subsequence II
https://leetcode.com/problems/longest-increasing-subsequence-ii/

Given an integer array nums and an integer k, find the longest strictly
increasing subsequence such that the difference between adjacent elements
is at most k.

Approaches:
1. lengthOfLIS    - O(n^2) time, O(n) space DP.
2. lengthOfLISSeg - O(n log m) time, O(m) space using a segment tree over
                    the value range, storing the longest subsequence length
                    ending at each value.
"""

from typing import List


def lengthOfLIS(nums: List[int], k: int) -> int:
    if not nums:
        return 0

    n = len(nums)
    dp = [1] * n
    res = 1
    for i in range(1, n):
        for j in range(i):
            if nums[i] - nums[j] <= k and nums[j] < nums[i]:
                dp[i] = max(dp[i], 1 + dp[j])
        res = max(res, dp[i])

    return res


# Using segmentation tree.
# The idea is to keep track of length of subsequence ending in number i in the segment tree.
# Time: O(nlogm), Space: O(m)
class SegmentTree:
    def __init__(self, n_: int):
        self.n = n_
        import math
        size = int(math.ceil(math.log2(n_)))
        size = (2 * (2 ** size)) - 1
        self.segTree = [0] * size

    def max_value(self) -> int:
        return self.segTree[0]

    def update(self, i: int, val: int) -> None:
        # For the end range, we should use n-1, instead of the size of entire seg tree!!
        self._update_util(0, 0, self.n - 1, i, val)

    # Update the latest longest length for subsequence for ranges.
    def _update_util(self, idx: int, start: int, end: int, pos: int, val: int) -> None:
        if start == end:
            self.segTree[idx] = max(val, self.segTree[idx])
            return

        mid = (start + end) // 2
        if pos <= mid:
            self._update_util(2 * idx + 1, start, mid, pos, val)
        else:
            self._update_util(2 * idx + 2, mid + 1, end, pos, val)
        self.segTree[idx] = max(self.segTree[2 * idx + 1], self.segTree[2 * idx + 2])

    def query(self, l: int, r: int) -> int:
        return self._query_util(0, 0, self.n - 1, l, r)

    def _query_util(self, idx: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or end < l:
            return float('-inf')
        if l <= start and end <= r:
            return self.segTree[idx]

        mid = (start + end) // 2
        return max(
            self._query_util(2 * idx + 1, start, mid, l, r),
            self._query_util(2 * idx + 2, mid + 1, end, l, r),
        )


def lengthOfLISSeg(nums: List[int], k: int) -> int:
    seg = SegmentTree(int(1e5) + 1)
    for i in nums:
        lower = max(0, i - k)
        q = seg.query(lower, i - 1)
        cur = 1 + q
        seg.update(i, cur)

    return seg.max_value()


if __name__ == "__main__":
    nums1 = [4, 2, 1, 4, 3, 4, 5, 8, 15]
    k1 = 3
    assert lengthOfLIS(nums1, k1) == 5
    assert lengthOfLISSeg(nums1, k1) == 5

    nums2 = [7, 4, 5, 1, 8, 12, 4, 7]
    k2 = 5
    assert lengthOfLIS(nums2, k2) == 4
    assert lengthOfLISSeg(nums2, k2) == 4

    nums3 = [1, 5]
    k3 = 1
    assert lengthOfLIS(nums3, k3) == 1
    assert lengthOfLISSeg(nums3, k3) == 1

    print("All tests passed.")
