"""
K Closest Points to Origin
https://leetcode.com/problems/k-closest-points-to-origin/

Given an array of points where points[i] = [xi, yi] represents a point on the
X-Y plane and an integer k, return the k closest points to the origin (0, 0).

Approaches:
    1. kClosest (Max-heap of size k):
       Time: O(n log k), Space: O(k)
    2. kClosestWithQuickSelect (Quickselect):
       Time: amortized O(n), worst O(n^2), Space: O(1)
"""

import math
import random
from heapq import heappush, heappop


def calc(v):
    diff1 = abs(v[0])
    diff2 = abs(v[1])
    return math.sqrt(diff1 * diff1 + diff2 * diff2)


# Time: O(n log k), Space: O(k)
def kClosest(points, k):
    if not points:
        return []

    # Python heapq is a min-heap; to emulate a max-heap of size k we push the
    # negated distance so the largest distance is at the top and gets popped
    # when the heap exceeds size k.
    pq = []  # entries: (-distance, index, point)
    for i, p in enumerate(points):
        heappush(pq, (-calc(p), i, p))
        if len(pq) > k:
            heappop(pq)

    res = []
    while pq:
        _, _, p = heappop(pq)
        res.append(p)
    return res


# Quick Select
# Since we are expected to reduce the number of elements to process by roughly
# half, the average time complexity T(n) satisfies T(n) = O(n) + T(n/2), which
# solves to T(n) = O(n). Worst case is O(n^2) when the pivot chosen is the
# smallest/largest element; probability shrinks exponentially with input size.
# Time: amortized O(n), Space: O(1)
def partitionPivot(points, left, right, pivot_idx):
    idx = left
    points[pivot_idx], points[right] = points[right], points[pivot_idx]
    for i in range(left, right):
        if calc(points[i]) < calc(points[right]):
            points[idx], points[i] = points[i], points[idx]
            idx += 1
    points[idx], points[right] = points[right], points[idx]
    return idx


def kClosestWithQuickSelect(points, k):
    if len(points) <= k:
        return points

    n = len(points)
    left, right = 0, n - 1
    while left <= right:
        pivot_idx = left + random.randint(0, right - left)
        new_pivot = partitionPivot(points, left, right, pivot_idx)
        if new_pivot == k - 1:
            return points[:k]
        elif new_pivot > k - 1:
            right = new_pivot - 1
        else:
            left = new_pivot + 1

    return []


if __name__ == "__main__":
    points = [[1, 3], [-2, 2]]
    res = kClosest(points, 1)
    for p in res:
        print(p[0], p[1])
    res = kClosestWithQuickSelect(points, 1)
    for p in res:
        print(p[0], p[1])

    points = [[3, 3], [5, -1], [-2, 4]]
    res = kClosest(points, 2)
    for p in res:
        print(p[0], p[1])
    res = kClosestWithQuickSelect(points, 2)
    for p in res:
        print(p[0], p[1])

    points2 = [[1, 3], [-2, 2], [2, -2]]
    res2 = kClosestWithQuickSelect(points2, 2)
    for p in res2:
        print(p[0], p[1])
