"""
Minimum Number of Arrows to Burst Balloons
https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons

Approaches:
1. findMinArrowShots: sort by start (tie-break by end), sweep and keep the
   running intersection of overlapping intervals.
   Time: O(n log n), Space: O(1).
"""

from typing import List


# Time: O(nlogn), Space: O(1)
def findMinArrowShots(points: List[List[int]]) -> int:
    if not points:
        return 0

    # O(nlogn) — sort by start, tie-break by end.
    points.sort(key=lambda p: (p[0], p[1]))

    res = 1
    n = len(points)

    curr = list(points[0])
    for i in range(1, n):
        # take intersections of two-overlapping intervals.
        if points[i][0] <= curr[1]:
            curr[0] = max(points[i][0], curr[0])
            curr[1] = min(points[i][1], curr[1])
            continue

        curr = list(points[i])
        res += 1

    return res


if __name__ == "__main__":
    points = [[10, 16], [2, 8], [1, 6], [7, 12]]
    res = findMinArrowShots(points)
    assert res == 2, res

    points = [[1, 2], [3, 4], [5, 6], [7, 8]]
    res = findMinArrowShots(points)
    assert res == 4, res

    points = [[1, 2], [2, 3], [3, 4], [4, 5]]
    res = findMinArrowShots(points)
    assert res == 2, res
