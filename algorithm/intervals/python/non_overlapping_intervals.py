"""
Non-overlapping Intervals
https://leetcode.com/problems/non-overlapping-intervals

Given an array of intervals where intervals[i] = [start_i, end_i], return the
minimum number of intervals you need to remove to make the rest of the
intervals non-overlapping.

Approaches:
1. Greedy after sorting by (start, end) - Time: O(n log n), Space: O(1)
"""

from typing import List


# Time: O(n log n), Space: O(1)
# Greedy
def eraseOverlapIntervals(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0

    # Custom comparator: sort by start, then by end
    intervals.sort(key=lambda x: (x[0], x[1]))

    n = len(intervals)
    res = 0

    curr = intervals[0]
    for i in range(1, n):
        # Overlapping
        if intervals[i][0] < curr[1]:
            if intervals[i][1] < curr[1]:
                curr = intervals[i]
            res += 1
            continue

        curr = intervals[i]

    return res


if __name__ == "__main__":
    intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
    res = eraseOverlapIntervals(intervals)
    assert res == 1

    intervals = [[1, 2], [1, 2], [1, 2]]
    res = eraseOverlapIntervals(intervals)
    assert res == 2

    intervals = [[1, 2], [2, 3]]
    res = eraseOverlapIntervals(intervals)
    assert res == 0
