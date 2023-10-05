```cpp
// https://leetcode.com/problems/meeting-rooms-iii/

/*
You are given an integer n. There are n rooms numbered from 0 to n - 1.
You are given a 2D integer array meetings where meetings[i] = [starti, endi] means that a meeting will be held during the half-closed time interval [starti, endi). All the values of starti are unique.
Meetings are allocated to rooms in the following manner:

Each meeting will take place in the unused room with the lowest number.
If there are no available rooms, the meeting will be delayed until a room becomes free. The delayed meeting should have the same duration as the original meeting.
When a room becomes unused, meetings that have an earlier original start time should be given the room.
Return the number of the room that held the most meetings. If there are multiple rooms, return the room with the lowest number.

A half-closed interval [a, b) is the interval between a and b including a and not including b.

Ex1:
Input: n = 2, meetings = [[0,10],[1,5],[2,7],[3,4]]
Output: 0
Explanation:
- At time 0, both rooms are not being used. The first meeting starts in room 0.
- At time 1, only room 1 is not being used. The second meeting starts in room 1.
- At time 2, both rooms are being used. The third meeting is delayed.
- At time 3, both rooms are being used. The fourth meeting is delayed.
- At time 5, the meeting in room 1 finishes. The third meeting starts in room 1 for the time period [5,10).
- At time 10, the meetings in both rooms finish. The fourth meeting starts in room 0 for the time period [10,11).
Both rooms 0 and 1 held 2 meetings, so we return 0.

Ex2:
Input: n = 3, meetings = [[1,20],[2,10],[3,5],[4,9],[6,8]]
Output: 1
Explanation:
- At time 1, all three rooms are not being used. The first meeting starts in room 0.
- At time 2, rooms 1 and 2 are not being used. The second meeting starts in room 1.
- At time 3, only room 2 is not being used. The third meeting starts in room 2.
- At time 4, all three rooms are being used. The fourth meeting is delayed.
- At time 5, the meeting in room 2 finishes. The fourth meeting starts in room 2 for the time period [5,10).
- At time 6, all three rooms are being used. The fifth meeting is delayed.
- At time 10, the meetings in rooms 1 and 2 finish. The fifth meeting starts in room 1 for the time period [10,12).
Room 0 held 1 meeting while rooms 1 and 2 each held 2 meetings, so we return 1.
*/

// [0, 0, 0] -> [0, 10, 1] -> [0, 11, 2]
// [1, 0, 0] -> [1, 5, 1] -> [1, 10, 2]

#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <cassert>

using namespace std;

class Room {
public:
    Room(int i) {
        idx = i;
        endTime = 0;
    }

    int idx;
    long long endTime;
};

// Time: O(nlogn), Space: O(n)
int mostBooked(int n, vector<vector<int>>& meetings) {
    if (meetings.empty() || n == 0) {
        return 0;
    }

    sort(meetings.begin(), meetings.end(), [](const vector<int>& m1, const vector<int>& m2) {
        return m1[0] < m2[0];
    });

    auto occupiedRoomCmp = [](Room a, Room b) {
        if (a.endTime == b.endTime) {
            return a.idx > b.idx;
        }

        return a.endTime > b.endTime;
    };

    auto unusedRoomCmp = [](Room a, Room b) {
        return a.idx > b.idx;
    };

    priority_queue<Room, vector<Room>, decltype(occupiedRoomCmp)> occupiedRoomPQ(occupiedRoomCmp);
    priority_queue<Room, vector<Room>, decltype(unusedRoomCmp)> unusedRoomPQ(unusedRoomCmp);
    unordered_map<int, int> meetingsHeld;

    for (int i = 0; i < n; i++) {
        Room r = Room(i);
        unusedRoomPQ.push(r);
    }

    int m = meetings.size();
    for (int i = 0; i < m; i++) {
        int meetingStartTime = meetings[i][0];
        int meetingEndTime = meetings[i][1];
        int meetingDuration = meetings[i][1] - meetings[i][0];
        // Move room from occupied room to unused room if previous meeting already ended.
        while (!occupiedRoomPQ.empty() && occupiedRoomPQ.top().endTime <= meetingStartTime) {
            Room curr = occupiedRoomPQ.top();
            occupiedRoomPQ.pop();
            unusedRoomPQ.push(curr);
        }

        Room curr = Room(-1);
        long long newEndTime = -1;
        // If we have empty room, use it.
        // Otherwise wait for occupied room to be released.
        if (unusedRoomPQ.size() > 0) {
            curr = unusedRoomPQ.top();
            unusedRoomPQ.pop();
            newEndTime = meetingEndTime;
        } else {
            curr = occupiedRoomPQ.top();
            occupiedRoomPQ.pop();
            newEndTime = curr.endTime + meetingDuration;
        }

        // Mark meeting room as occupied and update the meetings held for that room.
        meetingsHeld[curr.idx]++;
        curr.endTime = newEndTime;
        occupiedRoomPQ.push(curr);
    }

    int maxMeeting = 0;
    int res = -1;

    for (auto i : meetingsHeld) {
        int room = i.first;
        int meetings = i.second;
        if (meetings > maxMeeting) {
            res = room;
            maxMeeting = meetings;
        }
        else if (meetings == maxMeeting) {
            if (res == -1) res = room;
            else {
                res = min(res, room);
            }
        }
    }

    return res;
}

int main() {
    vector<vector<int>> meetings = {{0,10},{1,5},{2,7},{3,4}};
    assert(mostBooked(2, meetings) == 0);

    meetings = {{1,20},{2,10},{3,5},{4,9},{6,8}};
    assert(mostBooked(3, meetings) == 1);

    meetings = {{0, 10}, {1, 9}, {2, 8}, {3, 7}, {4, 6}};
    // [0, 0, 0] -> [0, 10, 1]
    // [1, 0, 0] -> [1, 9, 1]
    // [2, 0, 0] -> [2, 8, 1] -> [2, 12, 2]
    assert(mostBooked(3, meetings) == 1);

    /* 
     Why we use a separate PQ for unused rooms, if we only use one PQ, 
     for all rooms, we greedily return the room with earliest ending meeting, it will cause problem.

     Because for the following, case when we try to schedule meeting [18, 19)
     we have room 0, 1, and 2 both satisfy.

     In this case, greedy approach will make us use room 2.
     but in fact, we want to use room 0 because it has the smallest idx.
     REMEMBER our first requirement: Each meeting will take place in the unused room with the lowest number.
    */
    meetings = {{18, 19}, {3, 12}, {17, 19}, {2, 13}, {7, 10}};
    assert(mostBooked(4, meetings) == 0);
    // [0, 0, 0] -> [0, 13, 1]
    // [1, 0, 0] -> [1, 12, 1]
    // [2, 0, 0] -> [2, 10, 1]
    // [3, 0, 0] -> [3, 19, 1]
    return 0;
}```
