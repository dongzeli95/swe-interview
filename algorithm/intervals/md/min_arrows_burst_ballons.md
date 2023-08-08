```cpp
// https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons

/* 
There are some spherical balloons taped onto a flat wall that represents the XY-plane. 
The balloons are represented as a 2D integer array points where points[i] = [xstart, xend] denotes a balloon whose horizontal diameter stretches between xstart and xend. 
You do not know the exact y-coordinates of the balloons.

Arrows can be shot up directly vertically (in the positive y-direction) from different points along the x-axis. 
A balloon with xstart and xend is burst by an arrow shot at x if xstart <= x <= xend. 
There is no limit to the number of arrows that can be shot. A shot arrow keeps traveling up infinitely, bursting any balloons in its path.

Given the array points, return the minimum number of arrows that must be shot to burst all balloons.

Ex1:
Input: points = [[10,16],[2,8],[1,6],[7,12]]
Output: 2
Explanation: The balloons can be burst by 2 arrows:
- Shoot an arrow at x = 6, bursting the balloons [2,8] and [1,6].
- Shoot an arrow at x = 11, bursting the balloons [10,16] and [7,12].

Ex2:
Input: points = [[1,2],[3,4],[5,6],[7,8]]
Output: 4
Explanation: One arrow needs to be shot for each balloon for a total of 4 arrows.

Ex3:
Input: points = [[1,2],[2,3],[3,4],[4,5]]
Output: 2
Explanation: The balloons can be burst by 2 arrows:
- Shoot an arrow at x = 2, bursting the balloons [1,2] and [2,3].
- Shoot an arrow at x = 4, bursting the balloons [3,4] and [4,5].

*/

#include <vector>
#include <iostream>
#include <cassert>

using namespace std;

// Time: O(nlogn), Space: O(1)
int findMinArrowShots(vector<vector<int>>& points) {
    if (points.empty()) {
        return 0;
    }

    // O(nlogn)
    sort(points.begin(), points.end(), [](vector<int>& a, vector<int>& b) {
        if (a[0] == b[0]) {
            return a[1] < b[1];
        }

        return a[0] < b[0];
    });

    int res = 1;
    int n = points.size();

    vector<int> curr = points[0];
    for (int i = 1; i < n; i++) {
        // take intersections of two-overlapping intervals.
        if (points[i][0] <= curr[1]) {
            curr[0] = max(points[i][0], curr[0]);
            curr[1] = min(points[i][1], curr[1]);
            continue;
        }

        curr = points[i];
        res++;
    }

    return res;
}

int main() {
    vector<vector<int>> points = { {10,16},{2,8},{1,6},{7,12} };
    int res = findMinArrowShots(points);
    assert(res == 2);

    points = { {1,2},{3,4},{5,6},{7,8} };
    res = findMinArrowShots(points);
    assert(res == 4);

    points = { {1,2},{2,3},{3,4},{4,5} };
    res = findMinArrowShots(points);
    assert(res == 2);
}```
