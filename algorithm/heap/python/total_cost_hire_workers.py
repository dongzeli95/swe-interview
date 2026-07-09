"""
LeetCode: Total Cost to Hire K Workers
https://leetcode.com/problems/total-cost-to-hire-k-workers

Approaches:
1. Single min-heap with (cost, index) tuples over the two candidate windows.
   Time: O((candidates + k) * log(candidates)), Space: O(candidates)
"""

import heapq
from typing import List


# C is candidates size, K is the number of workers to hire
# Time complexity: O((C+K)*logC), Space complexity: O(C)
def totalCost(costs: List[int], k: int, candidates: int) -> int:
    if not costs:
        return 0

    n = len(costs)

    # Min-heap of (cost, index). Python tuple comparison naturally breaks ties
    # by smallest index, matching the C++ custom comparator.
    pq: List[tuple] = []

    for i in range(candidates):
        heapq.heappush(pq, (costs[i], i))

    # The boundary is important.
    # candidates size can be larger than n/2
    boundary = max(n - candidates - 1, candidates - 1)
    for i in range(n - 1, boundary, -1):
        heapq.heappush(pq, (costs[i], i))

    l = candidates
    r = boundary

    res = 0
    for _ in range(k):
        cost, idx = heapq.heappop(pq)
        res += cost

        if l > r:
            continue
        if idx < l:
            heapq.heappush(pq, (costs[l], l))
            l += 1
        elif idx > r:
            heapq.heappush(pq, (costs[r], r))
            r -= 1

    return res


if __name__ == "__main__":
    costs = [17, 12, 10, 2, 7, 2, 11, 20, 8]
    k = 3
    candidates = 4
    res = totalCost(costs, k, candidates)
    assert res == 11, res

    costs = [1, 2, 4, 1]
    k = 3
    candidates = 3
    res = totalCost(costs, k, candidates)
    assert res == 4, res

    costs = [18, 64, 12, 21, 21, 78, 36, 58, 88, 58, 99, 26, 92, 91, 53,
             10, 24, 25, 20, 92, 73, 63, 51, 65, 87, 6, 17, 32, 14, 42,
             46, 65, 43, 9, 75]
    k = 13
    candidates = 23
    res = totalCost(costs, k, candidates)
    assert res == 223, res

    costs = [69, 10, 63, 24, 1, 71, 55, 46, 4, 61, 78, 21, 85, 52, 83,
             77, 42, 21, 73, 2, 80, 99, 98, 89, 55, 94, 63, 50, 43, 62, 14]
    candidates = 31
    k = 21
    res = totalCost(costs, k, candidates)
    assert res == 829, res

    print("All tests passed!")
