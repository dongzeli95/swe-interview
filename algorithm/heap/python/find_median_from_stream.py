"""
Find Median from Data Stream
https://leetcode.com/problems/find-median-from-data-stream/

Approaches:
1. Two heaps (max-heap `lo` for lower half, min-heap `hi` for upper half).
   addNum: O(log n), findMedian: O(1), space: O(n).
"""

import heapq


class MedianFinder:
    def __init__(self) -> None:
        # `lo` is a max-heap of the lower half (negated values because
        # Python's heapq is a min-heap).
        self.lo: list[int] = []
        # `hi` is a min-heap of the upper half.
        self.hi: list[int] = []

    # Adds a number into the data structure.
    def addNum(self, num: int) -> None:
        # Add to max heap.
        heapq.heappush(self.lo, -num)

        # Balancing step: move the max of `lo` into `hi`.
        heapq.heappush(self.hi, -heapq.heappop(self.lo))

        # Rebalance: `lo` should have equal or one more element than `hi`.
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    # Returns the median of current data stream.
    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) * 0.5
