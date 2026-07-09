"""
Kth Largest Element in an Array
https://leetcode.com/problems/kth-largest-element-in-an-array

Given an integer array nums and an integer k, return the kth largest element
in the array. Note that it is the kth largest element in the sorted order,
not the kth distinct element.

Approaches:
    1. findKthLargest - Min-heap of size k. Time: O(N*logK), Space: O(K).
"""

import heapq
from typing import List


def findKthLargest(nums: List[int], k: int) -> int:
    """Min-heap of size k. Time: O(N*logK), Space: O(K)."""
    if len(nums) < k:
        return -1

    min_heap: List[int] = []
    for x in nums:
        heapq.heappush(min_heap, x)
        if len(min_heap) > k:
            heapq.heappop(min_heap)

    return min_heap[0]


if __name__ == "__main__":
    nums1 = [3, 2, 1, 5, 6, 4]
    assert findKthLargest(nums1, 2) == 5

    nums2 = [3, 2, 3, 1, 2, 4, 5, 5, 6]
    assert findKthLargest(nums2, 4) == 4
