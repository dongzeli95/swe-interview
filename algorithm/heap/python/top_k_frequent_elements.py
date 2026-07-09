"""
Top K Frequent Elements
https://leetcode.com/problems/top-k-frequent-elements/

Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.

Approaches:
1. topKFrequent          - Min-heap of size k over frequency map. Time: O(n log k), Space: O(n)
2. topKFrequentQuickSelect - Quickselect on unique values by frequency. Time: O(n) avg, Space: O(n)
"""

import heapq
import random
from collections import defaultdict
from typing import List


# Time: O(n log k), Space: O(n)
def topKFrequent(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    m = defaultdict(int)
    for i in range(n):
        m[nums[i]] += 1

    # Min-heap keyed by frequency; keep size <= k so the smallest freq is on top.
    pq = []  # entries: (freq, num)
    for num, freq in m.items():
        heapq.heappush(pq, (freq, num))
        if len(pq) > k:
            heapq.heappop(pq)

    res = []
    while pq:
        freq, num = heapq.heappop(pq)
        res.append(num)

    return res


def partitionPivot(unique: List[int], left: int, right: int, pivot_idx: int,
                   m: dict) -> int:
    idx = left
    unique[pivot_idx], unique[right] = unique[right], unique[pivot_idx]
    for i in range(left, right):
        if m[unique[i]] > m[unique[right]]:
            unique[idx], unique[i] = unique[i], unique[idx]
            idx += 1
    unique[right], unique[idx] = unique[idx], unique[right]
    return idx


# Time: O(n) avg, Space: O(n)
def topKFrequentQuickSelect(nums: List[int], k: int) -> List[int]:
    if len(nums) < k:
        return nums

    n = len(nums)
    m = {}
    unique = []
    for i in range(n):
        if nums[i] not in m:
            unique.append(nums[i])
            m[nums[i]] = 0
        m[nums[i]] += 1

    u = len(unique)
    left, right = 0, u - 1
    while left <= right:
        pivot_idx = left + random.randint(0, right - left)
        new_pivot = partitionPivot(unique, left, right, pivot_idx, m)
        if new_pivot == k - 1:
            return unique[:k]
        elif new_pivot > k - 1:
            right = new_pivot - 1
        else:
            left = new_pivot + 1

    return []


if __name__ == "__main__":
    nums1 = [1, 1, 1, 2, 2, 3]
    res = topKFrequentQuickSelect(nums1, 2)
    for i in res:
        print(i)
    # nums2 = [1]
