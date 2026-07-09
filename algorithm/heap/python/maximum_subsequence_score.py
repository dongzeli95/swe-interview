"""
Maximum Subsequence Score
https://leetcode.com/problems/maximum-subsequence-score

Approaches:
1. Sort by nums2 desc + min-heap over top-k nums1 values.
   Time: O(n log n), Space: O(n)
"""

import heapq
from typing import List


# Time complexity: O(nlogn), Space complexity: O(n)
def maxScore(nums1: List[int], nums2: List[int], k: int) -> int:
    if not nums1:
        return 0

    n = len(nums1)

    combos = [(nums1[i], nums2[i]) for i in range(n)]

    # sort by nums2 descending
    combos.sort(key=lambda p: -p[1])

    # store k largest nums1 values
    sum_ = 0
    mn = combos[k - 1][1]

    # min heap
    q: List[int] = []
    for i in range(k):
        heapq.heappush(q, combos[i][0])
        sum_ += combos[i][0]

    res = sum_ * mn
    for i in range(k, n):
        mn = combos[i][1]
        sum_ += combos[i][0]
        heapq.heappush(q, combos[i][0])

        val = heapq.heappop(q)
        sum_ -= val

        res = max(res, sum_ * mn)

    return res


if __name__ == "__main__":
    nums1 = [1, 3, 3, 2]
    nums2 = [2, 1, 3, 4]
    k = 3
    assert maxScore(nums1, nums2, k) == 12

    nums1 = [4, 2, 3, 1, 1]
    nums2 = [7, 5, 10, 9, 6]
    k = 1
    assert maxScore(nums1, nums2, k) == 30
