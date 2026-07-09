"""
Number of Flowers in Full Bloom
https://leetcode.com/problems/number-of-flowers-in-full-bloom/

Approaches:
1. fullBloomFlowers: Sort flowers by start, sort people, sweep people in order
   while pushing flower end times into a min-heap and popping those that ended
   before the current person. Cache count per unique person time, then map back
   to original order.
   Time: O(n log n + m * (log n + log m)), Space: O(n + m)
"""

import heapq
from typing import List


# Time: O(nlogn + m*(logn+logm)), Space: O(n+m)
def fullBloomFlowers(flowers: List[List[int]], people: List[int]) -> List[int]:
    sortedPeople = sorted(people)

    flowers.sort()
    dic = {}
    heap: List[int] = []

    i = 0
    for person in sortedPeople:
        while i < len(flowers) and flowers[i][0] <= person:
            heapq.heappush(heap, flowers[i][1])
            i += 1

        while heap and heap[0] < person:
            heapq.heappop(heap)

        dic[person] = len(heap)

    ans = [dic[person] for person in people]
    return ans
