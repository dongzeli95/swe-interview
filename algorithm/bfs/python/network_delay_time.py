"""
Network Delay Time
https://leetcode.com/problems/network-delay-time/

Approaches:
1. Dijkstra with min-heap priority queue.
   Time: O(N + E log N), Space: O(N + E)
"""

import heapq
from collections import defaultdict
from typing import List


def networkDelayTime(times: List[List[int]], n: int, k: int) -> int:
    if n <= 1:
        return 0

    # Construct a graph
    graph = defaultdict(list)
    for s, d, t in times:
        graph[s].append((d, t))

    min_dist = {}
    # Heap entries are (current best distance to node, node).
    # This mirrors the C++ custom comparator that orders nodes by minDist[node].
    pq = [(0, k)]
    min_dist[k] = 0

    while pq:
        curr_dist, curr = heapq.heappop(pq)

        # Stale entry: a better distance was already recorded.
        if curr_dist > min_dist[curr]:
            continue

        for d, t in graph[curr]:
            # Don't even explore if the distance is the same.
            if d in min_dist and min_dist[curr] + t >= min_dist[d]:
                continue
            min_dist[d] = min_dist[curr] + t
            heapq.heappush(pq, (min_dist[d], d))

    res = 0
    for i in range(1, n + 1):
        if i not in min_dist:
            return -1
        res = max(res, min_dist[i])

    return res


if __name__ == "__main__":
    times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    assert networkDelayTime(times, 4, 2) == 2

    times = [[1, 2, 1]]
    assert networkDelayTime(times, 2, 1) == 1

    times = [[1, 2, 1]]
    assert networkDelayTime(times, 2, 2) == -1

    print("All tests passed.")
