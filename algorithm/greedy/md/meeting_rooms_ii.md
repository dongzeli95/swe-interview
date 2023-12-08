```cpp
// https://leetcode.com/problems/meeting-rooms-ii/

/*
Given an array of meeting time intervals intervals where intervals[i] = [starti, endi], 
return the minimum number of conference rooms required.

Ex1:
Input: intervals = [[0,30],[5,10],[15,20]]
Output: 2

Ex2:
Input: intervals = [[7,10],[2,4]]
Output: 1

*/

// [[1, 13], [13, 15]]
#include <vector>
#include <iostream>

using namespace std;

// Time: O(nlogn), Space: O(n)
int minMeetingRooms(vector<vector<int>>& intervals) {
    if (intervals.empty()) {
        return 0;
    }

    vector<vector<int>> points;
    int n = intervals.size();
    for (int i = 0; i < n; i++) {
        points.push_back({intervals[i][0], 1});
        points.push_back({intervals[i][1], -1});
    }

    auto cmp = [](vector<int>& v1, vector<int>& v2) {
        if (v1[0] == v2[0]) {
            return v1[1] < v2[1];
        }
        return v1[0] < v2[0];
    };

    sort(points.begin(), points.end(), cmp);

    int occupiedRoom = 0;
    int res = 0;
    for (int i = 0; i < points.size(); i++) {
        occupiedRoom += points[i][1];
        res = max(res, occupiedRoom);
    }

    return res;
}

int main() {
    vector<vector<int>> intervals1 {{0, 30}, {5, 10}, {15, 20}};
    cout << minMeetingRooms(intervals1) << endl;

    vector<vector<int>> intervals2{ {7, 10}, {2, 4}};
    cout << minMeetingRooms(intervals2) << endl;

    return 0;
}```
