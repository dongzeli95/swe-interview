"""
Meeting Rooms II
https://leetcode.com/problems/meeting-rooms-ii/

Given an array of meeting time intervals intervals where
intervals[i] = [start_i, end_i], return the minimum number of
conference rooms required.

Approaches:
    1. Sweep line on (time, delta) events. Sort events; when times tie,
       process end (-1) before start (+1) so back-to-back meetings share
       a room. Track the running count of occupied rooms and return the
       max seen.
       Time: O(n log n), Space: O(n)
"""

from typing import List


# Time: O(n log n), Space: O(n)
def minMeetingRooms(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0

    points = []
    for start, end in intervals:
        points.append((start, 1))
        points.append((end, -1))

    # If two points share the same time, process the end (-1) before the
    # start (+1). Since -1 < 1, ordinary tuple sorting achieves this.
    points.sort(key=lambda p: (p[0], p[1]))

    occupied_room = 0
    res = 0
    for _, delta in points:
        occupied_room += delta
        res = max(res, occupied_room)

    return res


if __name__ == "__main__":
    intervals1 = [[0, 30], [5, 10], [15, 20]]
    print(minMeetingRooms(intervals1))

    intervals2 = [[7, 10], [2, 4]]
    print(minMeetingRooms(intervals2))
