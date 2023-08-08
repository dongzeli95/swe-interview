// https://leetcode.com/problems/non-overlapping-intervals

/* 
Given an array of intervals intervals where intervals[i] = [starti, endi], return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

Ex1:
Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
Output: 1
Explanation: [1,3] can be removed and the rest of the intervals are non-overlapping.

Ex2:
Input: intervals = [[1,2],[1,2],[1,2]]
Output: 2
Explanation: You need to remove two [1,2] to make the rest of the intervals non-overlapping.

Ex3:
Input: intervals = [[1,2],[2,3]]
Output: 0
Explanation: You don't need to remove any of the intervals since they're already non-overlapping.
*/

// [1, 2], [1, 3], [2, 3], [3, 4]

#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>

using namespace std;

// Time: O(nlogn), Space: O(1)
// Greedy
int eraseOverlapIntervals(vector<vector<int>>& intervals) {
    if (intervals.empty()) {
        return 0;
    }

    // Custom comparator
    sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) {
        if (a[0] == b[0]) {
            return a[1] < b[1];
        }
        return a[0] < b[0];
    });

    int n = intervals.size();
    int res = 0;

    vector<int> curr = intervals[0];
    for (int i = 1; i < n; i++) {
        // Overlapping
        if (intervals[i][0] < curr[1]) {
            if (intervals[i][1] < curr[1]) {
                curr = intervals[i];
            }
            res++;
            continue;
        }

        curr = intervals[i];
    }

    return res;
}

int main() {
    vector<vector<int>> intervals = {{1, 2}, {2, 3}, {3, 4}, {1, 3}};
    int res = eraseOverlapIntervals(intervals);
    assert(res == 1);

    intervals = {{1, 2}, {1, 2}, {1, 2}};
    res = eraseOverlapIntervals(intervals);
    assert(res == 2);

    intervals = {{1, 2}, {2, 3}};
    res = eraseOverlapIntervals(intervals);
    assert(res == 0);
}